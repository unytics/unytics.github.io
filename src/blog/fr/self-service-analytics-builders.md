---
title: "Self-Service Analytics : pourquoi vos métiers ne doivent pas être que des consommateurs d'IA (mais aussi des builders)"
description: "Tout le monde veut du conversationnel pour consommer la donnée. Chez Optic 2000, nous l'avons aussi mis au début de la chaîne, dans l'éditeur de code : 25 contributeurs, en majorité des métiers, construisent la data platform. Le récit complet, et les articles qui détaillent chaque partie."
date: 2026-11-16
---

# Self-Service Analytics : pourquoi vos métiers ne doivent pas être que des consommateurs d'IA (mais aussi des builders)

*Cet article reprend le fil de mon talk à la Forward Data Conference 2026, « Et si vos métiers construisaient la data platform ? » ([les slides sont ici](https://unytics.io/blog/fr/forward-data-conference-2026/)). C'est le récit complet, en version courte : chaque partie renvoie vers l'article qui la détaille.*

Toutes les directions générales et toutes les directions métiers demandent aujourd'hui la même chose : de l'analytique conversationnelle. Une interface où n'importe quel collaborateur pose une question à ses données, en langage naturel, et obtient aussitôt une analyse pertinente.

Chez Optic 2000, nous le faisons aussi. Mais ce n'est pas par là que nous avons commencé. Nous avons d'abord mis le conversationnel à l'autre bout de la chaîne : dans l'éditeur de code, là où la plateforme se construit. Dix mois plus tard, 25 personnes contribuent à notre data platform, et la plupart ne font partie d'aucune équipe data : **ce sont des métiers.**

---

## Le paradoxe : une IA ne répond juste que si quelqu'un entretient son contexte

Les équipes data savent ce qu'il y a sous le capot. L'équipe data d'Anthropic [l'a très bien raconté en juin](https://claude.com/blog/how-anthropic-enables-self-service-data-analytics-with-claude) :

* sans contexte préparé, Claude ne dépasse pas **21 %** de bonnes réponses sur leur entrepôt ;
* avec une équipe senior qui organise ce contexte — tables de référence, couche sémantique, skills, tests —, il dépasse **95 %** ;
* en un mois, faute d'entretien, il retombe à **65 %**.

Le contexte ne se prépare pas une fois : il s'entretient. Olga Berezovsky en a tiré la conclusion dans son [*Data Analysis Journal*](https://dataanalysis.substack.com/p/self-service-analytics-is-not) : pour faire fonctionner le self-service, et le faire durer, il faut tout un village d'analystes.

Voici ce que cela donne au quotidien. Un métier est en pleine analyse, et il lui manque une donnée : une colonne, une table, une mesure. Il a deux options.

1. **Bricoler dans son coin**, avec un export et un fichier Excel. C'est le *shadow data* : ce qu'il a compris ne revient jamais dans la plateforme.
2. **Ouvrir un ticket**, et attendre que l'équipe data prépare la donnée. Avant, on ouvrait un ticket pour avoir un dashboard ; maintenant, on en ouvre un pour avoir une colonne dans la couche sémantique. C'est le [Ticketing 2.0](https://unytics.io/blog/fr/the-ticketing-2-0-trap/).

Les équipes les plus avancées réduisent cette attente : elles analysent les questions restées sans réponse, et enrichissent le contexte avant même qu'on le leur demande. C'est remarquablement efficace, et nous le mettons en place nous aussi, pour ceux qui consomment. Mais l'équipe data y reste la seule à construire — donc le goulot d'étranglement de tout ce qui se construit.

---

## Le contre-pied : mettre le conversationnel au début de la chaîne

Chez Optic 2000, nous avions cette année un problème de plus : tout changeait en même temps. En dix mois, nous avons remplacé le socle PostgreSQL historique, intégré un nouveau logiciel de caisse, un nouveau CRM et un nouveau programme de fidélité, et débranché notre outil de BI. Le tout avec une équipe plateforme passée de six à quatre personnes. Notre équipe BI n'avait pas une minute pour traiter de nouveaux sujets métiers.

Face à ce mur, nous avons pris le contre-pied du marché. Une data platform classique enchaîne des sources, des transformations, une couche sémantique et des applications. L'équipe data prépare, les métiers consomment, et le marché branche le conversationnel tout au bout de la chaîne, dans une interface de consommation.

```
Sources → Transformations → Couche sémantique → Applications
                                                     ▲
                          le marché : le conversationnel ici

├── Optic 2000 : le conversationnel sur toute la chaîne ───┤
```

Nous l'avons mis au tout début : dans l'éditeur de code, là où la plateforme se construit. Au moment même où quelqu'un cherche à faire une analyse, l'IA l'aide à préparer et à enrichir la donnée, à la source, dans la plateforme. C'est la troisième option : ni bricoler, ni attendre. Construire.

**L'analyse construit la plateforme.** Un exemple. Nous analysions la performance de certains magasins, et nous avons voulu les comparer entre eux. Mais on ne compare pas des choux et des carottes : il fallait d'abord des segments. Nous les avons construits dans la même analyse, par un k-means sur le profil de vente de chaque magasin : haut, moyen ou bas de gamme, volumes, produits destinés aux personnes âgées ou aux enfants… L'analyse a répondu à la question posée : la performance de ces magasins, son évolution dans le temps, et leur position face à des magasins similaires. Et elle a laissé deux choses dans la plateforme : une dimension « segment » dans notre modèle `dim_magasins`, et une table de *features* — des statistiques de vente par magasin —, réutilisable par d'autres analyses comme par des algorithmes de machine learning.

Dans un outil d'analyse à part, cette segmentation serait restée dans un notebook. Ici, chacun construit sur les épaules de ceux qui l'ont précédé.

---

## Ce qui s'est passé : l'équipe BI d'abord, puis les métiers

Ouvrir le repository central à des non-développeurs ne s'est pas fait d'un coup. Nous avons commencé par les plus proches de nous : notre équipe BI, qui n'avait jamais touché à Git ni à dbt. En quelques semaines, elle construisait seule ses data apps, puis ses modèles. Les métiers du siège ont suivi, d'abord sur de petits sujets, puis sur des sujets critiques.

Résultat : en dix mois, le nombre de personnes qui contribuent à notre repository data est passé de **4 à 25**. Quatre à la plateforme, quatre à la BI, et tous les autres sont des métiers. Aucune de ces vingt-cinq personnes ne code à la main : elles conversent avec un agent.

Le village d'analystes qu'il faudrait pour faire vivre le self-service ? Le voilà. Sauf que nous ne l'avons pas recruté : **il était déjà dans l'entreprise.**

*Le détail — l'histoire de l'équipe BI, celles des métiers, le parcours d'embarquement, et ce qui se passe quand un contributeur s'en va — est dans [Personne ne code à la main](https://unytics.io/blog/fr/nobody-codes-by-hand/).*

---

## Ce qu'ils construisent : bien plus que des dashboards

En démultipliant les contributeurs, on ne gagne pas seulement du temps : on fait émerger des idées que l'équipe data n'aurait pas eues. Nous attendions des dashboards. Les métiers ont fait autre chose : ils ont remplacé des logiciels sous licence, et donné à SAP et à Salesforce les interfaces qui leur manquaient.

*Le détail — ce qu'ils ont construit, ce que ces data apps lisent et écrivent, et ce qui les garde homogènes — est dans [Un dashboard montre, une data app agit](https://unytics.io/blog/fr/data-apps-beyond-dashboards/).*

---

## Comment ça tient sans tourner au chaos

L'objection est légitime, et je me la faisais moi-même : laisser vingt-cinq personnes et leurs agents modifier la data platform, c'est fabriquer un plat de spaghettis, et passer plus de temps à relire leur code qu'à l'écrire soi-même. Cinq choses l'évitent, et chacune a son article.

* **Un seul repository.** L'ingestion, les transformations, la couche sémantique et les data apps vivent dans le même dépôt Git : un agent va de la source à l'écran dans la même conversation et la même Pull Request, ce qu'aucun ne pourrait faire avec des outils éclatés. C'est aussi ce qui nous rend [indépendants de nos fournisseurs](https://unytics.io/blog/fr/optic-2000-independence/).
* **Une contribution ennuyeuse.** Un contributeur n'écrit que de la configuration ; le déploiement, la sécurité et la supervision sont écrits une fois, par l'équipe plateforme. Ce qu'une contribution ne peut pas exprimer, un relecteur n'a pas à le vérifier. C'est le sujet d'[Ennuyeusement simple](https://unytics.io/blog/fr/boringly-simple-data-platform/).
* **Un seul nom par concept.** Une colonne porte le même nom dans tout l'entrepôt, et sa définition n'est écrite qu'une fois : l'agent n'a rien à deviner. C'est le sujet d'[Un nom, une définition](https://unytics.io/blog/fr/one-name-one-definition/).
* **Une revue faite d'abord par la machine.** Un agent relit le travail avant l'ouverture de la Pull Request, et chaque commentaire de revue devient une règle. Sans cela, nous aurions seulement déplacé le goulot d'étranglement, des tickets vers les Pull Requests. C'est le sujet de [La plateforme qui apprend](https://unytics.io/blog/fr/the-platform-that-learns/).
* **Des humains accompagnés.** La clé n'est pas technologique, elle est humaine : un de nos quatre data engineers se consacre à plein temps à l'accompagnement des métiers. C'est dans [Personne ne code à la main](https://unytics.io/blog/fr/nobody-codes-by-hand/).

---

## Builders et consumers : nous faisons les deux

Faut-il pour autant jeter l'analytique conversationnelle et mettre tout le monde dans VS Code ? Absolument pas. Au siège, les profils analytiques utilisent l'IA pour construire des actifs durables, dans le repository. Mais un opticien, dans l'un de nos magasins, n'ouvrira jamais un éditeur de code : lui doit être servi comme un client.

Pour les magasins, l'IA prend deux formes :

* **des agents spécialisés, embarqués dans leurs data apps.** Un directeur de magasin consulte son bilan financier et en discute avec un agent expert en finance de l'optique : il se compare aux magasins similaires, apporte son contexte local, obtient des recommandations ;
* **un serveur MCP et des skills**, qui exposent ces mêmes expertises : les magasins interrogent leurs données depuis leur propre Claude ou leur propre ChatGPT.

Dans les deux cas, les chiffres viennent de la même couche sémantique, et chacun ne voit que ses propres données.

Une organisation data compte trois rôles : ceux qui construisent la plateforme (les *platformers*), ceux qui construisent dessus (les *builders*) et ceux qui consomment (les *consumers*). Dans le modèle habituel, la frontière passe entre l'équipe data, qui construit, et les métiers, qui consomment. Nous l'avons déplacée.

| | Platformers | Builders | Consumers |
|---|---|---|---|
| **Le modèle habituel** | l'équipe data | l'équipe data | les métiers |
| **Chez Optic 2000** | l'équipe plateforme | les métiers du siège, avec l'équipe BI | les magasins |

Parmi ceux qui construisent, il y a désormais plus de métiers que de personnes de la data. Notre conviction : il faut mettre le plus de monde possible du côté des builders. À huit dans les équipes data, nous ne connaîtrons jamais toutes les subtilités comptables de SAP, ni toutes les règles de gestion du référentiel magasins. **Ce sont les métiers qui connaissent leurs données et leurs processus.**

---

## Une tendance qui dépasse notre cas

Je ne crois pas que cette façon de faire soit propre à une entreprise comme la nôtre. J'ai l'impression qu'une tendance s'installe : des métiers qui n'ont jamais codé se mettent à travailler dans des repositories de code, sous trois formes :

* ils ouvrent un ticket depuis Slack, et un agent le code ;
* ils construisent directement dans le repository d'une autre équipe, comme chez nous ;
* ils créent leur propre repository.

C'est particulièrement visible dans les équipes marketing et go-to-market, pour gérer leurs campagnes. Et les entreprises *digital native* sont concernées elles aussi. C'est même l'une d'elles qui m'a inspiré : Taha Le Bras, chez Supabase, me racontait qu'un matin, le marketing avait fait une Pull Request dans son repository data, et que lui-même, le même jour, en avait fait une dans celui du produit.

C'est peut-être une « git-ification » de l'entreprise qui commence. Ce qui change d'un cas à l'autre, c'est ce qu'on y construit : chez nous, la transformation de processus encore manuels. Et rien n'oblige à tout réunir d'emblée dans un seul repository : on peut ouvrir d'abord le repository dbt, puis y ramener le reste.

---

## Ce qu'il faut en retenir

On dit qu'il faut tout un village d'analystes pour faire vivre le self-service. Je crois que ce village existe déjà, dans chaque entreprise : **ce sont vos métiers.**

Gardez le conversationnel pour ceux qui consomment. Mais ne laissez pas à l'équipe data le monopole de la construction. La nôtre ne construit plus de simples tableaux de bord : libérée du ticketing et du clic-bouton, notre équipe BI aide les métiers à repenser leur façon de travailler, et l'équipe data dans son ensemble co-construit la transformation opérationnelle de l'entreprise.

Posez-vous la question pour votre propre entreprise : **qui, chez vous, pourrait devenir builder dès demain ?**

---

*Vous voulez ouvrir votre data platform à vos métiers, et savoir par où commencer ? [Parlons-en lors d'un échange data de 30 minutes](https://unytics.io/book-meeting/).*
