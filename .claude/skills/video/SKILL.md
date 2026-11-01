---
name: video
description: Point d'entrée unique pour la vidéo, organisé par tâche : couper/monter/couper les silences, sous-titres, voix off, musique et bruitages, étalonnage, reframe vertical, transitions et titres, vidéo explicative/lancement/B-roll, slideshow, reconstruire ou porter une vidéo existante. Utiliser dès que l'utilisateur parle de vidéo, clip, montage, sous-titres, B-roll, motion design, ou tape /video. Route vers le bon sous-skill et le bon fichier.
---

# /video — index par tâche

Les sous-skills sont dans `.claude/skills/video/<nom>/` et **ne sont pas chargés automatiquement**.
Procédure : 1) identifier la tâche ci-dessous ; 2) lire le fichier indiqué (chemin relatif à `.claude/skills/video/`) ;
3) si la tâche produit une vidéo complète, lire aussi le `SKILL.md` du sous-skill de sa famille.
Les chemins `skills/<nom>/...` cités dans les sous-skills s'entendent comme `.claude/skills/video/<nom>/...`.
Demande vague → d'abord : format, durée, destination, matériel source disponible.
Aucun rendu long ni appel à une API payante (HeyGen, Gemini) sans accord de l'utilisateur.

## A. Travailler sur une vidéo existante (post-production)

| Tâche | Lire |
|---|---|
| Couper / garder un extrait | `media-use/references/operations.md` § Cut / trim |
| Couper les silences, extraire le meilleur moment | `media-use/references/operations.md` § Silence-cut / highlight |
| Couper « par le texte » (supprimer des phrases via la transcription) | `media-use/references/operations.md` § Text-based editing (+ `media-use/scripts/transcript-cut.mjs`) |
| Monter bout à bout plusieurs clips | `media-use/references/operations.md` § Montage / stitch |
| Passer en vertical 9:16 / recadrer | `media-use/references/operations.md` § Reframe / crop, puis `hyperframes/references/types/vertical.md` |
| Détourer un fond (cutout) | `media-use/audio/references/remove-background.md` |
| Étalonnage, look, image sombre/plate | `media-use/references/grading.md`, `media-use/references/media-treatments.md` |
| Source HEVC/H.265 qui pose problème | `media-use/references/operations.md` § HEVC |

## B. Sous-titres et texte

| Tâche | Lire |
|---|---|
| Transcrire (mots + timings) | `media-use/audio/references/transcribe.md`, `media-use/references/operations.md` § Transcription |
| Sous-titres animés / incrustés | `hyperframes/references/captions.md`, puis `media-use/audio/references/captions/` |
| Export SRT / VTT | `hyperframes/references/captions.md` (`--to srt|vtt`) |
| Sous-titres depuis une voix off générée | `media-use/audio/references/tts-to-captions.md` |
| Langues non espacées (zh/ja) ou multilingue | `hyperframes/references/captions.md`, `onetake/SKILL.md` (versions localisées) |
| Titres, lower thirds, overlays | `hyperframes/references/overlays.md`, `hyperframes-registry/SKILL.md` |

## C. Son

| Tâche | Lire |
|---|---|
| Voix off (TTS), clonage de voix | `media-use/audio/references/tts.md` |
| Musique de fond | `media-use/audio/references/bgm.md` |
| Bruitages | `media-use/audio/references/sfx.md`, `hyperframes/references/sound.md` |
| Mixage, ducking, loudness de publication | `media-use/references/mixing.md`, `media-use/references/operations.md` § Ducking / Publish loudness |

## D. Créer une vidéo de zéro

| Besoin | Sous-skill |
|---|---|
| Vidéo HTML→MP4 générique (explicative, lancement, données, personnage, 3D, musique, vertical) | `hyperframes/SKILL.md` (lire en premier ; types dans `hyperframes/references/types/`) |
| Scaffold, preview, lint, rendu local/cloud | `hyperframes-cli/SKILL.md` |
| Transitions, effets, titres cinétiques, graphes, 3D prêts à l'emploi (~450 blocs) | `hyperframes-registry/SKILL.md` |
| Images, icônes, logos, avatar, vidéo générée | `media-use/SKILL.md` |
| Marque / maquette Figma → vidéo | `figma/SKILL.md` |
| Clip produit/skill 10–60 s, motion haut de gamme, sans HyperFrames | `onetake/SKILL.md` |
| B-roll collage papier demi-teinte (phrase de 5 s) | `collage-broll-explainers/SKILL.md` **ou** `gbro-collage-broll/SKILL.md` — en proposer un seul |
| Film en code dans un style nommé (huile, aquarelle, ukiyo-e, démontage…) | `lemo-opuscar/SKILL.md` |
| Présentation HTML projetée en direct | `slideshow/SKILL.md` |

## E. Reprendre un travail existant

| Besoin | Sous-skill |
|---|---|
| Rebuilder une vidéo comme projet éditable | `reverse-any-video/SKILL.md` |
| Porter Remotion / Lottie / Three.js / p5 / Manim… vers HyperFrames | `remotion-to-hyperframes/SKILL.md` |

## Limites à annoncer honnêtement

- Il n'existe **pas** d'éditeur de montage interactif : la coupe/le montage passent par ffmpeg et les scripts de `media-use`.
- Prérequis : Node.js, ffmpeg, Chrome/Chromium ; `GEMINI_API_KEY` pour les skills de collage ; compte HeyGen pour une partie de `media-use` (voix, avatar).
- `onetake` : licence PolyForm Noncommercial — prévenir avant tout usage client/commercial.
- Rien de tout cela n'a été exécuté dans ce dépôt : annoncer les échecs tels quels. Vérifier qu'un fichier existe avant de promettre son contenu.
