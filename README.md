# Med2686

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
