"""Procedural sound-effect synthesiser — the fallback when no library sound is good enough. 48 kHz, 24-bit stereo, clean (no noise floor).

usage:  python sfx_synth.py <kind> <out.wav> [key=value ...]
kinds and main params (all optional):
  whoosh   dur=0.6 lo=300 hi=6000 shape=updown|up|down peak=0.6 pan=1 air=0.5     filtered-noise pass-by with stereo sweep
  prelap   dur=0.45                                                               short rising whoosh that ENDS on the visual hit (Dark Teal word)
  whoomp   dur=0.7 sub=55 top=0.35                                                deep swoosh + sub swell (Violet Glass streak transition)
  riser    dur=1.2 lo=400 hi=9000 tone=1                                          noise + pitch sweep up, cut at the end (into a scene)
  boom     dur=0.9 f0=58 f1=34 click=0.5                                          sub impact with transient
  thump    dur=0.25 f=90                                                          soft low thud (stamp / camera shake)
  pop      f=700 dur=0.06                                                         soft UI pop (tags, chips)
  ping     f=1100 dur=0.35 h=0.25                                                 card ping (E10 donut card: 1.1 kHz)
  tick     f=3200 dur=0.03                                                        node tick / step
  blip     f=1800 f2=2600 dur=0.09                                                two-tone UI blip
  sparkle  dur=0.6 density=60 lo=4500 hi=12000 sweep=1                            glass shimmer grains + falling tone (Violet sparkle)
  click    dur=0.04                                                               mouse/button click
  smear    dur=0.35 f0=9000 f1=1500                                               streak smear (fast falling tone + noise) for a click/flash
  roll     dur=1.2 n=18                                                           counter digit roll (ticks that slow down)
  typing   dur=2.0 rate=9                                                          soft key clicks
  stamp    dur=0.4                                                                rubber stamp: thump + paper noise
  glitch   dur=0.3                                                                bit-crushed noise chops
Run with ~/.venvs/claude-video/Scripts/python.exe. Listen before using; tweak params; save good ones to sfx/bank/.
"""
import sys, numpy as np, soundfile as sf

SR = 48000
rng = np.random.default_rng(7)


def env_adsr(n, a, d, peak_at=None, curve=2.0):
    t = np.linspace(0, 1, n)
    if peak_at is not None:
        e = np.where(t < peak_at, (t / peak_at) ** curve, ((1 - t) / (1 - peak_at)) ** curve)
        return e
    A = max(1, int(a * SR)); e = np.ones(n)
    e[:A] = np.linspace(0, 1, A) ** 0.7
    e[A:] = np.exp(-np.arange(n - A) / (d * SR))
    return e


