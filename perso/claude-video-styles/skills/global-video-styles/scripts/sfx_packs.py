"""Big free SFX packs: download (Kenney, OpenGameArt CC0), manifest every file, feature-index the one-shots for sfx_match.py.

Packs live untouched (original files) in ../sfx/packs/<pack>/ — Sonniss GDC bundles are fetched by packs_tools/fetch_sonniss.sh,
Mixkit long/ambient originals by `sfx_fetch.py mixkit-all`. Licences and sources: ../sfx/LICENSES.md, contents: ../sfx/packs/README.md.

usage (claude-video venv: ~/.venvs/claude-video/Scripts/python.exe, runs at below-normal priority):
  python sfx_packs.py kenney                 # every Kenney audio pack (CC0)
  python sfx_packs.py oga                    # curated OpenGameArt CC0 SFX packs (licence checked on each page)
  python sfx_packs.py shorten <pack dir>     # rename so every path <= 240 chars (originals in <pack>/_renamed.json)
  python sfx_packs.py scan                   # (re)build ../sfx/packs/manifest.json: every audio file, duration, category, licence
  python sfx_packs.py index [--workers 2]    # features for files <= 12 s -> ../sfx/packs/index.json (incremental)
  python sfx_packs.py flac <dir>             # lossless WAV -> FLAC (bit-exact check) for big ambience beds
  python sfx_packs.py stats                  # totals: library per source + packs
  python sfx_packs.py report                 # rewrite ../sfx/packs/README.md from the manifest
  python sfx_packs.py find "whoosh,swish" [--max 8] [--min 0] [--top 30]   # text search over the whole manifest (long files too)
Index entries use the same format as library/index.json ("file" is relative to sfx/library), so sfx_match.py ranks both together.
Anything named "glass" (or UCS category GLAS) is kept on disk but flagged excluded (the user hates the glass sound).
"""
import os, sys, re, json, time, zipfile, shutil, subprocess, urllib.request, http.cookiejar, html as htmlmod
sys.path.insert(0, os.path.dirname(__file__))

ROOT = os.path.normpath(os.path.join(os.path.dirname(__file__), "..", "sfx"))
PACKS = os.path.join(ROOT, "packs")
LIB = os.path.join(ROOT, "library")
DL = os.path.join(PACKS, "_downloads")
MANIFEST = os.path.join(PACKS, "manifest.json")
PIDX = os.path.join(PACKS, "index.json")
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126 Safari/537.36"
AUDIO = (".wav", ".ogg", ".mp3", ".flac", ".aif", ".aiff", ".m4a", ".opus")
MAX_FEAT_DUR = 12.0
SEVENZ = r"C:\Program Files\7-Zip\7z.exe"

# pack-name prefix -> licence / source (longest prefix wins)
PACK_INFO = {
    "sonniss-gdc2026": ("Sonniss #GameAudioGDC licence (royalty-free, commercial OK, no attribution; no redistribution as SFX, no AI training)", "https://gdc.sonniss.com/"),
    "sonniss-gdc2024": ("Sonniss #GameAudioGDC licence (royalty-free, commercial OK, no attribution; no redistribution as SFX, no AI training)", "https://sonniss.com/gameaudiogdc"),
    "kenney": ("CC0 1.0", "https://kenney.nl/assets/category:Audio"),
    "opengameart": ("CC0 1.0 (checked on each page)", "https://opengameart.org/"),
    "mixkit-long": ("Mixkit Sound Effects Free License", "https://mixkit.co/free-sound-effects/"),
}

KENNEY = ["ui-audio", "interface-sounds", "impact-sounds", "digital-audio", "sci-fi-sounds", "rpg-audio", "casino-audio",
          "music-jingles", "voiceover-pack", "voiceover-pack-fighter"]

