---
title: "Un nom, une définition : comment nous documentons 1800 colonnes sans documenter un seul modèle dbt"
description: "Chez Optic 2000, aucun modèle dbt ne décrit ses colonnes, et pourtant chacune a sa définition : elle est attachée au nom de la colonne et écrite une seule fois, dans un dictionnaire métier. Conventions de nommage, garde-fous pour les agents de code, data portal généré : comment une seule façon de nommer supprime la dérive des définitions."
date: 2026-11-04
---

# Un nom, une définition : comment nous documentons 1800 colonnes sans documenter un seul modèle dbt

Chez Optic 2000, notre data platform compte plus de 350 modèles dbt et quelque 1800 noms de colonnes. Chacun a sa définition, consultable par tous dans notre data portal et rangée par entité métier.

Pourtant, ouvrez n'importe quel fichier YAML de nos modèles dbt : vous n'y trouverez pas une seule description de colonne.

Ce n'est pas un oubli. C'est le cœur de notre approche : **nous ne documentons pas les modèles, nous documentons les noms.**

Dans un projet dbt classique, chaque modèle redécrit ses colonnes dans son fichier YAML. Le même identifiant client est décrit dans le staging, puis dans le modèle intermédiaire, puis dans le mart, puis dans l'export : quatre copies d'une même définition, écrites à des moments différents par des personnes différentes. Elles finissent toujours par diverger. Une correction n'est faite qu'à un endroit ; une nouvelle colonne arrive sans description, parce que remplir le YAML est une corvée ; et le jour où deux descriptions se contredisent, plus personne ne sait laquelle croire.

Les data engineers reconnaîtront le problème : c'est une donnée dénormalisée, avec ses anomalies de mise à jour. Les blocs `{{ doc() }}` de dbt et les outils qui propagent les descriptions d'un modèle à l'autre soignent le symptôme, au prix de mécanismes supplémentaires. Ils ne suppriment pas les copies.

**Avec les agents d'IA, cette dérive se paie cher, et vite.** L'équipe Data d'Anthropic l'a mesuré : un mois après le lancement de son agent d'analyse, sans maintenance continue, sa précision était tombée de 95 % à 65 %, sous l'effet de l'évolution naturelle des schémas et du produit. Pour tenir le cap, près de 90 % de ses Pull Requests touchant un modèle de données embarquent désormais une mise à jour de *Skill* dans le même diff. Le contexte d'un agent se périme aussi vite que le code qu'il décrit.

Notre réponse tient en une phrase : **un concept a un seul nom, un nom a une seule définition, et cette définition est écrite une seule fois.** Elle ne tient qu'à une condition — qu'un nom désigne vraiment la même chose partout — et c'est tout l'objet de nos conventions de nommage.

Cet article explique pourquoi **ces règles comptent autant pour les agents que pour les humains**, comment nous les avons rendues impossibles à contourner, et comment la documentation de chaque modèle est devenue un sous-produit calculé. Pour les équipes qui voudraient reproduire l'approche, les détails techniques sont rangés dans des sections dépliables.

---

## Pourquoi des règles, pour les humains comme pour les agents

**Le nom est la documentation la plus lue.** Le nom d'une colonne voyage avec la donnée : dans chaque requête, chaque résultat, chaque export Excel, chaque réponse d'un assistant d'IA. Sa description n'est lue que par ceux qui vont la chercher, c'est-à-dire presque personne. Un nom ambigu comme `statut`, `date` ou `montant` produit des questions, des jointures fausses et des chiffres faux, souvent sans que personne ne s'en aperçoive.

**Les agents ne demandent pas : ils devinent.** Un agent de code redécouvre le repository à chaque session et reproduit ce qu'il y voit. S'il trouve `email`, `mail_client` et `customer_email`, il ne choisira pas « la bonne » : il en créera une quatrième. Devant une colonne `date` dans une table de commandes, un analyste demande s'il s'agit de la date de création, de facturation ou de livraison. Un agent en choisit une, et ne le dit pas.

