# Et si vos métiers construisaient la data platform ?

**Forward Data Conference · 16 novembre 2026 · 25 minutes · Paul Marcombes**

Contenu oral du talk : 44 slides, 3 031 mots à dire. C'est le même texte que les notes de présentation du deck (version HTML et backup Google Slides), slide par slide.

## Mode d'emploi

- **[clic]** : fais apparaître l'élément suivant de la slide. Les apparitions progressives existent dans la version HTML ; dans le backup Google Slides, tout est affiché d'emblée.
- Les repères de temps (`m:ss`) indiquent le moment où tu arrives sur la slide. Ils supposent 140 mots par minute, deux secondes par changement de slide et une seconde et demie par clic : **24:20 au total**. À 125 mots par minute, compte 26:56 ; à 155, 22:15.
- Chronomètre une répétition à voix haute avant de couper ou d'ajouter quoi que ce soit : ton débit réel compte plus que ces estimations.
- *(coupe possible)* : slide à sauter si tu es en retard. Voir « Si tu dépasses ».

## Le fil rouge

1. Tout le monde veut du conversationnel pour **consommer** la donnée. Mais une IA ne répond juste que si le contexte est préparé et entretenu : l'équipe data reste le goulot d'étranglement.
2. Chez Optic 2000, le conversationnel est **au début de la chaîne**, dans l'éditeur de code : ceux qui analysent construisent la plateforme en même temps.
3. Résultat : de 4 à 25 contributeurs, en majorité des métiers, et des applications que l'équipe data n'aurait pas imaginées.
4. Ça ne tourne pas au chaos, parce que la contribution est ennuyeuse (un seul repo, une seule façon de faire) et que la plateforme apprend de chaque revue.
5. Le conversationnel pour ceux qui consomment reste indispensable, pour les magasins. Et des métiers qui arrivent dans les repos de code, c'est une tendance qui dépasse notre cas : seul change ce qu'on y construit.

La phrase à faire retenir : **le village d'analystes existe déjà, ce sont vos métiers.**

La question à laisser à la salle : *chez vous, qui pourrait devenir builder dès demain ?*

### La structure

- Une slide de plan (slide 8) après le premier acte : elle annonce trois temps, « ce qui s'est passé », « comment ça tient », « ce que nous en retenons ».
- Chaque partie, de 02 à 08, s'ouvre sur une slide sombre : slides 9, 13, 19, 22, 29, 35 et 40. L'étiquette en haut de chaque slide rappelle le numéro de la partie.


## Plan et minutage

| Partie | Slides | Début | Durée | Mots |
| --- | --- | --- | --- | --- |
| 0 · Ouverture | 1 | 0:00 | 0:36 | 80 |
| 1 · Le paradoxe conversationnel | 2–8 | 0:36 | 3:58 | 491 |
| 2 · La fin des silos | 9–12 | 4:34 | 2:19 | 295 |
| 3 · Le métier devient builder | 13–18 | 6:53 | 3:20 | 414 |
| 4 · Au-delà du dashboard | 19–21 | 10:13 | 2:04 | 265 |
| 5 · L'architecture anti-chaos | 22–28 | 12:17 | 3:55 | 499 |
| 6 · La plateforme qui apprend | 29–34 | 16:13 | 3:00 | 357 |
| 7 · Builders et consumers | 35–39 | 19:13 | 2:52 | 354 |
| 8 · Le shift humain | 40–44 | 22:05 | 2:16 | 276 |
| **Total** | **1–44** | | **24:20** | **3 031** |

## Script

### Ouverture

#### Slide 1 · Titre · `0:00`

*À l'écran : Le titre du talk, ton nom, tes rôles. À droite, 25 points : le « village » qui reviendra plus loin.*

Bonjour à tous. Je m'appelle Paul Marcombes. J'ai passé six ans à construire la data chez Nickel, où l'équipe est passée de trois à plus de quarante personnes. Et depuis janvier, je suis Head of Data Platform chez Optic 2000, en indépendant. En dix mois, nous y avons reconstruit toute la plateforme data. Et je voudrais vous raconter ce qui nous a le plus surpris en chemin : ceux qui construisent aujourd'hui cette plateforme ne sont pas ceux que vous imaginez.

### Partie 1 · Le paradoxe conversationnel

#### Slide 2 · Tout le monde veut parler à ses données · `0:36`

*À l'écran : Un échange de chat : la question d'un métier, puis la réponse avec un mini-graphique.*

Aujourd'hui, si vous discutez avec vos directions générales ou vos directions métiers, la demande est unanime : tout le monde veut de l'analytique conversationnelle. **[clic]** On nous vend le rêve d'une interface où n'importe quel collaborateur pose une question à ses données, en langage naturel, **[clic]** et obtient instantanément une analyse pertinente. Et ce rêve devient réalité : on en voit de très beaux exemples ici même, aujourd'hui.

#### Slide 3 · Sous le capot, le contexte fait la réponse · `1:09`

*À l'écran : Trois chiffres qui apparaissent un à un (21 %, 95 %, 65 %), puis la phrase du « village d'analystes ».*

