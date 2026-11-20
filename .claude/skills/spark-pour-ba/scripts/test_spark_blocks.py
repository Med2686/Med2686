#!/usr/bin/env python3
"""Exécute dans Spark les blocs ```sql marqués '-- [spark]' des .md de references/ et vérifie 'attendu: N'.
Prérequis : Java + pyspark. Usage : python3 test_spark_blocks.py   (une trentaine de secondes)"""
import re, sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from spark_lab import get_spark, load_sandbox
root = pathlib.Path(__file__).resolve().parent.parent
spark = load_sandbox(get_spark())
bad = total = 0
for md in sorted((root / "references").glob("*.md")):
    for m in re.finditer(r"```sql\n(.*?)```", md.read_text(encoding="utf-8"), re.S):
        sql = m.group(1)
        if "-- [spark]" not in sql: continue
        total += 1
        exp = re.search(r"attendu: (\d+)", sql)
        try:
            n = spark.sql(sql.strip().rstrip(";")).count()
        except Exception as e:
            bad += 1; print(f"ERREUR {md.name}: {str(e)[:200]}\n{sql[:160]}"); continue
        if exp and int(exp.group(1)) != n:
            bad += 1; print(f"ECART {md.name}: attendu {exp.group(1)}, obtenu {n}\n{sql[:160]}")
print(f"{total} requêtes Spark SQL testées, {bad} en échec")
sys.exit(1 if bad else 0)