Comme je l'écrivais dans [Personne ne code à la main](https://unytics.io/blog/fr/nobody-codes-by-hand/), dans un repository où il n'existe qu'une seule façon de faire chaque chose, l'agent n'a qu'à copier le bon pattern. Le nommage est le cas d'école de cette règle : **chaque synonyme est un second pattern à copier.**

**Une convention est une décision prise une fois pour toutes.** Sans règle, chaque nouvelle colonne ouvre un micro-débat : entre deux humains en revue, ou dans le raisonnement d'un agent qui n'a pas le contexte pour le trancher. Avec 25 contributeurs, dont la plupart ne sont pas ingénieurs, ces débats ne passent pas à l'échelle.

**Et une règle qu'un agent peut enfreindre sans être prévenu n'est qu'une suggestion.** Écrire les conventions dans un fichier d'instructions ne suffit pas : la machine doit les vérifier au moment même où la colonne est écrite. J'y reviens plus bas.

---

## Le principe : un concept, un nom, une définition

Voici ce que produit l'approche classique, en trois modèles :

```yaml
models:
  - name: stg_crm__contacts
    columns:
      - name: email
        description: "Email du contact"
  - name: dim_clients
    columns:
      - name: email_client
        description: "Adresse e-mail du client, en minuscules"
  - name: exp_clients_newsletter
    columns:
      - name: customer_email
        description: "Email client nettoyé"
```

Trois noms et trois définitions pour un seul concept. Laquelle est la bonne ? Et laquelle l'agent recopiera-t-il dans le quatrième modèle ?

Notre règle de base est une bijection :

* **un concept = un nom**, partout : du staging aux marts, quels que soient le modèle, la source ou le format d'origine ;
* **un nom = un concept** : deux noms différents désignent deux concepts différents, et un même nom a toujours le même type et le même format. Le jour où le sens d'une colonne change, elle change de nom.

Si un nom désigne exactement la même chose dans tous les modèles qui le portent, sa définition ne dépend plus du modèle. On peut l'attacher au nom, une seule fois, dans un **dictionnaire métier**.

Notre dictionnaire est un unique fichier YAML, organisé par entité métier : client, commande, produit, magasin… une soixantaine au total. Chaque entité a une description, et ses colonnes sont rangées en deux sections : les `dimensions`, qui décrivent (identifiants, dates, libellés, booléens), et les `facts`, qui s'agrègent (montants, quantités, comptages). Une ligne par colonne, en ordre alphabétique, et chaque nom n'apparaît qu'une fois dans tout le fichier :

```yaml
commande:
  description: >-
    Commande passée par un client, en magasin ou sur le site e-commerce.
  dimensions:
    canal_commande: Canal par lequel la commande a été passée (magasin, site e-commerce, téléphone).
    date_creation_commande: Date à laquelle la commande a été enregistrée.
    est_annulee_commande: Indique si la commande a été annulée après sa création.
    id_commande: Identifiant unique de la commande, toutes sources confondues.
    statut_commande: Étape de la commande dans son cycle de vie (en préparation, expédiée, livrée).
  facts:
    montant_frais_livraison_commande: Frais de livraison facturés au client, TTC.
    montant_ttc_commande: Montant total de la commande, toutes taxes comprises, frais de livraison inclus.
    nombre_articles_commande: Nombre d'articles de la commande.
```

Et voici, du coup, le fichier YAML d'un modèle dbt : une description, un responsable, des tests. Aucune colonne.

```yaml
models:
  - name: fct_commandes
    description: |-
      Une ligne par commande, toutes sources confondues.
    config:
      meta:
        owner: "jane.doe@example.com"
    tests:
      - unique:
          column_name: id_commande
      - not_null:
          column_name: id_commande
```

La description du modèle dit ce que représente une ligne. Ce que signifie chaque colonne, le dictionnaire le dit déjà.