Mais nous sommes entre équipes data : nous savons ce qu'il y a sous le capot. L'équipe data d'Anthropic l'a très bien raconté en juin. **[clic]** Branché à froid sur leur entrepôt, Claude donne 21 % de bonnes réponses. **[clic]** Avec une équipe senior qui organise le contexte — tables de référence, couche sémantique, skills, tests — ils montent à plus de 95 %. **[clic]** Et un mois plus tard, faute d'entretien, ils retombent à 65 %. Le contexte ne se prépare pas une fois : il s'entretient. **[clic]** Certains en ont tiré une conclusion : pour que le self-service fonctionne, il faut tout un village d'analystes. Gardez cette image en tête, j'y reviendrai.

#### Slide 4 · En pleine analyse, il manque une donnée · `2:00`

*À l'écran : Deux cartes : « Bricoler dans son coin », puis « Ouvrir un ticket et attendre ».*

Concrètement, un métier est en pleine analyse, et il lui manque une donnée : une colonne, une table, une mesure. Il a deux options. **[clic]** Soit il bricole dans son coin, avec un export et un fichier Excel. C'est le shadow data : ce qu'il a compris ne revient jamais dans la plateforme. **[clic]** Soit il ouvre un ticket, et il attend que l'équipe data prépare la donnée. Avant, on ouvrait un ticket pour avoir un dashboard. Maintenant, on ouvre un ticket pour avoir une colonne dans la couche sémantique. C'est du ticketing 2.0 : l'équipe data reste le goulot d'étranglement.

#### Slide 5 · Chez Optic 2000, tout change en même temps · `2:47`

*À l'écran : « 10 mois », « 6 → 4 », et la liste des cinq chantiers.*

Chez Optic 2000, nous avions cette année un problème supplémentaire : tout changeait en même temps. En dix mois, nous avons remplacé le socle PostgreSQL historique, absorbé une nouvelle caisse, un nouveau CRM, un nouveau programme de fidélité, et débranché notre outil de BI. Le tout avec une équipe plateforme passée de six à quatre personnes. Autant vous dire que notre équipe BI n'avait pas une minute pour traiter de nouveaux sujets métiers. Nous étions face à un mur de bande passante.

#### Slide 6 · Le marché met le conversationnel à la fin · `3:23`

*À l'écran : La chaîne Sources → Transformations → Couche sémantique → Applications. La bulle « Conversationnel » est au-dessus de la dernière brique.*

Face à ce mur, nous avons pris le contre-pied du marché. Regardez une plateforme data classique : des sources, des transformations, une couche sémantique, des applications. L'équipe data prépare, les métiers consomment. Et le marché branche le conversationnel tout au bout de la chaîne, dans une interface de consommation.

#### Slide 7 · Nous l'avons mis au début · `3:46`

*À l'écran : La bulle s'étire sur toute la chaîne (transition animée), puis la phrase « L'analyse construit la plateforme. »*

Nous, nous l'avons mis au tout début : directement dans l'éditeur de code, là où la plateforme se construit. Pourquoi ? Pour qu'au moment même où un métier cherche à faire une analyse, l'IA l'aide à préparer et à enrichir la donnée, à la source, dans la plateforme. C'est la troisième option : ni bricoler, ni attendre. Construire. **[clic]** L'analyse construit la plateforme.

#### Slide 8 · Au programme · `4:15`

*À l'écran : Trois colonnes : ce qui s'est passé, comment ça tient, ce que nous en retenons.*

Voici comment nous en sommes arrivés là. D'abord, ce qui s'est passé : notre équipe BI, puis les métiers, puis des applications que nous n'attendions pas. Ensuite, comment tout cela tient sans tourner au chaos. Et enfin, ce que nous en retenons.

### Partie 2 · La fin des silos

#### Slide 9 · « Laisser des non-développeurs coder dans le repo ? » · `4:34`

*À l'écran : Slide sombre : la question du sceptique.*

Je vous vois sourire. Laisser des non-développeurs coder dans le dépôt central de la data platform ? Moi-même, j'étais très sceptique au démarrage. Alors nous avons procédé par étapes. Et nous avons commencé par le plus proche de nous : notre propre équipe BI.

#### Slide 10 · Avant : trois équipes, trois silos · `4:54`

*À l'écran : Trois cartes : 4 Data Engineers, 2 BI Engineers, 4 BI.*

Historiquement, la data chez Optic 2000, c'étaient trois équipes étanches. Quatre data engineers, qui géraient l'ingestion et les transformations, dans des procédures stockées PostgreSQL. Deux BI engineers, qui administraient la couche sémantique dans MicroStrategy. Et quatre personnes à la BI, qui construisaient les dashboards en clic-bouton. Cette équipe BI savait lire un peu de SQL. Mais elle n'avait jamais touché à Git, ni à Python, ni à dbt.

#### Slide 11 · Le test : converser au lieu de cliquer · `5:25`

*À l'écran : En haut : Tableau en clic-bouton → les apps Streamlit vibe-codées. En bas, trois résultats qui apparaissent un à un.*

