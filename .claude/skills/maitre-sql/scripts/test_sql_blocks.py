#!/usr/bin/env python3
"""Exécute les blocs ```sql marqués '-- [test]' des fichiers .md et vérifie '-- attendu: N'."""
import re, sqlite3, sys, pathlib
root = pathlib.Path(__file__).resolve().parent.parent
db = sqlite3.connect(":memory:")
db.executescript((root / "assets" / "bac-a-sable.sql").read_text(encoding="utf-8"))
bad = total = 0
for md in sorted((root / "references").glob("*.md")):
    for m in re.finditer(r"```sql\n(.*?)```", md.read_text(encoding="utf-8"), re.S):
        sql = m.group(1)
        if "-- [test]" not in sql: continue
        total += 1
        exp = re.search(r"attendu: (\d+)", sql)
        try:
            n = len(db.execute(sql).fetchall())
        except Exception as e:
            bad += 1; print(f"ERREUR {md.name}: {e}\n{sql[:200]}"); continue
        if exp and int(exp.group(1)) != n:
            bad += 1; print(f"ECART {md.name}: attendu {exp.group(1)}, obtenu {n}\n{sql[:200]}")
print(f"{total} requêtes testées, {bad} en échec")
sys.exit(1 if bad else 0)
