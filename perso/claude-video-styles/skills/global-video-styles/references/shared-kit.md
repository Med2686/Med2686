# Shared kit — the building blocks every style reuses

All measurements are for a 1080×1920 canvas. Colours were sampled with k-means from the reference frames
(`eightsenses-study/scripts/palette.py`). Code is Remotion (React + TSX); adapt sizes per style file.

## 1. Fonts (free substitutes first, original in brackets)

| Role | Use | Notes |
|------|-----|-------|
| Chrome headline / word behind head | **League Gothic** (Google) — [orig. Dharma Gothic E Heavy] | ultra-condensed, caps only, tracking −1 %, line-height 0.86. If Dharma Gothic E is installed, use it. Anton is the fallback in the user's brand. |
| Serif italic accent | **Instrument Serif Italic** (Google) | "The prospect", "Before and after Claude", "think again". Sentence case, tracking −2 %. |
| Heavy italic subline overlapping a headline | **Playfair Display 800 Italic** | "on this edit", "just one skill", "Claude adds them". Overlaps the bottom 30 % of the chrome word, rotated −4°. **Not in the user's brand** (no script) → Inter 900 Italic. |
| UI / captions / tags | **Inter** 500 / 600 / 700 | uppercase captions = Inter 600, tracking +2 %. |
| Terminal / code | **JetBrains Mono** 500 | Claude Code look. |
| Arabic (the user) | **Cairo 900** | Latin tech words stay Latin. |

Load with `@remotion/google-fonts/<Name>` (`loadFont()` at module top).

## 2. Global tokens

```ts
export const T = {
  ink: '#08090a', charcoal: '#16191c', panel: '#1c2023', panel2: '#2a2e31', stripeLight: '#363a3c',
  white: '#ffffff', paper: '#f4f5f6', muted: '#9aa0a6',
  claude: '#d97757',           // Claude orange (✻ chip, send button, CTA price) — swap to #E30A17 in the user's brand
  cyan: '#5ad4f0', teal: '#2fd2c0', tealUI: '#2bb3a3', tealDeep: '#0e3224',
  violet: '#7b4dff', violetDeep: '#260b40', violetGlow: '#b48cff', lilac: '#cec7d8',
  sticky: '#ffe066',
};
```

## 3. Chrome text (the signature of styles 1, 2, 4, 5, 8, 9, 10, 11)

Measured profile (top→bottom of the letters): white `#fcfdfe` → cool light grey `#d0d5d9` (35 %) →
**dark horizon band** `#6f747a` (≈50 %) → thin bright line `#f2f4f6` (52 %) → steel `#a9aeb4` (80 %) → white `#ffffff`.
A 4-point sparkle glints on one letter edge; sometimes a cyan scan line sweeps across (see CONDO frame).

```tsx
export const ChromeText: React.FC<{text: string; size: number; style?: React.CSSProperties}> = ({text, size, style}) => (
  <div style={{
    fontFamily: 'League Gothic', fontSize: size, lineHeight: 0.86, letterSpacing: '-0.01em', textTransform: 'uppercase',
    background: 'linear-gradient(180deg,#fcfdfe 0%,#e3e7ea 18%,#c9ced3 36%,#8b9096 47%,#6f747a 50%,#f2f4f6 52.5%,#d6dade 60%,#a9aeb4 80%,#ffffff 100%)',
    WebkitBackgroundClip: 'text', backgroundClip: 'text', color: 'transparent',
    filter: 'drop-shadow(0 6px 18px rgba(0,0,0,.55))', ...style}}>{text}</div>
);
// Sparkle: a 4-point star SVG (two thin diamonds crossed), white, 34–48 px, scale 0→1→0 over 18 frames, rotate 0→45°,
// placed on the top-right corner of one letter, 8 frames after the word lands.
// Scan line: 3 px tall horizontal bar, linear-gradient(90deg, transparent, #7fe9ff, transparent), glow 12 px #5ad4f0,
// sweeps the word's height once (top→bottom) in 14 frames.
```

