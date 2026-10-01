#!/usr/bin/env bash
# Installe / met à jour le skill brand-motion-design dans .claude/skills/ à
# partir de la dernière version amont (seul le dossier du skill est copié).
#
# Usage : scripts/update-brand-motion-design.sh [ref]   (ref par défaut : main)
set -euo pipefail

UPSTREAM_URL="https://github.com/ouerf-man/brand-motion-design-skill"
REF="${1:-main}"
SKILL_PATH="plugins/brand-motion-design/skills/brand-motion-design"

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
DEST="$ROOT/.claude/skills/brand-motion-design"
TMP="$(mktemp -d)"
trap 'rm -rf "$TMP"' EXIT

git clone --quiet --depth 1 --branch "$REF" "$UPSTREAM_URL" "$TMP/src"
COMMIT="$(git -C "$TMP/src" rev-parse HEAD)"
DATE="$(git -C "$TMP/src" log -1 --format=%cI)"

if [[ -f "$DEST/UPSTREAM" ]] && grep -q "^commit: $COMMIT$" "$DEST/UPSTREAM"; then
  echo "Déjà à jour ($COMMIT)."
  exit 0
fi

rm -rf "$DEST"
cp -r "$TMP/src/$SKILL_PATH" "$DEST"
# Licence MIT : le texte doit accompagner la copie.
cp "$TMP/src/LICENSE" "$DEST/"
cat > "$DEST/UPSTREAM" <<EOT
url: $UPSTREAM_URL
ref: $REF
path: $SKILL_PATH
commit: $COMMIT
date: $DATE
EOT

echo "brand-motion-design mis à jour vers $COMMIT ($DATE)."
