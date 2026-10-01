#!/usr/bin/env bash
# Installe / met à jour des skills de mattpocock/skills dans .claude/skills/.
# Par défaut : grill-me et grilling (grill-me ne fait qu'appeler grilling).
#
# Usage : scripts/update-mattpocock-skills.sh [skill...]
#         REF=<branche|tag> scripts/update-mattpocock-skills.sh   (défaut : main)
set -euo pipefail

UPSTREAM_URL="https://github.com/mattpocock/skills"
REF="${REF:-main}"
if [[ $# -gt 0 ]]; then WANTED=("$@"); else WANTED=(grill-me grilling); fi

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SKILLS="$ROOT/.claude/skills"
TMP="$(mktemp -d)"
trap 'rm -rf "$TMP"' EXIT

git clone --quiet --depth 1 --branch "$REF" "$UPSTREAM_URL" "$TMP/src"
COMMIT="$(git -C "$TMP/src" rev-parse HEAD)"
DATE="$(git -C "$TMP/src" log -1 --format=%cI)"

for name in "${WANTED[@]}"; do
  # Les skills amont sont rangés par catégorie : skills/<catégorie>/<skill>/SKILL.md
  src="$(find "$TMP/src/skills" -mindepth 2 -maxdepth 3 -type f -path "*/$name/SKILL.md" | head -1)"
  [[ -n "$src" ]] || { echo "Skill introuvable en amont : $name" >&2; exit 1; }
  src="$(dirname "$src")"
  dest="$SKILLS/$name"
  if [[ -f "$dest/UPSTREAM" ]] && grep -q "^commit: $COMMIT$" "$dest/UPSTREAM"; then
    echo "$name : déjà à jour ($COMMIT)."
    continue
  fi
  rm -rf "$dest"
  cp -r "$src" "$dest"
  rm -rf "$dest/agents"   # métadonnées pour Codex/OpenAI, inutiles à Claude Code
  cp "$TMP/src/LICENSE" "$dest/"   # licence MIT : le texte accompagne la copie
  cat > "$dest/UPSTREAM" <<EOT
url: $UPSTREAM_URL
ref: $REF
path: ${src#"$TMP/src/"}
commit: $COMMIT
date: $DATE
EOT
  echo "$name mis à jour vers $COMMIT ($DATE)."
done
