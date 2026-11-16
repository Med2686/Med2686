# Whisper on Tunisian Derja: what lies, what to trust

Learned on the ref-edit reel (IMG_2874 + Recording (52), 2026-11-11) and the kalfetni / n8n reels.

## 1. The ar pass translates

`language="ar"` on large-v3 returns **Modern Standard Arabic**, not what he said:
- « w ana personnellement ma nchouf ken zouz 7ajet » → « وأنا، بشخصوصي، لا أرى إلا 2 أشياء يفعلون الفرق »
- « el kol ye7taj el créativité » → « كل هذا يطلب التصميم »
The words look clean, so a retake or stutter disappears in the translation. Auto-detect also says "ar".
Use the ar pass for the gist and for the Arabic-script word list only.

## 2. Remedies (all built into the scripts)

| What | Script | Why |
|---|---|---|
| ar (Derja initial_prompt) + fr + en passes | transcribe.py | no single language is right; en shows repeats best, fr the French words |
| each region alone, 0.25 s zero padding, condition_on_previous_text=False | transcribe.py --regions | context of the last line makes Whisper "tidy" the next |
| boundary pairs: chunk before / after / both | bursts.py | a whole line hides a glued false start (« ou la cap… ou la capacité ») |
| tiny slices for every doubt | listen.py | what finally located the stutters |
| fuzzy n-grams up to 6 words across passes | scan.py, qa_clean.py | « ça reflète ce que tu fais, ça reflète ce que tu fais » is a 5-gram |

## 3. Hallucinations = non-speech

Blanked automatically (`tcc_common.HALLU`, `is_hallu`): they mark a breath, room noise or silence.
- « Sous-titrage ST' 501 », « Sous-titrage FR ? », « Sous-titres réalisés par… », « Amara.org »
- « ترجمة نانسي قنقر », « ترجمة نانا عبد الرحمن عبد الرحيم » (any « ترجمة … » credit)
- « Thanks for watching », « Thank you for watching », « We'll be right back », « Enjoy the video »
- « اشتركوا في القناة », « شكرا للمشاهدة », « Merci d'avoir regardé », « Abonnez-vous »
- **The prompt recited back**: on noise, the fr pass returns its own initial_prompt (« l'IA, prompt, créatif,
  intelligent, résultat, concept, barcha, chnowa, ya3ni, tawa »). `prompt_echo` blanks any text that is
  ≥ 60 % prompt words.
- **Loops**: « انا، انا، انا… » ×80. `whisper_loop` ignores a pass whose tokens are < 30 % distinct.

## 4. Prompts that invite repeats ("verbatim")

A disfluent prompt (« So, uh, I I think that, that it's… ») makes Whisper write repeats it would tidy:
« Learn, learn how to be smart around AI » came out only with it on a whole line.
- **Never put the clip's own words in a prompt.** A test prompt containing « ou la, ou la capacité »
  made Whisper "hear" that stutter on 0.35 s of breath. The prompts in `VERBATIM` are neutral on purpose.
- It also invents repeats (« Ça, ça, ça, ça » on a short noisy chunk). A verbatim-only hit is a lead;
  confirm it on the loudness strip (two bursts with a dip) and with a plain pass on a pair chunk.

## 5. Times

- Word times are off by up to 0.2 s, and the first word is pinned to the slice start (with padding, to
  the padded start: a word "at 237.55" in a slice starting at 237.80 means "at the start").
- **Cut points come from the 10 ms loudness strip** (`listen.py --strip`): a dip under T_low, or a notch.
- **Prove a cut** by transcribing from the proposed point to the line end (`proof.py`, `listen.py`): the
  whole intended phrase must be heard, without the stutter.
- **Prove a line end**: [end-1.3, end] vs [end-1.3, end+0.45]. A fuller last word in the longer slice =
  the end clips the word (« tekh » / « tekhdem », the « -sion » nasal).

## 6. Speed on this PC

RTX 1000 Ada 6 GB: model load ~40 s, then **1.5-3 s per Whisper call, whatever the slice length** (the
encoder always sees 30 s). Batching (`BatchedInferencePipeline`, batch 4) gave no gain and batch 8 ran out
of memory. So: count the calls before you run, run the long passes in the background, keep working.
Rough cost: transcribe --regions 3 calls/region; bursts.py ~6 calls/boundary (≈ 3-5 boundaries per
second of speech… it is the slowest pass: run it on the draft keep lines, not on 5 minutes of raw);
scan.py 5 calls/line (measured: bursts.py on 6 lines / 17 s of speech = 2 min 26 s incl. the 40 s model load); proof.py ~2 + 4 calls/line; qa_clean.py 2 calls per 8 s of clean voice.

## 7. Setup gotchas (Windows)

- `%USERPROFILE%\.venvs\claude-video\Scripts\python.exe` has faster-whisper 1.2.1 + CUDA. Before the
  import, register `Lib/site-packages/nvidia/*/bin` with `os.add_dll_directory` and prepend to PATH, else
  `cublas64_12.dll not found` (`tcc_common.cuda_setup`).
- Never pass a file path to `transcribe()`: PyAV in that venv breaks. Decode with ffmpeg to f32le numpy.
- `python -I` ignores PYTHONIOENCODING: `sys.stdout.reconfigure(encoding="utf8")` or Arabic crashes the console.
- `python -I` also drops the script folder from sys.path: every script inserts its own folder.
