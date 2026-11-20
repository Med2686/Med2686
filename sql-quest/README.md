# SQL Quest

Appli d'entraînement SQL pour BA / testeur, **100 % locale et hors connexion** : le cas de recette
bancaire fictif, un champ de réponse, puis la correction et l'explication une fois que tu as répondu.

## Lancer

Ouvre `index.html` dans ton navigateur (double-clic). Aucun serveur, aucune installation, aucun accès
internet. La base SQLite et le moteur sont embarqués dans les fichiers.

## Utilisation

- **Exercices de niveau 0** : questions à réponse libre sur la lecture d'une base. Tu écris ta réponse, la
  correction s'affiche, puis tu t'auto-évalues (Juste / Partielle / À revoir).
- **Exercices SQL (niveaux 1 à 3)** : tu écris la requête, **Exécuter** pour la tester, **Valider** pour la
  comparer à la correction (colonnes, lignes, valeurs). Jusqu'à 3 indices progressifs.
- **Atelier (glisser-déposer, animé)** : 5 exercices repérés « glisser-déposer » dans la liste.
  - *Assemble* (AT-1 à AT-3) : tu construis la requête avec des blocs (SELECT, FROM, WHERE, GROUP BY, HAVING).
    Un bloc posé dans la mauvaise zone est refusé avec une explication (par ex. `COUNT(*)` dans WHERE).
  - *Ordre d'exécution* (OR-1) : remettre les 7 étapes d'une requête dans l'ordre où le moteur les exécute.
  - *Jointure animée* (JN-1) : relier deux clés, prédire le nombre de lignes, puis voir la jointure se dérouler
    ligne à ligne (INNER vs LEFT).
  - Sur tactile ou au clavier : clique un bloc puis clique la zone, ou utilise les boutons ▲ ▼.
  - L'atelier sert à **comprendre la structure** ; les exercices SQL au clavier restent indispensables.
- **XP et rangs** : chaque exercice réussi rapporte des points (réduits de 30 % si tu as pris un indice).
- **Panneau Données** : toutes les tables. Les valeurs bleues (↗) sont des clés étrangères : un clic mène à
  la ligne visée dans l'autre table.
- **Bac à sable libre** : tes propres `SELECT` (lecture seule).
- **Copier mes réponses** : copie toutes tes réponses en texte, pour les coller dans la conversation et
  obtenir une correction détaillée.
- Ta progression reste dans le navigateur (`localStorage`) ; **Effacer ma progression** remet tout à zéro.

Limite : l'auto-évaluation des exercices de niveau 0 est déclarative (l'appli ne lit pas ton texte).

## Maintenance

- Exercices et corrections : `exercices.js` ; mécaniques de l'atelier : `atelier.js`.
- Base de données : générée par `.claude/skills/maitre-sql/scripts/build_seed.py`, puis embarquée par
  `python3 build.py` (régénère `seed.js`).
- Moteur : [sql.js](https://github.com/sql-js/sql.js) 1.10.3 (licence MIT, `vendor/LICENSE-sqljs`),
  en version asm.js (`vendor/sql-asm.js`, JavaScript pur) : pas de WebAssembly, donc il fonctionne depuis `file://` et dans un environnement à politique de sécurité stricte.
