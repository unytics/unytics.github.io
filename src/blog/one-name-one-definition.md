---
title: "One Name, One Definition: How We Document 1,800 Columns Without Documenting a Single dbt Model"
description: "At Optic 2000, no dbt model describes its columns, yet every column has a definition: it is attached to the column's name and written once, in a business dictionary. Naming conventions, guardrails for coding agents, a generated data portal: how a single way of naming things eliminates definition drift."
date: 2026-11-04
---

# One Name, One Definition: How We Document 1,800 Columns Without Documenting a Single dbt Model

At Optic 2000, our data platform has more than 350 dbt models and some 1,800 column names. Every one of them has a definition, available to everyone in our data portal and organized by business entity.

Yet open any of our dbt models' YAML files: you won't find a single column description.

That's not an oversight. It's the core of our approach: **we don't document models, we document names.**

In a typical dbt project, each model re-describes its columns in its YAML file. The same customer identifier is described in staging, then in the intermediate model, then in the mart, then in the export: four copies of one definition, written at different times by different people. They always end up diverging. A fix lands in one place only; a new column arrives without a description, because filling in the YAML is a chore; and the day two descriptions contradict each other, nobody knows which one to trust.

Data engineers will recognize the problem: it's denormalized data, with its update anomalies. The `{{ doc() }}` blocks in dbt and the tools that propagate descriptions from one model to the next treat the symptom, at the cost of extra machinery. They don't remove the copies.

**With AI agents, this drift gets expensive, and fast.** Anthropic's Data team measured it: a month after launching its analytics agent, without continuous maintenance, the agent's accuracy had dropped from 95% to 65%, as schemas and the product naturally evolved. To stay on course, nearly 90% of the team's Pull Requests that touch a data model now ship a *Skill* update in the same diff. An agent's context goes stale as fast as the code it describes.

Our answer fits in one sentence: **a concept has a single name, a name has a single definition, and that definition is written only once.** It only holds on one condition — that a name really means the same thing everywhere — and that's the whole point of our naming conventions.

This article explains why **these rules matter as much for agents as for humans**, how we made them impossible to bypass, and how every model's documentation became a computed by-product. For teams that want to replicate the approach, the technical details are tucked away in collapsible sections.

---

## Why Rules Matter, for Humans and Agents Alike

**A name is the most-read documentation there is.** A column's name travels with the data: in every query, every result, every Excel export, every answer from an AI assistant. Its description is read only by those who go looking for it — which is to say, almost nobody. An ambiguous name like `status`, `date` or `amount` breeds questions, wrong joins and wrong numbers, often without anyone noticing.

**Agents don't ask: they guess.** A coding agent rediscovers the repository at every session and reproduces what it sees there. If it finds `email`, `client_mail` and `customer_email`, it won't pick "the right one": it will create a fourth. Faced with a `date` column in an orders table, an analyst asks whether it's the creation, invoicing or delivery date. An agent picks one, and doesn't tell you.