OGA = ["512-sound-effects-8-bit-style", "gui-sound-effects", "37-hitspunches", "level-up-power-up-coin-get-13-sounds",
       "swishes-sound-pack", "swish-bamboo-stick-weapon-swhoshes", "100-cc0-sfx", "100-cc0-sfx-2", "80-cc0-rpg-sfx",
       "35-wooden-crackshitsdestructions", "16-button-clicks", "impact", "10-8bit-coin-sounds", "heartbeat-sounds", "ui-sounds",
       "hi-tech-button-sound-pack-i-non-themed", "50-cc0-retro-synth-sfx", "40-cc0-water-splash-slime-sfx", "bubbles-pop",
       "202-more-sound-effects", "atmospheric-interaction-sound-pack", "door-open-door-close-set", "75-cc0-breaking-falling-hit-sfx",
       "50-cc0-sci-fi-sfx", "25-cc0-bang-firework-sfx", "30-cc0-sfx-loops", "50-free-scifi-soundfx-192khz-64-bit-24576kbps-wav",
       "wind-hit-time-morph", "magic-spell-sfx", "card-game-sounds", "7-assorted-sound-effects-menu-level-up",
       "wood-and-metal-sound-effects-volume-2", "completion-sound", "space-ship-shield-sounds", "energy-drain",
       "steam-release-sounds", "synthesized-explosion", "point-bell", "click", "sound-effects-pack", "superpowers-assets-sound-effects",
       "fantasy-sound-effects-tinysized-sfx", "platformer-sounds-terminal-interaction-door-shots-bang-and-footsteps"]

# Universal Category System (UCS) CatID prefixes used by Sonniss vendors -> readable category
UCS = {"AIR": "air", "AERO": "aircraft", "ALARM": "alarms", "AMB": "ambience", "ANML": "animals", "BEEP": "beeps", "BELL": "bells",
       "BIRD": "birds", "BOAT": "boats", "BLLT": "bullets", "TOON": "cartoon", "CERM": "ceramics", "CHAIN": "chains", "CHEM": "chemicals",
       "CLOCK": "clocks", "CLOTH": "cloth", "COMM": "communications", "COMP": "computers", "CREA": "creatures", "CROWD": "crowds",
       "DSGN": "designed", "DEST": "destruction", "DIRT": "dirt & sand", "DOOR": "doors", "DRWR": "drawers", "ELEC": "electricity",
       "EQUIP": "equipment", "EXPL": "explosions", "FART": "farts", "FGHT": "fight", "FIRE": "fire", "FIREWRK": "fireworks",
       "FOLY": "foley", "FOOD": "food & drink", "FEET": "footsteps", "GAME": "games", "GEOT": "geothermal", "GLAS": "glass", "GORE": "gore",
       "GUN": "guns", "GUNS": "guns", "HORN": "horns", "HMN": "human", "ICE": "ice", "LASR": "lasers", "LETHR": "leather", "LIQ": "liquid & mud",
       "MACH": "machines", "MAGC": "magic", "MECH": "mechanical", "METL": "metal", "MOTR": "motors", "MOVE": "movement", "MUSC": "musical",
       "DSTR": "natural disaster", "OBJ": "objects", "PAPR": "paper", "PLAS": "plastic", "RAIN": "rain", "ROBO": "robots", "ROCK": "rocks",
       "ROPE": "rope", "RUBR": "rubber", "SCI": "sci-fi", "SNOW": "snow", "SPRT": "sports", "SWSH": "swooshes", "TOOL": "tools", "TOY": "toys",
       "TRAIN": "trains", "UI": "user interface", "VEG": "vegetation", "VEH": "vehicles", "VOX": "voices", "WATR": "water", "WEAP": "weapons",
       "WTHR": "weather", "WHSH": "whooshes", "WIND": "wind", "WINDW": "windows", "WING": "wings", "WOOD": "wood", "IMPT": "impacts",
       "STGR": "stingers", "TRANS": "transitions", "RISR": "risers", "HIT": "hits", "BOOM": "booms"}

