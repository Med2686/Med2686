"""Search + download free, high-quality sound effects into the skill library, with QC and features for matching.

Sources (all free for commercial social use):
  mixkit    Mixkit Sound Effects Free License — real WAV files, no attribution.   https://mixkit.co/free-sound-effects/
  freesound Freesound, CC0 only (filter enforced + checked per result) — HQ previews (~128 kbps mp3).   https://freesound.org
  uisfx     uisfx.com packs on GitHub, CC0 (procedural UI sounds).                 https://github.com/romainsimon/uisfx
Big packs (Sonniss GDC, Kenney, OpenGameArt...) live in ../sfx/packs and are indexed by sfx_packs.py, not here.

usage:
  python sfx_fetch.py mixkit whoosh swoosh transition --pages 3
  python sfx_fetch.py mixkit-all [--recrawl] [--part 1/2]   # the COMPLETE Mixkit catalogue (every category, every page; reruns retry failed pages)
  python sfx_fetch.py freesound "whoosh" "sub boom" --n 20 [--pages 3]
  python sfx_fetch.py freesound-file queries.txt --n 20 [--part 1/2]   # one query per line; --part splits it between 2 runs
  python sfx_fetch.py dedupe                    # merge sounds fetched twice (keeps one file, merges tags)
  python sfx_fetch.py freesound-verify          # re-check Freesound sounds against their page tags, drop unrelated ones
  python sfx_fetch.py uisfx
  python sfx_fetch.py categories                # list Mixkit categories
  python sfx_fetch.py flag                      # re-apply the "glass" exclusion flags to the index
Run with the claude-video venv: ~/.venvs/claude-video/Scripts/python.exe  (it lowers its own priority to below-normal)
Files land in ../sfx/library/<source>/<id>-<slug>.wav (44.1 kHz 24-bit, trimmed, peak -1 dBFS) and ../sfx/library/index.json.
QC rejects: clipped samples > 3, noise floor above -55 dB, bandwidth under 8 kHz (UI/whoosh sounds), duration > 12 s.
Mixkit sounds that fail QC (long ambiences, noisy beds) are kept untouched in ../sfx/packs/mixkit-long/<category>/ so the
catalogue stays complete. Every processed id (ok or rejected) is remembered in library/_seen.json, so reruns only fetch new sounds.
Anything named/tagged "glass" is kept on disk but flagged `excluded` in the index (the user hates the glass sound); sfx_match skips it.
Several fetchers can run at once: the index is saved by merging only the keys this process changed, under a lock file.
"""
import os, sys, re, json, time, subprocess, tempfile, urllib.request, urllib.parse, html as htmlmod
import numpy as np, soundfile as sf
sys.path.insert(0, os.path.dirname(__file__))
from sfx_feat import load_mono, trim, features, qc, SR

LIB = os.path.normpath(os.path.join(os.path.abspath(os.path.dirname(__file__)), "..", "sfx", "library"))
PACKS = os.path.normpath(os.path.join(os.path.abspath(os.path.dirname(__file__)), "..", "sfx", "packs"))
IDX = os.path.join(LIB, "index.json")
SEEN = os.path.join(LIB, "_seen.json")
UA = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126 Safari/537.36"}
EXCLUDE_WORDS = ("glass",)


def lowprio():
    """Below-normal priority for this process and the ffmpeg children it starts (Remotion renders share the CPU)."""
    try:
        import ctypes
        from ctypes import wintypes
        k32 = ctypes.WinDLL("kernel32", use_last_error=True)
        k32.GetCurrentProcess.restype = wintypes.HANDLE
        k32.SetPriorityClass.argtypes = [wintypes.HANDLE, wintypes.DWORD]
        k32.SetPriorityClass(k32.GetCurrentProcess(), 0x00004000)  # BELOW_NORMAL, inherited by ffmpeg / pool workers
    except Exception:
        try: os.nice(10)
        except Exception: pass


