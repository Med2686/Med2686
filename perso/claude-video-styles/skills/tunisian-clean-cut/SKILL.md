---
name: tunisian-clean-cut
description: Cut and clean the user's raw talking-head recording (iPhone camera + separate mic, Tunisian Derja mixed with French and English) with expert-editor precision, so he never has to correct it. Removes every pause, retake, false start, stutter, repeated word, filler and throat-clearing opener, always keeping the LAST take, judged from the meaning of what he says; covers script-reading glances; syncs the mic; cuts the 4K HLG camera on the same frames; delivers clean.json + voice + face video + a labelled CleanCut composition in Remotion Studio, plus a findings list. Use this skill WHENEVER the user says "cut my video", "clean my video", "clean cut", "use the skill to cut/clean", "remove the pauses / silences / stutters / retakes / repeated words", "nettoie / coupe ma vidéo", "9oss el video", hands a new IMG_xxxx.MOV and a Recording (N).m4a, or asks for the first step of any face-cam reel in Derja/Tunisian — even if he doesn't name the skill. Run it before any effects, captions or music skill (reel-pro-edit, split-reel-face, effects…), which all build on its clean cut. Not for AI voices, faceless videos or music edits.
---

# Tunisian clean cut

the user films himself talking (Tunisian Derja + French + English), reads the next line of his script from a
screen on the image-left during pauses, and records his voice on a separate mic. Your job is the clean
cut: every word he meant, in the order he meant it, with **nothing doubled, no tic, no pause, no clipped
word**. This is his most important editing requirement. Each time he had to point at a stutter himself,
the job had failed: catch it before he does.

You cannot hear. Your ears are: Whisper in three languages on tiny slices, the 10 ms loudness strip, an
acoustic echo score, and your understanding of what he is trying to say. Say so honestly when it matters,
and let his ear be the last word (the findings list and the Studio labels exist for that).

## Non-negotiables

- **Windows only.** Never WSL. Python with Whisper: `%USERPROFILE%\.venvs\claude-video\Scripts\python.exe -I`
  (GPU). Gaze needs the system Python 3.12 (mediapipe); gaze_cover.py calls it itself. ffmpeg 9 is on PATH.
- **Last take wins**, at every scale. A false start glued to the retake is still a false start.
- **Meaning first.** Reconstruct the sentence he meant in Derja before deciding anything. Cut tics and
  duplicates, but never a phrase that adds meaning. Unclear → flag it to him, never cut silently.
- **Findings list to him before the final cut**, with mic times. Labels `#n · mic t s` in Studio.
- **Zero pauses**, no silent gesture inserts. **Never clip a word.**
- **Show the clean cut in Remotion Studio and wait for his OK.** Never render on your own.
- **Don't idle**: while a Whisper pass runs in the background, read, decide, prepare the next step. When
  he asks a question mid-job, answer it and keep the job running.
- Don't touch other projects' files. Each version gets new file names (Studio locks open files).

Scripts are in `scripts/` (run them from anywhere, `-p <project folder>`). Read `references/` when a step
says so: `whisper-on-derja.md` (what Whisper does to Derja, hallucinations, speed), `derja-fillers.md`
(tics in arabizi + Arabic, when a word is NOT a filler), `decision-rules.md` (rules + the worked example +
findings format), `pipeline-details.md` (config, file contract, sync, HDR, Remotion).

```bash
PY="~/.venvs/claude-video/Scripts/python.exe -I"
S="~/.claude/skills/tunisian-clean-cut/scripts"
P="~/Desktop/videos/<reel-name>"
```

## Workflow

### 1. Sources, project, sync (minutes)
```bash
$PY $S/prep.py -p "$P" --camera "~/Downloads/IMG_xxxx.MOV" --mic latest --proxy
$PY $S/sync.py -p "$P" --write
```
`--mic latest` = newest `Documents\Sound Recordings\*.m4a` by date: check the printed dates match the camera
clip. The proxy (540p, SDR, fps grid) is for gaze; it can run in the background. Check sync's three local
offsets agree (ms); drift under 20 ms is ignored.

### 2. Listen to everything (background, ~10-15 min for 5 min of raw)
```bash
$PY $S/regions.py -p "$P"
$PY $S/transcribe.py -p "$P" --regions          # each region alone: ar (Derja prompt), fr, en
$PY $S/transcribe.py -p "$P" --full --langs fr  # optional, whole-file pass for the topic
$PY $S/gaze_cover.py -p "$P" --gaze-only     # MediaPipe gaze on the proxy -> READING? leads in the pack
$PY $S/reading_pack.py -p "$P"
# optional, slow (~6 Whisper calls per boundary): structural leads on the raw regions, merged into the pack
$PY $S/bursts.py -p "$P" --regions [--echo-gate 0.8]  &&  $PY $S/reading_pack.py -p "$P"
```
Remember: the ar pass translates Derja into MSA; en shows repeats best; empty = non-speech. Region
transcripts still TIDY repeats (« so don't, so don't just learn AI » came back as « So don't just learn
AI » from its region alone): a clean region text never proves a clean region. Step 4 exists for that.

