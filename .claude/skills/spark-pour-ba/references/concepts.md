# Le vocabulaire de Spark en langage de BA

Reformulé dans mes mots à partir des chapitres 1, 2, 4, 9, 15 et 18 du livre *Spark: The Definitive Guide*
(1ʳᵉ édition, 2018, Spark 2.x). Pour chaque terme : **ce que c'est**, **pourquoi un BA/testeur doit le connaître**.

## 1. Pourquoi Spark existe

- **Le problème.** Depuis environ 2005 les processeurs ne vont plus plus vite : on ajoute des cœurs. Un
  programme classique n'en profite pas tout seul. En parallèle, stocker des données coûte de moins en moins
  cher. Il faut donc répartir le calcul sur **plusieurs machines**.
- **La réponse.** Spark est un **moteur de calcul unifié** : un même moteur et des API cohérentes pour
  charger des données, les interroger en SQL, les transformer, faire du machine learning et traiter des flux.
  Il **ne stocke pas** les données : il lit et écrit dans un stockage (fichiers sur un système distribué ou le
  cloud, bases, files de messages) et calcule dessus.
- **Pour toi.** Si le client dit « c'est du Spark », ses données sont probablement des **fichiers** dans un
  stockage partagé, interrogeables en SQL, et ses traitements sont des **jobs** planifiés qui tournent sur un
  cluster. Ce n'est pas une base de données classique.

## 2. L'architecture d'une application

| Terme | Ce que c'est | Pourquoi tu le croises |
|---|---|---|
| **Cluster** | Un groupe de machines qui mettent leurs ressources en commun | « Le job a manqué de ressources » |
| **Gestionnaire de cluster** | Répartit les ressources entre applications (le livre cite le gestionnaire autonome de Spark, YARN, Mesos ; en pratique aujourd'hui souvent Kubernetes ou une plateforme managée) | Files d'attente, quotas, créneaux |
| **Driver** | Le « chef d'orchestre » de l'application : exécute le programme principal, planifie et distribue le travail, garde l'état | Si le driver tombe, **tout** s'arrête ; ne jamais lui faire rapatrier de gros volumes |
| **Executors** | Les « ouvriers » : exécutent les tâches et rendent compte au driver | Leur mémoire et leur nombre déterminent la capacité |
| **Mode local** | Driver et executors tournent sur ta machine | C'est le mode de notre laboratoire d'entraînement |
| **SparkSession** | Le point d'entrée de ton code vers Spark | Tu le verras dans tous les scripts |

## 3. Les données : DataFrame, schéma, catalogue

- **DataFrame** : un tableau (lignes et colonnes nommées et typées) **réparti sur plusieurs machines**. Il est
  **immuable** : on ne le modifie pas, on décrit comment en produire un nouveau.
- **Schéma** : les noms et types des colonnes. Sans schéma imposé, Spark peut le **deviner** (`inferSchema`) :
  pratique, mais une valeur inattendue peut changer le type d'une colonne entière (démonstration :
  `scripts/pieges_demo.py`, piège n°3).
- **Dataset** : variante typée pour Scala/Java ; **RDD** : l'ancienne couche de bas niveau (parties III du livre).
  Le livre insiste sur les **API structurées** (DataFrame, SQL, Dataset) qui sont la voie moderne ; un BA
  travaille presque toujours à ce niveau, voire seulement en SQL.
- **Catalogue / metastore** : le registre des tables et colonnes. Spark SQL peut se brancher sur un **metastore
  Hive** (chapitre 10) ; c'est ainsi que les tables d'un datalake sont retrouvées par leur nom.

## 4. Transformations, actions et paresse

- **Transformation** : une instruction de changement (filtrer, regrouper, joindre). Elle **ne calcule rien**.
- **Action** : une instruction qui **demande un résultat** (compter, afficher, écrire). C'est elle qui lance
  le travail.
- **Évaluation paresseuse (lazy).** Spark accumule les transformations dans un **plan** et ne l'exécute qu'à
  l'action, ce qui lui permet d'optimiser l'ensemble (par exemple **ne lire que les lignes utiles** : *predicate
  pushdown*). Conséquence pratique : **une erreur peut n'apparaître qu'à l'action**, bien après la ligne fautive ;
  et un `count()` relance tout le calcul.
- **Étroite / large.** Une transformation **étroite** (filtre) travaille partition par partition ; une
  **large** (regroupement, jointure) oblige à **déplacer des données entre machines**.

## 5. Le plan d'exécution (chapitre 4)