def get(url, binary=False, tries=3):
    for i in range(tries):
        try:
            req = urllib.request.Request(url, headers=UA)
            with urllib.request.urlopen(req, timeout=60) as r:
                data = r.read()
            return data if binary else data.decode("utf-8", "replace")
        except urllib.error.HTTPError as e:
            if e.code in (404, 403, 410) or i == tries - 1: raise
            if e.code == 429:  # rate limited: wait as asked (or 45 s, 90 s...)
                ra = e.headers.get("Retry-After", "")
                time.sleep(int(ra) if ra.isdigit() else 45 * (i + 1)); continue
        except Exception:
            if i == tries - 1: raise
        time.sleep(3 * (i + 1))


def slug(s):
    return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")[:60]


# ---------- index with merge-on-save (safe with parallel fetchers) ----------
class Index(dict):
    def __init__(self, path):
        self.path = path
        super().__init__(json.load(open(path, encoding="utf-8")) if os.path.exists(path) else {})
        self.dirty = set()

    def __setitem__(self, k, v):
        super().__setitem__(k, v); self.dirty.add(k)

    def save(self):
        lock = self.path + ".lock"
        for _ in range(1200):
            try:
                os.close(os.open(lock, os.O_CREAT | os.O_EXCL | os.O_WRONLY)); break
            except FileExistsError:
                try:
                    if time.time() - os.path.getmtime(lock) > 180: os.remove(lock)
                except OSError: pass
                time.sleep(0.1)
        try:
            disk = json.load(open(self.path, encoding="utf-8")) if os.path.exists(self.path) else {}
            for k in self.dirty: disk[k] = dict.__getitem__(self, k)
            for k, v in disk.items():
                if k not in self: dict.__setitem__(self, k, v)
            if self.path == IDX: flag_excluded(disk)
            os.makedirs(os.path.dirname(self.path), exist_ok=True)
            tmp = self.path + f".{os.getpid()}.tmp"
            json.dump(disk, open(tmp, "w", encoding="utf-8"), indent=1, ensure_ascii=False)
            for i in range(50):
                try: os.replace(tmp, self.path); break
                except PermissionError: time.sleep(0.2)
            self.dirty.clear()
        finally:
            try: os.remove(lock)
            except OSError: pass


def is_excluded(m):
    txt = " ".join(str(m.get(f, "")) for f in ("title", "category", "file", "id")) + " " + " ".join(m.get("tags", []))
    return next((w for w in EXCLUDE_WORDS if w in txt.lower()), None)


def flag_excluded(ix):
    for k, m in ix.items():
        w = is_excluded(m)
        if w: m["excluded"] = f"{w} (the user hates the glass sound; file kept, never suggested)"
        elif "excluded" in m and m["excluded"].startswith("glass"): m.pop("excluded")
    return ix


def load_index():
    return Index(IDX)


def save_index(ix):
    ix.save()


def ingest(raw_bytes, ext, key, meta, ix, strict=True):
    """Decode, trim, QC, normalise, write wav, add features to the index."""
    with tempfile.TemporaryDirectory(ignore_cleanup_errors=True) as td:
        src = os.path.join(td, "in" + ext); open(src, "wb").write(raw_bytes)
        wav = os.path.join(td, "out.wav")
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", src, "-ar", str(SR), "-ac", "2", wav], check=True)
        y2, _ = sf.read(wav, always_2d=True)
    mono = y2.mean(1)
    q = qc(mono)
    t = trim(mono)
    if len(t) == 0: return "empty"
    dur = len(t) / SR
    reasons = []
    if q["clipped"] > 3: reasons.append("clipped")
    if q["floor_db"] > -55 and dur > 0.6: reasons.append(f"noise floor {q['floor_db']}")
    if strict and q["bandwidth_hz"] < 8000: reasons.append(f"bandwidth {q['bandwidth_hz']}")
    if dur > 12: reasons.append("too long")
    if reasons: return "rejected: " + ", ".join(reasons)
    # trim the stereo file with the same bounds as the mono trim
    s = int(np.argmax(np.abs(mono) > np.max(np.abs(mono)) * 10 ** (-50 / 20)))
    y = y2[max(0, s - int(0.003 * SR)): max(0, s - int(0.003 * SR)) + len(t)]
    y = y / (np.max(np.abs(y)) + 1e-9) * 10 ** (-1 / 20)
    fade = min(len(y), int(0.02 * SR)); y[-fade:] *= np.linspace(1, 0, fade)[:, None]
    d = os.path.join(LIB, meta["source"]); os.makedirs(d, exist_ok=True)
    path = os.path.join(d, f"{key}.wav")
    sf.write(path, y, SR, subtype="PCM_24")
    vec, info = features(y.mean(1))
    entry = {**meta, **info, **q, "file": os.path.relpath(path, LIB).replace("\\", "/"), "vec": [round(float(v), 4) for v in vec]}
    w = is_excluded(entry)
    if w: entry["excluded"] = f"{w} (the user hates the glass sound; file kept, never suggested)"
    ix[f"{meta['source']}/{key}"] = entry
    return "ok"


