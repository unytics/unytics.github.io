# What if your business teams built the data platform?

**Forward Data Conference · 16 November 2026 · 25 minutes · Paul Marcombes**

English version of the talk script: 44 slides, 2,893 words to say. It is the same text as the speaker notes of the English deck, slide by slide. The talk itself is given in French: the French script (`src/blog/fr/forward-data-conference-2026/contenu.md`) is the reference.

## How to use it

- **[click]**: bring in the next element of the slide. The progressive builds exist in the HTML version; in the Google Slides backup, everything is shown at once.
- The timestamps (`m:ss`) show when you reach each slide. They assume 140 words per minute, two seconds per slide change and a second and a half per click: **23:21 in total**. At 125 words per minute, count 25:50; at 155, 21:21.

## The storyline

1. Everyone wants conversational AI to **consume** data. But an AI only answers correctly if the context is prepared and maintained: the data team remains the bottleneck.
2. At Optic 2000, conversational AI sits **at the start of the chain**, in the code editor: the people who analyse build the platform at the same time.
3. The result: from 4 to 25 contributors, most of them business users, and applications the data team would never have imagined.
4. It doesn’t turn into chaos, because contributing is boring (one repo, one way to do things) and the platform learns from every review.
5. Conversational AI for those who consume remains essential, for the stores. And business teams arriving in code repos is a trend bigger than our case: only what gets built changes.

The line to remember: **the village of analysts already exists: it’s your business teams.**

The question to leave with the room: *in your company, who could become a builder tomorrow?*

## Outline and timing

| Part | Slides | Start | Duration | Words |
| --- | --- | --- | --- | --- |
| 0 · Opening | 1 | 0:00 | 0:35 | 78 |
| 1 · The conversational paradox | 2–8 | 0:35 | 3:53 | 480 |
| 2 · The end of silos | 9–12 | 4:29 | 2:13 | 281 |
| 3 · Business users become builders | 13–18 | 6:42 | 3:05 | 379 |
| 4 · Beyond the dashboard | 19–21 | 9:46 | 1:57 | 248 |
| 5 · The anti-chaos architecture | 22–28 | 11:43 | 3:41 | 465 |
| 6 · The learning platform | 29–34 | 15:24 | 2:56 | 347 |
| 7 · Builders and consumers | 35–39 | 18:20 | 2:49 | 346 |
| 8 · The human shift | 40–44 | 21:09 | 2:13 | 269 |
| **Total** | **1–44** | | **23:21** | **2,893** |

## Script

### Opening

#### Slide 1 · Title · `0:00`

*On screen: The talk title, your name, your roles. On the right, 25 dots: the “village” that comes back later.*

Hello everyone. My name is Paul Marcombes. I spent six years building data at Nickel, where the team grew from three to more than forty people. And since January, I have been Head of Data Platform at Optic 2000, as a freelancer. In ten months, we rebuilt the entire data platform there. And I’d like to tell you what surprised us most along the way: the people building this platform today are not the ones you would expect.

### Part 1 · The conversational paradox

#### Slide 2 · Everyone wants to talk to their data · `0:35`

*On screen: A chat exchange: a business user’s question, then the answer with a mini chart.*

Today, if you talk to your executives or your business leaders, the request is unanimous: everyone wants conversational analytics. **[click]** We are sold the dream of an interface where any employee asks a question of their data, in natural language, **[click]** and instantly gets a relevant analysis. And that dream is becoming real: we are seeing great examples of it right here, today.

#### Slide 3 · Under the hood, context makes the answer · `1:07`

*On screen: Three figures appearing one by one (21%, 95%, 65%), then the “village of analysts” quote.*

But we are among data teams here: we know what’s under the hood. Anthropic’s data team told the story very well in June. **[click]** Plugged straight into their warehouse, Claude gets 21% of answers right. **[click]** With a senior team curating the context — reference tables, semantic layer, skills, tests — they climb to over 95%. **[click]** And a month later, without maintenance, they fall back to 65%. Context isn’t prepared once: it has to be maintained. **[click]** Some drew a conclusion from it: to make self-service work, you need a whole village of analysts. Keep that image in mind, I’ll come back to it.

