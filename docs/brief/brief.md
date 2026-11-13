# Construire un agent IA au service d'un Product Owner

> **Test technique · Product Builder** (Thiga) · **30 min de restitution**
> Transcription intégrale et autonome du sujet. Le PDF d'origine ([edc-product-builder.pdf](edc-product-builder.pdf)) est conservé en archive, mais ce document suffit.

## Les trois livrables en bref

1. **Agent fonctionnel** : code source et tests, outils au choix.
2. **Documentation** : démarche et choix techniques.
3. **Présentation** : démonstration de l'agent en action.

---

## 01 · Contexte

Une **startup SaaS** développe une **plateforme de gestion de projet**. Son Product Owner est submergé par les **feedbacks clients** et les **demandes de fonctionnalités**, qui lui arrivent par plusieurs canaux (emails, tickets, commentaires).

Il doit dans le même temps **reprioriser le backlog en permanence**, et il a besoin d'un assistant intelligent qui l'aide à prendre ses décisions.

**Votre mission : concevoir et construire un agent IA qui assiste ce Product Owner au quotidien**, sur trois tâches qui lui prennent du temps : analyser les feedbacks clients, prioriser les fonctionnalités et rédiger les user stories.

Aucun jeu de données n'est fourni. Vous constituez vous-même les exemples (feedbacks, demandes, éléments de backlog) sur lesquels vous ferez la démonstration.

*Mots-clés : Startup SaaS · Gestion de projet · Feedbacks multicanaux · Backlog à prioriser · User stories*

---

## 02 · Fonctionnalités attendues

### Analyse des feedbacks (COMPRENDRE)

- Traiter les feedbacks clients : emails, tickets, commentaires
- Identifier les motifs récurrents et les tendances
- Extraire les demandes de fonctionnalités

### Aide à la priorisation (ARBITRER)

- Proposer un scoring des fonctionnalités selon différents critères
- Appliquer des frameworks de priorisation (MoSCoW, RICE…)
- Expliquer et justifier ses recommandations de priorisation

### Rédaction assistée (FORMALISER)

- Générer des user stories structurées selon les standards
- Proposer des critères d'acceptation pertinents
- Estimer la complexité relative de développement

> **Les trois blocs sont attendus.** La profondeur avec laquelle vous traitez chacun d'eux relève de vos arbitrages et est évaluée au titre de la complétude. Rien ne vous empêche d'aller au-delà.

---

## 03 · Livrables attendus

### 1. Agent fonctionnel

Le code source de votre agent, dans le langage et avec le framework de votre choix.

- Les fonctionnalités des trois blocs, utilisables sur vos exemples
- Les tests que vous jugez nécessaires

### 2. Documentation

Un document qui explique votre démarche et vos choix techniques. Format libre.

- Votre démarche : comment vous êtes passé du problème à l'agent (hypothèses, étapes, itérations, impasses), ce que vous avez délégué aux assistants IA et ce que vous avez vérifié vous-même
- Vos choix techniques et ce qui les motive

### 3. Présentation et démonstration

30 minutes devant le jury : 20 minutes de présentation, dont la moitié consacrée à montrer l'agent en action, puis 10 minutes de questions.

| Durée | Séquence | Contenu |
|---|---|---|
| 10 min | **Démonstration** | L'agent en action sur des cas concrets |
| 5 min | **Architecture** | Architecture et choix techniques |
| 5 min | **Démarche & difficultés** | Le chemin suivi, les obstacles et leurs solutions |
| 10 min | **Questions** | Échange avec le jury sur vos choix |

---

## 04 · Critères d'évaluation

| Critère | Poids | Ce qui est évalué |
|---|---|---|
| **Compréhension métier** | 20 % | Les enjeux du Product Owner sont compris : des feedbacks qui le submergent et un backlog à reprioriser en permanence. L'agent l'aide concrètement à prendre ses décisions. |
| **Démarche** | 20 % | Le chemin du problème à l'agent est lisible : les hypothèses posées, ce qui a été essayé puis abandonné, la façon dont l'IA a été mise à contribution et contrôlée. |
| **Qualité technique** | 15 % | Architecture, code et tests. La solution fonctionne, ses composants s'articulent logiquement et les choix techniques restent proportionnés au besoin. |
| **Expérience utilisateur** | 15 % | Simplicité et efficacité d'usage : un Product Owner peut se servir de l'agent sans friction. |
| **Complétude** | 10 % | Jusqu'où la réflexion a été poussée : couverture des fonctionnalités attendues et profondeur de traitement de chacune. |
| **Présentation** | 20 % | Clarté et pédagogie, pendant la présentation comme dans les réponses aux questions. La démonstration montre l'agent sur des cas concrets et les choix sont expliqués. |

---

## 05 · Format & modalités

| | |
|---|---|
| **Préparation** | **Libre** : aucune durée imposée ; langage, framework, modèles et outils au choix. |
| **Restitution** | **30 minutes** : 20 min de présentation + 10 min de questions. |
| **Ressources autorisées** | **Tout, assistants IA compris** : usage à décrire dans la documentation, le jury vous interrogera dessus. |

> **Rappel :** le sujet est volontairement ouvert. Au-delà des fonctionnalités attendues, le périmètre, la forme et les outils sont à votre main, et nous aimons être surpris. Nous attendons une solution réfléchie, que vous savez défendre, plutôt qu'une solution parfaite. Les assistants IA sont autorisés parce que vous les utiliserez en mission. Pour toute question sur le sujet, n'hésitez pas à nous contacter.