# ---------- Mixkit ----------
def mixkit_items(html):
    return re.findall(r'active_storage/sfx/(\d+)/\1-preview\.mp3.*?item-grid-card__title">\s*([^<]+?)\s*<', html, re.S)


def mixkit_categories():
    return sorted(set(re.findall(r'href="/free-sound-effects/([a-z0-9-]+)/"', get("https://mixkit.co/free-sound-effects/whoosh/"))))


def mixkit_download(sid):
    try:
        return get(f"https://assets.mixkit.co/active_storage/sfx/{sid}/{sid}.wav", binary=True), ".wav"
    except Exception:
        return get(f"https://assets.mixkit.co/active_storage/sfx/{sid}/{sid}-preview.mp3", binary=True), ".mp3"


def mixkit_one(sid, title, cat, cats, ix, seen, page):
    key = f"mixkit-{sid}-{slug(title)}"
    raw, ext = mixkit_download(sid)
    url = f"https://assets.mixkit.co/active_storage/sfx/{sid}/{sid}{'.wav' if ext == '.wav' else '-preview.mp3'}"
    meta = {"source": "mixkit", "id": sid, "title": htmlmod.unescape(title), "category": cat, "tags": cats,
            "license": "Mixkit Sound Effects Free License", "page": page, "url": url}
    r = ingest(raw, ext, key, meta, ix)
    if r != "ok":  # keep the original in the long/ambient pack so the catalogue is complete
        d = os.path.join(PACKS, "mixkit-long", cat); os.makedirs(d, exist_ok=True)
        open(os.path.join(d, f"{key}{ext}"), "wb").write(raw)
        r += " -> packs/mixkit-long"
    seen[f"mixkit:{sid}"] = {"result": r, "title": meta["title"], "category": cat, "tags": cats, "url": url}
    return r


def mixkit(cats, pages=2):
    ix, seen = load_index(), Index(SEEN)
    have = {m["id"] for m in ix.values() if m["source"] == "mixkit"}
    for cat in cats:
        for p in range(1, pages + 1):
            url = f"https://mixkit.co/free-sound-effects/{cat}/" + (f"?page={p}" if p > 1 else "")
            try:
                h = get(url)
            except Exception as e:
                print("page fail", url, e); break
            items = mixkit_items(h)
            if not items: break
            for sid, title in items:
                if sid in have or f"mixkit:{sid}" in seen: continue
                try:
                    r = mixkit_one(sid, title, cat, [cat], ix, seen, url)
                except Exception as e:
                    print("dl fail", sid, e); continue
                have.add(sid)
                print(f"[mixkit/{cat}] {sid} {title}: {r}", flush=True)
                time.sleep(0.4)
            save_index(ix); seen.save()


