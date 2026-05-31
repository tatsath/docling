> *The AI Operating Manual for Investment Firms* — Essay 01

# The Last Mile of AI in Investment Management

### Almost every fund and advisory firm now has the tools. Very few have changed how the work actually gets done. The gap between those two facts is where the next decade of advantage will be won — and it is not a software problem.

*By [YOUR NAME] · [DATE] · ~12 min read*

---

Spend a week talking to portfolio managers, RIA principals, and private-credit teams about artificial intelligence and you stop hearing the question that dominated 2023. Almost nobody asks *whether* generative AI matters anymore. The numbers settled that argument. In its 2025 research, the Alternative Investment Management Association found that 95% of fund-manager respondents now use generative AI in their work, up from 86% a year earlier.[^aima] Charles Schwab's January 2026 study put adoption among registered investment advisers at 63%, more than double the level of 2023.[^schwab] At Balyasny Asset Management, roughly 95% of the firm's investment teams actively use its internal AI research platform.[^balyasny]

So the tools are everywhere. And yet, if you sit with the people inside these firms, a quieter and more uncomfortable question keeps surfacing:

**What, exactly, changed in our daily workflow?**

That question is the whole subject of this essay, and of everything I plan to write here. The frontier of AI in investment management is no longer the model. It is the last mile — the distance between a capable system sitting on a screen and a repeatable, reviewed, evidence-backed process that a firm can stand behind in front of an investor, a client, a compliance officer, or an examiner.

Most firms have not crossed that last mile. The interesting part is that the companies *selling* the tools now admit it openly.

---

## Usage Is Not Adoption

Start with the cleanest piece of evidence, because it reframes everything. In the same Schwab study that reported 63% adoption, only about one in ten advisers who use AI said they had fully integrated it into their business strategy.[^schwab] Read those two figures together and the picture sharpens: a large majority are *using* AI, and a small minority have *adopted* it.

Those are not the same thing, and conflating them is the single most expensive mistake a firm can make right now.

**Usage** means a person opened a tool and got a useful output.

**Adoption** means a workflow changed — permanently, for everyone on the desk, in a way the firm can describe, measure, and defend. Adoption means the firm knows which use cases are approved and which are prohibited, which documents may be fed to a model and which may not, who reviews the output before it leaves the building, where that output is stored, what evidence supports each claim in it, and how anyone would know whether the new process is actually better than the old one.

Without that operating layer, generative AI inside a firm is a collection of impressive but fragile experiments. One analyst uses it carefully, with citations. Another pastes a confidential deal memo into a consumer chatbot. One adviser uses it to clean up grammar. Another drafts a client-facing performance explanation that no one reviews. A senior partner watches a good demo and concludes the firm "is using AI." All of that is real usage. None of it is adoption.

> **🔧 PROOF SLOT — replace before publishing.** *Drop in one concrete, anonymized example you have lived through: a firm where three analysts were each using AI in three incompatible ways, or a moment where a polished AI output turned out to be subtly wrong. One real anecdote here does more for your credibility than the next three paragraphs of argument. If you don't have one yet, cut this block — never invent it.*

> **[Figure 1 — "Usage vs. Adoption"]**
>
> A simple two-column or before/after diagram.
> - **Left:** scattered, unconnected tool icons labelled "usage" (one analyst, one prompt, no review, no record)
> - **Right:** a single connected pipeline labelled "adoption" (input rules → workflow → review → evidence → storage → metric)
>
> *Caption: "Most firms are on the left and believe they are on the right."*

---

## The Bottleneck Is Not the Model

Here is the claim that most AI-finance commentary gets wrong. The frontier models are already good enough for an enormous range of useful work. They summarize transcripts, compare documents, draft memos and emails, extract entities, and write code at a level that was science fiction three years ago. If your firm has not changed how it works, the reason is almost never that the model is too weak.

The reason is that in investment management, **a beautiful answer is not a finished one.**

Consider what each desk actually needs, beyond the output itself:

| Role | What they actually need |
|------|------------------------|
| **Hedge fund analyst in earnings season** | What *changed* vs. prior quarter, which specific sentence supports that change, whether the KPI was calculated on the same basis as last time, whether management's language quietly contradicts the existing thesis, and what still requires human judgment before it touches a position |
| **RIA drafting a client email** | Whether the email contains promissory or performance-guaranteeing language, whether it matches the client's documented risk profile and suitability, whether every factual claim about returns is supported by data the firm actually holds, and whether compliance could reconstruct the review trail eighteen months from now |
| **Private-credit team writing a credit memo** | Covenant definitions pulled correctly, thresholds and baskets and EBITDA add-backs identified with their exact source pages, borrower reporting obligations laid out, ratio calculations checked, exceptions flagged — and a hard line between what the model *extracted* and what a credit professional *approved* |

In all three cases the model can produce the first artifact in seconds. And in all three cases, that artifact is worthless — or worse, dangerous — until it has been verified, sourced, reviewed, and recorded. That work is the last mile. It is not glamorous. It is the entire job.

> **Prompts are disposable. Workflows and controls are durable.**

---

## What "Good" Actually Looks Like

The most useful public example we have is Balyasny, because OpenAI documented it in detail in early 2026.[^balyasny] It is worth studying precisely because it is *not* a story about buying a subscription.

What Balyasny built is an operating model. The firm stood up a centralized Applied AI team — roughly twenty researchers, engineers, and domain experts — back in late 2022. Before putting a model into production, it evaluated that model across more than a dozen financial dimensions, including forecasting accuracy, numerical reasoning, and hallucination rates.[^bal2] Its agents are designed around traceable reasoning and testable behavior, with compliance guardrails held centrally while individual desks customize agents for their own asset class.[^balyasny] The results are real: research tasks that took days now take hours, and a "Central Bank Speech Analyst" cut a two-day macro scenario analysis to about thirty minutes.[^balyasny]

Notice what carried that result. Not the model alone — the *system* around it: evaluation, scoping, traceability, guardrails, and a team whose entire job was to embed the technology into how analysts actually work. The model was necessary. It was nowhere near sufficient.

Now notice the catch. Most firms do not have a twenty-person Applied AI team. A multi-strategy fund with billions under management can build that operating layer internally. A solo RIA, a boutique credit shop, or a sub-$1bn fund cannot — and that is precisely the divide the rest of the industry is now organizing around. The largest funds build the operating model themselves. Everyone else needs to acquire it some other way. That gap is real, it is structural, and it is not closed by another subscription.

The clearest signal that the gap is structural is who is rushing to fill it. The labs are no longer just selling models; they are selling *implementation*. In 2026 Anthropic shipped a set of ready-to-run finance agent templates for tasks like pitchbook creation, KYC screening, earnings review, and credit-memo drafting, and — tellingly — its own documentation states the agents produce drafts intended for qualified human review rather than executing anything autonomously.[^anthropic][^anthropic2] Around the same time, Anthropic formed a roughly $1.5bn joint venture with Blackstone, Hellman & Friedman, and Goldman Sachs whose explicit purpose is to embed engineers inside companies that cannot otherwise afford to build AI systems on their own.[^jv] You do not raise that kind of capital to sell software licenses. You raise it because the bottleneck is delivery.

> When the people who make the models tell you the hard part is putting them to work, believe them.

---

## The Operating Model, in Five Layers

If the last mile is the problem, what does crossing it actually require? Strip away the vocabulary and every durable AI workflow in a regulated investment firm has the same five layers. Most firms have built exactly one of them.

| Layer | What it is | Common mistake |
|-------|-----------|----------------|
| **Model** | The frontier system itself — Claude, GPT, Gemini, or an internal model | Obsessing over this; it is largely a commodity you rent |
| **Data** | What you point the model at: filings, transcripts, portfolio/CRM data, research archives, credit agreements, internal memos | Quality and accessibility of this layer dominates results |
| **Workflow** | The repeatable sequence a person follows: input rules, steps, output format | Where "usage" becomes "adoption" — mostly absent in firms that are merely experimenting |
| **Evidence** | Citations, source pages, numerical checks, source coverage, contradiction detection — not "the model said so" but "here is the claim, the line, the math, and what it conflicts with" | Treating a citation as proof rather than a pointer |
| **Control** | Human approval, review status, logging, policy rules, and an audit trail | Skipping this entirely and calling it done |

