"""Find the library sounds closest to a reference sound (e.g. a cut from a reference reel, or a sound the user likes).

usage:
  python sfx_match.py <ref.wav> [--top 6] [--source mixkit|freesound|uisfx|synth|pack:sonniss-gdc2024|pack] [--kw "whoosh,swoosh,air"]
                      [--scope all|library|packs] [--montage out.png] [--copy dir]
  --kw keeps only sounds whose title/category/tags/file path has a word starting with one of the keywords ("air" matches
  "air_whoosh", not "stairs"; pick the family first, then rank by sound).
  --scope: library = QC'd one-shots in sfx/library (default before 2026-11-14); packs = sfx/packs one-shots (Sonniss GDC, Kenney,
  OpenGameArt, Mixkit long); all (default) = both. --source pack keeps every pack, pack:<name> one pack (prefix match).
  Entries flagged "excluded" (anything named glass — the user hates the glass sound) are never returned.
Distance = standardised euclidean on the shared feature vector (duration, attack, centroid start/end/slope, low/high energy,
flatness, MFCC 1-7); duration and centroid slope are weighted x2 because they define the "gesture" (whoosh up/down, hit, tick).
Run with ~/.venvs/claude-video/Scripts/python.exe
"""
import os, sys, re, json, shutil
import numpy as np
sys.path.insert(0, os.path.dirname(__file__))
from sfx_feat import load_mono, trim, features

LIB = os.path.normpath(os.path.join(os.path.abspath(os.path.dirname(__file__)), "..", "sfx", "library"))
W = np.array([2, 1, 1, 1, 2, 1, 1, 1, .6, .6, .6, .6, .6, .6, .6], dtype=np.float32)


PIDX = os.path.normpath(os.path.join(LIB, "..", "packs", "index.json"))


def fpath(m):
    """Absolute, normalised path of an index entry (pack files are '../packs/...'; un-normalised they can pass MAX_PATH)."""
    return os.path.normpath(os.path.join(LIB, m["file"]))


def load_all(scope="all"):
    ix = {}
    if scope in ("all", "library"): ix.update(json.load(open(os.path.join(LIB, "index.json"), encoding="utf-8")))
    if scope in ("all", "packs") and os.path.exists(PIDX): ix.update(json.load(open(PIDX, encoding="utf-8")))
    return {k: m for k, m in ix.items() if not m.get("excluded") and m.get("vec")}


def _text(m):
    return " ".join([m.get("title", ""), m.get("category", ""), m.get("file", ""), " ".join(m.get("tags", []))]).lower()


def rank(ref, top=6, source=None, kw=None, scope="all"):
    ix = load_all(scope)
    kws = [k.strip().lower() for k in kw.split(",")] if kw else None
    keys = [k for k in ix if (not source or ix[k]["source"] == source or ix[k]["source"].startswith(source + (":" if source == "pack" else "")))
            and (not kws or any(re.search(r"(?<![a-z])" + re.escape(w), _text(ix[k])) for w in kws))]
    M = np.array([ix[k]["vec"] for k in keys], dtype=np.float32)
    mu, sd = M.mean(0), M.std(0) + 1e-6
    rv, rinfo = features(trim(load_mono(ref)))
    d = np.sqrt((((M - rv) / sd * W) ** 2).sum(1))
    order = np.argsort(d)[:top]
    return rinfo, [(keys[i], float(d[i]), ix[keys[i]]) for i in order]


def montage(ref, hits, out):
    import librosa, matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
    files = [("REF", ref)] + [(k.split("/")[-1][:28], fpath(m)) for k, _, m in hits]
    fig, ax = plt.subplots(1, len(files), figsize=(3 * len(files), 3))
    for a, (lab, f) in zip(ax, files):
        y = trim(load_mono(f))[: 44100 * 2]
        S = librosa.amplitude_to_db(np.abs(librosa.stft(y, n_fft=1024, hop_length=128)) + 1e-9, ref=np.max)
        a.imshow(S, origin="lower", aspect="auto", cmap="magma", vmin=-70, vmax=0); a.set_title(lab, fontsize=7); a.axis("off")
    fig.tight_layout(); fig.savefig(out, dpi=70); plt.close(fig)


if __name__ == "__main__":
    ref = sys.argv[1]
    opt = {sys.argv[i][2:]: sys.argv[i + 1] for i in range(2, len(sys.argv) - 1) if sys.argv[i].startswith("--")}
    info, hits = rank(ref, int(opt.get("top", 6)), opt.get("source"), opt.get("kw"), opt.get("scope", "all"))
    print("REF", info)
    for k, d, m in hits:
        print(f"{d:6.2f}  {k[:60]:60s} {m['dur']:5.2f}s  cen {m['cen_start']}->{m['cen_end']}  low {m['low']}  {m.get('title','')[:50]}  [{m.get('license','')[:24]}]")
        print(f"        {fpath(m)}")
    if "montage" in opt: montage(ref, hits, opt["montage"])
    if "copy" in opt:
        os.makedirs(opt["copy"], exist_ok=True)
        for k, _, m in hits[:3]: shutil.copy(fpath(m), opt["copy"])