def mixkit_all(recrawl=False, part=None):
    """Crawl every category page into packs/mixkit-long/../mixkit-catalog.json, then fetch every sound not processed yet."""
    os.makedirs(PACKS, exist_ok=True)
    catpath = os.path.join(PACKS, "mixkit-catalog.json")
    cat_ix = json.load(open(catpath, encoding="utf-8")) if os.path.exists(catpath) else {}
    if not cat_ix.get("_complete") or cat_ix.get("_failed") or recrawl:
        cats = mixkit_categories() if (recrawl or not cat_ix.get("_complete")) else cat_ix["_failed"]
        print(len(cats), "categories", flush=True)
        failed = []
        for cat in cats:
            for p in range(1, 40):
                url = f"https://mixkit.co/free-sound-effects/{cat}/" + (f"?page={p}" if p > 1 else "")
                try:
                    h = get(url, tries=4)
                except Exception as e:
                    print("page fail", url, e); failed.append(cat); break
                items = mixkit_items(h)
                if not items: break
                for sid, title in items:
                    e = cat_ix.setdefault(sid, {"title": htmlmod.unescape(title), "cats": [], "page": url})
                    if cat not in e["cats"]: e["cats"].append(cat)
                if f"?page={p + 1}" not in h: break
                time.sleep(0.6)
            print(f"[catalog] {cat}: total {len([k for k in cat_ix if not k.startswith('_')])}", flush=True)
            time.sleep(0.6)
        cat_ix["_complete"] = time.strftime("%Y-%m-%d")
        cat_ix["_failed"] = failed
        json.dump(cat_ix, open(catpath, "w", encoding="utf-8"), indent=1, ensure_ascii=False)
    ix, seen = load_index(), Index(SEEN)
    by_id = {m["id"]: k for k, m in ix.items() if m["source"] == "mixkit"}
    todo = 0
    for sid, e in cat_ix.items():
        if sid.startswith("_"): continue
        if sid in by_id:  # already in the library: just record every category it belongs to
            m = dict.__getitem__(ix, by_id[sid])
            tags = sorted(set(m.get("tags", [m.get("category")])) | set(e["cats"]))
            if tags != m.get("tags"): m["tags"] = tags; ix[by_id[sid]] = m
            continue
        if f"mixkit:{sid}" in seen: continue
        if part and int(sid) % part[1] != part[0] - 1: continue  # --part i/k: parallel fetchers split the ids
        try:
            r = mixkit_one(sid, e["title"], e["cats"][0], e["cats"], ix, seen, e["page"])
        except Exception as ex:
            print("dl fail", sid, ex, flush=True); continue
        todo += 1
        print(f"[mixkit/{e['cats'][0]}] {sid} {e['title']}: {r}", flush=True)
        if todo % 25 == 0: save_index(ix); seen.save()
        time.sleep(0.3)
    save_index(ix); seen.save()
    print("MIXKIT_ALL_DONE", todo, "new", flush=True)


# ---------- Freesound (CC0 only) ----------
def freesound_results(h):
    """Parse result cards: id, user, title, duration, downloads, rating, preview, cc0?"""
    out = []
    parts = h.split('class="bw-player"')[1:]
    for part in parts:
        g = lambda a: (re.search(a + r'="([^"]*)"', part) or [None, ""])[1]
        sid = g("data-sound-id")
        if not sid: continue
        rating = re.search(r'Average rating of ([\d.]+)', part)
        tags = [urllib.parse.unquote(t).lower() for t in re.findall(r'href="/browse/tags/([^/"]+)/"', part)]
        out.append({"id": sid, "user": g("data-username"), "title": htmlmod.unescape(g("data-title")), "tags": tags,
                    "dur": float(g("data-duration") or 0), "downloads": int(g("data-num-downloads") or 0),
                    "rating": float(rating.group(1)) if rating else 0.0, "mp3": g("data-mp3"),
                    "cc0": 'title="License: Creative Commons 0"' in part})
    return out


