"""Shared helpers for the tunisian-clean-cut scripts (Windows only, no WSL).

- project config (project.json in the project folder)
- audio loading through ffmpeg (never a file path into faster-whisper: PyAV in the venv breaks)
- CUDA DLL registration for faster-whisper on the RTX
- 10 ms loudness strips, hysteresis thresholds, bursts split on dips
- Whisper passes (ar with a Derja prompt, fr, en; optional "verbatim" prompts that invite repeats)
- hallucination filter, spelling normalisation, fuzzy n-gram repeat finder

Every script puts this folder on sys.path itself, so `python -I script.py` works.
"""
from __future__ import annotations

import glob
import json
import os
import re
import subprocess
import sys
import unicodedata
from difflib import SequenceMatcher
from pathlib import Path

import numpy as np

SKILL = Path(__file__).resolve().parent.parent
VENV_PY = os.environ.get("CLAUDE_VIDEO_PY", str(Path.home() / ".venvs" / "claude-video" / "Scripts" / "python.exe"))
SYS_PY = os.environ.get("CLAUDE_VIDEO_GAZE_PY", VENV_PY)  # python with mediapipe + opencv (gaze cover)
MODELS = Path(os.environ.get("LOCALAPPDATA", str(Path.home() / "AppData" / "Local"))) / "reel-pro-edit" / "models"
REEL_PRO_EDIT = SKILL / "scripts"  # gaze.py is bundled here
SR16 = 16000
HOP = 0.01  # loudness strip resolution (10 ms)


def utf8_stdout() -> None:
    """With python -I, PYTHONIOENCODING is ignored: Arabic would crash the console without this."""
    for s in (sys.stdout, sys.stderr):
        try:
            s.reconfigure(encoding="utf8")
        except Exception:
            pass


utf8_stdout()


# ----------------------------------------------------------------------------- project config
DEFAULT_CFG = {
    "camera": None,          # camera file (iPhone MOV etc.)
    "mic": None,             # separate mic recording; null = use the camera audio
    "offset": 0.0,           # camera_t = mic_t + offset (seconds)
    "drift_ms": None,
    "fps": 30,
    "work": "work",
    "remotion": "remotion-video",
    "screen_side": "left",   # image side of the script screen he reads from
    "gaze_seed": 0.4,
    "gaze_min_frames": 10,
}


class Project:
    def __init__(self, root: str | Path | None = None):
        self.root = Path(root or os.getcwd()).resolve()
        self.cfg_path = self.root / "project.json"
        cfg = dict(DEFAULT_CFG)
        if self.cfg_path.exists():
            cfg.update(json.loads(self.cfg_path.read_text(encoding="utf8")))
        self.cfg = cfg

    def __getitem__(self, k):
        return self.cfg[k]

    def save(self) -> None:
        self.cfg_path.write_text(json.dumps(self.cfg, ensure_ascii=False, indent=1), encoding="utf8")

    @property
    def work(self) -> Path:
        w = self.root / self.cfg["work"]
        w.mkdir(parents=True, exist_ok=True)
        return w

    @property
    def remotion(self) -> Path:
        return self.root / self.cfg["remotion"]

    @property
    def mic(self) -> Path:
        return Path(self.cfg["mic"] or self.cfg["camera"])

    @property
    def camera(self) -> Path:
        return Path(self.cfg["camera"])

    def mic16(self) -> Path:
        """16 kHz mono copy of the mic, made once by prep.py (falls back to the source)."""
        p = self.work / "mic16k.wav"
        return p if p.exists() else self.mic


def add_project_arg(ap):
    ap.add_argument("--project", "-p", default=None, help="project folder holding project.json (default: cwd)")
    return ap


def read_json(p):
    return json.loads(Path(p).read_text(encoding="utf8"))


def write_json(p, obj, indent=1):
    Path(p).write_text(json.dumps(obj, ensure_ascii=False, indent=indent), encoding="utf8")


