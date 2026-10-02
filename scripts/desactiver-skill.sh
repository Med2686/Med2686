#!/usr/bin/env bash
# Désactive un skill activé depuis le catalogue (le retire de .claude/skills/).
# Les skills installés autrement (mentor, update-selected-skills.sh…) sont protégés.
#
# Usage : scripts/desactiver-skill.sh <nom>
set -euo pipefail

NOM="${1:?Usage : scripts/desactiver-skill.sh <nom>}"
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
DEST="$ROOT/.claude/skills/$NOM"

if [[ ! -f "$DEST/.depuis-catalogue" ]]; then
  echo "« $NOM » n'a pas été activé depuis le catalogue : rien n'est supprimé." >&2
  exit 1
fi
rm -rf "$DEST"
echo "« $NOM » désactivé (il reste disponible dans catalogue/)."
