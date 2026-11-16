#!/usr/bin/env python3
"""Rappel de début de session : actions et réunions du journal de mission.

Lit mission/journal-de-mission.md et affiche les actions non terminées en retard
ou dues dans les 7 prochains jours, ainsi que les réunions à venir. Silencieux
s'il n'y a pas de journal ou rien à signaler. Stdlib uniquement.
"""

import json
import os
import re
import sys
from datetime import date, timedelta
from pathlib import Path

HORIZON_JOURS = 7
STATUTS_CLOS = {"fait", "abandonné", "abandonne", "clos", "fermé", "ferme", "terminé", "termine"}
DATE_RE = re.compile(r"\b(\d{4}-\d{2}-\d{2})\b")


def sections(texte):
    """Découpe le markdown en {titre de section ## : lignes}."""
    courant, res = None, {}
    for ligne in texte.splitlines():
        if ligne.startswith("## "):
            courant = ligne[3:].strip().lower()
            res[courant] = []
        elif courant is not None:
            res[courant].append(ligne)
    return res


def lignes_tableau(lignes):
    for ligne in lignes:
        if not ligne.strip().startswith("|") or set(ligne.strip()) <= set("|-: "):
            continue
        yield [c.strip() for c in ligne.strip().strip("|").split("|")]


def premiere_date(cellules):
    for cellule in cellules:
        m = DATE_RE.search(cellule)
        if m:
            try:
                return date.fromisoformat(m.group(1))
            except ValueError:
                return None
    return None


def main():
    racine = Path(os.environ.get("CLAUDE_PROJECT_DIR", "."))
    journal = racine / "mission" / "journal-de-mission.md"
    if not journal.is_file():
        return 0

    aujourd_hui = date.today()
    limite = aujourd_hui + timedelta(days=HORIZON_JOURS)
    secs = sections(journal.read_text(encoding="utf-8"))

    retard, a_venir = [], []
    for cells in lignes_tableau(secs.get("actions", [])):
        if cells and cells[0].lower() == "id":
            continue
        if cells and cells[-1].lower() in STATUTS_CLOS:
            continue
        echeance = premiere_date(cells)
        if echeance is None:
            continue
        libelle = " – ".join(c for c in cells[:3] if c)
        if echeance < aujourd_hui:
            retard.append(f"{echeance} {libelle}")
        elif echeance <= limite:
            a_venir.append(f"{echeance} {libelle}")

    reunions = []
    for cells in lignes_tableau(secs.get("prochaines réunions", [])):
        quand = premiere_date(cells)
        if quand and aujourd_hui <= quand <= limite:
            reunions.append(f"{quand} {' – '.join(c for c in cells[1:3] if c)}")

    if not (retard or a_venir or reunions):
        return 0

    parties = ["Journal de mission :"]
    if retard:
        parties.append(f"{len(retard)} action(s) en retard : " + " ; ".join(sorted(retard)))
    if a_venir:
        parties.append(f"{len(a_venir)} action(s) sous {HORIZON_JOURS} jours : " + " ; ".join(sorted(a_venir)))
    if reunions:
        parties.append("Réunions à venir : " + " ; ".join(sorted(reunions)))
    parties.append("Tapez /mentor pour faire le point.")
    message = "\n".join(parties)

    print(json.dumps({
        "systemMessage": message,
        "hookSpecificOutput": {
            "hookEventName": "SessionStart",
            "additionalContext": message + "\nSi l'utilisateur parle de sa mission, signale ces échéances en tête de réponse (skill mentor-ba-technico-fonctionnel).",
        },
    }, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
