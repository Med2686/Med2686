# Cycle de mission — de l'entretien à la passation

## Sommaire
0. Avant la mission : entretien de qualification
1. Prise de poste (J1 → J30)
2. Cadrage
3. Recueil et analyse du besoin
4. Spécification / affinage
5. Préparation de la recette
6. Exécution de la recette
7. Go/no-go et MEP
8. Après MEP : VSR, support, conduite du changement
9. Fin de mission : passation et capitalisation
10. Agile vs Cycle en V : correspondances
11. Routine hebdomadaire du BA

Pour chaque phase : **objectif — activités — livrables — avec qui — signal que la phase est finie — pièges**.

---

## 0. Avant la mission : entretien de qualification (client ou ESN)

**Objectif** : décrocher la mission ET vérifier qu'elle est tenable.

**Préparer (1 h suffit)**
- Relire la fiche de poste et surligner : méthode, outils, domaine, livrables attendus, niveau d'autonomie.
- Préparer 3 réalisations au format **STAR** (Situation, Tâche, Action, Résultat chiffré) : une de recueil
  du besoin, une de recette, une de gestion d'une situation tendue.
- Pitch de 2 minutes : qui je suis → double compétence métier/technique → 2 résultats → pourquoi cette mission.

**Questions à poser au client** (elles montrent la séniorité et évitent les pièges)
- Où en est le projet (cadrage, spéc, recette, MEP) et quelle est la prochaine échéance ?
- Qui sera mon interlocuteur principal côté métier ? côté MOE ?
- Comment se passe la recette aujourd'hui (outil, jeux de données, environnement dédié) ?
- Qu'est-ce qui ferait dire, dans 3 mois, que la mission est réussie ?
- Pourquoi ce poste est-il ouvert (création, remplacement, renfort en urgence) ?

**Signal d'alerte** : pas d'environnement de recette, pas de sachant métier disponible, date de MEP figée
sans périmètre figé → à creuser avant d'accepter, ou à tracer dès J1 comme risque.

---

## 1. Prise de poste (J1 → J30)

**Objectif** : devenir crédible vite, sans rien casser. On ne juge pas un BA sur ses 30 premiers jours, mais
on se fait une opinion de lui.

| Période | À faire | Livrable perso |
|---|---|---|
| Semaine 1 | Accès (outils, JIRA, Confluence, environnements), lecture de l'existant (EDB, spec, derniers CR de COPIL, backlog), rencontres individuelles de 30 min avec chef de projet, PO/RMOA, référent métier, lead MOE, testeurs | Carte des acteurs + glossaire + journal de mission créé |
| Semaine 2 | Assister à tous les rituels sans les changer, repérer ce qui marche / coince, reprendre une première petite tâche et la livrer impeccablement | Liste « constats » (non diffusée) |
| Semaines 3-4 | Proposer 1-2 améliorations ciblées (ex. trame de CR, suivi des anomalies), prendre en main un sujet de bout en bout | Point d'étonnement avec le manager |

**Point d'étonnement (fin S3-S4)** : 30 min avec le manager/chef de projet. Structure : ce que j'ai compris
(le projet en 5 lignes) → ce qui fonctionne bien → 3 points de vigilance → ce que je propose → ce dont j'ai
besoin. C'est le moment où l'on passe de « nouveau » à « référent ».

**Pièges** : critiquer l'existant dès la 1re semaine ; vouloir tout changer ; ne pas demander les accès
le J1 (ils prennent souvent 1 à 2 semaines) ; ne pas identifier qui décide réellement.

---

## 2. Cadrage

- **Objectif** : partager le pourquoi, le périmètre, les contraintes, la gouvernance.
- **Activités** : réunion de lancement, identification des parties prenantes, périmètre IN/OUT, hypothèses,
  contraintes (réglementaires, calendrier, budget), premiers risques.
- **Livrables** : note de cadrage, carte des parties prenantes, RACI, planning macro, registre des risques.
- **Avec qui** : sponsor, chef de projet, RMOA/PO, représentants métier, lead MOE, architecte.
- **Fini quand** : périmètre et gouvernance validés en COPIL, RACI partagé.
- **Pièges** : périmètre OUT non écrit (il reviendra par la fenêtre) ; oublier conformité, sécurité, exploitation.

## 3. Recueil et analyse du besoin

