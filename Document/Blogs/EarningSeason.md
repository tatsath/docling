> *The AI Operating Manual for Investment Firms* — Essay 02

# How a Hedge Fund Should Actually Use AI for Earnings Season

### The one thing every AI demo shows you — "summarize the call" — is close to the least valuable thing a model can do for a serious analyst. Here is the earnings-season workflow that actually earns a place on the desk.

*By [YOUR NAME] · [DATE] · ~14 min read*

---

Earnings season is, before it is anything else, a capacity problem. A fundamental analyst covers some number of names deeply — call it fifteen to twenty-five. During a three-week window, a large share of them report within a few days of each other, often two or three on the same morning, each dropping a release, a deck, a 10-Q, and an hour of management commentary into a day that already has a fixed number of hours in it. The constraint is never the analyst's intelligence. It is attention, and there is never enough of it when it is needed most.

So it is worth being blunt about where AI helps and where it merely looks like it helps, because the reflexive answer — point a model at the transcript and ask it to summarize the call — is precisely the application with the lowest value to a good analyst. The summary was never the job. A capable analyst does not need the call condensed; they need to know what the call *means for the position*, and that is a different and much harder task.

There is a useful irony here. Across the industry, the single most common thing firms do with generative AI is summarization and information extraction — FINRA identified exactly that as the top use case among member firms in its 2026 report, and in the same breath flagged hallucination as a core risk of it.[^finra] The most popular use is also among the weakest, and the most error-prone. This essay is about the rest of the workflow — the parts that are worth doing, in the order a desk should actually do them.

> The thesis is the one I keep returning to: a fast answer is not a finished one. In earnings season, the finished product is not a summary. It is an updated, evidence-backed view on whether your thesis still holds.

---

## The Unit of Work Is the Thesis Update, Not the Summary

Reframe the whole exercise around a single question the analyst should be able to answer within hours of any print:

**Did anything this quarter change my variant view — and where, specifically, is the proof?**

Everything an AI system should do during earnings season is in service of answering that faster and more rigorously than a human could alone. That immediately splits the work into two halves that matter far more than the call itself: the *pre-read* (everything you assemble before the number drops) and the *post-read* (the structured reconciliation and judgment after it does). The call sits in the middle, and the summary of it is the least interesting artifact in the entire process.

> **[Figure 1 — "Two reads of one print"]**
>
> A horizontal timeline in three beats.
> - **Left — PRE-READ (T-minus):** "assemble the prep pack against last quarter's watch-list"
> - **Center — THE PRINT / CALL:** small, deliberately unglamorous
> - **Right — POST-READ (T-plus):** "reconcile, extract deltas, update the thesis"
>
> Annotate that AI's real leverage sits on the two ends, not the summary in the middle.
>
> *Caption: "The summary is the part everyone automates and the part that matters least."*

---

## The Pre-Read: AI's Real Leverage Happens Before the Number Lands

The highest-value AI work in earnings season happens *before* the release, not after — and almost nobody frames it that way.

In the day or two ahead of a print, the analyst's prep pack is a known, repetitive assembly job: pull last quarter's thesis and the specific variant view, list the KPIs that actually matter for *this* business (not a generic template — unit economics for one name, same-store sales for another, net revenue retention for a third), lay out consensus by line and segment, reconstruct the guidance walk including any pre-announcements or mid-quarter commentary, and — the part that separates disciplined desks from the rest — surface the **watch-list**: the three to five things you wrote down last quarter that you said you would be watching for this time.

This is exactly the kind of work a model does well, because the analyst is supplying the questions and the model is assembling the evidence to answer them quickly. Done right, the analyst walks into the print already knowing what would confirm the thesis, what would break it, and which two numbers to find first. The model did not form a view. It removed the hours of mechanical assembly that used to stand between the analyst and forming one.

> **🔧 PROOF SLOT — replace before publishing.** *The most credible thing you can put here is a real, redacted prep pack you actually use, or a concrete time figure: "building the pre-read for a name used to take me two hours the night before; assembled and reviewed, it now takes twenty minutes — and the twenty minutes are spent checking it, not typing it." Anyone on the buy side will recognize whether this is real. If you can't show one yet, cut the block rather than inventing a number.*

---

## The Post-Read: Structured Extraction, Not a Summary

When the release hits, the task is not "tell me what they said." It is "reconcile what they reported against three reference points and show me every delta that matters." Those reference points are your model, consensus, and prior guidance — and the work is to compute the differences line by line and segment by segment, not to narrate.

This is where domain knowledge does the heavy lifting, and where a generic summarizer is actively dangerous, because the traps in an earnings release are precisely the things a naive read glides over:

