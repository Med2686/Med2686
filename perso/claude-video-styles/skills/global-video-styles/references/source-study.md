# Source study — where each style comes from

Study folder: `eightsenses-study/` (the study notes are not included in this repo)
- `ref\<id>.mp4` + `.info.json` — 114 videos from 121 posts of instagram.com/eightsenses.media (downloaded 2026-11-12, yt-dlp; photo slides skipped).
- `boards\board_XX.jpg` + `boards\index.txt` — 8 frames per reel, 5 reels per board (overview of everything).
- `hires\` — full-resolution key frames; `sheets\hi_*.jpg` — 6-frame detail boards per style.
- `audio\scan.json` — Whisper transcript + loud-onset list (SFX hits) per reel.
- `STUDY.md` — first-pass notes. `scripts\` — boards.py, palette.py (k-means hex), audio_scan.py, previews.py.

The account (Eight Senses Media, studio of video editor Ekaterina Nechaeva) sells two $20 Claude skills on Gumroad:
"Style 1 · Dark Teal" and "Style 2 · Violet Glass". **We never use their paid files** — everything here is rebuilt from their public reels.
Posts 2026-03 → 2026-07 = studio portfolio (styles 12–15); 2026-11-01 → 11-12 = ads for the skills (styles 1–11).

| Style | Best reference reels (open with `ref\<id>.mp4`) |
|---|---|
| 1 Dark Teal Chrome | DfSwAKtNITn (8–17 s full screen), DfOzNGchOyY, DfN1SHaPOVQ, DfRtKUJNOAG, DfT8b7ztRC3, DfT8QHptt8e, DfS8usttHKU, DfRtCkXthp0 |
| 2 Neon Mono | DfSxfGCNF0q, DfRszPLNxJK, DfhJhfCj2su, DfnK5SBtupw, DfkTb8UNTad |
| 3 Violet Glass | DfZP4RONqo8, Dfg9ZrMDxD7, DfZnxlXtzO_, DfmfESvjyIa, DfYbpLZI83k, Dfk2Wooj6LQ |
| 4 Silver Infographic | DfUkTLOt_82, DfgGfkRj7Rj, DfaryZmE5a6, DfirSEijwnU, DfcnVhPj5XH |
| 5 Before / After Ad | DfmfESvjyIa, Dfh5hqJj8v9, DfN1SHaPOVQ, Dfpn7X_D2KO, DfZTYkeNi2f, DfjiNrmD9Ry, DfaJYsED0Zd, Dfn03YzE-wO, DfkeSisD6dS |
| 6 Light Paper | DfewpCpD2YR, DfmTAS4D4uS, DfkGRfkkzl9, Dfeftadjxws, Dfdhq5oj2tv |
| 7 App Demo | DfnvsSwMsTk, DfnK5SBtupw, DffgwLZD3Gh, Dff405ZEynK, DffsyTYj9Pi, DfUPOTmthsX, DfdYkhhjz0n, DfdVANVDwk5 |
| 8 3D Studio Devices | DfSobPJtg_S, DfSlxBBt1ye, DfSwlcKNm9r, DfSxBKIto7B |
| 9 Speaker Carousel | DfSI1E8Nac8, DfSyjoxtZk1, DfSev5vtirg, DfSHzAHNxRr, DfhhdADEYs_, DfSolwBtZw5, DfT_u7Xtm8K, DfUA5wuNku1, DfUA--Tt7R3 |
| 10 Chrome Trailer | DfRgE0qt3DJ, DfNkCcqN89n, DfOzNGchOyY, DfRfg5MN8JM |
| 11 Screen Tutorial | DfQToUmPvBm |
| 12 Luxury Property Tour | DWWDIh0jbEa, DWmvVDDDWa4, DWmvPqNDTmr, DWqZYiRjcIB, DZ3UumbNy-U |
| 13 Pastel SaaS Motion | DW8aAzkDYGW, DW8ztQIDVXs |
| 14 Teal Ocean Funnel | DWu0GE-CATD, DWu0OCGCJ4d |
| 15 Clean White Before/After | DZ3VHJLNA28, DXkKEplDWiq, DXlcUpUDa3Y |

To re-check a motion: `ffmpeg -ss <t> -i ref\<id>.mp4 -frames:v 1 x.jpg`, or open the mp4. To re-measure colours:
`python scripts\palette.py <frame> x0 y0 x1 y1 k`.
