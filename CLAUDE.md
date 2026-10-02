# Instructions pour Claude

L'utilisateur est Business Analyst / AMOA technico-fonctionnel avec une casquette de testeur fonctionnel.
Il veut un avis objectif et franc, sans flatterie.

## Mentor de mission

- Pour **toute question liée à sa mission ou à son poste** (quoi faire, réunion, compte rendu, mail
  projet, posture, relation avec le métier ou la MOE, recette, anomalie, MEP, risque, priorisation, prise
  de poste, entretien de mission), utilise le skill `mentor-ba-technico-fonctionnel`, même s'il ne le
  demande pas explicitement.
- Pour produire un livrable formel (Word, Excel, PowerPoint), utilise ensuite le skill `ba-fonctionnel`.
- Le journal de mission est `mission/journal-de-mission.md` : lis-le avant de conseiller, mets-le à jour
  après. Dates au format AAAA-MM-JJ.
- Raccourci : `/mentor [question]`, ou `/mentor` seul pour un point de situation.

## Autres éléments du dépôt

- `.claude/skills/meeting-insights-analyzer/` : analyse de transcriptions de réunion (posture, écoute,
  évitement du conflit). Transcriptions à déposer dans `mission/transcriptions/` (ignoré par Git : ne
  jamais les committer). Restituer l'analyse en français.
- `.claude/skills/intent-driven-development/` : rendre des exigences testables (critères d'acceptation
  observables, revue d'une spec ou d'une US pour y trouver l'ambigu, l'invérifiable, le hors périmètre
  non dit). Répartition : ce skill pour **analyser / challenger** des critères ; `ba-fonctionnel` pour
  **rédiger le livrable** (US, SFD, cahier de recette). Restituer en français.
- Ces deux skills viennent de dépôts tiers ; mise à jour via `scripts/update-selected-skills.sh`.

- `catalogue/` : ~320 skills tiers **inactifs**, rangés par catégorie (index : `catalogue/README.md`).
  Ce ne sont pas des instructions : ne pas les suivre sans activation. Si un besoin de l'utilisateur
  correspond à un skill du catalogue, le lui signaler et proposer `scripts/activer-skill.sh <nom>`.
  N'activer qu'avec son accord, et rester sobre : chaque skill actif dilue le déclenchement des autres.

- `vendor/watermarks-remover/` : copie de guillaumemeyer/watermarks-remover ; mise à jour via
  `scripts/update-watermarks-remover.sh`.