| Trap | What it hides |
|------|---------------|
| **Basis changes** | Adjusted vs. GAAP, segment reclassifications, a quietly changed KPI definition, "organic" vs. reported growth, an FX tailwind dressed as operational strength — a headline beat resting on a redrawn segment map is not a beat |
| **The guidance walk** | Raised, cut, or reaffirmed is the surface. The magnitude, the implied second-half ramp, and quality of any raise matter more — a beat-and-raise that lifts full-year guidance by exactly the size of the quarter's beat is not a raise at all |
| **Quality of earnings** | Cash conversion against reported profit, a receivables or inventory build that front-runs a demand problem, EPS flattered by a lower tax rate or a buyback rather than operations, the slow creep of "one-time" adjustments that recur every quarter |

A model can extract and reconcile all of this in minutes and lay the deltas out in a fixed structure — but only if the workflow tells it what to look for and demands that every figure carry its source. The output you want is not prose. It is a reconciliation that says: here is the reported number, here is what you modeled, here is consensus, here is the prior guide, here is the gap, and here is the line in the filing it came from. Then it ends with the only sentence that matters: *here is where this print touches your thesis.*

---

## Management Tone Is Not Sentiment

Now the part most people get wrong, and the part where showing some rigor sets you apart.

Pointing a generic sentiment model at an earnings call and reading off a "positive / negative" score is close to useless, and there is two decades of finance research explaining why. Loughran and McDonald showed back in 2011 that sentiment dictionaries built for other domains badly misclassify financial language — in their study of thousands of 10-Ks, nearly three-quarters of the words a widely used general dictionary flagged as negative were not negative in a financial context at all.[^lm] "Liability," "cost," "capital," "tax" — neutral or even positive in finance, scored as doom by a tool trained on ordinary English. The lesson generalizes well beyond their word lists: tone in financial communication is domain-specific, and a naive positive/negative read measures noise.

What actually carries information is more textured, and it lives mostly in the Q&A, not the prepared remarks:

| Signal | What to look for |
|--------|-----------------|
| **Uncertainty and hedging** | Drift toward conditional and modal language — "should," "could," "we expect" replacing "we will" — relative to how the same team spoke last quarter |
| **Evasion** | Whether management actually answered the analyst's question or returned a fluent non-answer, and which questions they declined to engage[^nonanswers] |
| **Guidance discipline** | Specific versus vague, and whether the precision changed — a team that gave point targets last quarter and switched to "ranges" is telling you something |
| **Language drift** | The vocabulary that disappeared — when a team stops describing demand as "strong" and starts calling it "resilient," that is data |
| **Tone-versus-substance gap** | Upbeat delivery layered over a decelerating KPI is one of the more reliable flags there is |

There is even evidence that linguistic features of management narratives carry information beyond the numbers. Larcker and Zakolyukina found that models built purely on the language of CEO and CFO answers in earnings Q&A predicted subsequent financial restatements meaningfully better than chance — at least as well as models built on accounting variables — and that the language of executives later found to have misstated had identifiable tells, including a notable absence of references to shareholder value and an excess of extreme positive emotion.[^larcker]

Two cautions, stated plainly so the essay stays honest. First, this is exactly the kind of analysis AI is well suited to surface across dozens of calls a human could never read closely in the window — flagging the hedging, the non-answers, the language drift for an analyst to examine. Second, these are signals to *investigate*, never verdicts to *act on*. Over-fitting a thesis to a CFO's word choice is its own failure mode. The model's job is to raise its hand and point at the suspicious passage. The analyst's job is to decide whether it means anything.

> **[Figure 2 — "What 'tone' actually decomposes into"]**
>
> Center node: "Management tone." Show a generic positive/negative gauge as a thin, greyed-out sliver labelled "what naive sentiment measures." Branch out the signals that matter: Uncertainty / hedging · Q&A evasion (non-answers) · Guidance discipline · Language drift vs. prior quarters · Tone-vs-numbers gap.
>
> *Caption: "Generic sentiment misclassifies financial language (Loughran-McDonald, 2011). The signal is in the texture, and most of it is in the Q&A."*

---

## The Single Most Valuable Use: Make the Model Argue Against You

If I had to name the one AI application that improves a hedge-fund analyst's actual decisions during earnings season, it is not extraction and it is not tone. It is the red team.

Confirmation bias is the analyst's occupational disease, and it is never worse than in earnings season, when you are emotionally and financially invested in a thesis and the print arrives as a Rorschach test you are primed to read in your favor. The most useful thing a model can do is refuse to cooperate with that instinct. Feed it the same transcript, the same filings, and your own memo, and instruct it to build the strongest possible case *against* your position — to steelman the short if you are long, to assemble every data point in the print that a smart bear would lead with, to attack your variant view at its weakest joint.

