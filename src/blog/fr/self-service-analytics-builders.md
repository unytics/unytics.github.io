---
title: "Self-Service Analytics : pourquoi vos métiers ne doivent pas être que des consommateurs d'IA (mais aussi des Builders)"
description: "Le conversational analytics et les boucles de rétroaction proactives transforment l'accès à la donnée. Mais dans une entreprise aux opérations complexes, il faut aller plus loin : ouvrir le mono-repo aux métiers pour qu'ils deviennent les Builders de la plateforme et de leurs applications opérationnelles."
date: 2026-11-16
---

# Self-Service Analytics : pourquoi vos métiers ne doivent pas être que des consommateurs d'IA (mais aussi des Builders)

*Cet article est le miroir écrit de mon talk donné lors de la Forward Data Conference 2026 : « L'analyse qui construit la plateforme : dites adieu au Ticketing 2.0 ».*

En juin dernier, l'équipe Data d'Anthropic a publié un retour d'expérience passionnant sur la façon dont elle a construit son propre *self-service analytics* interne avec Claude. Leurs chiffres résument à eux seuls le défi de toute notre industrie en 2026.

En branchant directement Claude « à froid » sur leur Data Warehouse pourtant très propre, **le taux de réponses exactes plafonnait à 21 %**. En construisant un *harness* rigoureux en quatre couches — tables canoniques, couche sémantique, *Skills* documentés et validation automatisée — **ils ont fait grimper la précision à plus de 95 %**. Mais le chiffre le plus instructif vient après : un mois seulement après le lancement, sans maintenance continue, **la précision de leur agent avait déjà chuté de 95 % à 65 %** sous l'effet de l'évolution naturelle des schémas et du produit. Pour maintenir le cap, **près de 90 % des Pull Requests** touchant un modèle de données chez Anthropic incluent désormais une mise à jour de *Skill* dans le même diff Git.

