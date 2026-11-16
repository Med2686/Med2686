#!/usr/bin/env bash
# Installe / met à jour dans .claude/skills/ une sélection de skills issus de
# dépôts tiers. Seuls les skills listés dans SELECTION sont copiés ; le reste
# des dépôts est ignoré.
#
# Usage : scripts/update-selected-skills.sh
set -euo pipefail

# dépôt | branche | licence | skill (dossier relatif au dépôt)
SELECTION=(
  "https://github.com/ComposioHQ/awesome-claude-skills|master|Apache-2.0|meeting-insights-analyzer"
  "https://github.com/affaan-m/ECC|main|MIT|skills/intent-driven-development"
)

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
TMP="$(mktemp -d)"
trap 'rm -rf "$TMP"' EXIT

for ENTRY in "${SELECTION[@]}"; do
  IFS='|' read -r URL REF LICENCE PATH_IN_REPO <<<"$ENTRY"
  CLONE="$TMP/$(basename "$URL")-$REF"
  [[ -d "$CLONE" ]] || git clone --quiet --depth 1 --branch "$REF" "$URL" "$CLONE"
  COMMIT="$(git -C "$CLONE" rev-parse HEAD)"
  DATE="$(git -C "$CLONE" log -1 --format=%cI)"
  SKILL="$(basename "$PATH_IN_REPO")"
  SRC="$CLONE/$PATH_IN_REPO"
  DEST="$ROOT/.claude/skills/$SKILL"
  [[ -f "$SRC/SKILL.md" ]] || { echo "Skill introuvable en amont : $URL/$PATH_IN_REPO" >&2; exit 1; }
  rm -rf "$DEST"
  cp -R "$SRC" "$DEST"
  cat > "$DEST/UPSTREAM" <<EOT
url: $URL/tree/$COMMIT/$PATH_IN_REPO
ref: $REF
commit: $COMMIT
date: $DATE
licence: $LICENCE (licence du dépôt amont, sauf LICENSE propre au skill)
EOT
  echo "$SKILL installé ($COMMIT, $DATE)."
done
