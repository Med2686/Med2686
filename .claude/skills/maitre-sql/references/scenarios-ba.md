# Scénarios SQL de BA / testeur fonctionnel

Chaque scénario part d'une **situation de mission**, énonce la **règle à contrôler**, donne une requête,
et dit comment **lire le résultat**. Les requêtes marquées `-- [test]` sont exécutées contre
`assets/bac-a-sable.sql` ; `-- attendu: N` est le nombre de lignes retourné. Pour adapter à la base réelle,
remplace les noms de tables/colonnes et vois `dialectes.md` pour les fonctions de date.

**Principe général d'une requête de contrôle** : elle retourne **uniquement les lignes en anomalie**.
Zéro ligne = contrôle OK. Cela se lit d'un coup d'œil et se colle tel quel dans une fiche d'anomalie.

---

## 1. Doublons

**Situation.** Le métier dit « j'ai deux fiches pour le même client ». Règle : un e-mail = un client.

```sql
-- [test] attendu: 2
SELECT email, COUNT(*) AS nb
FROM clients
GROUP BY email
HAVING COUNT(*) > 1;
```

Voir les fiches complètes en doublon (pour les donner à la MOE) :

```sql
-- [test] attendu: 4
SELECT c.*
FROM clients c
WHERE c.email IN (SELECT email FROM clients GROUP BY email HAVING COUNT(*) > 1)
ORDER BY c.email, c.id;
```

**Lecture.** Le doublon peut être légitime (homonymes, e-mail familial partagé) : ne conclus pas à une
anomalie avant d'avoir confirmé la règle de gestion avec le métier. Choisis la clé de doublon sur la règle
métier, pas sur ce qui est pratique.

---

## 2. Orphelins (clé étrangère sans parent)

**Situation.** Après une migration, des comptes pointent vers des clients qui n'existent plus.

```sql
-- [test] attendu: 3
SELECT cp.id AS compte_id, cp.client_id
FROM comptes cp
LEFT JOIN clients cl ON cl.id = cp.client_id
WHERE cl.id IS NULL;
```

**Lecture.** `LEFT JOIN ... WHERE parent.id IS NULL` est la forme sûre. Évite `NOT IN (SELECT id ...)` :
si la sous-requête contient un seul `NULL`, `NOT IN` ne renvoie plus rien (voir `pieges.md` n°1).
Une clé étrangère **nullable** à `NULL` n'est pas forcément un orphelin : la règle métier tranche.

---

## 3. Réconciliation d'un batch : compteur annoncé vs écritures réelles

**Situation.** Le batch de nuit dit « 18 écritures » ; combien en base ? Écart = anomalie ou perte.

```sql
-- [test] attendu: 2
SELECT b.id, b.date_run, b.statut, b.nb_ecrits AS annonce, COUNT(t.id) AS en_base
FROM batchs b
LEFT JOIN transactions t ON t.batch_id = b.id
GROUP BY b.id, b.date_run, b.statut, b.nb_ecrits
HAVING COUNT(t.id) <> b.nb_ecrits
ORDER BY b.date_run;
```

**Lecture.** Le `LEFT JOIN` est indispensable : un batch qui n'a rien écrit (statut KO) n'apparaît pas avec
un `JOIN` simple, alors que c'est justement le cas à voir. `COUNT(t.id)` (et non `COUNT(*)`) compte les
lignes réellement jointes : sur un `LEFT JOIN`, `COUNT(*)` renverrait 1 pour un batch vide.

---

## 4. Réconciliation de montants : solde vs somme des mouvements

**Situation.** Le solde affiché ne correspond pas à l'historique.

```sql
-- [test] attendu: 3
SELECT c.id, c.solde,
       ROUND(SUM(CASE WHEN t.sens = 'C' THEN t.montant ELSE -t.montant END), 2) AS calcule
FROM comptes c
JOIN transactions t ON t.compte_id = c.id
GROUP BY c.id, c.solde
HAVING ABS(c.solde - SUM(CASE WHEN t.sens = 'C' THEN t.montant ELSE -t.montant END)) > 0.005;
```

**Lecture.** Compare des montants **avec une tolérance** (`ABS(écart) > 0.005`), jamais avec `=` : les
nombres décimaux flottants produisent des écarts d'arrondi parasites. Sur des montants stockés en
`DECIMAL`/`NUMERIC` la tolérance est inutile, mais ne parie pas sans vérifier le type.

---

## 5. Trous de couverture : exigences sans cas de test

**Situation.** Avant le go/no-go, le chef de projet demande « tout est couvert ? ».

