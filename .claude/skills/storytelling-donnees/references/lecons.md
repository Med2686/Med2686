# Les leçons du livre, reformulées et reliées à la recette

Synthèse **dans mes mots** de *Storytelling with Data* (10 chapitres : introduction, chapitres 1 à 8 = les
leçons, chapitre 9 = cas pratiques, chapitre 10 = conclusion). Les numéros renvoient aux chapitres du livre,
à lire pour les exemples visuels. Rien n'est recopié : c'est une carte pour retrouver l'idée vite.

---

## Leçon 1 : comprendre le contexte (chapitre 1)

**Idée centrale.** Réussir une visualisation commence **avant** la visualisation. On ne montre pas des données,
on cherche à faire comprendre ou faire agir.

- **Exploratoire vs explicatif.** L'exploration, c'est ouvrir cent huîtres pour trouver deux perles ; l'explication,
  c'est présenter les deux perles. L'erreur courante est de montrer les cent huîtres pour prouver le travail
  accompli : on fait alors rouvrir toutes les huîtres à l'audience.
- **Qui, quoi, comment.** *Qui* : une audience précise (idéalement le décideur), et la relation qu'on a avec elle
  (crédibilité acquise ou à établir). *Quoi* : ce qu'on veut qu'elle sache **ou fasse** ; si on ne sait pas dire
  l'action attendue, on se demande pourquoi on communique. *Comment* : seulement ensuite, quelles données
  et quel format.
- **Oser recommander.** L'analyste connaît souvent mieux les données que l'audience : il doit proposer une
  action, ou à défaut des pistes. Même une recommandation discutée déclenche une conversation utile, alors
  qu'un simple « voici les chiffres » appelle un « intéressant » puis plus rien.
- **Histoire en trois minutes.** Si on n'avait que trois minutes, que dirait-on ? Cela rend indépendant des slides
  et résiste à un créneau raccourci.
- **Idée directrice (Big Idea).** Une seule phrase complète qui contient un point de vue, ce qui est en jeu, et
  qui est complète (sujet-verbe-complément). Notion empruntée à Nancy Duarte (*Resonate*).
- **Storyboard à la main.** Papier, post-it, tableau blanc, **pas** le logiciel de présentation : on réarrange
  sans attachement, et on évite la production de slides avant d'avoir une structure. Faire valider la structure
  par le demandeur quand c'est possible.

**À retenir pour un BA.** Cette leçon est celle qui change le plus de choses, car le défaut de la plupart des
supports de COPIL n'est pas graphique : il est dans l'absence de décision demandée.

---

## Leçon 2 : choisir un visuel adapté (chapitre 2)

**Idée centrale.** Le type de visuel suit la question à laquelle le lecteur doit répondre.

| Besoin | Visuel recommandé par le livre | Remarques |
|---|---|---|
| Un ou deux chiffres | **Texte simple** : le chiffre en grand + quelques mots | Un graphique pour deux nombres n'ajoute rien |
| Beaucoup de valeurs précises, plusieurs unités | **Tableau** | Lecture de valeurs ; allège bordures, aligne les nombres |
| Tableau avec repérage de motifs | **Carte de chaleur (heatmap)** | Un tableau où la couleur guide l'œil |
| Relation entre deux variables | **Nuage de points** | Montre corrélation, regroupements |
| Évolution dans le temps | **Courbe** (+ variantes : moyenne dans une plage) | Pour des données continues |
| Comparer deux points dans le temps pour plusieurs catégories | **Slopegraph** | Montre qui monte, qui baisse |
| Comparer des catégories | **Barres verticales** ; **barres horizontales** quand les libellés sont longs | **Base à zéro obligatoire pour les barres** : la longueur est ce qu'on compare. Barres plus larges que l'espace entre elles, sans devenir des surfaces |
| Parties d'un tout | **Barres empilées** (verticales ou horizontales), en valeur absolue ou à 100 % | On ne compare bien que la série posée sur la base commune ; au-delà, plus de repère commun. En version à 100 %, penser à donner aussi les totaux |
| Passage d'une valeur à une autre par étapes | **Cascade (waterfall)** | Utile pour un écart, un solde, un budget |
| Aire | Utiliser avec prudence | Difficile à lire hors empilement simple |