# keyword families for files without a UCS prefix (Kenney, OGA, Mixkit long): first match wins
FAMILIES = [
    ("whooshes", "whoosh woosh swoosh swish swipe whip swing flyby fly-by passby pass-by"),
    ("risers", "riser uplifter downlifter swell build-up buildup reverse"),
    ("impacts", "impact hit punch thud slam knock stomp smash crash braam kick slap"),
    ("explosions", "explosion explode blast boom bang firework detonat"),
    ("user interface", "click button menu select interface toggle switch confirm cancel back_ error notification tick tap ui_ bleep blip beep"),
    ("sci-fi", "glitch digital computer scifi sci-fi laser zap synth robot hologram tech phaser forcefield shield energy"),
    ("magic", "magic spell sparkle shimmer chime fairy enchant"),
    ("games", "coin powerup power-up power_up levelup level-up jump 8bit 8-bit retro jingle win lose gameover game-over"),
    ("voices", "voice vocal scream laugh grunt breath male female taunt"),
    ("water", "water splash liquid drip bubble slime"),
    ("footsteps", "footstep footsteps step walk run"),
    ("doors", "door drawer lock key"),
    ("foley", "paper cloth wood metal plastic book card chip dice cards"),
    ("ambience", "ambience ambient atmos atmosphere loop wind rain forest city crowd room"),
    ("creatures", "creature monster growl roar zombie goblin ghost"),
    ("weapons", "gun shot rifle pistol sword blade weapon reload"),
    ("machines", "mechanical machine mechanism gear steampunk servo motor engine"),
    ("vehicles", "car traffic vehicle truck driveby drive-by atv motorbike"),
    ("destruction", "debris collapse rumble earthquake crumble break shatter"),
    ("musical", "drum guitar piano synth bass note chord"),
]


def lowprio():
    try:
        import ctypes
        from ctypes import wintypes
        k32 = ctypes.WinDLL("kernel32", use_last_error=True)
        k32.GetCurrentProcess.restype = wintypes.HANDLE
        k32.SetPriorityClass.argtypes = [wintypes.HANDLE, wintypes.DWORD]
        k32.SetPriorityClass(k32.GetCurrentProcess(), 0x00004000)  # BELOW_NORMAL, inherited by ffmpeg / pool workers
    except Exception:
        pass


LPFX = "\\\\?\\"  # the Windows long-path prefix  \\?\


def LP(path):
    """Windows long-path form (prefix + absolute path) so Python file calls work past 260 characters."""
    a = os.path.abspath(path)
    return LPFX + a if os.name == "nt" and not a.startswith(LPFX) else a


def _h4(s):
    import hashlib
    return hashlib.md5(s.encode("utf-8")).hexdigest()[:4]


def shorten(pack_dir, limit=240):
    """Rename files/folders so every path stays <= limit chars (MAX_PATH-safe for Python, Explorer, ffmpeg).
    Long folder names -> first 36 chars + ~hash, long file names -> truncated stem + ~hash (UCS prefix kept, extension kept).
    Original names are recorded in <pack>/_renamed.json."""
    pack_dir = os.path.abspath(pack_dir)
    rp = os.path.join(pack_dir, "_renamed.json")
    ren = json.load(open(rp, encoding="utf-8")) if os.path.exists(rp) else {"dirs": {}, "files": {}}
    n, stuck = 0, set()
    while True:
        changed = False
        for dp, ds, fs in os.walk(LP(pack_dir)):
            real = dp[len(LPFX):] if dp.startswith(LPFX) else dp
            for f in fs:
                full = os.path.join(real, f)
                if len(full) <= limit or full in stuck: continue
                parts = os.path.relpath(real, pack_dir).split(os.sep) if real != pack_dir else []
                i = max(range(len(parts)), key=lambda k: len(parts[k])) if parts else -1
                if len(real) > limit - 60 and i >= 0 and len(parts[i]) > 42:
                    new = parts[i][:36].rstrip(" .-_") + "~" + _h4(parts[i])
                    old_d = os.path.join(pack_dir, *parts[:i + 1]); new_d = os.path.join(pack_dir, *parts[:i], new)
                    if os.path.exists(LP(new_d)):  # merge (bundle parts extracting into the same library)
                        for dp2, _, fs2 in os.walk(LP(old_d)):
                            r2 = os.path.relpath(dp2, LP(old_d))
                            tgt = LP(new_d) if r2 == "." else os.path.join(LP(new_d), r2)
                            os.makedirs(tgt, exist_ok=True)
                            for f2 in fs2: os.replace(os.path.join(dp2, f2), os.path.join(tgt, f2))
                        shutil.rmtree(LP(old_d), ignore_errors=True)
                    else:
                        os.rename(LP(old_d), LP(new_d))
                    ren["dirs"][os.path.relpath(new_d, pack_dir).replace("\\", "/")] = os.path.relpath(old_d, pack_dir).replace("\\", "/")
                else:
                    stem, ext = os.path.splitext(f)
                    keep = max(8, limit - len(real) - 1 - len(ext) - 5)
                    if keep + 5 + len(ext) >= len(f): stuck.add(full); continue
                    nf = stem[:keep].rstrip(" .-_") + "~" + _h4(f) + ext
                    os.replace(LP(full), LP(os.path.join(real, nf)))
                    ren["files"][os.path.relpath(os.path.join(real, nf), pack_dir).replace("\\", "/")] = f
                n += 1; changed = True; break
            if changed: break
        if not changed: break
    if n: json.dump(ren, open(rp, "w", encoding="utf-8"), indent=1, ensure_ascii=False)
    print(f"[shorten] {pack_dir}: {n} renames", flush=True)
    return n


