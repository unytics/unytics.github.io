---
title: "Ennuyeusement simple : comment 25 contributeurs modifient notre data platform presque sans relecture"
description: "Chez Optic 2000, 25 contributeurs et leurs agents d'IA modifient la data platform presque sans relecture de l'équipe plateforme. Le secret : une plateforme ennuyeusement simple, où la configuration est séparée de la plomberie de déploiement, où les paramètres sont déduits plutôt que déclarés, où sécurité et supervision sont intégrées, et où les règles attendent l'agent là où il travaille."
date: 2026-11-05
---

# Ennuyeusement simple : comment 25 contributeurs modifient notre data platform presque sans relecture

Dans [Personne ne code à la main](https://unytics.io/blog/fr/nobody-codes-by-hand/), je racontais comment le nombre de personnes contribuant à notre data platform chez Optic 2000 était passé de 4 à 25 — pour la plupart des profils métier, qui travaillent avec un agent de code. Je concluais sur un constat : avec 25 contributeurs, **la revue devient le chemin critique**. Une équipe plateforme de quatre personnes ne peut pas relire tout ce que produisent 25 personnes et leurs agents.

Chaque modification passe toujours par une Pull Request validée par un humain. Mais dans la plupart d'entre elles, il ne nous reste presque rien à relire. Non pas parce que nous faisons davantage confiance aux agents qu'avant, mais parce que nous avons conçu la plateforme pour qu'une erreur soit presque impossible à exprimer dans une contribution.

Notre plateforme est volontairement **ennuyeuse**. Ajouter une source de données, c'est écrire un fichier YAML. Déployer une fonction, c'est un fichier Python et quelques lignes de YAML. Publier une data app, c'est sortir un fichier d'un dossier. Tout ce qui est difficile — infrastructure, sécurité, déploiement, supervision — est écrit une fois, par l'équipe plateforme, dans ce que j'appellerai la **plomberie**. Les contributeurs n'ont jamais besoin d'y toucher, leurs agents non plus.

Cet article décrit les cinq principes qui font cet ennui, et ce qu'ils changent pour une équipe plateforme. Comme dans [Un nom, une définition](https://unytics.io/blog/fr/one-name-one-definition/), les détails techniques sont rangés dans des sections dépliables, pour ceux qui veulent les reproduire.

---

## Pourquoi viser l'ennui

Une data platform contient deux sortes de code. La **configuration** dit *de quoi* l'entreprise a besoin : telle source et ses tables, telle fonction et sa planification, tel rôle et ce qu'il peut lire, telle data app et son propriétaire. La **plomberie** dit *comment* le déployer : permissions cloud, droits dans l'entrepôt, règles de load balancer, définitions de conteneurs, étapes de CI, alertes.

Dans la plupart des plateformes, les deux sont entremêlées. Ajouter une source, c'est copier un module Terraform, ajouter une permission cloud, brancher une notification, déclarer une alerte. Chaque contribution touche à la plomberie, donc chaque revue doit vérifier la plomberie : cette permission est-elle trop large ? Cette règle va-t-elle entrer en collision avec une autre ? L'alerte est-elle branchée ? C'est une revue de spécialiste. Elle ne passe pas à l'échelle de 25 contributeurs, encore moins de leurs agents, qui écriront volontiers une policy parfaitement plausible donnant accès à tous les buckets.

Nous avons fait le choix inverse : **les contributeurs n'écrivent que de la configuration, et la configuration ne peut dire que ce que la plomberie lui permet de dire.** Ce qu'une contribution ne peut pas exprimer, un relecteur n'a pas à le vérifier.

Les équipes data connaissent déjà un outil construit ainsi : dbt. Vous écrivez un modèle SQL, et dbt gère pour vous l'incrémental et l'ordre d'exécution. Nous avons construit tout le repository de cette façon.

C'est encore plus vrai avec les agents de code. Un agent reproduit ce qu'il voit dans le repository. Dans une plateforme où chaque pipeline est déployé un peu différemment, il a une douzaine de patterns au choix, et en prend un sans vous dire lequel. Dans une plateforme ennuyeuse, la trentième source ressemble exactement à la vingt-neuvième : l'agent copie la précédente, et il a raison.

Les ingénieurs connaissent le conseil « choisir une technologie ennuyeuse » (*choose boring technology*). Nous l'appliquons un cran plus haut : **nous rendons la contribution ennuyeuse.** L'ingéniosité a sa place dans la plomberie, écrite une fois par ceux qui la maintiennent. Où qu'aille un contributeur, il ne devrait rien y avoir à deviner.

---

## Principe 1 : séparer la configuration de la plomberie

Toute la plateforme est pilotée par une poignée de fichiers YAML. Terraform les lit et déploie, en boucle, tout ce qu'ils décrivent : personne n'écrit de Terraform pour ajouter une source, une fonction, une app web ou un rôle.

| Fichier de configuration | Ce que déclare un contributeur | Ce que déploie la plomberie |
|---|---|---|
| `load/<source>.yml` | les tables d'une source, leurs colonnes et les fichiers qui les alimentent | un schéma dans l'entrepôt, un stage, une table et un Snowpipe par table, la surveillance de la fraîcheur |
| `functions.yml` | la planification ou le déclencheur d'une fonction, son timeout et sa mémoire | une fonction Lambda ou une tâche Fargate, sa planification ou son déclencheur, ses logs, ses alarmes et la détection de ses plantages |
| `apps.yml` | la taille d'une app web, et éventuellement ses chemins et son environnement | un service de conteneurs, sa règle de load balancer derrière l'authentification de l'entreprise, son health check et ses logs |
| `snowflake_roles.yml` | un rôle : quels warehouses, quelles bases ou quels schémas, avec quels privilèges | tous les droits, sur les objets existants et futurs |
| `snowflake_users.yml` | une personne : son email et ses rôles | un utilisateur dans l'entrepôt, son rôle par défaut et l'attribution de ses rôles |

Voici tout ce qu'écrit un contributeur pour amener une nouvelle source, depuis une API, jusque dans l'entrepôt. Quelques lignes dans `functions.yml` :

```yaml
get_crm:
  category: get_data
  schedule: cron(0 4 * * ? *)
  timeout: 600
  memory: 2048
```

Un fichier Python, `functions/get_crm.py`, dont la fonction, sous l'un de nos décorateurs, appelle l'API et dépose ses enregistrements tels quels dans S3. Et la description de ce qui arrive, dans `load/crm.yml` :

```yaml
source_path: crm/
source_type: API
data_extract_lambda: get_crm
description: |
  Données de la relation client : comptes, contacts, opportunités.
format:
  type: JSON
destination_tables:
  - name: ACCOUNTS
    description: Comptes clients, une ligne par compte et par extraction.
    pattern: "accounts/accounts_.*\\.ndjson"
    columns:
      - name: ID
        type: varchar
        description: Identifiant du compte dans le CRM.
      - name: NAME
        type: varchar
        description: Nom du compte.
```

Une fois la Pull Request mergée, le pipeline de déploiement fait le reste : la fonction entre en service avec sa planification, un schéma `CRM` apparaît dans l'entrepôt avec une table `ACCOUNTS` et son Snowpipe, et les fichiers déposés par la fonction commencent à y arriver. Pas une ligne de Terraform, pas un clic dans une console. **Ajouter une source ajoute de la configuration, jamais de plomberie** : aujourd'hui, une quarantaine de fichiers de sources et une quarantaine de fonctions sont déployés par moins de 5 000 lignes de Terraform que les contributeurs n'ont jamais besoin d'ouvrir.

Relire une telle contribution, c'est relire une déclaration : une planification, une taille de mémoire, la description d'une table. Le relecteur ne vérifie pas si une permission cloud est trop large ou si un Snowpipe est branché sur la bonne notification : il n'y a ni permission ni Snowpipe dans le diff. Ils ont été relus une fois, quand la plomberie a été écrite, et ce sont les mêmes pour toutes les sources.

Quand surgit un besoin que la configuration ne sait pas exprimer, nous ne faisons pas d'exception : **nous étendons la configuration, pour tout le monde, avec un champ optionnel.** Une fonction qui décompresse de grosses archives a besoin de plus de disque : `ephemeral_storage`. Une fonction qui appelle une API au rate limit strict ne doit jamais tourner plus de deux fois en même temps : `max_concurrency`. Une table rafraîchie une fois par semaine ne doit pas lever d'alerte de fraîcheur tous les jours : `max_staleness_hours`. Une source qui ne produit pas encore, ou qui est en panne le temps que son fournisseur la répare : `muted_until`, avec une date après laquelle la supervision reprend d'elle-même. Chaque champ a été ajouté une fois à la plomberie, et il est désormais à la disposition de tous les contributeurs, sans nouveau pattern à copier.

Et l'accès à l'entrepôt, c'est aussi de la configuration. Les jeux de privilèges sont définis une fois, et chaque rôle les combine ; une personne, c'est un email et une liste de rôles. Aucun `GRANT` n'est jamais lancé à la main : un privilège manquant est ajouté au YAML et déployé comme tout le reste. Le fichier YAML *est* la politique d'accès — versionnée, lisible par tous, relue comme n'importe quel changement.

<details>
<summary><strong>Pour aller plus loin : la plomberie derrière un fichier YAML</strong></summary>

<p>Terraform lit chaque fichier de configuration dans une valeur locale, sur laquelle chaque ressource boucle. Une version simplifiée pour les sources :</p>

<pre><code class="language-hcl">locals {
  sources = {
    for file in fileset("${path.module}/../load", "*.yml") :
    trimsuffix(file, ".yml") =&gt; yamldecode(file("${path.module}/../load/${file}"))
  }
}

resource "snowflake_schema" "source" {
  for_each = local.sources
  database = "RAW"
  name     = upper(replace(each.key, "-", "_"))
  comment  = split("\n", trimspace(each.value.description))[0]
}</code></pre>

<p>Le schéma prend le nom du fichier, et son commentaire la première ligne de la description de la source. Les stages, les tables, les Snowpipes et les notifications suivent le même pattern, sur une entrée par table.</p>

<p>L'accès à l'entrepôt fonctionne de la même façon. Les jeux de privilèges sont des ancres YAML, définies une fois, que les rôles combinent par base ou par schéma :</p>

<pre><code class="language-yaml">read: &amp;read
  TABLES: [SELECT]
  VIEWS: [SELECT]

write: &amp;write
  SCHEMA: [CREATE TABLE, CREATE VIEW]
  TABLES: [SELECT, INSERT, UPDATE, DELETE, TRUNCATE]
  VIEWS: [SELECT]

role_grants:
  FINANCE:
    warehouses: [FINANCE_WH]
    objects:
      MARTS: *read
      SANDBOX.FINANCE: *write
  MARKETING:
    warehouses: [MARKETING_WH]
    objects:
      MARTS.MARKETING: *read</code></pre>

<p>La plomberie transforme chaque entrée en droits sur tous les objets existants et futurs : une table créée demain sera lisible par les rôles qui doivent la lire, sans que personne ait à y penser. Les utilisateurs sont encore plus simples :</p>

<pre><code class="language-yaml">human_users:
  jane.doe@example.com:
    roles: [FINANCE]
  john.smith@example.com:
    roles: [MARKETING, FINANCE]</code></pre>

<p>Le nom d'utilisateur est déduit de l'email, et le premier rôle est le rôle par défaut.</p>

</details>

---

## Principe 2 : déduire plutôt que déclarer

Chaque champ que remplit un contributeur est un champ qu'il peut mal remplir. Nous posons donc la même question pour chaque paramètre : la plomberie pourrait-elle le calculer ? Si oui, le champ n'existe pas.

**Si deux paramètres doivent concorder, l'un des deux ne devrait pas exister.**

* **Où tourne une fonction.** Une fonction Lambda ne peut pas tourner plus de 15 minutes ni utiliser plus de 10 Go de mémoire. Nos fonctions déclarent leur `timeout` et leur `memory` ; quand elles demandent plus que ce que Lambda permet, la plomberie les déploie à la place en tâche Fargate planifiée — même fichier Python, même décorateur, même remontée des statuts. Il n'y a pas de champ `backend`, donc aucun backend ne peut contredire le timeout.
* **Combien de CPU.** Fargate n'accepte que certaines paires de CPU et de mémoire. Déclarer le CPU ne serait qu'une occasion de déclarer une paire invalide : la plomberie choisit donc le plus petit CPU valide pour la mémoire demandée. Une tâche qui a besoin de plus de calcul demande plus de mémoire.
* **Où vit une app web.** L'URL d'une app web, c'est son nom, et son health check a un chemin par défaut. Sa règle de load balancer a besoin d'une priorité, unique parmi toutes les apps web. Personne ne la choisit, et ce n'est pas non plus son rang dans l'ordre alphabétique : ajouter une app web décalerait toutes celles qui la suivent, et le load balancer refuse deux règles de même priorité, même un instant. Elle est déduite d'un hash du nom : ajouter ou retirer une app web ne déplace jamais les autres.
* **Comment s'appellent les choses.** Le schéma d'une source dans l'entrepôt porte le nom de son fichier YAML. Le nom d'utilisateur d'une personne dans l'entrepôt est déduit de son email, et son premier rôle est son rôle par défaut.
* **Ce qu'affiche le menu.** Nos data apps — des tableaux de bord et de petits outils métier, chacune un seul fichier Python — sont listées dans un menu, mais il n'y a pas de fichier de menu : le menu, c'est l'arborescence des dossiers. Une section est un dossier avec un court `_section.yml`, et chaque data app déclare elle-même, dans son propre fichier, son titre, son icône, sa description et son propriétaire :

```python
page.config(
    title="Factures fournisseurs",
    icon="🧾",
    description="Factures reçues des fournisseurs, par magasin et par mois.",
    owner="jane.doe@example.com",
)
```

Ajouter une data app, c'est ajouter un fichier ; supprimer le fichier la retire du menu. Pas de liste centrale à mettre à jour, pas d'entrée de menu qui pointe vers une data app disparue. Même publier, c'est déplacer un fichier : une nouvelle data app démarre dans un dossier « en construction », que l'app web servie à nos magasins n'affiche jamais ; elle y apparaît quand le fichier en sort.

La déduction a un second avantage : la plateforme peut évoluer sans que personne ne migre quoi que ce soit. Si les limites de Lambda changent demain, nous changeons une règle dans la plomberie, et chaque fonction atterrit là où elle doit au déploiement suivant.

---

## Principe 3 : un seul endroit pour chaque type de logique

La configuration règle la question de l'infrastructure. Mais les contributeurs écrivent aussi de la logique : des fonctions Python, des modèles SQL, des data apps. Là, la même idée prend une autre forme : **chaque type de logique a exactement un endroit où vivre**, et les frontières sont strictes.

* **Une fonction dépose sa source telle quelle.** Chaque champ que renvoie la source, sous le nom que lui donne la source, objets imbriqués et tableaux conservés entiers : ni renommage, ni filtre, ni aplatissement. Toute la transformation se fait dans dbt. Une extraction n'a rien à décider, et nulle part où cacher une règle métier.
* **Les données n'entrent dans l'entrepôt que par un chemin.** Chaque source atterrit d'abord dans S3, et Snowpipe la charge : aucune fonction n'écrit jamais directement dans l'entrepôt. Chaque ligne brute remonte à son fichier, et n'importe quel chargement peut être rejoué.
* **La logique métier vit dans dbt, les métriques dans la couche sémantique.** Un ratio est calculé par la couche sémantique comme un ratio de sommes, jamais moyenné dans une data app. Les comparaisons d'une année sur l'autre — à quelle période comparer, quels magasins inclure — sont calculées par un seul moteur, à partir d'une règle écrite une fois dans les guides de notre portail data ; aucune data app ni aucune requête ad hoc ne les recalcule. Même un agent qui répond à une question ad hoc interroge d'abord la couche sémantique, pour que ses chiffres soient ceux des data apps.
* **Les définitions vivent dans le dictionnaire métier**, rattachées aux noms de colonnes, comme décrit dans [Un nom, une définition](https://unytics.io/blog/fr/one-name-one-definition/).
* **L'apparence vit dans une charte graphique.** Les data apps ne stylent pas elles-mêmes leurs cartes d'indicateurs ou leurs tableaux : elles appellent les helpers d'un module de charte graphique partagé, pour que des data apps écrites par des personnes différentes ressemblent à un seul et même produit.
* **Les explications vivent à côté de ce qu'elles expliquent.** L'entrée d'une fonction dans `functions.yml` ne porte aucun commentaire explicatif : ce que la fonction extrait, pourquoi cette planification, comment fonctionne son chargement incrémental, tout cela va dans la docstring de son fichier Python, que le portail data publie sur la page de la fonction. La définition d'une métrique vit dans sa description, dans la couche sémantique, et le portail l'affiche.

Quand chaque type de logique a un seul endroit, **un relecteur ne se demande plus *où* une chose devrait être, seulement *si* elle est juste.** Et un agent n'a jamais à choisir entre deux endroits : il n'y en a qu'un.

---

## Principe 4 : faire du chemin sûr le seul chemin

Un contributeur ne devrait pas avoir à *penser* à la sécurité, au déploiement ni à la supervision. Quand quelque chose compte, c'est intégré à la plomberie, sans moyen d'y échapper — et **ce qui ne peut pas être oublié n'a pas besoin d'être vérifié.**

### La sécurité à la porte, pas dans chaque data app

Nos apps web sont derrière un load balancer qui exige l'authentification de l'entreprise avant qu'une seule requête ne les atteigne, et chacune revérifie l'identité de l'utilisateur via une bibliothèque partagée. Un responsable de magasin ne voit que les chiffres de ses propres magasins, parce que le périmètre est appliqué par la couche sémantique, à partir de l'identité de l'utilisateur, pour toutes les data apps à la fois — que la question vienne d'une data app, d'une carte Teams ou d'un assistant IA via notre serveur MCP. Un contributeur qui construit une data app ne peut pas oublier un contrôle de sécurité : il n'y en a aucun à écrire.

Les agents sont logés à la même enseigne. Sur le poste d'un contributeur, l'agent se connecte à l'entrepôt avec le compte et les rôles du contributeur lui-même : l'agent d'un contributeur du marketing ne peut pas lire ce que le marketing ne peut pas lire.

### La configuration là où son propriétaire peut la changer

**Mettez chaque élément de configuration là où son propriétaire peut le changer sans risque.** L'infrastructure a sa place dans du YAML relu. Qui peut ouvrir quelle data app, non : cela change souvent, et ce sont des managers qui en décident, pas des contributeurs. Nous avons d'abord déclaré les accès dans le fichier de chaque data app, puis nous les avons complètement sortis du repository. Aujourd'hui, ils vivent dans une base de données, modifiée par une poignée de managers depuis une data app dédiée. Une data app dont l'accès n'a été donné à personne n'est ouverte qu'à son propriétaire et aux admins. Une demande d'accès arrive dans Teams avec un lien qui ouvre cette personne et cette data app, et suggère les groupes qui lui donneraient l'accès en ouvrant le moins d'autres data apps possible. Une Pull Request ne peut pas donner d'accès : aucun relecteur n'a donc à vérifier qui peut voir quoi.

Il en va de même pour un paramètre qu'un opérateur doit pouvoir changer sans ingénieur : il va dans un stockage clé-valeur où il peut écrire, pas dans le code. Les secrets contiennent des identifiants, rien d'autre.

### Un seul chemin de déploiement

Un merge sur main déclenche le seul chemin de déploiement. Selon les fichiers modifiés, le pipeline reconstruit ce qui doit l'être, dans un ordre fixe : l'infrastructure d'abord, puis les transformations de données, puis le code et les apps web qui les lisent — le code n'est donc jamais livré avant les données qu'il attend. Même les définitions des métriques sont livrées avec les données : le run dbt les publie à côté des exports qu'il produit, et chaque data app récupère la nouvelle version en quelques minutes.

Une Pull Request construit les modèles qu'elle modifie dans un schéma qui lui est propre, où relecteurs et agents peuvent les comparer à la production. Mais elle ne peut rien déployer, ni par accident ni volontairement : le cloud ne délivre d'identifiants de production qu'aux pipelines qui tournent sur main. Et quand une app web se comporte mal après un déploiement, revenir en arrière tient en une ligne dans `apps.yml` : épingler son image sur le commit précédent.

### Une supervision intégrée à chaque fonction

Chaque fonction tourne sous l'un de nos décorateurs : planifiée, ou déclenchée par un fichier, un événement ou un appel HTTP. Le décorateur enregistre le statut, la durée et les logs de chaque exécution. Si la fonction meurt avant d'avoir pu rendre compte — mémoire épuisée, temps écoulé — un gestionnaire de plantages écrit l'erreur à sa place. Toutes les heures, un contrôle compare la dernière exécution de chaque fonction à sa planification ; chaque matin, après qu'un job a rechargé les fichiers manqués par Snowpipe, un autre compare la fraîcheur de chaque table brute à son seuil : 24 heures, sauf si le YAML de la source en dit autrement. Une erreur reste signalée jusqu'à ce que quelqu'un la marque comme résolue dans le portail, même si l'exécution suivante réussit. Et comme les statuts d'exécution sont exposés dans la couche sémantique comme n'importe quelle autre donnée, une carte Teams planifiée liste les fonctions en anomalie. Quand il n'y en a aucune, elle le dit : une carte qui se tait quand tout va bien ne se distingue pas d'une carte en panne.

Un contributeur obtient tout cela pour sa fonction sans en écrire une ligne.

### Une documentation générée depuis la configuration

À chaque changement de configuration, le portail data est régénéré à partir d'elle : une page par source et par table, à partir des fichiers YAML ; une page par fonction, avec sa docstring, sa configuration, son dernier statut et un bouton pour la lancer ; une page par modèle dbt ; le dictionnaire et les métriques. Les contributeurs documentent en remplissant les descriptions de leur configuration — il n'y a pas de documentation à part à tenir à jour.

**La sécurité, le déploiement et la supervision ne sont pas des points d'une checklist de revue : ce sont des propriétés de la plateforme.**

---

## Principe 5 : mettre les règles là où travaille l'agent

La configuration et la plomberie éliminent l'essentiel de la marge d'erreur. Ce qui reste — SQL, Python, data apps — est écrit par des agents. Pour cette partie, les règles doivent atteindre l'agent au moment où il agit, et la machine doit les vérifier.

* **Des instructions à côté du code qu'elles régissent**, et un skill pour chaque type de tâche : le contexte de l'agent contient les règles de ce qu'il fait, pas tout le règlement.
* **Des contrôles à l'écriture**, qui renvoient toute violation à l'agent avant qu'un humain ne voie le diff.
* **Des agents relecteurs avant même l'ouverture de la Pull Request** : quand un humain la reçoit, l'essentiel est déjà propre.
* **Une règle d'or** : chaque commentaire de revue devient une règle, pour que la même remarque ne revienne pas.

Je détaille ces mécanismes, et les règles que nos incidents nous ont apprises, dans [La plateforme qui apprend](https://unytics.io/blog/fr/the-platform-that-learns/).

L'approbation humaine ne disparaît pas : chaque Pull Request est toujours validée par une personne. Mais elle arrive après une première relecture, qui a déjà vérifié les conventions. Ce qui reste à l'humain, c'est la question qu'aucune machine ne peut trancher : est-ce la bonne chose à construire ?

---

## Ce que ça change

* **La revue se réduit à ce qui compte.** La plupart des diffs sont des déclarations YAML et du code qui suit un pattern déjà vérifié par un agent relecteur. Nous lisons l'intention, pas la plomberie.
* **Les agents font juste du premier coup.** Une plateforme ennuyeuse a un pattern par tâche. L'agent copie la dernière source, la dernière fonction, la dernière data app — et il a raison.
* **Les contributeurs construisent ce qu'ils connaissent.** Un contrôleur de gestion peut ajouter une source, un modèle et une data app sans jamais entendre parler d'IAM, de VPC ou de droits dans l'entrepôt. Son expertise va dans la logique métier, là où nous en avons besoin.
* **La plomberie s'améliore pour tout le monde à la fois.** Quand nous améliorons la détection des plantages, resserrons un droit ou changeons une valeur par défaut, chaque fonction et chaque rôle en bénéficie au déploiement suivant. Personne ne migre son pipeline, parce que personne ne possède la plomberie d'un pipeline.
* **L'infrastructure reste remplaçable.** Comme la configuration dit *quoi* et pas *comment*, passer une fonction de Lambda à Fargate — ou la plateforme chez un autre fournisseur — est un changement dans la plomberie, pas dans quarante contributions. C'est ce que je voulais dire, dans [mon article sur l'indépendance](https://unytics.io/blog/fr/optic-2000-independence/), par *la configuration est un actif, le métal est une commodité*.
* **L'équipe plateforme devient une équipe produit.** Son produit, c'est la plomberie, les conventions et les agents relecteurs ; ses utilisateurs, ce sont les 25 contributeurs et leurs agents.

---

## Ce que ça coûte

Cet ennui a un prix, et c'est l'équipe plateforme qui le paie.

* **La plomberie est plus difficile à écrire.** Tout déduire, prendre en charge chaque champ optionnel, fermer chaque chemin risqué : notre Terraform est plus dense que ne le serait un module par pipeline. Il est écrit une fois, mais il doit être bien écrit. Et quand une déduction sert aussi hors de Terraform — le portail a lui aussi besoin de savoir où tourne une fonction — les deux implémentations doivent changer ensemble.
* **Il faut savoir dire non.** Chaque exception « juste pour cette fois » est un second pattern que les agents copieront. Quand un besoin ne rentre pas dans le cadre, la réponse est d'étendre la configuration pour tout le monde, ou de refuser.
* **La configuration doit rester déclarative.** Un fichier YAML qui se met à contenir des conditions et des boucles devient un langage de programmation sans débogueur. La nôtre ne dit que *quoi* ; tout ce qui demande de la logique va dans la plomberie, sous forme de déduction.

---

## Ce qu'il faut en retenir

Notre plateforme est ennuyeuse pour que ce que l'on construit dessus n'ait pas à l'être.

Tout ce qui est difficile — infrastructure, sécurité, déploiement, supervision — est écrit une fois, dans la plomberie, par l'équipe qui la maintient. Tout le reste est de la configuration qui dit *quoi* — et seulement ce qui ne peut pas être déduit —, avec un seul endroit pour chaque type de logique et des règles qui attendent l'agent partout où il travaille. Ce qui reste au relecteur, c'est la seule question qui ait jamais compté : est-ce la bonne chose à construire ?

Posez-vous cette question sur votre propre plateforme : **quand quelqu'un ajoute une source de données, combien des lignes qu'il écrit sont de la plomberie ?** Chaque ligne de plomberie dans une contribution est une ligne que quelqu'un doit relire — et avec des agents qui en écrivent de plus en plus, ce quelqu'un ne suivra pas.

---

*Vous voulez ouvrir votre data platform aux métiers et à leurs agents sans devenir le goulot d'étranglement ? [Parlons-en lors d'un échange data de 30 minutes](https://unytics.io/book-meeting/).*
