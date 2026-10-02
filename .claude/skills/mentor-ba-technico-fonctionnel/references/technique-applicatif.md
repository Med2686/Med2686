# Culture technique et applicative du BA technico-fonctionnel

Objectif : comprendre suffisamment la technique pour spécifier juste, diagnostiquer une anomalie et parler
d'égal à égal avec la MOE — sans faire son travail.

## Sommaire
1. Architecture d'un SI en 5 minutes
2. API REST et Postman
3. SQL pour le BA/testeur
4. Batchs, flux et ordonnancement
5. Environnements et livraisons
6. Outils du quotidien
7. Lire un log / diagnostiquer
8. SI bancaire
9. SI assurance
10. SI énergie

---

## 1. Architecture d'un SI

- **Front** (écran web/mobile) → **back** (règles métier) → **base de données**.
- Les applications échangent par **API** (temps réel), **fichiers/flux** (souvent la nuit, par batch),
  ou **messages** (bus, files type MQ/Kafka).
- Questions de BA à toujours poser : quelle application est **maître** de la donnée ? Qui est appelé en
  temps réel, qui en différé ? Que se passe-t-il si l'appel échoue (rejeu, file d'erreur, alerte) ?
- Un **schéma de flux** simple (applications = boîtes, échanges = flèches avec nature et fréquence) évite
  la moitié des oublis de spécification.

## 2. API REST et Postman

