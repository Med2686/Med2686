# Questions à poser aux data engineers (Spark) : à emporter en réunion

Pour un BA/testeur, la valeur n'est pas de répondre à ces questions mais de **savoir les poser** et de comprendre
la réponse. Classées par moment du projet. Les termes sont expliqués dans `concepts.md`.

## À l'ouverture d'un chantier
1. Quelle **plateforme** (Spark autogéré, Databricks, service cloud) et quelle **version** de Spark ?
2. Quel **format de table** (Parquet, Delta, Iceberg, CSV) ? Peut-on faire `UPDATE`/`DELETE` ou seulement ajouter ?
3. Quels **environnements** de recette existent, avec quels **volumes** par rapport à la production ?
4. Qui fournit les **données de test**, sont-elles **masquées** (RGPD, secret bancaire) ?
5. Ai-je un accès **lecture seule** à une session SQL ou à un notebook ? Sur quel cluster, à quels horaires ?

## Sur les données entrantes
6. Quel est le **mode de lecture** (permissif, rejet silencieux, échec immédiat) ? Où vont les lignes corrompues ?
7. Le **schéma** est-il imposé ou deviné ? Que se passe-t-il quand le fournisseur ajoute ou renomme une colonne ?
8. Comment sont gérés les **`NULL`**, les valeurs vides, les doublons à la source ?

## Sur les traitements
9. Le job est-il **idempotent** ? Que se passe-t-il si on le **relance** après un échec (doublons ? écrasement ?) ?
10. Quel **mode d'écriture** (ajout, écrasement) ? Quelles **clés de partitionnement** ?
11. Y a-t-il des **UDF** (fonctions personnalisées) ? Où sont-elles testées ?
12. La division par zéro et les conversions ratées produisent-elles une **erreur ou un `NULL`** (mode ANSI) ?
13. Comment sont gérés les **fuseaux horaires** et les dates (heure locale, UTC) ?

## Sur la qualité et le contrôle
14. Quels **contrôles de volumétrie** existent entre source et cible ? Quelle tolérance ?
15. Existe-t-il une **table de rejets** ? Qui la lit, à quelle fréquence ?
16. Quel **historique** de `NULL` et de volumes par jour est conservé pour détecter une dérive ?

## Sur la performance et l'exploitation
17. Quel est le **SLA** (heure de fin attendue) ? Que se passe-t-il s'il est dépassé ?
18. Y a-t-il des **déséquilibres connus** (clé très dominante) ? Une jointure **diffusée** (broadcast) est-elle utilisée ?
19. Combien de **petits fichiers** produit-on par jour ? Existe-t-il une **compaction** ?
20. Où voit-on les jobs (Spark UI, History Server, outil de supervision) ? Peut-on me donner l'accès ?

## Pour les flux (streaming)
21. Que se passe-t-il pour les **événements en retard** ou **désordonnés** ? Quel **watermark** ?
22. Comment teste-t-on la **reprise après panne** (aucune perte, aucun doublon) ?

## Conseil de posture
Pose ces questions pour **comprendre**, pas pour piéger. Note les réponses dans la stratégie de test, et
relance sur les « on verra » : un risque non nommé reste un risque.
