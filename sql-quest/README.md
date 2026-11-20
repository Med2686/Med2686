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
- **Panneau Données** : toutes les tables. Les valeurs bleues (↗) sont des clés étrangères : un clic mène à
  la ligne visée dans l'autre table.
- **Bac à sable libre** : tes propres `SELECT` (lecture seule).
- **Copier mes réponses** : copie toutes tes réponses en texte, pour les coller dans la conversation et
  obtenir une correction détaillée.
- Ta progression reste dans le navigateur (`localStorage`) ; **Effacer ma progression** remet tout à zéro.

Limite : l'auto-évaluation des exercices de niveau 0 est déclarative (l'appli ne lit pas ton texte).

## Maintenance

- Exercices et corrections : `exercices.js`.
- Base de données : générée par `.claude/skills/maitre-sql/scripts/build_seed.py`, puis embarquée par
  `python3 build.py` (régénère `seed.js`).
- Moteur : [sql.js](https://github.com/sql-js/sql.js) 1.10.3 (licence MIT, `vendor/LICENSE-sqljs`),
  embarqué en base64 (`vendor/sql-wasm-base64.js`) pour fonctionner depuis `file://`.
