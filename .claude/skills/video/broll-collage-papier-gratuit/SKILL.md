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
- Demi-teinte d'impression (trame à 45°, bruit d'encre) visible même sur les teintes foncées ; les couleurs ressortent un peu passées, ce qui est voulu (look imprimé). Les petits détails (< 4 % de la largeur) se perdent dans la trame : les garder gros.
- Animation « boil » : une fois posées, les pièces tremblent légèrement à 12 images/s (effet stop-motion papier). Désactiver avec `"boil": false` dans spec.json.

## Protocole en 3 portes (ne jamais sauter une porte)

**Porte 1 — Métaphore (texte seul).** À partir de la phrase, proposer 3 métaphores visuelles (une idée forte chacune, 3–5 pièces max :
sujet principal, 1–2 éléments de contexte, 1 élément de mouvement/direction). Pour chacune : liste des pièces, ordre d'arrivée, sens du récit.
Attendre le choix de l'utilisateur. Rien d'autre n'est produit avant.

**Porte 2 — Image fixe finale.**
1. Créer un dossier de travail `mission/…`-hors-dépôt ou `/tmp`, par exemple `collage-<sujet>/pieces/`.
2. Écrire un SVG par pièce (fond transparent, viewBox serré autour de la forme, 2–4 couleurs plates, formes simples, pas de texte fin).
   Palette éditoriale : couleurs moyennes, un accent chaud (rouge/orange), un neutre sombre, un bleu ou vert.
   **Commencer par `bibliotheque/`** (12 pièces prêtes : soleil, loupe, cadenas, graphique, coche, croix, pièce, personne, double engrenage, bulle, maison, flèche courbe) : copier/adapter plutôt que redessiner. Ne dessiner de zéro que ce qui manque. Pour un rendu plus riche : une pièce = 2–3 formes superposées (aplat + reflet clair + ombre propre), pas de dégradés complexes.
   Modèles supplémentaires : `exemple/pieces/*.svg`.
3. Rastériser : `node scripts/svg2png.mjs collage-<sujet>/pieces collage-<sujet>/pieces_png 1200`
4. Écrire `spec.json` (voir format ci-dessous), puis : `python3 scripts/collage.py collage-<sujet>/spec.json --still collage-<sujet>/final.png`
5. **Regarder l'image** (outil Read) : lisibilité, équilibre, pièces qui se chevauchent mal. Corriger avant de la montrer.
Montrer l'image à l'utilisateur ; attendre son accord.

**Porte 3 — Animation.** `python3 scripts/collage.py collage-<sujet>/spec.json --video collage-<sujet>/b-roll.mp4`
puis contrôler : `ffmpeg -i b-roll.mp4 -vf "select='not(mod(n,24))',tile=5x1" -frames:v 1 planche.png` et regarder la planche.
Livrer le MP4 muet, sauf demande de voix off :

```bash
scripts/voix_off.sh "La phrase à dire." voix.wav 4.5 b-roll.mp4 b-roll-voix.mp4
```
Moteurs essayés dans l'ordre : `edge-tts` (voix naturelle, gratuite mais service en ligne non officiel de Microsoft → ne pas l'utiliser pour des contenus confidentiels), `piper` (si `PIPER_MODEL` pointe vers une voix .onnx), puis `espeak-ng` (hors ligne, **robotique**, installable par `apt-get install -y espeak-ng`).
Le script accélère la voix jusqu'à ×1,35 pour tenir dans la durée ; au-delà il avertit : raccourcir le texte.
Annoncer à l'utilisateur quel moteur a servi et que `espeak-ng` est une voix de secours, pas de qualité « production ». Sous-titres → `montage-son-et-medias`.

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
`exemple/demo-voix.mp4` : même clip avec voix `espeak-ng`. Régénérer : voir les commandes ci-dessus avec `exemple/` comme dossier (les PNG de `pieces_png/` se recréent avec `svg2png.mjs`).
