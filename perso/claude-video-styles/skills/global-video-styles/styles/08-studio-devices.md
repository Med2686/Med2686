# 8 · 3D Studio Devices

Preview: `previews/08-studio-devices.jpg`. Reference reels: DfSobPJtg_S ("This took Claude ONE BRIEF" — monitor + phone + blue orb),
DfSlxBBt1ye ("Claude edits WHILE I SLEEP" — laptop), DfSwlcKNm9r ("Editors now take 30 MIN instead of 3–4 hours"), DfSxBKIto7B (phone with orbit ring).

## Look
A dark **ribbed-curtain studio** (shared-kit §8, deeper: `#0e1012 → #3c4043`, top-down soft light, reflective floor) with **photoreal 3D devices**:
a monitor or laptop showing Claude Code + Premiere side by side, a phone propped beside it playing the edited reel, a **glossy blue glass orb**
(`#4a6cff → #9fb4ff`, emissive, light pool `#3b5bff` on the floor). Chrome headline + serif italic on top. Slow, expensive, product-film.

## Elements
- **Headline**: serif italic line ("*This took Claude*", "*Claude edits*", "*Editors now take*") Instrument Serif 64 px + chrome League Gothic 170 px ("ONE BRIEF", "WHILE I SLEEP", "30 MIN") + small serif under ("*instead of 3–4 hours*").
- **Screen content** (real UI recording or rebuilt): left = Claude Code terminal (prompt text + green ✓ list: "words found in the clip", "pauses and um cut", "person cut out", "stills ready", "every frame checked: no overlaps", "rendered sales_edit.mp4");
  right = Premiere timeline with teal clips and the vertical preview. For "WHILE I SLEEP": "Rendering 6 reels… ✓ reel 1 · checked · 177 s" list.
- **Phone**: tilted 12°, playing the reel. **Orb**: slow bob ±10 px, specular highlight moving.
- **Orbit ring** variant (DfSxBKIto7B): a floating phone with an elliptical thin white ring around it and 2 glowing dots orbiting; BEFORE → AFTER swap inside the phone with a flip.

## Build
Three.js via `@remotion/three` (60 fps): GLB laptop/monitor/phone (free models, Sketchfab CC0 / poly.pizza), screen = `VideoTexture` of a pre-rendered UI clip,
`MeshPhysicalMaterial` for the orb (transmission .9, ior 1.4, emissive blue), ribbed wall as a normal-mapped plane, `ContactShadows`, soft key light from top-left.
Camera: slow dolly-in 8 % over the clip + 3° orbit. Or fake it in 2.5D with a device PNG frame and CSS perspective if time is short.

## Sound
Low ambient pad, soft keyboard, a gentle "ding" when renders finish, whoosh on the headline. Music at −14 dB under the voice of the clip playing on the screens.

## Voice & music (measured on the references)
The edited clip's voice plays from the screens (the speaker), no narrator; music under it; ≈1.2 hits/s, all soft whooshes.

## Orbit-ring wrapper — measured on DfSxBKIto7B (26 s), the user's favourite (2026-11-14: « I want it really really like that »)
Study: `eightsenses-study/deep/W-orbit-DfSxBKIto7B/` (4 fps sheets `sheet0-6.jpg`, Demucs stems + `audio/spec.png`).
Reference build: the author's Outlook reel (composition OutlookOrbit, not included here).

**Layout (1080×1920)** — background = the ribbed dark studio (`assets/ribbed-glass.png` at brightness .62, diagonal light band from
top-right, faint violet bounce bottom-right `rgba(140,70,210,.16)`, strong vignette). Top: chrome League Gothic headline ≈150 px centred
at y≈280 (« CLAUDE EDITED THIS » / FR « CLAUDE A MONTÉ ÇA »), serif italic 54 px at y≈396 (« Before and after. »), a small dark pill at
y≈504 (« BEFORE » grey text, or « • AFTER » with a red #ff4d3d dot). Phone 560×1008 centred, top 560, radius 46, thin grey bevel + side
buttons, the 1080×1920 clip scaled ×0.507 inside. AFTER screen has a small dark badge with the Claude spark top-right. Orbit ring:
ellipse centre (540,1062) rx 466 ry 88, 2 px white .42 with glow; back half drawn behind the phone, front half over it; 3 glowing white
dots, one orbit per ≈7 s. White CTA pill 58 px high at y≈1660 (« Get the skills for only $20 » → your own CTA, e.g. « Follow @yourhandle for more »).

**Timeline** — 0.00: phone already there, ×0.82 and lower, no text. 0.17–0.5: phone grows to ×1, headline mask-rises.
0.6–0.9: serif line fades in. ≈1.0: pill + ring (ring widens from ×0.82). 1.2–1.5: CTA fades in (grey → white).
1.85: first FLIP to AFTER. Rhythm: AFTER 3.7–5.2 s, BEFORE ≈1.25–1.4 s, repeat. **Flip** = rotateY 0→−88° in 7 f (ease-in), swap
content, 88→0° in 8 f (ease-out), glass reflection sweeps; during the flip a huge faint outlined word (« BEFORE »/« AFTER », League Gothic
≈300 px, white .09 fill + .2 stroke) shows behind the phone for ≈0.7 s. BEFORE = the raw clip, AFTER = the edit, SAME timeline (voice
never stops). Phone floats ±5 px between flips. End: a grid fly-through of the edit's scenes inside the phone (24–25 s) then the speaker.

**Sound (Demucs)** — voice ≈ −22 dB RMS continuous; music = sustained, pulsing synth-BASS line (8ths, ≈140 bpm, key ≈E, energy almost
all < 150 Hz) at ≈ −16 dB RMS, i.e. LOUDER than the voice (sub-bass does not mask speech). One full drop-out of the bass (22.7–23.4 s)
right before a key moment, then it slams back. SFX: airy broadband swoosh (centroid 5.5→2.6 kHz, 0.4–0.6 s) on flips and inner scene
changes, with a low thump (60–120 Hz) on the biggest ones. Free matches: Mixkit #1484 « Speeding swoosh » (best on all 3 flips), #1481
« Cinematic swoosh »; thump = `sfx_synth.py thump`. Closest free bed: Mixkit music #134 (sustained pulsing bass, low-energy 0.90,
mids 0.04 vs theirs 0.96/0.02). Kick-driven tracks (#132, #162, #371) are the wrong character.

## Opening (measured at 10 fps on 5 wrappers: W06, W10, C09, D08, L06)
**There is no intro build.** Frame 0 already shows the full layout: comment bubble, tag, chrome headline + subline, both phones, prompt
bar. The first frame IS the cover (feed thumbnail) — it must read instantly. Only these move: the AFTER clip plays from its first beat
(already mid-sentence), the BEFORE clip plays raw, the CTA pill fades in at 0.4–0.7 s, a carousel keeps turning. Ignore my older
"0–1 s build-up" timings in this file: build-ups lose the scroll.
