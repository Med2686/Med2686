# SFX licences and sources

Everything in `sfx/` is free for commercial social-media videos (Instagram, TikTok, YouTube, client work) without a paid licence.
No source here needs attribution. Licences were checked on the source pages on 2026-11-14.
Two rules apply to every source: never sell or share the raw sound files as a sound library, and never register them with
Content ID. Using them inside your own videos is always fine.

| Source | Where on disk | Licence | Commercial | Credit | Main restrictions | Source URL |
|---|---|---|---|---|---|---|
| Mixkit (full catalogue, 2,999 sounds) | `library/mixkit/` (2,249 QC'd one-shots), `packs/mixkit-long/` (750 sounds that are long, noisy or low-band, such as ambiences, beds and booms, kept as lossless FLAC of the original WAV), `packs/mixkit-catalog.json` | Mixkit Sound Effects Free License | yes | not required | no redistribution as standalone files or a library | https://mixkit.co/free-sound-effects/ · https://mixkit.co/license/#sfxFree |
| Freesound (1,918 sounds, 124 queries in `freesound_queries.txt`) | `library/freesound/` | CC0 1.0 (public domain) only: the search uses the CC0 filter and each result's licence badge is checked again | yes | not required | none (CC0) | https://freesound.org (each sound's page is in `index.json` → `page`) |
| uisfx | `library/uisfx/` | CC0 1.0 | yes | not required | none | https://github.com/romainsimon/uisfx |
| Kenney audio packs | `packs/kenney/<pack>/` (each pack has its own `License.txt`) | CC0 1.0 | yes | not required (Kenney says "would be nice") | none | https://kenney.nl/assets/category:Audio |
| OpenGameArt | `packs/opengameart/<pack>/` (`.done` holds the page, author and licence seen) | CC0 1.0. A pack is downloaded only if its page lists CC0 | yes | not required | none | https://opengameart.org (one URL per pack below) |
| Sonniss #GameAudioGDC 2026 (Part 9) | `packs/sonniss-gdc2026/` (licence PDF inside) | Sonniss GDC Bundle licence v2.0 | yes | not required | no reselling or redistributing the sounds as SFX, no claiming authorship, **no AI/ML training** | https://gdc.sonniss.com/ · https://sonniss.com/gdc-bundle-license/ |
| Sonniss #GameAudioGDC 2024 (Part 8) | `packs/sonniss-gdc2024/` | Sonniss GDC Bundle licence | yes | not required | same as above | https://sonniss.com/gameaudiogdc |
| synth | `synth/`, library `synth/*` | own (procedural, `sfx_synth.py`) | yes | — | — | — |

Sonniss terms in short: royalty-free, lifetime and worldwide, for personal and commercial projects (games, film, TV, online
video), with no attribution. Finished projects can be published and sold normally. You cannot supply the sounds to anyone else as
sound effects; sharing with your own team on your own projects is allowed. Extracting features for `sfx_match.py` is search, not
AI training. Never feed these files to a model.

## Sources not used, and why

| Source | Why it was skipped |
|---|---|
| BBC Sound Effects | RemArc licence: personal, educational and research use only. Not allowed in commercial videos. |
| Zapsplat (free tier) | Needs an account and requires attribution. |
| Pixabay sound effects | The pages have no direct file links. Bulk download would need browser automation, and Pixabay's terms forbid scraping. Single sounds can be downloaded by hand in a browser (Pixabay Content License, commercial OK). |
| 99Sounds | Free and royalty-free, but every download goes through a Gumroad checkout form that asks for an email. |
| Sonniss GDC 2021–2023 (38.7 GB) and 2015–2020 | Direct downloads with no login, but they would go over the 45 GB budget. Only the two most recent bundles were taken (there was no 2025 bundle). |
| ElevenLabs / any AI generation, YouTube rips | Never used. |

## Excluded sounds
Every file whose name, title or tags contain "glass" (and UCS category `GLAS…`) stays on disk, but `index.json` flags it
`excluded` and `sfx_match.py` never suggests it, because the user hates the glass sound.

