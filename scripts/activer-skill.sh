#!/usr/bin/env bash
# Active un skill du catalogue : le copie dans .claude/skills/ (pris en compte
# à la prochaine session Claude Code).
#
# Usage : scripts/activer-skill.sh <nom>
set -euo pipefail

NOM="${1:?Usage : scripts/activer-skill.sh <nom>}"
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
DEST="$ROOT/.claude/skills/$NOM"

mapfile -t TROUVES < <(find "$ROOT/catalogue" -mindepth 2 -maxdepth 3 -type d -name "$NOM" \
  -exec test -f '{}/SKILL.md' ';' -print)
if [[ ${#TROUVES[@]} -eq 0 ]]; then
  echo "Aucun skill « $NOM » dans catalogue/. Voir catalogue/README.md." >&2
  exit 1
fi
if [[ -e "$DEST" ]]; then
  echo "« $NOM » est déjà dans .claude/skills/." >&2
  exit 1
fi

cp -R "${TROUVES[0]}" "$DEST"
# Marqueur : permet à desactiver-skill.sh de ne retirer que ce qui vient du catalogue.
echo "${TROUVES[0]#"$ROOT/"}" > "$DEST/.depuis-catalogue"
echo "« $NOM » activé depuis ${TROUVES[0]#"$ROOT/"}. Ouvrez une nouvelle session pour qu'il soit chargé."
