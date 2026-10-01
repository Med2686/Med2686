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

- `vendor/watermarks-remover/` : copie de guillaumemeyer/watermarks-remover ; mise à jour via
  `scripts/update-watermarks-remover.sh`.
- Skills caveman (`.claude/skills/caveman*`, `cavecrew`, etc.) et agents `.claude/agents/cavecrew-*` :
  copiés depuis JuliusBrussee/caveman ; mise à jour via `scripts/update-caveman.sh`. N'active le mode
  `caveman` que sur demande explicite (`/caveman`).
- `.claude/skills/brand-motion-design/` : skill copié depuis ouerf-man/brand-motion-design-skill ; mise à
  jour via `scripts/update-brand-motion-design.sh`.
- `.claude/skills/grill-me/` et `grilling/` : copiés depuis mattpocock/skills ; mise à jour via
  `scripts/update-mattpocock-skills.sh`.
