/* Exercices de SQL Quest. Format texte léger : paragraphes séparés par une ligne vide,
   listes avec "- ", `code`, **gras**, blocs ```sql ... ```.
   type "texte"  : réponse libre, correction affichée après réponse, auto-évaluation.
   type "sql"    : requête à écrire, comparée à la solution (colonnes, lignes, valeurs). */
window.NIVEAUX = {
  0: "Niveau 0 · Lire une base",
  1: "Niveau 1 · Lire et filtrer",
  2: "Niveau 2 · Compter et regrouper",
  3: "Niveau 3 · Relier les tables"
};

window.EXERCICES = [
  /* ---------------- Niveau 0 : texte ---------------- */
  {
    id: "N0-1", niveau: 0, type: "texte", tables: ["anomalies"],
    titre: "Une ligne, c'est quoi ?",
    situation: "Tu relis le registre des anomalies avant le COPIL. Tu remarques que les anomalies **1 et 2** ont le même titre et sont rattachées au même cas de test.",
    cours: "Une **table** est un tableau. Une **ligne** est un enregistrement, une **colonne** est une information sur cet enregistrement. Le **grain** d'une table répond à : « une ligne représente quoi ? ». C'est le premier réflexe avant de lire ou de compter quoi que ce soit.",
    question: "Dans la table `anomalies`, une ligne représente quoi ? Compare les anomalies 1 et 2 (panneau **Données**, onglet **anomalies**) : que peut signifier qu'elles aient le même cas de test et le même titre ? Que regarderais-tu pour trancher ?",
    correction: "Une ligne de `anomalies` = **une anomalie**.\n\nDeux explications sont possibles :\n\n- un même cas de test peut légitimement produire **plusieurs** anomalies (un cas, des défauts distincts) ;\n- la même anomalie a été **saisie deux fois** (doublon).\n\nLes données donnent des indices : les deux fiches ont le même cas (4), le même titre, la même sévérité (majeure) et le même statut (fermée), mais **pas la même date de création** (13 et 17 septembre) ni le même assigné (Thomas L. et Yanis K.). Ça ressemble à un doublon déclaré par deux personnes, mais **les données seules ne le prouvent pas**.",
    explication: "Pour trancher il faut sortir de la base : lire la description détaillée et les étapes de reproduction de chaque fiche, demander au testeur et à la MOE si c'est le même défaut. Un BA ne conclut pas « doublon » sur la seule base d'un titre identique. Retiens aussi le réflexe : **ne pas supprimer ni fusionner** une fiche sans l'accord de son propriétaire."
  },
  {
    id: "N0-2", niveau: 0, type: "texte", tables: ["anomalies", "cas_test", "exigences"],
    titre: "Les clés qui relient les tables",
    situation: "Le chef de projet te demande : « cette anomalie, elle touche quelle exigence ? ». La réponse n'est pas dans la table `anomalies`.",
    cours: "Une **clé primaire** (`id`) identifie une ligne de façon unique. Une **clé étrangère** est une colonne qui contient l'`id` d'une ligne d'une autre table : c'est un numéro qui pointe. Dans le panneau **Données** (à droite, ou sous l'énoncé sur petit écran), les colonnes liées (en bleu) sont cliquables : un clic t'amène à la ligne visée.",
    question: "Quelle colonne de `anomalies` relie une anomalie à son cas de test ? Quelle colonne de `cas_test` relie un cas de test à son exigence ? Pour chaque lien, dis vers quelle table il pointe.",
    correction: "- `anomalies.cas_test_id` pointe vers la table `cas_test` (colonne `id`).\n- `cas_test.exigence_id` pointe vers la table `exigences` (colonne `id`).\n\nLa chaîne se lit donc : **anomalie → cas de test → exigence**.",
    explication: "Retiens la forme du nom : `xxx_id` pointe presque toujours vers l'`id` de la table `xxx` (ici `cas_test_id` → `cas_test`, `exigence_id` → `exigences`). Ce mécanisme est exactement ce que fera une **jointure** au niveau 3 : suivre une clé d'une table à l'autre, mais pour toutes les lignes d'un coup."
  },
  {
    id: "N0-3", niveau: 0, type: "texte", tables: ["anomalies", "cas_test", "exigences"],
    titre: "Suivre l'anomalie 2 jusqu'à son exigence",
    situation: "Tu veux savoir quelle exigence est touchée par l'anomalie 2.",
    question: "Suis l'anomalie 2 jusqu'à son exigence en écrivant chaque étape (colonne et numéro), puis compare avec l'anomalie 1. Tu peux cliquer sur les valeurs bleues du panneau **Données** pour te déplacer.",
    correction: "- Anomalie 2 : `cas_test_id` = **4** → ligne 4 de `cas_test`.\n- Cas de test 4 : `exigence_id` = **8** → ligne 8 de `exigences`.\n- Exigence 8 : **EXG-008, « Consultation du solde »** (priorité Must).\n\nL'anomalie 1 suit exactement le même chemin (cas 4, exigence 8). Les deux anomalies touchent donc **la même exigence**.",
    explication: "C'est cohérent avec N0-1 : deux fiches, un seul cas de test, une seule exigence. Retiens aussi que les **titres peuvent induire en erreur** : ici le cas « Doublon de message » est rattaché à « Consultation du solde », ce qui n'a pas de sens métier. C'est un défaut de la base fictive. En mission, **suis les clés, pas les titres**."
  },
  {
    id: "N0-4", niveau: 0, type: "texte", tables: ["exigences", "cas_test", "anomalies"],
    titre: "Pourquoi les comptages se gonflent",
    situation: "Un collègue assemble exigences, cas de test et anomalies dans un seul grand tableau et te dit : « j'ai 49 lignes, donc 49 cas de test ». Pourtant la table `cas_test` n'a que 45 lignes.",
    cours: "Quand on relie une table « parent » à une table « enfant », chaque parent apparaît **autant de fois qu'il a d'enfants**. Si on compte ensuite les lignes du tableau assemblé, on compte les enfants, pas les parents.",
    question: "À ton avis, d'où viennent les 4 lignes en trop ? Prends l'exigence **EXG-008** : elle a 3 cas de test (4, 19 et 34). Compte les anomalies de chacun de ces cas : combien de lignes EXG-008 occupe-t-elle dans le grand tableau ? (Ne cherche pas de requête, compte à la main dans les onglets.)",
    correction: "Dans la base :\n\n- le cas **4** a 2 anomalies (les fiches 1 et 2) → 2 lignes ;\n- le cas **19** a 1 anomalie → 1 ligne ;\n- le cas **34** n'a aucune anomalie → 1 ligne (le cas existe, sans fiche).\n\nEXG-008 occupe donc **4 lignes** alors qu'elle n'est qu'**une exigence** (et 3 cas de test). Sur l'ensemble de la base, 45 cas de test donnent 49 lignes une fois reliés aux anomalies : les 4 lignes en trop viennent des cas qui ont plusieurs anomalies ou aucune.",
    explication: "C'est le piège le plus courant des jointures, appelé **fan-out** (multiplication des lignes). Il explique des totaux faux sans aucune erreur affichée. Le remède : savoir quel est le **grain** du résultat avant de compter, et compter `DISTINCT` ou agréger **avant** de joindre. On le pratiquera au niveau 3. Remarque aussi le cas 34 : un cas KO sans aucune anomalie, c'est exactement le genre d'écart qu'un testeur doit repérer (exercice N3-3)."
  },

  /* ---------------- Niveau 1 : SQL ---------------- */
  {
    id: "N1-1", niveau: 1, type: "sql", tables: ["anomalies"],
    titre: "Les bloquantes encore ouvertes",
    situation: "Le COPIL est dans une heure. Le chef de projet te demande la liste des **anomalies bloquantes encore ouvertes**, avec l'id, le titre et la personne à qui elles sont assignées.",
    cours: "Une requête de lecture a la forme :\n\n```sql\nSELECT colonne1, colonne2\nFROM table\nWHERE condition;\n```\n\n`SELECT` choisit les colonnes, `FROM` la table, `WHERE` garde les lignes qui remplissent la condition. Plusieurs conditions se combinent avec `AND` / `OR`. Les textes s'écrivent entre apostrophes : `'bloquante'`.",
    question: "Écris la requête. Colonnes attendues, dans cet ordre : `id`, `titre`, `assigne_a`. Statut exact à utiliser : `ouverte`.",
    indices: [
      "Il y a deux conditions à remplir en même temps : la sévérité et le statut.",
      "Squelette : `SELECT id, titre, assigne_a FROM anomalies WHERE ... AND ...;`",
      "Les valeurs sont `'bloquante'` (colonne severite) et `'ouverte'` (colonne statut)."
    ],
    solution: "SELECT id, titre, assigne_a\nFROM anomalies\nWHERE severite = 'bloquante' AND statut = 'ouverte';",
    explication: "On filtre sur **deux colonnes** avec `AND` : les deux conditions doivent être vraies. Erreur fréquente : écrire `OR`, qui ramène toutes les bloquantes **et** toutes les ouvertes, donc beaucoup trop de lignes. Réflexe : prédis le nombre de lignes avant d'exécuter (ici, une poignée, pas des dizaines)."
  },
  {
    id: "N1-2", niveau: 1, type: "sql", tables: ["anomalies"], ordered: true,
    titre: "Les 5 dernières en REC2",
    situation: "On te demande les **5 dernières anomalies créées en REC2** (colonne `environnement`).",
    cours: "`ORDER BY colonne DESC` trie du plus grand au plus petit (donc du plus récent au plus ancien pour une date). `LIMIT n` ne garde que les `n` premières lignes. Pour départager des égalités, on ajoute un deuxième critère : `ORDER BY date_creation DESC, id DESC`.",
    question: "Colonnes attendues : `id`, `titre`, `date_creation`. En cas de même date, la plus grande `id` vient d'abord.",
    indices: [
      "Filtre d'abord (`WHERE`), trie ensuite (`ORDER BY`), limite en dernier (`LIMIT`).",
      "`... WHERE environnement = 'REC2' ORDER BY date_creation DESC, id DESC LIMIT 5;`"
    ],
    solution: "SELECT id, titre, date_creation\nFROM anomalies\nWHERE environnement = 'REC2'\nORDER BY date_creation DESC, id DESC\nLIMIT 5;",
    explication: "L'**ordre d'écriture** est imposé : `WHERE` avant `ORDER BY` avant `LIMIT`. Sans le second critère `id DESC`, deux anomalies de même date pourraient apparaître dans un ordre qui change d'une exécution à l'autre : un résultat non reproductible est un problème dès qu'on le colle dans une fiche d'anomalie."
  },
  {
    id: "N1-3", niveau: 1, type: "sql", tables: ["anomalies"],
    titre: "Les anomalies qui parlent d'IBAN",
    situation: "Le métier te demande : « toutes les anomalies qui mentionnent l'IBAN, c'est quoi ? »",
    cours: "`LIKE` cherche un motif dans un texte. `%` remplace n'importe quelle suite de caractères : `LIKE '%IBAN%'` trouve « IBAN » n'importe où dans le titre.",
    question: "Colonnes attendues : `id`, `titre`.",
    indices: ["Le filtre porte sur la colonne `titre`.", "`WHERE titre LIKE '%IBAN%'`"],
    solution: "SELECT id, titre\nFROM anomalies\nWHERE titre LIKE '%IBAN%';",
    explication: "`LIKE` ne trouve que ce que tu cherches : si certaines fiches écrivent « Iban » ou « RIB », elles peuvent t'échapper selon le moteur (la sensibilité à la casse varie). Dans une vraie base, vérifie plusieurs graphies avant d'affirmer « il n'y en a que 2 »."
  },

  /* ---------------- Niveau 2 : SQL ---------------- */
  {
    id: "N2-1", niveau: 2, type: "sql", tables: ["cas_test"],
    titre: "Combien de cas KO ?",
    situation: "Le chef de projet veut un chiffre : **combien de cas de test sont KO** ?",
    cours: "Les **fonctions d'agrégation** résument plusieurs lignes en une : `COUNT(*)` compte les lignes, `SUM`, `AVG`, `MIN`, `MAX`. On peut filtrer avant de compter avec `WHERE`.",
    question: "Une seule colonne, une seule ligne : le nombre de cas dont le résultat est `KO`.",
    indices: ["`SELECT COUNT(*) FROM cas_test WHERE ...`"],
    solution: "SELECT COUNT(*) AS nb_ko\nFROM cas_test\nWHERE resultat = 'KO';",
    explication: "Attention : « KO » et « Bloqué » sont deux résultats différents. Ce chiffre ne compte que les `KO`. Quand tu donnes un chiffre à quelqu'un, précise toujours **ce qui est inclus**."
  },
  {
    id: "N2-2", niveau: 2, type: "sql", tables: ["cas_test"],
    titre: "Répartition par résultat",
    situation: "On te demande la **répartition des cas de test par résultat**, du plus fréquent au moins fréquent.",
    cours: "`GROUP BY colonne` fait un paquet par valeur de la colonne ; chaque agrégat est alors calculé **par paquet**. Règle : toute colonne du `SELECT` qui n'est pas dans un agrégat doit figurer dans le `GROUP BY`.",
    question: "Colonnes attendues : `resultat`, puis le nombre de cas. Tri : du plus grand nombre au plus petit.",
    indices: ["Regroupe par `resultat` et compte avec `COUNT(*)`.", "Pour trier sur le compte, donne-lui un alias : `COUNT(*) AS nb` puis `ORDER BY nb DESC`."],
    solution: "SELECT resultat, COUNT(*) AS nb\nFROM cas_test\nGROUP BY resultat\nORDER BY nb DESC;",
    explication: "Vérification express : la somme des quatre nombres doit faire 45, le total des cas de test. Si ce n'est pas le cas, une ligne a été perdue (souvent un `WHERE` oublié ou une valeur `NULL`)."
  },
  {
    id: "N2-3", niveau: 2, type: "sql", tables: ["cas_test", "campagnes"],
    titre: "Avancement par campagne",
    situation: "Pour le point d'avancement, tu dois fournir par campagne le **nombre de cas**, le **nombre de cas OK** et le **pourcentage de OK arrondi à 1 décimale**.",
    cours: "Pour compter selon une condition, on utilise `CASE WHEN ... THEN 1 ELSE 0 END` dans un `SUM`. Pour un pourcentage, multiplie par `100.0` (et pas `100`) afin d'éviter la division entière. `ROUND(x, 1)` arrondit à 1 décimale.",
    question: "Colonnes attendues : `campagne_id`, nombre de cas, nombre OK, pourcentage OK (1 décimale). Regroupe sur `campagne_id` de `cas_test`.",
    indices: [
      "Nombre de cas : `COUNT(*)`. Nombre OK : `SUM(CASE WHEN resultat = 'OK' THEN 1 ELSE 0 END)`.",
      "Pourcentage : `ROUND(100.0 * SUM(CASE WHEN resultat = 'OK' THEN 1 ELSE 0 END) / COUNT(*), 1)`."
    ],
    solution: "SELECT campagne_id,\n       COUNT(*) AS nb_cas,\n       SUM(CASE WHEN resultat = 'OK' THEN 1 ELSE 0 END) AS nb_ok,\n       ROUND(100.0 * SUM(CASE WHEN resultat = 'OK' THEN 1 ELSE 0 END) / COUNT(*), 1) AS pct_ok\nFROM cas_test\nGROUP BY campagne_id;",
    explication: "Si tu écris `100 * SUM(...) / COUNT(*)` sans `.0`, certains moteurs (SQL Server, PostgreSQL, SQLite) font une division entière et tronquent. Dis aussi **quel dénominateur** tu prends : ici tous les cas, y compris « Non exécuté ». Deux « taux de réussite » différents circulent souvent dans un projet : précise lequel tu présentes."
  },
  {
    id: "N2-4", niveau: 2, type: "sql", tables: ["cas_test"],
    titre: "Les testeurs avec au moins 3 KO",
    situation: "Le chef de projet veut savoir quels testeurs ont **au moins 3 cas KO** (pour caler une revue de leurs cas).",
    cours: "`WHERE` filtre les lignes **avant** le regroupement ; `HAVING` filtre les paquets **après**, ce qui permet de tester un agrégat : `HAVING COUNT(*) >= 3`. On ne peut pas écrire `WHERE COUNT(*) >= 3`.",
    question: "Colonnes attendues : `testeur`, nombre de cas KO. Tri : plus de KO d'abord.",
    indices: ["Filtre les `KO` avec `WHERE`, regroupe par `testeur`, puis filtre le regroupement avec `HAVING`."],
    solution: "SELECT testeur, COUNT(*) AS nb_ko\nFROM cas_test\nWHERE resultat = 'KO'\nGROUP BY testeur\nHAVING COUNT(*) >= 3\nORDER BY nb_ko DESC;",
    explication: "Retiens l'**ordre logique d'exécution** : `FROM` → `WHERE` → `GROUP BY` → `HAVING` → `SELECT` → `ORDER BY`. C'est pourquoi un agrégat ne peut pas être dans le `WHERE`. Un point de posture : ce nombre de KO n'est **pas** une mesure de la qualité du testeur (les cas n'ont pas la même difficulté) ; si ce chiffre est présenté ainsi, sache le contester."
  },

  /* ---------------- Niveau 3 : SQL ---------------- */
  {
    id: "N3-1", niveau: 3, type: "sql", tables: ["anomalies", "campagnes"],
    titre: "Bloquantes avec le nom de la campagne",
    situation: "Le rapport de recette doit afficher chaque anomalie bloquante avec le **nom de sa campagne**, pas seulement son numéro.",
    cours: "`JOIN ... ON` relie deux tables en suivant une clé : \n\n```sql\nFROM anomalies a\nJOIN campagnes ca ON ca.id = a.campagne_id\n```\n\nLes lettres `a` et `ca` sont des **alias** : des raccourcis. Une colonne qui existe dans les deux tables se préfixe : `a.id`, `ca.nom`.",
    question: "Colonnes attendues : `id` de l'anomalie, `titre`, nom de la campagne. Trie par `id` de l'anomalie. Seulement les anomalies de sévérité `bloquante`.",
    indices: [
      "Relie `anomalies` à `campagnes` avec `ON ca.id = a.campagne_id`.",
      "`SELECT a.id, a.titre, ca.nom FROM anomalies a JOIN campagnes ca ON ca.id = a.campagne_id WHERE ... ORDER BY a.id;`"
    ],
    solution: "SELECT a.id, a.titre, ca.nom AS campagne\nFROM anomalies a\nJOIN campagnes ca ON ca.id = a.campagne_id\nWHERE a.severite = 'bloquante'\nORDER BY a.id;",
    explication: "Une jointure se lit en suivant la clé : « pour chaque anomalie, va chercher la campagne dont l'`id` est égal à `campagne_id` ». Contrôle de sanité : le nombre de lignes doit être **le même** que sans la jointure (ici une campagne par anomalie, donc aucune ligne ajoutée ni perdue). Si ce n'est pas le cas, pose-toi la question du grain."
  },
  {
    id: "N3-2", niveau: 3, type: "sql", tables: ["exigences", "cas_test"], ordered: true,
    titre: "Exigences Must : les cas en échec",
    situation: "Pour le go/no-go, il faut lister, pour chaque exigence de priorité **Must**, les cas de test **KO** qui la concernent.",
    cours: "Une jointure peut porter sur n'importe quelle clé étrangère : ici `cas_test.exigence_id = exigences.id`. Les filtres peuvent porter sur les colonnes des **deux** tables dans le même `WHERE`.",
    question: "Colonnes attendues : code de l'exigence, titre du cas de test. Tri : `code`, puis `id` du cas de test.",
    indices: [
      "Relie `exigences e` et `cas_test ct` avec `ON ct.exigence_id = e.id`.",
      "`WHERE e.priorite = 'Must' AND ct.resultat = 'KO' ORDER BY e.code, ct.id`"
    ],
    solution: "SELECT e.code, ct.titre\nFROM exigences e\nJOIN cas_test ct ON ct.exigence_id = e.id\nWHERE e.priorite = 'Must' AND ct.resultat = 'KO'\nORDER BY e.code, ct.id;",
    explication: "Cette requête perd volontairement les exigences Must **sans** cas KO : c'est ce qu'on veut ici. Quand on veut aussi voir celles qui n'ont rien en face, on passe à `LEFT JOIN` (voir N3-3). Choisir `JOIN` ou `LEFT JOIN`, c'est décider ce qu'on veut voir **quand il n'y a rien en face**."
  },
  {
    id: "N3-3", niveau: 3, type: "sql", tables: ["cas_test", "anomalies"],
    titre: "Des KO sans fiche d'anomalie",
    situation: "Avant la clôture de la recette, le responsable demande : « est-ce que tous les cas KO ou Bloqués ont bien une **fiche d'anomalie** ? »",
    cours: "`LEFT JOIN` garde **toutes** les lignes de la table de gauche, même sans correspondance ; les colonnes de droite valent alors `NULL`. Pour trouver les lignes **sans** correspondance (« anti-jointure ») : `LEFT JOIN ... WHERE table_droite.id IS NULL`. On teste `NULL` avec `IS NULL`, jamais avec `= NULL`.",
    question: "Colonnes attendues : `id`, `titre`, `testeur` des cas dont le résultat est `KO` ou `Bloqué` et qui n'ont aucune anomalie.",
    indices: [
      "`FROM cas_test ct LEFT JOIN anomalies a ON a.cas_test_id = ct.id`",
      "Filtre : `WHERE ct.resultat IN ('KO', 'Bloqué') AND a.id IS NULL`"
    ],
    solution: "SELECT ct.id, ct.titre, ct.testeur\nFROM cas_test ct\nLEFT JOIN anomalies a ON a.cas_test_id = ct.id\nWHERE ct.resultat IN ('KO', 'Bloqué')\n  AND a.id IS NULL;",
    explication: "Avec un `JOIN` simple, les cas sans anomalie **disparaîtraient** : c'est justement ceux qu'on cherche. Le `LEFT JOIN` suivi de `IS NULL` est la forme sûre. Évite `NOT IN (SELECT ...)` : si la sous-requête contient un seul `NULL`, `NOT IN` ne renvoie plus rien. Dans la base, ce contrôle trouve un cas (campagne 3) : un KO jamais déclaré, donc invisible dans les statistiques d'anomalies."
  }
];