Trois principes complètent la règle :

* **Une entité est un domaine métier large** — client, produit, magasin —, jamais une table source, un fournisseur ou un agrégat. Une table de paramétrage qui ne fait que traduire un code en libellé n'est pas une entité : ses libellés rejoignent l'entité qu'ils décrivent. C'est ce qui garde le dictionnaire lisible à 1800 colonnes.
* **Une définition décrit le concept, pas sa fabrication.** Elle ne cite ni le nom technique d'un champ source ni un modèle dbt : `email_client` reste « l'adresse e-mail du client » le jour où l'on change de CRM ou de modèle.
* **Le dictionnaire dit ce qu'une colonne signifie ; la couche sémantique dit comment l'agréger.** Le SQL des métriques vit dans notre couche sémantique, que je décrivais dans [cet article sur l'indépendance](https://unytics.io/blog/fr/optic-2000-independence/). Ses entités portent le nom d'une entité du dictionnaire et n'ont pas de description propre : elles héritent de la sienne. Un indicateur que personne ne matérialise, comme un panier moyen, n'existe que dans la couche sémantique ; le dictionnaire ne documente que des colonnes réelles.

---

## Les conventions qui rendent un nom unique

Pour servir de clé à sa définition, un nom doit être unique dans tout l'entrepôt, et prévisible. Nos conventions de nommage n'ont pas d'autre but : elles ne sont pas une affaire de goût.

* **Le nom porte son entité.** `email` devient `email_client`, `statut` devient `statut_commande`. Ce suffixe rend le nom unique et dit à quelle entité du dictionnaire il appartient.
* **Le suffixe désigne l'entité décrite, pas la table qui la porte.** La famille d'un produit s'appelle `famille_produit` dans les lignes de vente, de devis et de retour : trois modèles, une seule définition. Jamais `famille_produit_vente`.
* **Le préfixe annonce le type.** `est_` ou `a_` pour un booléen (`est_annulee_commande`, `a_telephone_client`), `date_` pour une date, `date_heure_` pour un horodatage en UTC, `montant_` pour un montant. Un agent qui lit `est_actif_client` sait qu'il filtre sur `true` — pas sur `1`, ni sur `'O'`.
* **Des mots entiers.** Ni abréviation ni acronyme maison (`conformite`, pas `conf`), sauf les codes officiels (GTIN, SIRET…).
* **Le concept métier dès le staging.** Une colonne prend le nom du concept métier dès la première transformation, pas celui de la source : le champ `AccountId` d'une opportunité Salesforce devient `id_client_salesforce`, pas `account_id`.
* **Une seule langue.** Nos noms sont en français, la langue de ceux qui lisent ces colonnes. L'important n'est pas la langue choisie, c'est de n'en avoir qu'une : jamais `_client` et `_customer` dans le même entrepôt.
* **Le nom d'un identifiant dit jusqu'où il a été unifié.** `id_client_salesforce` n'a de sens que dans Salesforce ; `id_client_source` réunit les identifiants de plusieurs sources, chacun préfixé de la sienne ; `id_client` désigne le client unifié. Une jointure sur `id_client` vaut partout, une jointure sur `id_client_salesforce` ne vaut que dans le monde Salesforce — et le nom le dit.

<details>
<summary><strong>Pour aller plus loin : erreurs fréquentes et règles de format</strong></summary>

<p>Les erreurs les plus courantes :</p>

<table>
<thead>
<tr><th>À éviter</th><th>À préférer</th><th>Pourquoi</th></tr>
</thead>
<tbody>
<tr><td><code>email</code></td><td><code>email_client</code></td><td>L'e-mail de quelle entité ?</td></tr>
<tr><td><code>statut</code></td><td><code>statut_commande</code></td><td>Le nom doit être unique dans tout l'entrepôt.</td></tr>
<tr><td><code>date</code></td><td><code>date_creation_commande</code></td><td>Mot réservé SQL, et quelle date ?</td></tr>
<tr><td><code>date_cree_commande</code></td><td><code>date_creation_commande</code></td><td>Un nom d'action, pas un participe passé.</td></tr>
<tr><td><code>valeur_remise</code></td><td><code>montant_remise</code></td><td>Un montant commence par <code>montant_</code>.</td></tr>
<tr><td><code>nb_art_cmd</code></td><td><code>nombre_articles_commande</code></td><td>Pas d'abréviation.</td></tr>
<tr><td><code>est_actif</code> à <code>1</code> / <code>0</code></td><td><code>est_actif_client</code> à <code>true</code> / <code>false</code></td><td>Un booléen est un vrai booléen, et porte son entité.</td></tr>
<tr><td><code>famille_produit_vente</code></td><td><code>famille_produit</code></td><td>Le suffixe nomme l'entité décrite, pas le modèle.</td></tr>
<tr><td><code>pays_site_web</code></td><td><code>pays_visiteur_site_web</code></td><td>Le pays du visiteur, pas celui du site.</td></tr>
<tr><td><code>nom_client_crm</code></td><td><code>nom_client</code></td><td>Un attribut métier ne porte pas le nom de sa source.</td></tr>
</tbody>
</table>

<p>Et les règles de format :</p>

<ul>
<li><strong>Dates :</strong> <code>date_&lt;événement&gt;_&lt;entité&gt;</code> (<code>date_livraison_commande</code>). Horodatages : <code>date_heure_&lt;événement&gt;_&lt;entité&gt;</code>, en UTC sauf mention contraire dans la définition.</li>
<li><strong>Parties de date :</strong> le nom dit le format (<code>annee_aaaa</code>, <code>mois_mm</code>, <code>mois_aaaamm</code>) et ne porte pas d'entité : c'est la même année partout.</li>
<li><strong>Montants :</strong> <code>montant_</code>, jamais <code>valeur_</code>. Un montant qui n'est pas exprimé dans l'unité monétaire le dit dans son nom (<code>prix_en_centimes_article</code>).</li>
<li><strong>Mots réservés SQL :</strong> jamais seuls comme nom de colonne (<code>date</code>, <code>order</code>, <code>group</code>), à une exception près : <code>date</code> désigne le jour calendaire des tables à la maille jour, comme dans le calendrier.</li>
<li><strong>Suffixe qualifiant :</strong> seulement quand deux versions d'un même attribut coexistent dans un modèle, et avec un sens métier : <code>nom_marque_produit</code> à côté de <code>nom_marque_produit_avant_unification</code>. Jamais <code>_old</code>, <code>_new</code> ou <code>_v2</code>.</li>
<li><strong>Colonnes techniques :</strong> la traçabilité porte un nom unique dans tout le projet, préfixé de <code>_</code>, et vit, comme les identifiants des tables de paramétrage, dans une entité <code>technique</code> du dictionnaire. <code>_source</code> donne la source d'une ligne dans les modèles qui en réunissent plusieurs ; <code>_source_row_updated_at</code> est la date de modification de la ligne dans la source, quel que soit le nom du champ d'origine (<code>SystemModstamp</code> dans Salesforce, <code>updated_at</code> ailleurs).</li>
<li><strong>Casse :</strong> tout en minuscules, en <em>snake_case</em>. Les modèles sont au pluriel, nommés <code>stg_&lt;source&gt;__&lt;table&gt;</code> en staging.</li>
</ul>

</details>

<details>
<summary><strong>Pour aller plus loin : les trois niveaux d'identifiants</strong></summary>

<p>Quand un même objet métier vient de plusieurs sources — un produit référencé dans l'ERP et sur le site e-commerce, par exemple —, le nom de son identifiant dit jusqu'où il a été unifié, et sa valeur dit d'où il vient :</p>

<table>
<thead>
<tr><th>Niveau</th><th>Nom</th><th>Exemple de valeur</th><th>Créé dans</th></tr>
</thead>
<tbody>
<tr><td>1. Identifiant d'une source</td><td><code>id_produit_erp</code></td><td><code>12345</code></td><td>le staging de la source</td></tr>
<tr><td>2. Identifiant multi-source</td><td><code>id_produit_source</code></td><td><code>erp::12345</code>, <code>ecommerce::SKU-987</code></td><td>le modèle qui réunit les sources</td></tr>
<tr><td>3. Identifiant unifié</td><td><code>id_produit</code></td><td><code>GTIN::3600000000016</code>, ou <code>erp::12345</code> à défaut</td><td>le modèle qui rapproche les sources</td></tr>
</tbody>
</table>

<ul>
<li>Le niveau 3 est préfixé par la règle qui a permis le rapprochement (ici le GTIN), ou à défaut par la source retenue.</li>
<li>Chaque niveau n'est créé que s'il sert : sans union de sources, pas de niveau 2 ; sans rapprochement utilisé en aval, pas de niveau 3.</li>
<li>Le séparateur est toujours <code>::</code> et les préfixes de source sont en minuscules, comme les valeurs de la colonne <code>_source</code>. Quand une source a plusieurs instances (une base par société, par exemple), un discriminant s'intercale : <code>erp::societe_02::12345</code>.</li>
<li>Un identifiant de source ne sert jamais d'identifiant métier : il ne sort pas du staging et des modèles intermédiaires, et dans les marts, l'identifiant de référence s'appelle <code>id_produit</code>, même quand l'ERP fait foi. Sinon, le nom ne dit plus si l'on manipule l'identifiant de l'ERP ou l'identifiant unifié.</li>
</ul>

<p>Le bénéfice : le nom d'une clé de jointure dit le niveau de confiance qu'on peut lui accorder, et la valeur d'un identifiant dit d'où elle vient sans remonter le lignage.</p>

</details>

---

## Rendre la règle impossible à contourner

Des conventions écrites dans un fichier Markdown restent des vœux pieux. Avec 25 contributeurs et autant d'agents, elles ne tiennent que si la machine les fait respecter, au moment de l'écriture plutôt qu'en revue. Nous avons posé quatre verrous.

### 1. Une seule porte d'entrée : une CLI

Les agents n'écrivent pas le dictionnaire à la main : ils passent par une petite CLI Python, celle qui sert aussi à interroger notre couche sémantique. Elle répond aux deux questions qu'il faut se poser avant de nommer une colonne — ce nom existe-t-il déjà ? que veut-il dire ? — et c'est elle qui écrit :

```console
$ uv run scripts/semantic_layer.py search email
- colonne `email_magasin` (magasin.dimensions) — Adresse email du magasin.
- colonne `email_client` (client.dimensions) — Adresse email du client (en minuscules).
- colonne `est_optin_email_client` (client.dimensions) — Indique si le client a accepté les communications par email.
…

$ uv run scripts/semantic_layer.py add-column client dimensions email_client "Email du client."
colonne `email_client` déjà définie dans client.dimensions (l.836)

$ uv run scripts/semantic_layer.py add-column clients dimensions segment_client "Segment du client."
entité inconnue 'clients'. Proches : client.

$ uv run scripts/semantic_layer.py add-column client dimensions segment_client "Valeur de CUSTOMER_TIER__C."
la description cite un nom de champ source `CUSTOMER_TIER__C` : une définition métier ne le porte pas
```

Chaque écriture insère la ligne à sa place alphabétique, affiche le diff et lance le contrôle complet avant et après : si elle introduit un écart, elle est annulée. Renommer ou supprimer une colonne est refusé tant que la couche sémantique l'utilise ; sinon, la commande liste les modèles qui citent encore l'ancien nom. Les commandes de lecture acceptent une révision Git (`--ref`), pour relire le dictionnaire tel qu'une Pull Request le modifie.

Au passage, l'agent ménage son contexte : il charge une définition, pas un fichier de plusieurs dizaines de milliers de tokens.

### 2. Un contrôle après chaque écriture d'un agent

Dans Claude Code, deux *hooks* encadrent l'agent :

* **après chaque écriture de fichier**, un hook relance le contrôle si le dictionnaire ou la couche sémantique a changé — y compris quand l'agent a écrit le fichier sans passer par la CLI. Il remet le dictionnaire en ordre alphabétique et, s'il reste un écart, renvoie un code d'erreur : la liste des écarts revient à l'agent, qui corrige dans la même session, avant qu'un humain ne voie le diff ;
* **avant chaque lecture**, un autre hook refuse de charger ces deux fichiers en entier, et indique à l'agent la commande qui répond à sa question.

L'agent n'a pas besoin de se souvenir de la règle : il ne peut pas l'enfreindre sans que la machine le lui dise.

### 3. Une vérification avant de rendre la main

Le *skill* dbt — les instructions que l'agent charge avant de toucher à un modèle — se termine par une porte de sortie. Avant de déclarer le travail terminé, l'agent cherche dans le dictionnaire chaque colonne du `select` final de chaque modèle modifié, et en rend compte : « Dictionnaire : 24 colonnes vérifiées dans 3 modèles, 0 manquante ». Une colonne manquante est définie dans le même diff que le modèle.

### 4. La CI

Le même contrôle tourne enfin dans la CI, sur chaque Pull Request comme sur main, dès que le dictionnaire ou la couche sémantique change, avant que dbt ne s'exécute.

Résultat : un nouveau nom arrive avec sa définition, dans le même diff que le SQL qui le crée. Anthropic obtient cela par la discipline de ses équipes ; nous le confions, autant que possible, à la machine.

<details>
<summary><strong>Pour aller plus loin : les hooks Claude Code et ce que vérifie le contrôle</strong></summary>

<p>Les deux hooks, déclarés dans le <code>.claude/settings.json</code> du repository (version simplifiée) :</p>

<pre><code class="language-json">{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Read",
        "hooks": [{"type": "command", "command": "uv run scripts/semantic_layer.py read-hook"}]
      }
    ],
    "PostToolUse": [
      {
        "matcher": "Write|Edit",
        "hooks": [{"type": "command", "command": "uv run scripts/semantic_layer.py hook || exit 2"}]
      }
    ]
  }
}</code></pre>

