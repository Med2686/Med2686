# Bac à sable : base de recette bancaire fictive

Fichier : `assets/bac-a-sable.sql` (SQLite, données 100 % inventées, déterministe : régénérable avec
`python3 scripts/build_seed.py assets/bac-a-sable.sql`). Mode d'emploi pour l'exécuter : voir `SKILL.md`.

## Schéma

| Table | Colonnes | Lignes | Rôle |
|---|---|---|---|
| `clients` | id, nom, prenom, email, segment (Particulier/Pro/Entreprise), ville, statut (actif/clos/suspendu), date_creation | 60 | Référentiel client |
| `comptes` | id, client_id → clients, type (courant/livret/pro), statut (ouvert/clos), date_ouverture, solde | 80 | Comptes d'un client |
| `transactions` | id, compte_id → comptes, date_op, montant, sens (C/D), canal (agence/web/mobile/batch), libelle, batch_id → batchs | ~710 | Mouvements |
| `batchs` | id, nom, date_run, statut (OK/PARTIEL/KO), nb_lus, nb_ecrits | 12 | Exécutions de batch de nuit |
| `exigences` | id, code, titre, priorite (Must/Should/Could), statut | 18 | Exigences à recetter |
| `campagnes` | id, nom, environnement (REC1/REC2/PREPROD), date_debut, date_fin | 3 | Campagnes de recette |
| `cas_test` | id, campagne_id, exigence_id, titre, resultat (OK/KO/Bloqué/Non exécuté), testeur | 45 | Cas de test et leur résultat |
| `anomalies` | id, cas_test_id, campagne_id, titre, severite (bloquante/majeure/mineure), statut (ouverte/en correction/corrigée/fermée/rejetée), assigne_a, environnement, date_creation, date_cloture | 17 | Fiches d'anomalie |

Relations : `clients 1—n comptes 1—n transactions` ; `batchs 1—n transactions` (via `batch_id`, nul pour
les opérations hors batch) ; `exigences 1—n cas_test n—1 campagnes` ; `cas_test 1—n anomalies`.
Aucune clé étrangère n'est déclarée (comme dans beaucoup de bases réelles) : c'est ce qui permet les
orphelins. Dates en texte `AAAA-MM-JJ`.

## Anomalies de données plantées (à trouver, ne les révèle pas d'emblée)

- 2 e-mails clients en doublon (clients 58 et 59 recréés).
- 3 comptes dont le `client_id` n'existe pas (901, 902, 903).
- 3 comptes dont le solde ne correspond pas à la somme des mouvements (comptes 4, 17, 33 : +120,50).
- Batch 5 (PARTIEL) annonce 3 écritures de plus qu'il n'y en a en base ; batch 9 (KO) en annonce 7, 0 en base.
- 3 exigences sans aucun cas de test (EXG-007, EXG-012, EXG-016).
- 4 clients actifs dont l'unique compte est clos ; 4 clients suspendus avec un compte ouvert.
- 1 cas de test KO sans aucune fiche d'anomalie (campagne 3, cas « Montant au plafond (EXG-008) »).
- Go/No-Go : campagne 1 → GO, campagne 2 → NO GO (2 bloquantes ouvertes), campagne 3 → RÉSERVES.

## Exercices (du plus simple au plus riche)

Règle d'usage : l'énoncé est donné à l'utilisateur, **les corrigés ne sont montrés qu'après sa tentative**
et l'échelle d'aide de `SKILL.md`. Exécute sa réponse et compare au corrigé (colonnes, lignes, valeurs).

### Niveau 1 : lire et filtrer

**1.** « Le COPIL est dans une heure : donne-moi les anomalies bloquantes encore ouvertes (id, titre,
assigné à). »
```sql
-- [test] attendu: 2
SELECT id, titre, assigne_a
FROM anomalies
WHERE severite = 'bloquante' AND statut = 'ouverte';
```

**2.** « Les 5 dernières anomalies créées en REC2 » (égalité de date : id décroissant).
```sql
-- [test] attendu: 5
SELECT id, titre, date_creation
FROM anomalies
WHERE environnement = 'REC2'
ORDER BY date_creation DESC, id DESC
LIMIT 5;
```

**3.** « Toutes les anomalies qui parlent d'IBAN. »
```sql
-- [test] attendu: 2
SELECT id, titre
FROM anomalies
WHERE titre LIKE '%IBAN%';
```

### Niveau 2 : compter et regrouper

**4.** « Combien de cas de test sont KO ? »
```sql
-- [test] attendu: 1
SELECT COUNT(*) AS nb_ko
FROM cas_test
WHERE resultat = 'KO';
```

