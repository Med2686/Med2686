#!/usr/bin/env bash
# Installe / met à jour tous les skills de caveman dans .claude/skills/ et les
# agents cavecrew-* (utilisés par le skill cavecrew) dans .claude/agents/.
# Seuls ces dossiers sont copiés : le reste du dépôt (proxy, engine, CLI, SDK…
# ~23 Mo) n'est pas utile aux skills.
#
# Usage : scripts/update-caveman.sh [ref]   (ref par défaut : main)
set -euo pipefail

UPSTREAM_URL="https://github.com/JuliusBrussee/caveman"
REF="${1:-main}"

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SKILLS="$ROOT/.claude/skills"
AGENTS="$ROOT/.claude/agents"
MANIFEST="$SKILLS/caveman/UPSTREAM"
TMP="$(mktemp -d)"
trap 'rm -rf "$TMP"' EXIT

git clone --quiet --depth 1 --branch "$REF" "$UPSTREAM_URL" "$TMP/src"
COMMIT="$(git -C "$TMP/src" rev-parse HEAD)"
DATE="$(git -C "$TMP/src" log -1 --format=%cI)"

if [[ -f "$MANIFEST" ]] && grep -q "^commit: $COMMIT$" "$MANIFEST"; then
  echo "Déjà à jour ($COMMIT)."
  exit 0
fi

# Supprime les éléments installés par la version précédente (liste dans UPSTREAM).
if [[ -f "$MANIFEST" ]]; then
  sed -n 's/^skill: //p' "$MANIFEST" | while read -r s; do rm -rf "${SKILLS:?}/$s"; done
  sed -n 's/^agent: //p' "$MANIFEST" | while read -r a; do rm -f "$AGENTS/$a"; done
fi

mkdir -p "$SKILLS" "$AGENTS"
installed_skills=()
for dir in "$TMP/src/skills"/*/; do
  name="$(basename "$dir")"
  [[ -f "$dir/SKILL.md" ]] || continue   # generated/, native/ : pas des skills
  rm -rf "${SKILLS:?}/$name"
  cp -r "$dir" "$SKILLS/$name"
  installed_skills+=("$name")
done
installed_agents=()
for f in "$TMP/src/agents"/cavecrew-*.md; do
  cp "$f" "$AGENTS/"
  installed_agents+=("$(basename "$f")")
done

# Licence Apache-2.0 : le texte et le NOTICE doivent accompagner la copie.
cp "$TMP/src/LICENSE" "$TMP/src/NOTICE" "$SKILLS/caveman/"
{
  echo "url: $UPSTREAM_URL"
  echo "ref: $REF"
  echo "commit: $COMMIT"
  echo "date: $DATE"
  printf 'skill: %s\n' "${installed_skills[@]}"
  printf 'agent: %s\n' "${installed_agents[@]}"
} > "$MANIFEST"

echo "caveman mis à jour vers $COMMIT ($DATE) : ${#installed_skills[@]} skills, ${#installed_agents[@]} agents."
