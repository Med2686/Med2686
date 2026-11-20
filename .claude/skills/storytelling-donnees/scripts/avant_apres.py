#!/usr/bin/env python3
"""Avant / après sur les données du bac à sable de recette : le même graphique, d'abord « par défaut »,
puis réécrit avec les leçons de Storytelling with Data (contexte, désencombrement, focus, titre d'action).
Usage : python3 avant_apres.py [dossier_de_sortie]      (nécessite matplotlib)"""
import sqlite3, sys, pathlib
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

here = pathlib.Path(__file__).resolve().parent
out = pathlib.Path(sys.argv[1]) if len(sys.argv) > 1 else here.parent / "assets"
out.mkdir(parents=True, exist_ok=True)

db = sqlite3.connect(":memory:")
db.executescript((here.parent.parent / "maitre-sql" / "assets" / "bac-a-sable.sql").read_text(encoding="utf-8"))
rows = db.execute("""SELECT ca.environnement, ct.resultat, COUNT(*) FROM cas_test ct
                     JOIN campagnes ca ON ca.id = ct.campagne_id GROUP BY 1, 2""").fetchall()
envs = ["REC1", "REC2", "PREPROD"]
res = ["OK", "KO", "Bloqué", "Non exécuté"]
n = {(e, r): 0 for e in envs for r in res}
for e, r, c in rows: n[(e, r)] = c
tot = {e: sum(n[(e, r)] for r in res) for e in envs}

# ---------------- AVANT : réglages par défaut, légende, quadrillage, couleurs arc-en-ciel ----------------
fig, ax = plt.subplots(figsize=(8, 4.6))
bottom = [0] * 3
for r, col in zip(res, ["#1f77b4", "#ff7f0e", "#2ca02c", "#d62728"]):
    vals = [n[(e, r)] for e in envs]
    ax.bar(envs, vals, bottom=bottom, label=r, color=col)
    bottom = [b + v for b, v in zip(bottom, vals)]
ax.set_title("Cas de test par environnement et par résultat")
ax.set_xlabel("Environnement"); ax.set_ylabel("Nombre de cas")
ax.grid(True); ax.legend()
fig.tight_layout(); fig.savefig(out / "avant.png", dpi=130); plt.close(fig)

# ---------------- APRÈS : un message, un accent, étiquettes directes ----------------
GRIS, GRIS_FONCE, ACCENT, TEXTE, FOND = "#c9ced4", "#7d8793", "#c2410c", "#2b3138", "#ffffff"
fig, ax = plt.subplots(figsize=(8, 4.6)); fig.patch.set_facecolor(FOND)
y = list(range(len(envs)))[::-1]
for yi, e in zip(y, envs):
    left = 0
    for r in res:
        v = n[(e, r)]
        if not v: continue
        if r == "Non exécuté": col = ACCENT if e == "PREPROD" else GRIS_FONCE
        elif r == "OK": col = GRIS
        else: col = GRIS_FONCE
        ax.barh(yi, v, left=left, color=col, height=0.55, edgecolor=FOND, linewidth=1.5)
        if v >= 1:
            ax.text(left + v / 2, yi, str(v), ha="center", va="center", color="white" if col != GRIS else TEXTE, fontsize=10)
        left += v
    ax.text(-0.4, yi, e, ha="right", va="center", fontsize=11, color=TEXTE)
# étiquettes directes des catégories, une seule fois, sous la barre qui contient les quatre résultats
left = 0
for r in res:
    ax.text(left + n[("PREPROD", r)] / 2, y[-1] - 0.5, r, ha="center", va="top", fontsize=9, color=GRIS_FONCE)
    left += n[("PREPROD", r)]
ax.set_xlim(-3.2, 16); ax.set_ylim(-1.1, 2.3)
for s in ax.spines.values(): s.set_visible(False)
ax.set_xticks([]); ax.set_yticks([])
fig.text(0.04, 0.93, "En préproduction, 6 cas de test sur 15 ne sont pas encore exécutés", fontsize=14, fontweight="bold", color=TEXTE, ha="left")
fig.text(0.04, 0.865, "Recommandation : ne pas prononcer le Go avant la fin de l'exécution des cas restants.", fontsize=10.5, color=GRIS_FONCE, ha="left")
fig.text(0.04, 0.03, "Source : campagnes de recette REC1, REC2 et PREPROD (données fictives). Chaque barre = 15 cas.", fontsize=8.5, color=GRIS_FONCE, ha="left")
fig.subplots_adjust(top=0.82, bottom=0.10, left=0.04, right=0.98)
fig.savefig(out / "apres.png", dpi=130); plt.close(fig)
print("écrit :", out / "avant.png", "et", out / "apres.png")