## OpenGameArt packs (all CC0; two are dual-licensed OGA-BY 3.0 / CC0, used under CC0)

| Folder | Title | Author (OGA user) | Licences listed | Page |
|---|---|---|---|---|
| 10-8bit-coin-sounds | 10 8bit coin sounds | lukerustltd | CC0 | https://opengameart.org/content/10-8bit-coin-sounds |
| 100-cc0-sfx | 100 CC0 SFX | rubberduck | CC0 | https://opengameart.org/content/100-cc0-sfx |
| 100-cc0-sfx-2 | 100 CC0 SFX #2 | rubberduck | CC0 | https://opengameart.org/content/100-cc0-sfx-2 |
| 16-button-clicks | 16 button clicks | qubodup | CC0 | https://opengameart.org/content/16-button-clicks |
| 202-more-sound-effects | 202 More Sound Effects | owlishmedia | CC0 | https://opengameart.org/content/202-more-sound-effects |
| 25-cc0-bang-firework-sfx | 25 CC0 bang / firework SFX | rubberduck | CC0 | https://opengameart.org/content/25-cc0-bang-firework-sfx |
| 30-cc0-sfx-loops | 30 CC0 SFX loops | rubberduck | CC0 | https://opengameart.org/content/30-cc0-sfx-loops |
| 35-wooden-crackshitsdestructions | 35 wooden cracks/hits/destructions | qubodup | CC0 | https://opengameart.org/content/35-wooden-crackshitsdestructions |
| 37-hitspunches | 37 hits/punches | qubodup | CC0 | https://opengameart.org/content/37-hitspunches |
| 40-cc0-water-splash-slime-sfx | 40 CC0 water / splash / slime SFX | rubberduck | CC0 | https://opengameart.org/content/40-cc0-water-splash-slime-sfx |
| 50-cc0-retro-synth-sfx | 50 CC0 retro / synth SFX | rubberduck | CC0 | https://opengameart.org/content/50-cc0-retro-synth-sfx |
| 50-cc0-sci-fi-sfx | 50 CC0 Sci-Fi SFX | rubberduck | CC0 | https://opengameart.org/content/50-cc0-sci-fi-sfx |
| 50-free-scifi-soundfx-192khz-64-bit-24576kbps-wav | 50 Free SciFi SoundFX - 192kHz, 64-bit 24,576kbps WAV | blacklodgegames | CC0 | https://opengameart.org/content/50-free-scifi-soundfx-192khz-64-bit-24576kbps-wav |
| 512-sound-effects-8-bit-style | 512 Sound Effects (8-bit style) | subspaceaudio | CC0 | https://opengameart.org/content/512-sound-effects-8-bit-style |
| 7-assorted-sound-effects-menu-level-up | 7 Assorted Sound Effects (Menu, Level Up) | joth | CC0 | https://opengameart.org/content/7-assorted-sound-effects-menu-level-up |
| 75-cc0-breaking-falling-hit-sfx | 75 CC0 breaking / falling / hit sfx | rubberduck | CC0 | https://opengameart.org/content/75-cc0-breaking-falling-hit-sfx |
| 80-cc0-rpg-sfx | 80 CC0 RPG SFX | rubberduck | CC0 | https://opengameart.org/content/80-cc0-rpg-sfx |
| atmospheric-interaction-sound-pack | Atmospheric Interaction Sound Pack | qubodup | CC0 | https://opengameart.org/content/atmospheric-interaction-sound-pack |
| bubbles-pop | bubbles 'pop' | farfadet46 | CC0 | https://opengameart.org/content/bubbles-pop |
| card-game-sounds | Card Game sounds | haeldb | CC0 | https://opengameart.org/content/card-game-sounds |
| click | Click | qubodup | CC0 | https://opengameart.org/content/click |
| completion-sound | Completion sound. | haeldb | OGA-BY 3.0, CC0 | https://opengameart.org/content/completion-sound |
| door-open-door-close-set | Door Open, Door Close Set | qubodup | CC0 | https://opengameart.org/content/door-open-door-close-set |
| energy-drain | Energy Drain | qubodup | CC0 | https://opengameart.org/content/energy-drain |
| fantasy-sound-effects-tinysized-sfx | Fantasy Sound Effects (Tinysized SFX) | vehicle | CC0 | https://opengameart.org/content/fantasy-sound-effects-tinysized-sfx |
| gui-sound-effects | GUI Sound Effects | lokif | CC0 | https://opengameart.org/content/gui-sound-effects |
| heartbeat-sounds | Heartbeat sounds | bart | CC0 | https://opengameart.org/content/heartbeat-sounds |
| hi-tech-button-sound-pack-i-non-themed | Hi-Tech Button Sound Pack I (Non Themed) | circlerun | CC0 | https://opengameart.org/content/hi-tech-button-sound-pack-i-non-themed |
| impact | Impact | qubodup | CC0 | https://opengameart.org/content/impact |
| level-up-power-up-coin-get-13-sounds | Level up, power up, Coin get (13 Sounds) | wobbleboxx | CC0 | https://opengameart.org/content/level-up-power-up-coin-get-13-sounds |
| magic-spell-sfx | Magic Spell SFX | jaggedstone | CC0 | https://opengameart.org/content/magic-spell-sfx |
| platformer-sounds-terminal-interaction-door-shots-bang-and-footsteps | Platformer Sounds: Terminal, Interaction, Door, Shots, Bang and Footsteps | yd | CC0 | https://opengameart.org/content/platformer-sounds-terminal-interaction-door-shots-bang-and-footsteps |
| point-bell | Point bell | haeldb | OGA-BY 3.0, CC0 | https://opengameart.org/content/point-bell |
| sound-effects-pack | Sound Effects Pack | owlishmedia | CC0 | https://opengameart.org/content/sound-effects-pack |
| space-ship-shield-sounds | Space Ship Shield Sounds | bart | CC0 | https://opengameart.org/content/space-ship-shield-sounds |
| steam-release-sounds | Steam release sounds | bart | CC0 | https://opengameart.org/content/steam-release-sounds |
| superpowers-assets-sound-effects | Superpowers assets sound effects | medicinestorm | CC0 | https://opengameart.org/content/superpowers-assets-sound-effects |
| swish-bamboo-stick-weapon-swhoshes | Swish - bamboo stick weapon swhoshes | qubodup | CC0 | https://opengameart.org/content/swish-bamboo-stick-weapon-swhoshes |
| swishes-sound-pack | Swishes Sound Pack | artisticdude | CC0 | https://opengameart.org/content/swishes-sound-pack |
| synthesized-explosion | Synthesized explosion | qubodup | CC0 | https://opengameart.org/content/synthesized-explosion |
| ui-sounds | UI Sounds | stumpystrust | CC0 | https://opengameart.org/content/ui-sounds |
| wind-hit-time-morph | Wind, hit, time morph | qubodup | CC0 | https://opengameart.org/content/wind-hit-time-morph |
| wood-and-metal-sound-effects-volume-2 | Wood and Metal Sound Effects: Volume 2 | ogrebane | CC0 | https://opengameart.org/content/wood-and-metal-sound-effects-volume-2 |

## Kenney packs (all CC0, by Kenney Vleugels)

| Folder | Page |
|---|---|
| casino-audio | https://kenney.nl/assets/casino-audio |
| digital-audio | https://kenney.nl/assets/digital-audio |
| impact-sounds | https://kenney.nl/assets/impact-sounds |
| interface-sounds | https://kenney.nl/assets/interface-sounds |
| music-jingles | https://kenney.nl/assets/music-jingles |
| rpg-audio | https://kenney.nl/assets/rpg-audio |
| sci-fi-sounds | https://kenney.nl/assets/sci-fi-sounds |
| ui-audio | https://kenney.nl/assets/ui-audio |
| voiceover-pack | https://kenney.nl/assets/voiceover-pack |
| voiceover-pack-fighter | https://kenney.nl/assets/voiceover-pack-fighter |
