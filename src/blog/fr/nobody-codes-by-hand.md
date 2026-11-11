---
title: "Personne ne code à la main : comment nous sommes passés de 4 à 25 contributeurs sur notre data platform"
description: "Chez Optic 2000, personne ne code à la main : en dix mois, le nombre de contributeurs à la data platform est passé de 4 à 25, en majorité des métiers. L'équipe BI d'abord, puis les métiers du siège : comment nous les embarquons, ce qui se passe quand l'un d'eux s'en va, et ce que cela change pour l'équipe data."
date: 2026-11-03
---

# Personne ne code à la main : comment nous sommes passés de 4 à 25 contributeurs sur notre data platform

Dans [un précédent article](https://unytics.io/blog/fr/optic-2000-independence/), je décrivais l'architecture que nous avons bâtie chez Optic 2000, en dix mois et plusieurs migrations simultanées.

Le chiffre le plus marquant de ce projet n'est pas technique. Sur la même période, l'équipe data platform est passée de 6 à 4 personnes, tandis que le nombre de personnes contribuant au repository data passait de **4 à 25**. Dix-sept d'entre elles ne font partie d'aucune équipe data : ce sont des métiers.

Et aucune ne code à la main.

Cet article raconte comment c'est arrivé : par qui nous avons commencé, comment nous embarquons un métier, et ce que cela change pour l'équipe data.

---

## Une petite équipe ne peut pas être le goulot d'étranglement

Avec autant de chantiers à la fois, une petite équipe qui doit traiter chaque demande métier devient un goulot d'étranglement en quelques semaines. C'est le [piège du Ticketing 2.0](https://unytics.io/blog/fr/the-ticketing-2-0-trap/) : l'équipe data prépare, le métier attend.

Il y avait deux issues : recruter, ou permettre aux autres de contribuer. Nous avons choisi la seconde. Mais laisser des non-développeurs modifier le repository central de la data platform ? J'étais moi-même très sceptique. Nous avons donc procédé par étapes, en commençant par les plus proches de nous.

---

## Première étape : notre propre équipe BI

Historiquement, la data chez Optic 2000, c'étaient trois équipes étanches :

* **quatre data engineers**, qui géraient l'ingestion et les transformations, dans des procédures stockées PostgreSQL ;
* **deux BI engineers**, qui administraient la couche sémantique dans MicroStrategy ;
* **quatre personnes à la BI**, qui construisaient les dashboards en clic-bouton.

Cette équipe BI savait lire un peu de SQL. Elle n'avait jamais touché à Git, à Python ni à dbt.

En quittant MicroStrategy, Optic 2000 avait d'abord choisi Tableau, et l'équipe BI y passait un temps phénoménal, sur des tâches répétitives et laborieuses. Nous lui avons proposé un test : construire ses tableaux de bord sous forme de data apps Streamlit, en *vibe-codant* dans notre repository, avec l'IA. Elle était elle-même sceptique : est-ce que ce sera propre ? Est-ce que les chiffres seront justes ? Est-ce qu'on saura le maintenir ?

En quelques semaines, le déclic a été spectaculaire :

* l'équipe est devenue **autonome** sur Streamlit ;
* l'expérience de l'utilisateur final est **bien meilleure**, pour une fraction du temps que nous passions sur Tableau ;
* et surtout, elle ne s'est pas arrêtée là : d'elle-même, elle s'est mise à créer et à maintenir **ses propres modèles dbt**.

Aujourd'hui, nous sommes passés de trois équipes à deux : quatre data engineers, quatre personnes à la BI, et plus de couche intermédiaire. La BI maîtrise toute la chaîne, du modèle dbt jusqu'à la data app, et Streamlit est devenu notre outil de dashboarding, y compris pour des milliers d'utilisateurs en magasin. Les data engineers, eux, posent le cadre et accompagnent ceux qui construisent.

---

## Deuxième étape : les métiers du siège

Quand nous avons vu notre équipe BI créer des modèles marts impeccables, sans aucun bagage logiciel au départ, nous nous sommes dit : pourquoi s'arrêter là ?

Nous sommes allés voir les métiers du siège : les chefs de projet AMOA, le contrôle de gestion, la finance, la comptabilité, le marketing digital. Des profils analytiques, qui suivent leurs chiffres au quotidien, mais qui n'avaient jamais écrit une ligne de code.

**Tout a commencé par de petits sujets.** Une cheffe de projet s'est construit une data app de suivi de ses tickets Jira, pour mieux piloter ses chantiers. Rien de stratégique. Mais c'est ainsi que la confiance s'installe : la sienne, et la nôtre.

**Puis les sujets sont devenus critiques.** Le responsable du référentiel magasins, dans Salesforce, doit tenir à jour un référentiel qui bouge en permanence, avec des rachats et des ouvertures. Avant, c'est nous qui écrivions des tests dbt sur ce référentiel : quand un test tombait en erreur, nous le prévenions, et il corrigeait après coup. Aujourd'hui, il s'est construit son propre cockpit, bien plus détaillé que nos tests. Quand un magasin est racheté, par exemple, les dates d'ouverture de l'ancien et du nouveau ne doivent pas se chevaucher. Il voit les incohérences, et il peut être proactif. Ces règles de gestion, c'est lui qui les connaît. Pas nous.

**Et certains vont très vite.** Un chef de projet AMOA, qui connaît SAP et travaille avec la logistique, a rapatrié des données de SAP dans Snowflake, les a mises en qualité selon nos conventions, et a construit un dashboard opérationnel de suivi des KPI des équipes logistiques. En une seule conversation.

*Le détail — tout ce que les métiers construisent, bien au-delà des dashboards — est dans [Un dashboard montre, une data app agit](https://unytics.io/blog/fr/data-apps-beyond-dashboards/).*

---

## La barrière à l'entrée est quasi nulle

Il faut casser un mythe : contribuer à un repository ne demande plus de savoir coder. Ces collaborateurs n'écrivent pas de code. Ils ne le lisent même pas. Et ils ne tapent aucune commande Git. **Ils conversent** avec Claude, dans VS Code ou directement dans Claude Desktop, sans même ouvrir d'éditeur. Ils décrivent leur besoin ; en quelques prompts, l'agent peut connecter une nouvelle source, écrire le YAML, créer les modèles dbt, construire une data app Streamlit, puis gérer la branche, le commit et la Pull Request.

Embarquer un métier tient en deux réunions, et un peu de préparation entre les deux :

1. **Une première réunion.** Nous installons les outils sur son poste — vingt minutes —, nous lui montrons comment nous travaillons, et nous cherchons ensemble les sujets qui auraient du sens pour lui.
2. **Entre les deux, nous préparons le terrain.** Nous mettons en place la récupération des données et nous initialisons une data app Streamlit, pour un premier cas d'usage dont nous avons parlé.
3. **Une seconde réunion.** Le métier prend le clavier, et itère lui-même sur sa data app.

Sur nos quatre data engineers, une personne travaille à plein temps à embarquer et à accompagner les métiers.

Tout le monde n'a pas vocation à construire pour autant. Il faut une appétence analytique, et au siège, personne n'y est obligé. Quant aux magasins, ils sont les clients de la plateforme : ils parlent à leurs données à travers des agents d'IA, embarqués dans leurs data apps ou branchés sur notre serveur MCP, sans repository, sans éditeur de code et sans Git. Ce chemin-là est de loin le plus accessible, et beaucoup de besoins y trouvent leur réponse. Le repository sert à ce qui doit devenir une partie de la plateforme.

---

## Et quand un contributeur s'en va ?

On pourrait craindre que tout ce travail ne tienne qu'à ses auteurs. C'est l'inverse. Avant, les métiers fabriquaient déjà leurs propres outils, mais dans l'ombre : des fichiers Excel sur mesure, avec du VBA par exemple. Quand la personne partait, tout était perdu. Aujourd'hui, tout est dans la plateforme, écrit selon nos standards : n'importe qui peut le reprendre, avec Claude.

---

## Le nouveau métier de l'équipe data

L'équipe plateforme ne produit plus l'essentiel des dashboards et des pipelines. Son rôle est de :

* maintenir les patterns et les conventions que les agents copient ;
* maintenir les briques de la plateforme (déploiement, ingestion, couche sémantique, serveur MCP) ;
* embarquer et accompagner ceux qui construisent ;
* relire et intégrer les contributions.

C'est ainsi qu'une équipe de 4 personnes peut accompagner 25 contributeurs.

Le métier de l'équipe BI change lui aussi. Hier, elle répondait à des tickets, en clic-bouton. Libérée de l'un et de l'autre, elle devient proactive : souvent, les métiers n'ont pas seulement besoin d'un chiffre de plus, ils ont besoin d'un regard extérieur pour repenser leur façon de travailler. Et le chantier est immense : Optic 2000 a été créé en 1969, et beaucoup de ses processus sont encore manuels.

---

## Pourquoi cela ne tourne pas au chaos

Vingt-cinq personnes et leurs agents dans le même repository : l'objection vient aussitôt. Et de fait, avec 25 contributeurs, **la revue devient le chemin critique** : ce qui limite le débit n'est plus la capacité de développement, mais la capacité de revue. Trois choses la rendent tenable, chacune détaillée dans son article.

* **Le repository est conçu pour cela.** Dans un repository où il n'existe qu'une seule façon de faire chaque chose, l'agent n'a qu'à copier le bon pattern. C'est le sujet d'[Ennuyeusement simple](https://unytics.io/blog/fr/boringly-simple-data-platform/).
* **Un concept n'a qu'un seul nom.** L'agent ne choisit jamais entre trois synonymes. C'est le sujet d'[Un nom, une définition](https://unytics.io/blog/fr/one-name-one-definition/).
* **Chaque raté devient une règle.** Aucun de nos garde-fous n'existait au départ, et une Pull Request nous arrive aujourd'hui déjà relue par un agent. C'est le sujet de [La plateforme qui apprend](https://unytics.io/blog/fr/the-platform-that-learns/).

---

## Ce qu'il faut en retenir

Avec les agents de code, la question n'est plus « qui sait coder ? » mais « notre repository est-il conçu pour qu'un agent ne puisse pas se tromper ? ». Le reste est une affaire de méthode : commencer par l'équipe la plus proche de soi, puis par un métier volontaire sur un sujet sans enjeu, et laisser chaque raté devenir une règle. C'est ainsi que nous avons transformé les métiers en contributeurs — et une équipe plus petite en équipe plateforme.

Posez-vous la question pour votre propre entreprise : **combien d'outils métier y vivent dans un fichier Excel que seul son auteur sait faire tourner ?** Chacun de ces auteurs est un contributeur qui s'ignore.

*Cet article détaille une partie d'un récit plus large : [Pourquoi vos métiers ne doivent pas être que des consommateurs d'IA (mais aussi des builders)](https://unytics.io/blog/fr/self-service-analytics-builders/).*

---

*Vous voulez ouvrir votre data platform aux métiers sans perdre le contrôle ? [Parlons-en lors d'un échange data de 30 minutes](https://unytics.io/book-meeting/).*
