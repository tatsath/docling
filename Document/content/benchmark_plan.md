# Head-to-Head Benchmark Plan
### Proving the assembled stack beats Claude Cowork on accuracy, validation, cost, and speed — using the fund's own documents

**Purpose.** A defensible, reproducible bake-off that a hedge fund's CIO/Head of Research can trust. It compares the live-reading agent baseline (Claude Cowork) against assembled architectures on the metrics they actually care about: **accuracy and validation first, then cost and speed.** The output is a single table they can act on.

**Core principle.** Run it on *their* documents and *their* questions, not a public benchmark. A public number ("we hit 84% on X") is a credibility risk in finance; "we answered 47 of your 50 covenant questions correctly, with every number cited and every uncertain one flagged" is a purchase order.

---

## 1. What we are comparing (the arms)

| Arm | Description | Why it's in the test |
|---|---|---|
| **Baseline: Cowork alone** | Point [Claude Cowork](https://www.anthropic.com/product/claude-cowork) at a folder of PDFs, ask the questions live | The status quo the fund is complaining about |
| **Arm A: Cloud-native** | [Reducto](https://reducto.ai/) parse → [Bedrock KB](https://aws.amazon.com/blogs/machine-learning/amazon-bedrock-knowledge-bases-now-supports-hybrid-search/) or [Azure AI Search](https://azure.microsoft.com/en-us/products/ai-services/ai-search) (hybrid) → rerank → Claude → validation | Lowest-friction production option |
| **Arm C: Best-of-breed** | [Unsiloed](https://www.unsiloed.ai/)/Reducto → [Contextual Retrieval](https://www.anthropic.com/news/contextual-retrieval) → hybrid + rerank → Claude → full validation engine | Accuracy-maximalist flagship |
| **Arm E: Hebbia** *(optional)* | Same corpus loaded into [Hebbia Matrix](https://www.hebbia.com/) | Upper bound reference; only if the fund has access |

Keep it to 3 arms (Baseline, A, C) for a first engagement. Add Hebbia only if the fund already licenses it or will trial it — it's the "ceiling" reference, not a build target.

---

## 2. Test corpus (representative, not cherry-picked)

Assemble ~50–100 real documents the fund works with daily. The mix matters more than the volume. Suggested for a private-credit / buy-side fund:

- 10–15 **borrower financial packages** (messy, multi-tab, scanned pages)
- 5–10 **loan / credit agreements** (covenant definitions, conditional clauses)
- 10 **10-Ks / 10-Qs** (clean, standardized — the "easy" control set)
- 5–10 **investor decks / CIMs** (chart-heavy, KPI tables)
- 5–10 **fund / portfolio statements** (holdings, NAV, transactions)
- 5 **earnings transcripts** (text-heavy, qualitative)

Deliberately include 10–15 **adversarial documents**: scanned 1990s filings, rotated pages, merged-cell tables, footnoted restatements, units in thousands-vs-millions. This is where Cowork breaks and the assembled stack earns its fee.

---

## 3. Question set (the ground truth is the hard part)

Write 50–100 questions spanning four difficulty tiers, each with a **human-verified gold answer + the exact source location** (doc, page, table, cell). This gold set is the single most valuable asset of the engagement — build it carefully with an analyst.

| Tier | Type | Example | What it stresses |
|---|---|---|---|
| **T1 — Lookup** | Single exact value | "What was FY24 revenue for Borrower X?" | Parsing + extraction |
| **T2 — Computed** | Value requiring a calc | "What is current net leverage (debt − cash) / LTM EBITDA?" | Extraction + arithmetic + validation |
| **T3 — Multi-doc** | Synthesis across files | "Did the covenant headroom improve vs last quarter?" | Retrieval + comparison over time |
| **T4 — Reasoning** | Conditional / abstract | "Which covenant is closest to breach, and why?" / "What in this credit agreement looks weak?" | Decomposition + logic (Hebbia's sweet spot) |

Balance: roughly 40% T1, 25% T2, 20% T3, 15% T4. The T1/T2 tiers are where validation matters most (wrong number = loss); T4 is where you honestly concede ground to Hebbia (see the advisory note).

---

## 4. Metrics

### Accuracy & validation (primary — weight these highest)
- **Exact-match accuracy** (T1/T2): is the number right, with correct unit and period? Binary per question.
- **Computed-value accuracy** (T2): does the derived figure match gold within tolerance?
- **Citation precision**: does the cited source page/cell actually contain the value? ([Industry production target ≥90%](https://customgpt.ai/rag-evaluation-metrics/).)
- **Faithfulness / groundedness**: is every claim supported by retrieved context? Score with [RAGAS](https://github.com/explodinggradients/ragas) / claim-level entailment (entailed / contradicted / baseless). (Target ≥0.85; fail a release below 0.80.)
- **Abstention quality**: of the questions the system *couldn't* answer correctly, how many did it correctly flag as "needs review" rather than answering confidently wrong? **This is the metric finance cares about most** — a flagged unknown beats a confident error.
- **Hallucination rate**: % of answers with an unsupported/fabricated claim. (Benchmark context: [Stanford measured 17–33% on leading legal RAG tools](https://galileo.ai/blog/rag-evaluation-tools); aim materially below.)

### Cost (secondary)
- **Tokens per query** (and per task for Cowork) — input + output, including vision tokens.
- **$ per query** at the model's published rate.
- **One-time ingestion cost** (parse + contextualize + embed) — amortized over expected query volume.

### Speed (secondary)
- **End-to-end latency per query** (p50 and p95).
- **Ingestion throughput** (pages/min) — one-time.

### Operational (tie-breakers)
- Deployment fit (VPC / on-prem / cloud-native), data-retention posture, auditability of logs.

---

## 5. Procedure

1. **Freeze the corpus and question set.** Same inputs to every arm. No tuning to the test questions (hold out a 20-question validation slice you never look at until the final run).
2. **Ingest once per arm** (except Cowork, which has no persistent index — that asymmetry is the point). Record ingestion cost/time.
3. **Run all questions through each arm**, logging the answer, the citation(s), token usage, and latency for every question.
4. **Score against gold**: automated for exact-match/citation/faithfulness (RAGAS + scripts), plus a **20-question blind human audit** per arm by a fund analyst (the human audit is what makes the result credible internally).
5. **Compute the table.** Report p50 and p95 for latency; report cost both per-query and fully-loaded (incl. amortized ingestion).
6. **Error taxonomy.** For every wrong answer, tag the failure: parsing error / retrieval miss / extraction error / reasoning error / unit-period error. This tells the fund *why* each arm failed and justifies each layer of the stack.

---

## 6. The output table (template — fill with real numbers)

> Illustrative shape only. Replace every cell with measured results from the fund's corpus. Numbers below are plausible expected ranges, NOT measured — do not present them as data.

| Metric | Cowork (baseline) | Arm A (cloud-native) | Arm C (best-of-breed) | Arm E (Hebbia) |
|---|---|---|---|---|
| **Exact-match acc. (T1)** | low–mid | high | **highest** | high |
| **Computed acc. (T2)** | low | mid–high | **highest** (rule-checked) | mid–high |
| **Multi-doc (T3)** | low–mid | high | high | **highest** |
| **Reasoning (T4)** | mid | mid | mid–high | **highest** |
| **Citation precision** | unreliable | high | **highest** | high |
| **Faithfulness (RAGAS)** | low–mid | high | **highest** | high |
| **Abstention quality** | none | medium | **full (flags unknowns)** | partial |
| **Hallucination rate** | high | low | **lowest** | low |
| **Tokens / query** | 100k–1M+ (re-reads) | ~3–10k | ~3–10k | n/a (opaque) |
| **$ / query** | $$$$$ | $ | $ | $$$$ (license) |
| **Ingestion cost (1×)** | none | low–med | med | included |
| **Latency p50** | minutes | seconds | seconds | seconds–min |
| **Validation control** | none | partial | **full (yours)** | none (theirs) |
| **Deploy in VPC** | no | yes | **yes** | limited |

**Headline framing for the fund:** *"On your own 50 documents, the baseline answered N of 50 correctly and flagged none of its errors. The assembled stack answered M of 50, cited every number to the source cell, and flagged the rest for review — at ~Xx lower cost and ~Yx faster per query."*

---

## 7. Pitfalls to avoid (so the result holds up)

- **Don't tune to the test.** Hold out a slice. Funds will (rightly) suspect a rigged demo.
- **Don't use only clean 10-Ks.** They make every arm look good and hide the parsing differentiator.
- **Don't skip the human audit.** Automated faithfulness scoring is necessary but a fund's own analyst signing off on 20 answers is what closes the deal.
- **Don't over-claim on T4 reasoning.** Be honest that pure synthesis/reasoning is where Hebbia is strongest; your edge is exact, validated, audit-grade numbers.
- **Report cost honestly including ingestion.** The assembled stack front-loads cost; show the crossover point (typically after a handful of queries per document).

---

## 8. References & Sources

*Clickable, annotated with the claim each supports. Re-verify figures against primary sources before external use.*

### Benchmarks & accuracy data
- **OfficeQA Pro** (Databricks) — https://arxiv.org/abs/2603.08655 — agents 34.1%; **+16.1% from structured parsing** (justifies parsing-first + adversarial corpus, §2)
- **ParseBench** (LlamaIndex) — https://www.llamaindex.ai/blog/parsebench — five parsing dimensions (justifies the table/chart/grounding test mix)
- **LlamaParse accuracy note** (85–95% clean / 70–85% scanned) — https://dev.to/melek_messoussi_651bf64f4/i-built-a-production-ready-document-parser-for-rag-apps-that-actually-handles-complex-tables-full-3lgn

### Validation & evaluation metrics (§4)
- **Galileo** (Stanford **17–33%** legal-RAG hallucination; LLM-as-judge **>85%** human correlation) — https://galileo.ai/blog/rag-evaluation-tools
- **Maxim** (up-to-**40%** hallucination even when correct info was retrieved) — https://www.getmaxim.ai/articles/rag-evaluation-a-complete-guide-for-2025/
- **CustomGPT** (production rubric: retrieval recall **≥85%**, citation precision **≥90%**, groundedness **≥4.0** gate) — https://customgpt.ai/rag-evaluation-metrics/
- **Deepchecks** (RAGAS faithfulness, NLI entailment, claim labeling) — https://deepchecks.com/rag-evaluation-metrics-answer-relevancy-faithfulness-accuracy/
- **RT4CHART** (claim-decomposition: entailed / contradicted / baseless) — https://arxiv.org/pdf/2603.27752

### Cost & token mechanics (§4 cost metrics, baseline arm)
- **Anthropic — PDF support** (1,500–3,000 tokens/page **+ an image per page**) — https://platform.claude.com/docs/en/build-with-claude/pdf-support
- **Anthropic — Pricing** — https://platform.claude.com/docs/en/about-claude/pricing
- **Token-limit explainer** (50-page PDF = 75k–150k tokens) — https://limitededitionjonathan.substack.com/p/why-you-keep-hitting-claudes-usage

### Competitor reference (Arm E)
- **Hebbia — "Goodbye RAG"** (Full Attention; strongest on reasoning/synthesis; validation via log-likelihoods) — https://www.hebbia.com/blog/goodbye-rag-how-hebbia-solved-information-retrieval-for-llms
