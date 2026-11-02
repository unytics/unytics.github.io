---
title: "Independence at Optic 2000: Zero Proprietary BI, Interchangeable Infrastructure and AI of Your Choice"
description: "Changing cloud, BI or AI model without rebuilding everything: how we decoupled Optic 2000's data platform from its vendors, keeping all business logic in a single repository."
date: 2026-11-02
---

# Independence at Optic 2000: Zero Proprietary BI, Interchangeable Infrastructure and AI of Your Choice

**If you wanted to change cloud, BI tool or AI model tomorrow, how much would it cost you?**

For most companies, the answer is a months-long migration: their business logic — sources, metrics, dashboards — is scattered across their vendors' tools.

At **Optic 2000**, where I took over the data platform last January, we rebuilt the platform so that the answer is: not much. Here's how.

---

## Lock-In Has Three Floors

When people talk about vendor dependency, they first think about infrastructure. Yet that's rarely where lock-in is the most expensive.

1. **Infrastructure** — the cloud, the warehouse. That's the floor everyone watches.
2. **BI and metrics** — often the stickiest lock-in. Your metric definitions live in a vendor's proprietary semantic model, and you pay a license for every employee who wants to look at a number. Changing clouds is a project; changing BI tools means rewriting every metric and every dashboard.
3. **AI** — a new floor, and the fastest-moving one. The best model changes every few months. Locking yourself into a single AI solution means missing the next ones.

On every floor, we applied the same rule.

---

## The Principle: Configuration Is an Asset, the Metal Is a Commodity

All of Optic 2000's business logic lives in **a single Git repository**: data sources, transformations, metric definitions, apps, schedules. It is described declaratively, in YAML and code, independently of the technology that runs it.

For example, here is how we declare the needs of a processing function:

```yaml
compute:
  cpu: 256
  memory: 512
  timeout: 300
schedule: "0 6 * * *"
```

This file describes *what* we want. It says nothing about *how*: today it is deployed on AWS; tomorrow it could be deployed elsewhere without being modified.

Vendors only provide the engine. The business logic — what has value and what is expensive to rebuild — stays with us.

```
┌────────────────────────────────────────────────────────┐
│ AI: OpenWebUI, Claude, ChatGPT, Dust, local model      │  ← your choice
├────────────────────────────────────────────────────────┤
│ Usage: Streamlit apps, agents, MCP server              │  ← open
├────────────────────────────────────────────────────────┤
│ Business logic: sources, metrics, transformations      │  ← the asset, in one repo
├────────────────────────────────────────────────────────┤
│ Metal: AWS, S3, Snowflake, DuckDB                      │  ← interchangeable
└────────────────────────────────────────────────────────┘
```

---

## Floor 1 — Interchangeable Infrastructure

We use AWS for compute, S3 for storage and Snowflake for the warehouse. But none of these choices is baked into the business logic.

Take ingestion. Each source is described by a YAML file: its schema and its storage location. Today, this configuration drives Snowpipe, which loads the data into Snowflake. Tomorrow, the same file could drive a simple serverless function writing to DuckDB. **The configuration doesn't change, and neither does the data: only the engine does.**

Changing infrastructure vendors becomes a contained piece of work — rewriting a deployment module — rather than a platform migration.

---

## Floor 2 — Zero Proprietary BI

We switched off the legacy BI tool without replacing it with another one.

Our metrics are defined once, in a **semantic layer** that lives in the repository. Our dashboards are **open-source Streamlit applications** connected to that semantic layer. The result: no more per-seat licenses — giving a store manager access to their KPIs costs nothing extra — and apps that go beyond dashboards. *Dashboards are passive. Data Apps act.*

Our metrics don't depend on the warehouse either. Depending on the query, the semantic layer runs on Snowflake or on DuckDB, which loads a single store's data into memory to answer in milliseconds. Same definitions, two engines: concrete proof that our metrics aren't locked in anywhere.

If every dashboard has to be coded, haven't we just recreated a ticket queue to the data team? No: 25 contributors vibe-code these apps, and many needs are handled directly by AI agents. I tell that story in [Nobody Codes by Hand](https://unytics.io/blog/nobody-codes-by-hand/).

---

## Floor 3 — AI of Your Choice

The semantic layer is exposed through an **MCP server** (Model Context Protocol) — an open protocol that lets any AI assistant query our metrics.

Internally, we use a single interface based on OpenWebUI. Stores can bring their own client — Claude, ChatGPT, Dust. Either way, the AI answers with certified figures, and **each user only sees their own data**.

Above all, **we can change AI client or model at any time** without touching the metrics. When a better model comes out, we can adopt it without waiting for a vendor to integrate it.

---

## Why a Single Repository Changes Everything

Having all the business logic in one place has effects that go beyond reversibility:

* **It belongs to the company.** Versioned, auditable, readable — not scattered across the interfaces of five vendors.
* **One change, one place.** Adding a source, transforming it, deriving a metric and displaying it in an app happens in a single Pull Request, consistent end to end.
* **AI agents see the whole platform.** A coding agent reading the repository understands everything. That's what allowed us to go from 4 to 25 contributors, as I detail in [Nobody Codes by Hand](https://unytics.io/blog/nobody-codes-by-hand/).

---

## What It Brings

* **No per-seat tax:** access to KPIs no longer costs a license per user — no more paying around €50 per person per month.
* **Tomorrow's AI without a migration:** changing AI model or client doesn't touch the metrics.
* **A healthy balance of power with vendors:** when you can leave, you negotiate differently.
* **No big-bang migrations:** each building block can be replaced independently.
* **And speed:** four major projects absorbed in ten months, while the team went from 6 to 4 people.

---

## The Limits

* **Our semantic layer is home-grown.** It's code we maintain. We built it for performance (multiple backends) and for business-specific calculations, and we may revisit that choice as open standards mature.
* **We haven't left a vendor yet.** Running our metrics on two engines shows that the decoupling works, but reversibility is something you prepare for — it's only truly proven when you leave.

---

## Key Takeaways

Being independent doesn't mean doing without vendors. We use AWS, Snowflake and Claude, and we're happy with them. What matters is where your business logic lives: in your repository, as configuration and code — not inside a vendor's tool.

Ask yourself the question about your own platform: if you wanted to change cloud, BI or AI model tomorrow, how long would it take?

---

*Your BI bill keeps growing, your stack locks you in, or you want to put AI on reliable data without tying yourself to a vendor? [Let's talk about it in a 30-minute data chat](https://unytics.io/book-meeting/).*
