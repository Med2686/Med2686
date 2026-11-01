---
name: video
description: Point d'entrée unique pour la vidéo, organisé par tâche : couper/monter/couper les silences, sous-titres, voix off, musique et bruitages, étalonnage, reframe vertical, transitions et titres, vidéo explicative/lancement/B-roll, slideshow, reconstruire ou porter une vidéo existante. Utiliser dès que l'utilisateur parle de vidéo, clip, montage, sous-titres, B-roll, motion design, ou tape /video. Route vers le bon sous-skill et le bon fichier.
---

# /video — index par tâche

Les sous-skills sont dans `.claude/skills/video/<nom>/` et **ne sont pas chargés automatiquement**.
Procédure : 1) identifier la tâche ci-dessous ; 2) lire le fichier indiqué (chemin relatif à `.claude/skills/video/`) ;
3) si la tâche produit une vidéo complète, lire aussi le `SKILL.md` du sous-skill de sa famille.
Les sous-skills ont été renommés. Quand un sous-skill ou un script cite l'ancien nom (`skills/<ancien>/...`, `/media-use`, `hyperframes`…), traduire avec la table « Noms » en bas de ce fichier ; les chemins se lisent alors `.claude/skills/video/<nouveau nom>/...`.
Demande vague → d'abord : format, durée, destination, matériel source disponible.
Aucun rendu long ni appel à une API payante (HeyGen, Gemini) sans accord de l'utilisateur.

## A. Travailler sur une vidéo existante (post-production)

| Tâche | Lire |
|---|---|
| Couper / garder un extrait | `montage-son-et-medias/references/operations.md` § Cut / trim |
| Couper les silences, extraire le meilleur moment | `montage-son-et-medias/references/operations.md` § Silence-cut / highlight |
| Couper « par le texte » (supprimer des phrases via la transcription) | `montage-son-et-medias/references/operations.md` § Text-based editing (+ `montage-son-et-medias/scripts/transcript-cut.mjs`) |
| Monter bout à bout plusieurs clips | `montage-son-et-medias/references/operations.md` § Montage / stitch |
| Passer en vertical 9:16 / recadrer | `montage-son-et-medias/references/operations.md` § Reframe / crop, puis `creer-video-html/references/types/vertical.md` |
| Détourer un fond (cutout) | `montage-son-et-medias/audio/references/remove-background.md` |
| Étalonnage, look, image sombre/plate | `montage-son-et-medias/references/grading.md`, `montage-son-et-medias/references/media-treatments.md` |
| Source HEVC/H.265 qui pose problème | `montage-son-et-medias/references/operations.md` § HEVC |

## B. Sous-titres et texte

| Tâche | Lire |
|---|---|
| Transcrire (mots + timings) | `montage-son-et-medias/audio/references/transcribe.md`, `montage-son-et-medias/references/operations.md` § Transcription |
| Sous-titres animés / incrustés | `creer-video-html/references/captions.md`, puis `montage-son-et-medias/audio/references/captions/` |
| Export SRT / VTT | `creer-video-html/references/captions.md` (`--to srt|vtt`) |
| Sous-titres depuis une voix off générée | `montage-son-et-medias/audio/references/tts-to-captions.md` |
| Langues non espacées (zh/ja) ou multilingue | `creer-video-html/references/captions.md`, `clip-produit-motion-pro/SKILL.md` (versions localisées) |
| Titres, lower thirds, overlays | `creer-video-html/references/overlays.md`, `bibliotheque-effets-et-transitions/SKILL.md` |

## C. Son

| Tâche | Lire |
|---|---|
| Voix off (TTS), clonage de voix | `montage-son-et-medias/audio/references/tts.md` |
| Musique de fond | `montage-son-et-medias/audio/references/bgm.md` |
| Bruitages | `montage-son-et-medias/audio/references/sfx.md`, `creer-video-html/references/sound.md` |
| Mixage, ducking, loudness de publication | `montage-son-et-medias/references/mixing.md`, `montage-son-et-medias/references/operations.md` § Ducking / Publish loudness |

## D. Créer une vidéo de zéro

