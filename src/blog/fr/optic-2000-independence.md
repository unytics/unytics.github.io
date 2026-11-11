---
title: "L'indépendance chez Optic 2000 : zéro BI propriétaire, infrastructure interchangeable et IA au choix"
description: "Changer de cloud, de BI ou de modèle d'IA sans tout reconstruire : comment nous avons découplé la data platform d'Optic 2000 de ses fournisseurs, en gardant toute la logique métier dans un seul repository."
date: 2026-11-02
---

# L'indépendance chez Optic 2000 : zéro BI propriétaire, infrastructure interchangeable et IA au choix

**Si demain vous vouliez changer de cloud, d'outil de BI ou de modèle d'IA, combien cela vous coûterait-il ?**

Pour la plupart des entreprises, la réponse est une migration de plusieurs mois : leur logique métier — sources, métriques, dashboards — est dispersée dans les outils de leurs fournisseurs.

Chez **Optic 2000**, où j'ai pris la tête de la data platform en janvier dernier, nous l'avons reconstruite pour que la réponse soit : peu. Voici comment.

---

## Le lock-in a trois étages

Quand on parle de dépendance à un fournisseur, on pense d'abord à l'infrastructure. C'est pourtant rarement là que l'enfermement coûte le plus cher.

1. **L'infrastructure** — le cloud, le warehouse. C'est l'étage que tout le monde surveille.
2. **La BI et les métriques** — souvent le lock-in le plus tenace. Vos définitions de métriques vivent dans le modèle sémantique propriétaire d'un éditeur, et vous payez une licence pour chaque collaborateur qui veut consulter un chiffre. Changer de cloud est un projet ; changer d'outil de BI, c'est réécrire chaque métrique et chaque dashboard.
3. **L'IA** — un étage nouveau, et le plus mouvant. Le meilleur modèle change tous les quelques mois. S'enfermer dans une seule solution d'IA, c'est se condamner à rater les suivantes.

À chaque étage, nous avons appliqué la même règle.

---

## Le principe : la configuration est un actif, le métal est une commodité

Toute la logique métier d'Optic 2000 vit dans **un seul repository Git** : les sources de données, les transformations, les définitions de métriques, les apps, les planifications. Elle y est décrite de façon déclarative, en YAML et en code, indépendamment de la technologie qui l'exécute.

Par exemple, voici comment on déclare les besoins d'une fonction de traitement :

```yaml
get_crm:
  schedule: cron(0 4 * * ? *)
  timeout: 600
  memory: 2048
```

Ces quelques lignes décrivent *ce que* l'on veut. Elles ne disent rien du *comment* : aujourd'hui, la fonction est déployée sur AWS ; demain, elle pourrait l'être ailleurs sans être modifiée.

Les fournisseurs ne fournissent que le moteur. La logique métier — ce qui a de la valeur et ce qui coûte cher à reconstruire — reste chez nous.

```
┌────────────────────────────────────────────────────────┐
│ IA : OpenWebUI, Claude, ChatGPT, Dust, modèle local    │  ← au choix
├────────────────────────────────────────────────────────┤
│ Usages : apps Streamlit, agents, serveur MCP           │  ← ouverts
├────────────────────────────────────────────────────────┤
│ Logique métier : sources, métriques, transformations   │  ← l'actif, dans un seul repo
├────────────────────────────────────────────────────────┤
│ Métal : AWS, S3, Snowflake, DuckDB                     │  ← interchangeable
└────────────────────────────────────────────────────────┘
```

---

## Étage 1 — Une infrastructure interchangeable

Nous utilisons AWS pour le compute, S3 pour le stockage et Snowflake pour le warehouse. Mais aucun de ces choix n'est gravé dans la logique métier.

Prenons l'ingestion. Chaque source est décrite par un fichier YAML : son schéma, son emplacement de stockage. Aujourd'hui, cette configuration pilote Snowpipe, qui charge la donnée dans Snowflake. Demain, le même fichier pourrait piloter une simple fonction serverless qui écrit dans DuckDB. **La configuration ne change pas, les données non plus : seul le moteur change.**

Changer de fournisseur d'infrastructure devient un chantier circonscrit — réécrire un module de déploiement — et non une migration de plateforme.

---

## Étage 2 — Zéro BI propriétaire

Nous avons débranché l'outil de BI historique et, après un passage par Tableau, nous ne l'avons remplacé par aucun autre outil de BI propriétaire.

