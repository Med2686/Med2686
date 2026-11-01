---
name: broll-collage-papier-gratuit
description: Transformer une phrase de ~5 s (voix off, idée, concept abstrait) en B-roll « collage papier demi-teinte » animé (les pièces se posent une à une), 100 % gratuit et local — Claude dessine les pièces en SVG, un script ajoute demi-teinte, bord découpé, ombre et grain papier, ffmpeg produit le MP4. Utiliser pour un collage b-roll, une métaphore visuelle animée, une illustration éditoriale animée, sans API ni clé.
---

# B-roll collage papier — version gratuite

Remplace les anciens skills payants (génération d'images/vidéo par API). Aucune clé, aucun crédit.
Prérequis : `ffmpeg`, `node` + `playwright` (Chromium), `python3` + `pillow` + `numpy`. Vérifier avec
`ffmpeg -version && node -e "require('playwright')" && python3 -c "import PIL,numpy"` avant de promettre quoi que ce soit.

## Ce que c'est — et ce que ce n'est pas

- C'est un style **illustratif** : formes de papier découpé, aplats et demi-teinte. Rapide (≈10 s de rendu), déterministe, entièrement éditable (SVG + JSON).
- Ce n'est **pas** du photoréalisme ni de la génération d'images par IA. Ne pas promettre « mieux » qu'un modèle génératif sur le réalisme ; promettre : gratuit, reproductible, modifiable pièce par pièce.
- Variante réaliste possible : l'utilisateur fournit des PNG détourés (fond transparent) de ses propres photos/logos ; le script leur applique le même traitement.
- Limite connue : les couleurs très foncées/saturées restent en aplat (la demi-teinte y est peu visible). Privilégier des teintes moyennes pour les pièces principales.

## Protocole en 3 portes (ne jamais sauter une porte)

**Porte 1 — Métaphore (texte seul).** À partir de la phrase, proposer 3 métaphores visuelles (une idée forte chacune, 3–5 pièces max :
sujet principal, 1–2 éléments de contexte, 1 élément de mouvement/direction). Pour chacune : liste des pièces, ordre d'arrivée, sens du récit.
Attendre le choix de l'utilisateur. Rien d'autre n'est produit avant.

**Porte 2 — Image fixe finale.**
1. Créer un dossier de travail `mission/…`-hors-dépôt ou `/tmp`, par exemple `collage-<sujet>/pieces/`.
2. Écrire un SVG par pièce (fond transparent, viewBox serré autour de la forme, 2–4 couleurs plates, formes simples, pas de texte fin).
   Palette éditoriale : couleurs moyennes, un accent chaud (rouge/orange), un neutre sombre, un bleu ou vert.
   Modèles : `exemple/pieces/*.svg`.
3. Rastériser : `node scripts/svg2png.mjs collage-<sujet>/pieces collage-<sujet>/pieces_png 1200`
4. Écrire `spec.json` (voir format ci-dessous), puis : `python3 scripts/collage.py collage-<sujet>/spec.json --still collage-<sujet>/final.png`
5. **Regarder l'image** (outil Read) : lisibilité, équilibre, pièces qui se chevauchent mal. Corriger avant de la montrer.
Montrer l'image à l'utilisateur ; attendre son accord.

**Porte 3 — Animation.** `python3 scripts/collage.py collage-<sujet>/spec.json --video collage-<sujet>/b-roll.mp4`
puis contrôler : `ffmpeg -i b-roll.mp4 -vf "select='not(mod(n,24))',tile=5x1" -frames:v 1 planche.png` et regarder la planche.
Livrer le MP4 muet. Pour ajouter une voix off ou des sous-titres → `montage-son-et-medias` (voix locale gratuite Kokoro si installée).

## Format de `spec.json`

```json
{"size":[1280,720], "fps":24, "duration":5, "background":"#efe6d2", "grain":0.05,
 "layers":[
  {"src":"pieces_png/nuage.png", "x":0.80, "y":0.20, "width":0.26, "rot":4,
   "enter":"right", "delay":0.0, "dur":0.8}
 ]}
```
- `x`,`y` : centre final en fraction de l'écran ; `width` : fraction de la largeur ; `rot` : degrés.
- `enter` : `left` `right` `top` `bottom` (glisse), `drop` (tombe en tournant), `spin` (pop tournant), `scale` (pop).
- `delay`/`dur` en secondes. Étaler les arrivées sur ~2,5 s et laisser ≥ 1,5 s de plan final fixe.
- Vertical : `"size":[720,1280]`. 1080p : `[1920,1080]` (rendu plus lent).
- Options par pièce : `"halftone":false` (aplat), `"cell":N` (taille des points), `"strength":0.5–1.2`, `"edge":px` (bord blanc).

## Exemple

`exemple/` contient 4 pièces SVG, `spec.json`, `final.png` et `demo.mp4` (ampoule, engrenage, flèche, nuage).
Régénérer : voir les commandes ci-dessus avec `exemple/` comme dossier.
