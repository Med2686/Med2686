# Où pratiquer en dehors du bac à sable

Synthèse d'une recherche web (novembre 2026). **Limites** : la plupart des sources sont des blogs ou des
pages éditeur ; plusieurs comparatifs sont écrits par les plateformes qu'ils comparent. Je n'ai pas vérifié
les tarifs ni les contenus actuels : à confirmer sur le site avant de s'inscrire. Aucune de ces ressources
n'est conçue pour le métier de BA/testeur : c'est pourquoi `bac-a-sable.md` existe.

## Ce que les sources disent en commun

- Les feuilles de route convergent : requêtes de base → jointures et agrégations → sous-requêtes et CTE →
  notions avancées (fenêtres), avec pratique sur des jeux de données réalistes à chaque étape.
- Les pièges les plus cités sont les mêmes que dans `pieges.md` : fonctions de fenêtre dans le `WHERE`,
  `NULL`, `NOT IN`, `LEFT JOIN` transformé en `INNER JOIN`, fan-out de jointure, égalités de rang.
- Pour les contrôles de données (testeur), le trio doublons / orphelins / réconciliation (comptages,
  agrégats, différence d'ensembles dans les deux sens) est le socle ; un test qui ne renvoie **que les
  lignes en échec** est le plus lisible et le plus automatisable.
- Je n'ai pas trouvé de source solide prouvant que la gamification fait mieux apprendre qu'un entraînement
  régulier avec correction. Ce qui compte : pratiquer souvent, écrire soi-même, recevoir un retour précis.

## Ressources (à qui elles servent)

| Ressource | Type | Utile pour | Réserves |
|---|---|---|---|
| SQLBolt | Leçons interactives courtes | Niveaux 1-3, démarrer vite | Débutant uniquement ; peu de cas métier |
| SQLZoo | Exercices en ligne | Niveaux 1-5, beaucoup de répétition | Interface datée |
| Mode SQL Tutorial | Cours texte orienté analyste (PostgreSQL) | Niveaux 1-5 ; ~10-15 h d'après un comparatif | Pas de projet ni de certificat |
| SQL Murder Mystery (Knight Lab) | Enquête ludique, SQLite en ligne | Se motiver, niveaux 1-3 | 1-3 h selon les sources ; pas d'indices intégrés |
| SQL Island | Jeu narratif (8 quêtes) | Grand débutant | Très simple, hors métier |
| DataLemur | Exercices type entretien, leçons | Niveaux 3-5, fenêtres, CTE | Orienté entretien tech, pas contrôle de données |
| Dataquest | Parcours avec données réelles | Niveaux 1-5, parcours guidé | Payant (vérifier) |
| DataCamp (version française) | Cours vidéo + exercices | Démarrer en français | Intro gratuite, suite payante (vérifier) |
| LearnSQL.fr, SQL.sh | Cours et exercices en français | Lecture en français | Contenu parfois ancien selon une source |
| Coursera, Udemy (cours SQL pour analystes) | Cours | Parcours structuré | Qualité inégale : lire les avis, éviter d'acheter sur un titre |

## Outils pour pratiquer chez soi

- **DB Browser for SQLite** ou la ligne de commande `sqlite3` : charger `assets/bac-a-sable.sql`.
- **DBeaver** (client multi-moteurs) : celui qu'on rencontre souvent en mission pour requêter en lecture
  seule ; à ne configurer que sur un accès fourni par la MOE.
- Éditeurs SQL en ligne (SQLite/PostgreSQL dans le navigateur) : pratiques pour tester une syntaxe, **jamais
  avec des données réelles de mission**.

## Recommandation

1. Faire le parcours de ce skill (niveaux 0 à 4) : c'est ce qui sert **directement** en mission.
2. Compléter avec une ressource externe **uniquement** pour la répétition volumique (SQLZoo ou Mode) ou la
   préparation d'entretien (DataLemur). Éviter d'empiler les plateformes : mieux vaut une pratique
   régulière sur une seule.
3. Si le client donne accès à un environnement de recette en lecture seule, **basculer dessus dès le
   niveau 3** : les tables réelles (noms douteux, `NULL` partout, codes magiques) forment plus que n'importe
   quel jeu propre.
