# Recette et test fonctionnel — la casquette testeur

## Sommaire
1. Niveaux et types de tests
2. Stratégie de test fondée sur les risques
3. Techniques de conception de cas de test
4. Rédiger un bon cas de test
5. Jeux de données
6. Anomalies : qualification, cycle de vie, fiche
7. TNR (tests de non-régression)
8. Indicateurs et reporting
9. Critères d'entrée / de sortie et go/no-go

---

## 1. Niveaux et types de tests

| Niveau | Qui | Quoi |
|---|---|---|
| Tests unitaires | MOE | Chaque composant |
| Tests d'intégration | MOE / intégrateur | Interfaces entre composants et applications (API, flux, batchs) |
| Recette fonctionnelle (système) | Équipe de test / BA | Conformité aux spécifications, bout en bout dans l'application |
| Recette utilisateur (VABF / UAT) | Métier, accompagné par le BA | Adéquation au besoin réel, processus métier complets |
| Pré-production / VSR | Exploitation + métier | Fonctionnement en conditions réelles, volumétrie |

Types transverses : TNR, tests de performance, sécurité/habilitations, tests de reprise de données,
tests d'exploitabilité (batchs, relances, supervision).

## 2. Stratégie fondée sur les risques

On ne teste jamais tout : on teste **d'abord ce qui coûterait le plus cher s'il cassait**.

**Risque = probabilité de défaut × impact métier.**
- Probabilité élevée : code nouveau ou très modifié, règles complexes, interfaces, reprise de données,
  équipe nouvelle.
- Impact élevé : argent (paiements, facturation), réglementaire (KYC, LCB-FT, reporting), client final,
  volume, image.

| Priorité | Couverture attendue |
|---|---|
| P1 (risque fort) | Nominal + erreurs + limites + TNR associés, testés en premier |
| P2 | Nominal + principaux cas d'erreur |
| P3 | Nominal, ou tests exploratoires |

**Plan de la stratégie** : contexte et périmètre → risques et priorités → niveaux et types de tests →
environnements et données → outils → organisation et rôles → circuit des anomalies → critères
d'entrée/sortie → livrables → planning.

## 3. Techniques de conception

- **Classes d'équivalence** : découper les valeurs en groupes traités de la même façon, un cas par
  groupe. Ex. âge : <18 / 18-65 / >65.
- **Valeurs limites** : tester juste avant, sur, et juste après chaque limite (17, 18, 19 ; 65, 66).
  C'est là que se cachent la plupart des bugs.
- **Table de décision** : pour les règles à plusieurs conditions. Ex. scoring KYC :

| Pays à risque | PPE | Activité sensible | Niveau de risque attendu |
|---|---|---|---|
| Oui | Oui | – | Élevé |
| Oui | Non | Oui | Élevé |
| Oui | Non | Non | Moyen |
| Non | Oui | – | Élevé |
| Non | Non | Oui | Moyen |
| Non | Non | Non | Faible |

- **Transitions d'état** : pour les objets à cycle de vie (dossier, contrat, sinistre, anomalie) : tester
  chaque transition autorisée ET les transitions interdites.
- **Parcours métier (bout en bout)** : un scénario suit un processus complet à travers plusieurs écrans
  et applications (ex. entrée en relation → KYC → ouverture de compte → premier virement).
