# Les 12 pièges SQL qui coûtent cher à un BA / testeur

Pour chaque piège : **ce qui se passe**, **pourquoi c'est dangereux en recette**, **la parade**. Les
exemples tournent sur le bac à sable (`bac-a-sable.md`). Demande à l'utilisateur de **prédire** le
résultat avant de l'exécuter : c'est la meilleure façon d'ancrer le piège.

## 1. `NOT IN` + une valeur `NULL` = zéro ligne
`WHERE x NOT IN (SELECT y ...)` : si `y` contient un seul `NULL`, la condition n'est jamais vraie.
Résultat : « aucun orphelin » alors qu'il y en a. **Parade** : `LEFT JOIN ... WHERE parent.id IS NULL`
ou `NOT EXISTS`.

## 2. Le filtre du `LEFT JOIN` placé dans le `WHERE`
`LEFT JOIN cas_test ct ON ... WHERE ct.resultat = 'OK'` élimine les lignes sans correspondance : le
`LEFT JOIN` est devenu un `INNER JOIN`. **Parade** : le filtre sur la table de droite va dans le `ON` ;
seul le test `IS NULL` d'un anti-join va dans le `WHERE`.

## 3. `INNER JOIN` qui fait disparaître le cas intéressant
Un batch qui n'a rien écrit, un client sans compte : le `JOIN` simple les masque. **Parade** : se demander
« qu'est-ce que je veux voir *quand il n'y a rien en face* ? » ; si la réponse est « la ligne quand même »,
c'est un `LEFT JOIN`.

## 4. Fan-out : la jointure multiplie les lignes
Joindre `clients` à `comptes` puis sommer une colonne de `clients` additionne chaque valeur autant de fois
qu'il y a de comptes. Les totaux explosent sans erreur. **Parade** : connaître le **grain** de chaque
table (une ligne = quoi ?), comparer `COUNT(*)` avant/après la jointure, agréger **avant** de joindre.
`DISTINCT` qui « règle » un doublon inexpliqué cache souvent un fan-out : comprends-le d'abord.

## 5. `COUNT(*)` vs `COUNT(colonne)` après un `LEFT JOIN`
`COUNT(*)` compte une ligne même quand la jointure ne trouve rien (résultat 1 au lieu de 0).
**Parade** : `COUNT(t.id)` sur la colonne de la table jointe.

## 6. `= NULL` au lieu de `IS NULL`
`WHERE date_cloture = NULL` ne renvoie jamais rien : toute comparaison avec `NULL` est « inconnue ».
**Parade** : `IS NULL` / `IS NOT NULL`. Idem pour `<> 'x'` qui ignore les lignes `NULL` : écris
`(col <> 'x' OR col IS NULL)` si elles comptent. `COALESCE(col, valeur)` remplace un `NULL` (Oracle :
`NVL`).

## 7. Filtrer sur un alias ou un agrégat dans le `WHERE`
`WHERE nb > 3` avec `nb = COUNT(*)` échoue : le `WHERE` s'exécute avant le `GROUP BY`. **Parade** :
`HAVING COUNT(*) > 3`. Retiens l'ordre logique : FROM/JOIN → WHERE → GROUP BY → HAVING → SELECT → ORDER BY
→ LIMIT.

## 8. `GROUP BY` incomplet
Toute colonne du `SELECT` qui n'est pas dans un agrégat doit être dans le `GROUP BY` (la plupart des
moteurs refusent ; MySQL et SQLite le tolèrent et renvoient une valeur arbitraire : pire, car silencieux).
**Parade** : liste explicitement les colonnes de regroupement.

## 9. Division entière
`SUM(ok) / COUNT(*)` entre deux entiers donne 0 ou 1 sous SQL Server, PostgreSQL, SQLite. **Parade** :
`100.0 * SUM(...) / COUNT(*)`. Précise toujours le dénominateur (tous les cas ? les cas exécutés ?).

## 10. Comparer des montants décimaux avec `=`
Des flottants peuvent différer à la 12ᵉ décimale. **Parade** : `ABS(a - b) > 0.005` ou `ROUND`, et vérifie
si la colonne est `DECIMAL`/`NUMERIC` (exact) ou `FLOAT`/`REAL` (approché).

## 11. Dates : texte, fuseau, bornes
- Une date stockée en texte se compare **alphabétiquement** : correct en `AAAA-MM-JJ`, faux en `JJ/MM/AAAA`.
- `BETWEEN '2026-11-01' AND '2026-11-30'` rate le 30 novembre si la colonne contient une heure. **Parade** :
  `>= début AND < lendemain de la fin`.
- Un horodatage en UTC affiché en heure locale décale un traitement de nuit d'un jour.
- Les fonctions de date changent selon le moteur : `dialectes.md`.

## 12. Fonction de fenêtre filtrée dans le `WHERE`, ou sans `ORDER BY`
`WHERE ROW_NUMBER() OVER (...) = 1` est refusé : la fenêtre est calculée après le `WHERE`. **Parade** :
CTE ou sous-requête, puis filtre dehors. Sans `ORDER BY` dans la fenêtre, le « premier » est arbitraire ;
ajoute un critère de départage (`, id`) pour un résultat reproductible.

---

## Les 4 réflexes anti-piège (à faire répéter à l'utilisateur)

1. **Prédire** le nombre de lignes avant d'exécuter, **comparer** après.
2. **Compter avant/après chaque jointure** pour détecter perte ou multiplication.
3. **Regarder 3 lignes à la main** dans la base (pas seulement le total).
4. **Se demander ce que deviennent les `NULL`** à chaque filtre et chaque jointure.