```sql
-- [test] attendu: 3
SELECT e.code, e.titre, e.priorite
FROM exigences e
LEFT JOIN cas_test ct ON ct.exigence_id = e.id
WHERE ct.id IS NULL
ORDER BY e.code;
```

Variante utile, exigences **Must** dont aucun cas n'est OK :

```sql
-- [test] attendu: 3
SELECT e.code, e.titre
FROM exigences e
LEFT JOIN cas_test ct ON ct.exigence_id = e.id AND ct.resultat = 'OK'
WHERE e.priorite = 'Must'
GROUP BY e.id, e.code, e.titre
HAVING COUNT(ct.id) = 0
ORDER BY e.code;
```

**Lecture.** Le filtre `ct.resultat = 'OK'` est dans le `ON`, pas dans le `WHERE` : c'est ce qui garde
l'exigence sans cas OK dans le résultat (voir `pieges.md` n°2). Le résultat mélange deux situations à
distinguer devant le chef de projet : des exigences **jamais testées** et des exigences **testées mais
sans cas OK** (ici, EXG-008 n'a que des échecs).

---

## 6. Tableau de bord de recette : avancement par campagne

```sql
-- [test] attendu: 3
SELECT ca.nom,
       COUNT(*)                                               AS nb_cas,
       SUM(CASE WHEN ct.resultat = 'OK' THEN 1 ELSE 0 END)    AS nb_ok,
       SUM(CASE WHEN ct.resultat = 'KO' THEN 1 ELSE 0 END)    AS nb_ko,
       SUM(CASE WHEN ct.resultat = 'Non exécuté' THEN 1 ELSE 0 END) AS nb_a_faire,
       ROUND(100.0 * SUM(CASE WHEN ct.resultat = 'OK' THEN 1 ELSE 0 END) / COUNT(*), 1) AS pct_ok
FROM campagnes ca
JOIN cas_test ct ON ct.campagne_id = ca.id
GROUP BY ca.id, ca.nom
ORDER BY ca.id;
```

**Lecture.** `100.0 *` force la division décimale (en SQL Server, `SUM(...) / COUNT(*)` entre entiers donne
un entier). Dis explicitement quel dénominateur tu prends (tous les cas ? les cas exécutés ?) : deux
« taux de réussite » différents circulent souvent dans un même projet.

---

## 7. Go / No-Go par campagne

**Règle (à valider avec le métier) :** NO GO s'il reste une anomalie bloquante non résolue ; RÉSERVES s'il
reste une majeure non résolue ; sinon GO. « Non résolue » = statut `ouverte` ou `en correction`.

```sql
-- [test] attendu: 3
SELECT ca.nom,
       CASE
         WHEN SUM(CASE WHEN a.severite = 'bloquante' AND a.statut IN ('ouverte','en correction') THEN 1 ELSE 0 END) > 0 THEN 'NO GO'
         WHEN SUM(CASE WHEN a.severite = 'majeure'   AND a.statut IN ('ouverte','en correction') THEN 1 ELSE 0 END) > 0 THEN 'RESERVES'
         ELSE 'GO'
       END AS decision
FROM campagnes ca
LEFT JOIN anomalies a ON a.campagne_id = ca.id
GROUP BY ca.id, ca.nom
ORDER BY ca.id;
```

**Lecture.** Les `WHEN` sont évalués dans l'ordre : le plus grave en premier. Cette requête automatise une
règle, pas une décision : le go/no-go reste une décision humaine arbitrée avec le chef de projet.

---

## 8. Délais de traitement des anomalies

```sql
-- [test] attendu: 3
-- SQLite : julianday(). Oracle : date_cloture - date_creation. SQL Server : DATEDIFF(day, ...).
SELECT severite,
       COUNT(*) AS nb,
       ROUND(AVG(julianday(date_cloture) - julianday(date_creation)), 1) AS delai_moyen_jours
FROM anomalies
WHERE date_cloture IS NOT NULL
GROUP BY severite
ORDER BY delai_moyen_jours DESC;
```

**Lecture.** Le `WHERE date_cloture IS NOT NULL` exclut les anomalies ouvertes : le délai moyen ne
concerne donc que les anomalies déjà traitées. Dis-le quand tu présentes le chiffre.

---

## 9. Traçabilité : exigence → cas de test → anomalie

**Situation.** « Quelles exigences Must sont impactées par une anomalie bloquante ouverte ? »

```sql
-- [test] attendu: 1
SELECT DISTINCT e.code, e.titre, a.id AS anomalie_id
FROM anomalies a
JOIN cas_test ct ON ct.id = a.cas_test_id
JOIN exigences e ON e.id = ct.exigence_id
WHERE e.priorite = 'Must'
  AND a.severite = 'bloquante'
  AND a.statut = 'ouverte'
ORDER BY e.code;
```

**Lecture.** Chaîne de jointures : relis-la dans l'ordre (anomalie → cas → exigence). Ajoute `DISTINCT`
seulement après avoir compris pourquoi il y aurait des doublons (voir fan-out, `pieges.md` n°4).

---

## 10. Différence entre deux ensembles (dans les deux sens)

**Situation.** « Tous les clients actifs ont-ils un compte ouvert, et inversement ? »

```sql
-- [test] attendu: 4
-- Sens 1 : clients actifs sans compte ouvert
SELECT id FROM clients WHERE statut = 'actif'
EXCEPT
SELECT client_id FROM comptes WHERE statut = 'ouvert';
```

```sql
-- [test] attendu: 7
-- Sens 2 : comptes ouverts dont le client n'est pas actif (ou n'existe pas)
SELECT client_id FROM comptes WHERE statut = 'ouvert'
EXCEPT
SELECT id FROM clients WHERE statut = 'actif';
```

**Lecture.** `EXCEPT` (SQL Server, PostgreSQL, SQLite) s'appelle `MINUS` sous Oracle. Une réconciliation
n'est complète que si tu la fais **dans les deux sens** : un seul sens ne voit que la moitié des écarts.
Ici le sens 2 ramène 7 valeurs : les 3 orphelins du scénario 2 (le client n'existe pas) et 4 clients
suspendus qui ont encore un compte ouvert (cas à confirmer avec le métier : anomalie ou règle admise ?).

---

## 11. Trouver une donnée de test qui remplit les préconditions

**Situation.** Le cas de test exige « un client Particulier actif, avec un livret et un compte courant
ouverts ». Tu ne veux pas créer de donnée : tu en cherches une existante.

```sql
-- [test] attendu: 1
SELECT cl.id, cl.nom, cl.prenom
FROM clients cl
JOIN comptes cp ON cp.client_id = cl.id AND cp.statut = 'ouvert'
WHERE cl.segment = 'Particulier'
  AND cl.statut = 'actif'
GROUP BY cl.id, cl.nom, cl.prenom
HAVING SUM(CASE WHEN cp.type = 'livret'  THEN 1 ELSE 0 END) >= 1
   AND SUM(CASE WHEN cp.type = 'courant' THEN 1 ELSE 0 END) >= 1
ORDER BY cl.id
LIMIT 1;
```

**Lecture.** Une condition « a au moins un X **et** un Y » se traite avec `HAVING` + sommes conditionnelles,
pas avec `WHERE type = 'livret' AND type = 'courant'` (qui ne renvoie jamais rien). `LIMIT 1` :
Oracle `FETCH FIRST 1 ROWS ONLY`, SQL Server `TOP 1`. Les données de test réelles sont sensibles : ne les
colle pas dans un ticket public.

---

## 12. Le plus récent / le premier par groupe (fonction de fenêtre)

**Situation.** « Quelle est l'anomalie ouverte la plus ancienne de chaque campagne ? »

```sql
-- [test] attendu: 2
WITH ouvertes AS (
  SELECT a.*,
         ROW_NUMBER() OVER (PARTITION BY campagne_id ORDER BY date_creation, id) AS rang
  FROM anomalies a
  WHERE statut = 'ouverte'
)
SELECT id, campagne_id, titre, date_creation
FROM ouvertes
WHERE rang = 1
ORDER BY campagne_id;
```

**Lecture.** On **ne peut pas** filtrer sur `ROW_NUMBER()` dans le `WHERE` de la même requête : la fonction
de fenêtre est calculée après le `WHERE`. On l'enferme dans une CTE (ou une sous-requête) et on filtre
dehors. Ajoute un critère de départage (`, id`) pour que le résultat soit déterministe.

---

## Check-list avant de présenter un résultat

1. Combien de lignes ? Est-ce plausible ? (comparer à un chiffre connu ou à un `COUNT(*)` simple)
2. Ai-je vérifié 2-3 lignes **à la main** dans la base ?
3. Ma requête perd-elle des lignes (INNER JOIN) ou en multiplie-t-elle (fan-out) ?
4. Les `NULL` sont-ils traités volontairement ?
5. Quel environnement, quelle date d'extraction, quelle requête exacte ? (à noter dans la fiche d'anomalie)
