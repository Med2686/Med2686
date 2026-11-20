#!/usr/bin/env python3
"""Régénère seed.js (base d'entraînement embarquée) à partir du bac à sable du skill maitre-sql.
Usage : python3 build.py"""
import json, pathlib
here = pathlib.Path(__file__).resolve().parent
seed = (here.parent / ".claude/skills/maitre-sql/assets/bac-a-sable.sql").read_text(encoding="utf-8")
(here / "seed.js").write_text("window.SEED_SQL = " + json.dumps(seed, ensure_ascii=False) + ";\n", encoding="utf-8")
print("seed.js à jour")
