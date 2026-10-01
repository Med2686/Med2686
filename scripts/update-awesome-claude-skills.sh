#!/usr/bin/env bash
# Installe / met à jour dans .claude/skills/ une sélection de skills issus de
# ComposioHQ/awesome-claude-skills. Seuls les skills listés dans SKILLS sont
# copiés : le reste du dépôt (dont les ~830 intégrations Composio) est ignoré.
#
# Usage : scripts/update-awesome-claude-skills.sh [ref]   (ref par défaut : master)
set -euo pipefail

UPSTREAM_URL="https://github.com/ComposioHQ/awesome-claude-skills"
REF="${1:-master}"
SKILLS=(
  meeting-insights-analyzer
)

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
TMP="$(mktemp -d)"
trap 'rm -rf "$TMP"' EXIT

git clone --quiet --depth 1 --branch "$REF" "$UPSTREAM_URL" "$TMP/src"
COMMIT="$(git -C "$TMP/src" rev-parse HEAD)"
DATE="$(git -C "$TMP/src" log -1 --format=%cI)"

for SKILL in "${SKILLS[@]}"; do
  SRC="$TMP/src/$SKILL"
  DEST="$ROOT/.claude/skills/$SKILL"
  [[ -f "$SRC/SKILL.md" ]] || { echo "Skill introuvable en amont : $SKILL" >&2; exit 1; }
  rm -rf "$DEST"
  cp -R "$SRC" "$DEST"
  cat > "$DEST/UPSTREAM" <<EOT
url: $UPSTREAM_URL/tree/$COMMIT/$SKILL
ref: $REF
commit: $COMMIT
date: $DATE
licence: Apache-2.0 (licence du dépôt amont, sauf LICENSE propre au skill)
EOT
  echo "$SKILL installé ($COMMIT, $DATE)."
done
