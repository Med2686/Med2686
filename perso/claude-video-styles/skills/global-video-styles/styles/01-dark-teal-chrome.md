# 1 · Dark Teal Chrome  (their "Style 1 · Dark Teal") — v2, rebuilt from frame-by-frame analysis

Preview: `previews/01-dark-teal-chrome.jpg`. Studied on 11 edits / 7 speakers (sales guy green room · Cluely guy violet room ·
curly guy warm room · realtor outdoor/kitchen · podcaster warm set ×4 · AI-websites guy white room). Frame notes:
`eightsenses-study/deep/E01 E03 E04 E07 E08 E09 E10 E11 E12 E13`. Element numbers (A1, B2, C4, D5, E1…) refer to
`references/element-catalog.md` — read it. Sound: `references/sound-design.md`. Quality: `references/quality.md`.

## The look in one breath
The speaker stays **full frame in his real room** (no letterbox, no regrade beyond a clean tone-map). On every idea a **giant chrome
word rises behind his head**, captions type word by word on his chest with a serif-italic key phrase under them, dark glass tags and
chips land on the spoken nouns, light graphics live **behind** him (rays, waves, bars, gauges), and every 4–8 s the film dissolves —
through a glowing cyan "bridge" dot — into a **fluted dark-glass scene** where a cyan comet draws the idea as a path. Voice-first,
almost no music. Premium, calm, very fast in information.

## Palette (measured)
| Token | Value | Use |
|---|---|---|
| Room | untouched (green `#0e3224`, warm `#44342a`, violet room, white walls all work) | the speaker plate |
| Chrome | `#fcfdfe → #e3e7ea → #c9ced3 → #8b9096 → #6f747a (band) → #f2f4f6 (line) → #d6dade → #a9aeb4 → #ffffff` | A1, A5 |
| Cyan accent | core `#5ad4f0`, glow `rgba(90,212,240,.55)`, sheen `#bff4ff`, scan `#7fe9ff` | dots, comet, nodes, badges, sheen |
| Teal UI | `#2fd2c0` / `#2bb3a3`, app chips `#3be8d0→#12a596` | pills, chips, charts |
| Glass | `rgba(28,30,33,.78)` + blur 14 + top highlight `rgba(255,255,255,.28)` | B1–B14 |
| Fluted glass scene | flutes `#16191c #232729 #2e3234 #383c3f #424649`, light half `#6f7b7e–#999999` | D1 |
| Text | `#ffffff`, secondary `#c4d1d4` | captions |
| Icon circles (chips) | red `#e5484d`, green `#30a46c`, blue `#3b82f6`, gold `#f5b942` | B2 |

## Typography
Chrome headline: Dharma Gothic E Heavy if installed, else **League Gothic** (local file). Captions: **Inter 600** caps. Accent:
**Instrument Serif Italic**. Tags/chips: Inter 500/700. Arabic (the user): Cairo 800 for line 1; keep line 2 in Instrument Serif
(French/English key phrase) or Cairo 900 if Arabic. All fonts bundled locally.

## Layout (1080×1920; fractions in the catalog)
- Chrome word A1: cap height ≈270 px, y 350–700, 85–98 % width. Must be readable: at least 60 % of the letters visible around the head.
- Tags B1: shoulders y≈960–1020. Caption A6 y≈1110–1190, A7 just under (y≈1190–1270).
- Lower-third cards (B5–B14): y 1300–1650, x 100–990. **Never over the face, never over a hand** (their bug list).
- Safe: nothing below y 1700 (IG UI), nothing above y 120.

## Beat grammar (what happens on each phrase)
1. **Key noun/verb** → A1 chrome word (+ A2 streak; + A3 cyan sheen on the 1–2 strongest words of the video).
2. **Two related things** → a pair of B1 tags (each on its own spoken word).
3. **A concrete thing** (place, product, photo-able) → B5 photo plate (AI still or stock) with ★ label + chips.
4. **A number / money** → A5 counter (behind the head or on D1), or B7 money card with chart; always land on the exact spoken value.
5. **A trend / growth / decline** → B6 mini chart (hockey stick for growth, falling line for "waffling").
6. **A time unit / routine** → B9 dot-matrix calendar (dots → bars morph), B10 stamp on the conclusion.
7. **A process / list / steps** → **cut to D1** (bridge-dot dissolve E1) with D2 comet path or D3 numbered rows.
8. **"Many people / audience / market"** → D1 + D4 person constellation (one turns cyan).
9. **Emotion / rhythm** → C1 rays or C2 wave behind the head; **measure / decision** → C6 gauge; **growth** → C4 bars behind.
10. **Story / who they are** → once per video, right after the hook: **D5 landing-page fly-over** built from the speaker's words, diving back into the live shot.
11. **Showable thing he mentions** → D7 B-roll (stock or AI still, slow push) with A1 behind the B-roll subject, captions continue.
12. **Ending** → C11 kinetic text wall or a last chrome word + serif line; optional CTA.

Density: a new event every 0.4–0.8 s; chrome word every 1.2–3 s; D1 scene every 4–8 s (1.5–4 s long); landing page ×1; B-roll ×1–2 per 30 s.

## Recipe (30 s template)
| t | Beat |
|---|---|
| 0.0–0.3 | open on the speaker mid-sentence (never on black), caption typing |
| 0.3–2.0 | hook word A1 + C1 rays behind |
| 2.0–6.0 | D5 landing page (his name, his headline, slider of his story, stat, "Watch his take" → dive back) |
| 6–12 | 3 speaker beats (tags, chips, money/chart card) |
| 12–15 | D1 scene (comet path or rows) |
| 15–20 | speaker beats + C4/C6 behind-graphic, D7 B-roll |
| 20–23 | D1 scene (counter or constellation) |
| 23–30 | final beats, A11 wall or final chrome word, CTA |

## Motion constants
Entrances 2–4 frames (fast, ease-out). Exits: dim 4 f + fade 6 f, everything of the beat together. Idle float ±4–6 px.
Camera on the speaker: none or a very slow push (≤3 % over a beat); **no punch-ins, no shakes** in this style.
Transitions: E1 bridge-dot dissolve (default), E5 hard cut on his own camera changes, E7 dive (landing page), E3/E4 blinds/push max once.

## Sound
Voice-first. Bed −36 … −42 dB (or no music). `scene_in_riser` into each D1, `scene_out_whoosh` back, `card_ping` on cards, optional
`word_prelap` on ≤1 in 3 chrome words, `counter_roll` under rolling numbers. Everything else silent. Master −14 LUFS / −1 dBTP.

## the user's brand variant
Cyan/teal → red `#E30A17` (sheen `#FF3B47`), chrome → his grey→black metal, glass without borders, no serif/script (→ Inter 900 Italic),
captions Cairo 900 for Derja. Keep the room natural.

## Build (Remotion)
Components: `ChromeWord` (mask-rise + streak + sheen), `CaptionTyper` (word timestamps), `SerifLine`, `GlassTag`, `Chip2`,
`AppChip`, `PhotoPlate`, `MiniChart`, `MoneyCard`, `DotCalendar`, `Stamp`, `FlowCard3`, `Rays`, `Wave`, `BarsBehind`, `Gauge`,
`FlutedScene` (PNG texture) + `Comet`, `NumberedRows`, `Constellation`, `Counter` (slot roll), `LandingPage3D`, `BridgeDot`.
Data: `beats.json` from the word timings + the grammar above. Cut-out: RVM matte of the 4K original (hair/glasses/mic kept).