<p>Claude Code transmet l'appel d'outil en JSON sur l'entrée standard : le script regarde quel fichier est visé et ne fait rien pour les autres. Le code de sortie 2 fait tout le travail. Après une écriture, il renvoie le message d'erreur à l'agent, qui le traite comme un retour à corriger ; avant une lecture, il bloque l'outil, et le message indique la commande à utiliser à la place.</p>

<p>Le contrôle, lancé par le hook, par chaque écriture de la CLI et par la CI, vérifie que :</p>

<ul>
<li>chaque colonne tient sur une ligne, en ordre alphabétique dans sa section ;</li>
<li>chaque nom n'est défini qu'une fois dans tout le fichier, toutes entités et sections confondues ;</li>
<li>chaque entité a une description, et chaque colonne une définition non vide ;</li>
<li>aucune définition ne cite un champ source (<code>CUSTOMER_TIER__C</code>, ou un nom en majuscules entre parenthèses) ni un modèle dbt (<code>stg_…</code>, <code>fct_…</code>) ;</li>
<li>chaque entité, dimension et attribut de la couche sémantique a sa définition dans le dictionnaire, et une entité inconnue y est signalée avec les noms les plus proches.</li>
</ul>

</details>

---

## Le data portal : une documentation calculée, jamais écrite