**À éviter, selon l'autrice :**
- **Camembert et donut.** On compare mal des angles et des surfaces ; l'exemple du livre montre un camembert
  où la part qui *paraît* la plus grande ne l'est pas. Alternatives : montrer les nombres directement, une
  simple barre, une barre empilée à 100 %, un slopegraph (chapitre 9).
- **3D.** Elle déforme la perception des valeurs.
- **Double axe vertical.** Il crée des corrélations visuelles arbitraires selon l'échelle choisie.
- **Éthique.** Une barre doit partir de zéro ; couper l'axe exagère les écarts. La règle **ne vaut pas pour les courbes** (on y compare des positions, pas des longueurs), mais une base non nulle se signale clairement et se manie avec prudence. Un seul lecteur attentif qui repère l'axe truqué suffit à ruiner la crédibilité de tout l'argument.
- **Axe ou étiquettes de données.** Selon ce que le lecteur doit retenir : pour **la tendance générale**, garde l'axe mais grisé ; pour **les valeurs précises**, étiquette les points directement et supprime l'axe (il serait redondant).

---

## Leçon 3 : éliminer l'encombrement (chapitre 3)

**Idée centrale.** Chaque élément ajouté consomme de l'attention du lecteur (la **charge cognitive**) ; ce qui
n'informe pas doit disparaître ou s'effacer.

- **Rapport signal/bruit (idée de data-ink).** Ce qui porte l'information (le signal) doit dominer ce qui ne la
  porte pas (le bruit).
- **Six principes de la Gestalt** pour décider ce qui regroupe ou sépare : **proximité** (ce qui est proche est
  groupé), **similarité** (même couleur/forme → même groupe), **enclosure** (ce qui est entouré est groupé),
  **fermeture** (le cerveau complète une forme), **continuité** (l'œil suit une ligne), **connexion** (reliés =
  groupés). On s'en sert pour dire « lis par ligne » ou « lis par colonne » sans tracer de traits.
- **Ordre visuel.** **Alignement** (bords nets, un seul axe d'alignement), **espace blanc** (il est utile, pas
  perdu), **contraste** employé seulement là où il sert un message.
- **Désencombrer en six gestes.** 1 supprimer la bordure du graphique ; 2 supprimer le quadrillage ; 3 supprimer
  les marqueurs de données superflus ; 4 nettoyer les libellés d'axe ; 5 **étiqueter directement** les séries
  (plus de légende à décoder) ; 6 utiliser une **couleur cohérente**.
- **Exception.** Un détail redondant peut rester s'il aide à lire (par exemple un repère utile à l'audience).

**À retenir.** Le désencombrement ne rend pas le graphique « joli » : il rend le message **plus rapide à voir**.

---

## Leçon 4 : attirer l'attention (chapitre 4)

**Idée centrale.** On voit avec le cerveau : décider où l'œil va, c'est décider de ce qui sera retenu.

- **Mémoire.** Iconique (instantanée), **à court terme (environ quatre éléments à la fois)**, à long terme
  (mots et images). D'où : pas dix séries de dix couleurs avec une légende lointaine ; on regroupe et on
  étiquette au plus près.
- **Attributs préattentifs.** Ce que l'œil repère sans effort : **taille, couleur, position, gras, orientation,
  soulignement, ombre**… On s'en sert pour désigner **la** chose importante, dans le texte comme dans les graphiques.
- **Un seul accent.** Plus on met en évidence, moins chaque élément ressort ; mettre en valeur un aspect peut
  en masquer d'autres.
- **Couleur.** À utiliser avec parcimonie (gris + une couleur d'accent) et **de façon cohérente** d'un visuel à
  l'autre. Penser au **daltonisme** (éviter le couple rouge/vert comme seul codage) et au **ton** que la couleur
  porte (rouge = alarme, variations culturelles, couleurs de marque à utiliser ou non).
- **Position.** Sans autre repère, le lecteur balaie en « Z » depuis le coin haut gauche : y placer l'essentiel (conclusion, appel à l'action) et ne pas lui faire lire à contre-sens de son habitude.

---

## Leçon 5 : penser comme un designer (chapitre 5)

