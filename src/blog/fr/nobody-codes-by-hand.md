---
title: "Personne ne code à la main : comment nous sommes passés de 4 à 25 contributeurs sur notre data platform"
description: "Chez Optic 2000, personne ne code à la main : 25 contributeurs vibe-codent apps et pipelines dans le repository, et tous les autres parlent directement à la donnée via des agents d'IA. La clé n'est pas le modèle : c'est un repository où il n'existe qu'une seule façon de faire les choses."
date: 2026-11-03
---

# Personne ne code à la main : comment nous sommes passés de 4 à 25 contributeurs sur notre data platform

Dans [un précédent article](https://unytics.io/blog/fr/optic-2000-independence/), je décrivais l'architecture que nous avons bâtie chez Optic 2000. En dix mois, nous avons remplacé un socle PostgreSQL historique, absorbé une nouvelle caisse, un nouveau CRM et un nouveau programme de fidélité, et débranché notre outil de BI.

Le chiffre le plus marquant de ce projet n'est pas technique. Sur la même période, l'équipe data platform est passée de 6 à 4 personnes, tandis que le nombre de personnes contribuant au repository data passait de **4 à 25**.

Et aucune d'entre elles ne code à la main.

---

## Une petite équipe ne peut pas être le goulot d'étranglement

Avec quatre migrations simultanées, une petite équipe qui doit traiter chaque demande métier devient un goulot d'étranglement en quelques semaines. C'est le [piège du Ticketing 2.0](https://unytics.io/blog/fr/the-ticketing-2-0-trap/) : l'équipe data prépare, le métier attend.

Il y avait deux issues : recruter, ou permettre aux autres de contribuer. Nous avons choisi la seconde. Mais pour que 25 personnes — dont la plupart ne sont pas ingénieurs — contribuent sans risque, le repository doit être conçu pour ça.

---

## La règle d'or : une seule façon de faire les choses

Toute la plateforme vit dans un **mono-repo Git unique**, régi par une règle : *il n'y a qu'une seule et unique façon d'accomplir chaque tâche, et tout passe par de la configuration déclarative (YAML).*

* **Une seule façon de déclarer une source :** un fichier YAML décrivant le schéma et le chemin de stockage.
* **Une seule façon de créer une fonction :** un fichier Python avec un décorateur maison, et un fichier YAML qui déclare ses besoins de compute et sa planification.
* **Une seule convention pour les modèles dbt**, du staging aux marts.
* **Une seule façon de consommer les métriques :** via la couche sémantique, que ce soit depuis Streamlit ou depuis le serveur MCP.

Par exemple, voici tout ce qu'il faut pour déployer une fonction :

```yaml
compute:
  cpu: 256
  memory: 512
  timeout: 300
schedule: "0 6 * * *"
```

Terraform lit ce YAML et déploie le job sur AWS Lambda ou ECS Fargate. Personne ne touche à la console AWS, n'écrit de Terraform ni ne gère d'infrastructure.

---

## Pourquoi la standardisation rend les agents de code fiables

Comme je l'expliquais dans [Pourquoi Claude Code dans VSCode révolutionne l'analyse de données](https://unytics.io/blog/fr/best-tool-for-deep-dive-analyses/), l'efficacité d'un agent de code dépend moins de l'intelligence brute du LLM que du contexte et des contraintes du projet.

Dans un repository où chaque pipeline est écrit différemment, un agent d'IA doit deviner : il invente des patterns, mélange les conventions et casse la CI.

Dans un repository où il n'existe qu'une seule façon de faire chaque chose, l'agent n'a qu'à copier le bon pattern. La standardisation était une question d'hygiène ; avec les agents de code, elle devient la condition de leur bon fonctionnement.

---

## Deux façons d'entrer : construire ou consommer

### 1. Construire : vibe-coder dans le repository

Un contributeur ouvre le repository avec Claude Code et décrit son besoin. En quelques prompts, l'agent peut connecter une nouvelle source, écrire le YAML, créer les modèles dbt, construire une app Streamlit ou mettre en place une activation de données.

Il n'a pas besoin de lire ni de comprendre le code. Les conventions et la revue s'en chargent.

### 2. Consommer : parler directement à la donnée

Pour la plupart des utilisateurs, il existe un chemin encore plus simple : pas de repository, pas d'éditeur de code, pas de Git. Ils consomment la donnée directement via des agents d'IA basés sur la couche sémantique.

* **OpenWebUI**, notre interface d'IA interne unique, connectée à la couche sémantique via notre serveur MCP — où chaque utilisateur ne voit que ses propres données. Les magasins peuvent aussi venir avec leur propre client d'IA (Claude, ChatGPT, Dust…), et nous pouvons changer de client ou de modèle à tout moment.
* **Des agents embarqués dans nos apps Streamlit :** un playground qui génère des analyses et des dashboards HTML que l'on peut enregistrer et partager, une app pour configurer et planifier des notifications Teams, et des dashboards métiers dotés d'une partie conversationnelle, avec un system prompt spécialisé sur le sujet.

Ce second chemin est de loin le plus accessible. Le premier sert à ce qui doit devenir une partie de la plateforme — et c'est là qu'interviennent les 25 contributeurs.

---

## Gouvernance : qui vérifie un code que personne ne lit ?

Si les contributeurs ne lisent pas leur code, quelqu'un d'autre doit en être garant. Chaque modification passe par une **Pull Request** relue et validée par l'équipe centrale.

Là encore, la standardisation aide : quand tout suit le même pattern, un relecteur repère immédiatement les écarts. Relire un fichier YAML et un modèle dbt qui ressemblent à tous les autres est bien plus rapide que relire du code sur mesure.

---

## Le nouveau métier de l'équipe centrale

L'équipe centrale ne produit plus l'essentiel des dashboards et des pipelines. Son rôle est de :

* maintenir les patterns et conventions que les agents copient ;
* maintenir les briques de la plateforme (déploiement, ingestion, couche sémantique, serveur MCP) ;
* relire et intégrer les contributions.

C'est ainsi qu'une équipe de 4 personnes peut accompagner 25 contributeurs.

---

## Ce que nous apprenons encore

* **La revue devient le chemin critique.** Avec 25 contributeurs, ce qui limite le débit n'est plus la capacité de développement, mais la capacité de revue.
* **Chaque exception a un coût.** Un seul pipeline écrit « différemment, juste pour cette fois » suffit à donner aux agents un second pattern à copier. La standardisation exige une discipline constante.
* **La qualité repose sur l'équipe centrale.** Des contributeurs qui ne lisent pas le code s'en remettent entièrement aux conventions et à la revue. C'est acceptable tant que les deux restent exigeantes.

---

## Ce qu'il faut en retenir

Avec les agents de code, la question n'est plus « qui sait coder ? » mais « notre repository est-il conçu pour qu'un agent ne puisse pas se tromper ? ». En misant sur une seule façon de faire, la configuration déclarative et une revue systématique, nous avons transformé les métiers en contributeurs — et une équipe plus petite en équipe plateforme.

---

*Vous voulez ouvrir votre data platform aux métiers sans perdre le contrôle ? [Parlons-en lors d'un échange data de 30 minutes](https://unytics.io/book-meeting/).*