**Entrance (measured frame by frame, E01/E03/E05):** the word **rises from a hidden baseline** — a mask at the word's bottom edge;
the letters slide up from below it: ≈50 % visible after 1 frame, fully up after 3 frames (ease-out). **No blur, no scale.**
6 frames later the light streak + 4-point sparkle sweeps L→R (≈18 f). On emphasis words the chrome turns icy cyan for ≈12 f (catalog A3).
**Exit:** the word dims to ≈40 % grey over 4 f, then opacity → 0 in 6 f — together with its caption lines. One word on screen at a time.
(The older "scale 1.18 + blur" entrance was my guess and is wrong.)
**Placement**: centre at y ≈ 470–560 (fills 85–95 % of the width, 2–8 letters), the head (matte) covers the middle letters.
In the user's brand the word sits HIGH so it stays readable (only a small part tucked behind his head).

## 4. Text behind the head (layer order)

`<Footage/>` → background graphics (halftone grid, glow) → **ChromeText** → `<OffthreadVideo src=cutout.webm transparent/>` (the person) → tags / plates / captions → overlays (vignette, grain).
The matte must keep hair, glasses and the mic ("Cut-out: hair, glasses, mic" is one of their selling points). Feather 1 px.

## 5. Halftone dot grid (behind the subject in 1, 2, 4)

Fine dots in the upper half of the room: `radial-gradient(circle, rgba(255,255,255,.22) 1.1px, transparent 1.6px)` with
`background-size: 9px 9px`, masked by `radial-gradient(ellipse 70% 45% at 50% 32%, #000 40%, transparent 75%)`.
Opacity 0.35. It sits between the footage and the chrome word.

## 6. Glass tag ("Sales call", "Prospect", "Our clients", "Leaders")