Si la définition est attachée au nom, la documentation d'un modèle n'a plus besoin d'être écrite. **C'est une jointure entre ses colonnes et le dictionnaire.**

À chaque mise en production, un script génère notre data portal :

1. `dbt compile` produit le manifeste, qui contient le SQL compilé de chaque modèle ;
2. sqlglot analyse ce SQL et en extrait les colonnes du `select` final, y compris derrière un `select * from final`, en déroulant les CTE jusqu'à leurs alias ;
3. chaque nom est cherché dans le dictionnaire.

Le portal en tire :

* **une page par modèle**, avec ses colonnes, leur définition et leurs tests, un aperçu des données, le lignage, les usages en aval et le SQL. Une zone « Ask AI » y traduit une question en requête SQL : le LLM reçoit les colonnes de la table *avec leur définition*, et le dictionnaire devient le contexte du text-to-SQL ;
* **une page dictionnaire**, qui expose l'intégralité des définitions regroupées par entité métier, avec pour chacune ses dimensions, ses faits et ses métriques. Chaque colonne y renvoie aux marts qui la portent. C'est un index inversé, qui répond à « où trouver le montant TTC d'une commande ? » sans lire une ligne de SQL — et le glossaire métier que nous n'avons jamais eu à acheter ni à synchroniser.

