---
title: "Un dashboard montre, une data app agit : ce que nos métiers construisent sur la data platform"
description: "Chez Optic 2000, nous pensions que Streamlit servirait à afficher des graphiques. Les métiers en ont fait autre chose : des outils qui remplacent des SaaS, des front-ends au-dessus de SAP et de Salesforce, des agents embarqués. Ce que font ces data apps, ce qu'elles lisent et ce qu'elles écrivent, et ce qui les garde homogènes."
date: 2026-11-12
---

# Un dashboard montre, une data app agit : ce que nos métiers construisent sur la data platform

Dans [Personne ne code à la main](https://unytics.io/blog/fr/nobody-codes-by-hand/), je racontais comment 25 personnes, en majorité des métiers, contribuent aujourd'hui à la data platform d'Optic 2000 sans écrire une ligne de code.

Au départ, nous pensions qu'elles construiraient des dashboards : des graphiques au-dessus de Snowflake. Elles ont construit autre chose. Des outils qui remplacent des logiciels que nous payions. Des interfaces au-dessus de SAP et de Salesforce. Des data apps qui embarquent un agent conversationnel. C'est l'usage que nous avions le moins imaginé, et peut-être celui qui changera le plus la donne.

Cet article décrit ce que sont ces *data apps*, ce qu'elles font exactement — ce qu'elles lisent, et ce qu'elles écrivent —, et ce qui les empêche de tourner au patchwork.

---

## Pourquoi des data apps plutôt qu'un outil de BI

Nos data apps sont écrites en Python, avec Streamlit, dans le repository de la data platform. Ce choix n'allait pas de soi : en quittant son outil de BI historique, Optic 2000 avait d'abord retenu Tableau. Trois raisons nous ont fait changer.

* **Le temps passé.** Notre équipe BI passait un temps phénoménal sur des tâches de clic-bouton, répétitives et laborieuses. En *vibe-codant* ses tableaux de bord avec un agent, elle obtient une bien meilleure expérience pour l'utilisateur final, en une fraction du temps.
* **Un produit, pas un outil interne.** Nos utilisateurs sont d'abord des milliers de personnes en magasin, opticiens et directeurs de magasin. Un magasin doit être servi comme un client : nous lui devons un produit fini, pas un accès à un outil d'analyse.
* **Pas de licence par utilisateur.** Donner ses indicateurs à un gérant de magasin ne coûte rien de plus, comme je l'expliquais dans [mon article sur l'indépendance](https://unytics.io/blog/fr/optic-2000-independence/).

Une quatrième raison s'est imposée ensuite : une data app est du code, dans le même repository que les données qu'elle affiche. Un agent peut donc la construire, et la faire évoluer dans la même Pull Request que le modèle dbt ou la métrique dont elle a besoin.

---

## Ce que les métiers ont construit

### Des outils qui remplacent des SaaS

* **Le géomarketing.** Nous payions un logiciel propriétaire, assez rigide, pour visualiser les zones de chalandise et de concession sur la carte de France. La personne qui en a la charge a entièrement recréé son outil. Il répond enfin à tous ses besoins, et nous supprimons une licence coûteuse.
* **Les liasses fiscales des magasins.** Il fallait les ressaisir à la main chaque année, ou payer très cher un logiciel d'OCR. Une data app les lit désormais automatiquement, et un humain valide. Avec la même qualité.

### Des front-ends pour nos back-ends

Nous n'avons aucune envie de remplacer SAP ou Salesforce : ce sont des back-ends robustes et standards. Mais leurs interfaces sont arides. Optic 2000 a été créé en 1969, et beaucoup de processus y reposent encore sur un export Excel, suivi d'heures de manipulations répétitives, avec un vrai risque d'erreur.

Les métiers construisent donc des front-ends taillés pour leurs processus :

* **le suivi des équipes logistiques**, construit par un chef de projet AMOA à partir des données de SAP ;
* **le cockpit du référentiel magasins**, construit par son responsable pour repérer les incohérences dans Salesforce, comme deux dates d'ouverture qui se chevauchent lors d'un rachat ;
* **l'enrichissement du référentiel magasins**, où un algorithme aide à compléter la fiche d'un magasin.

Nous n'en sommes qu'au début, et les prochains mois serviront à transformer l'essai.

### Des data apps qui embarquent des agents spécialisés

* **Le bilan financier d'un magasin.** Le directeur consulte son bilan et en discute avec un agent spécialisé en finance de l'optique, dont le *system prompt* est écrit pour ce sujet. Il se compare aux magasins similaires, apporte son contexte local, obtient des recommandations.
* **Un playground.** Les utilisateurs y génèrent leurs propres analyses et leurs propres dashboards, en conversant, puis les enregistrent. La data app en héberge aujourd'hui des dizaines, créés par les utilisateurs eux-mêmes : durables, découvrables, partageables, et réunis au même endroit.
* **La planification d'alertes.** Les utilisateurs configurent et planifient des alertes automatiques, branchées sur les indicateurs de la couche sémantique.

Ces mêmes expertises sont aussi exposées par un serveur MCP et des skills : les magasins peuvent interroger leurs données depuis leur propre Claude ou leur propre ChatGPT. Dans tous les cas, les chiffres viennent de la même couche sémantique, et chacun ne voit que ses propres données.

### Des outils pour la plateforme elle-même

La plateforme sert aussi à s'outiller elle-même :

* **un cockpit de suivi des Pull Requests**, au-dessus de Bitbucket : qui doit relire quoi, et quelles exigences restent à satisfaire ;
* **un éditeur visuel de la couche sémantique**, plus digeste que le YAML brut ;
* **un gestionnaire des droits d'accès**, depuis lequel une poignée de managers décident qui peut ouvrir quelle data app.

---

## « Agir » : ce que les data apps lisent, et ce qu'elles écrivent

« Une data app agit » ne veut pas dire que chaque data app écrit dans les systèmes de l'entreprise. Voici où nous en sommes, système par système.

* **Dans SAP, les data apps lisent.** Elles n'y écrivent pas encore. Ce sera la prochaine étape, et elle demandera des garde-fous à la hauteur : des tests, des droits, une validation humaine.
* **Dans Salesforce, c'est la plateforme qui écrit, pas la data app.** La data app d'enrichissement ne pousse rien elle-même dans Salesforce. C'est une fonction de la plateforme, planifiée chaque jour, qui y reporte un enrichissement quand il n'y figure pas encore. Un post-hook dbt écrit lui aussi dans Salesforce. Dans les deux cas, l'écriture passe par du code versionné, relu en Pull Request, et non par un bouton dans une interface.
* **Dans la plateforme elle-même, les data apps agissent déjà.** Valider la lecture d'une liasse fiscale, planifier une alerte, enregistrer un dashboard, accorder un accès : ce sont des gestes de travail, pas des chiffres à lire.

C'est le sens de la formule : un dashboard donne un chiffre à lire ; une data app prend en charge un morceau de processus.

---

## Ce qui empêche le patchwork

Des data apps écrites par des personnes différentes, avec des agents : sans précaution, chacune aurait son style, ses chiffres et ses droits. Quatre choses l'évitent.

* **Des composants communs.** L'équipe BI a créé elle-même une bibliothèque de composants — cartes d'indicateurs, tableaux, graphiques —, et nos skills imposent à l'agent de les utiliser. Des data apps écrites par des personnes différentes ressemblent à un seul et même produit.
* **Des chiffres définis ailleurs.** Les data apps destinées aux magasins s'appuient à 100 % sur la couche sémantique : la logique d'une mesure est définie à un seul endroit, et la data app ne fait que l'appeler et l'afficher. Les mêmes chiffres partout, et une IA qui n'invente rien.
* **Une sécurité que la data app n'écrit pas.** L'authentification est exigée avant qu'une requête n'atteigne la data app, le périmètre de chaque utilisateur est appliqué par la couche sémantique, et les accès se décident hors du repository. Un contributeur ne peut pas oublier un contrôle : il n'y en a aucun à écrire.
* **Une relecture avant la Pull Request.** Avant même qu'une Pull Request soit ouverte, un agent relecteur vérifie que la data app respecte ces règles, et signale tout doublon avec une data app existante.

Je détaille ces mécanismes dans [Ennuyeusement simple](https://unytics.io/blog/fr/boringly-simple-data-platform/), et la revue dans [La plateforme qui apprend](https://unytics.io/blog/fr/the-platform-that-learns/). L'IA ne conçoit pas chaque data app : elle assemble des briques.

---

## Artefacts ou data apps dans Git : où placer le curseur ?

Un artefact, c'est une petite application — un dashboard, un tableau interactif, une page HTML — que l'assistant d'IA génère directement dans la conversation, à partir d'une simple demande. Claude, ChatGPT et la plupart des outils d'analyse conversationnelle en produisent désormais, et la pratique se répand vite chez les métiers : plus besoin d'attendre une équipe data pour avoir son propre écran.

Ces artefacts progressent vite : ils se conservent, se partagent, et se brancheront demain sur les systèmes de l'entreprise. Aura-t-on encore besoin que des métiers vibe-codent des data apps dans un repository ?

Nous y voyons un continuum plutôt qu'une alternative.

* **Pour l'exploratoire et le léger**, un artefact suffit, et il est imbattable en vitesse. C'est le rôle de notre playground, qui donne en plus à ces artefacts un endroit où vivre : un dashboard né dans une conversation privée n'existe pour personne d'autre.
* **Pour ce qui touche aux processus critiques** — ce qui doit être testé, gouverné, déployé sur l'infrastructure de l'entreprise, et à plus forte raison ce qui écrira un jour dans SAP —, nous voulons du code versionné dans Git et validé par Pull Request.

---

## Ce qu'il faut en retenir

Nous pensions donner aux métiers un outil de dashboarding. Ils en ont fait un atelier : ils y remplacent des logiciels, y habillent SAP et Salesforce, y installent des agents. Une équipe data centrale n'aurait pas eu ces idées, parce qu'elle ne vit pas ces processus.

Cela ne tient que parce que les data apps reposent sur le même socle que le reste de la plateforme : un seul repository, des composants communs, des chiffres définis une seule fois, et des écritures qui passent par du code relu.

Posez-vous la question pour votre propre entreprise : **combien de vos processus tiennent encore dans un export Excel ?** Chacun est une data app qui attend son auteur.

*Cet article détaille une partie d'un récit plus large : [Pourquoi vos métiers ne doivent pas être que des consommateurs d'IA (mais aussi des builders)](https://unytics.io/blog/fr/self-service-analytics-builders/).*

---

*Vos métiers jonglent entre un ERP, un CRM et des fichiers Excel ? [Parlons-en lors d'un échange data de 30 minutes](https://unytics.io/book-meeting/).*
