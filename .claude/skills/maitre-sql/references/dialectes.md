# Dialectes : ce qui change selon le moteur

Le bac à sable est en **SQLite**. En mission, le client utilise probablement **Oracle**, **SQL Server**,
**PostgreSQL** ou **DB2**. La logique (SELECT, JOIN, GROUP BY, CTE, fenêtres) est la même ; les écarts sont
sur les fonctions. Les entrées marquées `(à vérifier)` sont à confirmer sur la version du client avant de
les affirmer devant la MOE : consulte la documentation officielle du moteur.

| Besoin | SQLite (bac à sable) | PostgreSQL | SQL Server | Oracle | MySQL |
|---|---|---|---|---|---|
| Limiter les lignes | `LIMIT n` | `LIMIT n` | `SELECT TOP n` ou `OFFSET/FETCH` | `FETCH FIRST n ROWS ONLY` (12c+), sinon `ROWNUM` | `LIMIT n` |
| Date du jour | `date('now')` | `CURRENT_DATE` | `CAST(GETDATE() AS date)` | `TRUNC(SYSDATE)` | `CURDATE()` |
| Écart en jours | `julianday(a) - julianday(b)` | `a::date - b::date` | `DATEDIFF(day, b, a)` | `a - b` (dates) | `DATEDIFF(a, b)` |
| Ajouter des jours | `date(d, '+7 day')` | `d + INTERVAL '7 days'` | `DATEADD(day, 7, d)` | `d + 7` | `DATE_ADD(d, INTERVAL 7 DAY)` |
| Concaténer | `a \|\| b` | `a \|\| b` | `a + b` ou `CONCAT` | `a \|\| b` | `CONCAT(a, b)` |
| Remplacer un NULL | `COALESCE` / `IFNULL` | `COALESCE` | `COALESCE` / `ISNULL` | `COALESCE` / `NVL` | `COALESCE` / `IFNULL` |
| Différence d'ensembles | `EXCEPT` | `EXCEPT` | `EXCEPT` | `MINUS` | `EXCEPT` (8.0.31+) (à vérifier) |
| Sous-chaîne | `substr(s, d, n)` | `SUBSTRING` | `SUBSTRING` | `SUBSTR` | `SUBSTRING` |
| Texte → date | `date(s)` | `TO_DATE(s, 'YYYY-MM-DD')` | `CONVERT(date, s)` / `CAST` | `TO_DATE(s, 'YYYY-MM-DD')` | `STR_TO_DATE` |
| Chaîne vide vs NULL | distincts | distincts | distincts | **`''` est traité comme `NULL`** | distincts |
| Insensible à la casse | `LIKE` (ASCII) | `ILIKE` | selon collation | `UPPER(col) LIKE ...` | selon collation |
| Agréger du texte | `group_concat(x)` | `string_agg(x, ',')` | `STRING_AGG(x, ',')` (2017+) | `LISTAGG(x, ',')` | `GROUP_CONCAT(x)` |
| Table sans FROM | `SELECT 1` | `SELECT 1` | `SELECT 1` | `SELECT 1 FROM DUAL` | `SELECT 1` |

## Points qui piègent vraiment

- **Oracle traite `''` comme `NULL`** : `WHERE col = ''` ne renvoie jamais rien ; un champ « vide » est
  `NULL`. Source classique de contrôles faux quand on vient d'un autre moteur.
- **SQL Server `/` entre entiers** donne un entier ; **`+` entre texte et `NULL`** donne `NULL`.
- **Sensibilité à la casse** et **tri** dépendent de la collation de la base : `'a' = 'A'` peut être vrai
  ou faux selon la configuration. Demande-le à la MOE avant de t'étonner d'un écart.
- Les **types de date** diffèrent (`DATE` Oracle contient l'heure ; `datetime2` SQL Server ; `timestamp`
  PostgreSQL) : le piège n°11 de `pieges.md` s'y applique.
- Les **noms** entre guillemets (`"Client"`) sont sensibles à la casse sous PostgreSQL/Oracle ;
  SQL Server utilise `[Client]`, MySQL des accents graves.

## Question à poser à la MOE au démarrage

« Quel moteur et quelle version, sur quel environnement puis-je faire des SELECT, avec quel compte
lecture seule, et existe-t-il des vues dédiées plutôt que les tables brutes ? »