def free_gb():
    return shutil.disk_usage(PACKS).free / 1e9


def pack_info(pack):
    best = max((k for k in PACK_INFO if pack.startswith(k)), key=len, default=None)
    return PACK_INFO.get(best, ("see LICENSES.md", ""))


_jar = http.cookiejar.CookieJar()
_opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(_jar))


def get(url, binary=False, referer=None, tries=3):
    for i in range(tries):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": UA, **({"Referer": referer} if referer else {})})
            with _opener.open(req, timeout=120) as r:
                data = r.read()
            return data if binary else data.decode("utf-8", "replace")
        except Exception as e:
            if i == tries - 1: raise
            time.sleep(5 * (i + 1))


def extract(archive, dest):
    """Extract zip (python, path-safe) or rar/7z (7-Zip) into dest; returns number of files."""
    os.makedirs(dest, exist_ok=True)
    if archive.lower().endswith(".zip"):
        with zipfile.ZipFile(archive) as z:
            for m in z.infolist():
                target = os.path.normpath(os.path.join(dest, m.filename))
                if not target.startswith(os.path.normpath(dest)): continue  # path traversal guard
                if m.is_dir(): os.makedirs(target, exist_ok=True); continue
                os.makedirs(LP(os.path.dirname(target)), exist_ok=True)
                with z.open(m) as src, open(LP(target), "wb") as out: shutil.copyfileobj(src, out)
            n = len(z.infolist())
        shorten(dest); return n
    r = subprocess.run([SEVENZ, "x", "-y", "-bd", "-mmt=2", f"-o{dest}", archive], capture_output=True, text=True)
    if r.returncode != 0 or "Everything is Ok" not in r.stdout: raise RuntimeError(r.stdout[-400:] + r.stderr[-400:])
    return r.stdout.count("\n")


def kenney():
    os.makedirs(DL, exist_ok=True)
    for slug in KENNEY:
        dest = os.path.join(PACKS, "kenney", slug)
        if os.path.exists(os.path.join(dest, ".done")): print("[kenney]", slug, "already there"); continue
        page = f"https://kenney.nl/assets/{slug}"
        try:
            h = get(page)
        except Exception as e:
            print("[kenney]", slug, "page fail", e); continue
        if "CC0" not in h: print("[kenney]", slug, "no CC0 mention, skipped"); continue
        m = re.search(r"data-download-id='([0-9a-f]+)'", h)
        if not m: print("[kenney]", slug, "no download id"); continue
        link = json.loads(get(f"https://kenney.nl/download-link/{m.group(1)}", referer=page)).get("url")
        if not link: print("[kenney]", slug, "no link"); continue
        zp = os.path.join(DL, f"kenney_{slug}.zip")
        open(zp, "wb").write(get(link, binary=True, referer=page))
        n = extract(zp, dest)
        json.dump({"source": page, "license": "CC0 1.0", "fetched": time.strftime("%Y-%m-%d")}, open(os.path.join(dest, ".done"), "w"))
        os.remove(zp)
        print(f"[kenney] {slug}: {n} entries extracted, free {free_gb():.0f} GB", flush=True)
        time.sleep(1)


