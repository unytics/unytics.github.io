---
title: "Pourquoi Claude Code dans VSCode révolutionne l'analyse de données"
description: "Claude Code dans VSCode est le meilleur outil pour les analyses approfondies — fin du Shadow Data, Shift Left et construction de la plateforme en explorant."
date: 2026-04-17
---

# Pourquoi Claude Code dans VSCode révolutionne l'analyse de données

Dans mon dernier article, j'écrivais sur [pourquoi j'ai quitté la direction de 100+ ingénieurs](/blog/fr/why-i-left-managing-100-engineers/). Replonger dans l'opérationnel donne une perspective neuve sur les points de friction qui ralentissent les équipes.

Aujourd'hui, j'en suis arrivé à une conclusion définitive : **Claude Code dans VSCode est le meilleur endroit pour réaliser des analyses de données.** Ce n'est pas une amélioration marginale ; c'est un véritable changement de paradigme.

Pour comprendre pourquoi, il faut d'abord regarder l'état actuel des outils data modernes.

---

## Le point de départ : la Semantic Layer, c'est génial, mais...

Il y a une conviction répandue en ce moment selon laquelle l'analytics conversationnel au-dessus d'une semantic layer serait le Saint Graal. Et effectivement, c'est absolument génial. Placer un agent conversationnel — comme Omni ou Snowflake Intelligence — au-dessus de vos marts permet non seulement aux métiers de récupérer n'importe quel chiffre ou graphique à partir de données propres, mais aussi d'exécuter des analyses avancées : analyse de causes racines, analyse du churn, segmentation client ou calculs de Lifetime Value (LTV).

**Mais cela ne couvre pas tous les cas d'usage.** Cette approche ne fonctionne *que* sur des données Marts (les données les plus préparées pour la consommation par la BI). Si un point de données, une table intermédiaire ou une dimension spécifique n'est pas déjà méticuleusement modélisé et exposé dans cette semantic layer, il est complètement invisible pour l'agent.

Quand on se heurte à ce « mur de la curation », il reste deux grands défis analytiques qu'un agent conversationnel standard ne peut tout simplement pas résoudre.

---

## 1. Explorer les données physiques dans le lineage

Pour vraiment comprendre vos données, un **catalogue de données** robuste est la voie à suivre. C'est là qu'on explore les données, qu'on navigue le lineage, qu'on vérifie les aperçus de données, qu'on consulte les statistiques de profiling et qu'on lit la documentation. Comme le catalogue est l'endroit naturel pour l'exploration, y ajouter une fonctionnalité de **Q&R en langage naturel** prend tout son sens :

* **Apprentissage contextuel :** Quand vous consultez le lineage ou le schéma d'une table spécifique, vous devriez pouvoir poser des questions sur la table directement, sur place.
* **Capitalisation des connaissances :** Les réponses à ces questions ne devraient pas disparaître. En persistant les résultats des Q&R directement sur la page de documentation, vous enrichissez le catalogue pour tout le monde. La prochaine personne qui se pose la même question trouve la réponse déjà prête.

**Comment nous faisons chez Optic 2000 :**
Nous avons construit un portail data custom directement au-dessus de notre dépôt Git pour remplir ce rôle. En intégrant les Q&R dans ce portail, nous avons transformé la documentation technique en une ressource métier vivante où la connaissance persiste et grandit.

---

## 2. Le Deep Dive : briser le cycle du Shadow Data

Le second grand défi est le deep dive. C'est là que le paradigme change véritablement et que Claude Code réécrit entièrement les règles. Pour comprendre pourquoi les deep dives sont si douloureux, il faut reconnaître le plus grand secret de polichinelle du secteur. Comme le dit Yoann Boudon, CDO d'Optic 2000 :

> « Un data analyst passe généralement 80 % de son temps à récupérer les données, et 20 % à faire l'analyse — et c'est dans le meilleur des cas. »

