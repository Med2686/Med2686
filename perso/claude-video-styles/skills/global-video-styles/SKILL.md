---
name: global-video-styles
description: GLOBAL video skill — a library of 15 complete, detailed video styles (studied frame by frame from every reel of @eightsenses.media, 2026-11-12) with a preview picture of each, a numbered gallery, and an intake that asks him which style, which colours and the other choices before building. Talking-head edits (Dark Teal Chrome, Neon Mono, Violet Glass, Silver Infographic), promo/showcase formats (Before/After Ad, Light Paper, App Demo with the Claude UI, 3D Studio Devices, Speaker Carousel, Chrome Trailer, Screen Tutorial) and studio looks (Luxury Property Tour, Pastel SaaS Motion, Teal Ocean Funnel, Clean White Before/After). Each style file gives the exact palette (hex), fonts, layout in 1080×1920, every graphic element, motion timings, captions, transitions, SFX map, music, voice and a Remotion build recipe. Use this skill WHENEVER the user says "global skill", "global style", "create me a video with the global skill", "use the global", "eightsenses style", "the styles gallery", names one of the 15 styles (dark teal, violet glass, ribbon, chrome, neon mono, light paper, carousel, chrome trailer, luxury property, pastel saas, teal ocean…) or asks to pick a style for a new video — even if he doesn't name the skill.
---

# Global video styles

15 styles in one skill. The job: **show the gallery → he picks → ask the questions → build that style exactly → he checks in Remotion Studio → render only on his OK.**

Files (v2, 2026-11-12 — rebuilt after the user rejected the first test for picture quality and sound):
- `previews/gallery.jpg` — numbered gallery of all 15 (always show this first). `previews/NN-<id>.jpg` — one per style.
- `styles/NN-<id>.md` — the full spec of each style (measured timelines, beat grammar, layout, palette, sound). Read the chosen one completely.
- `references/element-catalog.md` — **every graphic seen in the 13 studied edits** (A text, B glass UI, C behind-the-speaker, D scenes,
  E transitions, F pacing) with size, position, entrance/exit in frames and real sound. The style files reference it by code (A1, B5, E1…).
- `references/sound-design.md` — **measured** loudness and balance per family (Demucs stems), event → sound map, levels. Voice-first.
- `references/quality.md` — **picture & render rules** (4K original, HLG tone-map, never shrink the speaker, local fonts, PNG frames,
  CRF 14, 1080p phone copy, final checks). Read before building AND before rendering.
- `references/shared-kit.md` — building blocks (chrome text, glass tags, captions, comment bubble, prompt bar, phones, brand mapping).
- `references/source-study.md` — reel ids per style; the frame-by-frame study notes are not included in this repo.
- `assets/ribbed-glass.png` (+ `-red`) — 2160×3840 fluted dark-glass background matched to theirs (`scripts/make_ribbed.py` to re-render).
- **SFX toolkit** (run with `%USERPROFILE%\.venvs\claude-video\Scripts\python.exe`, Demucs + librosa + CUDA torch):
  - `sfx/bank/bank.json` + `sfx/bank/*.wav` — the curated sound per role (scene_in_riser, violet_whoomp, card_ping…). Use these first.
  - `sfx/library/` — QC'd one-shots ≤ 12 s, normalised (the whole Mixkit catalogue that passes QC, Freesound CC0 top sounds for ~125 editing queries, uisfx CC0) with `index.json` features; `sfx/refs/` their SFX cuts (A/B only, never in a video).
  - `sfx/packs/` — big free packs as original files: Sonniss #GameAudioGDC 2026 + 2024 (pro libraries), Kenney audio (CC0), OpenGameArt CC0 packs, Mixkit long/ambient originals. `packs/README.md` = contents, `packs/manifest.json` = every file (long ones too), `packs/index.json` = features of the ≤ 12 s ones. Licences: `sfx/LICENSES.md`.
  - `scripts/sfx_fetch.py` — search & download more (`mixkit <categories>`, `mixkit-all`, `freesound "<query>"`, `freesound-file sfx/freesound_queries.txt`, `uisfx`), QC + normalise + index.
  - `scripts/sfx_packs.py` — packs: `kenney`, `oga`, `shorten`, `scan`, `index` (2 workers, low priority), `report`, `find "rain,crowd" --min 10` (text search incl. long files). Sonniss: `scripts/packs_tools/fetch_sonniss.sh 2026 2024`.
  - `scripts/sfx_match.py <ref.wav> --kw "whoosh,air" [--scope library|packs|all]` — closest sounds to any reference across library + packs (+ spectrogram montage); prints the full path to copy.
  - `scripts/sfx_synth.py <kind> out.wav` — procedural fallback (whoosh, prelap, whoomp, riser, boom, pop, ping, tick, sparkle, smear, roll, typing, stamp, glitch…).
  - Never ElevenLabs for SFX; never anything "glass" ("glass" sound the user hates): such files are flagged `excluded` in both indexes and sfx_match skips them.
  - Sonniss sounds: use in videos only — never redistribute the raw files, never feed them to an AI model (licence).

