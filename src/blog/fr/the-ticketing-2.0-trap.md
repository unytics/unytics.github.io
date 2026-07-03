
# Le piège du Ticketing 2.0 : Pourquoi la data platform de 2026 ne doit pas séparer curation et analyse

Hier, j'ai eu le plaisir de présenter une conférence intitulée **"Bâtir une plateforme Data en 2026. Ce qui change, ce qui ne change pas"**.

Après avoir passé plus de six ans à construire et faire passer à l'échelle les équipes data de Nickel, j'ai passé ces six derniers mois les mains dans le cambouis, à reconstruire une plateforme complète en partant d'une page blanche. Ce retour brutal et salvateur sur le terrain, en pleine explosion des agents d'IA, m'a donné un prisme unique pour observer la direction que prend notre industrie.

S'il y a une certitude qui traverse les modes et les époques, c'est celle-ci : **le but ultime d'une data platform reste strictement le même : permettre le self-service en entreprise pour libérer de la valeur.** La finalité n'a pas bougé d'un iota. En revanche, les outils et la manière dont nous concevons l'autonomie des équipes sont en train de basculer radicalement.

Aujourd'hui, une "petite musique" très séduisante commence à se faire entendre dans notre écosystème. Une idée presque logique en apparence : *l'équipe data va s'occuper de fournir des données parfaitement préparées, nettoyées et certifiées (via une couche sémantique ou des datamarts), et le reste de l'entreprise n'aura plus qu'à les analyser.*

Sur le papier, c'est idyllique. Dans la réalité du business, **c'est un piège doré.** Cette approche est sous-optimale et risque de reproduire exactement les pires travers organisationnels que nous essayons de détruire depuis dix ans.

Laissez-moi vous expliquer pourquoi, et comment nous pouvons faire beaucoup mieux.

---

## L'illusion de la donnée parfaite

Ne vous méprenez pas : l'essor du *conversational analytics* adossé à des couches sémantiques modernes (à l'image d'outils comme Omni) est une véritable révolution. Pouvoir interroger ses données certifiées en langage naturel pour comprendre instantanément la baisse du chiffre d'affaires d'une région change radicalement la donne pour les profils non techniques. C'est un acquis formidable.

Mais croire que l'intégralité de l'analyse d'une entreprise peut — et doit — se cantonner à ce périmètre ultra-sécurisé relève de l'illusion, pour deux raisons fondamentales :

1. **La valeur se cache dans le brut :** Une part gigantesque de la valeur analytique se trouve précisément dans les données qui ne sont *pas encore* préparées ou modélisées. Les signaux faibles, les insights disruptifs et les réponses aux questions complexes naissent presque toujours de l'exploration de sources brutes ou de croisements inédits.
2. **L'omission de la valeur :** Limiter les métiers aux seules données validées par l'équipe centrale revient à occulter la majorité des opportunités. C'est restreindre le champ des possibles de toute votre entreprise à ce que votre équipe data a été capable d'anticiper et de planifier.

---

## Non au "Ticketing 2.0"

En voulant "protéger" les utilisateurs métiers en leur bloquant l'accès au reste de la plateforme, on réinvente une bureaucratie que l'on pensait disparue.

Souvenez-vous de l'ancienne époque : les équipes métiers créaient des tickets Jira pour que l'équipe data leur conçoive un dashboard. Le self-service était censé briser ce goulot d'étranglement. Si nous adoptons cette nouvelle vision d'une équipe data uniquement "curatrice", nous tombons tout droit dans le **Ticketing 2.0** : les métiers créeront désormais des tickets pour obtenir une nouvelle colonne, une nouvelle table ou une modification de jointure dans le modèle sémantique.

On déplace simplement le problème.

> **Cloisonner l'organisation en deux blocs hermétiques — d'un côté ceux qui préparent la donnée, de l'autre ceux qui l'analysent — détruit intrinsèquement les capacités d'analyse de l'entreprise.**

Pourquoi ? Parce que **l'attente tue le momentum de l'intuition.** Une part significative des grands insights business sont obtenus de façon totalement inattendue, au moment précis où l'on triture la donnée. C'est en testant une hypothèse, en observant une anomalie et en bifurquant instantanément qu'on découvre la faille ou l'opportunité.