**Quand on analyse un sujet inconnu, la semantic layer ne va <u>PAS</u> vous aider.**

Dans une configuration traditionnelle, un deep dive est un processus en stop-and-go. On commence une analyse, on réalise qu'il manque une colonne ou qu'on a besoin d'une nouvelle source brute, on change d'outil et on écrit un pipeline — tuant ainsi tout élan.

### L'ancienne façon de travailler (et pourquoi c'était pénible)
Traditionnellement, les Analystes et les Data Engineers vivaient dans deux mondes différents. Quand un analyste avait besoin de nouvelles données pour un deep dive, il faisait face à un choix frustrant :

1. **Le piège du ticket :** Ouvrir un ticket pour que le Data Engineer ajoute la colonne ou la source dans dbt. Comme l'analyste a besoin de réponses *maintenant*, attendre plusieurs jours le cycle de sprint n'est pas viable.
2. **Le chemin de l'ombre :** L'analyste prend un raccourci. Il extrait les données brutes dans un CSV local, un notebook séparé ou un schéma « sandbox ». Il refait un travail déjà fait ailleurs, créant des **Shadow Data Transforms**.

Ce « chemin de l'ombre » est un désastre pour l'entreprise. La logique utilisée dans ce deep dive n'est jamais réintégrée dans la base de connaissances globale.

Même dans des entreprises comme Nickel où les data analystes sont responsables des transformations, le fait de changer d'outil — utiliser dbt pour le pipe et un autre outil pour l'exploration — crée un fossé mental et technique qui mène au même travail redondant et isolé.

### La révolution du « Shift Left »
Claude Code dans VSCode brise ce cycle. Il permet à l'analyste de faire un **« Shift Left »** — se déplacer directement dans le dépôt où la curation se fait.

Parce que Claude a une visibilité complète sur vos sources brutes et vos transformations dbt, il élimine ces 80 % de friction de récupération des données. Au lieu de jongler entre les outils, tout se fait dans une **<u>seule conversation</u>** :

* **Piping des données à la volée :** Claude peut repérer des colonnes intéressantes dans les sources brutes et les remonter jusqu'à vos marts — en respectant exactement vos conventions de code — avant de les utiliser dans l'analyse.
* **Fin du Shadow Logic :** Puisque le travail se fait à l'intérieur du dépôt, la logique de transformation est commitée, testée et documentée. Le « deep dive » ne produit pas seulement un slide ; il produit une **amélioration permanente de votre plateforme data**.
* **Correction de code :** Il lit votre dépôt, identifie les erreurs dans votre logique et les corrige en cours de route. Il comprend vos règles métier et en propose de nouvelles pour résoudre le problème.

---

## La révolution du workflow : construire des « Skills »

Chaque fois que nous réalisons une analyse dans VSCode, nous construisons et affinons en réalité un **Claude Skill**. C'est un méta-prompt spécialisé qui garantit que chaque analyse suit un modèle de haute qualité :

* **Synthèses orientées objectif et impact :** Commencer par un objectif et présenter les résultats en premier pour les dirigeants.
* **Documentation persistante :** Le skill met automatiquement à jour la documentation data avec les conclusions qui doivent rester dans le dépôt sur le long terme.
* **Profondeur technique :** Chaque requête SQL est incluse pour l'auditabilité, mais rangée dans des sections repliables (admonitions).

### Du dépôt à la salle de direction
Parce que ces analyses sont écrites en fichiers Markdown à l'intérieur du dépôt Git, elles sont automatiquement exposées dans notre **Portail Data**. Les dirigeants obtiennent des rapports homogènes et de haute fidélité, toujours liés au code.

Nous ne changeons pas seulement les outils que nous utilisons ; nous mettons fin à l'ère du « Shadow Data » cloisonné et **<u>nous donnons aux analystes le pouvoir de construire la plateforme tout en réalisant leurs analyses</u>**.
