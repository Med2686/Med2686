# Application du storytelling aux livrables d'un BA / testeur

Pour chaque situation : **la question que le lecteur se pose**, **le visuel conseillé**, **le titre d'action
type**, **les pièges**. Les chiffres de l'exemple viennent du bac à sable fictif (`maitre-sql`).

## 1. Avancement de la recette (par campagne ou environnement)

- **Question du lecteur** : « Est-ce qu'on sera prêts pour le jalon ? » (pas « combien de cas OK »).
- **Visuel** : barres horizontales empilées à 100 % par campagne (une barre = tous les cas), **un seul accent**
  sur le segment problématique (cas non exécutés ou KO), les autres en gris. Étiquettes directes, pas de légende.
- **Titre d'action** : « En PREPROD, 6 cas sur 15 ne sont pas encore exécutés ».
- **Pièges** : barres empilées en valeurs absolues avec couleurs par défaut ; dénominateur flou (cas prévus ?
  cas exécutés ?) ; pourcentages à 3 décimales ; légende éloignée.
- **Démo** : `scripts/avant_apres.py` (images `assets/avant.png` et `assets/apres.png`).

## 2. Go / No-Go

- **Question** : « Peut-on mettre en production ? Sinon, qu'est-ce qui bloque et qui le débloque ? »
- **Format** : une slide de décision, pas un graphique : la **recommandation en titre** (GO, NO GO, GO avec
  réserves), 2 ou 3 raisons chiffrées, la **liste courte des bloquants** (anomalie, responsable, date cible),
  la décision demandée et à qui.
- **Visuel** : texte simple pour les chiffres clés (ex. « 2 anomalies bloquantes ouvertes »), tableau très
  allégé pour les bloquants, éventuellement un indicateur par campagne.
- **Titre** : « Recommandation : NO GO tant que les 2 anomalies bloquantes de REC2 ne sont pas corrigées ».
- **Pièges** : mur de graphiques sans recommandation ; feu tricolore rouge/vert seul (daltonisme, pas de
  nuance) ; masquer l'incertitude (dire ce qui n'est pas exécuté).

## 3. Anomalies par sévérité / par statut

- **Question** : « Où est le risque, et ça se résorbe ou ça s'aggrave ? »
- **Visuel** : barres horizontales triées (sévérité ou statut), **ouvertes en accent, fermées en gris** ; pour
  l'évolution dans le temps, une **courbe** du stock d'anomalies ouvertes (pas de barres empilées par jour).
- **Titre** : « 8 anomalies bloquantes ont été déclarées, 2 restent ouvertes, toutes en REC2 ».
- **Pièges** : camembert à 3 parts ; confondre anomalies déclarées et anomalies ouvertes ; moyenne de délai sans
  dire qu'elle ne couvre que les anomalies clôturées.

## 4. Délai de traitement des anomalies

- **Visuel** : barres horizontales (délai moyen par sévérité) avec le **nombre d'anomalies à côté** de chaque
  barre ; ou nuage de points / diagramme de dispersion si la répartition compte plus que la moyenne.
- **Piège** : une moyenne cache les extrêmes ; sur de petits effectifs (1 anomalie mineure), ne pas
  présenter une moyenne comme une tendance.

## 5. Couverture des exigences

- **Question** : « A-t-on testé ce qui compte ? »
- **Visuel** : **tableau-carte de chaleur** (exigences en lignes, résultat en couleur) ou simple liste des
  exigences **Must** non couvertes ; les trous en accent.
- **Titre** : « 3 exigences ne sont couvertes par aucun cas de test, dont 2 de priorité Must ».

## 6. Tendance de qualité d'une version à l'autre

- **Visuel** : **slopegraph** (avant/après par sous-système) ou courbe sur plusieurs versions ; une courbe mise
  en évidence, les autres grisées. Évite le « graphique spaghetti » (chapitre 9).
- **Titre** : « Le taux de KO a baissé dans 4 modules sur 5 entre R1 et R2 ; le module Paiement empire ».

## 7. Réponse à une question ponctuelle (mail ou compte rendu)

- **Format** : la conclusion en première phrase, puis 2 ou 3 chiffres, puis la demande ou la prochaine étape.
  Joindre le détail en pièce séparée, pas dans le corps du mail.
- **Exemple** : « Je recommande de décaler la MEP d'une semaine : 6 cas sur 15 restent à exécuter en PREPROD
  et 2 anomalies bloquantes sont ouvertes. Peux-tu valider la nouvelle date avant jeudi ? »

---

## Modèles à remplir

### Idée directrice (une phrase complète)
> « D'après [analyse], je recommande de [action] parce que [enjeu]. »

Test : contient un point de vue ? l'enjeu ? est-ce une phrase complète ? Peut-on la dire en 10 secondes ?

### Histoire en 3 minutes (cinq phrases à écrire à la main)
1. Contexte : pourquoi on est là.
2. Ce qui change ou ce qui inquiète.
3. Ce que montrent les données (2 chiffres maximum).
4. Ce qu'on recommande.
5. Ce que j'attends de l'audience, et pour quand.

### Storyboard de COPIL (sur papier, un carré = une slide)
| # | Titre d'action (la conclusion) | Preuve (visuel ou texte) | Décision attendue |
|---|---|---|---|
| 1 | Recommandation et ce que j'attends de vous | Texte simple | Oui |
| 2 | … | … | |
| N | Annexe : détails | Tableaux | Non |

Lecture horizontale : si on ne lit que la colonne « titre », l'histoire tient-elle ?

## Avant d'envoyer ou de présenter

- Le message tient-il en une phrase, en première position ?
- Le chiffre a-t-il été **vérifié** (nombre de lignes, jointure sans fan-out, dénominateur dit) ?
- Y a-t-il **une** chose en couleur ?
- Quelqu'un qui n'est pas du projet a-t-il compris en 10 secondes ?