def oga():
    os.makedirs(DL, exist_ok=True)
    for slug in OGA:
        dest = os.path.join(PACKS, "opengameart", slug)
        if os.path.exists(os.path.join(dest, ".done")): print("[oga]", slug, "already there"); continue
        page = f"https://opengameart.org/content/{slug}"
        try:
            h = get(page)
        except Exception as e:
            print("[oga]", slug, "page fail", e); continue
        lic = re.findall(r"license-name'>([^<]+)<", h)
        if "CC0" not in lic: print(f"[oga] {slug}: licence {lic} -> skipped"); continue
        title = htmlmod.unescape(re.search(r"<title>([^<|]+)", h).group(1).strip())
        author = (re.search(r'field-name-author-submitter.*?<a href="/users/([^"]+)"', h, re.S) or [None, ""])[1]
        files = re.findall(r'<span class="file">.*?<a href="([^"]+)" type="([^"]*)"', h, re.S)
        if not files: print("[oga]", slug, "no files"); continue
        total = 0
        for url, typ in files:
            name = urllib.request.unquote(url.split("/")[-1])
            length = int((re.search(r"length=(\d+)", typ) or [0, 0])[1])
            if length > 2e9: print("[oga]", slug, name, "too big, skipped"); continue
            raw = get(url, binary=True, referer=page)
            low = name.lower()
            if low.endswith((".zip", ".rar", ".7z")):
                ap = os.path.join(DL, f"oga_{slug}_{name}"); open(ap, "wb").write(raw)
                total += extract(ap, dest); os.remove(ap)
            elif low.endswith(AUDIO):
                os.makedirs(dest, exist_ok=True); open(os.path.join(dest, name), "wb").write(raw); total += 1
            else:
                print("[oga]", slug, "ignored", name)
            time.sleep(0.5)
        json.dump({"source": page, "title": title, "author": author, "license": "CC0 1.0", "licenses_listed": lic,
                   "fetched": time.strftime("%Y-%m-%d")}, open(os.path.join(dest, ".done"), "w"), ensure_ascii=False)
        print(f"[oga] {slug} ({title} by {author}): {total} entries, licence {lic}", flush=True)
        time.sleep(1)


# ---------- manifest ----------
def classify(rel):
    """Category from the UCS CatID prefix of the filename, else from keywords in the path."""
    name = os.path.basename(rel)
    m = re.match(r"([A-Z]{2,7}?)([A-Z][a-z0-9]+)?[-_ ]", name)
    if m and m.group(1) in UCS: return UCS[m.group(1)], m.group(1) + (m.group(2) or "")
    low = rel.lower().replace("\\", "/")
    toks = set(re.split(r"[^a-z0-9]+", low))
    for fam, kws in FAMILIES:
        for k in kws.split():
            if (len(k) <= 3 and k.strip("_") in toks) or (len(k) > 3 and k in low): return fam, ""
    return "other", ""


def is_excluded(rel, catid=""):
    return "glass" in rel.lower() or catid.startswith("GLAS")


def audio_info(path):
    import soundfile as sf
    try:
        i = sf.info(path); return round(i.duration, 3), int(i.samplerate), int(i.channels)
    except Exception:
        r = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "stream=sample_rate,channels:format=duration", "-of", "json", path],
                           capture_output=True, text=True)
        try:
            j = json.loads(r.stdout); s = j["streams"][0]
            return round(float(j["format"]["duration"]), 3), int(s["sample_rate"]), int(s["channels"])
        except Exception:
            return None, None, None


def scan():
    old = json.load(open(MANIFEST, encoding="utf-8")) if os.path.exists(MANIFEST) else {}
    out = {}
    for top in sorted(os.listdir(PACKS)):
        tp = os.path.join(PACKS, top)
        if top.startswith("_") or not os.path.isdir(tp): continue
        subs = [top + "/" + s for s in sorted(os.listdir(tp)) if os.path.isdir(os.path.join(tp, s))] if top in ("kenney", "opengameart") else [top]
        for pack in subs:
            pdir = os.path.join(PACKS, pack)
            lic, src = pack_info(pack.replace("/", "-") if top != "kenney" else "kenney")
            done = os.path.join(pdir, ".done")
            meta = json.load(open(done, encoding="utf-8")) if os.path.exists(done) else {}
            for dp, _, fs in os.walk(pdir):
                for f in fs:
                    if not f.lower().endswith(AUDIO) or f.startswith("._"): continue
                    p = os.path.join(dp, f)
                    if len(p) > 259: print("  long path (run shorten):", p[-80:]); continue
                    rel = os.path.relpath(p, PACKS).replace("\\", "/")
                    st = os.stat(p)
                    o = old.get(rel)
                    dur, sr, ch = (o["dur"], o["sr"], o["ch"]) if o and o.get("bytes") == st.st_size else audio_info(p)
                    cat, catid = classify(os.path.relpath(p, pdir))
                    if pack == "mixkit-long": cat = os.path.relpath(p, pdir).replace("\\", "/").split("/")[0]  # Mixkit's own category
                    e = {"pack": pack, "file": rel, "bytes": st.st_size, "dur": dur, "sr": sr, "ch": ch, "category": cat,
                         "license": lic, "source": meta.get("source", src)}
                    if catid: e["ucs"] = catid
                    if pack.startswith("sonniss"): e["library"] = os.path.relpath(p, pdir).replace("\\", "/").split("/")[0]
                    if is_excluded(rel, catid): e["excluded"] = "glass (the user hates the glass sound; file kept, never suggested)"
                    out[rel] = e
            print(f"[scan] {pack}: {sum(1 for v in out.values() if v['pack'] == pack)} files", flush=True)
    json.dump(out, open(MANIFEST, "w", encoding="utf-8"), indent=0, ensure_ascii=False)
    print("manifest:", len(out), "files")
    return out


