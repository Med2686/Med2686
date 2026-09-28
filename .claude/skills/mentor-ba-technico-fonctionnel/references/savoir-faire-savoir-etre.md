# Savoir-faire et savoir-être — la posture du BA technico-fonctionnel senior

## Sommaire
1. La posture en une phrase
2. Savoir-faire clés
3. Savoir-être clés
4. Posture selon l'interlocuteur
5. Situations délicates : posture, phrases types, escalade
6. Escalade graduée
7. Grille d'auto-évaluation hebdomadaire

---

## 1. La posture en une phrase

**Le BA est le garant neutre de la bonne compréhension entre le métier et la technique** : il ne décide pas
à la place du métier, ne code pas à la place de la MOE, mais rien ne passe sans qu'il ait vérifié que c'est
compris, écrit, testable et décidé par la bonne personne.

## 2. Savoir-faire clés

| Savoir-faire | En pratique |
|---|---|
| **Questionner** | Questions ouvertes d'abord (« Comment ça se passe aujourd'hui ? »), puis fermées pour valider. Les « 5 pourquoi » pour remonter du symptôme au besoin. « Et si… ? » pour trouver les exceptions. |
| **Reformuler** | « Si je comprends bien, quand un client change de pays, son score doit être recalculé immédiatement, c'est bien ça ? » — évite 80 % des malentendus. |
| **Traduire** | Au métier : impacts, délais, options. À la MOE : règles, données, cas limites, critères d'acceptation. Jamais de jargon technique au sponsor. |
| **Écrire pour être lu** | Conclusion en premier, une idée par paragraphe, tableaux pour les données, objet de mail explicite. Test : lisible en 30 secondes sur un téléphone. |
| **Faciliter** | Timeboxer, faire parler les silencieux, recadrer les digressions (« Je le note dans le parking lot, on y revient en fin de réunion »), conclure par décisions et actions. |
| **Dire non avec une alternative** | « Pas dans ce sprint, mais je peux le proposer en priorité au prochain refinement. » Un non sec ferme la discussion ; un non avec option la fait avancer. |
| **Structurer l'incertitude** | Transformer « on ne sait pas » en point ouvert avec porteur et échéance. |
| **Chiffrer** | « 3 bloquantes, 12 cas KO sur 140 » plutôt que « il reste des problèmes ». Les faits désamorcent les tensions. |
| **Lire la technique** | Ouvrir une trace d'API, lancer une requête SQL de contrôle, lire un log : arriver chez la MOE avec un diagnostic, pas une impression. |

## 3. Savoir-être clés

- **Neutralité** : tu représentes le besoin, pas un camp. Ne jamais dire « la MOE a encore planté » devant
  le métier, ni « le métier ne sait pas ce qu'il veut » devant la MOE.
- **Fiabilité** : faire ce qu'on a dit, quand on l'a dit. Si tu vas être en retard, préviens avant
  l'échéance, pas après. C'est la base de la crédibilité.
- **Écoute active** : laisser finir, reformuler, noter. Le silence après une question fait souvent sortir
  l'information importante.
- **Affirmation sans agressivité** : exprimer un désaccord sur les faits, pas sur les personnes. Méthode
  DESC : **D**écrire les faits → **E**xprimer l'impact → **S**pécifier ce que tu proposes → **C**onséquence
  positive.
- **Calme sous pression** : en recette et en MEP, tout le monde stresse. Celui qui reste factuel devient
  la référence.
- **Humilité active** : « Je ne sais pas, je vérifie et je reviens vers vous avant 16 h » vaut mieux
  qu'une réponse approximative.
- **Curiosité** : aller voir les utilisateurs travailler, comprendre les contraintes de la MOE et de
  l'exploitation.
- **Courage** : remonter un risque tôt, même s'il déplaît. Un risque tu est un problème reporté.

## 4. Posture selon l'interlocuteur

| Interlocuteur | Il attend de toi | Ta posture | À éviter |
|---|---|---|---|
| **Métier / utilisateurs** | Être compris, ne pas perdre de temps | Curieux, pédagogue, reformule dans ses mots | Jargon SI, promettre une date à la place de la MOE |
| **PO / RMOA** | Des éléments pour décider et prioriser | Force de proposition : options + recommandation | Décider à sa place |
| **MOE / développeurs** | Des spécs claires, stables, testables | Partenaire technique, précis, factuel | Imposer une solution technique, changer la spéc oralement |
| **Testeurs** | Des critères clairs, des données, des arbitrages | Référent fonctionnel disponible | Requalifier une anomalie sans eux |
| **Chef de projet** | Visibilité, pas de surprise | Transparent, synthétique, alerte tôt | Minimiser un retard |
| **Sponsor / direction** | Décisions à prendre, risques, impacts business | Synthétique : 3 messages, options chiffrées | Détails techniques, problèmes sans solution |
| **Exploitation / support** | Anticipation (MEP, procédures) | Les associer tôt | Les découvrir la semaine de la MEP |