#### Slide 4 · Mid-analysis, a piece of data is missing · `1:57`

*On screen: Two cards: “Hack it on your own”, then “Open a ticket and wait”.*

In practice, a business user is in the middle of an analysis, and a piece of data is missing: a column, a table, a measure. They have two options. **[click]** Either they hack it on their own, with an export and an Excel file. That’s shadow data: what they learned never makes it back into the platform. **[click]** Or they open a ticket, and wait for the data team to prepare the data. We used to open a ticket to get a dashboard. Now we open a ticket to get a column in the semantic layer. That’s ticketing 2.0: the data team is still the bottleneck.

#### Slide 5 · At Optic 2000, everything changes at once · `2:47`

*On screen: “10 months”, “6 → 4”, and the list of five projects.*

At Optic 2000, we had an extra problem this year: everything was changing at once. In ten months, we replaced the legacy PostgreSQL stack, absorbed a new point of sale, a new CRM, a new loyalty program, and switched off our BI tool. All with a platform team that went from six to four people. Needless to say, our BI team didn’t have a minute to take on new business topics. We had hit a bandwidth wall.

#### Slide 6 · The market puts conversation at the end · `3:22`

*On screen: The chain Sources → Transformations → Semantic layer → Applications. The “Conversational AI” bubble sits above the last block.*

Faced with that wall, we went against the market. Look at a classic data platform: sources, transformations, a semantic layer, applications. The data team prepares, business teams consume. And the market plugs conversational AI at the very end of the chain, in a consumption interface.

#### Slide 7 · We put it at the start · `3:43`

*On screen: The bubble stretches across the whole chain (animated transition), then “Analysis builds the platform.”*

We put it at the very start: directly in the code editor, where the platform is built. Why? So that the moment a business user starts an analysis, the AI helps them prepare and enrich the data, at the source, in the platform. That’s the third option: neither hacking nor waiting. Building. **[click]** Analysis builds the platform.

#### Slide 8 · Agenda · `4:10`

*On screen: Three columns: what happened, why it holds, what we take away.*

Here is how we got there. First, what happened: our BI team, then business teams, then applications we didn’t expect. Then, why it all holds together without turning into chaos. And finally, what we take away from it.

### Part 2 · The end of silos

#### Slide 9 · “Letting non-developers code in the repo?” · `4:29`

*On screen: Dark slide: the sceptic’s question.*

I can see you smiling. Letting non-developers code in the central data platform repo? I was very sceptical myself at the start. So we went step by step. And we started with the team closest to us: our own BI team.

#### Slide 10 · Before: three teams, three silos · `4:48`

*On screen: Three cards: 4 Data Engineers, 2 BI Engineers, 4 BI.*

Historically, data at Optic 2000 meant three watertight teams. Four data engineers, who handled ingestion and transformations, in PostgreSQL stored procedures. Two BI engineers, who managed the semantic layer in MicroStrategy. And four people in BI, who built dashboards with point-and-click. That BI team could read a bit of SQL. But they had never touched Git, Python or dbt.

#### Slide 11 · The test: talk instead of click · `5:15`

*On screen: Top: point-and-click Tableau → vibe-coded Streamlit apps. Bottom: three results appearing one by one.*

When it left MicroStrategy, Optic 2000 first chose Tableau. And the BI team spent a phenomenal amount of time on it, on repetitive, tedious point-and-click tasks. We offered them a test: build their dashboards as Streamlit applications, by vibe-coding in our repo, with AI. They were sceptical themselves: will it be clean? Will the numbers be right? Will we be able to maintain it? **[click]** Within a few weeks, the shift was spectacular: they became autonomous. **[click]** The end-user experience is ten times better, for a fraction of the time we used to spend on Tableau. **[click]** And above all, they didn’t stop at Streamlit: on their own, they started creating and maintaining their own dbt models.

#### Slide 12 · Today: two teams instead of three · `6:11`

*On screen: The middle card is gone: BI covers the whole chain. Bottom line: Streamlit and the stores.*