def band_noise(n, centers, width=0.35):
    """Noise whose spectrum follows a moving centre frequency (log-gaussian band), via STFT masking."""
    hop, nfft = 256, 2048
    frames = n // hop + 2
    X = (rng.standard_normal((nfft // 2 + 1, frames)) + 1j * rng.standard_normal((nfft // 2 + 1, frames)))
    f = np.linspace(0, SR / 2, nfft // 2 + 1) + 1
    cs = np.interp(np.linspace(0, 1, frames), np.linspace(0, 1, len(centers)), centers)
    mask = np.exp(-0.5 * ((np.log(f)[:, None] - np.log(cs)[None, :]) / width) ** 2)
    X *= mask
    import librosa
    y = librosa.istft(X, hop_length=hop, n_fft=nfft, length=n)
    return y / (np.max(np.abs(y)) + 1e-9)


def sweep(n, f0, f1, kind="exp"):
    t = np.arange(n) / SR
    if kind == "exp":
        f = f0 * (f1 / f0) ** (t / (t[-1] + 1e-9))
    else:
        f = np.linspace(f0, f1, n)
    return np.sin(2 * np.pi * np.cumsum(f) / SR)


def stereo(y, pan_from=0.0, pan_to=0.0, width=0.0):
    p = np.linspace(pan_from, pan_to, len(y))
    l = y * np.cos((p + 1) * np.pi / 4); r = y * np.sin((p + 1) * np.pi / 4)
    if width:
        d = int(0.012 * SR); r = (1 - width) * r + width * np.concatenate([np.zeros(d), r[:-d]])
    return np.stack([l, r], 1)


def room(x, size=0.25, mix=0.12):
    n = int(size * SR); ir = rng.standard_normal(n) * np.exp(-np.arange(n) / (0.25 * n))
    ir /= np.sqrt(np.sum(ir ** 2))
    out = np.stack([np.convolve(x[:, c], ir)[: len(x)] for c in range(x.shape[1])], 1)
    return (1 - mix) * x + mix * out


def finish(x, tail=0.01):
    x = x / (np.max(np.abs(x)) + 1e-9) * 10 ** (-1 / 20)
    f = int(tail * SR); x[-f:] *= np.linspace(1, 0, f)[:, None]
    return x


def make(kind, p):
    g = lambda k, d: float(p.get(k, d))
    if kind == "whoosh":
        n = int(g("dur", .6) * SR); lo, hi = g("lo", 300), g("hi", 6000); shape = p.get("shape", "updown")
        cs = {"up": [lo, hi], "down": [hi, lo], "updown": [lo, hi, lo * 1.5]}[shape]
        y = band_noise(n, cs, 0.45) * env_adsr(n, 0, 0, peak_at=g("peak", .6))
        air = band_noise(n, [hi * 1.2, hi * 1.5], 0.3) * env_adsr(n, 0, 0, peak_at=g("peak", .6), curve=3) * g("air", .5)
        x = stereo(y + air, -g("pan", 1) * .8, g("pan", 1) * .8, 0.3); return room(x, .3, .1)
    if kind == "prelap":
        n = int(g("dur", .45) * SR)
        y = band_noise(n, [600, 2500, 7000], 0.5) * env_adsr(n, 0, 0, peak_at=0.92, curve=2.5)
        return stereo(y, -.3, .3, .3)
    if kind == "whoomp":
        n = int(g("dur", .7) * SR); sub = g("sub", 55)
        body = band_noise(n, [120, 450, 180], 0.55) * env_adsr(n, 0, 0, peak_at=.28, curve=1.6)
        s = sweep(n, sub * .8, sub * 1.6) * env_adsr(n, 0, 0, peak_at=.3, curve=1.4) * 0.8
        top = band_noise(n, [2500, 6000, 3000], 0.4) * env_adsr(n, 0, 0, peak_at=.3, curve=2.2) * g("top", .35)
        return room(stereo(body + s + top, -.6, .6, .35), .4, .15)
    if kind == "riser":
        n = int(g("dur", 1.2) * SR)
        y = band_noise(n, [g("lo", 400), g("hi", 9000)], 0.5) * np.linspace(0, 1, n) ** 2.2
        t = sweep(n, 180, 1400) * np.linspace(0, 1, n) ** 2.5 * 0.35 * g("tone", 1)
        return room(stereo(y + t, 0, 0, .4), .5, .18)
    if kind == "boom":
        n = int(g("dur", .9) * SR)
        b = sweep(n, g("f0", 58), g("f1", 34)) * env_adsr(n, .004, .32)
        c = band_noise(n, [3000, 800], 0.8) * env_adsr(n, .001, .03) * g("click", .5)
        return room(stereo(b + c), .6, .2)
    if kind == "thump":
        n = int(g("dur", .25) * SR); return stereo(sweep(n, g("f", 90), g("f", 90) * .6) * env_adsr(n, .002, .06) + band_noise(n, [600], .6) * env_adsr(n, .001, .015) * .3)
    if kind == "pop":
        n = int(g("dur", .06) * SR + .1 * SR); f = g("f", 700)
        y = sweep(n, f * 1.4, f) * env_adsr(n, .002, .025) + band_noise(n, [f * 3], .4) * env_adsr(n, .001, .008) * .25
        return room(stereo(y), .15, .08)
    if kind == "ping":
        n = int(g("dur", .35) * SR); f = g("f", 1100)
        y = (np.sin(2 * np.pi * f * np.arange(n) / SR) + g("h", .25) * np.sin(2 * np.pi * 2.01 * f * np.arange(n) / SR)) * env_adsr(n, .003, g("dur", .35) / 3.5)
        return room(stereo(y), .3, .15)
    if kind == "tick":
        n = int(g("dur", .03) * SR + .05 * SR); f = g("f", 3200)
        return stereo(np.sin(2 * np.pi * f * np.arange(n) / SR) * env_adsr(n, .0005, .006))
    if kind == "blip":
        n = int(g("dur", .09) * SR); h = n // 2; f, f2 = g("f", 1800), g("f2", 2600)
        y = np.concatenate([np.sin(2 * np.pi * f * np.arange(h) / SR), np.sin(2 * np.pi * f2 * np.arange(n - h) / SR)]) * env_adsr(n, .002, .03)
        return room(stereo(y), .2, .1)
    if kind == "sparkle":
        n = int(g("dur", .6) * SR); y = np.zeros(n)
        for _ in range(int(g("density", 60))):
            s = int(rng.uniform(0, 0.7) * n); f = rng.uniform(g("lo", 4500), g("hi", 12000)); ln = int(rng.uniform(.02, .09) * SR)
            if s + ln >= n: continue
            y[s:s + ln] += np.sin(2 * np.pi * f * np.arange(ln) / SR) * env_adsr(ln, .002, .015) * rng.uniform(.2, 1)
        if g("sweep", 1): y += sweep(n, 9000, 2500) * env_adsr(n, .01, .18) * .35
        y *= np.linspace(1, .3, n)
        x = np.stack([np.roll(y, int(rng.integers(0, 200))), y], 1); return room(x, .5, .25)
    if kind == "click":
        n = int(g("dur", .04) * SR + .03 * SR)
        y = band_noise(n, [3500], .5) * env_adsr(n, .0003, .004); y[int(.012 * SR):] += band_noise(n - int(.012 * SR), [2200], .5) * env_adsr(n - int(.012 * SR), .0003, .005) * .6
        return stereo(y)
    if kind == "smear":
        n = int(g("dur", .35) * SR)
        y = sweep(n, g("f0", 9000), g("f1", 1500)) * env_adsr(n, .002, .09) * .6 + band_noise(n, [6000, 1500], .5) * env_adsr(n, .002, .08)
        return room(stereo(y, .4, -.4, .3), .3, .15)
    if kind == "roll":
        dur = g("dur", 1.2); n = int(dur * SR); y = np.zeros(n); k = int(g("n", 18))
        times = dur * np.linspace(0, 1, k) ** 1.8  # gaps grow = the counter slows down as it lands
        for i, t in enumerate(times):
            s = int(t * .95 * SR); ln = int(.025 * SR)
            if s + ln < n: y[s:s + ln] += np.sin(2 * np.pi * (2600 + 30 * i) * np.arange(ln) / SR) * env_adsr(ln, .0005, .005)
        return stereo(y)
    if kind == "typing":
        dur = g("dur", 2.0); n = int(dur * SR); y = np.zeros(n); t = 0.0
        while t < dur - .05:
            s = int(t * SR); ln = int(.03 * SR)
            y[s:s + ln] += band_noise(ln, [rng.uniform(1800, 4200)], .35) * env_adsr(ln, .0005, .006) * rng.uniform(.5, 1)
            t += rng.exponential(1 / g("rate", 9)) + .03
        return room(stereo(y), .2, .12)
    if kind == "stamp":
        n = int(g("dur", .4) * SR)
        y = sweep(n, 95, 60) * env_adsr(n, .002, .07) + band_noise(n, [1800, 900], .7) * env_adsr(n, .001, .05) * .7
        return room(stereo(y), .25, .12)
    if kind == "glitch":
        n = int(g("dur", .3) * SR); y = band_noise(n, [2500], 1.2)
        step = int(.012 * SR)
        for i in range(0, n, step):
            if rng.random() < .45: y[i:i + step] = 0
            else: y[i:i + step] = np.round(y[i:i + step] * 6) / 6
        return stereo(y * env_adsr(n, .002, .12))
    raise SystemExit(__doc__)


if __name__ == "__main__":
    if len(sys.argv) < 3: raise SystemExit(__doc__)
    kind, out = sys.argv[1], sys.argv[2]
    params = dict(a.split("=", 1) for a in sys.argv[3:])
    x = finish(make(kind, params))
    sf.write(out, x, SR, subtype="PCM_24"); print("wrote", out, f"{len(x) / SR:.2f}s")
