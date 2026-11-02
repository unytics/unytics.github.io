---
title: "Nobody Codes by Hand: How We Went from 4 to 25 Contributors on Our Data Platform"
description: "At Optic 2000, nobody writes code by hand: 25 contributors vibe-code apps and pipelines in the repository, and everyone else talks to the data directly through AI agents. The key isn't the model: it's a repository where there is only one way to do things."
date: 2026-11-03
---

# Nobody Codes by Hand: How We Went from 4 to 25 Contributors on Our Data Platform

In [a previous article](https://unytics.io/blog/optic-2000-independence/), I described the architecture we built at Optic 2000. In ten months, we replaced a legacy PostgreSQL platform, absorbed a new POS, CRM and loyalty program, and retired our BI tool.

The most striking number of that project isn't technical. Over the same period, the data platform team went from 6 to 4 people, while the number of people contributing to the data repository went from **4 to 25**.

And none of them writes code by hand.

---

## A Small Team Can't Be the Bottleneck

With four simultaneous migrations, a small team that has to handle every business request becomes a bottleneck within weeks. That's the [Ticketing 2.0 trap](https://unytics.io/blog/the-ticketing-2-0-trap/): the data team prepares, the business waits.

There were two ways out: hire, or let others contribute. We chose the second. But for 25 people — most of them not engineers — to contribute safely, the repository has to be designed for it.

---

## The Golden Rule: One Way to Do Things

The whole platform lives in a **single Git monorepo**, governed by one rule: *there is one and only one way to accomplish each task, and everything goes through declarative configuration (YAML).*

* **One way to declare a source:** a YAML file describing the schema and the storage path.
* **One way to create a function:** a Python file with an in-house decorator, plus a YAML file declaring its compute needs and schedule.
* **One convention for dbt models**, from staging to marts.
* **One way to consume metrics:** through the semantic layer, whether from Streamlit or from the MCP server.

For example, here is everything needed to deploy a function:

```yaml
compute:
  cpu: 256
  memory: 512
  timeout: 300
schedule: "0 6 * * *"
```

Terraform reads this YAML and deploys the job to AWS Lambda or ECS Fargate. Nobody touches the AWS console, writes Terraform, or manages infrastructure.

---

## Why Standardization Is What Makes Coding Agents Reliable

As I explained in [Why Claude Code in VSCode is a Game Changer for Data Analysis](https://unytics.io/blog/best-tool-for-deep-dive-analyses/), a coding agent's effectiveness depends less on the raw intelligence of the LLM than on the project's context and constraints.

In a repository where each pipeline is written differently, an AI agent has to guess: it invents patterns, mixes conventions and breaks the CI.

In a repository where there's only one way to do each thing, the agent just has to copy the right pattern. Standardization used to be a matter of hygiene; with coding agents, it becomes the condition for them to work well.

---

## Two Ways In: Build or Consume

### 1. Build: vibe-coding in the repository

A contributor opens the repository with Claude Code and describes what they need. In a few prompts, the agent can connect a new source, write the YAML, create the dbt models, build a Streamlit app or set up a data activation.

They don't need to read or understand the code. The conventions and the review take care of that.

### 2. Consume: talking directly to the data

For most users, there's an even simpler path: no repository, no code editor, no Git. They consume data directly through AI agents built on the semantic layer.

* **OpenWebUI**, our single internal AI interface, connected to the semantic layer through our MCP server — where each user only sees their own data. Stores can also bring their own AI client (Claude, ChatGPT, Dust…), and we can change client or model at any time.
* **Agents embedded in our Streamlit apps:** a playground that generates analyses and HTML dashboards users can save and share, an app to configure and schedule Teams notifications, and business dashboards with a conversational part whose system prompt is specialized on the topic.

This second path is by far the more accessible. The first is for what needs to become part of the platform — and that's where the 25 contributors come in.

---

## Governance: Who Checks Code That Nobody Reads?

If contributors don't read their code, someone else has to be accountable for it. Every change goes through a **Pull Request** reviewed and approved by the central team.

Standardization helps here too: when everything follows the same pattern, a reviewer spots deviations immediately. Reviewing a YAML file and a dbt model that look like all the others is much faster than reviewing bespoke code.

---

## The Central Team's New Job

The central team no longer produces most dashboards and pipelines. Its job is to:

* maintain the patterns and conventions that agents copy;
* maintain the platform's building blocks (deployment, ingestion, semantic layer, MCP server);
* review and merge contributions.

That's how a 4-person team can support 25 contributors.

---

## What We're Still Learning

* **Review becomes the critical path.** With 25 contributors, what limits throughput is no longer development capacity, but review capacity.
* **Every exception has a cost.** A single pipeline written "differently, just this once" is enough to give agents a second pattern to copy. Standardization requires constant discipline.
* **Quality rests on the central team.** Contributors who don't read code rely entirely on the conventions and the review. That's acceptable as long as both stay strict.

---

## Key Takeaways

With coding agents, the question is no longer "who knows how to code?" but "is our repository designed so that an agent can't get it wrong?". By betting on one way to do things, declarative configuration and systematic review, we turned business teams into contributors — and a smaller team into a platform team.

---

*Want to open your data platform to business teams without losing control? [Let's talk about it in a 30-minute data chat](https://unytics.io/book-meeting/).*