Today, we have moved to two teams: four data engineers, four in BI, and no intermediate layer anymore. BI owns the whole chain, from the dbt model to the application. And Streamlit has become our dashboarding tool, including for thousands of users in stores. The data engineers set the frame and coach the people who build. Remember this shift: we’ll see it again, on a larger scale.

### Part 3 · Business users become builders

#### Slide 13 · Why stop at the BI team? · `6:42`

*On screen: Dark slide: the question.*

When we saw our BI team create flawless mart models, with no software background to begin with, we asked ourselves: why stop there?

#### Slide 14 · We went to the business teams at headquarters · `6:53`

*On screen: Five business functions as tags, then two sentences.*

We went to the business teams at headquarters. Business project managers. Management control. Finance. Accounting. Digital marketing. **[click]** Analytical profiles, used to tracking their numbers. But who had never written a line of code.

#### Slide 15 · The barrier to entry is close to zero · `7:11`

*On screen: Three struck-through lines, “They converse.”, then a business project manager’s conversation with the agent.*

And here, we need to bust a myth: today, the barrier to entry for contributing to a repo is close to zero. These people don’t write code. They don’t even read the code. And they don’t type a single Git command. **[click]** They simply converse with Claude: in VS Code, or directly in Claude Desktop. **[click]** An example. A business project manager, who knows SAP and works with logistics, brought data from SAP into Snowflake, cleaned it up following our conventions, and built an operational dashboard tracking the logistics teams’ KPIs. In a single conversation. The agent handled Git, the branches and the code. And at the end of the conversation, the platform was richer.

#### Slide 16 · It all starts with a small topic · `8:04`

*On screen: On the left the sentence, on the right a mock-up of a tracking app.*

It all started with small side topics. A project manager built herself an app to track her Jira tickets, to better steer her projects. Nothing strategic. But that’s how trust builds up: hers, and ours.

#### Slide 17 · Then the topics become critical · `8:21`

*On screen: On the left, before and today. On the right, his cockpit: two overlapping date bars.*

Then trust set in, and complexity jumped. Example: the owner of the store master data, in Salesforce. Stores change all the time, with acquisitions and openings. Before, we were the ones writing dbt tests on this master data. When a test failed, we let him know, and he fixed it after the fact. **[click]** Today, he has built his own cockpit, far more detailed than our tests. For example, when a store is taken over, the opening dates of the old and the new owner must not overlap. He sees the inconsistencies, and he can be proactive. He is the one who knows these business rules. Not us.

#### Slide 18 · From 4 to 25 contributors in ten months · `9:11`

*On screen: “4 → 25”, then three rows of dots: platform, BI, business teams.*

The result: in ten months, the number of people contributing to our data repo went from 4 to 25. **[click]** Four in the platform team. **[click]** Four in BI. **[click]** And all the others are business users. None of these twenty-five people codes by hand. Remember the village of analysts you supposedly need to make self-service work? Here it is. Except we didn’t hire it: it was already in the company.

### Part 4 · Beyond the dashboard

#### Slide 19 · More contributors means more ideas · `9:46`

*On screen: Dark slide: the sentence alone.*

And by multiplying the number of contributors, we don’t just save time. Ideas emerge that we had absolutely not anticipated. At first, we thought Streamlit would only be used to display charts on top of Snowflake. Business teams proved us wrong. I see two trends.

#### Slide 20 · First trend: replacing SaaS tools · `10:08`

*On screen: Two cards: geomarketing, then tax returns.*

The first is replacing SaaS tools. In geomarketing, we paid for a rather rigid proprietary tool to visualise catchment and franchise areas on the map of France. The person in charge rebuilt the whole tool in Streamlit. It finally meets 100% of her needs, and we drop a costly license. **[click]** Same for the stores’ tax returns. Instead of re-entering them by hand every year, or paying a lot for OCR software, we have an automatic recognition app, with a human in the loop to validate. With exactly the same quality.

#### Slide 21 · Second trend: elevating the back-ends · `10:50`

*On screen: Yesterday: SAP → Excel → re-entry. Today: SAP ↔ Streamlit front-end ↔ business user. Then the closing line.*