Quelques semaines plus tard, Olga Berezovsky publiait une analyse remarquée sur son Substack (*« Self-Service Analytics Is Not Self-Service. But Don't Tell Anyone »*) en soulignant un détail : pour faire tourner cette mécanique, Anthropic emploie environ **30 professionnels de la data — soit près de 2 % des effectifs totaux de l'entreprise**. Sa conclusion : *« Il faut tout un village d'analystes »* pour faire fonctionner le self-service par l'IA.

Faut-il vraiment une armée en central ? Pas nécessairement : aujourd'hui, des équipes ultra-modernes prouvent qu'avec une boucle de rétroaction IA bien pensée, 2 ou 3 personnes suffisent à servir toute une scale-up.

Pourtant, en observant l'état de l'art actuel, je reste convaincu que notre écosystème s'arrête en chemin. Tout le monde cherche à perfectionner l'expérience des métiers en tant que **consommateurs conversationnels** (*Consumers*). Chez Optic 2000, nous avons fait le pari d'aller un cran plus loin : **permettre aux métiers de devenir eux-mêmes des Builders de la plateforme et de leurs applications opérationnelles.**

---

## 💬 Acte 1 : L'état de l'art du « Context Engineering » — et pourquoi ça marche redoutablement bien

Depuis quinze ans, les équipes data poursuivent le même objectif : casser les silos et rendre les équipes métiers autonomes, parce que l'autonomie est le plus puissant levier de valeur d'une entreprise.

Avec le *conversational analytics*, ce rêve est devenu tangible. Et les équipes les plus avancées ont résolu le problème des « 21 % de précision » d'Anthropic en industrialisant trois rôles bien distincts :

1. **Les Data Platformers**, qui construisent le *harness* technique (le mono-repo, le serveur MCP, la CI/CD, les évals).
2. **Les Builders (l'équipe Data)**, qui modélisent la donnée et maintiennent le contexte métier dans le *harness*.
3. **Les Consumers (les métiers)**, qui interrogent la donnée en langage naturel via Claude, Slack ou leurs outils de BI.

---

### 🏆 L'excellence du modèle proactif : Jolimoi, Gorgias, Photoroom...

Soyons parfaitement honnêtes : lorsqu'elle est poussée à son maximum, cette organisation est d'une efficacité redoutable.

Regardez ce que font des équipes comme **Gorgias** (où 83 % des employés posent plus de 1 000 questions par jour grâce au *Context Engineering*) ou **Photoroom** (où Juliette Duizabo explique comment 3 personnes côté Data servent toute l'entreprise).

Dans un éditeur de logiciel ou une scale-up de 60 à 150 personnes sans opérations physiques lourdes, avoir 2 ou 3 personnes à la Data (soit ces fameux 2 %) est tout à fait raisonnable. Surtout quand l'équipe centrale passe d'un mode réactif à une **boucle de rétroaction ultra-proactive** comme chez Jolimoi :

| Brique de la boucle proactive | Ce que cela change concrètement |
| ----- | ----- |
| **Capture automatique des impasses** | Dès qu'un utilisateur *Consumer* pose une question à laquelle le MCP ne peut pas répondre, l'intention est logguée automatiquement. |
| **Écoute proactive de l'entreprise** | Le système ingère les canaux Slack publics et les transcriptions Google Meet pour détecter les nouveaux sujets métiers avant même qu'une demande ne soit formulée. |
| **Génération automatique de Pull Requests** | Un digest quotidien génère des tickets Linear et ouvre automatiquement des dizaines de Pull Requests par jour pour enrichir les modèles et la couche sémantique. L'équipe centrale n'a plus qu'à relire et valider. |

Avec une telle vélocité, soyons justes : pour 90 % des questions analytiques courantes, la friction disparaît presque entièrement et la perte de sérendipité devient très faible. C'est d'ailleurs exactement cette approche de boucle de rétroaction que nous mettons en place chez Optic 2000 pour nos utilisateurs *Consumers*.

**Alors, si ce modèle fonctionne si bien, pourquoi affirmons-nous qu'il manque une pièce essentielle au puzzle ?**

---

## ⚠️ Acte 2 : Ce que le « Tout-Consumer » ne résout pas — La finesse métier et le passage à l'action

La grande majorité des équipes data cherchent aujourd'hui à copier le modèle d'Alexis Blandin : une petite équipe centrale ultra-efficace qui construit le *harness*, pilote la boucle de feedback et garde le monopole du *build*.

Mais dès que vous sortez du cadre d'un éditeur SaaS homogène pour entrer dans une entreprise aux opérations complexes (comme Optic 2000 avec ses 1 200 magasins, sa logistique, sa finance, ses mutuelles, SAP et Salesforce), **siloter la responsabilité de Builder côté Data et de Consumer côté Métier révèle deux grandes limites.**

### 1. Une petite équipe Data centrale ne maîtrisera jamais la finesse de tous les processus métiers

Chez Optic 2000, nous sommes **8 personnes côté Data à plein temps** : 4 personnes dans l'équipe Data Platform et 4 personnes dans l'équipe BI.

Même avec les meilleurs agents IA du monde, comment 8 personnes en central pourraient-elles prétendre connaître avec finesse toutes les subtilités comptables de SAP, toutes les règles de gestion du référentiel magasin dans Salesforce et toutes les exceptions financières du réseau ? C'est illusoire. **Ce sont les métiers qui connaissent leurs données et leurs processus.**

Si vous interdisez aux métiers qui ont une appétence analytique d'être des *Builders* :

* Vous perdez une efficacité considérable en allers-retours où l'information se déforme à chaque passage de relais (même assistés par IA) entre celui qui connaît le processus métier et celui qui valide le modèle dbt.
* Lors des **analyses approfondies (*deep dives*)** — où 80 % de la valeur se cache dans l'exploration de tables brutes non encore modélisées — l'analyste métier ne peut pas construire le pipeline en même temps qu'il explore. Il reste tributaire d'un aller-retour avec l'équipe centrale (un *Ticketing 2.0*, certes automatisé par des agents et des boucles de feedback, mais un intermédiaire quand même).

### 2. Les métiers n'ont pas seulement besoin d'analyses : ils ont besoin de construire des applications qui agissent

Dans le modèle classique, quand il faut construire de véritables applications qui vont au-delà de l'analyse — par exemple des outils opérationnels connectés en lecture et écriture à SAP, Salesforce ou Bitbucket — c'est encore l'équipe centrale qui doit développer à la place du métier.

Or, avec le *vibe-coding*, les métiers ont désormais la capacité de créer eux-mêmes les outils qui résolvent leurs frictions opérationnelles quotidiennes. Encore faut-il leur en donner le cadre.

---

## 🛠️ Acte 3 : Le modèle Optic 2000 — Compléter le Conversationnel en transformant les métiers en Builders

Chez Optic 2000, notre conviction est simple : **l'approche Consumer dans une interface conversationnelle et l'approche Builder dans VS Code ne s'opposent pas, elles se complètent.**

* On ne va évidemment pas demander à un opticien en magasin ou à un opérateur peu à l'aise avec l'informatique d'ouvrir VS Code sur notre repository Git ! Pour eux, l'interface conversationnelle *Consumer* avec boucle de rétroaction est parfaite.
* Mais se limiter uniquement à l'approche *Consumer* maintient un plafond de verre. C'est pourquoi nos **4 Data Platformers** ont ouvert notre mono-repo Git à nos **4 spécialistes BI** et à **une vingtaine de Builders issus des directions métiers** (contrôle de gestion, finance, responsables référentiels...), portant le total à **25 personnes qui buildent activement la plateforme** — sans qu'aucune d'entre elles ne code à la main.

---

### 🎨 Les 3 espaces où l'on « Vibe-Code » chez Optic 2000

Cette complémentarité s'incarne dans trois espaces de travail distincts sur notre plateforme :

| Espace de Vibe-Coding | Qui l'utilise ? | Ce qu'on y fait concrètement | Comment la plateforme s'enrichit |
| ----- | ----- | ----- | ----- |
| **1. Claude Desktop & OpenWebUI (sur serveur MCP)** | **Consumers** (Magasins, utilisateurs métiers) | Analyse conversationnelle directe sur la couche sémantique avec filtrage strict des droits d'accès. | **Boucle de rétroaction (comme chez Alexis Blandin)** : on ne *builde* pas pendant qu'on analyse, mais les feedbacks génèrent des PRs d'amélioration du YAML. |
| **2. Les Data Apps Streamlit (Playground & IA embarquée)** | **Consumers & Métiers avancés** | Dashboards et applications opérationnelles sur nos SaaS. Certaines apps **embarquent un agent Claude conversationnel** pour analyser les données affichées ou générer ses propres dashboards (voir ci-dessous). | Boucle de rétroaction aujourd'hui — et probablement demain la possibilité de déclencher directement des PRs depuis les agents embarqués dans Streamlit. |
| **3. Le Mono-repo Git dans VS Code (avec Claude Code)** | **Builders (Métiers & BI - ~24 pers.)** & **Data Platformers (4 pers.)** | **On builde en même temps qu'on analyse**. Le métier explore le brut, pipe une ingestion, modélise dans dbt, édite la couche sémantique et vibe-code des apps Streamlit. | **Autonomie complète** : le métier ouvre directement sa Pull Request dans le repo Git pendant son travail. |

---

### 💡 Focus sur l'Espace 2 : Quand les Apps Streamlit embarquent le Conversationnel et les Artefacts

La plupart de nos applications Streamlit sont des dashboards vibe-codés dans VS Code par les métiers ou l'équipe BI. Mais plusieurs d'entre elles hybrident le meilleur de l'application structurée et de l'IA générative :

* **Le bilan financier augmenté par un agent dédié :** Une application Streamlit affiche les bilans financiers d'un magasin. Directement dans l'application, un agent Claude est embarqué avec un *system prompt* financier hardcodé. L'utilisateur final discute avec Claude au sein de l'app pour fouiller son bilan, tester des hypothèses et générer des artefacts HTML complémentaires.
* **L'application Playground (« Claude Dashboards ») :** Nous avons construit une application Streamlit qui sert de générateur et d'hébergeur d'artefacts HTML. Un utilisateur *Consumer* y vibe-code son propre dashboard en mode playground, puis l'enregistre. L'application contient ainsi des dizaines de dashboards créés par les utilisateurs eux-mêmes, pérennes, découvrables, partageables et embarqués au même endroit.
* **L'application de planification d'alertes :** Une app Streamlit permettant aux utilisateurs de configurer et planifier des envois d'emails automatiques branchés sur les indicateurs de notre moteur de mesure.

---

## ⚡ Acte 4 : Au-delà du Read-Only — Les applications opérationnelles construites sur SAP, Salesforce et Git

Lorsqu'un métier devient *Builder* dans VS Code, il ne construit pas uniquement des pipelines analytiques ou des graphiques en lecture seule. Il construit des **applications opérationnelles qui permettent de voir ET d'agir** directement sur les systèmes de l'entreprise.

Voici 6 exemples concrets d'applications vibe-codées chez Optic 2000 :

| Application Vibe-Codée | Système connecté | Usage opérationnel (Voir & Agir) |
| ----- | ----- | ----- |
| **1. Détection & Correction d'incohérences** | **Salesforce** | Vibe-codée par le responsable métier du référentiel magasins : l'app détecte les anomalies dans Salesforce, les affiche clairement et permet au métier de **corriger directement les données dans Salesforce**. |
| **2. Enrichissement Human-in-the-Loop** | **Salesforce** | Des algorithmes calculent des propositions d'enrichissement du référentiel magasin. L'app Streamlit offre l'interface *Human-in-the-Loop* où le métier contrôle et valide avant écriture dans Salesforce. |
| **3. Front-end opérationnel métier** | **SAP** | Un front dédié et sur mesure branché au-dessus de SAP pour offrir des vues claires et exécuter des processus opérationnels précis sans subir la complexité de l'interface SAP native. |
| **4. Cockpit de gouvernance des PRs** | **Bitbucket** | Une interface bien plus lisible que Bitbucket pour suivre toutes les Pull Requests ouvertes, voir en un clin d'œil qui doit relire quoi, et vérifier que toutes nos exigences sont respectées. |
| **5. Éditeur visuel de Semantic Layer** | **Git Repository** | Une interface par-dessus Git pour visualiser et éditer toute la couche sémantique avec validation métier, bien plus digeste que le YAML brut (et qui s'intègre avec les PRs générées par nos boucles de feedback). |
| **6. Gestionnaire des droits d'accès** | **Plateforme Streamlit** | Une application dédiée pour administrer facilement les permissions d'accès à chaque application Streamlit. |

---

### 🤔 Artefacts Claude vs Applications sur Git : où placer le curseur demain ?

Une question légitime se pose : *« Demain, les artefacts générés dans Claude ou dans un playground ne seront plus de simples graphiques en lecture seule. Ils sont déjà pérennes, partageables, bientôt organisables comme un Google Drive, et pourront écrire directement dans Salesforce ou SAP via des connecteurs MCP. Aura-t-on encore besoin que les métiers vibe-codent des applications Streamlit dans VS Code et Git ? »*

La réponse ne sera pas binaire : il s'agira d'un **continuum de maîtrise et de contrôle**.

* **Pour les besoins légers, rapides ou exploratoires :** les artefacts générés à la volée, sauvegardés et partagés dans un espace type Drive (ou dans notre app Streamlit Playground) seront largement suffisants et imbattables en vélocité.
* **Pour les processus critiques d'entreprise :** dès qu'il s'agit d'écrire en masse dans SAP ou Salesforce avec des algorithmes complexes en amont, d'imposer une gouvernance stricte des droits d'accès, de garantir la non-régression par des tests CI et de déployer sur l'infrastructure sécurisée de l'entreprise, **on voudra toujours avoir de vrais fichiers de code versionnés sur Git et validés par Pull Request**.

---

## 🛡️ Acte 5 : Le secret d'architecture — Un Mono-Repo déclaratif pour aligner 25 Builders

Comment permettre à 25 personnes (4 Data Platform, 4 BI et une vingtaine de métiers) de builder dans le même repository Git sans que personne ne code à la main et sans créer le chaos ?

Tout repose sur le *harness* construit par les 4 Data Platformers dans un **mono-repo unique et 100 % déclaratif** :

1. **Une seule façon de faire chaque chose :** Qu'il s'agisse d'ingérer une donnée, de créer un modèle dbt, d'ajouter une métrique dans le semantic layer (comme chez Anthropic où 90 % des PRs unifient modèle et contexte) ou de déployer une app Streamlit sur AWS via Terraform, il n'existe qu'un seul pattern déclaratif. Dans VS Code, Claude Code voit tout le repository et reproduit scrupuleusement nos standards.
2. **L'analyse construit la plateforme (*Deep Dive & Pipe*) :** Guidé par nos *Skills*, un métier qui explore une donnée brute dans VS Code enrichit le modèle dbt et la couche sémantique dans le même mouvement que son analyse.
3. **La revue de PR centralisée :** Les 4 Data Platformers gardent le contrôle final en relisant les Pull Requests (aidés par la CI et notre application Bitbucket) avant toute mise en production.
4. **L'accompagnement des métiers :** Parmi les 4 Data Platformers, l'un d'entre eux est dédié à plein temps à l'accompagnement des métiers pour qu'ils exploitent pleinement la plateforme.

---

## 🎯 Conclusion : Ouvrez votre Harness aux métiers

Le *Conversational Analytics* couplé à une boucle de rétroaction proactive est une avancée majeure. Des équipes réduites de 2 ou 3 personnes comme chez Jolimoi ou Photoroom démontrent tous les jours à quel point cette approche transforme l'accès à la donnée pour les *Consumers*.

Mais ne vous arrêtez pas là. Si votre entreprise possède des processus opérationnels riches et complexes, votre équipe Data centrale — aussi brillante soit-elle — ne remplacera jamais la connaissance intime qu'ont vos métiers de leurs propres données et de leurs propres outils.

Gardez l'approche conversationnelle et les artefacts légers pour la consommation rapide. Mais **ouvrez votre mono-repo et VS Code à vos référents métiers**. Le jour où vos métiers ne se contentent plus de poser des questions à un chatbot, mais deviennent les *Builders* de la plateforme et de leurs propres applications opérationnelles, vous aurez enfin brisé le dernier silo de la data.
