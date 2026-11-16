# Sound design — measured on the reference reels (Demucs stems, 2026-11-12)

Method: every soundtrack separated with Demucs htdemucs (voice / drums / bass / other) on the RTX; the voice-free stem plotted
against the frame-accurate visual events (`eightsenses-study/audio/events/*.png`), loudness with ebur128.
Reference cuts of their SFX (for A/B matching only, never in a video): `sfx/refs/ref_*.wav`.

## 1. Loudness targets (all 20 references measured)
- Integrated **−14 LUFS** (−14.0 … −14.4), true peak about **−1 dBTP** (range −2.6 … −0.4). Master to exactly this.
- Voice RMS while speaking ≈ −17 … −20 dBFS.

## 2. Balance per family (bed = everything that is not the voice)

| Family | Music / bed under the voice | In the gaps | Hits per second (loud transients) | What the SFX are |
|---|---|---|---|---|
| **Dark Teal edits** (styles 1, 4) | **−36 … −42 dB** (practically silent) | −20 … −50 dB | 0.1 – 0.5 | a **rising whoosh / riser into each ribbed scene** (≈ −18 dB rel. voice), a soft whoosh back out, a **tiny ping** (≈1.1 kHz, −30 dB) when a card lands, sometimes a short **pre-lap whoosh that ends exactly on the chrome word**. Chrome words, tags, captions: **silent**. |
| **Violet Glass** (style 3) | −42 dB | — | 0.7 | **deep "whoomp"** (sub swell 50–120 Hz + broadband mid + airy top, 0.5 s) on every streak transition **at voice level**; **glass sparkle** (high grains 5–12 kHz + a falling tone) when cards/nodes appear; quiet UI blips on bars/nodes; a falling tonal **smear** on the button click. |
| **Neon Mono edit** (style 2, W1 version) | −36 dB | −39 dB | 0.2 | like Dark Teal: whooshes on scene changes only |
| Ads (styles 5–7 wrappers) | the ad often adds a **trending hip-hop / R&B song at voice level** (−4 … +9 dB) over the edit's voice | — | 0.1 – 1.4 | the song carries it; the edit's own whooshes are buried |
| Narrated explainer / tutorial (10b, 11) | **−11 … −14 dB** | −11 dB | 0.7 | whoosh per chapter/section change |
| Chrome trailer (10a) | song = backbone (rap), no voice-over | — | ≈2 (all musical) | **no added SFX**: every section starts right after a beat break, word lands on the downbeat |
| 3D devices (8) | music at about −4 dB under the clip voice | +7 dB in gaps | 1.9 | soft whooshes |
| Carousel (9) | song only (+15 dB over the muted cards) | | 0.3 | none |
| Luxury property (12) | music ≈ voice (cinematic VO) | | 0.07 | cuts follow the music, almost no SFX |
| Pastel SaaS (13) | music only | | low | UI pings on notification cards |
| Teal ocean (14) | music only (55 dB above any voice) | | — | soft low thumps per card |
| Clean before/after (15) | −8 dB under the clip voice | | 1.4 | the AFTER clip's own SFX |

**Lesson (my first test failed on this):** the talking-head styles are VOICE-FIRST. No boom on every chrome word, no music at
−19 dB under him. Music bed −36 … −42 dB (or none) unless the user wants a song (then make it an "ad" mix: song at voice level only in
the gaps and ducked −8 dB under speech).

## 3. Event → sound map (use the bank roles in `sfx/bank/bank.json`)

| Visual event | Bank role | Level vs voice peak | Timing |
|---|---|---|---|
| Cut to a ribbed scene (bridge-dot dissolve) | `scene_in_riser` | −18 dB | ends exactly on the dissolve's middle frame |
| Back to the speaker | `scene_out_whoosh` | −22 dB | starts 2 f before the dissolve |
| Violet streak transition | `violet_whoomp` | −2 … 0 dB | peak on the most blurred frame |
| Glass card / node appears (Violet) | `glass_sparkle` | −24 dB | onset on the first visible frame |
| Card / plate / chart lands (Dark Teal) | `card_ping` | −30 dB | first sharp frame |
| Chrome word lands | `word_prelap` (optional, 1 in 3 words max) | −28 dB | ENDS on the first full frame of the word |
| Comet reaches a node / chip pops | `node_tick` | −32 dB | on the bloom |
| Counter rolling | `counter_roll` | −32 dB | spans the roll, slows with it |
| Button click (Violet) | `click` + `click_smear` | −20 dB | on the press frame |
| Stamp | `stamp` | −20 dB | on the slam |
| Landing-page dive | `dive_whoosh` | −20 dB | into the thumbnail |
| Typing in a search bar / terminal | `typing` | −30 dB | under the typed characters |

Never stack two SFX within 120 ms. No SFX inside a word's consonant burst if it masks it (check with the voice envelope).
Never the "glass" SFX the user hates (the uisfx `glass/*` pings) — the Violet "sparkle" is a different, airy grain texture.
