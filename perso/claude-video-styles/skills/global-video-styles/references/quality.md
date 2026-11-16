# Picture & render quality — rules (from the failed first test, 2026-11-12, and the references)

the user's verdict on the first test (n8n, Dark Teal): « the video quality is so bad … and the sounds and every thing ».
What was wrong, and the rule that prevents it:

| What went wrong | Rule |
|---|---|
| Built from a 1080p SDR intermediate (`talk-clean.mp4`) instead of the 4K HLG original | **Always start from the camera original** (iPhone 4K HEVC HLG). Cut with frame-exact timestamps on the original, tone-map once (below), keep 2160×3840 until the final render. |
| The speaker was shrunk to 80 % over a blurred copy of himself → cheap letterbox look | **Never shrink the speaker into a box.** The references always keep the person full frame. If the shot is a tight selfie (face fills the frame), choose elements that live on the sides and lower third, put the chrome word on the ribbed scenes / B-roll, or punch OUT is impossible → say it in the plan and pick style 3/5/10 that suit close shots. |
| Phone copy at 720p CRF 23 (that's what he watched) | Phone copy = **1080×1920, CRF 18, AAC 192k**, under 30 MB if possible (else split or keep 1080 and bitrate 10 Mb/s). Never send 720p. |
| Fonts loaded from Google during the render; the Wi-Fi dropped (ERR_NETWORK_CHANGED) → risk of fallback fonts in some chunks | **Bundle every font locally**: download the .woff2/.ttf into `public/fonts/` and load with `@remotion/fonts` `loadFont({family, url: staticFile(...)})`; wait with `delayRender` until `document.fonts.ready`. No network fonts at render time. |
| JPEG intermediate frames, `yuvj420p` (full-range) output | Render with `--image-format=png` (or jpeg quality 100), `--pixel-format=yuv420p`, `--crf=14`, `--x264-preset=slow`, `--color-space=bt709`. Check `ffprobe` shows `yuv420p` and `bt709`. |
| CSS hard-stripe "ribbed" panel and flat chrome looked fake next to their soft fluted glass | Ribbed glass = **rendered texture**, not a CSS stripe: soft cylindrical shading per flute (each flute = a gradient dark→light→dark), irregular flute widths (14–26 px), a blurred reflection of a light source, the diagonal light split with a 1 px bright edge, + 2 % film grain. Build it once as a 2160×3840 PNG (or a Three.js plane with a normal map) and reuse it. |
| Emoji icons in greyscale looked cheap | Use real icon sets: Phosphor (MIT) duotone, or 3D icon PNGs (e.g. free "3dicons" set, CC0) rendered grey-metal; app-icon chips = gradient squircle + white Phosphor glyph. |
| SFX booms on every word + music at −19 dB under the voice | See `sound-design.md`: voice-first, bed −36 … −42 dB, SFX only on scene changes / card landings. |

## Colour pipeline for iPhone HLG footage
```
ffmpeg -i IMG.MOV -vf "zscale=t=linear:npl=203,format=gbrpf32le,zscale=p=bt709,tonemap=tonemap=mobius:desat=0:param=0.35,zscale=t=bt709:m=bt709:r=tv,format=yuv420p10le" -c:v libx265 -crf 12 -preset slow -tag:v hvc1 master_sdr.mp4
```
Then check skin: no clipping on the forehead (max luma < 940/1023), no orange push. The user wants his footage **natural** (no grade, no
vignette) — only the tone-map. A style grade (Violet Glass room violet) applies to the background plate only, never to his skin.

## Sharpness & texture
- Downscale 4K → 1080 with lanczos (Remotion `OffthreadVideo` of the 4K file at 1080 composition scales well; or pre-scale with `scale=1080:1920:flags=lanczos`).
- Light unsharp on the speaker plate only: `unsharp=5:5:0.4:5:5:0.0`. No sharpening on graphics.
- 2–3 % monochrome grain over the whole frame at the end (hides banding in dark gradients). Dither gradients (`filter: url(#noise)` or a grain PNG overlay at 4 % opacity).
- Motion blur on fast moves (fly-ins, streaks): `@remotion/motion-blur` `<Trail>` (6 layers, 0.5 frame) or render the shutter manually.

## Final checks before showing the user (automatic)
1. `ffprobe`: 1080×1920 (or 2160×3840), 30/60 fps, yuv420p, bt709, AAC 48 kHz.
2. Loudness −14 LUFS ±0.5, true peak ≤ −1 dBTP.
3. Contact sheet of 1 frame per beat; zoom-crop 3 frames at 100 % to check text edges, glass blur, cut-out edges (hair).
4. Re-transcribe the final mix with Whisper: every word intelligible.
5. Their own bug list: word too high · plate over a hand · gap between lines too big · start on black · text on text or on the face.