Nos métriques sont définies une seule fois, dans une **couche sémantique** qui vit dans le repository. Nos dashboards sont des **applications Streamlit open source**, connectées à cette couche sémantique. Résultat : plus de licence par utilisateur — donner ses KPIs à un gérant de magasin ne coûte rien de plus — et des apps qui vont au-delà du dashboard. *Les dashboards sont passifs. Les Data Apps agissent.*

Nos métriques ne dépendent pas non plus du warehouse. Selon la requête, la couche sémantique s'exécute sur Snowflake ou sur DuckDB, qui charge en mémoire les données d'un magasin pour répondre en quelques millisecondes. Les mêmes définitions, deux moteurs : la preuve concrète que nos métriques ne sont enfermées nulle part.

Si chaque dashboard doit être codé, n'a-t-on pas recréé une file de tickets vers l'équipe data ? Non : 25 contributeurs vibe-codent ces apps, et beaucoup de besoins passent directement par des agents d'IA. Je le raconte dans [Personne ne code à la main](https://unytics.io/blog/fr/nobody-codes-by-hand/).

---

## Étage 3 — L'IA au choix

La couche sémantique est exposée via un **serveur MCP** (Model Context Protocol) — un protocole ouvert qui permet à n'importe quel assistant d'IA d'interroger nos métriques.

En interne, nous utilisons une interface unique basée sur OpenWebUI. Les magasins peuvent venir avec leur propre client — Claude, ChatGPT, Dust. Dans tous les cas, l'IA répond avec des chiffres certifiés, et **chaque utilisateur ne voit que ses propres données**.

Surtout, **nous pouvons changer de client d'IA ou de modèle à tout moment**, sans toucher aux métriques. Quand un meilleur modèle sort, nous pouvons l'adopter sans attendre qu'un éditeur l'intègre.

---

## Pourquoi un seul repository change tout

Avoir toute la logique métier au même endroit a des effets qui vont au-delà de la réversibilité :

* **Elle appartient à l'entreprise.** Versionnée, auditable, lisible — et non dispersée dans les interfaces de cinq éditeurs.
* **Une évolution, un seul endroit.** Ajouter une source, la transformer, en tirer une métrique et l'afficher dans une app se fait dans une même Pull Request, cohérente de bout en bout.
* **Les agents d'IA voient toute la plateforme.** Un agent de code qui lit le repository comprend l'ensemble. C'est ce qui nous a permis de passer de 4 à 25 contributeurs, comme je le détaille dans [Personne ne code à la main](https://unytics.io/blog/fr/nobody-codes-by-hand/).

---

## Ce que ça rapporte

* **Pas de taxe par siège :** l'accès aux KPIs ne coûte plus une licence par utilisateur — finis les quelque 50 € par personne et par mois.
* **L'IA de demain sans migration :** changer de modèle ou de client d'IA ne touche pas aux métriques.
* **Un rapport de force sain avec les fournisseurs :** quand on peut partir, on négocie autrement.
* **Pas de migration « big bang » :** chaque brique se remplace indépendamment.
* **Et la vitesse :** quatre chantiers majeurs absorbés en dix mois, pendant que l'équipe passait de 6 à 4 personnes.

---

## Les limites

* **Notre couche sémantique est maison.** C'est du code à maintenir. Nous l'avons construite pour la performance (plusieurs backends) et pour des calculs propres à notre métier, et nous pourrions revoir ce choix à mesure que les standards ouverts mûrissent.
* **Nous n'avons pas encore quitté de fournisseur.** Faire tourner nos métriques sur deux moteurs montre que le découplage fonctionne, mais la réversibilité se prépare : elle ne se prouve vraiment qu'en partant.

---

## Ce qu'il faut en retenir

Être indépendant ne veut pas dire se passer de fournisseurs. Nous utilisons AWS, Snowflake et Claude, et nous en sommes satisfaits. Ce qui compte, c'est l'endroit où vit votre logique métier : dans votre repository, sous forme de configuration et de code — pas dans l'outil d'un éditeur.

Posez-vous la question pour votre propre plateforme : si demain vous vouliez changer de cloud, de BI ou de modèle d'IA, combien de temps cela prendrait-il ?

---

*Votre facture BI grimpe, votre stack vous enferme, ou vous voulez mettre l'IA sur des données fiables sans vous lier à un éditeur ? [Parlons-en lors d'un échange data de 30 minutes](https://unytics.io/book-meeting/).*