En quittant MicroStrategy, Optic 2000 avait d'abord choisi Tableau. Et l'équipe BI y passait un temps phénoménal, sur des tâches clic-bouton, répétitives et laborieuses. Nous leur avons proposé un test : construire leurs tableaux de bord sous forme d'applications Streamlit, en vibe-codant dans notre repo, avec l'IA. Eux-mêmes étaient sceptiques : est-ce que ce sera propre ? Est-ce que les chiffres seront justes ? Est-ce qu'on saura le maintenir ? **[clic]** En quelques semaines, le déclic a été spectaculaire : ils sont devenus autonomes. **[clic]** L'expérience de l'utilisateur final est dix fois meilleure, pour une fraction du temps que nous passions sur Tableau. **[clic]** Et surtout, ils ne se sont pas arrêtés à Streamlit : d'eux-mêmes, ils se sont mis à créer et à maintenir leurs propres modèles dbt.

#### Slide 12 · Aujourd'hui : deux équipes au lieu de trois · `6:23`

*À l'écran : La carte du milieu a disparu : la BI occupe toute la chaîne. En bas, Streamlit et les magasins.*

Aujourd'hui, nous sommes passés à deux équipes : quatre data engineers, quatre BI, et plus de couche intermédiaire. La BI maîtrise toute la chaîne, du modèle dbt jusqu'à l'application. Et Streamlit est devenu notre outil de dashboarding, y compris pour des milliers d'utilisateurs en magasin. Les data engineers, eux, posent le cadre et accompagnent ceux qui construisent. Retenez ce déplacement : nous allons le retrouver, en plus grand.

### Partie 3 · Le métier devient builder

#### Slide 13 · Pourquoi s'arrêter à l'équipe BI ? · `6:53`

*À l'écran : Slide sombre : la question.*

Quand nous avons vu notre équipe BI créer des modèles marts impeccables, sans aucun bagage logiciel au départ, nous nous sommes dit : pourquoi s'arrêter là ?

#### Slide 14 · Nous sommes allés voir les métiers du siège · `7:06`

*À l'écran : Cinq métiers en étiquettes, puis deux phrases.*

Nous sommes allés voir les métiers du siège. Les chefs de projet AMOA. Le contrôle de gestion. La finance. La comptabilité. Le marketing digital. **[clic]** Des profils analytiques, qui ont l'habitude de suivre leurs chiffres. Mais qui n'avaient jamais écrit une ligne de code.

#### Slide 15 · La barrière à l'entrée est quasi nulle · `7:28`

*À l'écran : Trois lignes barrées, « Ils conversent. », puis la conversation d'un chef de projet AMOA avec l'agent.*

Et là, il faut casser un mythe : aujourd'hui, la barrière à l'entrée pour contribuer dans un repo est quasi nulle. Ces collaborateurs n'écrivent pas de code. Ils ne lisent même pas le code. Et ils ne tapent aucune commande Git. **[clic]** Ils conversent, tout simplement, avec Claude : dans VS Code, ou directement dans Claude Desktop. **[clic]** Un exemple. Un chef de projet AMOA, qui connaît SAP et travaille avec la logistique, a rapatrié des données de SAP dans Snowflake, les a mises en qualité selon nos conventions, et a construit un dashboard opérationnel de suivi des KPI des équipes logistiques. En une seule conversation. C'est l'agent qui a géré Git, les branches et le code. Et à la fin de la conversation, la plateforme s'est enrichie.

#### Slide 16 · Tout commence par un petit sujet · `8:26`

*À l'écran : À gauche la phrase, à droite une maquette d'app de suivi.*

Tout a commencé par de petits sujets annexes. Une cheffe de projet s'est construit une application de suivi de ses tickets Jira, pour mieux piloter ses chantiers. Rien de stratégique. Mais c'est comme ça que la confiance s'installe : la sienne, et la nôtre.

#### Slide 17 · Puis les sujets deviennent critiques · `8:46`

*À l'écran : À gauche, avant et aujourd'hui. À droite, son cockpit : deux barres de dates qui se chevauchent.*

Puis la confiance s'est installée, et la complexité a bondi. Exemple : le responsable du référentiel magasins, dans Salesforce. Les magasins bougent en permanence, avec des rachats et des ouvertures. Avant, c'est nous qui écrivions des tests dbt sur ce référentiel. Quand un test tombait en erreur, nous le prévenions, et il corrigeait après coup. **[clic]** Aujourd'hui, il s'est construit son propre cockpit, beaucoup plus détaillé que nos tests. Par exemple, quand un magasin est racheté, les dates d'ouverture de l'ancien et du nouveau ne doivent pas se chevaucher. Il voit les incohérences, et il peut être proactif. Ces règles de gestion, c'est lui qui les connaît. Pas nous.

#### Slide 18 · De 4 à 25 contributeurs en dix mois · `9:36`

*À l'écran : « 4 → 25 », puis trois rangées de points : plateforme, BI, métiers.*