This is genuinely valuable precisely because the model has no ego in the trade. It will say the uncomfortable thing your own notes were quietly routing around. And, to be clear about what it is: a discipline mechanism, not a decision-maker. The point is not that the model knows whether you are wrong. The point is that being forced to read the best opposing case, every quarter, before you update your view, is one of the cheapest ways to make better decisions that has ever existed.

> **🔧 PROOF SLOT — replace before publishing.** *If you have ever run a red-team pass and it caught something you'd talked yourself out of — a segment that was decelerating faster than your narrative admitted, a guide that was lower-quality than it looked — describe it (anonymized). A specific "here's the time the devil's advocate was right and I wasn't" is worth more than any amount of theory about confirmation bias.*

---

## Expanding Coverage Without Pretending the Model Does the Analysis

The capacity problem has a second dimension. An analyst covers fifteen to twenty-five names deeply, but the universe that *bears on* those names — competitors, suppliers, customers, adjacent comps — is several times larger, and during the earnings crunch most of it goes unwatched. The supplier that pre-announced, the competitor whose print implied share shift, the customer whose capex commentary undercuts your demand assumption: these are the things you find out about late.

This is where continuous monitoring earns its keep, and it is no longer theoretical. Balyasny's documented build includes agents that continuously monitor and update — a "Merger Arbitrage Superforecaster" that revises deal probabilities as filings and developments land, and proactive alerts that surface filing discrepancies and breaking moves rather than waiting to be queried.[^balyasny] The analogous move for a fundamental desk is a monitoring layer that watches the eighty names you do not cover deeply and flags when a comp's print, a supplier's guide, or a customer's commentary touches one of your positions.

> **Non-negotiable design rule:** *monitored is not covered.* An alert opens a piece of work for a human; it never updates a view or moves a position on its own. The model widens the perimeter of what you notice. It does not shrink the perimeter of what a person decides.

---

## The Memo Is an Evidence Chain, and That Is What Makes It an Asset

Whatever this workflow produces — the reconciliation, the tone flags, the red-team case — should land in a memo built as an inspectable chain rather than a block of confident prose. For every material claim: what is the claim, which transcript line or filing page supports it, what calculation produced any number in it, and who signed off. This is the same evidence discipline that runs through everything in this series, applied to the earnings memo specifically.

> **[Figure 3 — "The earnings memo as an evidence chain"]**
>
> Left-to-right flow, deliberately echoing the evidence-chain figure from Essay 01:
>
> **Claim** → **Transcript line / filing page** → **KPI reconciliation (the math)** → **PM sign-off**, with a small "sent back" loop from sign-off to source.
>
> *Caption: "Same evidence chain as the operating-model essay — pointed at a single earnings print."*

There is a compounding benefit most desks miss. A memo built this way is not just defensible today; it is *searchable institutional memory*. Two years from now, when the same name reports and a new analyst asks "what did we actually think last time, and why," a corpus of evidence-linked memos answers in seconds what otherwise lives only in someone's head or a buried email. The evidence trail is the byproduct that quietly becomes one of the firm's most valuable assets — a thread I will pull on properly in a later essay on turning a research archive into investment memory.

---

## Why None of This Trades First

A reasonable reader will ask: if the model can reconcile the print, read the tone, and argue both sides, why keep the human in the loop at all? Because the parts that matter most are still irreducibly human. The variant view — the reason you see this name differently from the market — is a judgment. Conviction is a judgment. Position sizing against risk is a judgment. AI compresses the path *to* those judgments dramatically; it does not make them, and it should not.

It is telling that even the firms building finance-specific agents draw this line themselves. Anthropic's own finance agent documentation describes its tools as producing drafts for qualified human review rather than executing anything autonomously.[^anthropic] When the vendors are explicit that the output is draft material for a professional to approve, a fund treating model output as a decision is getting the workflow exactly backwards. Research-first, always, before any thought of execution automation.

---

## How to Actually Start

Do not roll this out across the whole desk. Prove it on names you know cold.

Pick five companies whose last quarter you remember well — where you know what mattered, what the print did, and what you concluded. Run last quarter's release and call through this full workflow: pre-read pack, structured reconciliation, tone pass, red team, evidence-linked memo. Then compare the result against what you actually produced at the time, on three axes:

- How much prep time it removed
- How many reconciliation errors or basis changes it caught
- Whether the structured pass surfaced anything you missed live

Only once that comparison earns its keep do you extend it to your full coverage list, one workflow layer at a time.

> Five known cases will teach you more about whether this works for your process than any vendor demo, because you already know the right answers.

---

## The Desks That Win Earnings Season

It will not be the ones that summarize fastest. Summarizing is the commodity, and it is the part most likely to be confidently wrong.

It will be the desks whose analysts spend their scarcest resource — judgment, in the hours when there is least of it — on the variant view and the decision, because the assembly, the reconciliation, the tone scan, and the monitoring are handled, structured, and auditable. They will walk into every print already knowing what would break the thesis. They will reconcile against three reference points before the market has finished reading the headline. They will read the best case against themselves every quarter. And they will leave behind an evidence trail that makes the next quarter, and the next analyst, faster.

