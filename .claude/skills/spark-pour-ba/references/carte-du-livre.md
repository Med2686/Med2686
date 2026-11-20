# Carte du livre *Spark: The Definitive Guide* pour un BA / testeur

**Fiche d'identité.** 1ʳᵉ édition (2018), centrée sur **Spark 2.x** et ses API structurées (DataFrame, SQL,
Dataset, Structured Streaming). Auteurs : Bill Chambers (Databricks) et Matei Zaharia (créateur du projet).
Public visé par les auteurs : **data scientists et data engineers**, pas les BA. Exemples en Scala et en Python.
33 chapitres en 7 parties, ~1 100 000 caractères (un très gros livre).

**Avis franc sur la pertinence pour toi.**
- Le livre est **excellent pour comprendre comment Spark pense**, mais **trop profond pour ton poste** si on le
  lit en entier. Ton objectif réaliste est de **dialoguer avec les data engineers, lire et écrire du Spark SQL,
  concevoir des tests de données et diagnostiquer un résultat faux**, pas de devenir développeur Spark.
- **Priorité de lecture : environ 30 % du livre.** Le reste peut attendre ou être ignoré.
- **Prérequis honnête** : sans SQL solide (niveau 3 de `maitre-sql`), le livre sera un mur. Commence par le SQL.
- **Âge du contenu** : écrit pour Spark 2. Spark 3 (exécution adaptative, etc.) et Spark 4 ont changé des
  comportements ; les concepts restent valables, les détails de configuration beaucoup moins. Vérifie la version
  du client avant d'affirmer quoi que ce soit.

## Priorités par chapitre

### À lire en priorité (le noyau pour ton métier)
| Chap. | Titre | Pourquoi |
|---|---|---|
| 1 | What Is Apache Spark? | La philosophie (moteur unifié), le contexte, le « pourquoi » |
| 2 | A Gentle Introduction to Spark | **Le chapitre fondamental** : architecture, partitions, transformations/actions, paresse, DataFrames et SQL |
| 4 | Structured API Overview | Schéma, types, **plans logique et physique**, optimiseur |
| 5 | Basic Structured Operations | Colonnes, sélection, filtre, tri, `NULL` : le « SELECT/WHERE » de Spark |
| 7 | Aggregations | Comptages, regroupements : le « GROUP BY » de Spark |
| 8 | Joins | **Types de jointures (dont SEMI et ANTI), shuffle vs broadcast** |
| 9 | Data Sources | **Formats, modes de lecture/écriture, partitionnement, petits fichiers** |
| 10 | Spark SQL | Tables, vues, catalogue, SQL : ton terrain principal |
| 15 | How Spark Runs on a Cluster | Du code à l'exécution, modes, cycle de vie d'une application |
| 18 | Monitoring and Debugging | **Spark UI, symptômes et remèdes (NULL inattendus, lenteurs, mémoire)** |
| 19 | Performance Tuning | Lire les choix de conception (formats, jointures, partitions) sans devenir optimiseur |

### À survoler (une lecture de repérage suffit)
| Chap. | Titre | Ce qu'il faut en retenir |
|---|---|---|
| 3 | A Tour of Spark's Toolset | Panorama des outils (production, streaming, ML) |
| 6 | Working with Different Types of Data | Chaînes, dates, **`NULL`** (`coalesce`, `ifnull`, `nvl`, `fill`, `drop`), types complexes |
| 11 | Datasets | Surtout Scala/Java ; sauter si tu es en Python/SQL |
| 16, 17 | Developing / Deploying Spark Applications | Comprendre comment un job arrive en production (`spark-submit`) |
| 20 à 23 | Streaming | Seulement les **idées** : event time vs processing time, micro-batch, watermarks, tolérance aux pannes |
| 32, 33 | PySpark, Ecosystem | Si ton équipe est en Python ; sinon repérage |

### À ignorer pour l'instant
| Chap. | Titre | Raison |
|---|---|---|
| 12 à 14 | RDDs, RDDs avancés, variables partagées | API de bas niveau, hors de ton rôle |
| 24 à 31 | Analytique avancée et ML, classification, régression, recommandation, non supervisé, graphes, deep learning | Lire **seulement le début du chapitre 24** pour savoir ce qui existe |

## Ce qui a changé depuis 2018 (à confirmer sur la version du client)

- **Spark 3** : exécution **adaptative** (AQE, observée dans les plans de notre laboratoire en 3.5),
  optimisations de jointures et de partitions dynamiques, davantage de fonctions SQL (par exemple `try_divide`).
- **Spark 4** : à ma connaissance, mode **ANSI par défaut** (la division par zéro et les conversions ratées
  produisent des erreurs et non des `NULL`) ; à confirmer dans la documentation officielle.
- **Formats de table** transactionnels (Delta, Iceberg, Hudi) : **absents du livre**, ils apportent
  `UPDATE`/`DELETE`/`MERGE` et la gestion de versions ; très répandus aujourd'hui.
- **Plateformes managées** (Databricks, services cloud) : le cluster est souvent invisible pour l'utilisateur.

## Ordre de lecture conseillé (un tiers du livre)

1 → 2 → 4 → 10 → 5 → 7 → 8 → 9 → 18 → 19 → 15, avec le laboratoire sous la main (`scripts/spark_lab.py`),
en exécutant chaque exemple sur la base de recette fictive plutôt que sur les données du livre.
