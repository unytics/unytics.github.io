---
title: "Self-Service Analytics: Why Your Business Teams Shouldn't Just Be AI Consumers (But Builders Too)"
description: "Everyone wants conversational AI to consume data. At Optic 2000, we also put it at the start of the chain, in the code editor: 25 contributors, most of them business people, build the data platform. The full story, with links to the articles that detail each part."
date: 2026-11-16
---

# Self-Service Analytics: Why Your Business Teams Shouldn't Just Be AI Consumers (But Builders Too)

*This article follows the thread of my talk at the Forward Data Conference 2026, "What if your business teams built the data platform?" ([the slides are here](https://unytics.io/blog/forward-data-conference-2026/)). It is the whole story, in its short version: each part points to the article that details it.*

Every executive team and every business department is asking for the same thing today: conversational analytics. An interface where any employee asks a question of their data, in natural language, and instantly gets a relevant analysis.

At Optic 2000, we do that too. But it's not where we started. We first put conversational AI at the other end of the chain: in the code editor, where the platform is built. Ten months later, 25 people contribute to our data platform, and most of them aren't on a data team: **they are business people.**

---

## The Paradox: An AI Only Answers Right If Someone Maintains Its Context

Data teams know what's under the hood. Anthropic's data team [told the story very well in June](https://claude.com/blog/how-anthropic-enables-self-service-data-analytics-with-claude):

* without prepared context, Claude gets no more than **21%** of answers right on their warehouse;
* with a senior team curating that context — reference tables, a semantic layer, skills, tests — it goes above **95%**;
* within a month, without maintenance, it falls back to **65%**.

Context isn't prepared once: it has to be maintained. Olga Berezovsky drew the conclusion in her [*Data Analysis Journal*](https://dataanalysis.substack.com/p/self-service-analytics-is-not): you need a village of analysts to make self-service work and keep it going.

Here is what that looks like in practice. A business user is in the middle of an analysis, and a piece of data is missing: a column, a table, a measure. They have two options.

1. **Hack it on their own**, with an export and an Excel file. That's *shadow data*: what they learned never makes it back into the platform.
2. **Open a ticket**, and wait for the data team to prepare the data. We used to open a ticket to get a dashboard; now we open one to get a column in the semantic layer. That's [Ticketing 2.0](https://unytics.io/blog/the-ticketing-2-0-trap/).

The most advanced teams shorten that wait: they analyze the questions that went unanswered, and enrich the context before anyone asks. It works remarkably well, and we are putting it in place too, for those who consume. But the data team remains the only one that builds — and therefore the bottleneck for everything that gets built.

---

## Going Against the Market: Conversational AI at the Start of the Chain

At Optic 2000, we had an extra problem this year: everything was changing at once. In ten months, we replaced the legacy PostgreSQL stack, absorbed a new point of sale, a new CRM and a new loyalty program, and switched off our BI tool. All with a platform team that went from six to four people. Our BI team didn't have a minute to take on new business topics.

Faced with that wall, we went against the market. A classic data platform chains sources, transformations, a semantic layer and applications. The data team prepares, business teams consume, and the market plugs conversational AI at the very end of the chain, in a consumption interface.

```
Sources → Transformations → Semantic layer → Applications
                                                  ▲
                       the market: conversational AI here

├─ Optic 2000: conversational AI along the whole chain ─┤
```

We put it at the very start: in the code editor, where the platform is built. The moment someone starts an analysis, the AI helps them prepare and enrich the data, at the source, in the platform. That's the third option: neither hacking nor waiting. Building.

**Analysis builds the platform.** An example. We were analyzing the performance of some of our stores, and we wanted to compare them with one another. But you can't compare apples and oranges: we first needed segments. We built them within the same analysis, with a k-means on each store's sales profile: high-end, mid-range or entry-level, volumes, products for seniors or for children… The analysis answered the question we had asked: how those stores perform, how that evolves over time, and where they stand against similar stores. And it left two things behind in the platform: a "segment" dimension in `dim_magasins`, our store dimension model, and a feature table — sales statistics per store — that other analyses and machine-learning algorithms can reuse.

In a separate analysis tool, that segmentation would have stayed in a notebook. Here, everyone builds on the shoulders of those who came before.

---

## What Happened: The BI Team First, Then Business Teams

Opening the central repository to non-developers didn't happen overnight. We started with the people closest to us: our BI team, who had never touched Git or dbt. Within a few weeks, they were building their data apps on their own, then their models. Business teams at headquarters followed, first on small topics, then on critical ones.

The result: in ten months, the number of people contributing to our data repository went from **4 to 25**. Four on the platform team, four in BI, and all the others are business people. None of these twenty-five people codes by hand: they converse with an agent.

The village of analysts you supposedly need to make self-service work? Here it is. Except we didn't hire it: **it was already in the company.**

*The details — the BI team's story, the business teams' stories, how we onboard people, and what happens when a contributor leaves — are in [Nobody Codes by Hand](https://unytics.io/blog/nobody-codes-by-hand/).*

---

## What They Build: Much More Than Dashboards

Multiplying contributors doesn't just save time: it brings out ideas the data team would never have had. We expected dashboards. Business people did something else: they replaced licensed software, and gave SAP and Salesforce the interfaces they were missing.

*The details — what they built, what these data apps read and write, and what keeps them consistent — are in [A Dashboard Shows, a Data App Acts](https://unytics.io/blog/data-apps-beyond-dashboards/).*

---

## Why It Holds Without Turning into Chaos

The objection is fair, and I raised it myself: letting twenty-five people and their agents change the data platform will create a plate of spaghetti, and we'll spend more time reviewing their code than writing it ourselves. Five things prevent that, and each has its own article.

* **A single repository.** Ingestion, transformations, the semantic layer and data apps live in the same Git repository: an agent goes from the source to the screen in the same conversation and the same Pull Request, which none could do with scattered tools. It is also what makes us [independent from our vendors](https://unytics.io/blog/optic-2000-independence/).
* **Boring contributions.** A contributor only writes configuration; deployment, security and monitoring are written once, by the platform team. What a contribution can't express, a reviewer doesn't have to check. That's the subject of [Boringly Simple](https://unytics.io/blog/boringly-simple-data-platform/).
* **One name per concept.** A column has the same name across the whole warehouse, and its definition is written only once: the agent has nothing to guess. That's the subject of [One Name, One Definition](https://unytics.io/blog/one-name-one-definition/).
* **A review done by the machine first.** A review agent reads the work before the Pull Request is opened, and every review comment becomes a rule. Otherwise, we would only have moved the bottleneck, from tickets to Pull Requests. That's the subject of [The Platform That Learns](https://unytics.io/blog/the-platform-that-learns/).
* **People who are supported.** The key isn't technology, it's people: one of our four data engineers is dedicated full time to supporting business people. That's in [Nobody Codes by Hand](https://unytics.io/blog/nobody-codes-by-hand/).

---

## Builders and Consumers: We Do Both

Does all this mean throwing away conversational analytics and putting everyone in VS Code? Absolutely not. At headquarters, analytical profiles use AI to build lasting assets, in the repository. But an optician in one of our stores will never open a code editor: they need to be served like a customer.

For stores, AI comes in two forms:

* **specialized agents, embedded in their data apps.** A store manager looks at the store's financial statement and talks it through with an agent that is an expert in optical retail finance: they compare themselves with similar stores, bring in their local context, and get recommendations;
* **an MCP server and skills**, which expose the same expertise: stores query their data from their own Claude or their own ChatGPT.

In both cases, the figures come from the same semantic layer, and everyone sees only their own data.

A data organization has three roles: those who build the platform (*platformers*), those who build on top of it (*builders*) and those who consume (*consumers*). In the usual model, the boundary runs between the data team, which builds, and business teams, which consume. We moved it.

| | Platformers | Builders | Consumers |
|---|---|---|---|
| **The usual model** | the data team | the data team | business teams |
| **At Optic 2000** | the platform team | business teams at headquarters, with the BI team | the stores |

Among those who build, there are now more business people than data people. Our conviction: put as many people as possible on the builders' side. With eight of us in data, we will never know every accounting subtlety of SAP, or every business rule of the store master data. **Business teams are the ones who know their data and their processes.**

---

## A Trend Bigger Than Our Case

I don't think this way of working is specific to a company like ours. I have the impression a trend is setting in: business people who have never coded are starting to work in code repositories, in three forms:

* they open a ticket from Slack, and an agent codes it;
* they build directly in another team's repository, as ours do;
* they create their own repository.

It's especially visible in marketing and go-to-market teams, to manage their campaigns. And digital-native companies are concerned too. One of them actually inspired me: Taha Le Bras, at Supabase, told me that one morning marketing had made a Pull Request in his data repository, and that he himself, the same day, had made one in the product's.

It may be the beginning of a "git-ification" of the company. What changes from one case to another is what gets built: in ours, the transformation of processes that are still manual. And nothing forces you to bring everything into a single repository from the start: you can open the dbt repository first, then bring the rest into it.

---

## Key Takeaways

People say you need a whole village of analysts to make self-service work. I believe that village already exists, in every company: **it's your business teams.**

Keep conversational AI for those who consume. But don't leave the data team with a monopoly on building. Ours no longer builds simple dashboards: freed from ticketing and point-and-click, our BI team helps business teams rethink the way they work, and the data team as a whole co-builds the operational transformation of the company.

Ask yourself the question about your own company: **who could become a builder tomorrow?**

---

*Want to open your data platform to your business teams, and wondering where to start? [Let's talk about it in a 30-minute data chat](https://unytics.io/book-meeting/).*
