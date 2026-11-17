# Restitution : présentation, démonstration, questions

> 30 minutes : 10 min de démonstration, 5 min d'architecture, 5 min de démarche et difficultés, 10 min de questions (brief §03).
>
> **Diapositives** (14, avec notes du présentateur et captures de secours) : https://claude.ai/artifact/Uvou3wJVtTvQHdhBGFSJSk (privées : à partager depuis le menu Partager, export PDF ou PowerPoint possible).

## Avant de commencer (J-0, 15 min avant)

- [ ] Double-cliquer sur `PO Assist.command` (ou `uv sync` puis `uv run streamlit run app.py`) : l'application s'ouvre sur http://localhost:8007.
- [ ] Barre latérale › **Réinitialiser** ; vérifier dans ⚙️ Réglages que le **mode démo** est activé (par défaut).
- [ ] Pendant la démo, jouer le parcours en direct : 🤖 Agent › **Lancer l'agent** (analyse, ~8 s) › **Importer** ; puis la priorisation ; puis ⚖️ Priorisation › **Lancer la rédaction**. Les résultats sont ceux de vrais passages du skill, calculés à l'avance : le dire au jury (le bandeau 🎬 le rappelle).
- [ ] Ouvrir à côté : un terminal Claude Code dans le dépôt, et l'onglet `handoff/demo/` (un pack et ses résultats).
- [ ] Filet de sécurité : les captures dans `docs/captures/` si l'application ne démarre pas.

## Déroulé des diapositives

| # | Durée | Diapositive | Message clé |
|---|---|---|---|
| 1 | 0:30 | **Le lundi matin de Camille** : 80 feedbacks en 10 semaines, 3 canaux, 30 issues au backlog, un sprint qui démarre aujourd'hui | Le problème n'est pas de lire, c'est de **décider vite et de pouvoir le justifier** |
| 2 | 0:30 | **Ce que fait PO Assist** : Comprendre → Arbitrer → Formaliser, avec Camille qui valide entre chaque étape | Un fil rouge : de la citation client à la story |
| — | **10:00** | **Démonstration** (script ci-dessous) | |
| 3 | 1:30 | **Architecture** : schéma du README (Linear simulé → pack → API Claude, ou skill en repli → import vérifié → Linear) | L'API par défaut, le skill en repli. Le même pack pour les deux : le format et la vérification ne dépendent pas du moteur |
| 4 | 1:30 | **L'IA estime, le code calcule** : tableau des rôles IA / code par pack | Tout chiffre est exact et rejouable ; tout jugement est justifié |
| 5 | 2:00 | **Garde-fous et qualité mesurée** : citations vérifiées, refus avec raison, import idempotent ; puis le tableau 84 % / 96 % / 98 % / 22 sur 22 / 100 % | On ne dit pas « ça marche », on le mesure contre une vérité terrain que l'agent n'a jamais vue |
| 6 | 1:30 | **La démarche** : cycles courts avec portes de validation, journal tenu au fil de l'eau | La trace est dans le dépôt (`docs/sdlc/`) |
| 7 | 2:00 | **Ce qui a changé en route** : pas d'accès au code (→ documentation), pas d'API d'abord (→ skill), puis l'API par défaut avec le skill en repli, P9 annoté à la main (→ règle calculée), biais du Reach (→ bascule) | Les impasses ont amélioré le produit |
| 8 | 1:30 | **L'IA comme équipe** : matrice imposée aux rédacteurs, agents évalués qui ne voient pas la vérité terrain, sous-agents qui ont repéré mes propres erreurs | Déléguer, oui ; sans contrôle, non |

## Script de démonstration (10 min)