> **The firms that win will not be the ones with the best model layer. They will be the ones that built the other four.**

> **[Figure 2 — "The five-layer stack"]**
>
> A vertical stack of five labelled bands: Model · Data · Workflow · Evidence · Control.
>
> Annotate the Model band with "rented / commodity / everyone has this" and bracket the top four bands with "the durable advantage." Keep it clean and diagrammatic — this is the visual spine of the whole blog and you will reuse it.
>
> *Caption: "Most firms have built the bottom band and called it an AI strategy."*

---

## Retrieval Is Not Evidence

Of those five layers, the one that quietly breaks the most projects is the evidence layer — and it breaks because of a confusion that sounds harmless: the belief that if a model retrieved a document, it has supported a claim.

It has not. Retrieval finds text. Evidence proves a specific assertion. The distance between the two is where finance lives.

There is now empirical weight behind this. A January 2026 benchmark called FinRetrieval tested AI agents on 500 financial retrieval questions with known answers. The leading configuration reached **90.8% accuracy** when it could pull from a structured financial database — but only **19.8%** when it was limited to general web search. That is a 71 percentage-point swing driven not by the model's intelligence but by what it was allowed to retrieve from.[^finretrieval] Related work points the same direction: state-of-the-art agents remain fragile on realistic, high-difficulty financial search, with recurring weaknesses in temporal reasoning and evidence integration.[^finagent]

Read that the right way. The bottleneck is not the model's reasoning. It is the system around it — the data it can reach and the discipline with which claims are checked against sources. A model that confidently cites the wrong fiscal period, the wrong table, or the wrong defined term has retrieved something and proven nothing.

The fix is to stop treating an AI output as an answer and start treating it as a chain that can be inspected. For every material claim: what is the claim, what source supports it, which page or section, what calculation produced any number in it, and who signed off. That chain — claim to source to calculation to reviewer — is the difference between an AI-assisted memo you can defend and a plausible document you merely hope is right.

> **[Figure 3 — "The evidence chain"]**
>
> A left-to-right flow:
>
> **Claim** → **Source (doc + page)** → **Calculation** → **Reviewer decision**, with a small "rejected / sent back" loop from Reviewer back to Source.
>
> Contrast it visually with a greyed-out box labelled "what most RAG demos actually show: Question → Answer → 🤞"
>
> *Caption: "In finance, the question is never 'did the model find a source?' It is 'does the source prove the claim?'"*

*(This deserves its own essay, and it will get one. For now the point stands: an evidence layer is not a nice-to-have. It is the thing that makes everything above it usable.)*

---

## The Regulatory Reality, Stated Correctly

This is where a lot of AI-finance writing loses its credibility, so let me be precise, because precision here is itself a signal that you actually read the source material.

A common claim is that a sweeping SEC "AI rule" is coming for advisers. It is not. The SEC's 2023 proposal on conflicts of interest in the use of predictive data analytics — the rule everyone meant when they said "the AI rule" — was **formally withdrawn in June 2025**, as part of a withdrawal of fourteen Gensler-era proposals.[^withdraw][^secwithdraw] The Commission stated it does not intend to finalize it and would have to start over with a fresh proposal to act in that area.

If you stop reading there, you draw the wrong conclusion. The withdrawal removed a specific *prescriptive* framework. It removed none of the existing obligations.[^withdraw] An adviser's fiduciary duties of care and loyalty still apply to AI-assisted work. Recordkeeping rules still apply to AI-generated communications. The duty to supervise still applies to AI tools. The principles-based regime did not relax; only the bespoke rulebook went away.

