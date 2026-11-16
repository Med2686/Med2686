# 9 · Speaker Carousel  ("4 speakers, 4 styles, one skill")

Preview: `previews/09-speaker-carousel.jpg`. Reference reels: DfSI1E8Nac8 (3D fan), DfSyjoxtZk1 + DfSev5vtirg (3D orbit carousel),
DfSHzAHNxRr (3×3 grid), DfhhdADEYs_ ("ALL OF THIS" fan on blue-violet curtain, 777 likes), DfSolwBtZw5 (2×2 grid), DfT_u7Xtm8K ("6 REELS").

## Look
Many finished reels at once, as **phone cards in 3D**: a fan (cards spread in an arc, the centre one forward), an **orbit carousel**
(cards on a ring rotating around the vertical axis, the front card big and sharp, the back ones dim and blurred), or a grid that fills up.
Chrome headline "5 SPEAKERS" / "ALL OF THIS" + serif italic "*Before and after Claude*" / "*4 speakers. one skill*".

## Specs
- Cards: 380×680, radius 40, 8 px dark bezel, each plays a different edit (muted except the front one). Front card has a BEFORE mini-card (160×280) pinned bottom-left that swaps raw ↔ after.
- **Fan**: 5 cards, angles −24°, −12°, 0°, +12°, +24° around a pivot 1400 px below; centre card z +120, scale 1.08. Cards slide in one by one from the bottom (6 f apart).
- **Orbit**: 6–8 cards on a ring radius 620, rotateY step 360/n, the ring rotates 1 card per 1.4 s with ease-in-out and a 0.3 s hold; back cards opacity .35 + blur 6.
- **Grid**: 3×3 (or 2×2), 12 px gaps, cells light up one by one, then all play; a light sweep across.
- Background: ribbed charcoal (§8) or blue→violet curtain (`#16224a → #5a3aa8` stripes).
- Bottom: CTA pill or prompt bar "Edit all 4 clips in my style · ✻ video-editing".

## Sound
Whoosh per card, a "tick" on each orbit step, the front card's audio at −6 dB, music bed −14 dB.

## Voice & music (measured on the references)
Music-led: a hip-hop / rap track WITH vocals (e.g. DfSI1E8Nac8) carries it, the front card's voice low or muted; very few SFX (0.3 hits/s), the orbit steps sit on the beat.

## Opening (measured at 10 fps on 5 wrappers: W06, W10, C09, D08, L06)
**There is no intro build.** Frame 0 already shows the full layout: comment bubble, tag, chrome headline + subline, both phones, prompt
bar. The first frame IS the cover (feed thumbnail) — it must read instantly. Only these move: the AFTER clip plays from its first beat
(already mid-sentence), the BEFORE clip plays raw, the CTA pill fades in at 0.4–0.7 s, a carousel keeps turning. Ignore my older
"0–1 s build-up" timings in this file: build-ups lose the scroll.