### 3. Understand, then decide (your editorial pass; the most important step)
Read `work/reading-pack.md` from top to bottom **before deciding anything**:
1. Write the topic in one line and the outline (hook, points, ending).
2. Per region, write **meant:** the Derja sentence in arabizi (7=ح 3=ع 9=ق 5=خ ch=ش), using all three
   passes and the leads (RETAKE, SIMILAR, REPEAT, REOPEN, OPENER, FILLER, NON-SPEECH, READING).
3. Per region, write **decision:** KEEP / CUT (why) / KEEP FROM t / CUT t1-t2 inside / FLAG.
   Apply `references/decision-rules.md`: last take; correction wins; restarts keep the second; cut tics and
   throat-clearing openers (« ena personnellement, donc ena, ki nchouf » → from « ki nchouf »); cut a
   reformulated duplicate idea but never lose a real moment; unclear → FLAG.
4. Find the exact cut points on the strip, never from Whisper word times:
   `$PY $S/listen.py -p "$P" 237.80-238.70 238.55-241.00 --strip --langs en,fr`
5. Write `work/keep.json`, in reel order:
```json
[
 [11.70, 15.25, "Ken enti mel 3bed elli t3allmou yetmannchou b Claude w mekech 3aref ta3mel kif hedhi"],
 {"a": 237.90, "b": 240.95, "text": "ou la capacité de juger le résultat", "cut": 238.20, 238.59, "why": "false start « ou la cap »"}
]
```
`cut` removes sub-spans inside a line. Line bounds can be generous (the speech mask trims the edges), but
must not include another take.

### 4. Structural pass on the draft: hunt what whole-line transcripts hide (background, the slow one)
```bash
$PY $S/bursts.py -p "$P" --keep      # every gap/notch boundary: chunk before / after / both, echo score
$PY $S/scan.py -p "$P"               # per line: fuzzy n-grams up to 6 words, REOPEN, fillers, SIMILAR-NEXT
```
Whisper on a whole line tidies repeats (« ou la cap… ou la capacité » heard as one clean phrase). bursts.py
splits each line on dips **and on 20-30 ms notches**, transcribes each side alone and together, and scores
PAIR-REPEAT / PREFIX / SOUNDS-LIKE / ECHO / TIDY. In a CLUSTER of flags the retake starts at the LAST one.
**Mandatory: read every flagged line yourself** (score ≥ 2 and every scan flag), confirm with `listen.py`
on tiny slices, and decide from the meaning. A flag is a lead, a clean scan proves nothing on its own.
Update keep.json, then rerun bursts/scan on the changed lines (`scan.py --lines 34,47`).

### 5. Prove every cut, then build
```bash
$PY $S/proof.py -p "$P"              # from each cut point to the line end; line ends +0.45 s; bounds in dips
$PY $S/build_clean.py -p "$P"        # -> work/clean.json + work/voice-clean.wav (prints longest pauses)
$PY $S/gaze_cover.py -p "$P"         # look-aways WHILE talking -> COVER entries; then LOOK at gaze-check.jpg
```
A proof « from t » must contain the whole intended phrase and no stutter; an END flag means move the end
to the next dip. Covers are for full-screen graphics later; the words are not cut. Thinking looks are fine.

### 6. QA the clean voice
```bash
$PY $S/qa_clean.py -p "$P"           # 10 s windows en+fr, repeat scanner on the CLEAN voice, pause audit
```
Every « DOUBLED? » maps to `line #n · mic t`: check it with listen.py on the mic, fix keep.json, rebuild.
Read the windows as a viewer: anything doubled, cut mid-idea, or senseless where a repeat would fit.
Longest quiet run must stay under ~0.1 s.

### 7. Picture + Studio
```bash
$PY $S/make_face.py -p "$P" --version 1 --small        # 1080x1920 preview first (fast)
$PY $S/publish.py   -p "$P" --version 1 --small [--scaffold --port 3211]
$PY $S/make_face.py -p "$P" --version 1                # 4K in the background ("keep same quality")
```
Start Studio with `preview_start` (launch entry `<reel>-studio`), open the `CleanCut` composition and
check a few stills yourself (face matches the voice at a join, labels readable). When the 4K file exists,
`publish.py --version 1` again points CleanCut at it (or bump the version).

### 8. Report to him, then wait for his OK
Send, in his language register (simple English, Derja words as he says them):
- the Studio link + composition name, length before → after, number of lines and pieces;
- the **findings list** (format in `references/decision-rules.md`): every retake / false start / filler
  cut with `#n · mic t`, every COVER, every FLAG as a question;
- what you could not verify by ear-proxy.
He answers with numbers ("restore 3", "#12 still doubled"). Fix in keep.json → steps 5-7 with version N+1.
Only after his OK do effects, captions or music start (another skill).

## Why the order matters

Every downstream file (captions, scene timing, SFX, music hits) is built on clean.json. A stutter found
after the effects are built costs a re-cut of everything. So the clean cut is proved first, by ear-proxy
and by his ear in Studio, and nothing else starts before his OK.