## Step 0 — First run on a new PC

If `sfx/library/index.json` does not exist yet, the sound library is not downloaded (the repo ships no third-party sound files).
Follow the « Install » section of the repo README: venv, models, then the SFX downloads and `scripts/build_bank.py restore`.
Until then, `sfx/synth/` (procedural sounds) and `sfx/bank/` (two procedural roles) still work.

## Step 1 — Show the gallery (never skip)

1. `SendUserFile` → `previews/gallery.jpg`, `display: "render"`, caption "Pick a style by number or name".
2. Under it, one line per style (number, name, what it is for):

| # | Style | Best for |
|---|-------|----------|
| 1 | Dark Teal Chrome | talking head: giant chrome word behind the head, glass tags on the spoken words, serif-italic captions, photo plates, ribbed-glass schema scenes |
| 2 | Neon Mono | talking head in a dark room: black & white, teal glowing wave, app-icon checklists, arc gauge |
| 3 | Violet Glass | talking head: violet room grade, 3D glass ribbon, purple spheres, white glass cards, abstract violet scenes, button click, shakes |
| 4 | Silver Infographic | talking head with data: dot-matrix calendar, stamp badge, charts, landing-page fly-over, thumbnail wall |
| 5 | Before / After Ad | selling an edit / a service: comment bubble hook, chrome headline, tilted BEFORE + AFTER phones, prompt bar, CTA |
| 6 | Light Paper | same as 5 but bright: white paper, mint particles, polaroids, receipt, timeline card, neon stamp |
| 7 | App Demo (Claude UI) | showing an AI/app doing the work: chat window, Claude Code terminal, checklist ticking, result video |
| 8 | 3D Studio Devices | laptop / monitor / phone in a dark ribbed studio with a glowing orb, the work playing on the screens |
| 9 | Speaker Carousel | many results at once: 3D fan / orbit / grid of phone cards |
| 10 | Chrome Trailer | kinetic promo / launch: huge chrome words + teal sticker tags, app UI, cut-out steps, timeline, logo end |
| 11 | Screen Tutorial | teaching software step by step: screen recording in a floating window, chrome chapter titles |
| 12 | Luxury Property Tour | real estate / architecture: bright renders, blueprint line-art drawing itself, airy kinetic type |
| 13 | Pastel SaaS Motion | product ad: pink-violet gradient, floating notification cards, condensed gradient type, typing cursor |
| 14 | Teal Ocean Funnel | carousel-like explainer slides: aerial ocean, deep teal, glowing cyan words, white/glass message cards |
| 15 | Clean White Before/After | portfolio showcase: white gradient, rounded before/after cards, "Viral Video Editing" title |

Then ask: **"Which one? (number or name — you can mix two, e.g. 1 with the captions of 3)"**. Wait for the answer. When he picks, send `previews/NN-<id>.jpg` as confirmation.

## Step 2 — Ask the questions (AskUserQuestion, max 4 per call, two calls)