Le même script liste enfin, modèle par modèle, les colonnes qui n'ont pas de définition — hors couche d'exposition, dont les colonnes suivent le contrat d'interface des outils qu'elle alimente.

<details>
<summary><strong>Pour aller plus loin : extraire les colonnes d'un modèle avec sqlglot</strong></summary>

<p>Le cœur de l'extraction tient en quelques lignes :</p>

<pre><code class="language-python">import sqlglot
import sqlglot.expressions
import sqlglot.optimizer.qualify_columns
import sqlglot.schema


def output_columns(compiled_sql: str, dictionary: dict[str, str]) -&gt; list[dict]:
    """Les colonnes du select final d'un modèle compilé, avec leur définition."""
    tree = sqlglot.parse_one(compiled_sql, read="snowflake")
    # Déroule les `select *` sur des CTE : `select * from final` rend les alias de `final`.
    tree = sqlglot.optimizer.qualify_columns.qualify_columns(
        tree, schema=sqlglot.schema.MappingSchema(), dialect="snowflake"
    )
    select = tree.find(sqlglot.expressions.Select)
    columns = []
    for expression in select.expressions:
        if isinstance(expression, sqlglot.expressions.Star):
            continue  # un `select *` sur un autre modèle : signalé sur la page du modèle
        name = expression.alias_or_name.lower()
        columns.append({"name": name, "description": dictionary.get(name, "")})
    return columns</code></pre>

