# Med2686

## Mentor BA technico-fonctionnel

Skill Claude Code qui accompagne une mission AMOA / BA / testeur fonctionnel : il situe la mission, pose
les bonnes questions, puis donne la démarche (réunions, participants, comptes rendus et destinataires),
la posture à adopter, un exemple et la trame à remplir. Il tient un journal de mission.

| Emplacement | Contenu |
| --- | --- |
| `.claude/skills/mentor-ba-technico-fonctionnel/` | Le skill et ses fiches de référence |
| `.claude/commands/mentor.md` | La commande `/mentor` |
| `.claude/hooks/rappel-mission.py` | Rappel des échéances du journal à chaque ouverture de session |
| `mission/journal-de-mission.md` | Votre journal de mission (créé par le mentor au démarrage d'une mission) |

### Utilisation

```
/mentor                      → point de situation (préparation le lundi, bilan le vendredi)
/mentor <question>           → conseil sur une situation précise
/mentor <texte collé>        → analyse d'un mail, d'un CR, d'une spec…
```

Sans commande, il suffit de parler de sa mission : le skill se déclenche seul.
Pour produire le document Word/Excel final, le mentor s'appuie sur le skill `ba-fonctionnel`.

## watermarks-remover

Copie complète de [guillaumemeyer/watermarks-remover](https://github.com/guillaumemeyer/watermarks-remover) (licence MIT).

| Emplacement | Contenu |
| --- | --- |
| `vendor/watermarks-remover/` | Code complet du projet (sans son historique Git). La version copiée est notée dans `UPSTREAM`. |
| `.claude/skills/remove-ai-marks/` | Le skill Claude Code, chargé automatiquement dans toute session ouverte sur ce dépôt. |
| `scripts/update-watermarks-remover.sh` | Met à jour la copie et réinstalle le skill. |
| `.github/workflows/update-watermarks-remover.yml` | Vérifie chaque lundi s'il y a une nouvelle version et ouvre une PR le cas échéant. |

### Utiliser le skill

Le skill `remove-ai-marks` est un client léger : il ne fait qu'appeler le service HTTP du projet. Ce service doit tourner avant d'utiliser le skill :

```bash
cd vendor/watermarks-remover
make serve    # ou : python3 service/scripts/server.py --host 127.0.0.1 --port 8765
```

Puis, dans Claude Code : `/remove-ai-marks`.

### Mettre à jour

```bash
scripts/update-watermarks-remover.sh        # dernière version de main
scripts/update-watermarks-remover.sh v0.7.0 # ou une version précise
```

La mise à jour automatique ouvre une PR à relire avant fusion ; rien n'est fusionné sans vous.

## Skills tiers sélectionnés

Seuls les skills utiles au poste de BA et sans doublon avec ceux déjà présents sont copiés. La version
copiée est notée dans le fichier `UPSTREAM` de chaque skill.

| Skill | Source (licence) | Usage |
| --- | --- | --- |
| `meeting-insights-analyzer` | [ComposioHQ/awesome-claude-skills](https://github.com/ComposioHQ/awesome-claude-skills) (Apache-2.0) | Analyse vos transcriptions de réunion : temps de parole, interruptions, hésitations, évitement du conflit, qualité de l'écoute, avec des exemples cités et des formulations alternatives. |
| `intent-driven-development` | [affaan-m/ECC](https://github.com/affaan-m/ECC) (MIT) | Transforme une demande floue en critères d'acceptation observables (scénario, action, résultat attendu, effet interdit, mode de vérification). Relit une spec ou une US existante pour y trouver ce qui est ambigu ou invérifiable, et sépare les règles métier des faits techniques. |

Déposez les transcriptions (Teams, Zoom : .vtt, .txt, .docx) dans `mission/transcriptions/`. Ce dossier est
exclu de Git, car il contient des données client.

Les autres skills de ces dépôts sont rangés, inactifs, dans le catalogue (section suivante).

Pour ajouter un skill à cette sélection maintenue, ajoutez une ligne au tableau `SELECTION` du script, puis lancez :

```bash
scripts/update-selected-skills.sh
```

## Catalogue de skills inactifs

`catalogue/` contient les quelque 360 autres skills d'awesome-claude-skills, d'ECC et de mattpocock/skills
(hors `grill-me` et `grilling`, déjà installés), rangés en 14 catégories. Il y a aussi un lot de 832 intégrations Composio. Voir l'index : [`catalogue/README.md`](catalogue/README.md).

**Claude Code ne les charge pas** : seuls ceux de `.claude/skills/` le sont. Les charger tous noierait le
mentor et `ba-fonctionnel` parmi des centaines de skills de développement.

| Catégorie | Intérêt pour un BA |
| --- | --- |
| `01-ba-specs-recette-produit` | Élevé : cadrage produit, arbitrages, revue de parcours, décisions |
| `02-redaction-communication`, `03-documents-bureautique`, `04-recherche-veille-analyse` | Moyen : à piocher selon le besoin |
| `05` à `06` (business, secteurs) | Ponctuel : selon le secteur de la mission |
| `07` à `14` (développement, infra, sécurité, agents IA, design, intégrations) | Faible : outils de développeur |

```bash
scripts/activer-skill.sh council       # rend le skill actif (nouvelle session nécessaire)
scripts/desactiver-skill.sh council    # le remet au catalogue
scripts/update-catalogue.py            # met à jour le catalogue depuis les dépôts sources
```

Pour changer un skill de catégorie, modifiez `catalogue/categories.tsv`, puis relancez `update-catalogue.py`.