SYN = {"whoosh": ("whoosh", "woosh", "swoosh", "swish", "whoom"), "woosh": ("whoosh", "woosh", "swoosh", "swish"),
       "swoosh": ("swoosh", "whoosh", "woosh", "swish"), "swish": ("swish", "swoosh", "whoosh", "woosh"),
       "riser": ("riser", "rise", "uplifter", "build up", "buildup"), "downlifter": ("downlifter", "down lifter", "drop", "fall"),
       "ui": ("ui", "interface", "gui", "menu", "button"), "typing": ("typing", "keyboard", "type", "keys"),
       "boom": ("boom", "bass", "impact", "explosion"), "hit": ("hit", "impact", "punch", "thud"), "braam": ("braam", "brass", "horn"),
       "applause": ("applause", "clapping", "clap"), "laugh": ("laugh", "laughter", "laughing"), "magic": ("magic", "spell", "magical"),
       "transition": ("transition", "whoosh", "swoosh", "sweep"), "notification": ("notification", "alert", "ping", "message")}


def relevance(q, title, tags):
    """2 = every query word is in the title/tags, 1 = only the main (last) word, 0 = unrelated (e.g. "zoom" = Zoom H4n recorder)."""
    txt = (title + " " + " ".join(tags)).lower().replace("-", " ").replace("_", " ")
    stems = [w[:-1] if w.endswith("s") and len(w) > 3 else w for w in re.split(r"[^a-z0-9]+", q.lower()) if len(w) > 1]
    alt = lambda w: SYN.get(w, (w,))
    has = lambda w: any(a in txt for a in alt(w))
    if "zoom h" in txt or "zoom h4" in txt: txt = txt.replace("zoom h", "recorder h")  # Zoom H4n/H5/H6 recorders
    if not stems or q.lower() in txt or all(has(w) for w in stems): return 2
    return 1 if len(stems[-1]) > 3 and has(stems[-1]) else 0


def freesound_verify():
    """Re-check Freesound sounds against their real tags (sound page); drop the unrelated ones (file + index entry)."""
    ix, seen = load_index(), Index(SEEN)
    keys = [k for k, m in ix.items() if m["source"] == "freesound" and "downloads" in m and len(m.get("tags", [])) <= 1]
    print(len(keys), "to verify", flush=True)
    dropped = 0
    for k in keys:
        m = dict.__getitem__(ix, k)
        try:
            h = get(m["page"])
        except Exception as e:
            print("page fail", k, e); continue
        tags = [urllib.parse.unquote(t).lower() for t in re.findall(r'href="/browse/tags/([^/"]+)/"', h)]
        name = htmlmod.unescape((re.search(r"<title>([^<]+)</title>", h) or [None, m["title"]])[1])
        if m["category"] == "zoom" or relevance(m["category"], m["title"] + " " + name, tags) == 0:
            try: os.remove(os.path.join(LIB, m["file"]))
            except OSError: pass
            dict.__delitem__(ix, k); ix.dirty.discard(k); dropped += 1
            seen[f"freesound:{m['id']}"] = {"result": "dropped: unrelated to query", "query": m["category"]}
            print(f"[verify] drop {k}: {m['title'][:50]} tags={tags[:6]}", flush=True)
        else:
            m["tags"] = [m["category"]] + tags[:12]; ix[k] = m
        time.sleep(0.5)
    # save: rewrite the index without the dropped keys (merge would resurrect them)
    lock = IDX + ".lock"
    while True:
        try: os.close(os.open(lock, os.O_CREAT | os.O_EXCL | os.O_WRONLY)); break
        except FileExistsError: time.sleep(0.1)
    try:
        disk = json.load(open(IDX, encoding="utf-8"))
        for k in keys:
            if not dict.__contains__(ix, k): disk.pop(k, None)
            else: disk[k] = dict.__getitem__(ix, k)
        flag_excluded(disk)
        json.dump(disk, open(IDX + ".v.tmp", "w", encoding="utf-8"), indent=1, ensure_ascii=False); os.replace(IDX + ".v.tmp", IDX)
    finally:
        os.remove(lock)
    seen.save()
    print("VERIFY_DONE dropped", dropped, flush=True)


