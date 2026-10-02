# Rituels et réunions — qui, pourquoi, ODJ, CR, diffusion

## Sommaire
1. Règles d'or de toute réunion
2. Catalogue des réunions
3. Matrice de communication : qui reçoit quoi
4. Trame de compte rendu universelle
5. Exemple de CR

---

## 1. Règles d'or

1. **Pas d'objectif, pas de réunion.** L'objectif s'écrit en une phrase avec un verbe de résultat :
   « valider », « décider », « prioriser » — pas « faire un point ».
2. **ODJ envoyé 24-48 h avant** avec les documents à lire. Une réunion de décision sans préparation
   devient une réunion d'information.
3. **Les bonnes personnes** : celui qui décide, ceux qui savent, ceux qui font. Pas plus.
4. **Timeboxer** chaque point ; parking lot pour les sujets hors ODJ.
5. **Conclure à l'oral** : relire les décisions et actions (qui / quoi / quand) avant de sortir.
6. **CR sous 24 h** (48 h max). Un CR envoyé 3 jours après ne sert plus à rien : chacun a déjà sa version.
7. **Le CR vaut validation tacite** : ajouter « Sans retour de votre part sous 48 h, ce CR est considéré
   comme validé. »

## 2. Catalogue

Format : **Organisateur — Participants — Fréquence/durée — Objectif — ODJ type — Sortie — Diffusion du CR**.

### Réunion de lancement (kick-off)
- **Org.** chef de projet (le BA prépare le contenu fonctionnel). **Part.** sponsor, métier, MOE, BA,
  testeurs, exploitation si impactée. **Durée** 1 h 30, une fois.
- **Objectif** : partager objectifs, périmètre, organisation, planning, règles du jeu.
- **ODJ** : contexte et enjeux → objectifs et périmètre IN/OUT → organisation et RACI → planning et
  jalons → gouvernance (instances) → risques connus → prochaines étapes.
- **Sortie** : support + CR. **Diffusion** : tous les participants + sponsor, sous 24 h.

### Entretien individuel de recueil
- **Org.** BA. **Part.** 1 expert métier (+ 1 max). **Durée** 45-60 min.
- **Objectif** : comprendre une activité, ses irritants, ses règles, ses exceptions.
- **ODJ** : son rôle → déroulé d'une journée type → ce qui marche / ce qui coince → cas particuliers →
  données manipulées → attentes.
- **Sortie** : notes structurées, points ouverts. **Diffusion** : synthèse à l'interviewé pour validation.

### Atelier fonctionnel
- **Org.** BA. **Part.** métier concerné (3-6 personnes), PO/RMOA, 1 représentant MOE. **Durée** 1 h 30-2 h.
- **Objectif** : valider un processus, des règles de gestion, une maquette.
- **ODJ** : rappel de l'objectif → rappel de ce qui a été validé → sujets à trancher (un par un) →
  décisions → points ouverts et porteurs.
- **Sortie** : CR d'atelier avec décisions et règles numérotées (RG-xx).
- **Diffusion** : participants + PO/RMOA + chef de projet, sous 24 h.

### Backlog refinement (Agile)
- **Org.** PO (le BA prépare souvent). **Part.** PO, BA, équipe de dev, testeur. **Fréquence** hebdo, 1 h.
- **Objectif** : rendre les US « prêtes » (claires, estimées, testables).
- **Sortie** : US mises à jour dans l'outil (pas de CR séparé ; tracer les décisions en commentaire).

### Daily (Agile)
- **Org.** équipe (Scrum Master facilite). **Durée** 15 min, debout, quotidien.
- **Objectif** : synchroniser et lever les blocages. Pas de résolution de problème en séance : on la sort.
- **Sortie** : aucune formelle ; le BA note dans son journal les blocages qui le concernent.

### Sprint review / démo
- **Org.** PO. **Part.** équipe, métier, parties prenantes. **Fin de sprint**, 1 h.
- **Objectif** : montrer ce qui est fait, recueillir le feedback, accepter ou non les US.
- **Sortie** : US acceptées / refusées, feedback transformé en nouvelles US. **Diffusion** : synthèse courte.

### Rétrospective
- **Org.** Scrum Master. **Part.** équipe seulement. **Sortie** : 1 à 3 actions d'amélioration, pas plus.
- CR : non diffusé hors équipe (confiance).