<p>Quelques précautions en production :</p>

<ul>
<li>le SQL vient du manifeste dbt (<code>compiled_code</code>, après <code>dbt compile</code>), débarrassé de ses éventuels restes de Jinja ;</li>
<li>sans schéma, <code>qualify_columns</code> échoue sur certaines requêtes : il est appelé dans un <code>try</code>, et l'arbre non qualifié sert alors tel quel ;</li>
<li>un <code>select *</code> qui subsiste porte sur un autre modèle, dont sqlglot ignore les colonnes : la page du modèle le signale ;</li>
<li>si sqlglot ne sait pas analyser le SQL, un repli par expression régulière récupère les alias <code>as …</code>.</li>
</ul>

<p>Le dictionnaire, lui, est aplati en <code>{nom: définition}</code> : chercher une colonne est une simple lecture de dictionnaire Python, et la page dictionnaire du portal se construit en inversant la relation — pour chaque nom, les marts qui le portent.</p>

</details>

---

## Une définition, tous ses lecteurs

La même ligne du dictionnaire sert tout le monde :

```
                Dictionnaire métier
        (un nom, une définition, une fois)
                         │
     ┌─────────────┬─────┴───────┬──────────────┐
     ▼             ▼             ▼              ▼
 Data portal   Agents de    Serveur MCP    Text-to-SQL
 (humains)     code (CLI)   (assistants)   (Ask AI)
```