Résultat : en dix mois, le nombre de personnes qui contribuent à notre repo data est passé de 4 à 25. **[clic]** Quatre à la plateforme. **[clic]** Quatre à la BI. **[clic]** Et tous les autres sont des métiers. Aucune de ces vingt-cinq personnes ne code à la main. Vous vous souvenez du village d'analystes qu'il faudrait pour faire vivre le self-service ? Le voilà. Sauf que nous ne l'avons pas recruté : il était déjà dans l'entreprise.

### Partie 4 · Au-delà du dashboard

#### Slide 19 · Plus de contributeurs, ce sont plus d'idées · `10:13`

*À l'écran : Slide sombre : la phrase seule.*

Et en démultipliant le nombre de contributeurs, on ne gagne pas seulement du temps. On fait émerger des idées que nous n'avions absolument pas anticipées. Au départ, nous pensions que Streamlit servirait uniquement à afficher des graphiques au-dessus de Snowflake. Les métiers nous ont prouvé le contraire. J'y vois deux dynamiques.

#### Slide 20 · Première dynamique : remplacer des SaaS · `10:37`

*À l'écran : Deux cartes : le géomarketing, puis les liasses fiscales.*

La première, c'est le remplacement de SaaS. Au géomarketing, nous payions un logiciel propriétaire, assez rigide, pour visualiser les zones de chalandise et de concession sur la carte de France. La personne en charge a intégralement recréé son outil dans Streamlit. Il répond enfin à 100 % de ses besoins, et nous supprimons une licence coûteuse. **[clic]** Même chose pour les liasses fiscales des magasins. Au lieu de les ressaisir à la main chaque année, ou de payer très cher un logiciel d'OCR, nous avons une application de reconnaissance automatique, avec un humain dans la boucle pour valider. Avec exactement la même qualité.

#### Slide 21 · Seconde dynamique : sublimer les back-ends · `11:24`

*À l'écran : Hier : SAP → Excel → ressaisies. Aujourd'hui : SAP ↔ front-end Streamlit ↔ métier. Puis la phrase finale.*

La seconde dynamique est encore plus stratégique : sublimer nos back-ends. Nous n'avons aucune envie de remplacer SAP ou Salesforce : ce sont des back-ends robustes et standards. En revanche, leurs interfaces sont arides. Optic 2000 a été créé en 1969, et nous avons encore énormément de processus manuels, notamment par-dessus SAP : des exports Excel, puis des heures de manipulations, répétitives, avec un vrai risque d'erreur. **[clic]** Aujourd'hui, nos métiers créent des front-ends Streamlit ergonomiques, branchés directement sur SAP et Salesforce, et taillés pour leurs processus. Nous n'en sommes qu'au début. Mais c'est l'usage que nous avions le moins imaginé, et peut-être celui qui changera le plus la donne. **[clic]** Un dashboard montre. Une data app agit.

### Partie 5 · L'architecture anti-chaos

#### Slide 22 · « C'est génial sur le papier. Mais… » · `12:17`

*À l'écran : Slide sombre : l'objection de la salle.*

À ce stade, je sais ce que pense la moitié de la salle. « C'est génial sur le papier. Mais laisser vingt ou trente métiers coder dans la data platform, ça va créer un plat de spaghettis impossible à maintenir. Et on passera plus de temps à relire leur code qu'à l'écrire nous-mêmes. » Vous avez raison de poser la question : c'est exactement celle que je me posais. Voici comment nous évitons le chaos.

#### Slide 23 · Premier pilier : un seul repo · `12:50`

*À l'écran : Un grand cadre « Mono-repo Git » qui contient les quatre briques, puis le trait « une conversation, une pull request ».*

Premier pilier : le mono-repo. L'intégralité de notre plateforme — l'ingestion, les transformations dbt, la couche sémantique, les applications Streamlit — vit dans un seul et unique dépôt Git. Si nos outils étaient éclatés, aucun agent ne pourrait comprendre le contexte de bout en bout. **[clic]** Là, pendant qu'un métier analyse une donnée, l'IA peut remonter à la source, enrichir la transformation, ajouter la mesure et créer l'écran. Dans le même mouvement. Dans la même pull request.

#### Slide 24 · Second pilier : une contribution ennuyeuse · `13:25`

*À l'écran : Deux cartes : la configuration (claire), la plomberie (sombre). Puis la phrase du bas.*

Second pilier : rendre le code le plus simple, le plus bête, le plus ennuyeux possible. Nous séparons radicalement deux choses. La configuration, qui dit de quoi le métier a besoin. Et la plomberie — le déploiement, la sécurité, la supervision — qui est écrite une seule fois, par l'équipe plateforme. Vous connaissez tous un outil qui fait ça : dbt. Vous écrivez un modèle SQL, et dbt gère pour vous l'incrémental et l'ordre d'exécution. Eh bien, dans notre repo, nous avons tout construit comme ça. **[clic]** Et ce qu'une contribution ne peut pas exprimer, un relecteur n'a pas à le vérifier.

#### Slide 25 · Une fonction : trois lignes de configuration · `14:10`

*À l'écran : Le YAML de la fonction (timeout: 600) → « AWS Lambda ».*