- **Tests exploratoires** : sessions timeboxées (60-90 min) avec une charte (« explorer la modification
  d'adresse avec des caractères spéciaux »), en complément, jamais en remplacement.

## 4. Rédiger un bon cas de test

| Champ | Contenu |
|---|---|
| ID | CT-KYC-012 |
| Titre | Recalcul du score quand le pays de résidence passe à un pays à risque |
| Exigence / US couverte | RG-12 / US-345 |
| Priorité | P1 |
| Prérequis | Client X en statut actif, risque Faible, résidence France |
| Données | Client test ID 100245 (anonymisé) |
| Étapes | 1. Ouvrir la fiche client 2. Modifier le pays de résidence en « Pays Y » 3. Valider |
| Résultat attendu | Score recalculé immédiatement, niveau Élevé, alerte créée dans la file conformité |
| Résultat obtenu / statut | OK / KO / Bloqué / Non exécuté |

Règles : un cas = un objectif ; résultat attendu **vérifiable** (valeur, message, statut, ligne en base) ;
pas de « vérifier que ça marche ». En Agile, les critères d'acceptation en Gherkin se transforment
directement en cas de test :

```
Étant donné un client actif résidant en France avec un risque Faible
Quand son pays de résidence est modifié en un pays de la liste à risque
Alors son niveau de risque devient Élevé
Et une alerte est créée dans la file conformité
```

## 5. Jeux de données

- Préparer les données **avant** la campagne (demande à la MOE ou script SQL d'injection).
- Couvrir chaque classe d'équivalence et chaque cas de la table de décision.
- **Anonymiser** : jamais de données réelles de clients en recette (RGPD). Utiliser des données fictives
  ou anonymisées.
- Tenir un référentiel : ID de la donnée → cas de test → état attendu (et prévoir leur réinitialisation).

## 6. Anomalies

**Sévérité** (impact technique/métier, fixé par le testeur/BA) vs **priorité** (urgence de correction, fixée
par le PO/RMOA). Une anomalie peut être mineure mais prioritaire (faute sur un écran client) ou majeure
mais peu prioritaire (fonction utilisée une fois par an).

| Sévérité | Définition |
|---|---|
| Bloquante | Empêche un processus métier ou le test de continuer, pas de contournement |
| Majeure | Fonction importante incorrecte, contournement possible mais coûteux |
| Mineure | Défaut limité, contournement simple |
| Cosmétique | Libellé, affichage, sans impact fonctionnel |

**Cycle de vie** : Nouvelle → Qualifiée (acceptée/rejetée/doublon/évolution) → Assignée → Corrigée →
Livrée en recette → Retestée → Fermée (ou Réouverte).

**Fiche anomalie** : titre explicite (quoi + où + condition), environnement et version, étapes pour
reproduire, résultat attendu (avec référence à la règle), résultat obtenu, preuves (capture, log, requête
SQL, trace API), données utilisées, sévérité, cas de test lié.

Une anomalie non reproductible par la MOE revient toujours : c'est la qualité de la fiche qui fait la
vitesse de correction.

## 7. TNR

- Objectif : vérifier que ce qui marchait marche toujours.
- Constituer un socle : parcours critiques (P1) + zones fréquemment impactées + anomalies déjà corrigées.
- Les rejouer à chaque livraison significative et avant chaque MEP.
- Candidats à l'automatisation : stables, répétitifs, à données maîtrisées (API, calculs). Le reste en manuel.

## 8. Indicateurs et reporting

| Indicateur | Pourquoi |
|---|---|
| Avancement : cas exécutés / prévus | Tenir le planning |
| Taux de succès : OK / exécutés | Qualité du livré |
| Couverture : exigences couvertes / total | Rien d'oublié |
| Anomalies ouvertes par sévérité, et leur âge | Où est le risque |
| Cas bloqués | Dépendances (environnement, données, livraison) |
| Taux de réouverture | Qualité des corrections |

Reporting quotidien (5 lignes) : chiffres du jour → bloquants → livraisons attendues → risque sur la date
de fin → besoin d'arbitrage.

## 9. Critères d'entrée / de sortie et go/no-go

**Entrée** (on démarre si) : version livrée avec note de livraison, tests d'intégration passés,
environnement disponible et stable, jeux de données prêts, cas de test validés.

**Sortie** (on termine si, exemple) : 100 % des P1 exécutés, ≥ 95 % des cas exécutés, 0 bloquante
ouverte, majeures ouvertes ≤ seuil convenu avec contournement documenté, TNR passés.

**Go/no-go** : le BA présente les faits et une recommandation ; **le décideur décide**. Trois issues :
go, go avec réserves (listées, contournements, date de correction, signées par le métier), no-go (avec
nouvelle date et conditions).
