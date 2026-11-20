# Les pièges de données Spark qu'un BA / testeur doit connaître

Colonne « Vérifié » : **oui** = reproduit ici dans Spark 3.5 en mode local (`scripts/pieges_demo.py` ou
`scripts/test_spark_blocks.py`) ; **livre** = décrit dans le livre (Spark 2.x) et non retesté ; **à vérifier** =
mon avis ou une connaissance à confirmer sur la version du client.

| # | Piège | Ce que fait Spark | Conséquence en recette | Parade | Vérifié |
|---|---|---|---|---|---|
| 1 | **Ligne corrompue en lecture** | En mode par défaut (`PERMISSIVE`), la valeur devient `NULL` **sans erreur** ; en `DROPMALFORMED`, la ligne disparaît silencieusement | Un fichier de 3 lignes dont 1 corrompue « charge bien » | Comparer les **volumes** source/cible ; demander le mode de lecture et la colonne `_corrupt_record` | oui |
| 2 | **Division par zéro et conversion ratée** | `1/0` → `NULL` ; `CAST('abc' AS INT)` → `NULL` ; `5 * ' '` → `NULL` (ANSI désactivé par défaut en 3.5) | Un taux ou un montant disparaît d'un rapport sans alerte | Chercher les `NULL` inattendus ; demander si le mode ANSI est activé | oui |
| 3 | **Conversion implicite de texte** | `5 * '23'` donne `115` (texte converti en nombre) | Un résultat « plausible » issu d'un mauvais typage | Vérifier le schéma (`printSchema`) et les `CAST` du plan | oui |
| 4 | **`inferSchema` qui change de type** | Une seule valeur `abc` suffit à faire deviner une colonne texte au lieu d'entier | Les contrôles numériques en aval changent de comportement sans erreur | Imposer un schéma explicite ; comparer les types entre deux livraisons | oui |
| 5 | **Format de données qui change** | Les traitements continuent, mais des colonnes passent à `NULL` | « Ça marchait hier » et les chiffres sont faux | Tests de contrat de schéma ; comptage de `NULL` par colonne avant/après | livre (chap. 18) |
| 6 | **`NOT IN` avec un `NULL`** | Ne renvoie aucune ligne | Un contrôle d'orphelins dit « aucun » à tort | `LEFT ANTI JOIN` ou `NOT EXISTS` | oui |
| 7 | **`NULL = NULL`** | Résultat inconnu (pas vrai) ; `<=>` est l'égalité « NULL-safe » | Des jointures sur clé nullable perdent des lignes | `<=>` ou traiter les `NULL` explicitement | oui |
| 8 | **Pas d'ordre garanti sans `ORDER BY`** | L'ordre des lignes dépend du partitionnement | Un résultat qui change d'une exécution à l'autre | Toujours trier avant de comparer ou de présenter | livre/à vérifier |
| 9 | **`append` + rejeu** | Les lignes sont ajoutées une 2ᵉ fois | **Doublons** après la reprise d'un job en échec | Demander si le traitement est **idempotent** ; contrôle de doublons après rejeu | livre (modes d'écriture) |
| 10 | **Paresse** | Une erreur n'apparaît qu'à l'action ; chaque action relance le calcul | Un test « vert » alors que la donnée fautive n'a pas été lue | Forcer une action dans le test (compter/écrire) | oui |
| 11 | **Rapatrier de gros volumes sur le driver** (`collect`, `toPandas`) | Le driver peut manquer de mémoire | Job qui s'arrête sur de gros jeux de données | Agréger ou échantillonner avant ; ne pas « tout afficher » | livre (chap. 18) |
| 12 | **Déséquilibre de clé (skew)** | Une tâche est bien plus lente que les autres | Job qui « traîne » en fin d'exécution | Repérer les tâches lentes dans la Spark UI ; en parler au data engineer | livre (chap. 18) |
| 13 | **Petits fichiers** | Lecture lente, surcharge de métadonnées | Lenteur inexpliquée après de nombreuses petites livraisons | Demander la taille moyenne des fichiers et le plan de compaction | livre (chap. 9) |
| 14 | **Affichage tronqué** (`show()` sans option) | 20 lignes seulement, libellés coupés avec « ... », et une simple mention « only showing top 20 rows » en pied | On croit avoir tout vu | Demander `show(n, truncate=False)` ou une requête filtrée et un `count()` | oui |
| 15 | **Fuseaux horaires et dates** | Les conversions dépendent de la configuration de session | Une transaction « de minuit » change de jour | Demander le fuseau de session et le type de date | à vérifier |

## Les cinq contrôles à systématiser sur une chaîne Spark

1. **Volumes** : comptages source vs cible, par jour et par statut.
2. **Doublons** après rejeu et sur la clé métier.
3. **`NULL` par colonne**, avant et après chaque étape.
4. **Types** : le schéma de sortie est celui attendu (jamais deviné).
5. **Rejets** : où vont les lignes corrompues ? Combien ? Qui les voit ?
