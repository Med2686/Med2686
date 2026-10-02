# Journal de mission — trame et règles

**Emplacement par défaut** : `mission/journal-de-mission.md` à la racine du répertoire de travail.
Un journal par mission. Le rappel automatique de début de session lit ce fichier : garder les **dates au
format AAAA-MM-JJ** et les tableaux ci-dessous tels quels.

## Règles de mise à jour

- Après chaque échange utile : ajouter décisions, actions, risques, réunions ; changer les statuts.
- Une action = un verbe + un résultat, **un porteur unique**, une échéance.
- Statuts d'action : `À faire`, `En cours`, `Fait`, `Abandonné`. Ne pas supprimer une ligne : changer son
  statut (historique).
- Section « Journal de bord » : 1 à 3 lignes datées, les plus récentes en haut.
- Pas de données personnelles de clients finaux, pas d'informations confidentielles inutiles.

## Trame

```markdown
# Journal de mission — [Client] / [Projet]

## Contexte
- Client / secteur : [à compléter]
- Projet (1 phrase) : [à compléter]
- Méthode : [Agile / Cycle en V / hybride]
- Mon rôle : [BA / AMOA / testeur] — rattaché à : [nom, rôle]
- Début de mission : [AAAA-MM-JJ] — fin prévue : [AAAA-MM-JJ]
- Phase actuelle : [cadrage / recueil / spéc / préparation recette / recette / MEP / après MEP]
- Prochain jalon : [jalon] — [AAAA-MM-JJ]

## Acteurs
| Nom | Rôle | Attentes / points d'attention | Canal préféré |
|---|---|---|---|

## Glossaire et applications
| Terme / appli | Signification |
|---|---|

## Actions
| ID | Action | Porteur | Échéance | Statut |
|---|---|---|---|---|
| A1 | [verbe + résultat] | [nom] | [AAAA-MM-JJ] | À faire |

## Prochaines réunions
| Date | Réunion | Objectif | Mon rôle | Préparation à faire |
|---|---|---|---|---|

## Décisions
| Date | Décision | Décideur | Source (CR, mail) |
|---|---|---|---|

## Risques et problèmes
| ID | Risque (si… alors… ce qui…) | Score | Plan d'action | Porteur | Statut |
|---|---|---|---|---|---|

## Points ouverts
| ID | Question | À qui | Depuis | Statut |
|---|---|---|---|---|

## Journal de bord
- [AAAA-MM-JJ] : [ce qui s'est passé d'important, 1-3 lignes]

## Apprentissages (pour le dossier de compétences)
- [réalisation au format STAR, résultat chiffré]
```