# ----------------------------------------------------------------------------- audio
def load_audio(path, sr=SR16, start=None, dur=None) -> np.ndarray:
    cmd = ["ffmpeg", "-v", "error", "-nostdin"]
    if start is not None:
        cmd += ["-ss", f"{start:.3f}"]
    if dur is not None:
        cmd += ["-t", f"{dur:.3f}"]
    cmd += ["-i", str(path), "-vn", "-ac", "1", "-ar", str(sr), "-f", "f32le", "-"]
    pcm = subprocess.run(cmd, capture_output=True, check=True).stdout
    return np.frombuffer(pcm, np.float32).copy()


def db_strip(y: np.ndarray, sr=SR16, hop=HOP) -> np.ndarray:
    h = int(sr * hop)
    n = len(y) // h
    return 20 * np.log10(np.sqrt((y[: n * h].reshape(n, h) ** 2).mean(1)) + 1e-9)


def thresholds_from(db: np.ndarray, spans=None, hop=HOP):
    """ref = p90 of speech frames. T_high = ref-13 (a burst must peak above it), T_low = ref-23 (it extends
    while above). With spans (the keep list) the ref comes from them; without, from frames well above the floor."""
    if spans:
        vals = np.concatenate([db[int(a / hop): int(b / hop)] for a, b in spans])
    else:
        floor = np.percentile(db, 20)
        vals = db[db > floor + 15]
        if len(vals) < 50:
            vals = db
    ref = float(np.percentile(vals, 90))
    return ref, ref - 13, ref - 23


def runs_of(mask: np.ndarray):
    """[(i, j)] index runs where mask is True."""
    out, i, n = [], 0, len(mask)
    while i < n:
        if not mask[i]:
            i += 1
            continue
        j = i
        while j < n and mask[j]:
            j += 1
        out.append((i, j))
        i = j
    return out


def speech_mask(db: np.ndarray, hi: float, lo: float, soft_near=0.20, hop=HOP) -> np.ndarray:
    """Hysteresis mask: a run above T_low is speech if it peaks above T_high; a soft run (never above
    T_high) still counts when it sits within soft_near s of a voiced burst (word tails: the « s », « kol »)."""
    runs = [(a, b, db[a:b].max() > hi) for a, b in runs_of(db > lo)]
    mask = np.zeros(len(db), bool)
    strong = [(a, b) for a, b, v in runs if v]
    for a, b in strong:
        mask[a:b] = True
    if strong:
        sa = np.array([a for a, _ in strong])
        sb = np.array([b for _, b in strong])
        for a, b, v in runs:
            if not v and np.minimum(np.abs(sa - b), np.abs(a - sb)).min() <= soft_near / hop:
                mask[a:b] = True
    return mask


def boundaries_in(db, a, b, hi, lo, min_gap=0.06, notch_depth=18.0, notch_reach=3.0, hop=HOP):
    """Every place inside [a,b] (s) where a take can start again. Two kinds:
    - 'gap'  : the level stays under T_low for >= min_gap s (a breath-length pause);
    - 'notch': a short valley that reaches T_low+notch_reach dB and lies >= notch_depth dB under the loudest
               frame within 150 ms on BOTH sides. A false start is often glued to its retake by a 20-30 ms
               notch that never makes a gap: « ou la cap|ou la capacité » (mic 238.59, -58 dB between -25 and -21).
    Notches also fall between ordinary words: a boundary is a place to LOOK, not a cut.
    Returns sorted [(t_s, kind, depth_db)], t = the quietest 10 ms frame."""
    i0, i1 = max(0, int(round(a / hop))), min(len(db), int(round(b / hop)))
    out = []
    # gaps
    for x, z in runs_of(db[i0:i1] <= lo):
        if (z - x) * hop >= min_gap and x > 0 and i0 + z < i1:
            k = i0 + x + int(np.argmin(db[i0 + x:i0 + z]))
            out.append((round(k * hop, 2), "gap", round(float(db[max(i0, k - 15):k].max() - db[k]), 1)))
    gap_spans = [(t - 0.5, t + 0.5) for t, kind, _ in out]
    # notches
    sm = np.convolve(db, np.ones(3) / 3, mode="same")
    k = i0 + 3
    while k < i1 - 3:
        if sm[k] == sm[k - 3:k + 4].min() and sm[k] <= lo + notch_reach:
            L = sm[max(i0, k - 15):k].max()
            R = sm[k + 1:min(i1, k + 16)].max()
            if L - sm[k] >= notch_depth and R - sm[k] >= notch_depth:
                t = round(k * hop, 2)
                if not any(abs(t - g) < 0.08 for g, _, _ in out):
                    out.append((t, "notch", round(float(min(L, R) - sm[k]), 1)))
                k += 5
                continue
        k += 1
    return sorted(out)