# ---------- feature index ----------
def _feat(args):
    rel, = args
    try:
        import numpy as np
        from sfx_feat import load_mono, trim, features, qc, SR
        p = os.path.join(PACKS, rel)
        try:
            y = load_mono(p)
        except Exception:
            import soundfile as sf, tempfile
            td = tempfile.mkdtemp(); w = os.path.join(td, "x.wav")
            subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", p, "-ac", "1", "-ar", str(SR), w], check=True)
            y = load_mono(w); shutil.rmtree(td, ignore_errors=True)
        q = qc(y); t = trim(y)
        if len(t) < 64: return rel, None, "silent"
        vec, info = features(t)
        return rel, {"vec": [round(float(v), 4) for v in vec], **info, **q}, "ok"
    except Exception as e:
        return rel, None, f"error {type(e).__name__}: {e}"[:200]


def index(workers=2):
    from multiprocessing import Pool
    man = json.load(open(MANIFEST, encoding="utf-8"))
    ix = json.load(open(PIDX, encoding="utf-8")) if os.path.exists(PIDX) else {}
    todo = [rel for rel, m in man.items() if m.get("dur") and 0.03 <= m["dur"] <= MAX_FEAT_DUR
            and not (f"packs/{rel}" in ix and ix[f"packs/{rel}"].get("bytes") == m["bytes"])]
    stale = [k for k in ix if k[len("packs/"):] not in man]
    for k in stale: ix.pop(k)
    print(f"indexing {len(todo)} files with {workers} workers (already {len(ix)}, {len(stale)} stale removed)", flush=True)
    done = 0
    with Pool(workers, initializer=lowprio) as pool:
        for rel, feat, status in pool.imap_unordered(_feat, [(r,) for r in todo], chunksize=8):
            done += 1
            if feat:
                m = man[rel]
                stem = os.path.splitext(os.path.basename(rel))[0]
                parent = os.path.basename(os.path.dirname(rel))
                ix[f"packs/{rel}"] = {"source": "pack:" + m["pack"], "id": rel, "title": f"{stem} [{parent}]", "category": m["category"],
                                      "tags": [m["category"], m["pack"], parent] + ([m["ucs"]] if m.get("ucs") else []),
                                      "license": m["license"], "page": m["source"], "url": "", "bytes": m["bytes"],
                                      "file": "../packs/" + rel, **feat, **({"excluded": m["excluded"]} if m.get("excluded") else {})}
            elif status != "ok":
                man[rel]["index_error"] = status
            if done % 500 == 0:
                json.dump(ix, open(PIDX, "w", encoding="utf-8"), ensure_ascii=False)
                print(f"  {done}/{len(todo)}", flush=True)
    json.dump(ix, open(PIDX, "w", encoding="utf-8"), ensure_ascii=False)
    json.dump(man, open(MANIFEST, "w", encoding="utf-8"), indent=0, ensure_ascii=False)
    print("pack index:", len(ix), "entries", flush=True)