And the supervisory attention is, if anything, sharper for being principles-based. The SEC's examination priorities for fiscal 2026 single out AI directly: examiners will look at whether firms have adequate policies to supervise their use of AI, and — this is the part to underline — they will *review for accuracy the representations firms make about their AI capabilities.*[^secpriorities][^secpriorities2] In plain terms, the regulator is now policing the gap between what a firm claims its AI does and what it actually does. That is AI-washing, and it is examinable.

FINRA points the same way. In its 2026 oversight report, FINRA identified summarization and information extraction as the single most common generative-AI use case among member firms — and in the same breath flagged hallucination as a core risk of exactly that use case.[^finra][^finra2] The most popular thing firms do with AI is also the thing most likely to produce a confident, well-formatted, wrong answer. That is not an argument against using it. It is an argument for the evidence and control layers.

Investors have arrived at the same conclusion from the other side. AIMA found that 29% of institutional allocators already include specific AI questions in their due-diligence questionnaires, with another 29% planning to add them — questions about model oversight, data privacy, IP, and compliance.[^aima2] The AI DDQ is no longer hypothetical. A firm that cannot describe its AI operating model in writing is, increasingly, a firm that loses an allocation to one that can.

> Put the regulatory picture together and the conclusion is almost the opposite of the hype. The absence of a prescriptive rule does not make a defensible process optional. It makes it the *commercial* differentiator — the thing investors reward and examiners probe — precisely because no one is going to hand you a checklist.

---

## The Cost Nobody Budgets For

When firms ask "what will AI cost us," they look at the model bill — the seats, the API usage, the data add-ons. That bill is real, and it is the smallest line item.

The real cost lives in the other four layers: cleaning and parsing data, tuning retrieval, designing and testing workflows, building the review process, doing vendor diligence, training staff, and — the one nobody forecasts — **the cost of failed adoption**, where a firm pays for capability that quietly goes unused.

> The right unit of measurement is not "what is our AI bill." It is "what does it cost us to produce one *approved* output" — one reviewed earnings memo, one compliant client letter, one signed-off credit memo. Measure that, and the build-versus-buy conversation changes completely.

*(Also its own essay. Flagged here so the thesis is complete.)*

---

## The Path Across the Last Mile

So what does a firm actually do on Monday? Not "use AI more." The opposite — narrow, on purpose.

Pick one workflow. Choose something that is repeated often, document-heavy, time-consuming, and reviewable — an earnings memo, a DDQ response, portfolio commentary, a client communication, a covenant extraction. Then build the operating layer around just that one workflow, in order:

1. Define the **output** you actually want, in a fixed structure.
2. Define the **evidence** each part of that output must carry.
3. Name the **human reviewer** and what they are accountable for.
4. Write down the **red flags** that send a draft back.
5. Specify where the output is **stored and logged**.
6. Run the workflow on five historical cases you already know the answers to, and compare the AI-assisted result against how you did it before — on time, on quality, and on error rate.

Only after that comparison earns its keep do you scale to a second workflow. This is slower than "roll out AI to the firm," and it is the only version that produces something you can measure, defend, and repeat.

> **🔧 PROOF SLOT — replace before publishing.** *This is the strongest possible place for a real exhibit: a redacted before/after of one workflow you ran this way, with actual timings ("partner review went from 40 minutes to 12"), a sample review-log row, or a screenshot of a workflow test catching an error. A reader who is a CCO or PM will trust one real artifact more than the entire essay above it. Clear anything you show against your own confidentiality obligations first.*

---

## The Advantage Was Never the Subscription

The firms that win with generative AI will not be the ones that gave everyone a login and hoped. They will be the ones that turned capability into approved, evidence-backed, workflow-specific systems — and can prove it.

They will know where AI is allowed and where it is prohibited. They will know which outputs require review and which do not. They will know which documents were used, which claims are source-backed, and how much time was actually saved. And when an investor, a client, a compliance officer, or an examiner asks how the firm uses AI, they will have a written answer rather than a shrug about people experimenting.

