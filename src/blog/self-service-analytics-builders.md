---
title: "Self-Service Analytics: Why Your Business Teams Shouldn't Just Be AI Consumers (But Builders Too)"
description: "Conversational analytics and proactive feedback loops are transforming access to data. But in a company with complex operations, you need to go further: open the mono-repo to business teams so they become Builders of the platform and of their own operational applications."
date: 2026-11-16
---

# Self-Service Analytics: Why Your Business Teams Shouldn't Just Be AI Consumers (But Builders Too)

*This article is the written version of the talk I gave at Forward Data Conference 2026: "The Analysis That Builds the Platform: Say Goodbye to Ticketing 2.0".*

Last June, Anthropic's Data team published a fascinating write-up on how they built their own internal *self-service analytics* with Claude. Their numbers alone sum up the challenge our entire industry faces in 2026.

By plugging Claude "cold" straight into their otherwise very clean Data Warehouse, **the rate of correct answers topped out at 21%**. By building a rigorous four-layer *harness* — canonical tables, a semantic layer, documented *Skills* and automated validation — **they pushed accuracy above 95%**. But the most telling number comes next: just one month after launch, without continuous maintenance, **their agent's accuracy had already dropped from 95% to 65%** as schemas and the product naturally evolved. To stay on course, **nearly 90% of Pull Requests** touching a data model at Anthropic now include a *Skill* update in the same Git diff.

A few weeks later, Olga Berezovsky published a widely shared analysis on her Substack (*"Self-Service Analytics Is Not Self-Service. But Don't Tell Anyone"*), highlighting one detail: to keep this machine running, Anthropic employs around **30 data professionals — nearly 2% of the company's total headcount**. Her conclusion: *"It takes a village of analysts"* to make AI-powered self-service work.

Do you really need an army at the center? Not necessarily: today, cutting-edge teams are proving that with a well-designed AI feedback loop, 2 or 3 people are enough to serve an entire scale-up.

And yet, looking at the current state of the art, I remain convinced that our ecosystem is stopping halfway. Everyone is trying to perfect the experience of business teams as **conversational consumers** (*Consumers*). At Optic 2000, we bet on going one step further: **enabling business teams to become Builders of the platform and of their own operational applications.**

---

## 💬 Act 1: The State of the Art of "Context Engineering" — and Why It Works Remarkably Well

For fifteen years, data teams have pursued the same goal: break down silos and make business teams autonomous, because autonomy is a company's most powerful value lever.

With *conversational analytics*, that dream has become tangible. And the most advanced teams have solved Anthropic's "21% accuracy" problem by industrializing three clearly distinct roles:

1. **Data Platformers**, who build the technical *harness* (the mono-repo, the MCP server, CI/CD, evals).
2. **Builders (the Data team)**, who model the data and maintain business context in the *harness*.
3. **Consumers (business teams)**, who query data in natural language through Claude, Slack or their BI tools.

---

### 🏆 The Excellence of the Proactive Model: Jolimoi, Gorgias, Photoroom...

Let's be completely honest: when pushed to its limit, this organization is remarkably effective.

Look at what teams like **Gorgias** (where 83% of employees ask more than 1,000 questions a day thanks to *Context Engineering*) or **Photoroom** (where Juliette Duizabo explains how 3 Data people serve the whole company) are doing.

In a software company or a 60–150 person scale-up without heavy physical operations, having 2 or 3 people in Data (those famous 2%) is perfectly reasonable. Especially when the central team moves from a reactive mode to an **ultra-proactive feedback loop** like at Jolimoi:

| Building block of the proactive loop | What it concretely changes |
| ----- | ----- |
| **Automatic capture of dead ends** | As soon as a *Consumer* asks a question the MCP can't answer, the intent is logged automatically. |
| **Proactive listening across the company** | The system ingests public Slack channels and Google Meet transcripts to detect new business topics before a request is even made. |
| **Automatic Pull Request generation** | A daily digest creates Linear tickets and automatically opens dozens of Pull Requests a day to enrich the models and the semantic layer. The central team just has to review and approve. |

With that kind of velocity, let's be fair: for 90% of everyday analytical questions, friction almost entirely disappears and the loss of serendipity becomes very small. This is exactly the feedback loop approach we are putting in place at Optic 2000 for our *Consumer* users.

**So if this model works so well, why do we claim a key piece of the puzzle is missing?**

---

## ⚠️ Act 2: What "All-Consumer" Doesn't Solve — Business Nuance and Taking Action