**Idée centrale.** La forme suit la fonction : le visuel doit **indiquer comment s'en servir**.

- **Affordances.** Trois gestes : **mettre en avant l'important**, **éliminer les distractions**, **créer une
  hiérarchie visuelle claire** (le regard sait par où entrer et dans quel ordre lire), notamment avec des
  super-catégories.
- **Accessibilité.** Ne pas surcompliquer ; **le texte est un allié** (annoter, expliquer, pas de jargon) ; un
  visuel mal compris est souvent une faute de conception, pas de lecteur.
- **Titres d'action.** Le titre énonce la conclusion (« les retards se concentrent sur trois lots »), pas le
  sujet (« retards par lot »).
- **Esthétique.** Un visuel soigné est jugé plus crédible et plus utilisable ; cohérence de police, d'alignement.
- **Acceptation.** Il faut parfois faire accepter la nouveauté auprès de l'audience (habitudes de lecture,
  charte) : y aller par étapes.

---

## Leçon 6 : raconter une histoire (chapitre 7) et tout assembler (chapitre 8)

**Idée centrale.** Une histoire a un début, un milieu et une fin ; les humains retiennent ce qui est raconté.

- **Début** : le contexte et pourquoi l'audience doit s'en soucier. **Milieu** : ce qui a changé, le problème, les
  données qui le montrent. **Fin** : ce que l'on propose ; l'appel à l'action.
- **Ordre narratif.** Décider selon l'audience : mener avec la demande (public pressé) ou construire la
  crédibilité d'abord ; l'ordre est un choix, pas un hasard. Un résumé exécutif en tête d'un long document aide.
- **Écrire les titres d'abord.** Si l'on ne peut enchaîner les titres de slides comme un récit cohérent, le
  contenu n'est pas prêt.
- **Logique horizontale / verticale.** *Horizontale* : lire seulement les titres doit raconter l'histoire.
  *Verticale* : chaque slide se comprend de haut en bas et les éléments se répondent.
- **Storyboard inversé.** Partir d'un document existant, noter l'idée de chaque page, et regarder si le fil
  tient ; c'est un outil de revue.
- **Répétition et formules mémorables.** Répéter l'idée clé à des endroits stratégiques et la formuler en
  phrase facile à reprendre (« sound bite »).
- **Chapitre 8 : l'exemple complet.** Un graphique de départ est retravaillé en suivant les six leçons dans l'ordre
  (contexte → visuel → désencombrement → focus → hiérarchie → récit). C'est le meilleur chapitre pour voir le
  processus entier ; à lire avec les figures.

---

## Chapitre 9 : cas pratiques (à consulter selon le problème rencontré)

Fond sombre et couleurs ; **animation** dans une présentation ; **logique d'ordre** ; **éviter le « graphique
spaghetti »** (trop de courbes : mettre en avant une ligne à la fois, ou séparer dans l'espace, ou combiner) ;
**alternatives au camembert** (quatre solutions). Utile quand on a un cas concret qui résiste.

## Chapitre 10 : après la lecture

Cinq conseils : **maîtriser ses outils**, **itérer et chercher du retour**, **consacrer du temps** à cette
pratique, **chercher l'inspiration** dans de bons exemples (et aussi dans les mauvais), **s'amuser et trouver son
style**. Pour une équipe : former tout le monde, avoir un ou deux experts internes, externaliser, ou combiner.
Piste concrète : ne pas refondre un rapport mensuel d'un coup ; **commencer par mettre le rapport existant en
annexe** et ajouter devant quelques slides qui racontent l'essentiel.

---

## Les 8 réflexes à installer (résumé opérationnel)

1. Dire l'idée directrice en une phrase complète avant d'ouvrir un outil.
2. Nommer l'audience : une personne ou un rôle, pas « tout le monde ».
3. Demander une action, ou proposer une piste.
4. Choisir le visuel d'après la question ; éviter camembert, 3D, double axe.
5. Retirer bordures, quadrillage, légende ; étiqueter directement.
6. Griser le reste, colorer **une** chose, de façon cohérente.
7. Écrire un titre qui énonce la conclusion.
8. Faire relire à quelqu'un qui ne connaît pas le sujet ; itérer.