| Temps | Écran | Geste | À dire |
|---|---|---|---|
| 0:00 | 🏠 Tableau de bord | Montrer les 5 indicateurs | « 80 feedbacks analysés, 38 besoins distincts dont 14 absents du backlog, et un chiffre qui compte : 39 600 € d'ARR Business à risque. » |
| 1:00 | 🏠 › Thèmes | Montrer T5 et T10 en tête | « Deux sujets dominent : le suivi des candidatures, qui accélère (+6 sur la seconde moitié de la période), et les besoins Business. Ce n'est pas une impression, c'est compté par semaine. » |
| 1:45 | 🏠 › Risques de départ | Cap Rebond en tête | « 36 k€ d'ARR, 120 sièges : ce compte conditionne son renouvellement de mai à une fonctionnalité. » |
| 2:30 | 📥 Feedbacks | Filtrer « Risque de départ », ouvrir l'e-mail de Cap Rebond | « Le texte brut à gauche, l'analyse à droite : 2 demandes extraites, chacune avec sa citation exacte et l'issue du backlog correspondante. » |
| 3:30 | 📥 Feedbacks | Ouvrir SAX-202 (« BUG inbox bloquée ») | « Piège : le client parle de bug, l'agent a compris que c'est la limite de l'offre Free. C'est une question, et un signal pour l'objectif de conversion. » |
| 4:15 | 🧩 Demandes | Activer « Besoins nouveaux », ouvrir la délivrabilité des e-mails | « 4 clients, 4 formulations (spam iCloud, Outlook, Gmail, Hotmail) : l'agent les a regroupées en un seul besoin, qui n'existe pas dans le backlog. » |
| 5:00 | ⚖️ Priorisation | Classement RICE, puis bascule Reach « clients » | « En personnes touchées, les comptes Business écrasent tout. En clients, les bugs B2C remontent. Ce n'est pas à l'IA de trancher : je rends l'arbitrage visible. » |
| 6:15 | ⚖️ Priorisation | Passer l'effort d'un besoin de 8 à 3, ou monter un poids | « Je ne suis pas d'accord avec l'estimation : je corrige, et le classement comme le sprint se recalculent instantanément. » |
| 7:00 | ⚖️ › Proposition | Capacité, reste à faire, Todo non retenus | « Le sprint 8 est déjà surchargé : il reste 9,5 points après le travail en cours. L'agent me dit ce qui ne rentre pas. » |
| 7:45 | ✍️ User stories | Ouvrir la story du tableau de suivi conseiller | « Persona précis, contexte chiffré et cité, critères Gherkin dont un cas sur la confidentialité des candidats, contrôle INVEST, découpage. » |
| 8:45 | ✍️ | **Envoyer vers Linear** sur le besoin nouveau | « L'issue est créée dans Linear, et les 4 feedbacks d'origine y sont rattachés : la boucle est fermée. » |
| 9:15 | 🤖 Agent + ⚙️ Réglages | Montrer le bouton (coût estimé), la progression paquet par paquet, puis les réglages : API par défaut, skill en repli | « En production, c'est l'API : un clic, un coût annoncé, des paquets, un import vérifié. En démo, ce flux est simulé, je le dis. Sans clé, l'outil se replie sur le skill Claude Code, avec le même pack. » |
| 9:45 | 🎯 Qualité | Tableau | « Et voilà comment je sais que je peux lui faire confiance, et où elle se trompe encore : des bugs classés en améliorations. » |

**Démonstration en direct du skill (si le jury le demande)** : Réinitialiser → 🤖 Agent › Exporter l'analyse → dans Claude Code, « traite les packs » → Importer. Prévoir 3 à 4 minutes pour 80 feedbacks ; pour aller vite : `uv run python -m po_assist export analyse --limit 5`.

## Questions probables

| Question | Réponse courte |
|---|---|
| Pourquoi l'API par défaut, et un skill en repli ? | L'API, c'est l'intégration attendue en production : aucun geste manuel, un coût annoncé avant et mesuré après. Le skill garde deux atouts : zéro clé, et un repli quand l'API est indisponible. Les deux traitent le **même pack** et passent par la **même vérification** : changer de moteur ne change que le transport. Le skill est l'architecture qui tourne en production sur saxobeat (257 tâches sur 258 traitées). |
| La démo appelle-t-elle vraiment l'API ? | Non, et le bandeau le dit : le flux API est simulé (aucun appel, rien n'est facturé). Les résultats sont ceux d'un vrai passage de l'agent, calculés à l'avance, et passent par la vraie vérification. Le moteur API est testé avec un client simulé ; un essai réel se fait en une commande avec une clé. |
| Comment évitez-vous les hallucinations ? | 1) Chaque demande doit citer le feedback **mot pour mot**, et l'import le vérifie. 2) Les chiffres sont calculés par le code, jamais par le LLM. 3) Les identifiants sont vérifiés contre le backlog. 4) Mesure contre une vérité terrain. |
| Pourquoi RICE et pas WSJF ? | RICE et MoSCoW sont demandés par le brief et parlent au PO. Le score pondéré réglable couvre les autres critères (ARR à risque, alignement OKR, tendance). WSJF s'ajouterait comme un pack de plus. |
| Le Reach en sièges n'est-il pas biaisé ? | Si, et c'est volontairement visible : la bascule personnes / clients montre l'arbitrage B2B / B2C. Le choix revient au PO, pas à l'agent. |
| Les données sont fictives : qu'est-ce qui prouve que ça marche sur du réel ? | Le produit et le backlog sont réels (saxobeat). Les feedbacks sont modelés sur les vrais retours de son chat intégré, et contiennent 9 types de pièges réalistes. La vraie limite, c'est le volume : 80 feedbacks, pas 8 000. |
| Ça passe à l'échelle ? | Les packs se découpent en parties (comme sur saxobeat, 150 tâches par fichier). Les agrégats sont en SQL et Python, linéaires. À grande échelle, un runner déclencherait le skill automatiquement. |
| Qu'avez-vous vérifié vous-même ? | Chaque porte de cycle, la matrice des données, la lecture d'échantillons, et surtout des tests (30) et une évaluation qui ne dépendent pas de mon jugement. Voir `docs/demarche.md` §4. |
| Que feriez-vous avec une semaine de plus ? | Brancher le vrai Linear (un module), un runner automatique, une vérité terrain pour la priorisation (décisions passées du PO), et des tests utilisateurs avec 2 PO. |
| Pourquoi Streamlit ? | Proportionné : une langue, zéro front à maintenir, testable sans navigateur. Pour un produit, je reprendrais la pile de saxobeat (Django + HTMX). |
| Comment le PO garde-t-il la main ? | Il lance l'agent après avoir vu le coût, il importe après aperçu, il corrige chaque estimation, il choisit les stories, et il est le seul à écrire dans Linear. |