- Une requête = **méthode** + **URL** + **en-têtes** (dont l'authentification) + **corps** (JSON).
- Méthodes : `GET` lire, `POST` créer, `PUT`/`PATCH` modifier, `DELETE` supprimer.
- Codes retour : `200` OK, `201` créé, `400` requête invalide, `401` non authentifié, `403` non autorisé,
  `404` introuvable, `409` conflit, `422` règle métier violée, `500` erreur serveur, `503` indisponible.
- Ce que le BA spécifie pour une API : champs obligatoires/facultatifs, formats, valeurs autorisées,
  règles de gestion, **messages et codes d'erreur métier**, comportement en cas de doublon.
- Tests avec **Postman** : une collection par API, une requête par cas (nominal, champ manquant, valeur
  hors limite, droits insuffisants), des **tests** qui vérifient le code retour et les valeurs.

```json
POST /clients/100245/adresse
{ "pays": "XX", "ville": "Exemple", "dateEffet": "2026-10-14" }
→ 200 { "clientId": 100245, "niveauRisque": "ELEVE", "alerteConformite": true }
```

## 3. SQL pour le BA/testeur

Savoir **lire** et écrire des requêtes de contrôle (lecture seule en recette, jamais de modification sans
accord de la MOE).

```sql
-- Vérifier le niveau de risque d'un client après modification
SELECT c.client_id, c.pays_residence, r.niveau_risque, r.date_calcul
FROM client c
JOIN risque_client r ON r.client_id = c.client_id
WHERE c.client_id = 100245;

-- Compter les clients par niveau de risque (contrôle de volumétrie après un batch)
SELECT niveau_risque, COUNT(*) AS nb
FROM risque_client
GROUP BY niveau_risque;

-- Trouver les incohérences : clients à risque élevé sans alerte
SELECT r.client_id
FROM risque_client r
LEFT JOIN alerte a ON a.client_id = r.client_id AND a.type = 'CONFORMITE'
WHERE r.niveau_risque = 'ELEVE' AND a.alerte_id IS NULL;
```

À connaître : `SELECT/WHERE`, `JOIN` (inner/left), `GROUP BY/COUNT`, `ORDER BY`, `IS NULL`, `LIKE`,
dates. Les requêtes « d'incohérence » (LEFT JOIN … IS NULL) sont les plus utiles en recette.

## 4. Batchs, flux et ordonnancement

- **Batch** : traitement en masse planifié (souvent la nuit) : calculs, échanges de fichiers, purges.
- **Ordonnanceur** (Control-M, $Universe, Autosys…) : enchaîne les batchs selon des dépendances.
- **Flux fichier** : format (CSV, positionnel, XML), nommage, fréquence, contrôles (nombre de lignes,
  totaux de contrôle), traitement des rejets.
- Questions BA : fréquence ? volumétrie ? que fait-on des rejets ? que se passe-t-il si le batch de la
  veille a échoué (rattrapage) ? quelle date de traitement vs date d'effet ?
- Tester un batch en recette : préparer les données → demander le lancement (ou le déclencher si
  autorisé) → contrôler en base (SQL) et les fichiers de sortie → vérifier les rejets et le compte rendu
  d'exécution.

## 5. Environnements et livraisons

| Environnement | Usage |
|---|---|
| DEV | Développement |
| INT | Intégration entre applications |
| REC / QA | Recette fonctionnelle et utilisateur |
| PREPROD | Répétition de MEP, performances, conditions proches de la production |
| PROD | Production |

- Toujours noter **la version testée** (numéro de build/livraison) dans les résultats et les anomalies.
- Exiger une **note de livraison** : contenu, anomalies corrigées, limites connues.
- Les données de recette ne sont pas celles de la production : vérifier qu'elles couvrent les cas à tester.

## 6. Outils du quotidien

- **JIRA** : US, anomalies, tableaux de bord (filtres JQL : `project = KYC AND type = Bug AND priority in
  (Blocker, Critical) AND status != Closed`).
- **XRAY / Squash / ALM** : référentiel de tests, campagnes, exécution, traçabilité exigences ↔ tests.
- **Confluence** : spécifications, CR, glossaire (une page par réunion récurrente, mise à jour au fil).
- **Postman** (API), client SQL (DBeaver, SQL Developer), **Excel** (analyse de données, contrôles).
- **Outils de modélisation** : BPMN (Bizagi, draw.io), maquettes (Figma, Balsamiq).

## 7. Diagnostiquer avant de déclarer une anomalie

1. Reproduire (2 fois) et noter les étapes exactes.
2. Vérifier les prérequis et les données (la donnée de test est-elle correcte ?).
3. Vérifier la spec : est-ce vraiment un écart ou un trou de spec ?
4. Collecter les preuves : capture, heure exacte, identifiant, trace API (code retour, message), requête SQL.
5. Localiser si possible : front (affichage), back (règle), donnée, interface (appel en échec), batch.

Arriver chez la MOE avec « l'API renvoie 200 mais niveauRisque reste FAIBLE en base à 14:32 pour le client
100245 » fait gagner des heures par rapport à « le score ne marche pas ».

## 8. SI bancaire

- **Briques** : core banking (comptes, tenue de position), référentiel clients (tiers), CRM, moteur de
  paiements (SEPA SCT/SDD, instantané, SWIFT), cartes, crédits, épargne, KYC/entrée en relation,
  filtrage (listes de sanctions, PPE), surveillance des opérations (LCB-FT), reporting réglementaire,
  comptabilité, datawarehouse.
- **Réglementaire** : LCB-FT (connaissance client, vigilance, déclarations de soupçon), KYC périodique
  selon le niveau de risque, DSP2 (authentification forte, API ouvertes), RGPD, Bâle III/IV et
  reporting (COREP/FINREP), MiFID II (marchés).
- **Points d'attention recette** : dates de valeur et jours ouvrés, arrondis, devises, multi-entités,
  habilitations fines, piste d'audit, volumétrie des batchs de fin de journée/mois.

## 9. SI assurance

- **Briques** : tarification/devis, souscription, gestion des contrats (avenants, résiliations),
  encaissement/quittancement, sinistres (déclaration, expertise, indemnisation), réassurance, gestion
  des intermédiaires/commissions, actuariat, reporting.
- **Branches** : IARD (auto, habitation, RC) et vie/épargne/prévoyance (versements, arbitrages, rachats,
  bénéficiaires).
- **Réglementaire** : Solvabilité II, DDA (conseil et distribution), RGPD, LCB-FT (assurance vie),
  loi Hamon/résiliation infra-annuelle.
- **Points d'attention recette** : effets de dates (date d'effet, prorata, anniversaire), cycle de vie du
  contrat, calculs de primes et de taxes, éditions (courriers, attestations), rétroactivité des avenants.

## 10. SI énergie

- **Briques** : CRM et souscription, gestion des contrats et offres, relève (compteurs communicants,
  index), facturation (estimation, régularisation, mensualisation), recouvrement, échanges avec le
  gestionnaire de réseau (flux normés), gestion des points de livraison, marchés/trading, SAP IS-U
  fréquent.
- **Réglementaire** : obligations du fournisseur (information, chèque énergie, trêve hivernale), RGPD
  (données de consommation), règles de marché.
- **Points d'attention recette** : changement de fournisseur/déménagement, index estimés vs réels,
  prorata de changement de tarif, taxes et contributions, volumétrie de la facturation cyclique.
