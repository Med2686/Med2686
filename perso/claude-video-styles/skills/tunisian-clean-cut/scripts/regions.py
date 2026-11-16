"""Speech regions of the mic: the phrases between his pauses (where he reads the next line of the script).

  python -I regions.py -p <project> [--merge 0.30] [--min 0.10]

Hysteresis on the 10 ms loudness: ref = p90 of frames well above the floor, a region must peak above
ref-13 dB and extends while above ref-23 dB (soft word tails within 0.2 s are kept). Runs closer than
--merge s are one region. Regions are where to listen, not cut points: a region can hold two takes glued
together, and two regions can be one sentence said in two breaths.
Out: work/regions.json [[a, b], ...] (mic seconds), printed with durations and gaps.
"""
import argparse
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from tcc_common import (Project, add_project_arg, db_strip, load_audio, runs_of, speech_mask,  # noqa: E402
                        thresholds_from, write_json)


def main():
    ap = add_project_arg(argparse.ArgumentParser())
    ap.add_argument("--merge", type=float, default=0.30)
    ap.add_argument("--min", type=float, default=0.10)
    ap.add_argument("--audio")
    a = ap.parse_args()
    P = Project(a.project)
    y = load_audio(a.audio or P.mic16())
    db = db_strip(y)
    ref, hi, lo = thresholds_from(db)
    m = speech_mask(db, hi, lo)
    rs = [[x * 0.01, z * 0.01] for x, z in runs_of(m)]
    out = []
    for r in rs:
        if out and r[0] - out[-1][1] < a.merge:
            out[-1][1] = r[1]
        else:
            out.append(r)
    out = [[round(x, 2), round(z, 2)] for x, z in out if z - x >= a.min]
    write_json(P.work / "regions.json", out, indent=0)
    print(f"ref {ref:.1f} dB  T_high {hi:.1f}  T_low {lo:.1f}  ->  {len(out)} regions, "
          f"{sum(z - x for x, z in out):.1f} s of speech in {len(y) / 16000:.1f} s")
    for i, (x, z) in enumerate(out):
        gap = x - out[i - 1][1] if i else x
        print(f"  #{i + 1:3} {x:7.2f}-{z:7.2f}  ({z - x:4.2f} s)  gap before {gap:5.2f} s")


if __name__ == "__main__":
    main()