Un exemple. Pour créer une fonction, un contributeur écrit un script Python, sous un décorateur, et trois lignes de configuration : la planification, le timeout, la mémoire. C'est tout. Ici, le timeout est de dix minutes : la plateforme déploie la fonction sur une Lambda.

#### Slide 26 · Une fonction : trois lignes de configuration (suite) · `14:30`

*À l'écran : La même slide : le timeout passe à 3600, la cible devient « ECS Fargate » (transition animée). Puis la question à la salle.*

Si le timeout dépasse quinze minutes, elle la déploie sur une tâche Fargate. Même script, même décorateur. Le contributeur n'a même pas à le savoir. Il n'existe pas de champ « backend » : ce qu'on ne peut pas déclarer, on ne peut pas le déclarer faux. **[clic]** Posez-vous la question pour votre propre plateforme : quand quelqu'un ajoute une source ou un traitement, combien de lignes de plomberie écrit-il ?

#### Slide 27 · Une seule façon de faire chaque chose · `15:02`

*À l'écran : Slide sombre : la phrase seule.*

Cet ennui a un effet direct sur l'IA. Dans un repo où chaque pipeline est écrit différemment, un agent doit deviner : il invente, il mélange les conventions. Dans un repo où il n'existe qu'une seule façon de faire chaque chose, il n'a qu'à copier le bon modèle. Chez nous, la trentième source ressemble exactement à la vingt-neuvième. L'agent copie la précédente. Et il a raison.

#### Slide 28 · Dans les apps, l'IA assemble des briques · `15:32`

*À l'écran : À gauche, une app en blocs (cartes, graphique, tableau). À droite, deux cartes qui apparaissent.*

Même logique dans les applications. **[clic]** L'équipe BI a créé elle-même une bibliothèque de composants standardisés — des cartes d'indicateurs, des tableaux, des graphiques — et nos skills imposent à l'IA de les utiliser. **[clic]** Quant aux chiffres, les applications destinées aux magasins s'appuient à 100 % sur la couche sémantique : la logique des mesures est définie à un seul endroit, et l'application ne fait que les appeler et les afficher. Résultat : des applications homogènes, les mêmes chiffres partout, et une IA qui n'invente rien. Elle assemble des briques.

### Partie 6 · La plateforme qui apprend

#### Slide 29 · Il faut aussi tenir dans la durée · `16:13`

*À l'écran : Slide sombre : la phrase seule.*

Éviter le chaos au premier jour, c'est une chose. Mais il faut aussi tenir dans la durée.

#### Slide 30 · Restent deux dangers : la dérive et la revue · `16:22`

*À l'écran : Deux cartes : la dérive, puis la revue.*

Deux vrais dangers guettent. Le premier, c'est la dérive : dès qu'une même chose est décrite à plusieurs endroits, les versions finissent par diverger, et l'IA suit la mauvaise. **[clic]** Le second, c'est la revue. Quatre personnes ne peuvent pas relire tout ce que produisent vingt-cinq contributeurs et leurs agents. Si nous n'y prenons pas garde, nous avons juste déplacé le goulot d'étranglement, des tickets vers les pull requests.

#### Slide 31 · Trois noms pour un même concept · `16:54`

*À l'écran : Trois noms de colonnes, trois modèles dbt, trois descriptions.*

Contre la dérive, nous avons des règles d'ingénierie draconiennes. Regardez ce que produit un projet dbt classique : « email » dans le staging, « email_client » dans la dimension, « customer_email » dans l'export. Trois noms, trois descriptions, pour un seul concept. Laquelle est la bonne ? Et laquelle l'agent recopiera-t-il dans le quatrième modèle ?

#### Slide 32 · Un concept, un nom, une définition · `17:17`

*À l'écran : Il ne reste qu'un nom (transition animée) et sa définition. Puis trois chiffres : 1 800, 350, 0.*

Chez nous, la règle est stricte : un concept métier n'a qu'un seul nom de colonne dans tout l'entrepôt, et un nom ne désigne qu'un seul concept. Du coup, nous ne documentons plus les modèles dbt un par un : nous documentons les noms, une seule fois, dans un dictionnaire unique. **[clic]** 1 800 noms de colonnes, 350 modèles dbt, et pas une seule description de colonne dans dbt.

#### Slide 33 · La machine vérifie avant le relecteur · `17:48`

*À l'écran : Quatre étapes qui apparaissent une à une, puis la question finale.*

Ensuite, la revue. La machine vérifie avant le relecteur. D'abord, l'agent code avec tous nos skills. **[clic]** Des hooks lui évitent les oublis : à chaque sauvegarde d'un modèle dbt, un script extrait les colonnes avec sqlglot et les cherche dans le dictionnaire métier. **[clic]** Le skill de PR lance deux revues, dbt et Streamlit, et itère avec l'utilisateur jusqu'au feu vert. **[clic]** La pull request arrive propre : le relecteur ne voit que ce que nos règles n'avaient pas prévu. **[clic]** Il lui reste la seule question qu'aucune machine ne peut trancher : est-ce la bonne chose à construire ?