Spark transforme ton code en **plan logique** (vérifié contre le catalogue : une colonne qui n'existe pas
est rejetée ici), l'optimise (optimiseur **Catalyst**), puis choisit un **plan physique** en comparant des coûts
(par exemple la meilleure façon de faire une jointure selon la taille des tables). On le lit avec `EXPLAIN`.
**Spark 3 ajoute l'exécution adaptative (AQE)** : le plan est ré-optimisé en cours d'exécution à partir des
statistiques réelles ; ce n'est pas dans le livre (écrit pour Spark 2).

## 6. Partitions, shuffle, jointures

- **Partition** : un paquet de lignes qui vit sur une machine. Le parallélisme maximal est limité par le
  nombre de partitions **et** d'executors.
- **Shuffle** : redistribution des données entre machines pour regrouper ou joindre ; c'est **l'opération
  coûteuse** (réseau, disque). Dans un plan, repère `Exchange`.
- **Jointure de grosse à grosse table** : *shuffle join* (tous les nœuds se parlent), coûteuse. **Grosse à
  petite table** : *broadcast join* (la petite est copiée partout, puis chacun travaille seul), nettement
  plus rapide (chapitre 8).
- **Déséquilibre (skew)** : si une clé concentre beaucoup de lignes (par exemple un client « 0 » ou un statut
  très dominant), une machine travaille bien plus que les autres et le job **traîne** (*stragglers*, chapitre 18).
- **Problème des petits fichiers** : trop de petits fichiers ralentissent lecture et métadonnées ; trop
  gros aussi (chapitre 9 : l'option `maxRecordsPerFile` existe pour plafonner).

## 7. Formats et lecture/écriture (chapitre 9)

| Format | Nature | À savoir |
|---|---|---|
| **CSV, JSON** | Texte, lisible | Pas de typage fiable, plus lents ; options de lecture à régler |
| **Parquet, ORC** | Colonnaires, typés, compressés | Formats usuels d'un datalake ; lecture ciblée de colonnes |
| **Base SQL via JDBC** | Lecture/écriture vers une base | *Query pushdown* : le filtre est exécuté côté base si possible |

- **Modes de lecture** : `PERMISSIVE` (défaut : une ligne corrompue devient des `NULL`, **sans erreur**),
  `DROPMALFORMED` (la ligne est **jetée**), `FAILFAST` (**erreur** immédiate). Démontré dans
  `scripts/pieges_demo.py`, piège n°2 : c'est ce qu'un testeur doit connaître par cœur.
- **Modes d'écriture** : `append`, `overwrite`, `errorIfExists`, `ignore` : `append` après un rejeu **duplique**
  les données si le traitement n'est pas idempotent.
- **Partitionnement** (`partitionBy`) : organise les fichiers en répertoires par valeur de colonne (par exemple par
  date) ; **bucketing** : répartit en paquets par clé. Les deux accélèrent certaines requêtes.

## 8. Observer et diagnostiquer (chapitre 18)

- **Spark UI** : l'écran de suivi (onglets Jobs, Stages, SQL…). **Job** = déclenché par une action ; **stage** =
  étape entre deux shuffles ; **task** = unité de travail sur une partition. Après la fin, le **History Server**
  conserve ces écrans.
- **Symptômes courants** : le job ne démarre pas (ressources), erreur avant exécution (colonne inexistante),
  erreur pendant l'exécution (donnée imprévue), tâches lentes, agrégations ou jointures lentes, mémoire du
  driver ou d'un executor, disque plein, **NULL inattendus après une transformation** (souvent un format de
  données qui a changé ou une conversion implicite ratée).

## 9. Flux (chapitres 20 à 23) : seulement les idées

- **Batch vs flux.** Un traitement de flux traite les données au fil de l'eau ; **Structured Streaming** réutilise
  les API structurées.
- **Event time vs processing time.** Le moment où l'événement s'est produit n'est pas celui où il est traité :
  des événements en retard faussent un calcul par fenêtre de temps, d'où la notion de **watermark** (seuil de
  tolérance au retard). Pour un testeur : tester **les événements tardifs et désordonnés** est indispensable.
- **Micro-batch vs continu.** Le mode par défaut découpe le flux en petits lots.

## 10. Ce que le livre ne couvre pas (d'après mes connaissances, à confirmer)

Formats de table transactionnels (**Delta Lake**, **Iceberg**, **Hudi**) qui apportent `UPDATE`/`DELETE`/`MERGE`,
versions de données et garanties ACID sur des fichiers ; **Spark 4** et son mode ANSI par défaut ; plateformes
managées (Databricks, services cloud). Demande au data engineer **quelle plateforme et quel format de table**
sont utilisés : cela change ce que tu peux tester.
