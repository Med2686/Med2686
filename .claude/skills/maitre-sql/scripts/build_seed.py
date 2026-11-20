#!/usr/bin/env python3
"""Génère assets/bac-a-sable.sql : base fictive de recette bancaire (SQLite), déterministe.
Anomalies de données plantées exprès (doublons, orphelins, écarts batch/solde, trous de couverture)."""
import random, sys
r = random.Random(42)
out = []
def q(v):
    if v is None: return "NULL"
    if isinstance(v, (int, float)): return repr(round(v, 2)) if isinstance(v, float) else str(v)
    return "'" + str(v).replace("'", "''") + "'"
def ins(t, cols, rows):
    for row in rows:
        out.append(f"INSERT INTO {t} ({', '.join(cols)}) VALUES ({', '.join(q(x) for x in row)});")

out.append("""-- Bac à sable SQL : recette bancaire fictive (SQLite). Données 100 % inventées.
-- Généré par scripts/build_seed.py — ne pas éditer à la main.
PRAGMA foreign_keys = OFF;
CREATE TABLE clients (id INTEGER PRIMARY KEY, nom TEXT, prenom TEXT, email TEXT, segment TEXT, ville TEXT, statut TEXT, date_creation TEXT);
CREATE TABLE comptes (id INTEGER PRIMARY KEY, client_id INTEGER, type TEXT, statut TEXT, date_ouverture TEXT, solde REAL);
CREATE TABLE batchs (id INTEGER PRIMARY KEY, nom TEXT, date_run TEXT, statut TEXT, nb_lus INTEGER, nb_ecrits INTEGER);
CREATE TABLE transactions (id INTEGER PRIMARY KEY, compte_id INTEGER, date_op TEXT, montant REAL, sens TEXT, canal TEXT, libelle TEXT, batch_id INTEGER);
CREATE TABLE exigences (id INTEGER PRIMARY KEY, code TEXT, titre TEXT, priorite TEXT, statut TEXT);
CREATE TABLE campagnes (id INTEGER PRIMARY KEY, nom TEXT, environnement TEXT, date_debut TEXT, date_fin TEXT);
CREATE TABLE cas_test (id INTEGER PRIMARY KEY, campagne_id INTEGER, exigence_id INTEGER, titre TEXT, resultat TEXT, testeur TEXT);
CREATE TABLE anomalies (id INTEGER PRIMARY KEY, cas_test_id INTEGER, campagne_id INTEGER, titre TEXT, severite TEXT, statut TEXT, assigne_a TEXT, environnement TEXT, date_creation TEXT, date_cloture TEXT);
""")

# --- clients
prenoms = ["Camille","Lucas","Emma","Hugo","Léa","Nathan","Chloé","Louis","Manon","Jules","Inès","Adam","Sarah","Paul","Zoé"]
noms = ["Martin","Bernard","Dubois","Thomas","Robert","Richard","Petit","Durand","Leroy","Moreau","Simon","Laurent","Lefebvre","Michel","Garcia","Roux"]
villes = ["Paris","Lyon","Lille","Nantes","Toulouse","Bordeaux","Strasbourg","Rennes"]
def ascii_(s): return s.lower().translate(str.maketrans("éèêëàâîïôöùûç", "eeeeaaiioouuc"))
clients, seen = [], set()
i = 0
while len(clients) < 60:
    i += 1
    p, n = prenoms[i % len(prenoms)], noms[(i * 7 + 3) % len(noms)]
    if (p, n) in seen: continue
    seen.add((p, n))
    cid = len(clients) + 1
    seg = r.choices(["Particulier","Pro","Entreprise"], [70,20,10])[0]
    st = r.choices(["actif","clos","suspendu"], [88,8,4])[0]
    dc = f"{r.randint(2019,2025)}-{r.randint(1,12):02d}-{r.randint(1,28):02d}"
    clients.append([cid, n, p, f"{ascii_(p)}.{ascii_(n)}@mail.fr", seg, r.choice(villes), st, dc])
# doublons plantés : 2 clients recréés avec le même email
clients[57][3] = clients[2][3]; clients[58][3] = clients[10][3]
ins("clients", ["id","nom","prenom","email","segment","ville","statut","date_creation"], clients)

