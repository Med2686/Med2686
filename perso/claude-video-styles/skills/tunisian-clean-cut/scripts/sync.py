"""Sync the separate mic to the camera: camera_t = mic_t * rate + offset.

  python -I sync.py -p <project> [--write]
  python -I sync.py --mic-file m.wav --cam-file c.wav --mic-range 30-45 --cam-range 45-65   (test on slices)

1. Coarse: loudness envelopes of both at 100 Hz, FFT cross-correlation -> lag to 10 ms.
2. Fine: in 3 loud windows of the mic (early / middle / late), cross-correlate the raw 16 kHz waveforms
   within +-60 ms of the coarse lag, parabolic peak -> sample-level offset at each place.
3. Drift: offset(late) - offset(early). Under ~20 ms over the take it is ignored (rate = 1). Above, rate is
   fitted so the camera frames stay on the voice to the end. Reel-ref-edit: offset 20.666 s, drift 6 ms.
--write stores offset / rate / drift_ms in project.json. Always look at the 3 local offsets: if one is far
from the others, a window fell on noise; rerun with --windows.
"""
import argparse
import os
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from tcc_common import SR16, Project, add_project_arg, db_strip, load_audio  # noqa: E402


def env(y):
    d = db_strip(y)
    d = np.clip(d, np.percentile(d, 30), None)
    return (d - d.mean()) / (d.std() + 1e-9)


def xcorr_lag(a, b):
    """lag L (samples) maximising sum a[t] * b[t + L]  (b is later by L)."""
    n = len(a) + len(b)
    f = np.fft.irfft(np.conj(np.fft.rfft(a, n)) * np.fft.rfft(b, n), n)
    f = np.concatenate([f[-(len(a) - 1):], f[:len(b)]])  # lags -(len(a)-1) .. len(b)-1
    k = int(np.argmax(f))
    return k - (len(a) - 1), f[k] / (np.linalg.norm(a) * np.linalg.norm(b) + 1e-9)


def fine(mic, cam, t_mic, off0, win=4.0, search=0.06):
    a = mic[int(t_mic * SR16): int((t_mic + win) * SR16)]
    c0 = int((t_mic + off0 - search) * SR16)
    c = cam[max(0, c0): int((t_mic + off0 + win + search) * SR16)]
    if len(a) < SR16 or len(c) < len(a):
        return None
    n = len(c) - len(a) + 1
    f = np.fft.irfft(np.conj(np.fft.rfft(a, len(c) + len(a))) * np.fft.rfft(c, len(c) + len(a)), len(c) + len(a))[:n]
    k = int(np.argmax(f))
    if 0 < k < n - 1:  # parabolic interpolation
        y0, y1, y2 = f[k - 1], f[k], f[k + 1]
        k = k + 0.5 * (y0 - y2) / (y0 - 2 * y1 + y2 + 1e-12)
    return (max(0, c0) + k) / SR16 - t_mic


def main():
    ap = add_project_arg(argparse.ArgumentParser())
    ap.add_argument("--mic-file")
    ap.add_argument("--cam-file")
    ap.add_argument("--mic-range")
    ap.add_argument("--cam-range")
    ap.add_argument("--windows", help="mic times for the fine pass, e.g. 30,150,300")
    ap.add_argument("--write", action="store_true")
    a = ap.parse_args()
    P = Project(a.project)
    mic_f = a.mic_file or P.work / "mic16k.wav"
    cam_f = a.cam_file or P.work / "cam16k.wav"
    m0, m1 = map(float, a.mic_range.split("-")) if a.mic_range else (0, None)
    c0, c1 = map(float, a.cam_range.split("-")) if a.cam_range else (0, None)
    mic = load_audio(mic_f, start=m0 or None, dur=(m1 - m0) if m1 else None)
    cam = load_audio(cam_f, start=c0 or None, dur=(c1 - c0) if c1 else None)
    lag, score = xcorr_lag(env(mic), env(cam))
    off0 = lag * 0.01  # local: cam_local = mic_local + off0
    print(f"coarse: camera_t = mic_t + {off0 + c0 - m0:.2f} s (corr {score:.2f})")
    dur = len(mic) / SR16
    d = db_strip(mic)
    if a.windows:
        ts = [float(t) - m0 for t in a.windows.split(",")]
    else:
        ts = []
        for frac in (0.15, 0.5, 0.85):
            i = int(frac * len(d))
            j = i + int(np.argmax([d[k:k + 400].mean() for k in range(i, max(i + 1, min(len(d) - 400, i + 1500)), 50)]) * 50)
            ts.append(min(j * 0.01, max(0, dur - 4.5)))
    offs = []
    for t in ts:
        o = fine(mic, cam, t, off0)
        if o is not None:
            offs.append((t, o))
            print(f"  fine @ mic {t + m0:7.2f} s: offset {o + c0 - m0:.4f} s")
    if not offs:
        sys.exit("fine pass failed: give --windows on loud speech")
    o_early, o_late = offs[0][1], offs[-1][1]
    span = offs[-1][0] - offs[0][0]
    drift = (o_late - o_early) * 1000
    rate = 1.0 + (o_late - o_early) / span if span > 0 and abs(drift) > 20 else 1.0
    offset = (offs[0][1] - (rate - 1) * offs[0][0]) + c0 - m0 * rate
    print(f"offset {offset:.3f} s, drift {drift:+.1f} ms over {span:.0f} s, rate {rate:.7f}")
    if a.write:
        P.cfg.update({"offset": round(float(offset), 4), "rate": float(rate), "drift_ms": round(float(drift), 1)})
        P.save()
        print("written to", P.cfg_path)


if __name__ == "__main__":
    main()
