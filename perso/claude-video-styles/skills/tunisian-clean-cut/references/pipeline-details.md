# Pipeline details: config, files, sync, video, Remotion

## project.json (in the project folder)

```json
{
  "camera": "~/Downloads/IMG_2874.MOV",
  "mic": "~/Documents/Sound Recordings/Recording (52).m4a",
  "offset": 20.666, "rate": 1.0, "drift_ms": 6,
  "fps": 30, "work": "work", "remotion": "remotion-video",
  "screen_side": "left", "gaze_seed": 0.4, "gaze_min_frames": 10
}
```
`camera_t = mic_t * rate + offset`. Single source (no separate mic): `"mic": null, "offset": 0`.
All scripts take `-p <project folder>` (default: the current folder). Nothing is hard-coded to a reel.

## Files in work/

| File | Made by | What |
|---|---|---|
| mic16k.wav, cam16k.wav | prep.py | 16 kHz mono copies for analysis |
| proxy540.mp4 | prep.py --proxy | 540p SDR, fps grid, for gaze |
| regions.json | regions.py | [[a,b],…] speech regions (mic s) |
| tx-regions.json/.txt | transcribe.py --regions | each region alone, ar/fr/en |
| tx-mic-ar/fr.json/.txt | transcribe.py --full | whole-file passes, for the topic |
| bursts-regions/keep.json/.txt | bursts.py | boundary evidence, flagged false starts |
| gaze-raw.json | gaze_cover.py --run-gaze (reel-pro-edit gaze.py) | blendshapes per camera frame |
| reading-pack.md | reading_pack.py | per region: passes, strip, leads, your meant/decision |
| keep.json | **you** | the editorial decisions |
| scan.txt/json | scan.py | repeats/fillers per kept line |
| proof.txt | proof.py | start/end/bound proofs |
| clean.json, voice-clean.wav | build_clean.py | the output contract |
| cover.json, gaze-check.jpg | gaze_cover.py | look-aways inside kept speech |
| qa.txt | qa_clean.py | clean voice re-heard, repeats, longest pauses |

## Output contract (what Remotion and later skills read)

`work/clean.json`:
```json
{"offset": 20.666, "rate": 1.0, "fps": 30,
 "pieces": [{"a": 238.6, "b": 240.833, "t0": 0, "n": 67, "camF": 7778, "text": "ou la capacité…", "line": 34, "lineA": 237.9}],
 "total": 15.83, "totalF": 475,
 "lines": [{"line": 34, "a": 237.9, "b": 240.95, "text": "…", "t0": 0, "n": 67, "pieces": 1}],
 "thresholds": {"ref": -23.8, "hi": -36.8, "lo": -46.8}}
```
`a/b` = mic seconds on the 30 fps grid, `t0/n` = frames in the clean timeline, `camF` = frame of the camera
on the fps=30 grid. `voice-clean.wav` = 48 kHz mono, the same pieces sample-exact, 6 ms fades, peak -1 dBFS.
`public/footage/talk-clean-vN.mp4` = the camera on exactly those frames (`n` frames total = totalF).

## Sync (sync.py)

Envelope cross-correlation at 100 Hz (coarse, 10 ms), then raw-waveform cross-correlation in 3 loud 4 s
windows within ±60 ms (sample-level, parabolic peak), then drift = late − early. Under 20 ms: rate 1.
Verified on 20 s slices of the ref-edit reel: 20.663 s early, 20.669 s late (the full-file value was 20.666,
drift 6 ms). If the 3 local offsets disagree by more than a few ms, a window fell on noise: pass --windows.

## Camera (make_face.py)

- iPhone 4K HLG + Dolby Vision, rotated (side data -90): ffmpeg applies the rotation itself → 2160x3840.
- 29.997 fps: `fps=30` FIRST, so the frame index n is the 30 fps grid that camF uses.
- `select` with a balanced-tree sum of `between(n,a,b)`: a flat chain of 113 terms crashes the parser.
- HLG → SDR: `zscale=tin=arib-std-b67:…:t=linear:npl=203, format=gbrpf32le, zscale=p=bt709,
  tonemap=mobius:param=0.3:desat=0, zscale=t=bt709:m=bt709:r=tv` (checked on stills against hable).
  PQ sources use tin=smpte2084. SDR sources skip it.
- ffmpeg 9 (winget Gyan.FFmpeg): `-/filter_complex file.txt` (not -filter_complex_script); no fontconfig,
  so drawtext needs `fontfile='C\:/Windows/Fonts/arial.ttf'`.
- `-t` on the input stops decoding 1 s after the last kept frame (without it, the whole 4K file is decoded:
  4 min for a 4 s test vs 32 s with it).
- Full 4K x264 CRF 14 by default ("keep same quality"); `--small` = 1080x1920 CRF 18 preview, much faster.
  Build the small one first for the Studio check, the 4K one in the background.

## Remotion (publish.py)

- `--scaffold` creates `<project>/remotion-video` from `assets/remotion` (Remotion 4.0.535, React 19) with
  node_modules as a junction to `Desktop/videos/remotion-video/node_modules`, and adds a launch entry
  `<project>-studio` to `Desktop/videos/.claude/launch.json`. Pick a free port (ref-edit is 3210).
- The node_modules junction points at the SHARED folder: never `rm -rf` a project folder that holds it
  (it can follow the link). Remove the link alone first: PowerShell `[System.IO.Directory]::Delete(<link>)`.
- Each version: new file names (`talk-clean-vN.mp4`, `voice-clean-vN.wav`): Studio locks open files.
- Composition `CleanCut`: the face, the clean voice, a clock, and per line a label « #n · mic t s » + text.
- Show it in Studio, send him the link, wait for his OK. Never render unless he says so.

## Gaze (gaze_cover.py)

Uses `~/.claude/skills/reel-pro-edit/scripts/gaze.py` with the system Python 3.12 (mediapipe) and
`%LOCALAPPDATA%\reel-pro-edit\models\face_landmarker.task`. Side score = (eyeLookOutRight + eyeLookInLeft)/2
for a screen on the image-left. Look-away = score > 0.4 for ≥ 10 frames inside kept speech → COVER entry.
Verified: on the ref-edit gaze data it returns exactly mic 187.37-188.27 (peak 0.65), the known reading glance.