# ---------- search + report ----------
def find(kw, maxdur=None, mindur=0, top=30):
    man = json.load(open(MANIFEST, encoding="utf-8"))
    kws = [k.strip().lower() for k in kw.split(",") if k.strip()]
    hits = [m for m in man.values() if not m.get("excluded") and m.get("dur") is not None
            and (maxdur is None or m["dur"] <= maxdur) and m["dur"] >= mindur
            and any(k in (m["file"] + " " + m["category"]).lower() for k in kws)]
    for m in sorted(hits, key=lambda m: m["dur"])[:top]:
        print(f"{m['dur']:7.2f}s  {m['category']:16s} {os.path.join(PACKS, m['file'])}")
    print(len(hits), "matches")


def to_flac(folder, min_age=60):
    """Losslessly re-encode integer-PCM WAVs to FLAC (bit-exact check, then the WAV is deleted). Float WAVs are left as they are.
    Used for packs/mixkit-long (ambience beds, 8 MB average) to keep the collection under its disk budget."""
    import soundfile as sf, numpy as np
    saved, n, kept = 0, 0, 0
    for dp, _, fs in os.walk(folder):
        for f in fs:
            if not f.lower().endswith(".wav"): continue
            w = os.path.join(dp, f); fl = w[:-4] + ".flac"
            if time.time() - os.path.getmtime(w) < min_age: continue
            info = sf.info(w)
            if info.subtype not in ("PCM_16", "PCM_24", "PCM_U8"): kept += 1; continue
            r = subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", w, "-map_metadata", "0", "-c:a", "flac", "-compression_level", "8", fl],
                               capture_output=True, text=True)
            if r.returncode != 0: print("flac fail", f, r.stderr[-200:]); kept += 1; continue
            a, _ = sf.read(w, dtype="int32", always_2d=True); b, _ = sf.read(fl, dtype="int32", always_2d=True)
            if a.shape != b.shape or not np.array_equal(a, b): print("not bit-exact, kept WAV:", f); os.remove(fl); kept += 1; continue
            saved += os.path.getsize(w) - os.path.getsize(fl); n += 1; os.remove(w)
    print(f"[flac] {folder}: {n} files -> FLAC, {saved / 1e9:.2f} GB saved, {kept} kept as WAV", flush=True)


def stats():
    """Totals for the whole SFX collection: library (QC'd one-shots) per source + packs."""
    from collections import Counter
    lib = json.load(open(os.path.join(LIB, "index.json"), encoding="utf-8"))
    man = json.load(open(MANIFEST, encoding="utf-8"))
    pidx = json.load(open(PIDX, encoding="utf-8")) if os.path.exists(PIDX) else {}
    size = lambda d: sum(os.path.getsize(os.path.join(dp, f)) for dp, _, fs in os.walk(LP(d)) for f in fs) / 1e9
    print("library:", len(lib), "sounds,", f"{size(LIB):.2f} GB,", "excluded", sum(1 for m in lib.values() if m.get("excluded")))
    for src, n in Counter(m["source"] for m in lib.values()).most_common(): print(f"  {src:10s} {n}")
    print("packs:", len(man), "files,", len(pidx), "indexed,", f"{sum(m['bytes'] for m in man.values()) / 1e9:.2f} GB")
    for g, n in Counter(m["pack"].split("/")[0] for m in man.values()).most_common(): print(f"  {g:16s} {n}")


