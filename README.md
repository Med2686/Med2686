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

## caveman

Skills [JuliusBrussee/caveman](https://github.com/JuliusBrussee/caveman) (licence Apache-2.0). Seuls les
skills et les agents `cavecrew-*` sont copiés, pas le reste du dépôt (proxy, engine, CLI…).

| Emplacement | Contenu |
| --- | --- |
| `.claude/skills/caveman*`, `cavecrew`, `investigate-first`, `lean-build`, `migration`, `safe-refactor`, `surgical-patch`, `verify-and-stop` | Les 20 skills. La liste et la version copiée sont dans `.claude/skills/caveman/UPSTREAM`. |
| `.claude/agents/cavecrew-*.md` | Les 3 sous-agents utilisés par le skill `cavecrew`. |
| `scripts/update-caveman.sh` | Met à jour skills et agents (`scripts/update-caveman.sh [ref]`). |

| Skills | Fonctionnent ici ? |
| --- | --- |
| `caveman`, `caveman-help`, `caveman-commit`, `caveman-review`, `caveman-compress` (Python 3), `caveman-explore`, `cavecrew`, `investigate-first`, `lean-build`, `migration`, `safe-refactor`, `surgical-patch`, `verify-and-stop` | Oui, autonomes. |
| `caveman-stats` | Partiellement : le rapport précis dépend de hooks caveman non installés. |
| `caveman-setup`, `caveman-discover`, `caveman-evidence-review`, `caveman-manage`, `caveman-optimize`, `caveman-learn` | Non sans compte/outils Caveman Cloud ou CLI caveman. |

Activation du mode compressé : `/caveman` (niveaux `lite`, `full`, `ultra`), arrêt : « stop caveman ».
Les documents, commits et messages destinés à d'autres personnes restent rédigés normalement.

## brand-motion-design

Skill [ouerf-man/brand-motion-design-skill](https://github.com/ouerf-man/brand-motion-design-skill) (licence MIT) :
crée un film motion design de marque (Reel, TikTok, vidéo de lancement…) en code avec HyperFrames et Three.js.

| Emplacement | Contenu |
| --- | --- |
| `.claude/skills/brand-motion-design/` | Le skill, ses scripts et modèles, avec `LICENSE` et la version copiée dans `UPSTREAM`. |
| `scripts/update-brand-motion-design.sh` | Met à jour le skill (`scripts/update-brand-motion-design.sh [ref]`). |

Prérequis : Node.js 22+, FFmpeg, [uv](https://docs.astral.sh/uv/) ; HyperFrames est installé par projet
(`npx hyperframes init`). Utilisation : demander par exemple « Fais un Reel de 20 secondes pour cette marque ».
Les vidéos sont générées dans `videos/`.