#### Slide 34 · Chaque commentaire de revue devient une règle · `18:36`

*À l'écran : Une boucle en quatre temps, qui se construit clic après clic.*

Et voici notre règle d'or. Chaque fois qu'un ingénieur écrit un commentaire dans une pull request, **[clic]** il doit se demander : pourquoi l'IA a-t-elle laissé passer ça ? **[clic]** Et mettre à jour le skill, immédiatement. **[clic]** Le commentaire ne corrige pas seulement cette pull request : il corrige toutes les suivantes. **[clic]** Grâce à cette boucle, la plateforme apprend de chaque revue. Et nos pull requests deviennent quasiment instantanées à valider.

### Partie 7 · Builders et consumers

#### Slide 35 · Faut-il mettre tout le monde dans VS Code ? · `19:13`

*À l'écran : Slide sombre : la question, puis la réponse au clic.*

Est-ce que tout cela veut dire qu'il faut jeter l'analytique conversationnelle classique, et mettre tout le monde dans VS Code ? **[clic]** Absolument pas. La preuve : nous faisons les deux.

#### Slide 36 · Deux populations, deux visages de l'IA · `19:28`

*À l'écran : Deux cartes : au siège (ils construisent), puis en magasin (ils consomment).*

Il faut distinguer deux populations. Au siège, les profils analytiques utilisent l'IA pour construire des actifs durables, dans le repo. **[clic]** Mais un opticien, dans l'un de nos magasins, n'ouvrira jamais un éditeur de code. Ça n'aurait aucun sens. Lui, il doit être servi comme un client.

#### Slide 37 · En magasin, l'IA se consomme sous deux formes · `19:51`

*À l'écran : Deux cartes reliées à une barre « Couche sémantique ».*

Pour les magasins, l'IA prend deux formes. D'abord, des agents spécialisés, embarqués dans leurs applications. Par exemple, un directeur de magasin consulte son bilan financier, et dialogue avec un agent expert en finance de l'optique : il se compare aux magasins similaires, il apporte son contexte local, il obtient des recommandations. **[clic]** Ensuite, ces mêmes expertises sont exposées par un serveur MCP et des skills : les magasins peuvent interroger leurs données depuis leur propre Claude ou leur propre ChatGPT. **[clic]** Dans les deux cas, les chiffres viennent de la même couche sémantique, et chacun ne voit que ses propres données.

#### Slide 38 · Nous avons déplacé la frontière · `20:38`

*À l'écran : Trois colonnes (Platformers, Builders, Consumers) et deux lignes : qui tient chaque rôle. La ligne orange (la frontière) se décale vers la gauche. Sous la ligne Optic 2000, les 25 contributeurs en points. Puis la phrase finale.*

Si je résume. Dans une organisation data, il y a trois rôles : ceux qui construisent la plateforme, ceux qui construisent dessus, et ceux qui consomment. Dans le modèle habituel, la frontière passe entre l'équipe data, qui construit, et les métiers, qui consomment. **[clic]** Nous, nous avons déplacé cette frontière. L'équipe plateforme construit le cadre. Et parmi ceux qui construisent dessus, il y a désormais plus de métiers que de data. **[clic]** Notre conviction : il faut mettre le plus de monde possible du côté des builders. Une équipe centrale ne détiendra jamais toute la connaissance de l'entreprise. Ce sont les métiers qui connaissent leurs données et leurs processus.

#### Slide 39 · Une tendance qui dépasse notre cas · `21:28`

*À l'écran : Trois cartes qui apparaissent une à une (équipes produit, marketing et GTM, toutes les équipes), puis la phrase de conclusion.*

Ce n'est pas propre à une entreprise comme la nôtre. Dans les équipes produit, un ticket Linear se crée depuis Slack, et quand c'est simple, un agent le code tout seul. **[clic]** Le marketing digital et le go-to-market, qui n'avaient jamais codé, se mettent à avoir leur propre repo. **[clic]** Et les équipes travaillent aussi dans les repos des autres : chez Supabase, le marketing ouvre des pull requests dans le repo data. **[clic]** Partout, le repo devient l'atelier de toute l'entreprise.

### Partie 8 · Le shift humain

#### Slide 40 · Pour conclure, deux messages · `22:05`

*À l'écran : Slide sombre : la phrase seule.*

Pour conclure, j'aimerais partager deux messages avec vous.

#### Slide 41 · Premier message : commencer petit, et itérer · `22:10`

*À l'écran : Un escalier de quatre marches, qui se construit clic après clic.*

Le premier : commencez petit, et itérez. N'ouvrez pas votre dépôt Git à cent métiers lundi matin. Nous avons commencé par notre équipe BI. **[clic]** Puis une cheffe de projet, sur un sujet sans enjeu. **[clic]** Chaque garde-fou dont je vous ai parlé a été construit pas à pas, au fil des premiers succès, et des premiers ratés. **[clic]** Et nous sommes nous-mêmes au début de l'histoire sur certains sujets, comme les front-ends SAP : les prochains mois vont servir à transformer l'essai.

#### Slide 42 · Second message : la clé est humaine · `22:50`