As I wrote in [Nobody Codes by Hand](https://unytics.io/blog/nobody-codes-by-hand/), in a repository where there's only one way to do each thing, the agent just has to copy the right pattern. Naming is the textbook case of that rule: **every synonym is a second pattern to copy.**

**A convention is a decision made once and for all.** Without a rule, every new column opens a micro-debate: between two humans in review, or inside the reasoning of an agent that lacks the context to settle it. With 25 contributors, most of them not engineers, these debates don't scale.

**And a rule an agent can break without being told is only a suggestion.** Writing the conventions down in an instructions file isn't enough: the machine has to check them at the very moment the column is written. More on that below.

---

## The Principle: One Concept, One Name, One Definition

Here's what the typical approach produces, across three models:

```yaml
models:
  - name: stg_crm__contacts
    columns:
      - name: email
        description: "Contact email"
  - name: dim_customers
    columns:
      - name: email_customer
        description: "Customer email address, in lowercase"
  - name: exp_customers_newsletter
    columns:
      - name: customer_email
        description: "Cleaned customer email"
```

Three names and three definitions for a single concept. Which one is right? And which one will the agent copy into the fourth model?

Our base rule is a bijection:

* **one concept = one name**, everywhere: from staging to marts, whatever the model, the source or the original format;
* **one name = one concept**: two different names mean two different concepts, and a given name always has the same type and the same format. The day a column's meaning changes, so does its name.

If a name means exactly the same thing in every model that carries it, its definition no longer depends on the model. It can be attached to the name, once, in a **business dictionary**.

Our dictionary is a single YAML file, organized by business entity: customer, order, product, store… about sixty in all. Each entity has a description, and its columns are filed into two sections: `dimensions`, which describe (identifiers, dates, labels, booleans), and `facts`, which aggregate (amounts, quantities, counts). One line per column, in alphabetical order, and each name appears only once in the whole file:

```yaml
order:
  description: >-
    Order placed by a customer, in store or on the e-commerce website.
  dimensions:
    channel_order: Channel through which the order was placed (store, e-commerce website, phone).
    date_creation_order: Date on which the order was recorded.
    id_order: Unique identifier of the order, across all sources.
    is_cancelled_order: Whether the order was cancelled after it was created.
    status_order: Stage of the order in its lifecycle (being prepared, shipped, delivered).
  facts:
    amount_including_tax_order: Total amount of the order, including tax and shipping fees.
    amount_shipping_fee_order: Shipping fees charged to the customer, including tax.
    number_items_order: Number of items in the order.
```

And here, as a result, is a dbt model's YAML file: a description, an owner, tests. No columns.

```yaml
models:
  - name: fct_orders
    description: |-
      One row per order, across all sources.
    config:
      meta:
        owner: "jane.doe@example.com"
    tests:
      - unique:
          column_name: id_order
      - not_null:
          column_name: id_order
```

The model's description says what a row represents. What each column means, the dictionary already says.

Three principles round out the rule:

* **An entity is a broad business domain** — customer, product, store — never a source table, a data provider or an aggregate. A reference table that only translates a code into a label isn't an entity: its labels join the entity they describe. That's what keeps the dictionary readable at 1,800 columns.
* **A definition describes the concept, not how it's built.** It mentions neither the technical name of a source field nor a dbt model: `email_customer` is still "the customer's email address" the day we switch CRMs or rewrite the model.
* **The dictionary says what a column means; the semantic layer says how to aggregate it.** The metrics' SQL lives in our semantic layer, which I described in [my article on independence at Optic 2000](https://unytics.io/blog/optic-2000-independence/). Its entities carry the name of a dictionary entity and have no description of their own: they inherit the dictionary's. A metric that no model materializes, such as average basket size, exists only in the semantic layer; the dictionary only documents real columns.

---

## The Conventions That Make a Name Unique

To serve as the key to its definition, a name must be unique across the whole warehouse, and predictable. That's the sole purpose of our naming conventions: they're not a matter of taste.

* **The name carries its entity.** `email` becomes `email_customer`, `status` becomes `status_order`. This suffix makes the name unique and says which dictionary entity it belongs to.
* **The suffix names the entity described, not the table that carries it.** A product's family is called `family_product` in sales lines, quote lines and return lines: three models, one definition. Never `family_product_sale`.
* **The prefix announces the type.** `is_` or `has_` for a boolean (`is_cancelled_order`, `has_phone_customer`), `date_` for a date, `datetime_` for a UTC timestamp, `amount_` for an amount. An agent that reads `is_active_customer` knows it filters on `true` — not on `1`, nor on `'Y'`.
* **Whole words.** No abbreviations or in-house acronyms (`compliance`, not `compl`), except official codes (GTIN, IBAN…).
* **The business concept from staging onwards.** A column takes the name of the business concept from the very first transformation, not the source's name: the `AccountId` field of a Salesforce opportunity becomes `id_customer_salesforce`, not `account_id`.
* **One language.** Our names are in French, the language of the people who read these columns; this article translates them into English. What matters isn't which language you choose, it's having only one: never `_commande` and `_order` in the same warehouse.
* **An identifier's name says how far it has been unified.** `id_customer_salesforce` only makes sense in Salesforce; `id_customer_source` brings together identifiers from several sources, each prefixed with its own; `id_customer` is the unified customer. A join on `id_customer` holds everywhere; a join on `id_customer_salesforce` only holds in the Salesforce world — and the name says so.

<details>
<summary><strong>Going further: common mistakes and format rules</strong></summary>

<p>The most common mistakes:</p>

<table>
<thead>
<tr><th>Avoid</th><th>Prefer</th><th>Why</th></tr>
</thead>
<tbody>
<tr><td><code>email</code></td><td><code>email_customer</code></td><td>The email of which entity?</td></tr>
<tr><td><code>status</code></td><td><code>status_order</code></td><td>The name must be unique across the warehouse.</td></tr>
<tr><td><code>date</code></td><td><code>date_creation_order</code></td><td>SQL reserved word, and which date?</td></tr>
<tr><td><code>date_created_order</code></td><td><code>date_creation_order</code></td><td>An action noun, not a past participle.</td></tr>
<tr><td><code>value_discount</code></td><td><code>amount_discount</code></td><td>An amount starts with <code>amount_</code>.</td></tr>
<tr><td><code>num_itm_ord</code></td><td><code>number_items_order</code></td><td>No abbreviations.</td></tr>
<tr><td><code>is_active</code> as <code>1</code> / <code>0</code></td><td><code>is_active_customer</code> as <code>true</code> / <code>false</code></td><td>A boolean is a real boolean, and carries its entity.</td></tr>
<tr><td><code>family_product_sale</code></td><td><code>family_product</code></td><td>The suffix names the entity described, not the model.</td></tr>
<tr><td><code>country_website</code></td><td><code>country_website_visitor</code></td><td>The visitor's country, not the website's.</td></tr>
<tr><td><code>name_customer_crm</code></td><td><code>name_customer</code></td><td>A business attribute doesn't carry the name of its source.</td></tr>
</tbody>
</table>

<p>And the format rules:</p>

<ul>
<li><strong>Dates:</strong> <code>date_&lt;event&gt;_&lt;entity&gt;</code> (<code>date_delivery_order</code>). Timestamps: <code>datetime_&lt;event&gt;_&lt;entity&gt;</code>, in UTC unless the definition says otherwise.</li>
<li><strong>Date parts:</strong> the name gives the format (<code>year_yyyy</code>, <code>month_mm</code>, <code>month_yyyymm</code>) and carries no entity: it's the same year everywhere.</li>
<li><strong>Amounts:</strong> <code>amount_</code>, never <code>value_</code>. An amount that isn't expressed in the currency unit says so in its name (<code>price_in_cents_item</code>).</li>
<li><strong>SQL reserved words:</strong> never on their own as a column name (<code>date</code>, <code>order</code>, <code>group</code>), with one exception: <code>date</code> is the calendar day of day-grain tables, as in the calendar.</li>
<li><strong>Qualifying suffix:</strong> only when two versions of the same attribute coexist in a model, and with a business meaning: <code>brand_name_product</code> next to <code>brand_name_product_before_unification</code>. Never <code>_old</code>, <code>_new</code> or <code>_v2</code>.</li>
<li><strong>Technical columns:</strong> lineage columns have a single name across the whole project, prefixed with <code>_</code>, and live, like the identifiers of reference tables, in a <code>technical</code> entity of the dictionary. <code>_source</code> gives a row's source in models that combine several; <code>_source_row_updated_at</code> is the date the row was last modified in the source, whatever the original field is called (<code>SystemModstamp</code> in Salesforce, <code>updated_at</code> elsewhere).</li>
<li><strong>Case:</strong> all lowercase, in <em>snake_case</em>. Models are plural, named <code>stg_&lt;source&gt;__&lt;table&gt;</code> in staging.</li>
</ul>

</details>

<details>
<summary><strong>Going further: the three tiers of identifiers</strong></summary>

<p>When the same business object comes from several sources — a product listed both in the ERP and on the e-commerce website, for example — the name of its identifier says how far it has been unified, and its value says where it comes from:</p>

<table>
<thead>
<tr><th>Tier</th><th>Name</th><th>Example value</th><th>Created in</th></tr>
</thead>
<tbody>
<tr><td>1. Source identifier</td><td><code>id_product_erp</code></td><td><code>12345</code></td><td>the source's staging</td></tr>
<tr><td>2. Multi-source identifier</td><td><code>id_product_source</code></td><td><code>erp::12345</code>, <code>ecommerce::SKU-987</code></td><td>the model that combines the sources</td></tr>
<tr><td>3. Unified identifier</td><td><code>id_product</code></td><td><code>GTIN::3600000000016</code>, or <code>erp::12345</code> as a fallback</td><td>the model that matches the sources</td></tr>
</tbody>
</table>

<ul>
<li>Tier 3 is prefixed with the rule that made the match possible (here the GTIN), or, failing that, with the source retained.</li>
<li>Each tier is only created when it's needed: no union of sources, no tier 2; no match used downstream, no tier 3.</li>
<li>The separator is always <code>::</code>, and source prefixes are lowercase, like the values of the <code>_source</code> column. When a source has several instances (one database per company, for example), a discriminator goes in between: <code>erp::company_02::12345</code>.</li>
<li>A source identifier never serves as a business identifier: it doesn't leave staging and intermediate models, and in the marts, the reference identifier is called <code>id_product</code>, even when the ERP is the source of truth. Otherwise, the name no longer tells you whether you're handling the ERP's identifier or the unified one.</li>
</ul>

<p>The payoff: a join key's name tells you how much you can trust it, and an identifier's value tells you where it comes from without tracing the lineage.</p>

</details>

---

## Making the Rule Impossible to Bypass

Conventions written in a Markdown file remain wishful thinking. With 25 contributors and as many agents, they only hold if the machine enforces them, at write time rather than in review. We put four locks in place.

### 1. A single way in: a CLI

Agents don't edit the dictionary by hand: they go through a small Python CLI, the same one we use to query our semantic layer. It answers the two questions to ask before naming a column — does this name already exist? what does it mean? — and it's the CLI that does the writing:

```console
$ uv run scripts/semantic_layer.py search email
- column `email_store` (store.dimensions) — Email address of the store.
- column `email_customer` (customer.dimensions) — Email address of the customer (in lowercase).
- column `is_optin_email_customer` (customer.dimensions) — Whether the customer has agreed to receive emails.
…

$ uv run scripts/semantic_layer.py add-column customer dimensions email_customer "Customer email."
column `email_customer` already defined in customer.dimensions (l.836)

$ uv run scripts/semantic_layer.py add-column customers dimensions segment_customer "Customer segment."
unknown entity 'customers'. Closest: customer.

$ uv run scripts/semantic_layer.py add-column customer dimensions segment_customer "Value of CUSTOMER_TIER__C."
the description cites a source field name, `CUSTOMER_TIER__C`: a business definition doesn't carry one
```

Every write inserts the line at its alphabetical position, shows the diff and runs the full check before and after: if the write introduces an inconsistency, it's rolled back. Renaming or deleting a column is refused as long as the semantic layer uses it; otherwise, the command lists the models that still reference the old name. Read commands accept a Git revision (`--ref`), to review the dictionary as a Pull Request changes it.

As a bonus, the agent spares its context window: it loads one definition, not a file of tens of thousands of tokens.

### 2. A check after every agent write

In Claude Code, two *hooks* keep the agent on track:

* **after every file write**, a hook re-runs the check if the dictionary or the semantic layer has changed — including when the agent wrote the file without going through the CLI. It puts the dictionary back in alphabetical order and, if any inconsistency remains, returns an error code: the list of issues goes back to the agent, which fixes them in the same session, before a human ever sees the diff;
* **before every read**, another hook refuses to load these two files in full, and points the agent to the command that answers its question.

The agent doesn't need to remember the rule: it can't break it without the machine telling it.

### 3. A check before handing back

The dbt *skill* — the instructions the agent loads before touching a model — ends with an exit gate. Before declaring the work done, the agent looks up every column of the final `select` of every modified model in the dictionary, and reports back: "Dictionary: 24 columns checked across 3 models, 0 missing". A missing column gets defined in the same diff as the model.

### 4. CI

Finally, the same check runs in CI, on every Pull Request as well as on main, whenever the dictionary or the semantic layer changes, before dbt runs.

The result: a new name arrives with its definition, in the same diff as the SQL that creates it. Anthropic gets there through the discipline of its teams; we hand as much of it as we can to the machine.

<details>
<summary><strong>Going further: the Claude Code hooks and what the check verifies</strong></summary>

<p>The two hooks, declared in the repository's <code>.claude/settings.json</code> (simplified version):</p>

<pre><code class="language-json">{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Read",
        "hooks": [{"type": "command", "command": "uv run scripts/semantic_layer.py read-hook"}]
      }
    ],
    "PostToolUse": [
      {
        "matcher": "Write|Edit",
        "hooks": [{"type": "command", "command": "uv run scripts/semantic_layer.py hook || exit 2"}]
      }
    ]
  }
}</code></pre>

