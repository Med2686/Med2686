#!/usr/bin/env python3
"""Laboratoire Spark local : charge la base de recette fictive (skill maitre-sql) comme vues Spark SQL.
Prérequis : Java 8/11/17 + `pip install pyspark`. Usage :
    python3 spark_lab.py                 # ouvre une session de démonstration et affiche des exemples
    from spark_lab import get_spark, load_sandbox   # dans un autre script
Aucune donnée réelle : base 100 % fictive."""
import os, sqlite3, sys, pathlib
os.environ.setdefault("PYSPARK_PYTHON", sys.executable)
from pyspark.sql import SparkSession

SEED = pathlib.Path(__file__).resolve().parents[2] / "maitre-sql" / "assets" / "bac-a-sable.sql"
TABLES = ["clients", "comptes", "transactions", "batchs", "exigences", "campagnes", "cas_test", "anomalies"]

def get_spark(shuffle_partitions=4):
    s = (SparkSession.builder.master("local[2]").appName("spark-pour-ba")
         .config("spark.ui.enabled", "false").config("spark.sql.shuffle.partitions", str(shuffle_partitions)).getOrCreate())
    s.sparkContext.setLogLevel("ERROR")
    return s

def load_sandbox(spark):
    db = sqlite3.connect(":memory:"); db.executescript(SEED.read_text(encoding="utf-8"))
    for t in TABLES:
        cur = db.execute(f"SELECT * FROM {t}")
        spark.createDataFrame(cur.fetchall(), [d[0] for d in cur.description]).createOrReplaceTempView(t)
    return spark

if __name__ == "__main__":
    sp = load_sandbox(get_spark())
    print("Spark", sp.version, "| tables :", [t.name for t in sp.catalog.listTables()])
    sp.sql("SELECT severite, COUNT(*) AS nb FROM anomalies GROUP BY severite ORDER BY nb DESC").show()
