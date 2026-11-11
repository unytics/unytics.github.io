---
title: "A Dashboard Shows, a Data App Acts: What Our Business Teams Build on the Data Platform"
description: "At Optic 2000, we thought Streamlit would be used to display charts. Business teams turned it into something else: tools that replace SaaS products, front-ends on top of SAP and Salesforce, embedded agents. What these data apps do, what they read and what they write, and what keeps them consistent."
date: 2026-11-12
---

# A Dashboard Shows, a Data App Acts: What Our Business Teams Build on the Data Platform

In [Nobody Codes by Hand](https://unytics.io/blog/nobody-codes-by-hand/), I told how 25 people, most of them business people, now contribute to Optic 2000's data platform without writing a line of code.

At first, we thought they would build dashboards: charts on top of Snowflake. They built something else. Tools that replace software we used to pay for. Interfaces on top of SAP and Salesforce. Data apps that embed a conversational agent. It's the use we least imagined, and maybe the one that will change the game the most.

This article describes what these *data apps* are, what exactly they do — what they read, and what they write — and what keeps them from turning into a patchwork.

---

## Why Data Apps Rather Than a BI Tool

Our data apps are written in Python, with Streamlit, in the data platform's repository. That choice wasn't obvious: when it left its legacy BI tool, Optic 2000 had first picked Tableau. Three reasons made us change.

* **The time spent.** Our BI team spent a phenomenal amount of time on repetitive, tedious point-and-click tasks. By *vibe-coding* its dashboards with an agent, it gets a far better experience for the end user, in a fraction of the time.
* **A product, not an internal tool.** Our users are first and foremost thousands of people in stores, opticians and store managers. A store has to be served like a customer: we owe it a finished product, not access to an analysis tool.
* **No per-seat license.** Giving a store manager their indicators costs nothing extra, as I explained in [my article on independence](https://unytics.io/blog/optic-2000-independence/).

A fourth reason became clear later: a data app is code, in the same repository as the data it displays. So an agent can build it, and change it in the same Pull Request as the dbt model or the metric it needs.

---

## What Business Teams Built

### Tools that replace SaaS products

* **Geomarketing.** We paid for a rather rigid proprietary tool to visualize catchment and franchise areas on the map of France. The person in charge rebuilt the whole tool. It finally meets all of her needs, and we drop a costly license.
* **The stores' tax returns.** They had to be re-entered by hand every year, or we had to pay a lot for OCR software. A data app now reads them automatically, and a human validates. With the same quality.

### Front-ends for our back-ends

We have no desire to replace SAP or Salesforce: they are robust, standard back-ends. But their interfaces are unfriendly. Optic 2000 was founded in 1969, and many processes still rely on an Excel export, followed by hours of repetitive manipulation, with a real risk of error.

So business people build front-ends tailored to their processes:

* **tracking of the logistics teams**, built by a business project manager from SAP data;
* **the store master data cockpit**, built by its owner to spot inconsistencies in Salesforce, such as two opening dates that overlap when a store is taken over;
* **store master data enrichment**, where an algorithm helps complete a store's record.

We are only at the beginning, and the coming months are about turning the attempt into a success.

### Data apps that embed specialized agents

* **A store's financial statement.** The manager looks at the statement and talks it through with an agent specialized in optical retail finance, whose *system prompt* is written for that topic. They compare themselves with similar stores, bring in their local context, and get recommendations.
* **A playground.** Users generate their own analyses and dashboards there, by conversing, then save them. The data app now hosts dozens of them, created by users themselves: durable, discoverable, shareable, and all in one place.
* **Alert scheduling.** Users configure and schedule automatic alerts, driven by the indicators of the semantic layer.

The same expertise is also exposed through an MCP server and skills: stores can query their data from their own Claude or their own ChatGPT. In every case, the figures come from the same semantic layer, and everyone sees only their own data.

### Tools for the platform itself

The platform is also used to equip itself:

* **a Pull Request tracking cockpit**, on top of Bitbucket: who has to review what, and which requirements are still unmet;
* **a visual editor for the semantic layer**, easier to digest than raw YAML;
* **an access rights manager**, from which a handful of managers decide who can open which data app.

---

## "Acting": What Data Apps Read, and What They Write

"A data app acts" doesn't mean every data app writes to the company's systems. Here is where we stand, system by system.

* **In SAP, data apps read.** They don't write to it yet. That's the next step, and it will need guardrails to match: tests, permissions, human validation.
* **In Salesforce, the platform writes, not the data app.** The enrichment data app doesn't push anything to Salesforce itself. A platform function, scheduled every day, carries an enrichment over when it isn't there yet. A dbt post-hook writes to Salesforce as well. In both cases, the write goes through versioned code, reviewed in a Pull Request, not through a button in an interface.
* **In the platform itself, data apps already act.** Validating the reading of a tax return, scheduling an alert, saving a dashboard, granting access: these are working steps, not numbers to read.

That's the meaning of the phrase: a dashboard gives you a number to read; a data app takes on a piece of a process.

---

## What Prevents the Patchwork

Data apps written by different people, with agents: left unchecked, each would have its own style, its own figures and its own permissions. Four things prevent that.

* **Shared components.** The BI team built a library of components itself — KPI cards, tables, charts — and our skills require the agent to use them. Data apps written by different people look like one product.
* **Figures defined elsewhere.** Store-facing data apps rely 100% on the semantic layer: a measure's logic is defined in one place, and the data app just calls and displays it. The same figures everywhere, and an AI that invents nothing.
* **Security the data app doesn't write.** Authentication is required before a request reaches the data app, each user's perimeter is applied by the semantic layer, and access is decided outside the repository. A contributor can't forget a check: there isn't one to write.
* **A review before the Pull Request.** Before a Pull Request is even opened, a review agent checks that the data app follows these rules, and flags any duplicate of an existing data app.

I detail these mechanisms in [Boringly Simple](https://unytics.io/blog/boringly-simple-data-platform/), and review in [The Platform That Learns](https://unytics.io/blog/the-platform-that-learns/). The AI doesn't design each data app: it assembles building blocks.

---

## Artifacts or Data Apps in Git: Where to Draw the Line?

An artifact is a small application — a dashboard, an interactive table, an HTML page — that an AI assistant generates right in the conversation, from a simple request. Claude, ChatGPT and most conversational analytics tools now produce them, and the practice is spreading fast among business teams: no need to wait for a data team to get your own screen.

These artifacts are improving fast: they can be kept, shared, and will tomorrow connect to the company's systems. Will we still need business people to vibe-code data apps in a repository?

We see a continuum rather than an alternative.

* **For exploratory, lightweight needs**, an artifact is enough, and unbeatable in speed. That's the role of our playground, which also gives those artifacts a place to live: a dashboard born in a private conversation exists for nobody else.
* **For anything that touches critical processes** — what has to be tested, governed, deployed on the company's infrastructure, and all the more so what will one day write to SAP — we want code versioned in Git and approved through a Pull Request.

---

## Key Takeaways

We thought we were giving business teams a dashboarding tool. They turned it into a workshop: they replace software there, dress up SAP and Salesforce, and install agents. A central data team wouldn't have had those ideas, because it doesn't live those processes.

It only holds because data apps rest on the same foundation as the rest of the platform: a single repository, shared components, figures defined once, and writes that go through reviewed code.

Ask yourself the question about your own company: **how many of your processes still run on an Excel export?** Each one is a data app waiting for its author.

*This article details one part of a larger story: [Why Your Business Teams Shouldn't Just Be AI Consumers (But Builders Too)](https://unytics.io/blog/self-service-analytics-builders/).*

---

*Are your business teams juggling an ERP, a CRM and Excel files? [Let's talk about it in a 30-minute data chat](https://unytics.io/book-meeting/).*
