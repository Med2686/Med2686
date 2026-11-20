# Parcours SQL du BA / testeur : 6 niveaux

Chaque niveau a un **objectif de mission**, des **critères de réussite** (« sait faire sans aide ») et des
exercices. On passe au niveau suivant quand les critères sont tenus **sans indice**, pas quand le cours est
« vu ». Les durées sont **indicatives** (mon estimation pour quelqu'un qui pratique 2-3 séances de 30-45 min
par semaine) ; des feuilles de route publiques proposent ~8 semaines pour un débutant complet, sans étude
qui le démontre : l'essentiel est la régularité, pas le calendrier.

Diagnostic de départ : lui demander ce qu'il fait déjà seul (SELECT ? jointure ? GROUP BY ?) et lui donner
**un exercice d'étalonnage** du niveau qu'il pense avoir. S'il échoue, redescends d'un niveau sans en faire
un drame.

## Niveau 0 : comprendre une base (1 séance)

- **Mission** : lire un schéma remis par la MOE sans se perdre.
- **Notions** : table, ligne, colonne, clé primaire, clé étrangère, **grain** (une ligne = quoi ?),
  cardinalité 1-n, référentiel vs transaction.
- **Réussite** : devant `bac-a-sable.md`, dit en une phrase le grain de chaque table et dessine à main
  levée les relations ; explique pourquoi `transactions` a beaucoup plus de lignes que `clients`.

## Niveau 1 : lire et filtrer (2-3 séances)

- **Mission** : « donne-moi la liste des anomalies bloquantes ouvertes ».
- **Notions** : `SELECT`, `WHERE` (`=`, `<>`, `IN`, `BETWEEN`, `LIKE`, `AND/OR/NOT` et parenthèses),
  `ORDER BY`, `LIMIT`, `DISTINCT`, alias, `NULL` (`IS NULL`).
- **Réussite** : écrit 5 requêtes de filtre sans aide en moins de 15 min ; explique pourquoi
  `= NULL` ne marche pas ; sait faire un `COUNT(*)` avant d'afficher un gros résultat.
- **Exercices** : 1 à 3. **Pièges** : n°6, 11.

## Niveau 2 : agréger (2-3 séances)

- **Mission** : « combien de cas KO par campagne ? »
- **Notions** : `COUNT`, `SUM`, `AVG`, `MIN`, `MAX`, `GROUP BY`, `HAVING`, `CASE WHEN` dans un agrégat,
  ordre logique d'exécution.
- **Réussite** : produit un tableau d'avancement de recette ; explique la différence `WHERE` / `HAVING` ;
  calcule un pourcentage sans division entière.
- **Exercices** : 4 à 7. **Pièges** : n°7, 8, 9.

## Niveau 3 : relier les tables (3-4 séances) : le vrai cap

- **Mission** : « pour chaque exigence Must, les cas en échec avec le nom de la campagne ».
- **Notions** : `INNER JOIN`, `LEFT JOIN`, jointure sur plusieurs tables, alias, `ON` vs `WHERE`, anti-join
  (`LEFT JOIN ... IS NULL`), grain et fan-out.
- **Réussite** : dit **avant d'exécuter** si une jointure peut perdre ou multiplier des lignes ; écrit un
  anti-join sans aide ; choisit `LEFT` vs `INNER` en justifiant par le besoin.
- **Exercices** : 8 à 10. **Pièges** : n°2, 3, 4, 5, 1.
- **Honnêteté** : c'est ici que la plupart décrochent. Ne passe pas au niveau 4 sans avoir validé ce
  niveau ; un BA qui comprend mal les jointures produira des chiffres faux avec aplomb.

## Niveau 4 : enquêter sur la donnée (3-4 séances) : l'utilité maximale en mission

- **Mission** : prouver un écart avec des chiffres avant d'ouvrir une anomalie.
- **Notions** : doublons, orphelins, réconciliation de compteurs et de montants (avec tolérance),
  différence d'ensembles dans les deux sens, couverture, sous-requêtes (`IN`, `EXISTS`), contrôle qui ne
  renvoie que les anomalies.
- **Réussite** : face à une règle de gestion en français, écrit la requête de contrôle, la teste sur un cas
  connu, et rédige la fiche d'anomalie avec requête, environnement, date d'extraction et résultat.
- **Exercices** : 11 à 16 (scénarios 1 à 5 et 10).

## Niveau 5 : analyser (3-5 séances)

- **Mission** : produire des indicateurs de pilotage (Go/No-Go, délais, tendances).
- **Notions** : `CASE`, dates (selon dialecte), sous-requêtes corrélées, **CTE** (`WITH`), fonctions de
  fenêtre (`ROW_NUMBER`, `RANK`, `LAG`, `SUM() OVER`), top-N par groupe, `UNION`.
- **Réussite** : décompose une question complexe en CTE nommées lisibles ; sait pourquoi une fenêtre ne se
  filtre pas dans le `WHERE` ; relit sa requête et en détecte un défaut.
- **Exercices** : 17 à 22 et les défis finaux. **Pièges** : n°10, 12.

## Niveau 6 : pratique professionnelle (continu)

- **Mission** : être crédible face à la MOE et aux DBA.
- **Notions** : lire une requête de la MOE (mode Lecture), adapter au dialecte du client
  (`dialectes.md`), documenter ses requêtes dans les fiches d'anomalie, utiliser les **vues** fournies,
  notion de coût (volume, filtre, heure), lecture seule et données sensibles, comprendre ce qu'est un plan
  d'exécution sans l'optimiser.
- **Réussite** : sait dire « cette requête fait un produit cartésien, voici pourquoi » ; sait refuser
  d'exécuter une requête lourde sur un environnement partagé et proposer une alternative.

## Rythme conseillé d'une séance (30-45 min)

1. 5 min : rappel d'une notion de la séance précédente (retrouver, sans regarder).
2. 20-30 min : un nouveau concept, 1 à 3 exercices sur scénario métier.
3. 5 min : bilan franc (juste / fragile / à revoir) et **un exercice à faire seul** avant la prochaine fois.
