---
title: "Nobody Codes by Hand: How We Went from 4 to 25 Contributors on Our Data Platform"
description: "At Optic 2000, nobody writes code by hand: in ten months, the number of contributors to the data platform went from 4 to 25, most of them business people. The BI team first, then business teams at headquarters: how we onboard them, what happens when one of them leaves, and what it changes for the data team."
date: 2026-11-03
---

# Nobody Codes by Hand: How We Went from 4 to 25 Contributors on Our Data Platform

In [a previous article](https://unytics.io/blog/optic-2000-independence/), I described the architecture we built at Optic 2000, in ten months and several simultaneous migrations.

The most striking number of that project isn't technical. Over the same period, the data platform team went from 6 to 4 people, while the number of people contributing to the data repository went from **4 to 25**. Seventeen of them aren't on any data team: they are business people.

And none of them writes code by hand.

This article tells how it happened: who we started with, how we onboard a business user, and what it changes for the data team.

---

## A Small Team Can't Be the Bottleneck

With that many projects at once, a small team that has to handle every business request becomes a bottleneck within weeks. That's the [Ticketing 2.0 trap](https://unytics.io/blog/the-ticketing-2-0-trap/): the data team prepares, the business waits.

There were two ways out: hire, or let others contribute. We chose the second. But letting non-developers change the central repository of the data platform? I was very sceptical myself. So we went step by step, starting with the people closest to us.

---

## Step One: Our Own BI Team

Historically, data at Optic 2000 meant three watertight teams:

* **four data engineers**, who handled ingestion and transformations, in PostgreSQL stored procedures;
* **two BI engineers**, who managed the semantic layer in MicroStrategy;
* **four people in BI**, who built dashboards with point-and-click.

That BI team could read a bit of SQL. They had never touched Git, Python or dbt.

When it left MicroStrategy, Optic 2000 first chose Tableau, and the BI team spent a phenomenal amount of time on it, on repetitive, tedious tasks. We offered them a test: build their dashboards as Streamlit data apps, by *vibe-coding* in our repository, with AI. They were sceptical themselves: will it be clean? Will the numbers be right? Will we be able to maintain it?

Within a few weeks, the shift was spectacular:

* the team became **autonomous** on Streamlit;
* the end-user experience is **far better**, for a fraction of the time we used to spend on Tableau;
* and above all, they didn't stop there: on their own, they started creating and maintaining **their own dbt models**.

Today, we have gone from three teams to two: four data engineers, four people in BI, and no intermediate layer anymore. BI owns the whole chain, from the dbt model to the data app, and Streamlit has become our dashboarding tool, including for thousands of users in stores. The data engineers set the frame and coach the people who build.

---

## Step Two: Business Teams at Headquarters

When we saw our BI team create flawless mart models, with no software background to begin with, we asked ourselves: why stop there?

We went to the business teams at headquarters: business project managers, management control, finance, accounting, digital marketing. Analytical profiles, who track their numbers every day, but who had never written a line of code.

**It all started with small topics.** A project manager built herself a data app to track her Jira tickets, to better steer her projects. Nothing strategic. But that's how trust builds up: hers, and ours.

**Then the topics became critical.** The owner of the store master data, in Salesforce, has to keep up to date a reference that changes all the time, with acquisitions and openings. Before, we were the ones writing dbt tests on that master data: when a test failed, we let him know, and he fixed it after the fact. Today, he has built his own cockpit, far more detailed than our tests. When a store is taken over, for example, the opening dates of the old and the new owner must not overlap. He sees the inconsistencies, and he can be proactive. He is the one who knows these business rules. Not us.

**And some move very fast.** A business project manager, who knows SAP and works with logistics, brought data from SAP into Snowflake, cleaned it up following our conventions, and built an operational dashboard tracking the logistics teams' KPIs. In a single conversation.

*The details — everything business people build, well beyond dashboards — are in [A Dashboard Shows, a Data App Acts](https://unytics.io/blog/data-apps-beyond-dashboards/).*

---

## The Barrier to Entry Is Close to Zero

A myth needs busting: contributing to a repository no longer requires knowing how to code. These people don't write code. They don't even read it. And they don't type a single Git command. **They converse** with Claude, in VS Code or directly in Claude Desktop, without even opening an editor. They describe what they need; in a few prompts, the agent can connect a new source, write the YAML, create the dbt models, build a Streamlit data app, then handle the branch, the commit and the Pull Request.

Onboarding a business user takes two meetings, and a bit of preparation in between:

1. **A first meeting.** We install the tools on their machine — twenty minutes — show them how we work, and look together for the topics that would make sense for them.
2. **In between, we prepare the ground.** We set up the data retrieval and initialize a Streamlit data app for a first use case we talked about.
3. **A second meeting.** The business user takes the keyboard, and iterates on the data app themselves.

Of our four data engineers, one works full time onboarding and coaching business people.

Not everyone is meant to build, though. It takes an appetite for analysis, and at headquarters nobody is forced to. As for the stores, they are the platform's customers: they talk to their data through AI agents, embedded in their data apps or plugged into our MCP server, with no repository, no code editor and no Git. That path is by far the more accessible, and many needs are met there. The repository is for what needs to become part of the platform.

---

## And When a Contributor Leaves?

You might fear that all this work depends on its authors. It's the opposite. Before, business people were already building their own tools, but in the shadows: custom Excel files, with VBA for instance. When the person left, everything was lost. Today, everything is in the platform, written to our standards: anyone can pick it up, with Claude.

---

## The Data Team's New Job

The platform team no longer produces most dashboards and pipelines. Its job is to:

* maintain the patterns and conventions that agents copy;
* maintain the platform's building blocks (deployment, ingestion, semantic layer, MCP server);
* onboard and coach the people who build;
* review and merge contributions.

That's how a 4-person team can support 25 contributors.

The BI team's job is changing too. Yesterday, it answered tickets, with point-and-click. Freed from both, it is becoming proactive: often, business teams don't just need one more number, they need an outside view to rethink the way they work. And the job is huge: Optic 2000 was founded in 1969, and many of its processes are still manual.

---

## Why It Doesn't Turn into Chaos

Twenty-five people and their agents in the same repository: the objection comes right away. And indeed, with 25 contributors, **review becomes the critical path**: what limits throughput is no longer development capacity, but review capacity. Three things keep it manageable, each detailed in its own article.

* **The repository is designed for it.** In a repository where there's only one way to do each thing, the agent just has to copy the right pattern. That's the subject of [Boringly Simple](https://unytics.io/blog/boringly-simple-data-platform/).
* **A concept has only one name.** The agent never has to choose between three synonyms. That's the subject of [One Name, One Definition](https://unytics.io/blog/one-name-one-definition/).
* **Every failure becomes a rule.** None of our guardrails existed at the start, and a Pull Request now reaches us already reviewed by an agent. That's the subject of [The Platform That Learns](https://unytics.io/blog/the-platform-that-learns/).

---

## Key Takeaways

With coding agents, the question is no longer "who knows how to code?" but "is our repository designed so that an agent can't get it wrong?". The rest is a matter of method: start with the team closest to you, then with a willing business user on a low-stakes topic, and let every failure become a rule. That's how we turned business teams into contributors — and a smaller team into a platform team.

Ask yourself the question about your own company: **how many business tools live in an Excel file that only its author knows how to run?** Each of those authors is a contributor waiting to happen.

*This article details one part of a larger story: [Why Your Business Teams Shouldn't Just Be AI Consumers (But Builders Too)](https://unytics.io/blog/self-service-analytics-builders/).*

---

*Want to open your data platform to business teams without losing control? [Let's talk about it in a 30-minute data chat](https://unytics.io/book-meeting/).*
