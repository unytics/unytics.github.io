---
title: "The Platform That Learns: Every Review Comment Becomes a Rule"
description: "At Optic 2000, four people can't review everything 25 contributors and their agents produce. Review holds because a correction is only made once — it becomes a rule — and because a Pull Request arrives already reviewed by an agent before a human opens it."
date: 2026-11-13
---

# The Platform That Learns: Every Review Comment Becomes a Rule

In [Nobody Codes by Hand](https://unytics.io/blog/nobody-codes-by-hand/), I told how 25 people, most of them business people, contribute to Optic 2000's data platform through a coding agent. The consequence is immediate: **review becomes the critical path**. Four people can't review everything that twenty-five contributors and their agents produce.

[Boringly Simple](https://unytics.io/blog/boringly-simple-data-platform/) gives the first half of the answer: a contribution only expresses configuration, so there is little left to review. Here is the second half, for what is left — SQL, Python, data apps: **a correction is only made once**, and a Pull Request reaches us already reviewed.

---

## A Correction Is Only Made Once

A rule is added to the platform in three situations.

1. **The agent doesn't get it right the first time**, and we have to explain. The explanation doesn't stay in the conversation: the agent writes it into the right instructions file, with its reason, before going on.
2. **We have to comment on a Pull Request.** Before fixing it, we ask ourselves why the AI let it through, and we update the skill, immediately. The comment becomes a rule.
3. **Something reached production that should have been blocked**, or that failed. The incident becomes a rule, or a check run by the machine.

In all three cases, the correction doesn't just fix the case at hand: it fixes all the next ones. That's how our Pull Requests become almost instant to approve.

The rule still has to reach the agent at the moment it acts. So it's written where the agent works: in an instructions file next to the code it governs, or in the skill the agent loads before that kind of task.

<details>
<summary><strong>Going further: where our rules live</strong></summary>

<ul>
<li><strong>Instructions next to the code they govern.</strong> A root instructions file (<code>CLAUDE.md</code>, for Claude Code) describes the platform and its non-negotiable rules. Each main folder — ingestion, functions, infrastructure, web apps — has its own, which the agent loads when it works there. Rules for a type of file — YAML, Terraform, Python, Markdown — load only when the agent touches such a file. The agent's context holds the rules of what it's doing, not the whole rulebook.</li>
<li><strong>A skill for each kind of task.</strong> Before touching a dbt model, the agent loads the dbt skill: layers, naming, tests, SQL style, and an exit gate before it hands back. Same for data apps and for the style guide.</li>
</ul>

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

---

## Seven Rules This Loop Gave Us

* **Never break what someone still uses.** Before stopping a source or deleting a table, find out who uses it — a model, a data app, an export — switch them over, then delete.
* **A shared business rule lives in the semantic layer, not in a data app.** A data app can do clever things, but a definition others need belongs to the shared metrics engine. A store-facing data app coded its own rule for recognizing connected glasses: stores that asked their AI the same question, through our MCP server, got different figures. Since then, those data apps only read the semantic layer, and recode no business rule.
* **A Pull Request does one thing.** A mistake spotted along the way is fixed separately. Otherwise, the reviewer of a new table unknowingly approves a change to existing figures.
* **Every metric, every domain, every data app has an owner.** A metric had been merged without the BI team validating it. The Pull Request is now assigned automatically to whoever answers for what it changes.
* **An aggregate matches the total of its fact table.** Null values had skewed a total. The skill now requires that check, and highlights any gap.
* **A certified figure from the past no longer moves.** One had changed. Certified measures are now checked on past data.
* **A data app isn't built twice.** It happened. The skill now checks that it doesn't already exist.

None of these shows up in a SQL diff: that's why they're written where the agent works.

---

## A Pull Request Arrives Already Reviewed

These rules apply before a human looks at anything.

**While the agent writes**, checks run: when it edits the business dictionary or the semantic layer, a hook sends any violation back to it, and it fixes it in the same session. I detail this in [One Name, One Definition](https://unytics.io/blog/one-name-one-definition/).

**Before the Pull Request is opened**, the contributor runs a single command. The publishing skill goes through the compliance checklist, then has the work reviewed by a review agent: one for dbt models, one for data apps. The rule files are its checklist, and it reports only what blocks — whatever changes a figure, a grain or a column name, crashes in production, touches access rights, or duplicates an existing data app. Style never blocks. And if a check can't run, the verdict is never "merge".

The verdict is addressed to the contributor, in plain language, before any technical detail (figures made up):

```
MERGE: NO, the "active stores" card shows 120 stores where the definition gives 100.

1. Duplicate: no.
2. Against our practices or a business rule: yes, 1 point:
   - the card counts every store with a sale; the definition counts stores open over the period.
3. Reinvents the wheel: partly — the cards are drawn by hand instead of using the style guide.
4. Merge: NO.
```

**Only then is the Pull Request opened.** The skill writes its description — including what a reviewer must not miss, such as a data source being stopped — and assigns it to the owners of what it changes.

The order matters. We could have plugged the review agent in after the Pull Request is opened, to comment on it. The human reviewer would then discover work that is still rough, under a pile of automated comments. Here, when they open a Pull Request, most of it is already clean.

---

## What's Left for Humans

**The contributor validates a result, not code.** Our business contributors don't read the code their agent writes. They validate what they know: their figures, their data app. The verdict speaks to them in plain language, and the business dictionary diff sums up the change: three lines of definitions are read before three hundred lines of SQL.

**The reviewer answers one question.** Every Pull Request is still approved by a person, and every owner answers for their domain. But the conventions have already been checked. What's left is the question no machine can settle: **is this the right thing to build?**

---

## What It Costs

* **Rules need gardening.** Instructions grow with every correction. Keeping each rule in one place, with its reason and without stale examples, is a job in itself.
* **The loop takes discipline.** Fixing the Pull Request is quicker than fixing the skill. Anthropic's data team reports that [roughly 90% of its data-model Pull Requests](https://claude.com/blog/how-anthropic-enables-self-service-data-analytics-with-claude) now include a skill change in the same diff: that's the price of a context that doesn't go stale.

---

## Key Takeaways

With agents writing the code, review capacity doesn't grow by adding reviewers. It grows when a correction is only made once, and when a Pull Request arrives already reviewed. What's left for the reviewer is the only question that matters.

Ask yourself the question about your own team: **of this week's review comments, how many had you already written before?** Each one is a rule waiting to be written.

*This article details one part of a larger story: [Why Your Business Teams Shouldn't Just Be AI Consumers (But Builders Too)](https://unytics.io/blog/self-service-analytics-builders/).*

---

*Is review becoming the bottleneck for your coding agents? [Let's talk about it in a 30-minute data chat](https://unytics.io/book-meeting/).*