def speech_edges(db, a, b, lo, hop=HOP):
    """First and last frame above T_low inside [a,b] (s)."""
    i0, i1 = int(round(a / hop)), int(round(b / hop))
    on = np.where(db[i0:i1] > lo)[0]
    if not len(on):
        return a, b
    return round((i0 + on[0]) * hop, 2), round((i0 + on[-1] + 1) * hop, 2)


# ----------------------------------------------------------------------------- acoustic echo
_FB = None


def _mfcc(y, a, b, sr=SR16):
    global _FB
    from scipy.fft import dct
    nfft = 512
    if _FB is None:
        mel = lambda f: 2595 * np.log10(1 + f / 700)
        imel = lambda m: 700 * (10 ** (m / 2595) - 1)
        pts = imel(np.linspace(mel(80), mel(7600), 42))
        bins = np.floor((nfft + 1) * pts / sr).astype(int)
        _FB = np.zeros((40, nfft // 2 + 1))
        for i in range(40):
            x, m, z = bins[i], bins[i + 1], bins[i + 2]
            _FB[i, x:m] = (np.arange(x, m) - x) / max(1, m - x)
            _FB[i, m:z] = (z - np.arange(m, z)) / max(1, z - m)
    s = slice_of(y, a, b)
    if len(s) < 400:
        s = np.pad(s, (0, 400 - len(s)))
    n = (len(s) - 400) // 160 + 1
    win = np.hanning(400)
    fr = np.stack([s[i * 160:i * 160 + 400] * win for i in range(n)])
    P = np.abs(np.fft.rfft(fr, nfft)) ** 2
    return dct(np.log(P @ _FB.T + 1e-8), type=2, axis=1, norm="ortho")[:, 1:14]


def _dtw_open(A, B):
    D = np.sqrt(((A[:, None, :] - B[None, :, :]) ** 2).sum(-1))
    n, m = D.shape
    acc = np.full((n + 1, m + 1), np.inf)
    acc[0, 0] = 0
    for i in range(1, n + 1):
        row, prev = acc[i], acc[i - 1]
        for j in range(1, m + 1):
            row[j] = D[i - 1, j - 1] + min(prev[j], row[j - 1], prev[j - 1])
    j0 = max(1, int(n * 0.6))
    js = np.arange(j0, m + 1)
    return float((acc[n, j0:] / (n + js)).min())


def echo_z(y, left_a, k, span_a, span_b):
    """Does the chunk [left_a, k] sound like the start of what follows k? (a false start re-said).
    MFCC + open-end DTW, scored against the same chunk compared with other places of the span.
    z >= 2 is a lead (« learn|learn » scored 3.9); ordinary word joins stay under ~1.5. Leads only."""
    L = k - left_a
    if L < 0.12:
        return 0.0
    A = _mfcc(y, left_a, k)
    e = _dtw_open(A, _mfcc(y, k, k + L * 1.6))
    base = [_dtw_open(A, _mfcc(y, t, t + L * 1.6)) for t in np.arange(span_a, span_b - L, 0.15)
            if (t + L * 1.6 < left_a or t > k + 0.2)]
    if len(base) < 6:  # too little of the span to compare with: z would be noise (a 2 s line gave z 7.6 on a clean join)
        return 0.0
    return round(float((np.mean(base) - e) / (np.std(base) + 1e-6)), 2)


def strip_text(db, a, b, lo, hi, hop=HOP, every=0.02):
    """Compact loudness strip: one char per `every` s.  # above T_high, + above T_low, . below T_low."""
    step = max(1, int(round(every / hop)))
    i0, i1 = int(round(a / hop)), int(round(b / hop))
    ch = []
    for i in range(i0, min(i1, len(db)), step):
        v = db[i:i + step].max()
        ch.append("#" if v > hi else "+" if v > lo else ".")
    return "".join(ch)


# ----------------------------------------------------------------------------- whisper
PROMPTS = {
    # Derja vocabulary in Arabic script: steers the ar pass towards Tunisian (it still drifts to MSA)
    "ar": "شنوة، برشا، باش، كيفاش، يعني، ماكش، نحب نقلك، توا، هكا، الـ AI، prompt، creative، intelligent، résultat، concept",
    "fr": "Bon, en fait, l'IA, prompt, créatif, intelligent, résultat, concept, barcha, chnowa, ya3ni, tawa",
    "en": None,
}
# disfluent prompts: Whisper imitates the style and writes repeats it would otherwise tidy away.
# Evidence only (it can invent repeats too): confirm every hit on the loudness strip.
VERBATIM = {
    # neutral content on purpose: a prompt that contains the words of the clip makes Whisper "hear" them
    "fr": "Euh, je, je pense que, que c'est, bon, c'est ça, on, on va voir. Le, le conteneur, euh, c'est une, une image.",
    "en": "So, uh, I I think that, that it's, um, it's the, the right one. And and then, uh, we, we go.",
    "ar": None,
}

_MODEL = None


def cuda_setup() -> None:
    """faster-whisper on Windows needs the pip nvidia DLLs registered, else `cublas64_12.dll not found`."""
    site = Path(sys.executable).resolve().parent.parent / "Lib" / "site-packages"
    dirs = glob.glob(str(site / "nvidia" / "*" / "bin")) or glob.glob(
        str(Path(VENV_PY).parent.parent / "Lib" / "site-packages" / "nvidia" / "*" / "bin"))
    for d in dirs:
        os.add_dll_directory(d)
        os.environ["PATH"] = d + os.pathsep + os.environ["PATH"]


def model(name="large-v3"):
    global _MODEL
    if _MODEL is None:
        cuda_setup()
        from faster_whisper import WhisperModel
        try:
            _MODEL = WhisperModel(name, device="cuda", compute_type="float16")
        except Exception as e:  # no GPU: slow but works
            print(f"[warn] CUDA failed ({e}); using CPU int8", file=sys.stderr)
            _MODEL = WhisperModel(name, device="cpu", compute_type="int8")
    return _MODEL


def transcribe(seg: np.ndarray, lang: str, t0: float, prompt="default", pad=0.25, words=True, raw=False):
    """Transcribe one numpy slice that starts at absolute time t0 (s). pad = zero padding on both sides
    (0.25 s keeps Whisper from pinning/clipping the first and last word). Returns (text, [(w, s, e, p)]).
    Hallucinations and prompt recitals come back empty, or tagged « [NON-SPEECH] … » with raw=True."""
    if prompt == "default":
        prompt = PROMPTS.get(lang)
    p = int(pad * SR16)
    x = np.concatenate([np.zeros(p, np.float32), seg.astype(np.float32), np.zeros(p, np.float32)]) if p else seg
    ss, _ = model().transcribe(x, language=lang, word_timestamps=words, beam_size=5, initial_prompt=prompt,
                               condition_on_previous_text=False, vad_filter=False, temperature=0.0)
    ss = list(ss)
    text = " ".join(s.text.strip() for s in ss).strip()
    if is_hallu(text) or prompt_echo(text, prompt):  # non-speech: Whisper hallucinated or recited its prompt
        return ("[NON-SPEECH] " + text, []) if raw else ("", [])
    ws = []
    if words:
        for s in ss:
            for w in s.words or []:
                ws.append((w.word.strip(), round(t0 - pad + w.start, 2), round(t0 - pad + w.end, 2), round(w.probability, 2)))
    return text, ws


def slice_of(y, a, b, sr=SR16):
    return y[max(0, int(a * sr)): max(0, int(b * sr))]


# ----------------------------------------------------------------------------- hallucinations
HALLU = [
    r"sous-?titr", r"ST' ?501", r"amara\.org", r"thanks? (you )?for watching", r"we'll be right back",
    r"merci d'avoir regard", r"abonnez-vous", r"subscribe", r"ترجمة", r"اشتركوا", r"القناة", r"شكرا للمشاهدة",
    r"نانسي", r"قنقر", r"\[musi", r"musique\]", r"♪", r"enjoy the video", r"see you (in the )?next",
    r"like and subscribe", r"n'oubliez pas", r"نلتقي", r"شكرا لكم",
]
_HALLU_RE = re.compile("|".join(HALLU), re.I)


def prompt_echo(text: str, prompt) -> bool:
    """Whisper recites its initial_prompt on noise (« l'IA, prompt, créatif, intelligent, résultat… »)."""
    if not prompt or not text:
        return False
    t, pr = norm_tokens(text), set(norm_tokens(prompt))
    return len(t) >= 3 and sum(w in pr for w in t) / len(t) >= 0.6


def is_hallu(text: str) -> bool:
    """These lines mark NON-speech (breath, room noise, silence). Never treat them as words he said."""
    return bool(_HALLU_RE.search(text or ""))


# ----------------------------------------------------------------------------- normalisation + repeats
_AR_MAP = str.maketrans({"أ": "ا", "إ": "ا", "آ": "ا", "ٱ": "ا", "ة": "ه", "ى": "ي", "ؤ": "و", "ئ": "ي", "ـ": ""})


def norm_tokens(text: str) -> list[str]:
    t = unicodedata.normalize("NFKD", (text or "").lower())
    t = "".join(c for c in t if not unicodedata.combining(c)).translate(_AR_MAP)
    t = re.sub(r"[’`´]", "'", t)
    t = re.sub(r"[^\w']+", " ", t).replace("'", " ")
    toks = []
    for w in t.split():
        if w.startswith("ال") and len(w) > 3:  # Arabic article: الكل ~ كل
            w = w[2:]
        toks.append(w)
    return [w for w in toks if w]


def tok_eq(x: str, y: str) -> bool:
    if x == y:
        return True
    if min(len(x), len(y)) >= 3 and (x.startswith(y) or y.startswith(x)):
        return True  # truncated false start: « cap » ~ « capacité »
    return min(len(x), len(y)) >= 4 and SequenceMatcher(None, x, y).ratio() >= 0.8


def seq_eq(A, B) -> bool:
    if len(A) != len(B):
        return False
    bad = sum(not tok_eq(a, b) for a, b in zip(A, B))
    return bad == 0 or (len(A) >= 4 and bad <= 1)


# legit doubles (« chwaya chwaya » = slowly): reported as info, not as a stutter
ALLOWED_DOUBLE = {"chwaya", "chwiya", "chouia", "شويه", "شوي", "très", "very", "step", "pas", "kif", "كيف"}


def find_repeats(tokens: list[str], max_n=6, restart_window=10):
    """Repeats in a token list, longest first, no overlapping duplicates:
    - 'repeat'  : a 1..max_n-gram immediately said again (« so don't so don't », « learn learn »,
                  « ça reflète ce que tu fais ça reflète ce que tu fais », « ou la cap ou la capacité »)
    - 'restart' : a >=3-gram said again after up to restart_window other words (a sentence restarted).
    Returns [(kind, n, i, j, phrase)] with i/j the token indices of the first and second take."""
    hits, used = [], set()
    L = len(tokens)
    for n in range(min(max_n, L // 2), 0, -1):
        for i in range(0, L - 2 * n + 1):
            A, B = tokens[i:i + n], tokens[i + n:i + 2 * n]
            if seq_eq(A, B) and not (set(range(i, i + 2 * n)) & used):
                if n == 1 and (len(A[0]) < 2 or A[0] in ALLOWED_DOUBLE):
                    continue
                hits.append(("repeat", n, i, i + n, " ".join(A)))
                used |= set(range(i, i + 2 * n))
    for n in range(min(max_n, 6), 2, -1):
        for i in range(0, L - n):
            for j in range(i + n + 1, min(L - n + 1, i + n + 1 + restart_window)):
                if seq_eq(tokens[i:i + n], tokens[j:j + n]) and not ((set(range(i, i + n)) | set(range(j, j + n))) & used):
                    hits.append(("restart", n, i, j, " ".join(tokens[i:i + n])))
                    used |= set(range(i, i + n)) | set(range(j, j + n))
                    break
    return hits


def is_prefix_take(first: list[str], nxt: list[str]) -> bool:
    """first is a false start of nxt: its tokens are (fuzzily) the opening of nxt, the last one may be
    cut short. « ou la cap » vs « ou la capacité de juger » -> True."""
    if not first or not nxt or len(first) > len(nxt):
        return False
    return all(tok_eq(a, b) for a, b in zip(first, nxt[: len(first)]))


def similar(a: list[str], b: list[str]) -> float:
    if not a or not b:
        return 0.0
    return SequenceMatcher(None, a, b).ratio()


def fmt_t(t: float) -> str:
    return f"{t:7.2f}"


# ----------------------------------------------------------------------------- fillers / tics
# How each tic tends to come back in the three passes (normalised tokens). references/derja-fillers.md has the
# full list with meanings and when a word is NOT a filler. Matches are leads: decide from the meaning.
OPENER_FILLERS = [
    # Derja / arabizi + what fr/en/ar passes write for it
    ["ena", "personnellement"], ["ana", "personnellement"], ["anna", "personally"], ["ena", "personally"],
    ["انا", "شخصيا"], ["انا", "بشخصي"], ["donc", "ena"], ["so", "anna"],
    ["donc"], ["bon"], ["ok"], ["okay"], ["alors"], ["voila"], ["en", "fait"], ["so"], ["well"], ["euh"], ["uh"], ["um"],
    ["ya3ni"], ["yani"], ["يعني"], ["mela"], ["ملا"], ["ehh"], ["ama"], ["w", "ena"],
]
ANY_FILLERS = {
    "euh", "heu", "uh", "um", "hmm", "mmm", "ehh", "eh", "dakord", "daccord", "fhemt", "فهمت", "ya3ni", "يعني",
    "voila", "okay", "ok", "genre", "quoi", "bref", "hakka", "هكا", "behi", "باهي", "ya", "jme3a", "kel3ada",
    "cetera", "etcetera", "w", "kol", "basically", "like",
}
TRAILING_FILLERS = [["wala"], ["walla"], ["ولا"], ["والا"], ["or"], ["ou"], ["et", "cetera"], ["w", "kol"],
                    ["etc"], ["and", "so", "on"], ["quoi"], ["ya3ni"], ["يعني"]]


def filler_hits(tokens: list[str]) -> list[str]:
    out = []
    for f in OPENER_FILLERS:
        if tokens[: len(f)] == f:
            out.append("OPENER « " + " ".join(f) + " »")
            break
    for f in TRAILING_FILLERS:
        if len(tokens) > len(f) and tokens[-len(f):] == f:
            out.append("TRAILING « " + " ".join(f) + " »")
            break
    mid = [w for w in tokens[1:-1] if w in ANY_FILLERS and w not in ("w", "kol", "like", "ya")]
    if mid:
        out.append("FILLER " + ", ".join(sorted(set(mid))))
    return out


STOP = {"the", "a", "an", "to", "of", "and", "or", "in", "on", "it", "is", "i", "you", "s", "t", "re", "de", "la", "le",
        "les", "l", "d", "et", "ou", "un", "une", "des", "du", "en", "que", "qu", "ce", "c", "w", "el", "fi", "bel", "fel",
        "lel", "و", "في", "من", "على", "ان", "ما", "لا"}


def whisper_loop(tokens: list[str]) -> bool:
    """« انا، انا، انا … » x80: Whisper stuck in a loop. That pass says nothing about the speech."""
    return len(tokens) >= 12 and len(set(tokens)) / len(tokens) < 0.3


def reopen_hits(tokens: list[str]) -> list[str]:
    """The opening of a line said twice with something in between: « ena personnellement donc ena ki nchouf »."""
    for i in range(min(3, len(tokens))):
        w = tokens[i]
        if len(w) < 2 or w in ALLOWED_DOUBLE or w in STOP:
            continue
        for j in range(i + 2, min(len(tokens), i + 5)):
            if tok_eq(w, tokens[j]) and len(w) >= 2:
                return [f"REOPEN « {' '.join(tokens[i:j + 1])} » (opening restarted: keep from the 2nd « {tokens[j]} » or later)"]
    return []