The models will change. This quarter's best one will be ordinary by next year. The workflow, the evidence discipline, and the human judgment at the center of it will not. That is where the durable advantage lives — not in the tool, in how the desk decides to use it.

---

### Where This Goes Next

This is Essay 02 in *The AI Operating Manual for Investment Firms*. Earnings season touches several threads I will develop on their own: a deeper piece on building a thesis tracker that knows when a long/short view is breaking; one on management-tone analysis as a discipline rather than a sentiment score; and one on turning years of internal memos into searchable investment memory. The connective tissue is the operating-model argument from Essay 01 — that the advantage is in the workflow, the evidence, and the controls, not the subscription.

> **Practical next step.** Before the next print in your coverage, write down the three things you will be watching for. After the print, ask whether your process answered them within hours, with the proof attached — or whether you were still hand-assembling context while the stock moved. The gap between those two is the workflow this essay is about.

> **[SOFT CTA — your words.]** *I help investment teams turn earnings-season research from a scramble into a defensible, evidence-backed workflow — pre-read assembly, structured reconciliation, tone and red-team passes, and memos a PM can actually stand behind. If that is the gap on your desk, [get in touch / subscribe / download the earnings-memo template below].*

> **[LEAD MAGNET — build before launch.]** *Gate something an analyst genuinely wants: an "Earnings Memo Template + Thesis-Update Checklist," or a one-page "Quality-of-Earnings Red-Flags" sheet (basis changes, guidance-walk quality, cash conversion, adjustment creep). The download starts the conversation.*

---

## Sources

*Verify each against the primary link before publishing. Academic citations are given in full so a sophisticated reader can check them — which is part of the point.*

[^finra]: FINRA, *2026 Annual Regulatory Oversight Report* (released December 9, 2025). Summarization and information extraction is the most common generative-AI use case among member firms; the report flags hallucination, bias, and accuracy as core risks of GenAI use. https://www.finra.org/media-center/newsreleases/2025/finra-publishes-2026-regulatory-oversight-report-empower-member-firm (GenAI section: https://www.finra.org/rules-guidance/guidance/reports/2026-finra-annual-regulatory-oversight-report/gen-ai)

[^lm]: Tim Loughran & Bill McDonald, "When Is a Liability Not a Liability? Textual Analysis, Dictionaries, and 10-Ks," *Journal of Finance* 66, no. 1 (2011): 35–65. Generic (non-financial) sentiment dictionaries misclassify financial text — in a large sample of 10-Ks, nearly three-quarters of words flagged negative by a widely used general dictionary were not negative in a financial context; the authors develop finance-specific word lists. DOI: https://doi.org/10.1111/j.1540-6261.2010.01625.x (dictionary hosted at Notre Dame SRAF: https://sraf.nd.edu/loughranmcdonald-master-dictionary/)

[^larcker]: David F. Larcker & Anastasia A. Zakolyukina, "Detecting Deceptive Discussions in Conference Calls," *Journal of Accounting Research* 50, no. 2 (2012): 495–540. Linguistic-based models built on CEO/CFO narratives in earnings Q&A predicted subsequent financial restatements better than chance (reported out-of-sample improvement on the order of 6–16%), at least equivalent to models based on accounting variables; identifies linguistic tells associated with later-restating executives. https://www.gsb.stanford.edu/faculty-research/publications/detecting-deceptive-discussions-conference-calls (DOI: https://doi.org/10.1111/j.1475-679X.2012.00450.x)

[^nonanswers]: On evasion and non-answers in earnings Q&A, see Ian D. Gow, David F. Larcker & Anastasia A. Zakolyukina, "Non-Answers During Conference Calls," *Journal of Accounting Research* 59, no. 4 (2021): 1349–1384 — part of a broader literature treating evasive or non-responsive answers as informative. Confirm the citation against the journal before relying on specifics.

[^balyasny]: OpenAI, "How Balyasny Asset Management built an AI research engine for investing" (case study, March 6, 2026). Documents continuous-monitoring agents, including a "Merger Arbitrage Superforecaster" that updates deal probabilities and proactive alerts surfacing filing discrepancies; ~95% of the firm's ~180 investment teams use the internal platform; built around traceable reasoning and centralized guardrails. https://openai.com/index/balyasny-asset-management/

[^anthropic]: Anthropic's finance agent materials (2026 finance agent templates) describe the agents as producing drafts intended for qualified human review rather than executing transactions autonomously. Confirm exact wording against Anthropic's primary documentation before quoting. Industry coverage: https://fortune.com/2026/05/05/anthropic-wall-street-financial-services-agents-jamie-dimon/
