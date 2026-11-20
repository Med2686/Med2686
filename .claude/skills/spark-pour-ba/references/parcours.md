# Parcours Spark pour BA / testeur : 6 étapes

**Prérequis honnête.** Ne commence pas Spark avant d'avoir **le niveau 3 de `maitre-sql`** (jointures, agrégats)
validé. Spark SQL, c'est du SQL : sans lui, le livre sera un mur et tu y perdras du temps. Autre prérequis :
savoir si ton client **utilise réellement Spark** (voir `questions-data-engineers.md`, questions 1 à 3). Si non,
ce parcours est une culture générale utile, pas une priorité.

Chaque étape a un **livrable**, des **critères de réussite** et un **exercice dans le laboratoire** (`scripts/spark_lab.py`,
base de recette fictive). On valide quand les critères sont tenus **sans aide** sur deux exercices différents.
Durées indicatives : 1 à 3 séances de 30-45 min par étape.

Installation du laboratoire (une fois) : Java 8, 11 ou 17, puis `pip install pyspark`, puis
`python3 .claude/skills/spark-pour-ba/scripts/spark_lab.py`.

## S0 : pourquoi et comment Spark pense (chapitres 1 et 2)
- **Livrable** : expliquer en 5 phrases à un collègue : cluster, driver, executor, partition, transformation vs action.
- **Réussite** : sans notes, explique pourquoi « une erreur apparaît à l'action » (paresse) et pourquoi
  un `count()` relance le calcul ; dessine l'architecture d'une application.
- **Exercice** : dans le laboratoire, construire une transformation (`where`, `groupBy`) puis mesurer ce qui se passe
  avant et après l'action (`scripts/pieges_demo.py`, piège 4).

## S1 : DataFrames et Spark SQL (chapitres 4, 5, 10)
- **Livrable** : réécrire en Spark SQL 5 requêtes du bac à sable (`spark-sql-ba.md`) et les exécuter.
- **Réussite** : sait ce qu'est un schéma, une vue temporaire, le catalogue ; lit un `printSchema`.
- **Exercice** : traduire les exercices N2-2 et N2-4 de SQL Quest en Spark SQL.

## S2 : agrégations et jointures (chapitres 7 et 8)
- **Livrable** : trois contrôles de qualité en Spark SQL (orphelins, doublons, couverture) dont deux avec `LEFT ANTI JOIN`.
- **Réussite** : explique SEMI vs ANTI vs INNER vs LEFT, et **shuffle join vs broadcast join** ; repère un
  `Exchange` et un `BroadcastHashJoin` dans un `EXPLAIN`.
- **Exercice** : écrire la requête de réconciliation de batch, puis lire son plan.

## S3 : données et formats (chapitres 9 et 6)
- **Livrable** : fiche « ce que je contrôle à l'ingestion » : modes de lecture, schéma imposé ou deviné,
  `NULL`, doublons après rejeu, volumes source/cible.
- **Réussite** : prédit ce que Spark fait d'une ligne corrompue dans chaque mode ; distingue CSV et Parquet ;
  explique le problème des petits fichiers.
- **Exercice** : rejouer `scripts/pieges_demo.py` (pièges 1 à 4) et écrire, pour chacun, le test qui l'aurait détecté.

## S4 : exécution et diagnostic (chapitres 15, 18, 19)
- **Livrable** : une **stratégie de test de chaîne Spark** d'une page : volumes, doublons, `NULL`, types, rejets,
  rejeu, SLA, avec les questions de `questions-data-engineers.md` posées au data engineer.
- **Réussite** : face à « le job est lent » ou « il y a des `NULL` », sait lister les 3 premières hypothèses
  (skew, petits fichiers, format changé, conversion ratée) et quoi regarder dans la Spark UI.
- **Exercice** : étude de cas à partir de `pieges.md` : relier chaque symptôme à sa cause probable.

## S5 : flux et machine learning : culture seulement (chapitres 20 à 23, début du 24)
- **Livrable** : une page « ce que je teste différemment sur un flux » (événements tardifs, désordre, reprise
  après panne, doublons).
- **Réussite** : explique event time vs processing time et le watermark en 3 phrases ; sait qu'un modèle
  de ML a ses propres tests (jeu d'évaluation, dérive) sans prétendre les écrire.

## Rythme d'une séance
1. 5 min : retrouver sans regarder 2 notions de la séance précédente.
2. 20-30 min : un concept, un exercice **exécuté** dans le laboratoire (jamais « imaginé »).
3. 5 min : bilan franc et **un exercice à faire seul**.

## Trame de `mission/progression-spark.md`

```markdown
# Progression Spark pour BA

- Plateforme et version du client : (inconnues / Spark x.y / Databricks / autre)
- Format de table : (Parquet / Delta / Iceberg / inconnu) — accès lecture seule : (oui / non)
- Prérequis SQL (maitre-sql) : niveau N
- Étape actuelle : S0 — dernière séance : AAAA-MM-JJ

## Notions
| Notion | Statut | Dernière vue | Remarque |
|---|---|---|---|
| Paresse (transformation/action) | à voir | | |
| Partition, shuffle | | | |
| Jointures SEMI/ANTI, broadcast | | | |
| Modes de lecture, schéma | | | |
| Lire un plan (EXPLAIN) | | | |
| Spark UI | | | |

Statuts : à voir · en cours · fragile · acquis (acquis = réussi sans aide sur deux exercices différents).

## Journal des séances
- AAAA-MM-JJ — sujet — exercice exécuté — verdict — **à faire seul** : ...

## Questions posées aux data engineers et réponses
- AAAA-MM-JJ — question n° — réponse — impact sur la stratégie de test
```

Règle : ne gonfle jamais un statut pour encourager ; le suivi sert à décider quoi retravailler.