<p>Claude Code passes the tool call as JSON on standard input: the script checks which file is targeted and does nothing for any other. Exit code 2 does all the work. After a write, it sends the error message back to the agent, which treats it as feedback to act on; before a read, it blocks the tool, and the message names the command to use instead.</p>

<p>The check, run by the hook, by every CLI write and by CI, verifies that:</p>

<ul>
<li>each column fits on one line, in alphabetical order within its section;</li>
<li>each name is defined only once in the whole file, across all entities and sections;</li>
<li>each entity has a description, and each column a non-empty definition;</li>
<li>no definition mentions a source field (<code>CUSTOMER_TIER__C</code>, or an uppercase name in parentheses) or a dbt model (<code>stg_…</code>, <code>fct_…</code>);</li>
<li>each entity, dimension and attribute of the semantic layer has its definition in the dictionary, and an unknown entity is reported along with the closest names.</li>
</ul>

</details>

---

## The Data Portal: Documentation That Is Computed, Never Written

If the definition is attached to the name, a model's documentation no longer needs to be written. **It's a join between its columns and the dictionary.**

On every production deployment, a script generates our data portal:

1. `dbt compile` produces the manifest, which contains every model's compiled SQL;
2. sqlglot parses that SQL and extracts the columns of the final `select`, even behind a `select * from final`, by unrolling the CTEs down to their aliases;
3. each name is looked up in the dictionary.