Call 1:
1. **Colours** — `Original palette (as in the preview)` (recommended) · `My brand: black + red #E30A17` · `Custom (tell me)`. Brand mapping rules are in `references/shared-kit.md` § Brand mapping (no script fonts, no borders, real footage untouched…).
2. **Input** — `Raw clip of me talking` · `Script / brief only (faceless)` · `Footage + script`. Ask for the path(s).
3. **Language of captions** — `As spoken (Derja in Arabic letters + Latin tech words)` · `French` · `English`.
4. **Length** — `≈30 s` · `≈45–60 s` · `As long as the clip`.

Call 2:
1. **Music** — `I give you the track` · `You pick a free one (Mixkit/Pixabay)` · `No music`.
2. **Text behind the head** — `Yes, on key words` (recommended for 1–4) · `No`.
3. **Hook / end card** — `Comment bubble hook + CTA` · `No hook, straight in` · `Custom text`.
4. **Density** — `Animated element on every phrase` (his default) · `One graphic every 3–4 s` · `Minimal`.

Skip a question the chosen style makes pointless (e.g. text-behind-head for 13). Record all answers in `<project>/BRIEF.md`.

## Step 3 — Build

1. Read `styles/NN-<id>.md`, `references/element-catalog.md`, `references/sound-design.md`, `references/quality.md`, `references/shared-kit.md`.
   Every hex, font, timing and level there is the target. When a motion is unclear, open the reference reel at that time (source-study.md).
2. **Check the footage against the style before anything else** (quality.md): camera original (4K HLG) available? Framing medium-close
   with headroom (styles 1–4 need the head in the middle third and room above it)? If the shot is a tight selfie, tell the user and propose
   the best-fitting style or a re-shoot — never shrink him into a box.
3. **Raw footage** → cut with the `tunisian-clean-cut` skill on the ORIGINAL file (frame-exact), show the clean cut in Studio, wait for his OK
   while preparing graphics. Tone-map HLG→SDR once (quality.md command), keep 4K until the final render.
4. **Matte** for text behind the head: `scripts/matte.py` on the 4K-derived plate (hair, glasses, mic kept).
   Word timings: `scripts/transcribe.py` (faster-whisper large-v3, CUDA venv `%USERPROFILE%\.venvs\claude-video`).
5. Project `Desktop\videos\<slug>\` — Remotion 1080×1920 (or 2160×3840), 30 fps (60 for 8 and 10). **Fonts bundled locally**
   (`public/fonts`, `@remotion/fonts`). Fluted scenes use `assets/ribbed-glass.png`. Write `EDIT-PLAN.md`: every graphic, on which word, why.
6. Map the transcript to beats with the style's **beat grammar** and the catalog's pacing (F): event every 0.4–0.8 s, one chrome word per idea.
7. **Sound**: follow `sound-design.md` (voice-first, bed level per family, event → bank role). Take sounds from `sfx/bank/`; if a role is
   missing or wrong for this video, `sfx_match.py` against the library or `sfx_fetch.py` new ones, else `sfx_synth.py`. Voice gaps ≤ 0.15 s.
   Master −14 LUFS / −1 dBTP.
8. Studio (`.claude/launch.json` entry, new port), send him stills + link, list decisions. **No render until he says render.**
   Render per quality.md (PNG frames, CRF 14, yuv420p bt709, 300-frame chunks with retry), then the automatic final checks; phone copy 1080p.

## Standing rules (from the user)

- Windows only, never WSL. One video at a time; few subagents (each costs 170–450 k tokens).
- No render without his OK. Never idle: answer him and keep the job moving.
- Free SFX only; no glass SFX; no ElevenLabs for SFX. French AI voice = ElevenLabs Kev only if he wants a voiceover.
- No pause between voice lines over 0.15 s; never a silent insert.
- His own footage keeps its natural colours unless the style grade is explicitly chosen (Violet Glass grades the room; ask if it's his face).
- Restraint over silly effects: every element must explain the word it sits on.
