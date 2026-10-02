#!/usr/bin/env python3
"""Construit catalogue/ : les skills tiers non actifs, rangés par catégorie.

Les skills du catalogue ne sont PAS chargés par Claude Code (seul .claude/skills/
l'est). Pour en activer un : scripts/activer-skill.sh <nom>.

La catégorie de chaque skill est lue dans catalogue/categories.tsv ; un skill
absent de ce fichier atterrit dans 99-a-classer. Les skills déjà actifs
(.claude/skills/) sont exclus.

Usage : scripts/update-catalogue.py
"""
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

# nom court, dépôt, branche, licence, dossiers contenant des skills
SOURCES = [
    ("awesome-claude-skills", "https://github.com/ComposioHQ/awesome-claude-skills",
     "master", "Apache-2.0", [".", "document-skills"]),
    ("ECC", "https://github.com/affaan-m/ECC", "main", "MIT", ["skills"]),
]
# Pas des skills utilisables : modèle vide, plugin sans SKILL.md.
IGNORES = {"template-skill", "connect-apps-plugin"}
# Lot de ~830 skills quasi identiques : copié d'un bloc, sans détail dans l'index.
LOTS = {"composio-skills"}
A_CLASSER = "99-a-classer"

ROOT = Path(__file__).resolve().parent.parent
CATALOGUE = ROOT / "catalogue"
ACTIFS = {p.name for p in (ROOT / ".claude" / "skills").iterdir() if p.is_dir()}


def lire_categories():
    cats = {}
    for ligne in (CATALOGUE / "categories.tsv").read_text().splitlines():
        if ligne.strip() and not ligne.startswith("#"):
            nom, cat = ligne.split("\t")
            cats[nom] = cat
    return cats


def description(skill_md):
    texte = skill_md.read_text(errors="replace")
    m = re.search(r"^description:\s*[\"']?(.*?)[\"']?\s*$", texte, re.M)
    d = m.group(1) if m else ""
    return d if len(d) <= 160 else d[:157].rstrip() + "…"


def main():
    cats = lire_categories()
    with tempfile.TemporaryDirectory() as tmp:
        trouves = {}  # nom -> (dossier source, nom de source)
        provenance = []
        for court, url, ref, licence, dossiers in SOURCES:
            clone = Path(tmp) / court
            subprocess.run(["git", "clone", "--quiet", "--depth", "1", "--branch", ref,
                            url, str(clone)], check=True)
            commit = subprocess.run(["git", "-C", str(clone), "rev-parse", "HEAD"],
                                    check=True, capture_output=True, text=True).stdout.strip()
            provenance.append(f"| {court} | [{url}]({url}/tree/{commit}) | `{commit[:12]}` | {licence} |")
            for d in dossiers:
                for sk in sorted((clone / d).iterdir()):
                    if not sk.is_dir() or sk.name in IGNORES or sk.name in ACTIFS:
                        continue
                    if not (sk / "SKILL.md").is_file() and sk.name not in LOTS:
                        continue
                    if sk.name in trouves:
                        sys.exit(f"Nom de skill en double entre sources : {sk.name}")
                    trouves[sk.name] = (sk, court)

        for p in CATALOGUE.iterdir():
            if p.is_dir():
                shutil.rmtree(p)
        index = {}
        for nom, (src, court) in sorted(trouves.items()):
            cat = cats.get(nom, A_CLASSER)
            shutil.copytree(src, CATALOGUE / cat / nom, ignore=shutil.ignore_patterns(".git"))
            if nom in LOTS:
                n = sum(1 for p in src.iterdir() if (p / "SKILL.md").is_file())
                desc = f"Lot de {n} skills « <app>-automation » ; nécessitent un compte et une clé API Composio."
            else:
                desc = description(src / "SKILL.md")
            index.setdefault(cat, []).append((nom, court, desc.replace("|", "\\|")))

    inconnus = sorted(set(cats) - set(trouves))
    lignes = [
        "# Catalogue de skills (inactifs)",
        "",
        "Skills tiers rangés par catégorie. **Ils ne sont pas chargés par Claude Code** : seuls ceux de",
        "`.claude/skills/` le sont. Ce rangement évite que des centaines de skills de développement",
        "parasitent le déclenchement du mentor et de `ba-fonctionnel`.",
        "",
        "```bash",
        "scripts/activer-skill.sh <nom>      # copie le skill dans .claude/skills/ (actif à la session suivante)",
        "scripts/desactiver-skill.sh <nom>   # le retire de .claude/skills/",
        "scripts/update-catalogue.py         # met à jour le catalogue depuis les dépôts sources",
        "```",
        "",
        "Pour changer un skill de catégorie : modifiez `categories.tsv`, puis relancez `update-catalogue.py`.",
        "Fichier généré : ne pas modifier à la main.",
        "",
        "## Sources",
        "",
        "| Source | Dépôt | Commit | Licence |",
        "| --- | --- | --- | --- |",
        *provenance,
        "",
        "## Sommaire",
        "",
    ]
    for cat in sorted(index):
        lignes.append(f"- [{cat}](#{cat}) ({len(index[cat])})")
    for cat in sorted(index):
        lignes += ["", f"## {cat}", "", "| Skill | Source | Description |", "| --- | --- | --- |"]
        lignes += [f"| `{n}` | {s} | {d} |" for n, s, d in index[cat]]
    if inconnus:
        lignes += ["", "## Entrées de categories.tsv sans skill correspondant", ""]
        lignes += [f"- `{n}`" for n in inconnus]
    (CATALOGUE / "README.md").write_text("\n".join(lignes) + "\n")

    total = sum(len(v) for v in index.values())
    print(f"{total} skills rangés dans {len(index)} catégories.")
    if A_CLASSER in index:
        print(f"À classer : {', '.join(n for n, _, _ in index[A_CLASSER])}")


if __name__ == "__main__":
    main()