*À l'écran : « 1 sur 4 », quatre points dont un bleu. Puis la carte sur l'équipe BI.*

Le second : la clé n'est pas technologique, elle est humaine. Sur nos quatre data engineers, une personne travaille à plein temps pour embarquer et accompagner les métiers. **[clic]** Et le métier de notre équipe BI est en train de muter. Libérée du ticketing et du clic-bouton, elle devient proactive. Souvent, les métiers n'ont pas juste besoin d'un chiffre de plus : ils ont besoin d'un regard extérieur pour repenser leur façon de travailler. Et chez nous, le chantier est immense : c'est sur cette plateforme que l'équipe BI va aider à transformer tous ces processus encore manuels.

#### Slide 43 · Le village d'analystes existe déjà : ce sont vos métiers · `23:34`

*À l'écran : Slide bleue : la phrase à retenir, puis la question à emporter.*

On dit qu'il faut tout un village d'analystes pour faire vivre le self-service. Je crois que ce village existe déjà, dans chacune de vos entreprises : ce sont vos métiers. Alors gardez le conversationnel pour ceux qui consomment. **[clic]** Mais en rentrant, posez-vous une question : chez vous, qui pourrait devenir builder dès demain ? Aujourd'hui, notre équipe data ne construit plus de simples tableaux de bord. Elle co-construit la transformation opérationnelle de l'entreprise.

#### Slide 44 · Merci · `24:07`

*À l'écran : Merci, tes coordonnées, les quatre articles.*

Merci beaucoup. Tout ce que je vous ai raconté est détaillé dans quatre articles, sur le blog d'Unytics. Et je suis ravi de prendre vos questions.

## Si tu dépasses

Par ordre de préférence :

1. **Slide 16, « Tout commence par un petit sujet »** : sautable (gain : 0:20). Dis alors « tout a commencé par de petits sujets annexes » en arrivant sur la slide 17.
2. **Slide 28, « des briques »** : sautable (gain : 0:41). La couche sémantique revient slide 37.
3. **Slide 20** : ne garde qu'un des deux exemples.
4. **Slide 8, le plan** : passe-le en une phrase.

À ne pas couper : les slides 6 et 7 (le contre-pied), 18 (le village), 22 (l'objection), 34 (la règle d'or), 39 (une tendance qui dépasse notre cas) et 43 (le message).

## Si tu es en avance

- **Après la slide 33** : dis que cet ennui a un prix, payé par l'équipe plateforme. La plomberie est plus difficile à écrire, il faut savoir refuser les exceptions « juste pour cette fois », et les règles demandent un jardinage permanent (ton article *Ennuyeusement simple*). La slide correspondante a été retirée pour tenir les 25 minutes.
- **Slide 3** : chez Anthropic, près de 90 % des pull requests qui touchent un modèle de données embarquent une mise à jour de skill dans le même diff (ton article *Un nom, une définition*).
- **Slide 21** : cite d'autres apps nées sur la plateforme, comme le cockpit de suivi des pull requests au-dessus de Bitbucket, ou l'éditeur visuel de la couche sémantique.
- **Slide 34** : raconte une règle « apprise à la dure », par exemple « ne jamais couper une alimentation encore lue » (ton article *Ennuyeusement simple*).

## Questions probables

Des débuts de réponse, rédigés comme tu les dirais, et appuyés sur tes articles. Ce qui manque est signalé.

**« La revue des pull requests ne devient-elle pas le nouveau goulot d'étranglement ? »**

Oui, c'est notre chemin critique. Trois réponses. La contribution est de la configuration : il n'y a pas de plomberie à relire. La machine vérifie avant l'humain : des hooks à chaque sauvegarde, la CI, puis le skill de PR, qui fait tourner les agents de revue dbt et Streamlit jusqu'au feu vert, avant même l'ouverture de la pull request. Et chaque commentaire devient une règle : la même remarque ne revient pas. Chaque pull request reste validée par un humain.

**« Comment un métier valide-t-il un code qu'il ne lit pas ? »**

Il ne valide pas le code, il valide son résultat : ses chiffres, son application. Le diff du dictionnaire métier est le résumé du changement : trois lignes de définitions avant trois cents lignes de SQL. Avant même l'ouverture de la pull request, le verdict de l'agent relecteur lui parle en langage courant. Puis la pull request construit ses modèles dans un schéma à part, comparable à la production.

**« Qui est responsable quand le contributeur change de poste ? »**

Chaque modèle dbt et chaque data app déclare son propriétaire, et les pull requests sont assignées aux owners des domaines et des métriques. Comme il n'existe qu'une seule façon de faire, n'importe quel contributeur peut reprendre le travail d'un autre. *À préparer : ce que vous faites concrètement quand un propriétaire s'en va.*

**« Et la sécurité, le RGPD ? »**

L'agent d'un contributeur se connecte à l'entrepôt avec le compte et les rôles de ce contributeur : il ne lit que ce que la personne a le droit de lire. Une pull request ne peut rien déployer : les identifiants de production ne sont délivrés qu'aux pipelines qui tournent sur la branche principale. Côté magasins, le périmètre est appliqué par la couche sémantique, à partir de l'identité de l'utilisateur, quel que soit le canal : app, Teams ou serveur MCP.

