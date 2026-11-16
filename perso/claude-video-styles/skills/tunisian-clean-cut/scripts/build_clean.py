"""keep.json (your editorial decisions) -> work/clean.json + work/voice-clean.wav, frame-exact.

  python -I build_clean.py -p <project> [--keep work/keep.json] [--gap-min 0.06] [--pad 0.02]

keep.json = the lines to keep, in mic seconds, in reel order. Each entry is either
    [a, b, "text in arabizi"]                                    or
    {"a": 237.9, "b": 240.95, "text": "...", "cut": 238.21, 238.59, "why": "false start « ou la cap »"}
`cut` removes exact sub-spans inside a line (a false start glued to the retake, a filler in the middle).
Everything outside the kept lines is gone: pauses, script reading, retakes, tics.

Inside each line a hysteresis speech mask removes every quiet run longer than --gap-min (default 0.06 s):
ref = p90 of the kept spans, a burst must peak above ref-13 dB and extends while above ref-23 dB; soft runs
within 0.2 s of a voiced burst stay (word tails). Each kept run gets 20 ms pads. Bounds land on the fps grid
of the mic timeline, so the camera is cut on exactly the same frames (camF = round((a*rate + offset)*fps)).

Out: work/clean.json {offset, rate, fps, pieces:[{a,b,t0,n,camF,text,line,lineA}], total, totalF, lines:[...]}
     work/voice-clean.wav (48 kHz mono 16-bit, 6 ms fades at every join, peak -1 dBFS)
"""
import argparse
import os
import sys
import wave

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from tcc_common import (Project, add_project_arg, db_strip, load_audio, read_json, runs_of,  # noqa: E402
                        speech_mask, thresholds_from, write_json)

SR = 48000
FADE = 0.006


def load_keep(path):
    out = []
    for k in read_json(path):
        if isinstance(k, dict):
            out.append({"a": float(k["a"]), "b": float(k["b"]), "text": k.get("text", ""), "cut": k.get("cut", []),
                        "why": k.get("why", "")})
        else:
            out.append({"a": float(k[0]), "b": float(k[1]), "text": k[2] if len(k) > 2 else "", "cut": [],
                        "why": k[3] if len(k) > 3 else ""})
    return out


def kept_runs(mask, db, hi, a, b, cuts, gap_min, pad, hop):
    i0, i1 = int(round(a / hop)), int(round(b / hop))
    m = mask[i0:i1].copy()
    for x, z in cuts:
        m[max(0, int(round(x / hop)) - i0): max(0, int(round(z / hop)) - i0)] = False
    rs = [[(i0 + x) * hop, (i0 + z) * hop] for x, z in runs_of(m)]
    if not rs:
        return []
    merged = [rs[0]]
    for r in rs[1:]:
        hole_cut = any(merged[-1][1] - 0.01 <= x and z <= r[0] + 0.01 for x, z in cuts)
        if r[0] - merged[-1][1] <= gap_min and not hole_cut:
            merged[-1][1] = r[1]
        else:
            merged.append(r)
    # a run with no voiced frame at all, standing alone, is a breath or a murmur: drop it
    merged = [r for r in merged if db[int(round(r[0] / hop)):int(round(r[1] / hop))].max() > hi]
    out = []
    for x, z in merged:
        lo_lim = max([a] + [cz for cx, cz in cuts if cz <= x + 1e-6])
        hi_lim = min([b] + [cx for cx, cz in cuts if cx >= z - 1e-6])
        out.append((max(lo_lim, x - pad), min(hi_lim, z + pad)))
    return out


def main():
    ap = add_project_arg(argparse.ArgumentParser())
    ap.add_argument("--keep")
    ap.add_argument("--gap-min", type=float, default=0.06)
    ap.add_argument("--pad", type=float, default=0.020)
    ap.add_argument("--soft-near", type=float, default=0.20)
    ap.add_argument("--out-dir", help="default: the project's work folder")
    a = ap.parse_args()
    P = Project(a.project)
    fps, off, rate = int(P["fps"]), float(P["offset"]), float(P.cfg.get("rate", 1.0))
    keep = load_keep(a.keep or P.work / "keep.json")
    out_dir = a.out_dir or P.work
    hop = 0.01

    y = load_audio(P.mic, sr=SR)
    db = db_strip(y, sr=SR, hop=hop)
    ref, hi, lo = thresholds_from(db, [(k["a"], k["b"]) for k in keep])
    print(f"speech ref {ref:.1f} dB -> T_high {hi:.1f}, T_low {lo:.1f}")
    dbm = db.copy()  # cut sub-spans are silenced first, so a breath next to a removed false start goes too
    for k in keep:
        for x, z in k["cut"]:
            dbm[int(round(x / hop)):int(round(z / hop))] = -120.0
    mask = speech_mask(dbm, hi, lo, a.soft_near, hop)

    pieces, t0, lines = [], 0, []
    for li, k in enumerate(keep, 1):
        n0 = len(pieces)
        for x, z in kept_runs(mask, dbm, hi, k["a"], k["b"], k["cut"], a.gap_min, a.pad, hop):
            fa, fb = int(round(x * fps)), int(round(z * fps))
            if fb - fa < 2:
                continue
            pieces.append({"a": fa / fps, "b": fb / fps, "t0": t0, "n": fb - fa,
                           "camF": int(round((fa / fps * rate + off) * fps)), "text": k["text"], "line": li, "lineA": k["a"]})
            t0 += fb - fa
        if len(pieces) == n0:
            print(f"[warn] line #{li} {k['a']:.2f}-{k['b']:.2f} kept nothing (no speech above T_high?)")
        else:
            lines.append({"line": li, "a": k["a"], "b": k["b"], "text": k["text"], "t0": pieces[n0]["t0"],
                          "n": t0 - pieces[n0]["t0"], "pieces": len(pieces) - n0})

    fl = int(FADE * SR)
    ramp = np.linspace(0, 1, fl, dtype=np.float32)
    segs = []
    for p in pieces:
        s = y[int(round(p["a"] * SR)): int(round(p["b"] * SR))].copy()
        s[:fl] *= ramp
        s[-fl:] *= ramp[::-1]
        segs.append(s)
    v = np.concatenate(segs) if segs else np.zeros(1, np.float32)
    v = v / (np.abs(v).max() + 1e-9) * 10 ** (-1 / 20)
    wav = os.path.join(out_dir, "voice-clean.wav")
    with wave.open(wav, "wb") as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(SR)
        wf.writeframes((np.clip(v, -1, 1) * 32767).astype(np.int16).tobytes())

    # silence audit on the result: the longest quiet run anywhere (he spots 0.3 s; target < 0.1 s)
    vdb = db_strip(v, sr=SR, hop=hop)
    quiet = sorted(((z - x) * hop, x * hop) for x, z in runs_of(vdb <= lo))[-5:][::-1]
    C = {"offset": off, "rate": rate, "fps": fps, "pieces": pieces, "totalF": t0, "total": t0 / fps, "lines": lines,
         "thresholds": {"ref": ref, "hi": hi, "lo": lo}}
    write_json(os.path.join(out_dir, "clean.json"), C)
    print(f"{len(keep)} lines -> {len(pieces)} pieces, {t0 / fps:.2f} s ({t0} frames)")
    print("longest quiet runs in the clean voice: " + ", ".join(f"{d:.2f} s @ {t:.2f}" for d, t in quiet))
    if quiet and quiet[0][0] > 0.15:
        print("[warn] a pause over 0.15 s survived: look at it (a soft word kept apart, or a cut too wide)")


if __name__ == "__main__":
    main()
