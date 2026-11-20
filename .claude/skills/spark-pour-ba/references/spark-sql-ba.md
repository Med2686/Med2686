# Spark SQL pour un BA / testeur : contrôles de données sur la base de recette

Les requêtes marquées `-- [spark]` sont **exécutées dans Spark 3.5 en mode local** contre la base fictive du
skill `maitre-sql` (`python3 scripts/test_spark_blocks.py`). `attendu: N` = nombre de lignes retournées.
Le livre présente Spark SQL comme un sous-ensemble du SQL ANSI (norme 2003) plus des extensions Hive : tout ce
que tu apprends avec `maitre-sql` s'applique ; ci-dessous, ce qui change ou s'ajoute.

Dans Spark, les tables sont des **vues temporaires** (créées par le laboratoire) ou des tables d'un catalogue
(souvent Hive/Delta/Iceberg en entreprise). Les dates de ce bac à sable sont des **textes** `AAAA-MM-JJ` : on les
convertit avec `to_date`.

---

## 1. Les jointures propres à Spark : `LEFT SEMI` et `LEFT ANTI`

Spark offre deux types de jointure qui n'existent pas dans tous les moteurs : **SEMI** (garde les lignes de
gauche qui ont une correspondance, sans dupliquer ni ramener les colonnes de droite) et **ANTI** (garde celles
qui n'en ont pas). Ce sont les formes les plus **sûres** pour « existe / n'existe pas » : pas de fan-out, pas
de piège `NOT IN`.

```sql
-- [spark] attendu: 3
-- Orphelins : comptes dont le client n'existe pas (ANTI)
SELECT cp.id, cp.client_id
FROM comptes cp
LEFT ANTI JOIN clients cl ON cl.id = cp.client_id
ORDER BY cp.id;
```

```sql
-- [spark] attendu: 60
-- Clients ayant au moins un compte (SEMI) : une ligne par client, même s'il a deux comptes
SELECT c.id
FROM clients c
LEFT SEMI JOIN comptes cp ON cp.client_id = c.id;
```

**Lecture.** Avec un `JOIN` ordinaire, un client à deux comptes apparaîtrait deux fois : c'est le fan-out. Avec
`SEMI`, jamais. Sur de gros volumes, `SEMI`/`ANTI` sont aussi souvent plus efficaces qu'un `JOIN` suivi d'un `DISTINCT`.

## 2. Contrôles de qualité (mêmes principes qu'en SQL classique)

```sql
-- [spark] attendu: 2
-- Doublons d'e-mail
SELECT email, COUNT(*) AS nb FROM clients GROUP BY email HAVING COUNT(*) > 1;
```

```sql
-- [spark] attendu: 3
-- Exigences sans cas de test
SELECT e.code, e.titre
FROM exigences e
LEFT ANTI JOIN cas_test ct ON ct.exigence_id = e.id;
```

```sql
-- [spark] attendu: 1
-- Cas KO ou Bloqué sans fiche d'anomalie
SELECT ct.id, ct.titre
FROM cas_test ct
LEFT ANTI JOIN anomalies a ON a.cas_test_id = ct.id
WHERE ct.resultat IN ('KO', 'Bloqué');
```

```sql
-- [spark] attendu: 2
-- Réconciliation d'un batch : compteur annoncé vs écritures réelles
SELECT b.id, b.statut, b.nb_ecrits AS annonce, COUNT(t.id) AS en_base
FROM batchs b
LEFT JOIN transactions t ON t.batch_id = b.id
GROUP BY b.id, b.statut, b.nb_ecrits
HAVING COUNT(t.id) <> b.nb_ecrits;
```

```sql
-- [spark] attendu: 3
-- Solde incohérent avec la somme des mouvements (tolérance sur les décimaux)
SELECT c.id, c.solde,
       ROUND(SUM(CASE WHEN t.sens = 'C' THEN t.montant ELSE -t.montant END), 2) AS calcule
FROM comptes c
JOIN transactions t ON t.compte_id = c.id
GROUP BY c.id, c.solde
HAVING ABS(c.solde - SUM(CASE WHEN t.sens = 'C' THEN t.montant ELSE -t.montant END)) > 0.005;
```

```sql
-- [spark] attendu: 4
-- Différence d'ensembles : clients actifs sans compte ouvert (EXCEPT)
SELECT id FROM clients WHERE statut = 'actif'
EXCEPT
SELECT client_id FROM comptes WHERE statut = 'ouvert';
```

**Lecture.** Réconciliation entre deux systèmes : en Spark, comparer un volume « source » et « cible » avec un
`COUNT` et un `SUM` par jour est le contrôle de base d'une chaîne ETL ; le faire **dans les deux sens** avec
`EXCEPT` détecte les lignes présentes d'un seul côté.

## 3. Analyse : CASE, dates, fenêtres

```sql
-- [spark] attendu: 3
-- Go / No-Go par campagne
SELECT ca.nom,
       CASE
         WHEN SUM(CASE WHEN a.severite = 'bloquante' AND a.statut IN ('ouverte','en correction') THEN 1 ELSE 0 END) > 0 THEN 'NO GO'
         WHEN SUM(CASE WHEN a.severite = 'majeure'   AND a.statut IN ('ouverte','en correction') THEN 1 ELSE 0 END) > 0 THEN 'RESERVES'
         ELSE 'GO'
       END AS decision
FROM campagnes ca
LEFT JOIN anomalies a ON a.campagne_id = ca.id
GROUP BY ca.id, ca.nom;
```

```sql
-- [spark] attendu: 3
-- Délai moyen de traitement : datediff(fin, début) en Spark (l'ordre des arguments est l'inverse de SQL Server)
SELECT severite,
       ROUND(AVG(datediff(to_date(date_cloture), to_date(date_creation))), 1) AS delai_moyen_jours
FROM anomalies
WHERE date_cloture IS NOT NULL
GROUP BY severite;
```

```sql
-- [spark] attendu: 4
-- Classement avec ex æquo (RANK)
SELECT assigne_a, COUNT(*) AS nb, RANK() OVER (ORDER BY COUNT(*) DESC) AS rang
FROM anomalies
GROUP BY assigne_a;
```

```sql
-- [spark] attendu: 2
-- Première anomalie ouverte par campagne (fenêtre dans une CTE)
WITH ouvertes AS (
  SELECT a.*, ROW_NUMBER() OVER (PARTITION BY campagne_id ORDER BY date_creation, id) AS rang
  FROM anomalies a WHERE statut = 'ouverte'
)
SELECT id, campagne_id FROM ouvertes WHERE rang = 1;
```

```sql
-- [spark] attendu: 2
-- Fonctions d'agrégation propres à Spark : regrouper les identifiants dans une liste
SELECT campagne_id, collect_list(id) AS anomalies_ouvertes
FROM anomalies WHERE statut = 'ouverte'
GROUP BY campagne_id;
```

## 4. Ce que Spark ajoute : le plan d'exécution et les indications

```sql
-- [spark] attendu: 3
-- Indication de diffusion : on demande à Spark de copier la petite table sur chaque machine (broadcast join)
SELECT /*+ BROADCAST(ca) */ ca.nom, COUNT(*) AS nb_cas
FROM cas_test ct
JOIN campagnes ca ON ca.id = ct.campagne_id
GROUP BY ca.nom;
```

Pour **voir comment** Spark va exécuter une requête (sans la lancer) : `EXPLAIN` (ou `EXPLAIN FORMATTED`).
Lis le plan **de bas en haut** : lecture des sources (`Scan`), filtres, échanges de données (`Exchange` =
**shuffle**, le mouvement coûteux entre machines), jointures (`SortMergeJoin` pour deux grosses tables,
`BroadcastHashJoin` quand l'une est petite), agrégats. Sous Spark 3, le plan commence par `AdaptiveSparkPlan` :
Spark ré-optimise **pendant** l'exécution (AQE), ce que le livre, écrit pour Spark 2, ne décrit pas.

```sql
-- [spark] attendu: 1
-- Division par zéro : sans le mode ANSI, Spark renvoie NULL SANS ERREUR (piège pour un contrôle de données)
SELECT 1 / 0 AS resultat_silencieux;
```

```sql
-- [spark] attendu: 1
-- Variante qui dit explicitement qu'on accepte NULL en cas de division impossible (Spark 3.2+)
SELECT try_divide(1, 0) AS resultat;
```

**Lecture.** Dans la configuration par défaut observée ici (Spark 3.5), `1/0` donne `NULL` et non une erreur : un
taux « calculé » peut donc disparaître silencieusement d'un rapport. À signaler au data engineer : le mode
**ANSI** (`spark.sql.ansi.enabled`) change ce comportement et, à ma connaissance, devient le défaut en Spark 4 (à
confirmer dans la documentation de la version du client).

---

## Équivalences avec ce que tu connais déjà

| SQL classique (bac à sable SQLite) | Spark SQL |
|---|---|
| `julianday(a) - julianday(b)` | `datediff(a, b)` (fin, début) |
| `date('now')` | `current_date()` |
| `a \|\| b` | `a \|\| b` ou `concat(a, b)` |
| `group_concat(x)` | `collect_list(x)` (liste) ou `concat_ws(',', collect_list(x))` |
| `LIMIT n` | `LIMIT n` |
| `NOT EXISTS` / anti-jointure `LEFT JOIN … IS NULL` | `LEFT ANTI JOIN` (idiomatique) |
| `EXISTS` / `IN (sous-requête)` | `LEFT SEMI JOIN` (idiomatique) |
| `WITH … AS (…)` | identique |
| `RANK() OVER (…)` | identique |

Ce qui **ne ressemble pas** à une base classique : pas de `UPDATE`/`DELETE` sur des fichiers bruts (selon le format
de table : voir Delta/Iceberg), pas d'index au sens habituel, les « tables » sont des fichiers dans un stockage
(Parquet, ORC, CSV…) accompagnés d'un catalogue. Voir `concepts.md`.