**« Vos apps écrivent-elles dans SAP ? »**

Pas encore : aujourd'hui, elles lisent. C'est la prochaine étape, et elle demandera des garde-fous à la hauteur : tests, droits, validation humaine.

**« Combien ça coûte en tokens ? »**

*Aucun chiffre dans tes notes : à préparer.* Un point de comparaison disponible : la fin des licences BI par utilisateur, environ 50 € par personne et par mois d'après ton article sur l'indépendance.

**« Et le coût d'embarquement : installer VS Code, Git, former les gens ? »**

Chez nous, une personne sur quatre dans l'équipe plateforme s'en occupe à plein temps. Les métiers peuvent passer par Claude Desktop, sans éditeur. Les skills font le reste : commit, push et pull request en une seule commande. Et on commence par des sujets sans enjeu.

**« Pourquoi ne pas se contenter d'un bon agent conversationnel, avec une boucle de rétroaction ? »**

Nous le faisons aussi, pour ceux qui consomment, et ça fonctionne très bien pour les questions courantes. Deux limites dans une entreprise aux opérations complexes. Une équipe centrale de huit personnes ne connaîtra jamais la finesse de SAP ou du référentiel magasins. Et les métiers n'ont pas seulement besoin d'analyses : ils ont besoin d'applications qui transforment leurs processus.

**« Est-ce généralisable ? »**

Je le crois, et c'est la slide 39. Des métiers qui n'ont jamais codé arrivent dans les repos de code, y compris dans les entreprises digital native. C'est l'une d'elles qui m'a inspiré : Taha Le Bras, chez Supabase, me racontait qu'un matin, le marketing avait fait une pull request dans son repo data, et que lui-même, le même jour, en avait fait une dans celui du produit. Ce qui change d'une entreprise à l'autre, c'est ce qu'on y construit. Notre particularité, c'est le mono-repo : il permet à un agent de tout relier. Mais on peut ouvrir d'abord le repo dbt, puis y ramener le reste.

**« Pourquoi tout le monde n'est-il pas builder ? »**

Il faut une appétence analytique. Un opticien en magasin est un client de la plateforme, pas un contributeur. Et au siège, personne n'y est obligé.

**« L'interface de build ne devrait-elle pas être un serveur MCP, ou des artefacts Claude ? »**

C'est un continuum. Pour l'exploratoire et le léger, les artefacts suffisent, et ils sont imbattables en vitesse. Pour ce qui touche aux processus critiques, ce qui doit être testé, gouverné et déployé sur l'infrastructure de l'entreprise, nous voulons du code versionné dans Git et validé par pull request.

## Échos possibles aux autres talks de la journée

À utiliser seulement si le talk est passé avant le tien, et s'il a bien dit ce que tes notes en retiennent.

- **Juliette Duizabo**, une plateforme « boringly reliable », une seule façon de faire : à citer slide 24 ou 27.
- **Steve Buckingham** (Back Market), « the business builds things you never planned » : à citer slide 19.
- **Nicolas Martignole** (Back Market), 300 personnes qui codent dans VS Code, mais surtout des développeurs : à citer slide 14, pour marquer la différence. Chez vous, ce sont des métiers.
- **Medhi Ouazza**, des agents qui construisent en plus de consommer : à citer slide 7.
- **Alexis Blandin** (Jolimoi), « on n'a plus de titres, on prend des responsabilités » : à citer slide 38.

## À vérifier avant le jour J

- **Le titre.** « Et si vos métiers construisaient la data platform ? » est une proposition : aligne-le sur celui du programme officiel.
- **Les chiffres d'Anthropic** (21 %, 95 %, 65 %) : vérifiés le 11 novembre dans l'article d'origine, « How Anthropic enables self-service data analytics with Claude » (3 juin 2026, claude.com/blog/how-anthropic-enables-self-service-data-analytics-with-claude). Formulations exactes : pas plus de 21 % sans skills ; plus de 95 % avec ; une dérive d'environ 95 % à environ 65 % en un mois.
- **La phrase du village** (slide 3) est une traduction, attribuée « d'après Olga Berezovsky, *Data Analysis Journal* ». Vérifiée le 11 novembre : n° 329, « Self-Service Analytics Is Not Self-Service. But Don't Tell Anyone » (19 août 2026, dataanalysis.substack.com/p/self-service-analytics-is-not). L'original : « you need a village of analysts to make self-service work and keep it going ».
- **Le nombre de magasins** n'apparaît plus nulle part, ni à l'écran ni dans le script. Attention à ne pas le citer à l'oral.
- **Les 25 contributeurs.** Le graphique de la slide 18 montre 4 + 4 + 17.
- **« Dix fois mieux »** (slide 11) est ta formule, pas une mesure.
- **Les exemples internes** (géomarketing, liasses fiscales, logistique et SAP, référentiel magasins) : vérifie qu'Optic 2000 est d'accord pour qu'ils soient cités.