| Besoin | Sous-skill |
|---|---|
| Vidéo HTML→MP4 générique (explicative, lancement, données, personnage, 3D, musique, vertical) | `creer-video-html/SKILL.md` (lire en premier ; types dans `creer-video-html/references/types/`) |
| Scaffold, preview, lint, rendu local/cloud | `rendu-et-outils-hyperframes/SKILL.md` |
| Transitions, effets, titres cinétiques, graphes, 3D prêts à l'emploi (~450 blocs) | `bibliotheque-effets-et-transitions/SKILL.md` |
| Images, icônes, logos, avatar, vidéo générée | `montage-son-et-medias/SKILL.md` |
| Marque / maquette Figma → vidéo | `video-depuis-figma/SKILL.md` |
| Clip produit/skill 10–60 s, motion haut de gamme, sans HyperFrames | `clip-produit-motion-pro/SKILL.md` |
| B-roll collage papier demi-teinte (phrase de 5 s), gratuit et local | `broll-collage-papier-gratuit/SKILL.md` |
| Film en code dans un style nommé (huile, aquarelle, ukiyo-e, démontage…) | `film-en-code-styles-artistiques/SKILL.md` |
| Présentation HTML projetée en direct | `presentation-en-direct/SKILL.md` |

## E. Reprendre un travail existant

| Besoin | Sous-skill |
|---|---|
| Rebuilder une vidéo comme projet éditable | `refaire-une-video-existante/SKILL.md` |
| Porter Remotion / Lottie / Three.js / p5 / Manim… vers HyperFrames | `convertir-animation-vers-hyperframes/SKILL.md` |

## Limites à annoncer honnêtement

- Il n'existe **pas** d'éditeur de montage interactif : la coupe/le montage passent par ffmpeg et les scripts de `montage-son-et-medias`.
- Prérequis : Node.js, ffmpeg, Chrome/Chromium  ; compte HeyGen pour une partie de `montage-son-et-medias` (voix, avatar).
- `clip-produit-motion-pro` (onetake) : licence PolyForm Noncommercial — prévenir avant tout usage client/commercial.
- Rien de tout cela n'a été exécuté dans ce dépôt : annoncer les échecs tels quels. Vérifier qu'un fichier existe avant de promettre son contenu.

## Noms (dossier actuel ← nom d'origine du dépôt amont)

| Dossier | Origine | Rôle en une phrase |
|---|---|---|
| `creer-video-html` | hyperframes | Créer une vidéo à partir de HTML (explicative, lancement, données, vertical…) |
| `rendu-et-outils-hyperframes` | hyperframes-cli | Commandes : créer le projet, prévisualiser, vérifier, rendre |
| `bibliotheque-effets-et-transitions` | hyperframes-registry | ~450 blocs prêts à l'emploi (transitions, titres, effets) |
| `montage-son-et-medias` | media-use | Couper, monter, sous-titrer, voix off, musique, bruitages, étalonnage |
| `video-depuis-figma` | figma | Utiliser une maquette ou une marque Figma dans une vidéo |
| `convertir-animation-vers-hyperframes` | remotion-to-hyperframes | Porter du code d'animation existant (Remotion, Lottie…) |
| `refaire-une-video-existante` | reverse-any-video | Reconstruire une vidéo en projet éditable |
| `presentation-en-direct` | slideshow | Diaporama HTML présenté en direct |
| `clip-produit-motion-pro` | onetake | Clip produit 10–60 s au motion soigné (licence non commerciale) |
| `broll-collage-papier-gratuit` | créé ici | B-roll collage papier animé, 100 % local et gratuit (remplace VOX-COLLAGE-BROLL et gbro-collage-broll, supprimés car payants) |
| `film-en-code-styles-artistiques` | lemo-opuscar | Film dans un style nommé (huile, aquarelle, ukiyo-e…) |

Le champ `name:` dans chaque `SKILL.md` interne est resté celui d'origine (pour pouvoir réimporter une mise à jour amont).

## Règle « gratuit d'abord »

Ne jamais déclencher d'abord une option payante. Par défaut : voix locale (Kokoro), images/logos gratuits ou fournis par l'utilisateur,
vidéo locale. HeyGen (voix premium, avatar, images/vidéo générées) uniquement si l'utilisateur le demande explicitement, après l'avoir prévenu du coût.
