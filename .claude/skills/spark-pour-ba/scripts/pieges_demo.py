#!/usr/bin/env python3
"""Démonstrations reproductibles des pièges de données en Spark (version locale). Prérequis : Java + pyspark.
Chaque piège affiche ce que Spark FAIT, pour qu'un testeur sache ce qu'il doit vérifier. Données fictives."""
import tempfile, os, pathlib
from spark_lab import get_spark
spark = get_spark(); spark.sparkContext.setLogLevel("OFF"); out = lambda t: print("\n== " + t)

out("1. Division par zéro et conversions implicites (mode ANSI désactivé par défaut)")
print("ansi =", spark.conf.get("spark.sql.ansi.enabled"))
print(spark.sql("SELECT 1/0 AS div0, 5 * '23' AS chaine_numerique, 5 * ' ' AS chaine_vide, cast('abc' AS int) AS cast_rate").collect())

out("2. Lecture d'un CSV avec une ligne corrompue : les 3 modes de lecture")
d = tempfile.mkdtemp(); p = os.path.join(d, "montants.csv")
pathlib.Path(p).write_text("id,montant\n1,100\n2,abc\n3,300\n", encoding="utf-8")
for mode in ["PERMISSIVE", "DROPMALFORMED", "FAILFAST"]:
    try:
        df = spark.read.schema("id INT, montant INT").option("header", True).option("mode", mode).csv(p)
        print(f"{mode:14s} ->", [tuple(r) for r in df.collect()])
    except Exception as e:
        print(f"{mode:14s} -> ERREUR : {str(e).splitlines()[0][:90]}")

out("3. Même fichier sans schéma imposé : inferSchema devine les types")
df = spark.read.option("header", True).option("inferSchema", True).csv(p); df.printSchema()

out("4. Paresse : une transformation ne calcule rien, une action déclenche le travail")
df2 = spark.range(5_000_000).where("id % 2 = 0").groupBy().count()
print("après transformation : type =", type(df2).__name__, "(aucun calcul)"); print("après action : résultat =", df2.collect()[0][0])

out("5. NULL dans une comparaison et dans NOT IN")
print(spark.sql("SELECT NULL = NULL AS egal_null, NULL <=> NULL AS egal_null_safe, 1 NOT IN (2, NULL) AS not_in_null").collect())

out("6. Ordre des lignes non garanti sans ORDER BY (résultat non reproductible d'une exécution à l'autre sur de gros volumes)")
print("Spark ne promet aucun ordre : toujours trier explicitement avant de comparer ou de présenter.")
spark.stop()