From this, the portal builds:

* **one page per model**, with its columns, their definitions and tests, a data preview, the lineage, downstream usages and the SQL. An "Ask AI" box turns a question into a SQL query: the LLM receives the table's columns *with their definitions*, so the dictionary becomes the context for text-to-SQL;
* **a dictionary page**, which lays out every definition grouped by business entity, with each entity's dimensions, facts and metrics. Every column links to the marts that carry it. It's an inverted index that answers "where do I find an order's amount including tax?" without reading a line of SQL — and the business glossary we never had to buy or keep in sync.

Finally, the same script lists, model by model, the columns that have no definition — except in the exposure layer, whose columns follow the interface contract of the tools it feeds.

<details>
<summary><strong>Going further: extracting a model's columns with sqlglot</strong></summary>

<p>The core of the extraction fits in a few lines:</p>

<pre><code class="language-python">import sqlglot
import sqlglot.expressions
import sqlglot.optimizer.qualify_columns
import sqlglot.schema


def output_columns(compiled_sql: str, dictionary: dict[str, str]) -&gt; list[dict]:
    """The columns of a compiled model's final select, with their definition."""
    tree = sqlglot.parse_one(compiled_sql, read="snowflake")
    # Expands `select *` over CTEs: `select * from final` yields the aliases of `final`.
    tree = sqlglot.optimizer.qualify_columns.qualify_columns(
        tree, schema=sqlglot.schema.MappingSchema(), dialect="snowflake"
    )
    select = tree.find(sqlglot.expressions.Select)
    columns = []
    for expression in select.expressions:
        if isinstance(expression, sqlglot.expressions.Star):
            continue  # a `select *` over another model: flagged on the model's page
        name = expression.alias_or_name.lower()
        columns.append({"name": name, "description": dictionary.get(name, "")})
    return columns</code></pre>

