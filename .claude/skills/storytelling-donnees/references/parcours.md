# Parcours de progression : Storytelling avec les données (7 étapes)

Chaque étape comporte un **livrable concret sur la mission**, des **critères de réussite**, et se valide quand
les critères sont tenus **sans aide** sur deux productions différentes. Les durées sont indicatives (1 à 2
séances de 30-45 min par étape, en appliquant sur un vrai livrable entre deux séances).

Diagnostic de départ : demander à l'utilisateur de décrire (ou coller en version masquée) **le dernier
visuel ou support chiffré qu'il a présenté**, et ce qu'il voulait que l'audience fasse. Appliquer la grille de
`checklist-critique.md` et en déduire le point de départ.

## Étape 0 : état des lieux
- **Livrable** : critique d'un support existant (le sien ou un exemple) avec la grille.
- **Réussite** : repère les défauts par leçon ; distingue « décrire » et « affirmer » dans un titre.

## Étape 1 : cadrer (leçon 1)
- **Livrable** : pour son prochain point d'avancement, qui / quoi / comment, **idée directrice en une phrase**,
  histoire en 3 minutes, storyboard sur papier.
- **Réussite** : dit son idée en 10 secondes sans support ; identifie le décideur ; formule la demande.
- **Piège** : l'idée est un sujet (« l'avancement de la recette »), pas une phrase avec un point de vue.

## Étape 2 : choisir le visuel (leçon 2)
- **Livrable** : pour 3 questions de recette (avancement, répartition des anomalies, évolution du stock),
  choisir et justifier le visuel ; refaire un de ses graphiques.
- **Réussite** : justifie chaque choix par la question du lecteur ; propose une alternative au camembert.

## Étape 3 : désencombrer (leçon 3)
- **Livrable** : un graphique de sa mission passé par les six gestes de désencombrement, avant/après.
- **Réussite** : plus de légende (étiquettes directes), plus de bordure ni de quadrillage, couleurs cohérentes.
- Outil : `scripts/avant_apres.py` comme modèle.

## Étape 4 : attirer l'attention et concevoir (leçons 4 et 5)
- **Livrable** : le même graphique avec **un** accent, un **titre d'action**, une hiérarchie claire, vérifié
  en simulation daltonienne.
- **Réussite** : un lecteur extérieur dit la conclusion en 10 secondes ; le titre énonce la conclusion.

## Étape 5 : raconter (leçon 6)
- **Livrable** : support de COPIL de 3 à 5 slides : titres d'abord, lecture horizontale, recommandation en tête,
  annexe pour le détail ; storyboard inversé d'un ancien support.
- **Réussite** : la lecture des titres seule raconte l'histoire ; la décision attendue est explicite.

## Étape 6 : pratiquer et diffuser (chapitres 9 et 10)
- **Livrable** : remplacer progressivement un reporting récurrent (rapport existant en annexe + 2 slides
  d'histoire devant) ; faire relire ; collecter un retour du décideur.
- **Réussite** : un retour concret de l'audience ; un modèle réutilisable pour la prochaine fois.

## Rythme d'une séance
1. 5 min : retrouver sans regarder 2 réflexes de la séance précédente.
2. 20-30 min : une leçon, appliquée à un livrable réel (ou fictif si confidentiel).
3. 5 min : bilan franc (acquis, fragile, à refaire) et **un exercice à faire avant la prochaine fois**.

## Trame de `mission/progression-dataviz.md`

```markdown
# Progression Storytelling avec les données

- Étape actuelle : N
- Dernière séance : AAAA-MM-JJ
- Audience principale en mission : (COPIL, métier, MOE…) — outil : (Excel, PowerPoint, Power BI…)

## Leçons
| Leçon | Statut | Dernière vue | Remarque |
|---|---|---|---|
| 1 Contexte / idée directrice | fragile | AAAA-MM-JJ | l'idée est un sujet, pas une phrase |
| 2 Choix du visuel | à voir | | |
| 3 Désencombrer | | | |
| 4 Attention / couleur | | | |
| 5 Design / titres d'action | | | |
| 6 Récit | | | |

Statuts : à voir · en cours · fragile · acquis (acquis = réussi sans aide sur deux productions différentes).

## Journal des séances
- AAAA-MM-JJ — sujet — livrable — verdict — **à faire avant la prochaine fois** : ...

## Erreurs récurrentes
- ...

## Supports réels retravaillés (sans donnée sensible)
- AAAA-MM-JJ — nature du support — avant/après — retour de l'audience
```

Règle : ne gonfle pas un statut pour encourager ; le suivi sert à décider quoi retravailler.
