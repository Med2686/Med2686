---
name: video
description: Point d'entrée unique pour tout ce qui touche à la production vidéo / animation / motion design / slideshow en code (HyperFrames, onetake, collage b-roll, Lemo-Opuscar). Utiliser quand l'utilisateur demande une vidéo, un teaser, une vidéo explicative, un B-roll, un film en code, un slideshow HTML, ou tape /video. Route vers le bon sous-skill.
---

# /video — routeur des skills vidéo

Les sous-skills ne sont **pas** chargés automatiquement : ils vivent dans `.claude/skills/video/<nom>/`.
Après avoir choisi, **lis `.claude/skills/video/<nom>/SKILL.md` en entier** et suis-le.
Les chemins `skills/<nom>/...` cités dans ces sous-skills s'entendent comme `.claude/skills/video/<nom>/...`.
Quand un sous-skill en mentionne un autre par son nom, va lire son `SKILL.md` de la même façon.

Si la demande est vague, pose d'abord la question : quel format, quelle durée, quel usage ?
Ne lance aucun rendu long ni appel d'API payante (HeyGen, Gemini) sans accord de l'utilisateur.

## Choisir

| Besoin | Sous-skill |
|---|---|
| Vidéo HTML→MP4 générique (lancement, explicatif, captions, graphiques, vertical) | `hyperframes` (lire en premier), + `hyperframes-cli` pour scaffold/rendu |
| Blocs prêts à l'emploi (transitions, titres, overlays, 3D…) | `hyperframes-registry` |
| Musique, bruitages, voix off, images, logos, avatars, étalonnage | `media-use` |
| Utiliser une maquette / marque Figma dans une vidéo | `figma` |
| Porter du code existant (Remotion, Lottie, Three.js, p5…) vers HyperFrames | `remotion-to-hyperframes` |
| Reconstruire une vidéo existante en projet éditable | `reverse-any-video` |
| Présentation HTML projetée en direct (pas une vidéo rendue) | `slideshow` |
| Court clip produit/skill 10–60 s, motion « haut de gamme », sans HyperFrames | `onetake` |
| B-roll collage papier demi-teinte à partir d'une phrase de 5 s | `collage-broll-explainers` (gemini-omni-flash) ou `gbro-collage-broll` (variante FR/CN, écrite pour Codex) — proposer l'un, ne pas lancer les deux |
| Film en code dans un style nommé (huile, aquarelle, ukiyo-e, démontage produit…) | `lemo-opuscar` |

## Prérequis à vérifier avant de promettre un résultat

- Node.js, ffmpeg, Chrome/Chromium pour tous les rendus.
- `GEMINI_API_KEY` pour les deux skills de collage ; compte HeyGen pour une partie de `media-use`.
- `onetake` : licence PolyForm Noncommercial — alerter l'utilisateur avant tout usage client/commercial.
- Aucun de ces sous-skills n'a été testé dans ce dépôt : annoncer les échecs tels quels.