The second trend is even more strategic: elevating our back-ends. We have no desire to replace SAP or Salesforce: they are robust, standard back-ends. Their interfaces, however, are unfriendly. Optic 2000 was founded in 1969, and we still have a huge number of manual processes, especially on top of SAP: Excel exports, then hours of repetitive manipulation, with a real risk of error. **[click]** Today, our business users build user-friendly Streamlit front-ends, connected directly to SAP and Salesforce, and tailored to their processes. We are only at the beginning. But it’s the use we least imagined, and maybe the one that will change the game the most. **[click]** A dashboard shows. A data app acts.

### Part 5 · The anti-chaos architecture

#### Slide 22 · “Great on paper. But…” · `11:43`

*On screen: Dark slide: the room’s objection.*

At this point, I know what half of the room is thinking. “Great on paper. But letting twenty or thirty business users code in the data platform will create a plate of spaghetti nobody can maintain. And we’ll spend more time reviewing their code than writing it ourselves.” You are right to ask: it’s exactly the question I was asking myself. Here is how we avoid chaos.

#### Slide 23 · First pillar: a single repo · `12:14`

*On screen: A large “Git mono-repo” frame holding the four blocks, then the line “one conversation, one pull request”.*

First pillar: the mono-repo. Our entire platform — ingestion, dbt transformations, the semantic layer, Streamlit applications — lives in one single Git repository. If our tools were scattered, no agent could understand the context end to end. **[click]** Here, while a business user analyses data, the AI can trace back to the source, enrich the transformation, add the measure and build the screen. In the same move. In the same pull request.

#### Slide 24 · Second pillar: boring contributions · `12:47`

*On screen: Two cards: configuration (light), plumbing (dark). Then the bottom line.*

Second pillar: making the code as simple, as dumb, as boring as possible. We radically separate two things. Configuration, which says what the business needs. And plumbing — deployment, security, monitoring — which is written once, by the platform team. You all know a tool that does this: dbt. You write a SQL model, and dbt handles incremental loading and execution order for you. Well, in our repo, we built everything that way. **[click]** And what a contribution cannot express, a reviewer doesn’t have to check.

#### Slide 25 · A function: three lines of configuration · `13:26`

*On screen: The function’s YAML (timeout: 600) → “AWS Lambda”.*

An example. To create a function, a contributor writes a Python script, under a decorator, and three lines of configuration: the schedule, the timeout, the memory. That’s it. Here, the timeout is ten minutes: the platform deploys the function as a Lambda.

#### Slide 26 · A function: three lines of configuration (continued) · `13:46`

*On screen: Same slide: the timeout becomes 3600, the target becomes “ECS Fargate” (animated transition). Then the question to the room.*

If the timeout goes beyond fifteen minutes, it deploys it as a Fargate task. Same script, same decorator. The contributor doesn’t even need to know. There is no “backend” field: what you can’t declare, you can’t declare wrong. **[click]** Ask yourself about your own platform: when someone adds a source or a job, how many lines of plumbing do they write?

#### Slide 27 · One way to do each thing · `14:15`

*On screen: Dark slide: the sentence alone.*

This boredom has a direct effect on AI. In a repo where every pipeline is written differently, an agent has to guess: it invents, it mixes conventions. In a repo where there is only one way to do each thing, it just copies the right pattern. In our repo, the thirtieth source looks exactly like the twenty-ninth. The agent copies the previous one. And it’s right to.

#### Slide 28 · In the apps, AI assembles building blocks · `14:46`

*On screen: On the left, an app made of blocks (cards, chart, table). On the right, two cards appearing.*

Same logic in the applications. **[click]** The BI team built a library of standard components itself — KPI cards, tables, charts — and our skills require the AI to use them. **[click]** As for the numbers, the store-facing applications rely 100% on the semantic layer: the logic of the measures is defined in one place, and the application just calls and displays them. The result: consistent applications, the same numbers everywhere, and an AI that invents nothing. It assembles building blocks.

### Part 6 · The learning platform

#### Slide 29 · It also has to hold up over time · `15:24`

*On screen: Dark slide: the sentence alone.*