Most data teams today are trying to copy Alexis Blandin's model: a small, ultra-efficient central team that builds the *harness*, runs the feedback loop and keeps a monopoly on *building*.

But as soon as you step outside a homogeneous SaaS company into a business with complex operations (like Optic 2000 with its 1,200 stores, logistics, finance, insurance partners, SAP and Salesforce), **siloing the Builder role in Data and the Consumer role in the business reveals two major limits.**

### 1. A small central Data team will never master the nuances of every business process

At Optic 2000, we are **8 full-time Data people**: 4 on the Data Platform team and 4 on the BI team.

Even with the best AI agents in the world, how could 8 people at the center claim to know in detail every accounting subtlety of SAP, every business rule of the store master data in Salesforce, and every financial exception across the network? It's an illusion. **Business teams are the ones who know their data and their processes.**

If you prevent analytically minded business people from being *Builders*:

* You lose a considerable amount of efficiency in back-and-forths where information gets distorted at every handoff (even with AI assistance) between the person who knows the business process and the person who validates the dbt model.
* During **deep dives** — where 80% of the value lies in exploring raw tables that haven't been modeled yet — the business analyst can't build the pipeline while exploring. They remain dependent on a round-trip with the central team (a *Ticketing 2.0*, automated by agents and feedback loops, sure, but still an intermediary).

### 2. Business teams don't just need analyses: they need to build applications that act

In the classic model, when you need real applications that go beyond analysis — for example operational tools with read and write access to SAP, Salesforce or Bitbucket — it's still the central team that has to build them on the business's behalf.

Yet with *vibe-coding*, business teams now have the ability to create the tools that solve their daily operational friction themselves. They just need to be given the framework to do it.

---

## 🛠️ Act 3: The Optic 2000 Model — Complementing Conversational Analytics by Turning Business Teams into Builders

At Optic 2000, our conviction is simple: **the Consumer approach in a conversational interface and the Builder approach in VS Code are not opposed — they complement each other.**

* We're obviously not going to ask an in-store optician or an operator who isn't comfortable with computers to open VS Code on our Git repository! For them, the *Consumer* conversational interface with a feedback loop is perfect.
* But limiting yourself to the *Consumer* approach keeps a glass ceiling in place. That's why our **4 Data Platformers** opened our Git mono-repo to our **4 BI specialists** and to **around 20 Builders from business departments** (financial controlling, finance, master data owners...), bringing the total to **25 people actively building the platform** — without a single one of them writing code by hand.

---

### 🎨 The 3 Spaces Where We "Vibe-Code" at Optic 2000

This complementarity takes shape in three distinct workspaces on our platform:

| Vibe-Coding Space | Who uses it? | What happens there | How the platform gets enriched |
| ----- | ----- | ----- | ----- |
| **1. Claude Desktop & OpenWebUI (on an MCP server)** | **Consumers** (Stores, business users) | Direct conversational analysis on the semantic layer with strict access-rights filtering. | **Feedback loop (like at Alexis Blandin's)**: you don't *build* while analyzing, but feedback generates PRs that improve the YAML. |
| **2. Streamlit Data Apps (Playground & embedded AI)** | **Consumers & advanced business users** | Dashboards and operational apps on top of our SaaS tools. Some apps **embed a conversational Claude agent** to analyze the data on screen or generate your own dashboards (see below). | Feedback loop today — and probably tomorrow the ability to trigger PRs directly from the agents embedded in Streamlit. |
| **3. The Git Mono-repo in VS Code (with Claude Code)** | **Builders (Business & BI - ~24 people)** & **Data Platformers (4 people)** | **You build while you analyze**. The business user explores raw data, pipes an ingestion, models in dbt, edits the semantic layer and vibe-codes Streamlit apps. | **Full autonomy**: the business user opens their Pull Request directly in the Git repo as part of their work. |

---

### 💡 Focus on Space 2: When Streamlit Apps Embed Conversational AI and Artifacts

Most of our Streamlit applications are dashboards vibe-coded in VS Code by business teams or the BI team. But several of them combine the best of structured applications and generative AI:

* **The financial statement augmented by a dedicated agent:** A Streamlit app displays a store's financial statements. Right inside the app, a Claude agent is embedded with a hardcoded financial *system prompt*. The end user chats with Claude within the app to dig into their statements, test hypotheses and generate complementary HTML artifacts.
* **The Playground app ("Claude Dashboards"):** We built a Streamlit app that acts as a generator and host for HTML artifacts. A *Consumer* vibe-codes their own dashboard there in playground mode, then saves it. The app now holds dozens of dashboards created by users themselves — durable, discoverable, shareable and all in one place.
* **The alert scheduling app:** A Streamlit app that lets users configure and schedule automatic emails driven by the indicators from our metrics engine.

---

## ⚡ Act 4: Beyond Read-Only — Operational Applications Built on SAP, Salesforce and Git

When a business user becomes a *Builder* in VS Code, they don't just build analytical pipelines or read-only charts. They build **operational applications that let them see AND act** directly on the company's systems.

Here are 6 concrete examples of apps vibe-coded at Optic 2000:

| Vibe-Coded App | Connected system | Operational use (See & Act) |
| ----- | ----- | ----- |
| **1. Inconsistency Detection & Correction** | **Salesforce** | Vibe-coded by the business owner of the store master data: the app detects anomalies in Salesforce, displays them clearly and lets the business **fix the data directly in Salesforce**. |
| **2. Human-in-the-Loop Enrichment** | **Salesforce** | Algorithms compute enrichment proposals for the store master data. The Streamlit app provides the *Human-in-the-Loop* interface where the business reviews and approves before anything is written to Salesforce. |
| **3. Operational business front-end** | **SAP** | A dedicated, custom front-end on top of SAP that offers clear views and runs specific operational processes without the complexity of the native SAP interface. |
| **4. PR governance cockpit** | **Bitbucket** | A far more readable interface than Bitbucket to track all open Pull Requests, see at a glance who needs to review what, and check that all our requirements are met. |
| **5. Visual Semantic Layer editor** | **Git Repository** | An interface on top of Git to visualize and edit the entire semantic layer with business validation, far easier to digest than raw YAML (and integrated with the PRs generated by our feedback loops). |
| **6. Access rights manager** | **Streamlit platform** | A dedicated app to easily manage access permissions for every Streamlit application. |

---

### 🤔 Claude Artifacts vs Apps on Git: Where Will the Line Be Tomorrow?

A legitimate question arises: *"Tomorrow, artifacts generated in Claude or in a playground won't just be read-only charts. They're already durable and shareable, soon organizable like a Google Drive, and will be able to write directly to Salesforce or SAP via MCP connectors. Will we still need business teams to vibe-code Streamlit apps in VS Code and Git?"*

The answer won't be binary: it will be a **continuum of mastery and control**.

* **For lightweight, quick or exploratory needs:** artifacts generated on the fly, saved and shared in a Drive-like space (or in our Streamlit Playground app) will be more than enough and unbeatable in velocity.
* **For business-critical processes:** as soon as you need to write in bulk to SAP or Salesforce with complex upstream algorithms, enforce strict access governance, guarantee non-regression through CI tests and deploy on the company's secure infrastructure, **you'll always want real code files versioned in Git and approved through Pull Requests**.

---

## 🛡️ Act 5: The Architectural Secret — A Declarative Mono-Repo to Align 25 Builders

How do you let 25 people (4 Data Platform, 4 BI and around 20 business users) build in the same Git repository without anyone coding by hand and without creating chaos?

It all relies on the *harness* built by the 4 Data Platformers in a **single, 100% declarative mono-repo**:

1. **Only one way to do each thing:** Whether it's ingesting data, creating a dbt model, adding a metric to the semantic layer (like at Anthropic, where 90% of PRs unify model and context) or deploying a Streamlit app on AWS via Terraform, there's only one declarative pattern. In VS Code, Claude Code sees the whole repository and faithfully reproduces our standards.
2. **The analysis builds the platform (*Deep Dive & Pipe*):** Guided by our *Skills*, a business user exploring raw data in VS Code enriches the dbt model and the semantic layer as part of the same motion as their analysis.
3. **Centralized PR review:** The 4 Data Platformers keep final control by reviewing Pull Requests (helped by CI and our Bitbucket app) before anything goes to production.
4. **Supporting business teams:** One of the 4 Data Platformers is dedicated full-time to supporting business teams so they can make the most of the platform.

---

## 🎯 Conclusion: Open Your Harness to Business Teams

*Conversational Analytics* combined with a proactive feedback loop is a major step forward. Small teams of 2 or 3 people like at Jolimoi or Photoroom demonstrate every day how much this approach transforms access to data for *Consumers*.

But don't stop there. If your company has rich, complex operational processes, your central Data team — however brilliant — will never replace the intimate knowledge your business teams have of their own data and their own tools.

Keep the conversational approach and lightweight artifacts for quick consumption. But **open your mono-repo and VS Code to your business experts**. The day your business teams stop merely asking a chatbot questions and become the *Builders* of the platform and of their own operational applications, you will finally have broken down data's last silo.
