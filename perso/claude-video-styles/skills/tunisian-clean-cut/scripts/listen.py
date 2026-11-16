"""Close listening of tiny slices: the tool that finally locates stutters and false starts.

  python -I listen.py -p <project> 237.80-238.70 238.55-241.00 [--langs en,fr,ar] [--verbatim]
                      [--pad 0.25] [--strip] [--audio file.wav]

Per slice, for each language: the words Whisper hears with their absolute time (word@t), with the slice
zero-padded by 0.25 s (no pinned first word). --verbatim adds a pass with a disfluent prompt that invites
Whisper to write repeats. --strip prints the 10 ms loudness (dB) with the T_low/T_high marks and the gap/notch
boundaries. Whisper times are +-0.2 s: cut points come from the strip, never from word@t.

Use it to:
  - check a doubt (what is in 238.55-241.00 ?),
  - prove a cut point: transcribe from the proposed point to the line end; the whole phrase must be heard,
  - check a line end: [end-1.3, end] vs [end-1.3, end+0.45]; a fuller last word in the 2nd = clipped end.
"""
import argparse
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from tcc_common import (VERBATIM, Project, add_project_arg, boundaries_in, db_strip, load_audio,  # noqa: E402
                        slice_of, thresholds_from, transcribe)


def main():
    ap = add_project_arg(argparse.ArgumentParser())
    ap.add_argument("slices", nargs="+", help="a-b in seconds of the audio")
    ap.add_argument("--audio", help="audio file (default: the project's mic16k.wav)")
    ap.add_argument("--langs", default="en,fr,ar")
    ap.add_argument("--pad", type=float, default=0.25)
    ap.add_argument("--verbatim", action="store_true")
    ap.add_argument("--strip", action="store_true")
    a = ap.parse_args()
    src = a.audio or Project(a.project).mic16()
    y = load_audio(src)
    db = db_strip(y)
    ref, hi, lo = thresholds_from(db)
    if a.strip:
        print(f"ref {ref:.1f} dB  T_high {hi:.1f}  T_low {lo:.1f}")
    for spec in a.slices:
        s, e = map(float, spec.split("-"))
        seg = slice_of(y, s, e)
        print(f"--- [{s:.2f}-{e:.2f}] ({e - s:.2f} s)")
        for lang in a.langs.split(","):
            passes = [("plain", "default")]
            if a.verbatim and VERBATIM.get(lang):
                passes.append(("verb", VERBATIM[lang]))
            for label, pr in passes:
                text, ws = transcribe(seg, lang, s, prompt=pr, pad=a.pad, raw=True)
                said = " ".join(f"{w}@{t:.2f}" for w, t, _, _ in ws) if ws else text or "(nothing)"
                print(f"  {lang} {label:5}: {said}", flush=True)
        if a.strip:
            i0, i1 = int(s * 100), int(e * 100)
            row = []
            for i in range(i0, min(i1, len(db))):
                v = db[i]
                m = "#" if v > hi else "+" if v > lo else "."
                row.append(f"\n   {i / 100:7.2f} " if (i - i0) % 20 == 0 else "")
                row.append(f"{v:4.0f}{m}")
            print("  dB (10 ms, # >T_high, + >T_low, . below):" + "".join(row))
            bs = boundaries_in(db, s, e, hi, lo)
            print("  boundaries (where a take can restart): " + "  ".join(f"{t:.2f} {k} {d:.0f}dB" for t, k, d in bs))


if __name__ == "__main__":
    main()
