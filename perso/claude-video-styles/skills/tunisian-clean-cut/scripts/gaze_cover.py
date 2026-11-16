"""Script-reading check: where does he look at his screen WHILE TALKING in the clean cut?

  python -I gaze_cover.py -p <project> --gaze-only          # step 2: just run gaze on the proxy (system Python)
  python -I gaze_cover.py -p <project> [--gaze work/gaze-raw.json] [--run-gaze] [--seed 0.4] [--min-frames 10]

He reads from a screen on the image-left during his pauses; the speech mask already removes most of it.
What is left are look-aways inside kept speech. Those words are needed, so they are NOT cut: each one gets
a COVER entry (clean-timeline frames) for a full-screen graphic / cutaway in the edit.
--run-gaze first runs reel-pro-edit's gaze.py (MediaPipe face landmarker, system Python 3.12) on
work/proxy540.mp4 (made by prep.py --proxy, on the same fps grid as the camera cut).
Side score per frame = (eyeLookOutRight + eyeLookInLeft) / 2 for a screen on the image-left (swap for right).
A run above --seed for >= --min-frames frames inside kept speech = a look-away.
Then LOOK at work/gaze-check.jpg (the peak frame of each entry): a thinking look (eyes up, hand on the
chin) is fine and needs no cover; only reading glances do. Out: work/cover.json + work/gaze-check.jpg
"""
import argparse
import os
import subprocess
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from tcc_common import MODELS, REEL_PRO_EDIT, SYS_PY, Project, add_project_arg, read_json, runs_of, write_json  # noqa: E402

FONT = "C\\:/Windows/Fonts/arial.ttf"  # ffmpeg 9 here has no fontconfig: drawtext always needs fontfile=


def main():
    ap = add_project_arg(argparse.ArgumentParser())
    ap.add_argument("--gaze")
    ap.add_argument("--clean")
    ap.add_argument("--proxy")
    ap.add_argument("--run-gaze", action="store_true")
    ap.add_argument("--gaze-only", action="store_true", help="only make gaze-raw.json (step 2, before clean.json exists)")
    ap.add_argument("--seed", type=float, default=None)
    ap.add_argument("--min-frames", type=int, default=None)
    ap.add_argument("--out-dir")
    a = ap.parse_args()
    P = Project(a.project)
    od = a.out_dir or str(P.work)
    seed = a.seed if a.seed is not None else float(P.cfg.get("gaze_seed", 0.4))
    minf = a.min_frames or int(P.cfg.get("gaze_min_frames", 10))
    gz = a.gaze or str(P.work / "gaze-raw.json")
    proxy = a.proxy or str(P.work / "proxy540.mp4")
    if a.run_gaze or not os.path.exists(gz):
        subprocess.run([SYS_PY, "-I", str(REEL_PRO_EDIT / "gaze.py"), proxy, str(MODELS / "face_landmarker.task"), gz], check=True)
    if a.gaze_only:
        print("gaze ->", gz)
        return
    G = read_json(gz)
    C = read_json(a.clean or P.work / "clean.json")
    ix = {k: i for i, k in enumerate(G["cols"])}
    side = P.cfg.get("screen_side", "left")
    ko, ki = ("eyeLookOutRight", "eyeLookInLeft") if side == "left" else ("eyeLookOutLeft", "eyeLookInRight")
    S = np.array([0.0 if r[1] is None else (r[ix[ko]] + r[ix[ki]]) / 2 for r in G["rows"]])
    # clean timeline: camera frame for every clean frame
    cam = np.concatenate([np.arange(p["camF"], p["camF"] + p["n"]) for p in C["pieces"]])
    line = np.concatenate([[p.get("line", 0)] * p["n"] for p in C["pieces"]])
    mic = np.concatenate([p["a"] + np.arange(p["n"]) / C["fps"] for p in C["pieces"]])
    sc = np.where(cam < len(S), S[np.minimum(cam, len(S) - 1)], 0)
    covers = []
    for x, z in runs_of(sc > seed):
        if z - x >= minf:
            pk = x + int(np.argmax(sc[x:z]))
            covers.append({"f0": int(x), "f1": int(z), "t0": round(x / C["fps"], 2), "t1": round(z / C["fps"], 2),
                           "line": int(line[x]), "mic": [round(float(mic[x]), 2), round(float(mic[z - 1]), 2)],
                           "peak": round(float(sc[pk]), 2), "peakCamF": int(cam[pk])})
    write_json(os.path.join(od, "cover.json"), covers)
    print(f"side={side} seed={seed} min={minf} frames: {len(covers)} look-aways in kept speech")
    for i, c in enumerate(covers, 1):
        print(f"  COVER {i}: clean {c['t0']:.2f}-{c['t1']:.2f} s ({c['f1'] - c['f0']} fr) line #{c['line']} "
              f"· mic {c['mic'][0]:.2f}-{c['mic'][1]:.2f} s, peak {c['peak']}")
    if covers and os.path.exists(proxy):
        sel = "+".join(f"eq(n,{c['peakCamF']})" for c in covers)
        cols = min(4, len(covers))
        rows = (len(covers) + cols - 1) // cols
        g = (f"[0:v]select='{sel}',scale=270:-2,drawtext=fontfile='{FONT}':text='%{{n}}':x=8:y=8:fontsize=28:"
             f"fontcolor=yellow:box=1:boxcolor=black@0.6,tile={cols}x{rows}[v]")
        gf = os.path.join(od, "gaze-check-graph.txt")
        open(gf, "w", encoding="utf8").write(g)
        subprocess.run(["ffmpeg", "-nostdin", "-v", "error", "-y", "-i", proxy, "-/filter_complex", gf, "-map", "[v]",
                        "-frames:v", "1", "-update", "1", os.path.join(od, "gaze-check.jpg")], check=True)
        print("look at", os.path.join(od, "gaze-check.jpg"), "(tiles numbered 0.. in COVER order)")


if __name__ == "__main__":
    main()