<p>A few precautions in production:</p>

<ul>
<li>the SQL comes from the dbt manifest (<code>compiled_code</code>, after <code>dbt compile</code>), stripped of any leftover Jinja;</li>
<li>without a schema, <code>qualify_columns</code> fails on some queries: it's called inside a <code>try</code>, and the unqualified tree is then used as is;</li>
<li>a remaining <code>select *</code> is over another model, whose columns sqlglot doesn't know: the model's page flags it;</li>
<li>if sqlglot can't parse the SQL, a regular-expression fallback picks up the <code>as …</code> aliases.</li>
</ul>

<p>The dictionary, for its part, is flattened into <code>{name: definition}</code>: looking up a column is a plain Python dictionary lookup, and the portal's dictionary page is built by inverting the relationship — for each name, the marts that carry it.</p>

</details>

---

## One Definition, Every Reader

The same dictionary line serves everyone:

```
                   Business dictionary
             (one name, one definition, once)
                            │
      ┌──────────────┬──────┴───────┬──────────────┐
      ▼              ▼              ▼              ▼
 Data portal   Coding agents   MCP server     Text-to-SQL
 (humans)      (CLI)           (assistants)   (Ask AI)
```

* **humans**, in the data portal;
* **coding agents**, through the CLI and its hooks;
* **AI assistants**, through our MCP server: its catalog includes the dictionary description of every entity it serves, and its search tool finds every column's definition there;
* **text-to-SQL** in the portal.