- **Objectif** : comprendre le problème métier avant de parler solution.
- **Activités** : entretiens individuels, ateliers, observation terrain (voir l'utilisateur travailler),
  analyse des irritants, modélisation des processus AS-IS / TO-BE, règles de gestion, données manipulées.
- **Livrables** : EDB, cartographie des processus, règles de gestion numérotées, glossaire, liste des
  points ouverts.
- **Avec qui** : utilisateurs clés, experts métier, RMOA/PO ; MOE en observateur pour la faisabilité.
- **Fini quand** : EDB validée par le métier, points ouverts < seuil convenu et tous portés.
- **Pièges** : prendre la solution proposée par le métier pour le besoin (« il faut un bouton ») — demander
  toujours « pour quoi faire ? » ; ne recueillir que le cas nominal.

## 4. Spécification / affinage

- **Objectif** : rendre le besoin réalisable et testable.
- **Cycle en V** : SFG puis SFD, validées formellement. **Agile** : user stories + critères d'acceptation,
  affinées en backlog refinement, prêtes selon la Definition of Ready.
- **Côté technico-fonctionnel** : mapping de données, contrats d'interface (API, fichiers), impacts
  sur les batchs et flux, règles de calcul, gestion des erreurs, habilitations.
- **Livrables** : SFD ou US prêtes, matrice de traçabilité exigences ↔ tests (amorce), maquettes validées.
- **Avec qui** : métier (validation du quoi), MOE (faisabilité, estimation), architecte, testeurs.
- **Fini quand** : chaque exigence/US est comprise par la MOE, testable, et validée par le métier.
- **Pièges** : spéc sans cas d'erreur ; oublier les données existantes (reprise, migration) ; critères
  d'acceptation non mesurables (« rapide », « ergonomique »).

## 5. Préparation de la recette

- **Activités** : stratégie de recette (périmètre, niveaux, risques, critères d'entrée/sortie), plan de
  recette (planning, ressources, environnements), conception des cas de test, jeux de données, TNR à
  rejouer, circuit de gestion des anomalies.
- **Livrables** : stratégie, plan, cahier de recette, jeux de données, matrice de traçabilité complète.
- **Avec qui** : testeurs, métier (recette utilisateur), MOE (livraisons, environnement), exploitation.
- **Fini quand** : critères d'entrée atteints (build livré, environnement disponible, données prêtes).
- **Pièges** : découvrir le jour J que l'environnement n'a pas de données ; pas de TNR prévus.

## 6. Exécution de la recette

- **Activités** : exécution, qualification et suivi des anomalies, points anomalies quotidiens pendant
  la campagne, reporting d'avancement, retests, TNR.
- **Livrables** : fiches d'anomalie, rapport d'avancement quotidien/hebdo, rapport de campagne.
- **Fini quand** : critères de sortie atteints ou dérogation décidée par la bonne instance.
- **Pièges** : reporter un % de cas passés sans parler des bloquants ; laisser la MOE requalifier seule
  la sévérité des anomalies.

## 7. Go/no-go et MEP

- **Activités** : bilan de recette, liste des anomalies résiduelles et contournements, plan de MEP, plan
  de retour arrière, communication utilisateurs, plan de vérification post-MEP.
- **Livrables** : PV de recette (avec ou sans réserves), dossier de go/no-go, plan de MEP.
- **Avec qui** : sponsor/décideur, chef de projet, métier, MOE, exploitation, support.
- **Pièges** : go « parce que la date est fixée » sans écrire les réserves ; pas de plan de retour arrière.

## 8. Après MEP

- Vérifications en production (checklist post-MEP), hypercare (support renforcé 1 à 4 semaines),
  suivi des incidents, VSR (vérification de service régulier), bilan projet / rétrospective.
- Conduite du changement : voir `pilotage-risques-changement.md`.

## 9. Fin de mission

- **Passation** : document de passation (contexte, acteurs, sujets en cours, points de vigilance, où
  sont les documents, accès), 2-3 sessions de transfert, dernière semaine en binôme si possible.
- **Capitalisation** : fiche mission pour le dossier de compétences (via `ba-fonctionnel`), 3 réalisations
  STAR mises à jour, demande de recommandation au manager.
- **Pièges** : partir en laissant des actions sans porteur ; ne pas mettre à jour son dossier à chaud.

## 10. Agile vs Cycle en V : correspondances

| Besoin | Cycle en V | Agile (Scrum) |
|---|---|---|
| Exprimer le besoin | EDB | Vision produit, epics |
| Spécifier | SFG / SFD | User stories + critères d'acceptation (Gherkin) |
| Valider la spéc | Validation formelle du document | Definition of Ready, refinement |
| Planifier | Planning projet, lots | Roadmap, sprint planning |
| Suivre | Comité de suivi | Daily, burndown, sprint review |
| Tester | Recette en fin de cycle | Tests dans le sprint + recette métier en review |
| Valider | PV de recette | Definition of Done + acceptation PO |
| S'améliorer | Bilan de projet | Rétrospective à chaque sprint |

En **hybride** (fréquent en banque) : cadrage et gouvernance en V, réalisation en sprints, recette
d'intégration et MEP en V. Le BA fait le pont : il traduit les epics en lots et les sprints en jalons COPIL.

## 11. Routine hebdomadaire du BA

**Lundi (30 min) — préparer la semaine**
- Relire le journal : actions en retard, échéances de la semaine.
- 3 priorités de la semaine (pas 10).
- Préparer les ODJ des réunions que j'anime ; envoyer les relances.

**Chaque jour (10 min)** : noter décisions et actions dans le journal le jour même ; CR des réunions de la
veille envoyés avant midi.

**Vendredi (30 min) — bilan**
- Journal à jour (fait / reporté / nouveau).
- Point hebdo au chef de projet (5 lignes : fait, prévu, risques, besoins).
- Auto-évaluation posture (grille dans `savoir-faire-savoir-etre.md`).
