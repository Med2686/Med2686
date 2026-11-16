# Pilotage : risques, priorisation, modélisation, traçabilité, changement, RGPD

## Sommaire
1. Registre RAID (risques, actions, problèmes, décisions)
2. Priorisation
3. Estimation
4. Modélisation
5. Traçabilité exigences ↔ tests
6. Conduite du changement
7. RGPD et confidentialité

---

## 1. Registre RAID

- **R**isque : peut arriver (incertain). **A**ction : à faire. **I**ssue/problème : est déjà arrivé.
  **D**écision : tranchée, par qui, quand.
- Un risque bien écrit : « **Si** [cause], **alors** [conséquence], **ce qui** [impact métier/planning]. »
  Ex. « Si l'environnement de recette n'est pas livré le 12/10, alors la campagne démarre en retard, ce
  qui menace la MEP du 30/10. »
- Cotation : probabilité (1-3) × impact (1-3). ≥ 6 → plan d'action et remontée en comité.
- Réponse : éviter, réduire, transférer, accepter (et l'écrire).

| ID | Risque (si… alors… ce qui…) | P | I | Score | Plan d'action | Porteur | Échéance | Statut |
|---|---|---|---|---|---|---|---|---|
| R1 | [à compléter] | | | | | | | Ouvert |

## 2. Priorisation

- **MoSCoW** : Must (sans ça, pas de MEP) / Should (important, contournable) / Could (confort) /
  Won't (pas cette fois, écrit). Simple, parlant pour le métier. Garde-fou : les Must ne devraient pas
  dépasser ~60 % de la capacité.
- **Valeur / effort** : matrice 2×2 → quick wins d'abord, gros paris à arbitrer, le reste en bas.
- **WSJF** (SAFe) : (valeur métier + urgence + réduction de risque) / taille. Utile quand plusieurs
  métiers se disputent la capacité.
- **Kano** : basiques (attendus, leur absence mécontente), performances, enthousiasmants.
- Règle : **le BA propose, le PO/métier tranche**, et la décision est tracée.

## 3. Estimation

- Le BA n'estime pas le développement, mais il estime **son propre travail** (ateliers, spécs, cas de
  test, exécution) et challenge la cohérence des estimations.
- Ordres de grandeur utiles pour la recette : conception ≈ 30-45 min par cas simple, exécution ≈ 15-30 min
  par cas, + 20-30 % pour retests et anomalies, + TNR. À ajuster avec l'historique du projet.
- En Agile : points d'histoire en planning poker ; le BA apporte la clarté qui réduit l'écart d'estimation.

## 4. Modélisation

| Besoin | Outil | Quand |
|---|---|---|
| Processus métier | BPMN (couloirs par acteur, tâches, décisions, événements) | Recueil AS-IS / TO-BE |
| Qui fait quoi avec le système | Cas d'utilisation UML | Cadrage fonctionnel |
| Enchaînement entre applications | Diagramme de séquence | Interfaces, API |
| Cycle de vie d'un objet | Diagramme d'états | Dossier, contrat, anomalie |
| Données | Modèle conceptuel, dictionnaire de données, mapping source → cible | Interfaces, reprise, reporting |
| Découpage du produit | Story mapping | Agile, construction du backlog |

Conseil : un schéma simple validé vaut mieux qu'un schéma parfait que personne ne lit. Toujours faire
valider le processus TO-BE par le métier avant d'écrire la spéc.

**Mapping de données (trame)** :

| Champ source | Appli source | Format | Champ cible | Format | Règle de transformation | Obligatoire | Valeur par défaut | Commentaire |

## 5. Traçabilité exigences ↔ tests

| Exigence / US | Règle | Cas de test | Dernier statut | Anomalies liées |
|---|---|---|---|---|
| US-345 | RG-12 | CT-KYC-012, CT-KYC-013 | OK | — |

Elle répond à deux questions de go/no-go : « tout a-t-il été testé ? » et « qu'est-ce qui est impacté
par cette anomalie ? ». Dans XRAY/Squash, elle est native si les liens sont faits au fil de l'eau.

## 6. Conduite du changement

Une MEP réussie techniquement peut échouer si les utilisateurs n'adoptent pas.

1. **Analyse d'impact** : par population, qu'est-ce qui change (processus, écrans, rôles, volumes) ?
   Impact fort / moyen / faible.
2. **Plan de communication** : quoi, à qui, quand, par qui (le sponsor pour le pourquoi, le BA pour le
   comment).
3. **Formation** : supports courts (guide pas à pas, vidéo de 3 min, FAQ), sessions ciblées, formation
   des relais/key users.
4. **Accompagnement au démarrage** : hypercare, relais sur le terrain, canal de questions.
5. **Mesure** : indicateurs d'usage, remontées du support, enquête rapide à 1 mois.

| Population | Changement | Impact | Action | Canal | Date | Porteur |

## 7. RGPD et confidentialité

- Données de recette **fictives ou anonymisées** ; jamais d'extraction de production non anonymisée.
- Spécifier pour toute donnée personnelle : finalité, base légale, durée de conservation, droits
  d'accès, purge. Associer le DPO dès qu'un nouveau traitement de données personnelles apparaît.
- Captures d'écran d'anomalies : masquer les données personnelles.
- Dans le journal de mission : pas de données nominatives de clients finaux ni d'informations
  confidentielles non nécessaires.