That is the real advantage. It was never the subscription. It is the operating model.

The models will keep changing. Claude, GPT, and Gemini will leapfrog each other; today's best tool will be unremarkable in a year. None of that touches the thesis, because the durable work is not at the model layer. It is in the workflows, the evidence, and the controls — the things that stay relevant no matter which logo is on the model.

> **Prompts are disposable. Workflows and controls are durable. Everything I write here will be about building the durable part.**

---

### Where This Goes Next

This is the first essay in *The AI Operating Manual for Investment Firms*. Over the coming weeks I will take the pieces I only gestured at here and make them concrete: why retrieval-augmented generation fails in finance and what an evidence layer looks like in practice; the real cost model for GenAI in a fund; what every RIA chief compliance officer should ask before allowing ChatGPT or Claude; how a hedge fund should actually run earnings season; why private credit may be the single best GenAI use case in finance; and what the coming AI DDQ will demand of you.

> **Practical next step.** Take one AI-assisted workflow in your firm — a client communication, a DDQ response, a research memo, a credit memo, a piece of portfolio commentary — and ask three questions of it. Is every claim source-backed? Is there a named reviewer? Could you reconstruct the process in a year? If the answer to any of those is no, that workflow is usage, not adoption. That gap is where to start.

> **[SOFT CTA — your words.]** *I help investment firms move from scattered AI usage to defensible, evidence-backed workflows across research, client communication, DDQs, credit memos, and compliance review. If that is the gap you are staring at, [get in touch / subscribe / download the AI Usage Policy starter below].*

> **[LEAD MAGNET — build one before launch.]** *Gate something a buyer genuinely wants in exchange for an email: an "AI Usage Policy" starter template, a DDQ-readiness checklist, or a "cost per approved output" worksheet. The download is the start of the conversation — far stronger than a contact link.*

---

## Sources

*Verify each of these against the primary link before publishing; for an anti-hype brand, a single garbled statistic is the most expensive error you can make. Where a figure originates with a regulator or company, I have linked the regulator or company directly rather than a secondary write-up.*

[^aima]: Alternative Investment Management Association, *Charting the Course: Lessons from AI Leaders in Alternative Investments* (2025). 95% of fund-manager respondents reported using generative AI, up from 86% in 2023; survey of 150 fund managers (~$788bn AUM) plus 18 institutional investors. AIMA press release: https://www.aima.org/article/press-release-front-office-gen-ai-adoption-shifts-from-if-to-when-for-leading-fund-managers-aima-research-finds.html

[^schwab]: Charles Schwab, *RIA and AI Research Study* (released January 22, 2026; fielded October 2025, 533 advisers). 63% of RIAs use AI tools in some capacity (more than double 2023); most remain early-stage, concentrated on administrative tasks; only ~1 in 10 AI-using advisers have fully integrated AI into business strategy. https://pressroom.aboutschwab.com/press-releases/press-release/2026/Schwab-Study-Reveals-RIA-AI-Adoption-More-Than-Doubles---But-Most-Firms-Still-in-Early-Stages/default.aspx

[^balyasny]: OpenAI, "How Balyasny Asset Management built an AI research engine for investing" (case study, March 6, 2026). ~95% of Balyasny's ~180 investment teams actively use the internal platform; centralized Applied AI team; traceable reasoning and centralized guardrails with desk-level customization; research tasks cut from days to hours; Central Bank Speech Analyst from ~2 days to ~30 minutes. https://openai.com/index/balyasny-asset-management/ (Balyasny's own note: https://www.bamfunds.com/news-and-insights/balyasny-openai-feature)

[^bal2]: Per the same OpenAI case study and contemporaneous coverage, Balyasny evaluated its production model across 12+ financial dimensions (forecasting accuracy, numerical reasoning, hallucination reduction) before deployment. Confirm specifics against the OpenAI source above.

