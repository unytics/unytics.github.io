---
title: "La plateforme qui apprend : chaque commentaire de revue devient une règle"
description: "Chez Optic 2000, quatre personnes ne peuvent pas relire tout ce que produisent 25 contributeurs et leurs agents. La revue tient parce qu'une correction ne se fait qu'une fois — elle devient une règle — et parce qu'une Pull Request arrive déjà relue par un agent avant qu'un humain ne l'ouvre."
date: 2026-11-13
---

# La plateforme qui apprend : chaque commentaire de revue devient une règle

Dans [Personne ne code à la main](https://unytics.io/blog/fr/nobody-codes-by-hand/), je racontais comment 25 personnes, en majorité des métiers, contribuent à la data platform d'Optic 2000 avec un agent de code. La conséquence est immédiate : **la revue devient le chemin critique**. Quatre personnes ne peuvent pas relire tout ce que produisent vingt-cinq contributeurs et leurs agents.

[Ennuyeusement simple](https://unytics.io/blog/fr/boringly-simple-data-platform/) donne la première moitié de la réponse : une contribution n'exprime que de la configuration, donc il reste peu à relire. Voici la seconde, pour ce qui reste — du SQL, du Python, des data apps : **une correction ne se fait qu'une fois**, et une Pull Request nous arrive déjà relue.

---

## Une correction ne se fait qu'une fois

Une règle s'ajoute à la plateforme dans trois situations.

1. **L'agent n'y arrive pas du premier coup**, et il faut lui expliquer. L'explication ne reste pas dans la conversation : l'agent l'inscrit dans le bon fichier d'instructions, avec sa raison, avant de continuer.
2. **Nous devons commenter une Pull Request.** Avant de corriger, nous nous demandons pourquoi l'IA a laissé passer cela, et nous mettons à jour le skill, immédiatement. Le commentaire devient une règle.
3. **Quelque chose est arrivé en production qui aurait dû être bloqué**, ou qui a échoué. L'incident devient une règle, ou un contrôle que la machine exécute.

Dans les trois cas, la correction ne répare pas seulement le cas présent : elle répare tous les suivants. C'est ainsi que nos Pull Requests deviennent quasiment instantanées à valider.

Encore faut-il que la règle atteigne l'agent au moment où il agit. Elle s'écrit donc là où il travaille : dans un fichier d'instructions à côté du code qu'elle régit, ou dans le skill que l'agent charge avant ce type de tâche.

<details>
<summary><strong>Pour aller plus loin : où vivent nos règles</strong></summary>

<ul>
<li><strong>Des instructions à côté du code qu'elles régissent.</strong> Un fichier d'instructions à la racine (<code>CLAUDE.md</code>, pour Claude Code) décrit la plateforme et ses règles non négociables. Chaque dossier principal — ingestion, fonctions, infrastructure, apps web — a le sien, que l'agent charge quand il y travaille. Les règles propres à un type de fichier — YAML, Terraform, Python, Markdown — ne se chargent que quand l'agent touche un tel fichier. Le contexte de l'agent contient les règles de ce qu'il fait, pas tout le règlement.</li>
<li><strong>Un skill pour chaque type de tâche.</strong> Avant de toucher à un modèle dbt, l'agent charge le skill dbt : couches, nommage, tests, style SQL, et une porte de sortie avant de rendre la main. De même pour les data apps et pour la charte graphique.</li>
</ul>

<pre><code>CLAUDE.md                          vue d'ensemble de la plateforme et règles non négociables
load/CLAUDE.md                     conventions d'ingestion
functions/CLAUDE.md                conventions des fonctions
infra/CLAUDE.md                    conventions d'infrastructure
data_portal/CLAUDE.md              conventions des apps web
.claude/rules/yml.md               chargé quand l'agent touche un fichier YAML
.claude/rules/terraform.md         chargé quand il touche un fichier Terraform
.claude/rules/python-standards.md  chargé quand il touche un fichier Python
.claude/skills/dbt-model/          chargé avant de créer ou de modifier un modèle dbt
.claude/skills/streamlit/          chargé avant de créer ou de modifier une data app
.claude/skills/publish-pr/         commit, push et Pull Request en une seule commande
.claude/skills/review-*/           revue d'une Pull Request, verdict MERGE ou NO MERGE
.claude/settings.json              hooks</code></pre>

<p>Un fichier de règles déclare dans un en-tête les fichiers auxquels il s'applique :</p>

<pre><code class="language-markdown">---
paths:
  - "**/*.tf"
---

# Terraform Style
…</code></pre>

</details>

---

## Sept règles nées de cette boucle

* **Ne jamais casser ce que quelqu'un utilise encore.** Avant d'arrêter une source ou de supprimer une table, on cherche qui s'en sert — un modèle, une data app, un export —, on le fait basculer, puis on supprime.
* **Une règle métier partagée vit dans la couche sémantique, pas dans une data app.** Une data app peut faire des choses intelligentes, mais une définition dont d'autres ont besoin appartient au moteur de mesure commun. Une data app destinée aux magasins codait elle-même la règle qui reconnaît une lunette connectée : les magasins qui posaient la même question à leur IA, à travers notre serveur MCP, obtenaient d'autres chiffres. Depuis, ces data apps ne lisent que la couche sémantique, et ne recodent aucune règle métier.
* **Une Pull Request ne fait qu'une chose.** Une erreur repérée en chemin se corrige à part. Sinon, le relecteur d'une nouvelle table approuve, sans le savoir, un changement de chiffres existants.
* **Chaque métrique, chaque domaine, chaque data app a un responsable.** Une métrique avait été mergée sans que l'équipe BI l'ait validée. La Pull Request est maintenant assignée automatiquement à ceux qui répondent de ce qu'elle modifie.
* **Un agrégat retrouve le total de sa table de faits.** Des valeurs nulles avaient faussé un total. Le skill demande maintenant ce contrôle, et met tout écart en évidence.
* **Un chiffre certifié du passé ne bouge plus.** L'un d'eux avait changé. Les mesures certifiées sont maintenant contrôlées sur des données passées.
* **Une data app n'est pas construite deux fois.** C'est arrivé. Le skill vérifie maintenant qu'elle n'existe pas déjà.

Aucune de ces règles ne se voit dans un diff SQL : c'est pour cela qu'elles sont écrites là où travaille l'agent.

---

## Une Pull Request arrive déjà relue

Ces règles s'appliquent avant qu'un humain ne regarde quoi que ce soit.

**Pendant que l'agent écrit**, des contrôles tournent : quand il modifie le dictionnaire métier ou la couche sémantique, un hook lui renvoie toute violation, et il la corrige dans la même session. Je le détaille dans [Un nom, une définition](https://unytics.io/blog/fr/one-name-one-definition/).

**Avant d'ouvrir la Pull Request**, le contributeur lance une seule commande. Le skill de publication passe la checklist de conformité, puis fait relire le travail par un agent relecteur : un pour les modèles dbt, un pour les data apps. Les fichiers de règles sont sa checklist, et il ne remonte que ce qui bloque — ce qui change un chiffre, un grain ou un nom de colonne, plante en production, touche aux droits d'accès, ou fait doublon avec une data app existante. Le style ne bloque jamais. Et si un contrôle ne peut pas tourner, le verdict n'est jamais un feu vert.

Le verdict s'adresse au contributeur, en langage courant, avant tout détail technique (chiffres inventés) :

```
MERGE : NON, la carte « magasins actifs » affiche 120 magasins là où la définition en donne 100.

1. Doublon : non.
2. Contraire à nos pratiques ou à une règle métier : oui, 1 point :
   - la carte compte tous les magasins ayant une vente ; la définition compte les magasins ouverts sur la période.
3. Réinvente la roue : en partie — les cartes sont dessinées à la main au lieu d'utiliser la charte graphique.
4. Merger : NON.
```

**La Pull Request n'est ouverte qu'ensuite.** Le skill en rédige la description — y compris ce qu'un relecteur ne doit pas manquer, comme l'arrêt d'une source de données — et l'assigne aux responsables de ce qu'elle modifie.

L'ordre compte. Nous aurions pu brancher l'agent relecteur après l'ouverture, pour qu'il commente la Pull Request. Le relecteur humain découvrirait alors un travail encore brouillon, sous une pile de commentaires automatiques. Ici, quand il ouvre une Pull Request, l'essentiel est déjà propre.

---

## Ce qui reste aux humains

**Le contributeur valide un résultat, pas du code.** Nos contributeurs métier ne lisent pas le code que leur agent écrit. Ils valident ce qu'ils connaissent : leurs chiffres, leur data app. Le verdict leur parle en langage courant, et le diff du dictionnaire métier résume le changement : trois lignes de définitions se lisent avant trois cents lignes de SQL.

**Le relecteur répond à une seule question.** Chaque Pull Request est toujours validée par une personne, et chaque responsable répond de son domaine. Mais les conventions sont déjà vérifiées. Il lui reste la question qu'aucune machine ne peut trancher : **est-ce la bonne chose à construire ?**

---

## Ce que ça coûte

* **Les règles demandent du jardinage.** Les instructions grossissent à chaque correction. Garder chaque règle à un seul endroit, avec sa raison et sans exemple périmé, est un travail à part entière.
* **La boucle demande de la discipline.** Corriger la Pull Request va plus vite que corriger le skill. L'équipe data d'Anthropic rapporte que [près de 90 % de ses Pull Requests touchant un modèle de données](https://claude.com/blog/how-anthropic-enables-self-service-data-analytics-with-claude) embarquent désormais une mise à jour de skill dans le même diff : c'est le prix d'un contexte qui ne se périme pas.

---

## Ce qu'il faut en retenir

Avec des agents qui écrivent le code, la capacité de revue ne grandit pas en ajoutant des relecteurs. Elle grandit quand une correction ne se fait qu'une fois, et quand une Pull Request arrive déjà relue. Il reste alors au relecteur la seule question qui compte.

Posez-vous la question pour votre propre équipe : **parmi vos commentaires de revue de la semaine, combien en aviez-vous déjà écrit un jour ?** Chacun est une règle qui attend d'être écrite.

*Cet article détaille une partie d'un récit plus large : [Pourquoi vos métiers ne doivent pas être que des consommateurs d'IA (mais aussi des builders)](https://unytics.io/blog/fr/self-service-analytics-builders/).*

---

*La revue devient le goulot d'étranglement de vos agents de code ? [Parlons-en lors d'un échange data de 30 minutes](https://unytics.io/book-meeting/).*