def _rewrite_index(update, drop):
    """Write the index under the lock: set `update` entries, delete `drop` keys (a merge-save would resurrect them)."""
    lock = IDX + ".lock"
    while True:
        try: os.close(os.open(lock, os.O_CREAT | os.O_EXCL | os.O_WRONLY)); break
        except FileExistsError: time.sleep(0.1)
    try:
        disk = json.load(open(IDX, encoding="utf-8"))
        for k in drop: disk.pop(k, None)
        disk.update(update); flag_excluded(disk)
        json.dump(disk, open(IDX + ".d.tmp", "w", encoding="utf-8"), indent=1, ensure_ascii=False); os.replace(IDX + ".d.tmp", IDX)
    finally:
        os.remove(lock)


def dedupe():
    """Same sound fetched twice (parallel runs / several queries): keep one entry, merge the tags, delete the extra files."""
    ix = load_index()
    groups = {}
    for k, m in ix.items():
        if m["source"] in ("freesound", "mixkit"): groups.setdefault((m["source"], m["id"]), []).append(k)
    update, drop = {}, []
    for (src, sid), ks in groups.items():
        if len(ks) < 2: continue
        ks.sort(key=lambda k: (-len(ix[k].get("tags", [])), k))
        keep = dict(ix[ks[0]])
        keep["tags"] = sorted(set(sum((ix[k].get("tags", [ix[k].get("category", "")]) + [ix[k].get("category", "")] for k in ks), [])) - {""})
        update[ks[0]] = keep
        for k in ks[1:]:
            if ix[k]["file"] != keep["file"]:
                try: os.remove(os.path.join(LIB, ix[k]["file"]))
                except OSError: pass
            drop.append(k)
    _rewrite_index(update, drop)
    print(f"dedupe: {len(drop)} duplicate entries removed, {len(update)} sounds kept with merged tags")


def freesound(queries, n=12, pages=2):
    ix, seen = load_index(), Index(SEEN)
    have = {m["id"] for m in ix.values() if m["source"] == "freesound"}
    for q in queries:
        done_q = 0
        if os.path.exists(IDX):  # pick up sounds another fetcher added meanwhile (parallel --part runs)
            try:
                disk = json.load(open(IDX, encoding="utf-8"))
                have |= {m["id"] for m in disk.values() if m["source"] == "freesound"}
                done_q = sum(1 for m in disk.values() if m["source"] == "freesound" and m.get("category") == q)
            except Exception: pass
        if done_q >= n: print(f"[freesound/{q}] already {done_q} in library", flush=True); continue
        cands = {}
        for sort in ("Automatic by relevance",):  # relevance first (downloads sort pulls in "Zoom H4n" recordings etc.)
            for p in range(1, pages + 1):
                url = "https://freesound.org/search/?" + urllib.parse.urlencode(
                    {"q": q, "f": 'license:"Creative Commons 0" duration:[0.05 TO 12]', "s": sort, "page": p})
                try:
                    res = freesound_results(get(url))
                except Exception as e:
                    print("search fail", q, e); break
                for r in res:
                    if r["cc0"]: cands.setdefault(r["id"], r)
                if len(res) < 15: break
                time.sleep(0.8)
        order = sorted([r for r in cands.values() if relevance(q, r["title"], r.get("tags", []))],
                       key=lambda r: (-relevance(q, r["title"], r.get("tags", [])), -(r["rating"] >= 3.5), -r["downloads"]))
        got = sum(1 for r in order if r["id"] in have)
        for r in order:
            if got >= n: break
            sid = r["id"]
            if sid in have or f"freesound:{sid}" in seen: continue
            key = f"freesound-{sid}-{slug(q)}"
            prev = r["mp3"].replace("-lq.mp3", "-hq.mp3")
            try:
                raw = get(prev, binary=True)
            except Exception as e:
                print("dl fail", sid, e); continue
            meta = {"source": "freesound", "id": sid, "title": f"{r['title']} ({r['user']})", "category": q, "tags": [q] + r.get("tags", [])[:12],
                    "license": "CC0 1.0", "page": f"https://freesound.org/people/{r['user']}/sounds/{sid}/", "url": prev,
                    "downloads": r["downloads"], "rating": r["rating"]}
            res = ingest(raw, ".mp3", key, meta, ix, strict=False)
            seen[f"freesound:{sid}"] = {"result": res, "query": q}
            print(f"[freesound/{q}] {sid} {r['title'][:40]} ({r['downloads']} dl): {res}", flush=True)
            if res == "ok": got += 1; have.add(sid)
            time.sleep(0.7)
        save_index(ix); seen.save()
        print(f"[freesound/{q}] {got} in library", flush=True)
    print("FREESOUND_DONE", flush=True)