# --- comptes
comptes = []
for c in clients:
    for k in range(r.choice([1,1,2])):
        t = "pro" if c[4] != "Particulier" else r.choice(["courant","courant","livret"])
        comptes.append([len(comptes)+1, c[0], t, "clos" if c[6] == "clos" else "ouvert", c[7], 0.0])
# 4 clients actifs dont l'unique compte est clos (cas "client actif sans compte ouvert")
nb_cpt = {}
for cp in comptes: nb_cpt[cp[1]] = nb_cpt.get(cp[1], 0) + 1
cibles = [c[0] for c in clients if c[6] == "actif" and nb_cpt.get(c[0]) == 1 and c[0] > 20][:4]
for cp in comptes:
    if cp[1] in cibles: cp[3] = "clos"
for cid in (901, 902, 903):  # comptes orphelins plantés
    comptes.append([len(comptes)+1, cid, "courant", "ouvert", "2024-05-02", 0.0])

# --- batchs (12 nuits) ; BATCH 5 = PARTIEL, BATCH 9 = KO
batchs = []
for b in range(1, 13):
    d = f"2026-11-{b+2:02d}"
    batchs.append([b, "BATCH_VIREMENTS_PERMANENTS", d, "OK", 0, 0])

# --- transactions
tx = []
libelles = ["Virement entrant","Paiement CB","Prélèvement SEPA","Retrait DAB","Frais de tenue de compte","Remboursement","Virement sortant"]
for c in comptes:
    first = True
    for _ in range(r.randint(5, 9)):
        d = f"2026-{r.choice([9,10,11])}-{r.randint(1,28):02d}"
        if first:
            sens, m, first = "C", round(r.uniform(1500, 5000), 2), False
        else:
            sens = r.choice(["C","D","D"]); m = round(r.uniform(5, 900), 2)
        tx.append([len(tx)+1, c[0], d, m, sens, r.choice(["agence","web","mobile"]), r.choice(libelles), None])
active = [c for c in comptes if c[3] == "ouvert"]
for b in batchs:
    n = 0 if b[0] == 9 else r.randint(10, 16)
    for _ in range(n):
        c = r.choice(active)
        tx.append([len(tx)+1, c[0], b[2], round(r.uniform(20, 600), 2), "D", "batch", "Virement permanent", b[0]])
    b[4] = n
    b[5] = n
    if b[0] == 5: b[3], b[4], b[5] = "PARTIEL", n + 5, n + 3    # annonce 3 écritures de trop
    if b[0] == 9: b[3], b[4], b[5] = "KO", 12, 7                # 7 écritures annoncées, 0 en base
ins("batchs", ["id","nom","date_run","statut","nb_lus","nb_ecrits"], batchs)
ins("transactions", ["id","compte_id","date_op","montant","sens","canal","libelle","batch_id"], tx)

# --- soldes cohérents, sauf 3 écarts plantés
bal = {}
for t in tx: bal[t[1]] = bal.get(t[1], 0) + (t[3] if t[4] == "C" else -t[3])
for c in comptes: c[5] = round(bal.get(c[0], 0), 2)
for cid in (4, 17, 33): comptes[cid-1][5] = round(comptes[cid-1][5] + 120.5, 2)
ins("comptes", ["id","client_id","type","statut","date_ouverture","solde"], comptes)

# --- exigences (18) ; 7, 12, 16 jamais couvertes
ex_titres = ["Saisie d'un virement SEPA","Contrôle de l'IBAN","Plafond de virement journalier","Virement instantané","Prélèvement SEPA : mandat","Rejet de prélèvement","Relevé de compte mensuel","Consultation du solde","Opposition carte","Clôture de compte","Changement d'adresse","Authentification forte","Alerte découvert","Calcul des frais de tenue","Export comptable","Archivage des opérations","Reprise de l'historique","Droit d'accès RGPD"]
prio = ["Must","Must","Should","Could"]
exigences = [[i+1, f"EXG-{i+1:03d}", t, prio[(i*3) % 4], r.choice(["validée","développée","recettée"])] for i, t in enumerate(ex_titres)]
ins("exigences", ["id","code","titre","priorite","statut"], exigences)

camp = [[1,"Recette Sprint 4 - Virements","REC1","2026-09-07","2026-09-25"],
        [2,"Recette Sprint 5 - Prélèvements SEPA","REC2","2026-10-12","2026-11-06"],
        [3,"Pré-production Release 2","PREPROD","2026-11-09","2026-11-27"]]
