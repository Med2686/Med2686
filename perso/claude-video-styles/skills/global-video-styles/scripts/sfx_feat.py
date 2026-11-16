"""Shared audio features for the SFX tools (same features as the reference miner, so matches are comparable)."""
import numpy as np, soundfile as sf, librosa

SR = 44100


def load_mono(path, sr=SR):
    y, s = sf.read(path, always_2d=True)
    y = y.mean(1).astype(np.float32)
    if s != sr:
        y = librosa.resample(y, orig_sr=s, target_sr=sr)
    return y


def trim(y, sr=SR, floor_db=-50):
    """Cut leading silence (< floor relative to peak) and the tail below -60 dB."""
    if len(y) == 0: return y
    pk = np.max(np.abs(y)) + 1e-9
    a = np.abs(y) / pk
    idx = np.where(a > 10 ** (floor_db / 20))[0]
    if not len(idx): return y[:0]
    s = max(0, idx[0] - int(0.003 * sr))
    e = idx[np.where(a[idx] > 10 ** (-60 / 20))[0][-1]] + int(0.02 * sr)
    return y[s:min(len(y), e)]


def features(y, sr=SR):
    """Vector + dict describing a one-shot sound. Uses only the first 2.5 s."""
    y = y[: int(2.5 * sr)]
    if len(y) < 256: y = np.pad(y, (0, 256 - len(y)))
    S = np.abs(librosa.stft(y, n_fft=1024, hop_length=256)) + 1e-9
    fr = librosa.fft_frequencies(sr=sr, n_fft=1024)
    cen = (S * fr[:, None]).sum(0) / S.sum(0)
    tot = S.sum()
    low = float(S[fr < 150].sum() / tot); high = float(S[fr > 5000].sum() / tot)
    flat = float(np.mean(librosa.feature.spectral_flatness(S=S)))
    mf = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=13).mean(1)
    rms = librosa.feature.rms(y=y, frame_length=1024, hop_length=256)[0]
    att = float(np.argmax(rms) * 256 / sr)
    dur = len(y) / sr
    q = max(1, len(cen) // 4)
    c0, c1 = float(np.mean(cen[:q])), float(np.mean(cen[-q:]))
    vec = np.array([np.log(dur), att, np.log(c0), np.log(c1), np.log(c1 / c0), low, high, flat, *mf[1:8]], dtype=np.float32)
    info = {"dur": round(dur, 3), "attack": round(att, 3), "cen_start": int(c0), "cen_end": int(c1), "low": round(low, 3),
            "high": round(high, 3), "flat": round(flat, 3)}
    return vec, info


def qc(y, sr=SR):
    """Quality numbers: clipping, noise floor (quietest 50 ms window rel. to peak), bandwidth (highest freq within 60 dB of the spectral peak)."""
    pk = float(np.max(np.abs(y)) + 1e-12)
    clipped = int(np.sum(np.abs(y) >= 0.999))
    w = int(0.05 * sr)
    floors = [20 * np.log10(np.sqrt(np.mean(y[i:i + w] ** 2)) + 1e-12) for i in range(0, max(1, len(y) - w), w)]
    floor = float(min(floors) - 20 * np.log10(pk)) if floors else 0.0
    spec = np.abs(np.fft.rfft(y[: sr * 3])) + 1e-12
    f = np.fft.rfftfreq(len(y[: sr * 3]), 1 / sr)
    sdb = 20 * np.log10(spec / spec.max())
    sm = np.convolve(sdb, np.ones(64) / 64, mode="same")
    bw = float(f[np.where(sm > -60)[0][-1]]) if np.any(sm > -60) else 0.0
    return {"peak_db": round(20 * np.log10(pk), 1), "clipped": clipped, "floor_db": round(floor, 1), "bandwidth_hz": int(bw)}
