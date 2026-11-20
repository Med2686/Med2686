# Trame du suivi de progression : `mission/progression-sql.md`

Le skill lit ce fichier en début de séance et le met à jour à la fin. Si le fichier n'existe pas, propose de
le créer avec cette trame. Dates AAAA-MM-JJ. Rien de confidentiel client dedans (pas de vraies données).

```markdown
# Progression SQL

- Moteur de la mission : (Oracle / SQL Server / PostgreSQL / MySQL / inconnu)
- Accès à la base réelle : (aucun / lecture seule recette / autre) — environnement : ...
- Niveau actuel (parcours.md) : N
- Dernière séance : AAAA-MM-JJ

## Notions
| Notion | Statut | Dernière vue | Remarque |
|---|---|---|---|
| SELECT / WHERE | acquis | AAAA-MM-JJ | |
| GROUP BY / HAVING | fragile | AAAA-MM-JJ | confond WHERE et HAVING |
| LEFT JOIN anti-join | à revoir | AAAA-MM-JJ | filtre mis dans le WHERE |

Statuts : à voir · en cours · fragile · acquis (acquis = réussi sans indice, deux séances différentes).

## Journal des séances
- AAAA-MM-JJ — sujet — exercices faits (n°) — verdict — **exercice à faire seul** : ...

## Erreurs récurrentes
- ...

## Cas réels de mission traités
- AAAA-MM-JJ — contrôle réalisé (sans donnée réelle) — requête gardée dans : ...
```

Règles de mise à jour : ne marque « acquis » qu'après une réussite sans indice dans **deux séances
différentes** ; rétrograde une notion en « fragile » si l'erreur revient. Ne gonfle pas le statut pour
encourager : le suivi sert à décider quoi retravailler.
