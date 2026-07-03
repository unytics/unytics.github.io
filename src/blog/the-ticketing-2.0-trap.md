---
title: "The Ticketing 2.0 Trap: Why the 2026 Data Platform Must Not Separate Curation and Analysis"
description: "The data team prepares, the business analyzes — it sounds idyllic. In reality, it's a golden trap that reproduces the exact organizational flaws we've spent ten years trying to destroy."
date: 2026-07-03
---

# The Ticketing 2.0 Trap: Why the 2026 Data Platform Must Not Separate Curation and Analysis

Yesterday, I had the pleasure of presenting a talk entitled **"Building a Data Platform in 2026: What Changes, What Doesn't"**.

After spending over six years building and scaling the data teams at Nickel, I've spent the last six months getting my hands dirty, rebuilding a complete platform from scratch. This brutal yet reinvigorating return to the field, right in the midst of the AI agent explosion, has given me a unique perspective on where our industry is heading.

If there is one certainty that transcends trends and eras, it's this: **the ultimate goal of a data platform remains strictly the same: to enable self-service within the company to unlock value from data.** The end goal hasn't shifted an inch. However, the tools and the way we design team autonomy are shifting radically.

Today, a very seductive narrative is starting to echo across our ecosystem. An idea that seems almost logical on the surface: *the data team will take care of providing perfectly prepared, cleaned, and certified data (via a semantic layer or datamarts), and the rest of the company will just have to analyze it.*

On paper, it's idyllic. In business reality, **it's a golden trap.** This approach is sub-optimal and risks reproducing the exact same organizational flaws we've been trying to destroy for the past ten years.

Let me explain why, and how we can do much better.

---

## The Illusion of Perfect Data

Don't get me wrong: the rise of *conversational analytics* backed by modern semantic layers (like tools such as Omni) is a true revolution. Being able to query certified data in natural language to instantly understand a drop in revenue in a specific region is a total game-changer for non-technical profiles. It's a fantastic achievement.

But believing that a company's entire analytics scope can—and should—be confined to this ultra-secure perimeter is an illusion, for two fundamental reasons:

1. **Value is hidden in the raw:** A massive chunk of analytical value lies precisely in data that is *not yet* prepared or modeled. Weak signals, disruptive insights, and answers to complex questions almost always stem from exploring raw sources or unprecedented cross-references.
2. **The omission of value:** Restricting business teams solely to data validated by the central team means overlooking the majority of opportunities. It restricts your entire company's scope of possibilities to what your data team was able to anticipate and plan for.

---

## Say No to "Ticketing 2.0"

By trying to "protect" business users by blocking their access to the rest of the platform, we are reinventing a bureaucracy we thought was long gone.

Think back to the old days: business teams created Jira tickets for the data team to build them a dashboard. Self-service was supposed to break this bottleneck. If we adopt this new vision of a data team serving solely as a "curator," we fall straight into **Ticketing 2.0**: business teams will now create tickets to get a new column, a new table, or a join modification in the semantic model.

We are simply moving the problem somewhere else.

> **Siloing the organization into two airtight blocks—those who prepare the data on one side, and those who analyze it on the other—inherently destroys the company's analytical capabilities.**

Why? Because **waiting kills the momentum of intuition.** A significant portion of great business insights are uncovered entirely unexpectedly, at the exact moment you are digging into the data. It's by testing a hypothesis, spotting an anomaly, and instantly pivoting that you discover a flaw or an opportunity.

If a business team has to log a ticket based on a mere hunch, and a technical team handles the preparation three days later on their own, serendipity vanishes. The technical team simply executes the request coldly, without understanding its subtle intent or the business context. The creative flow of analysis is broken.

---

## The Target Architecture in 2026: The Two-Tool Model

To overcome this roadblock, we must rethink the platform not around data access rights, but around the users' **technical background**. In 2026, a modern, high-performing architecture is structured around two clear pillars:

### 1. Conversational Analytics (For business users without a technical background)

For employees with no appetite for coding, chat tools built on top of a semantic layer are perfect. They query trusted data with total autonomy. In this paradigm, dashboards don't disappear, but their role evolves: they are no longer static deliverables, but results generated and iterated on the fly through conversation. They remain essential for tracking recurring KPIs, but their maintenance drops to zero.

### 2. The "Shift Left" in a Mono-repo (For anyone with a technical background)

This is where the true breakthrough of 2026 lies. Instead of confining semi-technical profiles to restricted visualization tools, we need to bring them on board the data platform's Git mono-repo.

Why is this possible today when it was a pipe dream yesterday? Thanks to development agents like **Claude Code**. The barrier to entry for engineering (understanding Git, dbt, complex file architectures) has collapsed.

Anyone with a basic technical background can now conduct their analysis directly where the curation happens.

Let's look back at my experience at Nickel: the 150 business users who used to write SQL on their own every month to run their analyses could today work directly in the mono-repo. Guided by an AI agent, they run their explorations and, in doing so, modify and enrich the underlying dbt models on the fly.

This is exactly the collaborative approach we are experimenting with alongside Yoann Boudon (CDO of Optic 2000): it is now possible to iterate with Claude Code on a Streamlit application for a business need and, through this simple act of exploration, modify and push two dbt models into production. **Analysis self-builds the platform.**

---

## Conclusion: Merging Engineering and Analysis

Let's not let old centralizing habits dictate how we organize our modern platforms. Isolating engineering in an ivory tower of curation and restricting analysis to a pre-packaged data catalog is a sub-optimal model. It breeds frustration, spawns *Shadow Data*, and misses out on raw value.

In 2026, technology finally offers us the opportunity to reconcile these two worlds. Let's empower technical and semi-technical profiles to enrich the platform at the exact moment they explore it. This is where true self-service lies, and this is how you build an authentically *data-driven* organization.

---

*This return to the field is a continuation of my global rebuilding process. If you want to understand why I chose to leave managing massive teams to return to this agile model, you can read my article [Why I Left Managing 100+ Engineers to Build From Scratch Again](https://unytics.io/blog/why-i-left-managing-100-engineers/). And to take a closer look at how tools like Claude Code are concretely transforming day-to-day analysis, discover my full exploration in [Why Claude Code in VSCode is a Game Changer for Data Analysis](https://unytics.io/blog/best-tool-for-deep-dive-analyses/).*