def uisfx():
    ix = load_index()
    api = "https://api.github.com/repos/romainsimon/uisfx/git/trees/main?recursive=1"
    tree = json.loads(get(api))["tree"]
    for t in tree:
        p = t["path"]
        if not re.match(r"packages/uisfx/sounds/[^/]+/[^/]+\.(ogg|wav|mp3)$", p): continue
        pack, cue = p.split("/")[-2], os.path.splitext(p.split("/")[-1])[0]
        key = f"uisfx-{pack}-{cue}"
        if f"uisfx/{key}" in ix: continue
        raw = get("https://raw.githubusercontent.com/romainsimon/uisfx/main/" + p, binary=True)
        meta = {"source": "uisfx", "id": f"{pack}/{cue}", "title": f"{pack} {cue}", "category": pack, "license": "CC0 1.0",
                "page": "https://uisfx.com/", "url": "https://github.com/romainsimon/uisfx/blob/main/" + p}
        print(f"[uisfx] {pack}/{cue}: {ingest(raw, os.path.splitext(p)[1], key, meta, ix, strict=False)}", flush=True)
    save_index(ix)


def add_synth(folder):
    """Register synthesised sounds (sfx_synth.py outputs) as library candidates (source 'synth')."""
    import glob
    ix = load_index()
    for f in glob.glob(os.path.join(folder, "*.wav")):
        name = os.path.splitext(os.path.basename(f))[0]
        key = f"synth-{name}"
        meta = {"source": "synth", "id": name, "title": f"synth {name}", "category": "synth", "license": "own (procedural)", "page": "", "url": ""}
        print(f"[synth] {name}: {ingest(open(f, 'rb').read(), '.wav', key, meta, ix, strict=False)}")
    save_index(ix)


if __name__ == "__main__":
    lowprio()
    try: sys.stdout.reconfigure(encoding="utf-8", errors="replace"); sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception: pass
    cmd = sys.argv[1] if len(sys.argv) > 1 else "help"
    args = [a for a in sys.argv[2:] if not a.startswith("--")]
    opt = {sys.argv[i][2:]: sys.argv[i + 1] for i in range(2, len(sys.argv) - 1) if sys.argv[i].startswith("--")}
    args = [a for a in args if a not in opt.values()]
    if cmd == "mixkit": mixkit(args, int(opt.get("pages", 2)))
    elif cmd == "mixkit-all": mixkit_all("--recrawl" in sys.argv, tuple(map(int, opt["part"].split("/"))) if "part" in opt else None)
    elif cmd == "freesound": freesound(args, int(opt.get("n", 12)), int(opt.get("pages", 2)))
    elif cmd == "freesound-file":
        qs = [l.strip() for l in open(args[0], encoding="utf-8") if l.strip() and not l.startswith("#")]
        if "part" in opt:  # --part 1/2 and --part 2/2 split the list between two parallel fetchers
            i, k = map(int, opt["part"].split("/")); qs = qs[i - 1::k]
        freesound(qs, int(opt.get("n", 12)), int(opt.get("pages", 2)))
    elif cmd == "freesound-verify": freesound_verify()
    elif cmd == "dedupe": dedupe()
    elif cmd == "uisfx": uisfx()
    elif cmd == "synth": add_synth(args[0])
    elif cmd == "flag":
        ix = load_index(); flag_excluded(ix)
        for k in ix: ix.dirty.add(k)
        save_index(ix); print("excluded:", sum(1 for m in ix.values() if m.get("excluded")))
    elif cmd == "categories": print(" ".join(mixkit_categories()))
    else: print(__doc__)