- Box: height 64, padding 0 22 px 0 10 px, radius 16, fill `rgba(28,30,33,.78)`, `backdrop-filter: blur(14px)`,
  top highlight `inset 0 1px 0 rgba(255,255,255,.28)`, outer shadow `0 10px 30px rgba(0,0,0,.45)`, border `1px solid rgba(255,255,255,.10)`
  (the user's brand: **no border**, keep the highlight).
- Icon: 42×42 rounded-10 square, fill `#3a3e42→#1f2225` gradient, a monochrome 3D-ish emoji/icon (people, bag, trophy, camera, target, calendar) in light grey.
- Text: Inter 500, 30 px, `#f2f4f6`.
- Pairs: one left of the face (x≈70–330), one right (x≈760–1010), both at shoulder height (y≈1000 in a full frame), tilted −3° / +3°.
- In (measured): 1 frame blurred and half transparent → sharp in 2 frames, no travel; left first, the right one on its own spoken word
  (often 0.6–0.8 s later). Idle bob ±4 px. Silent (no pop in their mix).

## 7. Caption system "small caps + big serif italic" (styles 1, 4, 10)

```
WHEN I'M ON A SALES CALL      ← Inter 600, 34 px, uppercase, white, tracking +2 %, centred
The prospect                  ← Instrument Serif Italic, 96–110 px, white, line-height .95, centred, 4 px under
```
- y: line 1 at ≈1140–1180, line 2 right under (the chest). Both have `text-shadow 0 4px 20px rgba(0,0,0,.6)`.
- Line 1 types word by word with the voice (each word fades in 3 frames on its timestamp).
- Line 2 = the key phrase of the beat; it lands with blur 12→0 and y+12→0 in 8 frames when the speaker says it.
- Violet Glass variant: line 1 is a **cream pill** (`#f1ebe2`, radius 999, Inter 500 26 px dark `#2a2230`, padding 6×16) and line 2 mixes
  sans + serif: "guides" (Inter 500, 76 px) + "*people*" (Playfair Display 800 Italic, 84 px) with a thin underline.
- Plain caption (Neon Mono, Silver Infographic): Inter 600 uppercase 34–38 px white, 2–5 words, centred at y≈1300.

## 8. Ribbed glass panel (full-screen cut-away "schema scene")

**Quality note:** the CSS below is only a placeholder. The real look is soft fluted glass — each flute a cylinder (dark edge → light
centre → dark edge), irregular widths 14–26 px, a blurred light reflection, the diagonal split with a 1 px bright edge, 2 % grain.
Pre-render it as a 2160×3840 PNG (`scripts/make_ribbed.py` if present, else build in Three.js) — see `quality.md`.
**Transition into it (measured): NOT a wipe.** A cyan dot appears on the speaker shot 0.2–0.3 s before, at the exact spot it will
have in the scene, then a 6-frame cross-dissolve (bridge-dot dissolve, catalog E1). Riser into it, soft whoosh out.

The background of every abstract scene in 1, 4, 8, 9, 10: vertical flutes + one diagonal light split.

```tsx
const ribs = 'repeating-linear-gradient(90deg,#1b1f22 0px,#2f3336 14px,#3c4043 20px,#2a2e31 28px,#16191c 38px)';
const split = 'linear-gradient(118deg, rgba(0,0,0,0) 49.6%, rgba(255,255,255,.10) 50%, rgba(255,255,255,.03) 62%, rgba(0,0,0,0) 100%)';
// <AbsoluteFill style={{background: `${split}, ${ribs}`}}/> + a soft top light: radial-gradient(60% 35% at 50% 0%, rgba(255,255,255,.12), transparent)
```
Measured: flutes `#16191c / #232729 / #2e3234 / #383c3f / #424649`, light side `#6f7b7e–#999999`.
Content on it: chrome title at top (y≈140–260), then a **cyan step path**: numbered nodes (28 px circle `#5ad4f0`, white number Inter 700 16 px,
glow `0 0 18px #5ad4f0`) linked by a 3 px cyan curve drawn with `strokeDashoffset` (or dashed 6/8 for "Waffle → Use it → Close"),
each node with a glass tag (§6) or a serif-italic label. Nodes appear one per spoken item, the curve draws to the next node in 10 frames.

## 9. Photo plate ("QUALITY CONTENT", "A UNIT NEARBY")

Dark glass card 560×320, radius 22, header strip 56 px of ribs (§8 at 40 % size) with "★ QUALITY CONTENT" (Inter 600 24 px caps),
inside a photo (generated or stock) with radius 14; 1–3 small glass chips orbit its corners ("Our clients", "To create ✓" with a blue check badge `#3b82f6`).
Enters with a 3D tilt: rotateX 18° → 0, y+60 → 0, opacity, 12 frames; floats ±6 px (sin, 3 s period).

## 10. Comment bubble hook (promo styles 5, 6, 7, 10)

White pill 640–760 × 96, radius 48, shadow `0 12px 40px rgba(0,0,0,.35)`; grey avatar circle 56 px (gradient #d9d9d9→#9a9a9a);
line 1 "some_editor · 2m" Inter 500 22 px `#8a8a8a`; line 2 the hater line ("Claude can't edit. It's garbage.") Inter 700 34 px `#111`, preceded by a ✻ in `#d97757`.
Variants: **yellow sticky** (`#ffe066` → `#ffd84a`, square corners 6 px, rotated −2°, Inter 700) and **dark Instagram-like card** (white text on `#1a1a1a`).
In: drop from y−40 + scale .92 with a little overshoot, 10 frames, sound "pop".

## 11. Orange tag + headline stack (promo)

`✻ 1 skill` pill: `#d97757`, radius 10, rotated −4°, Inter 700 30 px white, placed left of a small white line ("I spent", "skip the", "no After Effects.") Inter 700 40 px.
Then the **ChromeText** headline (130–190 px) and the **heavy italic subline** overlapping it (Playfair 800 Italic 70–90 px, white, rotated −4°, x-offset +60).

## 12. Prompt bar ("Edit this in my style")

Dark: 860×110, radius 26, fill `#1f2124`, inner border `rgba(255,255,255,.08)`; left chip "📎 raw.mp4" (`#2b2d31`, Inter 500 24 px `#c9c9c9`);
text Inter 500 36 px white typed at 2 chars/frame with a blinking caret; right chip "✻ video-editing" (`#3a2a24` fill, `#d97757` text);
send button 72 px circle `#d97757` with ↑. Light variant: fill `#f5f2ee`, text `#1c1c1c`.
Chips under it appear one by one when the edit "happens": "✓ Cut the pauses", "✓ Word behind the head", "✓ Infographics", "✓ Sound" (Inter 600 22 px, teal check `#2fd2c0`, pill `#1a2a2a` with teal border).

## 13. Phone frames + BEFORE / AFTER

Phone card radius 44, 10 px bezel `#1e2023` with a 1 px `rgba(255,255,255,.18)` rim, shadow `0 30px 80px rgba(0,0,0,.6)`.
BEFORE: 340×600, rotated −4° to −6°, left, lower. AFTER: 470×830, upright or +2°, right, higher. Label pills on the top corner:
"BEFORE" (dark pill, Inter 700 26 px) and "✻ AFTER" (dark pill, orange ✻). Cyan curved arrow (stroke 5, `#7fd3f7`) or dotted arc from a ✻ app icon to the AFTER phone.
The AFTER phone plays the real edited video; BEFORE plays the raw (muted).

## 14. CTA pill

White pill 520×74, radius 37, Inter 700 30 px `#111`: "✻ Get the skills for only **$20**" (price in `#d97757`). Bottom at y≈1700.
Light-theme variant: black pill, "Comment **EDIT** for the skill" (EDIT in `#2fd2c0`). In the user's brand: black pill, red keyword.

## 15. Motion vocabulary

| Move | Spec |
|------|------|
| Land (words, tags) | spring {damping 14, stiffness 170, mass .8}; from scale .9 + y 24 + blur 8 |
| Card fly-in | rotateX 18°→0, rotateY ±12°→0, z −300→0, 14 frames, ease out-cubic |
| Camera on footage | slow push 1.00→1.06 per beat; punch-in 1.00→1.12 in 4 frames on the key word, hold, ease back in 20 |
| Shake (Violet Glass, impacts) | 6 frames, amplitude 14 px → 0, random-seeded, + 2° rotation jitter |
| Transition to schema scene | bridge-dot + 6-frame cross-dissolve (measured); Violet Glass: radial→vertical streak blur 9 f |
| Exit | opacity 1→0 + blur 0→10, 6 frames — never let two plates overlap; check every frame for text on text / text on face |

## 16. Sound design — SUPERSEDED by `sound-design.md` (measured) and the bank `sfx/bank/bank.json`

The table below was my first guess (booms on every word). The measured truth: talking-head styles are voice-first, bed −36 … −42 dB,
SFX only on scene changes and card landings. Keep the table only as a vocabulary list.

| Event | Sound | Level (relative to voice peak) |
|-------|-------|------|
| Chrome word lands | low sub "boom/impact" + short air whoosh | −12 dB |
| Glass tag / chip appears | soft UI pop / bubble click | −18 dB |
| Card / plate flies in | short whoosh (0.3 s) | −16 dB |
| Schema scene / cut-away | whoosh + light riser (0.6 s) into it | −14 dB |
| Node lights up / step ticks | tiny tick / "blip" | −20 dB |
| Typing in prompt bar / terminal | mechanical keys loop | −22 dB |
| Button click ("Convert", send ↑) | mouse click + soft confirm chime | −16 dB |
| Stamp / neon box hits | thump + paper/rubber stamp | −14 dB |
| Outro streaks | reverse swell → cut | −14 dB |

Measured on the ads: a hit every 0.3–0.6 s during dense parts; loudness ≈ −17 dB mean, peaks −1 dB (they master loud).
Music: a soft modern beat (lo-fi / minimal hip-hop or ambient pulse, 90–110 BPM), ducked −14 dB under speech, up to −6 dB in gaps
and on the outro. Master −14 LUFS, true peak −1 dB. **Never the "glass" SFX.**

## 16b. Gotchas from the first build (n8n test, 2026-11-12)

- **Close selfie footage** (face fills the frame): no room for a word behind the head → scale the footage to 0.8, bottom-aligned, over a
  blurred (38 px) darkened copy of itself, feather its edges; chrome word centre y≈318 so only its bottom quarter tucks behind the hair;
  give the cut-out layer the same top feather (else a hard straight cut where the head touches the frame top).
- Any `interpolate(t, [a, b])` built from beat lengths must guard `b > a` (`Math.max(a + 1, b)`): a 9-frame word crashed the render.
- Render in 300-frame chunks with a retry loop (`--frames=a-b --muted`), audio as one separate `--codec=wav` render, concat, then
  `loudnorm=I=-14:TP=-1`. Headless Chrome dies on Wi-Fi changes (`ERR_NETWORK_CHANGED`); a chunk retry saves the rest.

## 17. Brand mapping — when he picks "My brand: black + red"

- Every accent (cyan, teal, violet, Claude orange) → red `#E30A17` (light `#FF3B47`, deep `#B8000F`); backgrounds → `#0D0D0D` / `#141414` / `#1A1A1A`.
- Chrome text → his grey→black metal gradient (`#f2f2f2 → #9a9a9a → #3a3a3a`), key word with a red underline.
- No script/handwritten fonts: Playfair/Instrument italics → **Inter 900 Italic**; Arabic → Cairo 900.
- Glass = frosted, visible, top-left highlight, **no borders**. No cream/white paper cards.
- His footage: natural colours, no grade, never replace his background. Big words sit HIGH.
- No red label pills with his handle; captions = words only (no box).
