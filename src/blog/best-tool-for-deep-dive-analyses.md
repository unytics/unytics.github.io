---
title: "Why Claude Code in VSCode is a Game Changer for Data Analysis"
description: "Claude Code in VSCode is the best tool for deep-dive data analysis — ending shadow data, shifting left, and building the platform as you explore."
date: 2026-04-17
---

# Why Claude Code in VSCode is a Game Changer for Data Analysis

In my last post, I wrote about [why I left managing 100 engineers](/blog/why-i-left-managing-100-engineers/). Diving back into the trenches gives you a fresh perspective on the friction points that slow teams down.

As of today, I've come to a definitive conclusion: **Claude Code in VSCode is the absolute best place to perform data analysis.** It’s not just a marginal improvement; it’s a complete game-changer.

To understand why, we first need to look at the current state of modern data tools.

---

## The Baseline: The Semantic Layer is Awesome, But...

There is a prevailing belief right now that conversational analytics on top of a semantic layer is the ultimate holy grail. And for sure, it is absolutely awesome. Placing a chat agent — like Omni or Snowflake Intelligence — on top of your marts not only enables stakeholders to safely pull any figure or chart from curated data, but it also allows them to execute advanced analyses: root cause analysis, churn analysis, customer segmentation, or Lifetime Value (LTV) calculations.

**But it does not answer every use case.** This approach *only* works on very curated data. If a data point, an intermediate table, or a specific dimension isn't already meticulously modeled and exposed in that semantic layer, it is completely invisible to the agent. 

When you hit this "curation wall," you are left with two major analytical challenges that a standard chat agent simply cannot solve.

---

## 1. Exploring Physical Data in the Lineage

To truly understand your data, a robust **data catalog** is the way to go. It’s where you explore the data, navigate the lineage, check data previews, look at profiling stats, and read the documentation. Because the catalog is the natural place for exploration, adding a **Natural Language Q&A** feature makes perfect sense:

* **Contextual Learning:** When you are looking at a specific table’s lineage or schema, you should be able to ask questions about it right then and there.
* **Knowledge Compounding:** The answers to these questions shouldn't disappear. By persisting Q&A results directly on the documentation page, you enrich the catalog for everyone. The next person with the same question finds the answer already waiting for them.

**How we do this at Optic 2000:**
We built a custom data portal directly on top of our Git repository to serve this purpose. By embedding Q&A into this portal, we've turned technical documentation into a living business resource where knowledge persists and grows.

---

## 2. The Deep Dive: Breaking the Shadow Data Cycle

The second major challenge is the deep dive. This is where the paradigm truly shifts and where Claude Code entirely rewrites the rules. To understand why deep dives are so painful, you have to acknowledge the industry's biggest open secret. As Yoann Boudon, CDO of Optic 2000, says:

> "A data analyst usually spends 80% of their time getting the data, and 20% doing the analysis — and this is the best-case scenario."

**When you are analyzing an unknown topic, the semantic layer is <u>NOT</u> going to help you.**

In a traditional setup, a deep dive is a stop-and-go process. You start an analysis, realize you're missing a column or need a new raw source, switch tools, and write a pipeline — effectively killing your momentum.

### The Way We Used to Work (And Why It Sucked)
Traditionally, Analysts and Data Engineers lived in two different worlds. When an analyst needed new data for a deep dive, they faced a frustrating choice:

1. **The Ticket Trap:** Open a ticket for the Data Engineer to add the column or source to dbt. Because the analyst needs answers *now*, waiting days for a sprint cycle isn't viable.
2. **The Shadow Path:** The analyst takes a shortcut. They pull raw data into a local CSV, a separate notebook, or a "sandbox" schema. They redo work that’s already been done elsewhere, creating **Shadow Data Transforms**.

This "Shadow Path" is a disaster for the company. The logic used in that deep dive is never merged back into the global knowledge base.

Even in companies like Nickel where data analysts are responsible for the transforms, switching tools — using dbt for the pipe and a different tool for exploration — creates a mental and technical gap that leads to the same redundant, isolated work.

### The "Shift Left" Revolution
Claude Code in VSCode breaks this cycle. It allows the analyst to **"Shift Left"** — moving directly into the repository where the curation happens.

Because Claude has full visibility of your raw sources and your dbt transforms, it eliminates that 80% of data retrieval friction. Instead of jumping between tools, you handle everything in a **<u>single conversation</u>**:

* **Piping Data on the Fly:** Claude can spot interesting columns in raw sources and pipe them up to your marts — following your exact coding conventions — before using them in the analysis.
* **Ending Shadow Logic:** Since the work happens inside the repo, the transformation logic is committed, tested, and documented. The "deep dive" doesn't just produce a slide; it produces a **permanent improvement to your data platform**.
* **Code Correction:** It reads your repository, identifies mistakes in your logic, and corrects them mid-stream. It understands your business rules and proposes new ones to solve the problem.

---

## The Workflow Revolution: Building "Skills"

Every time we perform an analysis in VSCode, we are actually building and refining a **Claude Skill**. This is a specialized meta-prompt that ensures every analysis follows a high-standard blueprint:

* **Objective-First & Impactful Summaries:** Starting with a goal and leading with the results for executives.
* **Persistent Documentation:** The skill automatically updates the data documentation with findings that need to stay in the repo for the long term.
* **Technical Depth:** Every SQL query is included for auditability but tucked away in collapsed sections (admonitions).

### From Repo to Boardroom
Because these analyses are written as Markdown files inside the Git repository, they are automatically surfaced in our **Data Portal**. Executives get high-fidelity, homogenous reports that are always linked to the code.

We aren't just changing the tools we use; we are ending the era of siloed "Shadow Data" and **<u>we are empowering analysts to build the platform as they explore it</u>**.