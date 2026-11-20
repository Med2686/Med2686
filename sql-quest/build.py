#!/usr/bin/env python3
"""Régénère seed.js (base d'entraînement) et vendor/sql-wasm-base64.js (moteur SQLite embarqué).
Ces deux fichiers permettent d'ouvrir index.html directement (file://), sans serveur ni internet.
Usage : python3 build.py [chemin/vers/sql-wasm.wasm]   (le .wasm est requis seulement la 1re fois)"""
import base64, json, pathlib, sys
here = pathlib.Path(__file__).resolve().parent
seed = (here.parent / ".claude/skills/maitre-sql/assets/bac-a-sable.sql").read_text(encoding="utf-8")
(here / "seed.js").write_text("window.SEED_SQL = " + json.dumps(seed, ensure_ascii=False) + ";\n", encoding="utf-8")
out = here / "vendor/sql-wasm-base64.js"
if len(sys.argv) > 1:
    b64 = base64.b64encode(pathlib.Path(sys.argv[1]).read_bytes()).decode()
    out.write_text('window.SQLJS_WASM_B64 = "' + b64 + '";\n', encoding="utf-8")
elif not out.exists():
    sys.exit("Premier lancement : fournir le chemin de sql-wasm.wasm (npm i sql.js@1.10.3)")
print("seed.js et", out.name, "à jour")
