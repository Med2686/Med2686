#!/usr/bin/env bash
# Installe / met à jour le skill caveman dans .claude/skills/ à partir de la
# dernière version amont. Seul le dossier skills/caveman est copié : le reste du
# dépôt (proxy, engine, CLI, SDK… ~23 Mo) n'est pas utile au skill.
#
# Usage : scripts/update-caveman.sh [ref]   (ref par défaut : main)
set -euo pipefail

UPSTREAM_URL="https://github.com/JuliusBrussee/caveman"
REF="${1:-main}"

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
DEST="$ROOT/.claude/skills/caveman"
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
cp -r "$TMP/src/skills/caveman" "$DEST"
# Licence Apache-2.0 : le texte et le NOTICE doivent accompagner la copie.
cp "$TMP/src/LICENSE" "$TMP/src/NOTICE" "$DEST/"
cat > "$DEST/UPSTREAM" <<EOT
url: $UPSTREAM_URL
ref: $REF
path: skills/caveman
commit: $COMMIT
date: $DATE
EOT

echo "caveman mis à jour vers $COMMIT ($DATE)."
