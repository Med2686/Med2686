# Progression SQL

- Moteur de la mission : inconnu (à demander à la MOE)
- Accès à la base réelle : inconnu
- Niveau actuel (parcours.md du skill maitre-sql) : 0 (en cours)
- Dernière séance : 2026-11-20
- Outil d'entraînement : SQL Quest (https://claude.ai/artifact/HxDzVnWj3L1tzmZDnTaSnU, ou `sql-quest/index.html` en local)

## Notions
| Notion | Statut | Dernière vue | Remarque |
|---|---|---|---|
| Table, ligne, colonne, grain | en cours | 2026-11-20 | Lit correctement une ligne d'anomalie ; confond encore les trois tables quand il raisonne sur les titres plutôt que sur les clés |
| Clés primaire / étrangère | en cours | 2026-11-20 | A identifié `cas_test_id` comme colonne de liaison ; reste à nommer la table visée et à enchaîner anomalie → cas → exigence |
| SELECT / WHERE | à voir | | |
| GROUP BY / HAVING | à voir | | |
| JOIN / LEFT JOIN | à voir | | |

Statuts : à voir · en cours · fragile · acquis (acquis = réussi sans indice, deux séances différentes).

## Journal des séances
- 2026-11-20 — niveau 0 : lire une base, grain, clés — questions N0-1 à N0-3 en échange — départ « je ne me rappelle de rien » ; progression nette sur la lecture d'une ligne et l'idée de clé — **à faire seul** : exercices N0-1 à N0-4 dans SQL Quest, puis copier les réponses pour correction

## Erreurs récurrentes
- Raisonne sur le **contenu des titres** au lieu de suivre les clés entre tables
- Mélange la ligne d'une table avec la chaîne anomalie → cas de test → exigence

## Cas réels de mission traités
- (aucun pour l'instant)