Avoiding chaos on day one is one thing. But it also has to hold up over time.

#### Slide 30 · Two dangers remain: drift and review · `15:33`

*On screen: Two cards: drift, then review.*

Two real dangers lurk. The first is drift: as soon as the same thing is described in several places, the versions end up diverging, and the AI follows the wrong one. **[click]** The second is review. Four people can’t review everything that twenty-five contributors and their agents produce. If we’re not careful, we have just moved the bottleneck, from tickets to pull requests.

#### Slide 31 · Three names for one concept · `16:03`

*On screen: Three column names, three dbt models, three descriptions.*

Against drift, we have strict engineering rules. Look at what a typical dbt project produces: “email” in staging, “email_client” in the dimension, “customer_email” in the export. Three names, three descriptions, for one single concept. Which one is right? And which one will the agent copy into the fourth model?

#### Slide 32 · One concept, one name, one definition · `16:26`

*On screen: Only one name is left (animated transition) with its definition. Then three figures: 1,800, 350, 0.*

In our platform, the rule is strict: a business concept has only one column name across the whole warehouse, and a name refers to only one concept. As a result, we no longer document dbt models one by one: we document names, once, in a single dictionary. **[click]** 1,800 column names, 350 dbt models, and not a single column description in dbt.

#### Slide 33 · The machine checks before the reviewer · `16:56`

*On screen: Four steps appearing one by one, then the final question.*

Next, review. The machine checks before the reviewer. As soon as a dbt model changes, a check verifies that every column is declared in the dictionary. **[click]** Then our skills prepare the pull request: they tick the compliance checklist before the code is even pushed. **[click]** A reviewer agent reviews the work, before the pull request is opened. **[click]** It arrives already reviewed, assigned to the business owners of the domains or metrics that changed. **[click]** What’s left for the human is the one question no machine can settle: is this the right thing to build?

#### Slide 34 · Every review comment becomes a rule · `17:43`

*On screen: A four-step loop, built click by click.*

And here is our golden rule. Every time an engineer writes a comment on a pull request, **[click]** they must ask themselves: why did the AI let this through? **[click]** And update the skill, immediately. **[click]** The comment doesn’t only fix this pull request: it fixes all the next ones. **[click]** Thanks to this loop, the platform learns from every review. And our pull requests become almost instant to approve.

### Part 7 · Builders and consumers

#### Slide 35 · Should everyone be in VS Code? · `18:20`

*On screen: Dark slide: the question, then the answer on click.*

Does all this mean we should throw away classic conversational analytics, and put everyone in VS Code? **[click]** Absolutely not. The proof: we do both.

#### Slide 36 · Two populations, two faces of AI · `18:34`

*On screen: Two cards: at headquarters (they build), then in stores (they consume).*

We need to distinguish two populations. At headquarters, analytical profiles use AI to build lasting assets, in the repo. **[click]** But an optician, in one of our stores, will never open a code editor. It would make no sense. They need to be served like a customer.

#### Slide 37 · In stores, AI is consumed in two ways · `18:57`

*On screen: Two cards linked to a “Semantic layer” bar.*

For stores, AI comes in two forms. First, specialised agents, embedded in their applications. For example, a store manager looks at the store’s financial statement, and talks it through with an agent that is an expert in optical retail finance: they compare themselves with similar stores, bring in their local context, and get recommendations. **[click]** Second, the same expertise is exposed through an MCP server and skills: stores can query their data from their own Claude or their own ChatGPT. **[click]** In both cases, the numbers come from the same semantic layer, and everyone sees only their own data.

#### Slide 38 · We moved the boundary · `19:43`

*On screen: Two rows Platformers / Builders / Consumers: the orange bar (the boundary) moves. Then the closing line.*

To sum up. In a data organisation, there are three roles: those who build the platform, those who build on top of it, and those who consume. In the usual model, the boundary runs between the data team, which builds, and business teams, which consume. **[click]** We moved that boundary. The platform team builds the frame. And among those who build on top of it, there are now more business users than data people. **[click]** Our conviction: put as many people as possible on the builders’ side. A central team will never hold all of the company’s knowledge. Business teams are the ones who know their data and their processes.