## 5. Situations délicates

### Le métier change d'avis en cours de réalisation
- **Posture** : ne pas refuser, rendre le coût visible et faire décider.
- **Phrase** : « C'est possible. Pour que vous puissiez décider en connaissance de cause : cette évolution
  impacte 3 US déjà développées, soit environ 5 jours et un décalage de la recette. On l'intègre
  maintenant ou au lot suivant ? »
- **Écrit** : tracer la demande et la décision (CR ou commentaire JIRA).

### La MOE conteste une anomalie (« c'est une évolution »)
- **Posture** : revenir au référentiel, sans affect.
- **Phrase** : « Regardons la règle RG-12 de la SFD validée le 03/09 : elle prévoit le recalcul. Si la
  spéc est ambiguë, on la clarifie avec le PO et on requalifie ensemble. »
- **Si pas de référentiel** : c'est un trou de spéc → point ouvert, arbitrage PO, et leçon pour la suite.

### Pression pour valider une MEP malgré des anomalies
- **Posture** : tu n'es pas le décideur du go, tu es le garant de l'information.
- **Phrase** : « Je ne peux pas recommander un go sans réserve : 2 bloquantes restent ouvertes, dont une
  sans contournement. Je propose trois options : report d'une semaine, go avec désactivation de la
  fonctionnalité X, ou go avec réserves signées par le métier. »
- **Écrit** : les réserves figurent dans le PV. Ne jamais signer seul un PV qui masque un risque.

### Le périmètre gonfle (scope creep)
- **Phrase** : « Bonne idée. Je l'ajoute au backlog ; au prochain refinement, on la priorise face au reste
  avec le PO. »

### Un acteur clé ne répond pas / bloque
- Relance écrite courte avec échéance → relance orale → point bilatéral → escalade (voir §6).
- **Phrase de relance** : « Sans retour de votre part d'ici jeudi, je considère la règle RG-08 validée
  telle que proposée, pour ne pas bloquer le développement. »

### Tu as fait une erreur
- Le dire vite, avec l'impact et la correction : « J'ai oublié le cas des clients mineurs dans la SFD. Impact :
  2 cas de test à ajouter, pas d'impact planning. La mise à jour est en ligne. » La transparence renforce la
  crédibilité ; la dissimulation la détruit.

### Réunion qui dérape (conflit, digression)
- Recentrer sur l'objectif : « Je propose qu'on revienne à la décision attendue aujourd'hui. Ce sujet est
  important : je le note et j'organise un point dédié avec les bonnes personnes. »

## 6. Escalade graduée

1. **Direct** : échange avec la personne concernée (oral puis écrit).
2. **Relance tracée** : mail avec échéance et impact.
3. **Manager de proximité / chef de projet** : informer, pas accuser (« pour information et appui »).
4. **Comité de suivi** : point inscrit à l'ODJ avec faits et options.
5. **COPIL** : arbitrage demandé, avec recommandation.

Règle : on n'escalade jamais sans avoir prévenu la personne concernée (« Je vais devoir le remonter en
comité de suivi jeudi pour qu'on trouve une solution »). Escalader n'est pas dénoncer : c'est demander de
l'aide pour débloquer.

## 7. Grille d'auto-évaluation hebdomadaire (vendredi, 5 min)

Noter de 1 à 4 :
1. Mes CR sont partis sous 24 h.
2. Chaque action a un porteur unique et une échéance.
3. J'ai reformulé avant de spécifier.
4. J'ai alerté tôt sur au moins un risque (ou il n'y en avait pas).
5. J'ai tenu mes engagements de la semaine ou prévenu avant.
6. J'ai été neutre entre métier et MOE.
7. J'ai appuyé mes messages sur des faits chiffrés.
8. J'ai dit non avec une alternative quand il le fallait.
9. J'ai appris quelque chose de technique ou de métier.
10. J'ai demandé du feedback à quelqu'un.

Puis 3 lignes : ce qui a marché / ce que j'ai évité / ce que je change la semaine prochaine.