def report():
    from collections import Counter, defaultdict
    man = json.load(open(MANIFEST, encoding="utf-8"))
    pidx = json.load(open(PIDX, encoding="utf-8")) if os.path.exists(PIDX) else {}
    by = defaultdict(list)
    for m in man.values(): by[m["pack"]].append(m)
    groups = defaultdict(list)
    for p in by: groups[p.split("/")[0]].append(p)
    L = ["# SFX packs", "",
         "Big free packs kept as original files (not normalised). One-shots up to 12 s are feature-indexed in `index.json` and ranked by",
         "`scripts/sfx_match.py` together with `../library`; longer files (ambiences, loops, beds) are only listed in `manifest.json` —",
         "search them with `python scripts/sfx_packs.py find \"rain,crowd\" --min 10`. Licences: `../LICENSES.md`.",
         "Files named \"glass\" (or UCS GLAS…) stay on disk but are flagged `excluded` and never suggested.",
         "`mixkit-long/` = the Mixkit sounds that fail the one-shot QC (long ambiences, beds, low-band booms), stored as lossless FLAC",
         "(bit-exact with Mixkit's WAV, checked on every file) to save 2.5 GB; the Mixkit catalogue = `../library/mixkit` + this folder.",
         "Paths longer than 240 characters were shortened (`~hash` suffix) so Python, ffmpeg and Explorer can open them; the",
         "original names are in each pack's `_renamed.json`. Sonniss licence PDFs and track lists are inside their folders.", "",
         f"Generated {time.strftime('%Y-%m-%d %H:%M')} by `sfx_packs.py report`.", "",
         "| Pack | Files | Indexed (≤12 s) | Long (>12 s) | Size | Licence | Source |", "|---|---:|---:|---:|---:|---|---|"]
    tot = Counter()
    for g in sorted(groups):
        ms = [m for p in groups[g] for m in by[p]]
        n = len(ms); ni = sum(1 for m in ms if f"packs/{m['file']}" in pidx); nl = sum(1 for m in ms if (m.get("dur") or 0) > MAX_FEAT_DUR)
        size = sum(m["bytes"] for m in ms) / 1e9
        lic, src = pack_info(g if g != "opengameart" else "opengameart")
        L.append(f"| {g} ({len(groups[g])} packs) | {n} | {ni} | {nl} | {size:.2f} GB | {lic} | {src} |" if len(groups[g]) > 1 else
                 f"| {g} | {n} | {ni} | {nl} | {size:.2f} GB | {lic} | {src} |")
        tot.update(files=n, idx=ni, long=nl); tot["bytes"] += sum(m["bytes"] for m in ms)
    L.append(f"| **total** | **{tot['files']}** | **{tot['idx']}** | **{tot['long']}** | **{tot['bytes'] / 1e9:.2f} GB** | | |")
    L += ["", "## Files per category (all packs)", "", "| Category | Files | ≤12 s |", "|---|---:|---:|"]
    cc = Counter(m["category"] for m in man.values()); ci = Counter(m["category"] for m in man.values() if (m.get("dur") or 99) <= MAX_FEAT_DUR)
    for c, n in cc.most_common(): L.append(f"| {c} | {n} | {ci[c]} |")
    for g in sorted(groups):
        L += ["", f"## {g}", ""]
        if len(groups[g]) > 1 or g in ("kenney", "opengameart"):
            L += ["| Pack | Files | Top categories | Source |", "|---|---:|---|---|"]
            for p in sorted(groups[g]):
                c = Counter(m["category"] for m in by[p]).most_common(3)
                L.append(f"| {p.split('/', 1)[-1]} | {len(by[p])} | {', '.join(f'{k} {v}' for k, v in c)} | {by[p][0]['source']} |")
        else:
            c = Counter(m["category"] for m in by[g]).most_common(12)
            L.append("Categories: " + ", ".join(f"{k} {v}" for k, v in c))
            libs = Counter(m.get("library") for m in by[g] if m.get("library"))
            if libs:
                L += ["", f"{len(libs)} vendor libraries, e.g. " + "; ".join(k for k, _ in libs.most_common(12)) + "."]
    open(os.path.join(PACKS, "README.md"), "w", encoding="utf-8").write("\n".join(L) + "\n")
    print("\n".join(L[:30]))


if __name__ == "__main__":
    lowprio()
    try: sys.stdout.reconfigure(encoding="utf-8", errors="replace"); sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception: pass
    cmd = sys.argv[1] if len(sys.argv) > 1 else "help"
    opt = {sys.argv[i][2:]: sys.argv[i + 1] for i in range(2, len(sys.argv) - 1) if sys.argv[i].startswith("--")}
    args = [a for a in sys.argv[2:] if not a.startswith("--") and a not in opt.values()]
    if cmd == "kenney": kenney()
    elif cmd == "oga": oga()
    elif cmd == "scan": scan()
    elif cmd == "shorten": [shorten(a) for a in args]
    elif cmd == "index": index(int(opt.get("workers", 2)))
    elif cmd == "report": report()
    elif cmd == "stats": stats()
    elif cmd == "flac": [to_flac(a) for a in args]
    elif cmd == "find": find(args[0], float(opt["max"]) if "max" in opt else None, float(opt.get("min", 0)), int(opt.get("top", 30)))
    else: print(__doc__)