#### Slide 39 · A trend bigger than our case · `20:35`

*On screen: Two cards: what is taking hold (business teams in code repos), then what changes from one company to the next.*

This isn’t specific to a company like ours. Business users who have never written code are arriving in code repos. They open a ticket from Slack, and an agent codes it. They open a pull request in another team’s repo. Or they create their own repo. **[click]** Digital natives too: at Supabase, marketing opens pull requests in the data repo. Only what gets built changes: for us, processes that are still manual.

### Part 8 · The human shift

#### Slide 40 · To conclude, two messages · `21:09`

*On screen: Dark slide: the sentence alone.*

To conclude, I’d like to share two messages with you.

#### Slide 41 · First message: start small, and iterate · `21:15`

*On screen: A four-step staircase, built click by click.*

The first: start small, and iterate. Don’t open your Git repo to a hundred business users on Monday morning. We started with our BI team. **[click]** Then a project manager, on a low-stakes topic. **[click]** Every guardrail I told you about was built step by step, with the first successes, and the first failures. **[click]** And we ourselves are at the beginning of the story on some topics, like the SAP front-ends: the coming months are about turning the attempt into a success.

#### Slide 42 · Second message: the key is human · `21:56`

*On screen: “1 in 4”, four dots, one of them blue. Then the card about the BI team.*

The second: the key isn’t technology, it’s people. Of our four data engineers, one works full time onboarding and coaching business users. **[click]** And our BI team’s job is changing. Freed from ticketing and point-and-click, it is becoming proactive. Often, business teams don’t just need one more number: they need an outside view to rethink the way they work. And in our case, the job is huge: it’s on this platform that the BI team will help transform all those processes that are still manual.

#### Slide 43 · The village of analysts already exists: it’s your business teams · `22:35`

*On screen: Blue slide: the key sentence, then the question to take home.*

People say you need a whole village of analysts to make self-service work. I believe that village already exists, in each of your companies: it’s your business teams. So keep conversational AI for those who consume. **[click]** But when you get back, ask yourself one question: in your company, who could become a builder tomorrow? Today, our data team no longer builds simple dashboards. It co-builds the operational transformation of the company.

#### Slide 44 · Thank you · `23:09`

*On screen: Thank you, your contact details, the QR code to LinkedIn, the four articles.*

Thank you very much. Everything I told you is detailed in four articles, on the Unytics blog. And I’m happy to take your questions.

## If you run over

In order of preference:

1. **Slide 16, “It all starts with a small topic”**: can be skipped (saves 0:17). Then say “it all started with small side topics” when you reach slide 17.
2. **Slide 28, “building blocks”**: can be skipped (saves 0:38). The semantic layer comes back on slide 37.
3. **Slide 20**: keep only one of the two examples.
4. **Slide 8, the agenda**: go through it in one sentence.

Do not cut: slides 6 and 7 (the reversal), 18 (the village), 22 (the objection), 34 (the golden rule), 39 (a trend bigger than our case) and 43 (the message).

## Likely questions

**“Doesn’t pull request review become the new bottleneck?”**

Yes, it’s our critical path. Three answers. Contributions are configuration: there is no plumbing to review. The machine checks before the human: checks on write, CI, then a reviewer agent that returns a “merge” or “no merge” verdict before the pull request is even opened. And every comment becomes a rule: the same remark doesn’t come back. Every pull request is still approved by a human.

**“How does a business user validate code they don’t read?”**

They don’t validate the code, they validate its result: their numbers, their app. The dictionary diff is the summary of the change: three lines of definitions before three hundred lines of SQL. Before the pull request is even opened, the reviewer agent’s verdict speaks to them in plain language. Then the pull request builds its models in a separate schema, comparable with production.

**“Do your apps write to SAP?”**

Not yet: today, they read. That’s the next step, and it will need guardrails to match: tests, permissions, human validation.

**“Isn’t this only possible with a mono-repo?”**

Our setup is specific: everything is in one repo, and that’s what lets an agent connect everything. You can start with the dbt repo, then bring the rest into it. And the trend goes beyond our case: see slide 39.