### Comité de suivi projet (hebdo)
- **Org.** chef de projet. **Part.** chef de projet, BA, lead MOE, lead test, RMOA. **Durée** 45-60 min.
- **Objectif** : piloter l'avancement, les risques, les actions ; préparer les arbitrages pour le COPIL.
- **ODJ** : météo globale → avancement par lot → anomalies (si recette) → risques et problèmes → actions
  (revue du plan d'actions) → points à remonter en COPIL.
- **Sortie** : CR + plan d'actions mis à jour. **Diffusion** : participants, sous 24 h.

### COPIL (comité de pilotage)
- **Org.** chef de projet ; le BA prépare les éléments fonctionnels et de recette. **Part.** sponsor,
  directions métier et SI, chef de projet. **Fréquence** mensuelle ou aux jalons, 1 h.
- **Objectif** : **décider** (arbitrages, go/no-go de jalon, budget, périmètre). Pas un reporting détaillé.
- **ODJ** : décisions attendues (en premier !) → météo et jalons → faits marquants → risques majeurs et
  plans d'action → arbitrages demandés avec options et recommandation → prochaines étapes.
- **Sortie** : relevé de décisions. **Diffusion** : participants + comité de suivi, sous 24-48 h.
- **Règle** : aucune surprise en COPIL — un décideur ne doit jamais découvrir un problème en séance ;
  le prévenir avant en bilatéral.

### Point anomalies (pendant la recette)
- **Org.** lead test ou BA. **Part.** testeurs, BA, lead MOE (ou dev concernés), PO/RMOA pour arbitrer
  la priorité. **Fréquence** quotidienne en campagne, 30 min max.
- **Objectif** : qualifier les nouvelles anomalies, prioriser, suivre les corrections et retests.
- **ODJ** : chiffres du jour (ouvertes / corrigées / retestées / fermées par sévérité) → nouvelles
  anomalies bloquantes et majeures (qualification, porteur, date) → anomalies en retard → livraisons
  prévues → risques sur la date de fin de recette.
- **Sortie** : tableau de suivi mis à jour dans l'outil + CR court (décisions de priorité, dates).
- **Diffusion** : participants + chef de projet, le jour même.

### Go/no-go
- **Org.** chef de projet. **Part.** décideur (sponsor/direction métier), chef de projet, BA/lead test,
  lead MOE, exploitation, support. **Durée** 1 h, avant chaque MEP.
- **ODJ** : rappel des critères de sortie → bilan de recette (couverture, résultats, anomalies
  résiduelles et contournements) → état de préparation MEP (plan, retour arrière, communication) →
  risques → **décision** go / go avec réserves / no-go.
- **Sortie** : PV de décision signé ou validé par mail. **Diffusion** : participants + comité de suivi
  + support/exploitation, immédiatement.

### Point d'étonnement / point avec le manager
- **Org.** le BA. **Part.** manager ou chef de projet. **Durée** 30 min, mensuel.
- **Objectif** : aligner les attentes, remonter les signaux faibles, demander du feedback.

## 3. Matrice de communication — qui reçoit quoi

| Document | Métier | PO/RMOA | Chef de projet | MOE | Testeurs | Sponsor/Direction | Délai |
|---|---|---|---|---|---|---|---|
| CR d'atelier | ✔ participants | ✔ | ✔ | ✔ si présent | — | — | 24 h |
| CR comité de suivi | — | ✔ | ✔ | ✔ | ✔ lead | — | 24 h |
| Relevé de décisions COPIL | ✔ directions | ✔ | ✔ | ✔ lead | ✔ lead | ✔ | 24-48 h |
| Suivi anomalies quotidien | — | ✔ | ✔ | ✔ | ✔ | — | jour même |
| Rapport de campagne | ✔ référents | ✔ | ✔ | ✔ | ✔ | synthèse | fin de campagne |
| PV de recette / go-no-go | ✔ | ✔ | ✔ | ✔ | ✔ | ✔ | immédiat |
| Point hebdo BA | — | — | ✔ | — | — | — | vendredi |

Règle : **le destinataire principal (À) est celui qui doit agir ; en copie (Cc) ceux qui doivent savoir.**
Objet de mail normé : `[Projet] CR <réunion> du JJ/MM – <décision clé>`.

## 4. Trame de CR universelle

```
Objet : [Projet] CR <réunion> du [JJ/MM/AAAA] – [décision clé en 5 mots]

Participants : [noms – rôle]     Absents / excusés : [ ]
Objectif de la réunion : [1 phrase]

1. DÉCISIONS
| # | Décision | Décideur |
|---|---|---|
| D1 | [à compléter] | [ ] |

2. ACTIONS
| # | Action | Porteur | Échéance | Statut |
|---|---|---|---|---|
| A1 | [verbe + résultat attendu] | [1 nom, pas une équipe] | [AAAA-MM-JJ] | À faire |

3. POINTS OUVERTS / RISQUES
| # | Sujet | Porteur | Prochaine étape |

4. SYNTHÈSE DES ÉCHANGES (par point de l'ODJ, 3-5 lignes max chacun)

Prochaine réunion : [date] – [objectif]
Sans retour sous 48 h, ce compte rendu est considéré comme validé.
```

Décisions et actions **en premier** : la plupart des lecteurs ne lisent que ça.

## 5. Exemple (extrait) — CR de point anomalies

```
Objet : [KYC-Refonte] CR point anomalies du 14/10 – 2 bloquantes à corriger avant jeudi

Chiffres : 12 ouvertes (2 bloquantes, 5 majeures, 5 mineures) – 4 corrigées à retester – 31 fermées

DÉCISIONS
D1 – ANO-142 (score de risque non recalculé après changement de pays) passe en bloquante (décideur : PO).

ACTIONS
A1 – Corriger ANO-142 et livrer en REC – Karim (MOE) – 2026-10-16
A2 – Retester ANO-142 + TNR scoring (15 cas) – Med (BA) – 2026-10-17
A3 – Confirmer la date de livraison du lot 3 – Julie (CP) – 2026-10-15

RISQUE : si ANO-142 n'est pas livrée jeudi, la fin de recette glisse d'une semaine (MEP du 30/10 menacée).
```