Fixing a definition fixes it for all its readers, at the next deployment. There's no second copy to forget.

---

## What This Changes

* **Agents that search instead of guessing.** Before creating a column, the agent searches for the existing name, and finds it. Reuse becomes the default path, because the CLI makes what already exists visible and refuses duplicates. Whole classes of agent errors disappear: invented synonyms, joins between two different concepts, booleans encoded as `'Y'` and `'N'`.
* **No drifting copies, almost no maintenance.** A definition changes in one line, in one place. No `doc()` blocks, no propagation tool, no fifteen YAML files to realign. Renaming a column is a single command, which tells you which models still reference the old name.
* **A business review rather than a SQL review.** In a business contributor's Pull Request, the dictionary diff is the business summary of the change: which new concepts, defined how. The reviewer reads three lines of definitions before three hundred lines of SQL, and the machine has already checked format, uniqueness and consistency. Reviewers can focus on the one question the machine can't settle: is this really a new concept? When [review becomes the critical path](https://unytics.io/blog/nobody-codes-by-hand/), that's a direct gain in throughput.
* **Business teams that contribute without learning the conventions.** A financial controller vibe-coding a model doesn't need to know our naming rules: the agent applies them, and the tooling enforces them. It's one of the conditions that let some twenty business contributors work on the platform without weighing down the review.
* **Joins you can guess.** Same name, same concept, same type, same format: a join on `id_product` between two marts is always valid, and an identifier's suffix says how far it has been unified.
* **AI-ready context.** The MCP server and text-to-SQL read the same definitions as humans do. When an assistant hesitates between two columns, the definition settles it, and it's the same for everyone.
* **A vocabulary we own.** The dictionary is a YAML file versioned in our repository, not a database inside a vendor's tool. Like the rest of our business logic, it [survives a change of tools](https://unytics.io/blog/optic-2000-independence/).

---

## Key Takeaways

Documenting a model describes a table. Documenting a name builds a vocabulary, shared by every model, every team and every agent.

With coding agents, naming stops being a matter of style and becomes an interface: names are how an agent understands the data, and how it gets the data wrong. We treated a name and its definition as a key and its value, written once. Everything else — portal pages, agent context, business glossary — is computed from them.

Ask yourself this about your own platform: **how many places do you have to edit to change a column's definition?** If the answer is more than one, drift is only a matter of time.

---

*Want to make your data platform readable by your teams and your AI agents alike? [Let's talk about it in a 30-minute data chat](https://unytics.io/book-meeting/).*