ins("campagnes", ["id","nom","environnement","date_debut","date_fin"], camp)

# --- cas de test (45) : résultats imposés par campagne
plan = {1: ["OK"]*11+["KO"]*3+["Bloqué"],
        2: ["OK"]*8+["KO"]*4+["Bloqué"]*2+["Non exécuté"],
        3: ["OK"]*5+["KO"]*3+["Bloqué"]+["Non exécuté"]*6}
scen = [("IBAN invalide saisi", ["IBAN invalide accepté sans message d'erreur","Message d'erreur IBAN affiché en anglais"]),
        ("Montant au plafond", ["Plafond journalier non contrôlé","Montant plafond tronqué à 2 chiffres"]),
        ("Compte clôturé", ["Virement possible vers un compte clos"]),
        ("Doublon de message", ["Doublon de virement non détecté"]),
        ("Rejet technique", ["Rejet sans code motif","Statut du virement non mis à jour"]),
        ("Droits insuffisants", ["Opérateur sans droit voit le bouton Valider"]),
        ("Reprise après incident", ["Reprise batch : opérations rejouées deux fois"]),
        ("Date d'exécution week-end", ["Date d'exécution décalée d'un jour"])]
testeurs = ["Camille R.","Karim B.","Julie M.","Nicolas D."]
couvrables = [e[0] for e in exigences if e[0] not in (7, 12, 16)]
cas = []
for cp in (1, 2, 3):
    res = plan[cp][:]; r.shuffle(res)
    for k, rs in enumerate(res):
        s = scen[(len(cas)) % len(scen)]
        eid = couvrables[(len(cas)*7) % len(couvrables)]
        cas.append([len(cas)+1, cp, eid, f"{s[0]} ({exigences[eid-1][1]})", rs, r.choice(testeurs), s])
ins("cas_test", ["id","campagne_id","exigence_id","titre","resultat","testeur"], [c[:6] for c in cas])

# --- anomalies : 1 par cas KO/Bloqué + quelques doublons de cas
devs = ["Thomas L.","Sophie P.","Yanis K.","Inès C."]
debut = {1:(9,7),2:(10,12),3:(11,9)}
ano = []
oubli = False  # un cas KO de la campagne 3 n'a volontairement aucune fiche d'anomalie
for c in cas:
    if c[4] not in ("KO","Bloqué"): continue
    if c[1] == 3 and c[4] == "KO" and not oubli:
        oubli = True; continue
    for rep in range(2 if c[0] % 4 == 0 else 1):
        m, d0 = debut[c[1]]
        dc = f"2026-{m:02d}-{min(d0 + r.randint(0, 12), 28):02d}"
        sev = r.choices(["bloquante","majeure","mineure"], [25,45,30])[0]
        if c[4] == "Bloqué": sev = "bloquante"
        ano.append([len(ano)+1, c[0], c[1], r.choice(c[6][1]), sev, "ouverte", r.choice(devs), camp[c[1]-1][2], dc, None])
def cloturer(a, st):
    y, m, d = map(int, a[8].split("-"))
    a[5] = st; a[9] = f"{y}-{m:02d}-{min(d + r.randint(1, 14), 28):02d}"
for a in ano:
    if a[2] == 1: cloturer(a, r.choice(["fermée","corrigée","rejetée"]))
a2 = [a for a in ano if a[2] == 2]; a3 = [a for a in ano if a[2] == 3]
for a in a2[:2]: a[4], a[5], a[9] = "bloquante", "ouverte", None
a2[2][4], a2[2][5], a2[2][9] = "majeure", "en correction", None
for a in a2[3:]: cloturer(a, r.choice(["fermée","corrigée"]))
for a in a3:
    if a[4] == "bloquante": cloturer(a, "corrigée")
a3[0][4], a3[0][5], a3[0][9] = "majeure", "ouverte", None
ins("anomalies", ["id","cas_test_id","campagne_id","titre","severite","statut","assigne_a","environnement","date_creation","date_cloture"], ano)

open(sys.argv[1] if len(sys.argv) > 1 else "bac-a-sable.sql", "w", encoding="utf-8").write("\n".join(out) + "\n")
