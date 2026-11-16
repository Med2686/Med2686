"""Final QA on the CLEAN voice: re-hear it and prove nothing is doubled and no pause survived.

  python -I qa_clean.py -p <project> [--voice work/voice-clean.wav] [--langs en,fr] [--win 10 --step 8]

1. Re-transcribe the clean voice in overlapping 10 s windows (en is the most readable proxy, fr second).
   A pause-free voice cannot be split into phrases, so windows it is.
2. Run the fuzzy n-gram repeat scanner on every window and map each hit back to the line (#n · mic t s)
   through clean.json, so it can be found in the Studio labels and in keep.json.
3. Pause audit: the longest quiet runs (under T_low) in the clean voice. Target: none over ~0.1 s
   (he spots 0.3 s gaps instantly).
Read the windows yourself too, as a viewer would: a word that makes no sense where a repeat would fit,
a phrase that stops mid-idea, a doubled idea across a join. Out: work/qa.txt
"""
import argparse
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from tcc_common import (Project, add_project_arg, db_strip, find_repeats, load_audio, norm_tokens,  # noqa: E402
                        read_json, runs_of, slice_of, transcribe)


def where(C, t):
    """clean-voice time -> (line, mic time)."""
    f = t * C["fps"]
    for p in C["pieces"]:
        if p["t0"] <= f < p["t0"] + p["n"]:
            return p.get("line", "?"), p["a"] + (f - p["t0"]) / C["fps"]
    return "?", None


def main():
    ap = add_project_arg(argparse.ArgumentParser())
    ap.add_argument("--voice")
    ap.add_argument("--clean")
    ap.add_argument("--langs", default="en,fr")
    ap.add_argument("--win", type=float, default=10.0)
    ap.add_argument("--step", type=float, default=8.0)
    a = ap.parse_args()
    P = Project(a.project)
    C = read_json(a.clean or P.work / "clean.json")
    y = load_audio(a.voice or P.work / "voice-clean.wav")
    L = len(y) / 16000
    out, hits = [], []
    t = 0.0
    while t < L - 0.5:
        e = min(L, t + a.win)
        for lang in a.langs.split(","):
            # no prompt here: on a pause-free voice the fr pass recited its prompt instead of transcribing
            text, ws = transcribe(slice_of(y, t, e), lang, t, prompt=None)
            out.append(f"{t:6.1f}-{e:5.1f}s {lang}: {text or '(EMPTY: re-hear this window with listen.py --audio voice-clean.wav)'}")
            print(out[-1], flush=True)
            toks = [(tk, s) for w, s, _, _ in ws for tk in norm_tokens(w)]
            for kind, n, i, j, ph in find_repeats([x for x, _ in toks]):
                tt = toks[j][1] if j < len(toks) else t
                li, mt = where(C, tt)
                hits.append(f"DOUBLED? {kind} « {ph} » ({lang}) at clean {tt:.2f} s = line #{li} · mic {mt if mt is None else round(mt, 2)} s")
        t += a.step
    v = db_strip(y)
    lo = C.get("thresholds", {}).get("lo", -50)
    quiet = sorted(((z - x) * 0.01, x * 0.01) for x, z in runs_of(v <= lo))[-8:][::-1]
    rep = ["== windows"] + out + ["", "== repeats found in the clean voice (check each by ear-proxy: listen.py on the mic)"]
    rep += sorted(set(hits)) or ["none"]
    rep += ["", "== longest quiet runs (target < 0.10 s)"]
    for d, s in quiet:
        li, mt = where(C, s)
        rep.append(f"  {d:.2f} s at clean {s:.2f} s (line #{li} · mic {mt if mt is None else round(mt, 2)} s)"
                   + ("   <-- PAUSE" if d > 0.15 else ""))
    (P.work / "qa.txt").write_text("\n".join(rep) + "\n", encoding="utf8")
    print("\n".join(rep[len(out) + 1:]))


if __name__ == "__main__":
    main()