* **les humains**, dans le data portal ;
* **les agents de code**, par la CLI et ses hooks ;
* **les assistants d'IA**, via notre serveur MCP : son catalogue reprend, pour chaque entité qu'il sert, la description du dictionnaire, et son outil de recherche y trouve la définition de chaque colonne ;
* **le text-to-SQL** du portal.

Corriger une définition, c'est la corriger pour tous ses lecteurs, au déploiement suivant. Il n'existe pas de deuxième copie à oublier.

---

## Ce que ça change

* **Des agents qui cherchent au lieu de deviner.** Avant de créer une colonne, l'agent cherche le nom existant, et le trouve. Réutiliser devient le chemin par défaut, parce que la CLI rend l'existant visible et refuse les doublons. Autant d'erreurs d'agent qui disparaissent : synonymes inventés, jointures entre deux concepts différents, booléens encodés en `'O'` et `'N'`.
* **Aucune copie qui dérive, presque aucune maintenance.** Une définition se change en une ligne, à un seul endroit. Pas de bloc `doc()`, pas d'outil de propagation, pas de quinze fichiers YAML à réaligner. Renommer une colonne est une commande, qui dit quels modèles citent encore l'ancien nom.
* **Une revue métier plutôt qu'une revue SQL.** Dans la Pull Request d'un contributeur métier, le diff du dictionnaire est le résumé métier du changement : quels nouveaux concepts, définis comment. Le relecteur lit trois lignes de définitions avant trois cents lignes de SQL, et la machine a déjà vérifié le format, l'unicité et la cohérence. Il concentre son attention sur la seule question qu'elle ne sait pas trancher : s'agit-il vraiment d'un nouveau concept ? Quand [la revue devient le chemin critique](https://unytics.io/blog/fr/nobody-codes-by-hand/), c'est un gain direct de débit.
* **Des métiers qui contribuent sans apprendre les conventions.** Un contrôleur de gestion qui vibe-code un modèle n'a pas besoin de connaître nos règles de nommage : l'agent les applique, les outils les font respecter. C'est l'une des conditions qui permettent à une vingtaine de métiers de contribuer à la plateforme sans alourdir la revue.
* **Des jointures qui se devinent.** Même nom, même concept, même type, même format : une jointure sur `id_produit` entre deux marts est toujours valide, et le suffixe d'un identifiant dit jusqu'où il a été unifié.
* **Un contexte prêt pour l'IA.** Le serveur MCP et le text-to-SQL lisent les mêmes définitions que les humains. Quand un assistant hésite entre deux colonnes, c'est la définition qui tranche, et c'est la même pour tous.
* **Un vocabulaire qui nous appartient.** Le dictionnaire est un fichier YAML versionné dans notre repository, pas une base dans l'outil d'un éditeur. Comme le reste de notre logique métier, il [survit à un changement d'outil](https://unytics.io/blog/fr/optic-2000-independence/).

---

## Ce qu'il faut en retenir

Documenter un modèle, c'est décrire une table. Documenter un nom, c'est construire un vocabulaire, que partagent tous les modèles, toutes les équipes et tous les agents.

Avec les agents de code, le nommage cesse d'être une affaire de style pour devenir une interface : c'est par les noms qu'un agent comprend la donnée, et c'est par eux qu'il se trompe. Nous avons traité le nom et sa définition comme une clé et sa valeur, écrites une seule fois. Tout le reste — pages du portal, contexte des agents, glossaire métier — en est calculé.

Posez-vous la question pour votre propre plateforme : **combien d'endroits faut-il modifier pour changer la définition d'une colonne ?** Si la réponse est plus d'un, la dérive n'est qu'une question de temps.

---

*Vous voulez rendre votre data platform lisible par vos équipes comme par vos agents d'IA ? [Parlons-en lors d'un échange data de 30 minutes](https://unytics.io/book-meeting/).*