[^anthropic]: Anthropic launched *Claude for Financial Services* in July 2025 and on May 5, 2026 released ten ready-to-run finance agent templates (pitchbook creation, KYC screening, earnings review, month-end close, credit-memo drafting, etc.), with Microsoft 365 add-ins and data partnerships (Moody's, FactSet, Morningstar, S&P Global, Dun & Bradstreet). Coverage: https://fortune.com/2026/05/05/anthropic-wall-street-financial-services-agents-jamie-dimon/ — verify product specifics against Anthropic's own announcement before citing.

[^anthropic2]: Multiple reports note Anthropic's finance agent documentation states the agents produce drafts for qualified human review and do not execute transactions autonomously. Confirm against Anthropic's primary documentation/GitHub before relying on the exact wording.

[^jv]: Anthropic's ~$1.5bn joint venture with Blackstone, Hellman & Friedman, and Goldman Sachs to embed engineers in enterprises ("forward-deployed" delivery), reported May 2026. https://fortune.com/2026/05/04/anthropic-claude-consulting-industry-joint-venture-blackstone-goldman-sachs/

[^finretrieval]: E. Kim & J. Huang (Daloopa), *FinRetrieval: A Benchmark for Financial Data Retrieval by AI Agents* (January 2026). Leading configuration: 90.8% accuracy with structured-data APIs vs. 19.8% with web search alone — a 71-point gap; "tool availability dominates performance." arXiv: https://arxiv.org/abs/2603.04403

[^finagent]: See also *FinAgentBench* (agentic retrieval over S&P-500 filings; ACM ICAIF 2025): https://dl.acm.org/doi/10.1145/3768292.3770362 and *FinSearchComp* (high-difficulty financial search). Both report persistent fragility in realistic financial retrieval despite strong base reasoning.

[^withdraw]: U.S. SEC, withdrawal of *Conflicts of Interest Associated with the Use of Predictive Data Analytics by Broker-Dealers and Investment Advisers* (proposed July 2023; formally withdrawn June 12, 2025; Federal Register notice June 17, 2025). The withdrawal removes the proposed framework but not existing fiduciary, recordkeeping, or supervision obligations. SEC: https://www.sec.gov/rules-regulations/2025/06/s7-12-23

[^secwithdraw]: Context on the withdrawal of 14 Gensler-era proposals (the SEC stated it does not intend to finalize them and would re-propose to act): e.g., Dechert, https://www.dechert.com/knowledge/onpoint/2025/6/sec-withdraws-significant-number-of-rule-proposals.html

[^secpriorities]: U.S. SEC Division of Examinations, *Fiscal Year 2026 Examination Priorities* (released November 17, 2025). Heightened attention to AI; examiners to assess whether firms adequately supervise AI use and to review for accuracy firms' representations about their AI capabilities. Cite the SEC document directly from SEC.gov (Division of Examinations priorities page).

[^secpriorities2]: Practitioner analysis of the FY2026 priorities' AI section (governance, oversight, accuracy of AI representations): e.g., Corporate Compliance Insights, https://www.corporatecomplianceinsights.com/sec-2026-examination-priorities-financial-services/

[^finra]: FINRA, *2026 Annual Regulatory Oversight Report* (released December 9, 2025). Summarization and information extraction is the most common generative-AI use case among member firms; rules are technology-neutral; firms expected to conduct robust testing and maintain audit trails. https://www.finra.org/media-center/newsreleases/2025/finra-publishes-2026-regulatory-oversight-report-empower-member-firm

[^finra2]: FINRA GenAI section (hallucination, bias, and accuracy risks tied to the summarization/extraction use case): https://www.finra.org/rules-guidance/guidance/reports/2026-finra-annual-regulatory-oversight-report/gen-ai

[^aima2]: AIMA (2025 research, as above): 29% of surveyed institutional investors already include specific Gen AI questions in DDQs, with a further 29% expecting to add them; focus areas include model oversight, IP risk, data privacy, and compliance. https://www.aima.org/article/press-release-front-office-gen-ai-adoption-shifts-from-if-to-when-for-leading-fund-managers-aima-research-finds.html
