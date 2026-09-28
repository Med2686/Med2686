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
