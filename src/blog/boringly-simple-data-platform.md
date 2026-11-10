---
title: "Boringly Simple: How 25 Contributors Change Our Data Platform With Almost No Review"
description: "At Optic 2000, 25 contributors and their AI agents change the data platform with almost no review from the platform team. The secret is a boringly simple platform: configuration separated from deployment glue, settings derived rather than declared, security and monitoring built in, and rules that reach the agent where it works."
date: 2026-11-05
---

# Boringly Simple: How 25 Contributors Change Our Data Platform With Almost No Review

In [Nobody Codes by Hand](https://unytics.io/blog/nobody-codes-by-hand/), I told how the number of people contributing to our data platform at Optic 2000 went from 4 to 25 — most of them business people, working through a coding agent. I ended with a lesson we were still learning: with 25 contributors, **review becomes the critical path**. A platform team of four can't read everything 25 people and their agents produce.

Every change still goes through a Pull Request approved by a human. But in most of them, there's almost nothing left for us to review. Not because we trust agents more than we used to, but because we designed the platform so that a contribution can hardly express a mistake.

Our platform is deliberately **boring**. Adding a data source means writing a YAML file. Deploying a function means a Python file and a few lines of YAML. Publishing a data app means moving a file out of a folder. Everything that's hard — infrastructure, security, deployment, monitoring — is written once, by the platform team, in what I'll call the **glue**. Contributors never need to touch it, and neither do their agents.

This article describes the five principles behind that boredom, and what they change for a platform team. As in [One Name, One Definition](https://unytics.io/blog/one-name-one-definition/), the technical details are tucked away in collapsible sections, for those who want to replicate them.

---

## Why Boring Is the Goal

A data platform contains two kinds of code. The **configuration** says *what* the company needs: this source and its tables, this function and its schedule, this role and what it can read, this data app and who owns it. The **glue** says *how* to deploy it: cloud permissions, warehouse grants, load balancer rules, container definitions, CI steps, alerts.

In most platforms, the two are intertwined. Adding a source means copying a Terraform module, adding a cloud permission, wiring a notification, declaring an alert. Every contribution touches the glue, so every review has to check the glue: is this permission too broad? Will this rule collide with another? Is the alert wired? That's specialist review. It doesn't scale to 25 contributors, let alone to their agents, which will happily write a perfectly plausible policy granting access to every bucket.

We made the opposite choice: **contributors only write configuration, and the configuration can only say what the glue lets it say.** What a contribution can't express, a reviewer doesn't have to check.

It matters even more with coding agents. An agent reproduces what it sees in the repository. In a platform where each pipeline is deployed a little differently, it has a dozen patterns to choose from, and picks one without telling you which. In a boring platform, the thirtieth source looks exactly like the twenty-ninth: the agent copies the previous one, and it's right.

Engineers know the advice to *choose boring technology*. We apply it one level up: **we make contributing boring.** Cleverness belongs in the glue, written once by the people who maintain it. Wherever a contributor goes, there should be nothing to figure out.

---

## Principle 1: Separate Configuration From Glue

The whole platform is driven by a handful of YAML files. Terraform reads them and deploys everything they describe, in loops: nobody writes Terraform to add a source, a function, a web app or a role.

| Configuration file | What a contributor declares | What the glue deploys |
|---|---|---|
| `load/<source>.yml` | a source's tables, their columns and the files that feed them | a warehouse schema, a stage, one table and one Snowpipe per table, freshness monitoring |
| `functions.yml` | a function's schedule or trigger, timeout and memory | a Lambda function or a Fargate task, its schedule or trigger, its logs, alarms and crash detection |
| `apps.yml` | a web app's size, and optionally its paths and environment | a container service, its load balancer rule behind the company login, its health check and logs |
| `snowflake_roles.yml` | a role: which warehouses, which databases or schemas, with which privileges | every grant, on existing and future objects |
| `snowflake_users.yml` | a person: their email and their roles | a warehouse user, with its default role and role grants |

Here is everything a contributor writes to bring a new source from an API into the warehouse. A few lines in `functions.yml`:

```yaml
get_crm:
  category: get_data
  schedule: cron(0 4 * * ? *)
  timeout: 600
  memory: 2048
```

A Python file, `functions/get_crm.py`, whose function calls the API and drops its records in S3 as they are, under one of our decorators. And the description of what lands, in `load/crm.yml`:

```yaml
source_path: crm/
source_type: API
data_extract_lambda: get_crm
description: |
  Customer relationship data: accounts, contacts, opportunities.
format:
  type: JSON
destination_tables:
  - name: ACCOUNTS
    description: Customer accounts, one row per account and extraction.
    pattern: "accounts/accounts_.*\\.ndjson"
    columns:
      - name: ID
        type: varchar
        description: Identifier of the account in the CRM.
      - name: NAME
        type: varchar
        description: Name of the account.
```

Once the Pull Request is merged, the deployment pipeline does the rest: the function goes live with its schedule, a `CRM` schema appears in the warehouse with an `ACCOUNTS` table and its Snowpipe, and the files the function drops start flowing in. Not a line of Terraform, not a click in a console. **Adding a source adds configuration, never glue**: today, about forty source files and some forty functions are deployed by under 5,000 lines of Terraform that contributors never need to open.

Reviewing such a contribution means reviewing a declaration: a schedule, a memory size, the description of a table. The reviewer doesn't check whether a cloud permission is too broad or a Snowpipe wired to the right notification: there's no permission and no Snowpipe in the diff. Those were reviewed once, when the glue was written, and they're the same for every source.

When a need comes up that the configuration can't express, we don't make an exception: **we extend the configuration, for everyone, with an optional field.** A function that unzips large archives needs more disk: `ephemeral_storage`. A function calling an API with a strict rate limit must never run more than twice at once: `max_concurrency`. A table refreshed once a week mustn't raise a freshness alert every day: `max_staleness_hours`. A source that isn't producing yet, or is down while its supplier fixes it: `muted_until`, with a date, after which monitoring resumes on its own. Each field was added to the glue once, and is now available to every contributor, with no new pattern to copy.

And access to the warehouse is configuration too. Privilege sets are defined once, and each role combines them; a person is an email and a list of roles. No `GRANT` is ever run by hand: a missing privilege is added to the YAML and deployed like everything else. The YAML file *is* the access policy — versioned, readable by anyone, reviewed like any change.

<details>
<summary><strong>Going further: the glue behind a YAML file</strong></summary>

<p>Terraform reads every configuration file into a local value, and each resource loops over it. A simplified version for sources:</p>

<pre><code class="language-hcl">locals {
  sources = {
    for file in fileset("${path.module}/../load", "*.yml") :
    trimsuffix(file, ".yml") =&gt; yamldecode(file("${path.module}/../load/${file}"))
  }
}

resource "snowflake_schema" "source" {
  for_each = local.sources
  database = "RAW"
  name     = upper(replace(each.key, "-", "_"))
  comment  = split("\n", trimspace(each.value.description))[0]
}</code></pre>

<p>The schema takes the name of the file, and its comment the first line of the source's description. Stages, tables, Snowpipes and notifications follow the same pattern, over one entry per table.</p>

<p>Warehouse access works the same way. Privilege sets are YAML anchors, defined once, and roles combine them per database or schema:</p>

<pre><code class="language-yaml">read: &amp;read
  TABLES: [SELECT]
  VIEWS: [SELECT]

write: &amp;write
  SCHEMA: [CREATE TABLE, CREATE VIEW]
  TABLES: [SELECT, INSERT, UPDATE, DELETE, TRUNCATE]
  VIEWS: [SELECT]

role_grants:
  FINANCE:
    warehouses: [FINANCE_WH]
    objects:
      MARTS: *read
      SANDBOX.FINANCE: *write
  MARKETING:
    warehouses: [MARKETING_WH]
    objects:
      MARTS.MARKETING: *read</code></pre>

<p>The glue turns each entry into grants on all existing and future objects, so a table created tomorrow is readable by the roles that should read it, without anyone thinking about it. Users are even simpler:</p>

<pre><code class="language-yaml">human_users:
  jane.doe@example.com:
    roles: [FINANCE]
  john.smith@example.com:
    roles: [MARKETING, FINANCE]</code></pre>

<p>The username is derived from the email, and the first role is the default role.</p>

</details>

---

## Principle 2: Derive, Don't Declare

Every field a contributor fills in is a field they can get wrong. So we ask the same question of every setting: could the glue compute it? If it can, the field doesn't exist.

**If two settings must agree, one of them shouldn't exist.**

* **Where a function runs.** A Lambda function can't run longer than 15 minutes or use more than 10 GB of memory. Our functions declare their `timeout` and `memory`; when they ask for more than Lambda allows, the glue deploys them as a scheduled Fargate task instead — same Python file, same decorator, same status reporting. There's no `backend` field, so no backend can contradict the timeout.
* **How much CPU.** Fargate only accepts certain pairs of CPU and memory. Declaring the CPU would just be a chance to declare an invalid pair, so the glue picks the smallest valid CPU for the requested memory. A task that needs more compute asks for more memory.
* **Where a web app lives.** A web app's URL is its name, and its health check has a default path. Its load balancer rule needs a priority, unique across all web apps. Nobody picks it, and it isn't the web app's rank in alphabetical order either: adding a web app would shift all the ones after it, and the load balancer refuses two rules with the same priority, even for a moment. It's derived from a hash of the name, so adding or removing a web app never moves the others.
* **What things are called.** A source's warehouse schema is the name of its YAML file. A person's warehouse username is derived from their email, and their first role is their default role.
* **What the menu shows.** Our data apps — dashboards and small business tools, each a single Python file — are listed in a menu, but there's no menu file: the menu is the folder tree. A section is a folder with a short `_section.yml`, and each data app declares its own title, icon, description and owner, in its own file:

```python
page.config(
    title="Supplier Invoices",
    icon="🧾",
    description="Invoices received from suppliers, by store and by month.",
    owner="jane.doe@example.com",
)
```

Adding a data app means adding a file; deleting the file removes it from the menu. There's no central list to update, and no menu entry pointing to a data app that's gone. Even publishing is a file move: a new data app starts in an under-construction folder, which the web app we serve to our stores never shows, and goes live there when the file moves out.

Derivation has a second benefit: the platform can change without anyone migrating anything. If Lambda's limits change tomorrow, we change one rule in the glue, and every function lands where it should at the next deployment.

---

## Principle 3: One Place for Each Kind of Logic

Configuration takes care of infrastructure. But contributors also write logic: Python functions, SQL models, data apps. There, the same idea takes another form: **each kind of logic has exactly one place where it can live**, and the boundaries are strict.

* **A function lands its source as is.** Every field the source returns, under the source's own name, nested objects and arrays kept whole: no renaming, no filtering, no unnesting. All transformation happens in dbt. An extraction has nothing to decide, and nowhere to hide a business rule.
* **Data enters the warehouse one way.** Every source lands in S3 first, and Snowpipe loads it: no function ever writes to the warehouse directly. Every raw row can be traced back to its file, and any load can be replayed.
* **Business logic lives in dbt, metrics in the semantic layer.** A ratio is computed by the semantic layer as a ratio of sums, never averaged in a data app. Year-over-year comparisons — which period to compare with, which stores to include — are computed by a single engine, from a rule written once in our data portal's guides; no data app and no ad hoc query re-derives them. Even an agent answering an ad hoc question queries the semantic layer first, so its figures match those of the data apps.
* **Definitions live in the business dictionary**, attached to column names, as described in [One Name, One Definition](https://unytics.io/blog/one-name-one-definition/).
* **Look and feel lives in a style guide.** Data apps don't style their own indicator cards or tables: they call the helpers of a shared style-guide module, so that data apps written by different people look like one product.
* **Explanations live next to what they explain.** A function's entry in `functions.yml` holds no explanatory comment: what the function extracts, why that schedule, how its incremental load works goes in the docstring of its Python file, which the data portal publishes on the function's page. A metric's definition lives in its description in the semantic layer, and the portal renders it.

When every kind of logic has a single place, **a reviewer no longer asks *where* something should be, only *whether* it's right.** And an agent never has to choose between two places: there's only one.

---

## Principle 4: Make the Safe Path the Only Path

A contributor shouldn't have to *remember* security, deployment or monitoring. When something matters, it's built into the glue, with no way to opt out — and **what can't be forgotten doesn't need to be checked.**

### Security at the door, not in each data app

Our web apps sit behind a load balancer that requires the company login before a single request reaches them, and each one re-checks the user's identity through a shared library. A store manager only ever sees their own stores' figures, because the perimeter is applied by the semantic layer, from the user's identity, for every data app at once — whether the question comes from a data app, a Teams card or an AI assistant through our MCP server. A contributor building a data app can't forget a security check: there isn't one to write.

Agents get the same treatment. On a contributor's workstation, the agent connects to the warehouse with the contributor's own login and roles: a marketing contributor's agent can't read what marketing can't.

### Configuration where its owner can change it

**Put each piece of configuration where its owner can change it safely.** Infrastructure belongs in reviewed YAML. Who can open which data app doesn't: it changes often, and it's decided by managers, not contributors. We first declared access in each data app's file, then moved it out of the repository altogether. Today it lives in a database, edited by a handful of managers from a dedicated data app. A data app nobody has been granted access to is open only to its owner and to admins. An access request arrives in Teams with a link that opens that person and that data app, and suggests the groups that would grant it while opening the fewest other data apps. A Pull Request can't grant access, so no reviewer has to check who gets to see what.

The same goes for a setting an operator must change without an engineer: it goes to a key-value store they can write to, not into the code. Secrets hold credentials, nothing else.

### One deployment path

A merge to main triggers the only deployment path. Based on the files changed, the pipeline rebuilds what's needed, in a fixed order: infrastructure first, then the data transformations, then the code and web apps that read them — so code never ships ahead of the data it expects. Even metric definitions ship with the data: the dbt run publishes them next to the exports it produces, and every data app picks up the new version within minutes.

A Pull Request builds the models it changes in a schema of its own, where reviewers and agents can compare them with production. But it can't deploy anything, by accident or on purpose: the cloud only issues production credentials to pipelines running on main. And when a web app misbehaves after a deployment, rolling it back is one line in `apps.yml`: pin its image to the previous commit.

### Monitoring built into every function

Every function runs under one of our decorators: scheduled, or triggered by a file, an event or an HTTP call. The decorator records each run's status, duration and logs. If the function dies before it can report — out of memory, out of time — a crash handler writes the error in its place. Every hour, a check compares each function's last run with its schedule; every morning, after a job has reloaded any file Snowpipe missed, another compares each raw table's freshness with its threshold: 24 hours, unless the source's YAML says otherwise. An error stays flagged until someone marks it as resolved in the portal, even if the next run succeeds. And since run statuses are exposed in the semantic layer like any other data, a scheduled Teams card lists the functions in trouble. When there are none, it says so: a card that stays silent when all is well can't be told from a card that's broken.

A contributor gets all of this for their function without writing a line of it.

### Documentation generated from the configuration

Whenever the configuration changes, the data portal is regenerated from it: a page per source and per table, from the YAML files; a page per function, with its docstring, its configuration, its latest status and a button to run it; a page per dbt model; the dictionary and the metrics. Contributors document by filling in the descriptions of their configuration — there's no separate documentation to keep in sync.

**Security, deployment and monitoring aren't items on a review checklist: they're properties of the platform.**

---

## Principle 5: Put the Rules Where the Agent Works

Configuration and glue remove most of the room for error. What's left — SQL, Python, data apps — is written by agents. For that part, the rules have to reach the agent at the moment it acts, and the machine has to check them.

* **Instructions next to the code they govern.** A root instructions file (`CLAUDE.md`, for Claude Code) describes the platform and its non-negotiable rules. Each main folder — ingestion, functions, infrastructure, web apps — has its own, which the agent loads when it works there. Rules for a type of file — YAML, Terraform, Python, Markdown — load only when the agent touches such a file. The agent's context holds the rules of what it's doing, not the whole rulebook.
* **A skill for each kind of task.** Before touching a dbt model, the agent loads the dbt skill: layers, naming, tests, SQL style, and an exit gate before it hands back. Same for data apps and for the style guide. And contributors publish with a single command: a skill commits their work, pushes it, opens the Pull Request with its reviewers and writes its description — including what a reviewer must not miss, such as a data feed being cut.
* **Checks at write time.** When the agent edits the business dictionary or the semantic layer, a hook re-runs their check and sends any violation back to the agent, which fixes it before a human ever sees the diff — as described in [One Name, One Definition](https://unytics.io/blog/one-name-one-definition/).

<details>
<summary><strong>Going further: how the instructions are organized</strong></summary>

<pre><code>CLAUDE.md                          platform overview and non-negotiable rules
load/CLAUDE.md                     ingestion conventions
functions/CLAUDE.md                function conventions
infra/CLAUDE.md                    infrastructure conventions
data_portal/CLAUDE.md              web app conventions
.claude/rules/yml.md               loaded when the agent touches a YAML file
.claude/rules/terraform.md         loaded when it touches a Terraform file
.claude/rules/python-standards.md  loaded when it touches a Python file
.claude/skills/dbt-model/          loaded before creating or changing a dbt model
.claude/skills/streamlit/          loaded before creating or changing a data app
.claude/skills/publish-pr/         commit, push and open the Pull Request in one command
.claude/skills/review-*/           review a Pull Request, verdict MERGE or NO MERGE
.claude/settings.json              hooks</code></pre>

<p>A rule file declares the files it applies to in a header:</p>

<pre><code class="language-markdown">---
paths:
  - "**/*.tf"
---

# Terraform Style
…</code></pre>

</details>

### Rules about rules

Instructions files drift like any documentation. Two meta-rules keep them sharp. **Every correction becomes a rule**: when we correct the agent, it writes the lesson into the right instructions file, with its technical reason, before going on, so the same mistake doesn't happen twice. And **each rule lives in one place**: a business rule is written once, in the data portal's guides, and instructions only point to it, because two copies end up contradicting each other and the agent follows the wrong one.

### Rules learned the hard way

Several of our sharpest rules come from something that went wrong. They're worth stealing:

* **Never cut a feed that's still read.** Removing a function's schedule stops every table it feeds at once — and readers aren't only dbt models: some data apps read raw tables directly. Search the whole repository, switch the readers first, then cut.
* **A mute never comes with a cut.** Silencing a table's freshness alert at the same time as you stop feeding it hides exactly the signal that would reveal the mistake.
* **A model only reads data that's already in production.** Ingestion ships in a first Pull Request, and the models that read it in a second, once the data has landed.
* **No write to production as a side effect of a code change.** A data migration runs after the code that needs it is deployed, on an explicit go, after a dry run: until then, production still reads the old format.
* **A change that adds something leaves everything else as it was.** A fix noticed along the way is proposed separately, never slipped into the same diff: a reviewer approving a new table shouldn't unknowingly approve a change to existing figures.

None of these shows up in a SQL diff. That's precisely why they're written where the agent works, and why the publishing skill flags any cut feed in the Pull Request description.

### Review agents before human reviewers

Finally, a contribution meets review agents before it meets us. Two review skills, one for dbt models and one for data apps, read a Pull Request the way we would: the rule files are their checklist, and they report only what blocks — whatever changes a figure, a grain or a column name, crashes in production, touches access rights or a file shared by every data app, or duplicates an existing data app. Style never blocks. They also check the data: the dbt reviewer queries the models the Pull Request built, and the data app reviewer recomputes, with independent queries, every figure the data app displays — the real bugs of our past data app reviews were all found in the data, not in the code. If a check can't run, the verdict is never "merge".

A verdict opens with a summary in plain language, written for the contributor, before the technical details and the comments to post on the Pull Request (figures made up):

```
MERGE: NO, the "active stores" card shows 120 stores where the definition gives 100.

1. Duplicate: no.
2. Against our practices or a business rule: yes, 1 point:
   - the card counts every store with a sale; the definition counts stores open over the period.
3. Reinvents the wheel: partly — the cards are drawn by hand instead of using the style guide.
4. Merge: NO.
```

Human approval doesn't disappear. Every Pull Request is still approved by a person, and business owners still answer for their domain: that's governance, the subject of [Nobody Codes by Hand](https://unytics.io/blog/nobody-codes-by-hand/). But the approval now rests on a verdict that has already checked the conventions and the figures. What's left for the human is the question no machine can settle: is this the right thing to build?

---

## What This Changes

* **Review shrinks to what matters.** Most diffs are YAML declarations and code that follows a pattern a review agent has already checked. We read intent, not plumbing.
* **Agents get it right the first time.** A boring platform has one pattern per task. The agent copies the last source, the last function, the last data app — and it's right.
* **Contributors build what they know.** A financial controller can add a source, a model and a data app without ever hearing about IAM, VPCs or warehouse grants. Their expertise goes into the business logic, which is where we need it.
* **The glue improves for everyone at once.** When we improve crash detection, tighten a grant or change a default, every function and every role gets it at the next deployment. Nobody migrates their pipeline, because nobody owns a pipeline's plumbing.
* **The infrastructure stays replaceable.** Since the configuration says *what* and not *how*, moving a function from Lambda to Fargate — or the platform to another provider — is a change in the glue, not in forty contributions. That's what I meant, in [my article on independence](https://unytics.io/blog/optic-2000-independence/), by *configuration is an asset, the metal is a commodity*.
* **The platform team becomes a product team.** Its product is the glue, the conventions and the review agents; its users are the 25 contributors and their agents.

---

## What It Costs

Boring for contributors isn't free for the platform team.

* **The glue is harder to write.** Deriving everything, supporting every optional field, closing every unsafe path: our Terraform is denser than a module per pipeline would be. It's written once, but it has to be written well. And when a derivation is needed outside Terraform — the portal also needs to know where a function runs — both implementations must change together.
* **You have to say no.** Every "just this once" exception is a second pattern for agents to copy. When a need doesn't fit, the answer is to extend the configuration for everyone, or to decline.
* **The configuration must stay declarative.** A YAML file that grows conditions and loops is a programming language without a debugger. Ours only says *what*; anything that needs logic goes into the glue, as a derivation.
* **Rules need gardening.** Instructions grow with every correction. Keeping each rule in one place, with its reason and without stale examples, is a job in itself.

---

## Key Takeaways

Our platform is boring so that what people build on it doesn't have to be.

Everything hard — infrastructure, security, deployment, monitoring — is written once, in the glue, by the team that maintains it. Everything else is configuration that says *what*, derived wherever it can be, with a single place for each kind of logic and the rules waiting for the agent wherever it works. What's left for the reviewer is the only question that ever mattered: is this the right thing to build?

Ask yourself this about your own platform: **when someone adds a data source, how many of the lines they write are plumbing?** Every line of plumbing in a contribution is a line someone has to review — and with agents writing more and more of them, that someone won't keep up.

---

*Want to open your data platform to business teams and their agents without becoming the bottleneck? [Let's talk about it in a 30-minute data chat](https://unytics.io/book-meeting/).*