**5.** « Répartition des cas de test par résultat, du plus fréquent au moins fréquent. »
```sql
-- [test] attendu: 4
SELECT resultat, COUNT(*) AS nb
FROM cas_test
GROUP BY resultat
ORDER BY nb DESC;
```

**6.** « Par campagne : nombre de cas, nombre OK, pourcentage OK arrondi à 1 décimale. » → corrigé : scénario 6
de `scenarios-ba.md`.

**7.** « Quels testeurs ont au moins 3 cas KO ? »
```sql
-- [test] attendu: 2
SELECT testeur, COUNT(*) AS nb_ko
FROM cas_test
WHERE resultat = 'KO'
GROUP BY testeur
HAVING COUNT(*) >= 3
ORDER BY nb_ko DESC;
```

### Niveau 3 : relier les tables

**8.** « Les anomalies bloquantes avec le nom de leur campagne. »
```sql
-- [test] attendu: 8
SELECT a.id, a.titre, ca.nom AS campagne
FROM anomalies a
JOIN campagnes ca ON ca.id = a.campagne_id
WHERE a.severite = 'bloquante'
ORDER BY a.id;
```

**9.** « Pour chaque exigence Must, les cas de test en échec (code exigence, titre du cas). »
```sql
-- [test] attendu: 5
SELECT e.code, ct.titre
FROM exigences e
JOIN cas_test ct ON ct.exigence_id = e.id
WHERE e.priorite = 'Must' AND ct.resultat = 'KO'
ORDER BY e.code, ct.id;
```

**10.** « Quels cas KO ou Bloqués n'ont aucune fiche d'anomalie ? » (contrôle de rigueur du testeur)
```sql
-- [test] attendu: 1
SELECT ct.id, ct.titre, ct.testeur
FROM cas_test ct
LEFT JOIN anomalies a ON a.cas_test_id = ct.id
WHERE ct.resultat IN ('KO', 'Bloqué')
  AND a.id IS NULL;
```

### Niveau 4 : enquêter sur la donnée

Corrigés dans `scenarios-ba.md` : **11** doublons clients (scénario 1), **12** comptes orphelins
(scénario 2), **13** batchs dont le compteur ne colle pas (scénario 3), **14** soldes incohérents
(scénario 4), **15** exigences non couvertes (scénario 5), **16** différence d'ensembles dans les deux
sens (scénario 10).

### Niveau 5 : analyser

Corrigés dans `scenarios-ba.md` : **17** Go/No-Go par campagne (scénario 7), **18** délai de traitement
par sévérité (scénario 8), **19** traçabilité exigence → anomalie (scénario 9), **20** première anomalie
ouverte par campagne (scénario 12).

**21.** « Classe les développeurs (assigné à) par nombre d'anomalies reçues, ex æquo avec le même rang. »
```sql
-- [test] attendu: 4
SELECT assigne_a,
       COUNT(*) AS nb,
       RANK() OVER (ORDER BY COUNT(*) DESC) AS rang
FROM anomalies
GROUP BY assigne_a
ORDER BY rang, assigne_a;
```

**22.** « Quels testeurs ont un taux de KO supérieur au taux de KO global ? » (à faire avec une CTE)
```sql
-- [test] attendu: 2
WITH par_testeur AS (
  SELECT testeur,
         COUNT(*) AS nb,
         SUM(CASE WHEN resultat = 'KO' THEN 1 ELSE 0 END) AS nb_ko
  FROM cas_test
  GROUP BY testeur
),
global AS (
  SELECT 1.0 * SUM(nb_ko) / SUM(nb) AS taux FROM par_testeur
)
SELECT p.testeur, ROUND(100.0 * p.nb_ko / p.nb, 1) AS pct_ko
FROM par_testeur p, global g
WHERE 1.0 * p.nb_ko / p.nb > g.taux
ORDER BY pct_ko DESC;
```
*À dire à l'utilisateur :* ce taux de KO par testeur n'est **pas** un indicateur de performance du
testeur (les cas qu'on lui a confiés n'ont pas la même difficulté). Si ce chiffre sort en réunion, tu
dois savoir le contester.

## Défis de fin de parcours (sans corrigé : à construire ensemble)

- Écrire le « rapport de sortie de recette » en une seule requête : une ligne par campagne avec avancement,
  nombre d'anomalies ouvertes par sévérité, décision Go/No-Go.
- Détecter les clients dont les comptes cumulent un solde négatif et au moins un prélèvement rejeté
  (invente la règle, formule-la en une phrase, puis écris-la).
- Réécrire une requête de la MOE trouvée en mission (anonymisée) et comparer les résultats.
