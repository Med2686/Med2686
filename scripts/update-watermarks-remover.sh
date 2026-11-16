#!/usr/bin/env bash
# Met à jour la copie de watermarks-remover (vendor/) et réinstalle le skill
# remove-ai-marks dans .claude/skills/ à partir de la dernière version amont.
#
# Usage : scripts/update-watermarks-remover.sh [ref]   (ref par défaut : main)
set -euo pipefail

UPSTREAM_URL="https://github.com/guillaumemeyer/watermarks-remover"
REF="${1:-main}"
SKILL="remove-ai-marks"

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
VENDOR="$ROOT/vendor/watermarks-remover"
TMP="$(mktemp -d)"
trap 'rm -rf "$TMP"' EXIT

git clone --quiet --depth 1 --branch "$REF" "$UPSTREAM_URL" "$TMP/src"
COMMIT="$(git -C "$TMP/src" rev-parse HEAD)"
DATE="$(git -C "$TMP/src" log -1 --format=%cI)"

if [[ -f "$VENDOR/UPSTREAM" ]] && grep -q "^commit: $COMMIT$" "$VENDOR/UPSTREAM"; then
  echo "Déjà à jour ($COMMIT)."
  exit 0
fi

rm -rf "$TMP/src/.git"
# Le .gitignore amont refuse tout par défaut (/*) : dans ce dépôt il exclurait
# l'installeur et les skills eux-mêmes. On le garde, renommé, pour référence.
mv "$TMP/src/.gitignore" "$TMP/src/.gitignore.upstream"
rm -rf "$VENDOR"
mkdir -p "$(dirname "$VENDOR")"
mv "$TMP/src" "$VENDOR"
cat > "$VENDOR/UPSTREAM" <<EOF
url: $UPSTREAM_URL
ref: $REF
commit: $COMMIT
date: $DATE
EOF

python3 "$VENDOR/install_skill.py" --skill "$SKILL" --target claude-project \
  --project-dir "$ROOT" --force
# L'installeur sauvegarde l'ancienne version à côté ; inutile dans un dépôt Git.
rm -rf "$ROOT/.claude/skills/$SKILL".backup.*

echo "watermarks-remover mis à jour vers $COMMIT ($DATE)."