Si une équipe métier doit émettre un ticket basé sur une simple intuition, et qu'une équipe technique réalise la préparation trois jours plus tard dans son coin, la sérendipité disparaît. L'équipe technique se contente d'exécuter froidement la demande formulée, sans en comprendre l'intention fine ni le contexte business. Le flux créatif de l'analyse est rompu.

---

## L'architecture cible en 2026 : Le modèle à deux outils

Pour dépasser ce blocage, nous devons repenser la plateforme non pas autour des droits d'accès à la donnée, mais autour du **vernis technique** des utilisateurs. En 2026, une architecture moderne et performante s'articule autour de deux piliers clairs :

### 1. Le Conversational Analytics (Pour le business sans vernis technique)

Pour les collaborateurs qui n'ont pas d'appétence pour le code, les outils de chat sur couche sémantique sont parfaits. Ils requêtent la donnée fiabilisée en toute autonomie. Dans ce paradigme, les dashboards ne disparaissent pas, mais leur rôle évolue : ils ne sont plus des livrables figés, mais des résultats générés et itérés à la volée via la conversation. Ils restent indispensables pour piloter les KPIs récurrents, mais leur maintenance devient nulle.

### 2. Le "Shift Left" en Mono-repo (Pour tous ceux qui ont un vernis technique)

C'est ici que réside la véritable rupture de 2026. Plutôt que de cantonner les profils semi-techniques à des outils de visualisation bridés, nous devons les faire monter à bord du mono-repo Git de la data platform.

Pourquoi est-ce possible aujourd'hui alors que c'était une utopie hier ? Grâce aux agents de développement comme **Claude Code**. La barrière à l'entrée de l'ingénierie (comprendre Git, dbt, les architectures de fichiers complexes) s'est effondrée.

Toute personne disposant d'un vernis technique peut désormais mener ses analyses directement là où la curation s'opère.

Reprenons l'exemple de mon expérience chez Nickel : les 150 personnes métiers qui écrivaient chaque mois du SQL dans leur coin pour faire leurs analyses pourraient aujourd'hui travailler directement dans le mono-repo. Guidées par un agent d'IA, elles mènent leurs explorations et, ce faisant, modifient et enrichissent les modèles dbt sous-jacents au fil de l'eau.

C'est exactement la démarche collaborative que nous expérimentons avec Yoann Boudon (CDO d'Optic 2000) : il est désormais possible d'itérer avec Claude Code sur une application Streamlit pour un besoin business et, par ce simple geste d'exploration, de modifier et de pousser en production deux modèles dbt. **L'analyse auto-construit la plateforme.**

---

## Conclusion : Fusionner l'ingénierie et l'analyse

Ne laissons pas les vieux réflexes centralisateurs dicter l'organisation de nos plateformes modernes. Isoler l'ingénierie dans une tour d'ivoire de curation et brider l'analyse à un catalogue de données pré-mâchées est un modèle sous-optimal. Il génère de la frustration, crée de la *Shadow Data* et passe à côté de la valeur brute.

En 2026, la technologie nous offre enfin l'opportunité de réconcilier ces deux mondes. Donnons aux profils techniques et semi-techniques les moyens d'enrichir la plateforme au moment même où ils l'explorent. C'est là que réside le véritable self-service, et c'est ainsi que l'on crée une organisation authentiquement *data-driven*.

---

*Ce retour sur le terrain s'inscrit dans la continuité de ma démarche de reconstruction globale. Si vous voulez comprendre pourquoi j'ai choisi de quitter le management d'équipes massives pour revenir à ce modèle agile, vous pouvez lire mon article [Why I Left Managing 100+ Engineers to Build From Scratch Again](https://unytics.io/blog/why-i-left-managing-100-engineers/). Et pour voir de plus près comment des outils comme Claude Code transforment concrètement le quotidien de l'analyse, découvrez mon exploration complète dans [Why Claude Code in VSCode is a Game Changer for Data Analysis](https://unytics.io/blog/best-tool-for-deep-dive-analyses/).*

