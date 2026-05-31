# RAG, Agents, and the Finance Evidence Layer

> **Type:** Strategic analysis — document intelligence product positioning  
> **Covers:** Agent vs. RAG framing, extraction vs. validation tiers, competitive landscape, feasibility, recommended wedge

---

## Research Notes — Benchmark Verification

> The two load-bearing claims below were independently verified before writing. **OfficeQA Pro** is a March 2026 Databricks benchmark — 89,000 pages of US Treasury Bulletins, 26M+ numerical values, frontier agents averaging 34.1% accuracy when given direct document-corpus access, and a 16.1% average relative gain from structured document representation via Databricks' `ai_parse_document`. **ParseBench** is an April 2026 LlamaIndex benchmark — ~2,000 human-verified enterprise pages across tables, charts, content faithfulness, semantic formatting, and visual grounding, with no method consistently strong across all five dimensions. Both are recent, citable, and on-point. The Anthropic agent list in Section 3(b) is also exactly right.
>
> The one attribution to double-check before pitching is the "Pieter Stock / Mistral" quote — the benchmarks and Anthropic lineup carry the argument; that quote is decorative and unconfirmed. The YouTube link was rate-limited and could not be opened.

---

## 1. The One Fix: It's Not "Agent vs. RAG"

**The sharper framing:** probabilistic reading vs. deterministic extraction.

The current document frames this as a two-bucket world — agents here, RAG there. That framing will get picked apart, because **RAG is not the answer for exact financial numbers either.** RAG and agents are both *probabilistic reading* approaches — an LLM still reads a chunk of retrieved text and transcribes the number, and it can still grab the wrong cell, the wrong unit (millions vs. thousands), or the wrong period (FY24 vs. Q4 vs. LTM). RAG improves *retrieval* (finding the right page) but not *extraction correctness* (getting the value exactly right). That is the deeper meaning of the OfficeQA result: better parsing helped more than a better model.

The real dividing line — and the sharper version of the thesis — is **three tiers, not two:**

| Tier | What it is | Good for | Fundamental weakness |
|------|------------|----------|----------------------|
| **Agent** | Model + tools, reads/reasons/acts in a loop | Open-ended, multi-step, flexible work | Slow, expensive, hard to audit; fragile on exact numbers |
| **RAG** | Chunk → embed → retrieve → generate | Search & synthesis over a large corpus | Retrieves text, not validated values; same extraction fragility |
| **Deterministic extraction + validation** | Parse → structured schema → rule checks → cell-level citation + confidence + abstention | Exact, repeatable, audit-grade numbers | Needs known fields/templates; ingestion cost upfront |

RAG sits *underneath* an agent or an extraction pipeline as a retrieval technique — it is not a peer category to "agent." If you pitch "agents vs. RAG," a technical buyer hears a category error.

**The pitch that lands:**

> *Probabilistic reading is fine for synthesis. Finance numbers need a deterministic extraction-and-validation layer.*

---

## 2. The Isolation, Scored

### Where agents win — use freely

Multi-step, flexible, fault-tolerant work where a fuzzy answer is acceptable and a human reviews output anyway:

- Cross-document search, sector/thesis research, news + filing synthesis, expert-call search
- Drafting: memos, notes, profiles, CIM summaries, pitchbook *assembly*, meeting prep
- Comps *screening structure*, code generation / backtesting, exception routing

| Dimension | Agents |
|-----------|--------|
| Accuracy | Adequate |
| Control | Weakest |
| Cost | Highest |
| Speed | Slowest |

### Where RAG specifically earns its place

"Find and synthesize across our data room / research library / filings" — diligence Q&A, deal-room search, precedent-transaction *discovery*, "every mention of X across 3,000 docs." Always with citations and a human check.

| Dimension | RAG |
|-----------|-----|
| Accuracy on *locating* | Good |
| Accuracy on *exact figures* | **Do not trust** |
| Cost (after initial parse/embed) | Low at query time |
| Speed | Fast at query time |

### Where deterministic extraction + validation is mandatory — the moat

Anything where a wrong number is not a harmless hallucination:

- Financial spreading from borrower packages
- Covenant thresholds and breach monitoring, debt schedules
- Interest-coverage / liquidity calcs, NAV, portfolio holdings ingestion
- Position-level reconciliation, bank-statement transactions, GL reconciliation
- Statement tie-outs, segment tables, guidance ranges, reported-vs-adjusted, chart-value extraction

| Dimension | Deterministic extraction |
|-----------|--------------------------|
| Accuracy on known fields | **Highest** |
| Control / auditability | **Highest** — cell-level provenance, confidence, abstention |
| Cost per repeated query | **Lowest** — parse once, cache, send compact evidence |
| Speed | Fast once ingested |

### Mapped to the three segments

| Segment | Agents | RAG | Extraction + validation |
|---------|--------|-----|------------------------|
| **Buy-side** (HF / AM / PE / private credit) | Thesis monitoring, earnings synthesis, sector research | Data-room / diligence search | Spreading, covenants, debt schedules, NAV, holdings, reconciliation |
| **Sell-side** (IB / equity research) | Pitchbook drafting, profiles, market updates, note drafting | Filing / CIM / research search | Spreading, EV/EBITDA, precedent-transaction values, valuation-bridge numbers, chart data, guidance ranges |
| **Finance ops / audit** | Checklist orchestration, variance commentary, audit-packet assembly | — | GL reconciliation, NAV, tie-outs, SOX evidence |

> Sections 5–8 in the original document already had these lists largely right. The upgrade is the scoring axis and putting RAG in its correct (subordinate) place.

---

## 3. Feasibility — and Why "Sell to Anthropic" Is the Wrong Frame

Does the thesis make sense? **Yes** — and it is now empirically backed by two fresh benchmarks. But three hard truths:

### (a) This is not greenfield — it is one of the most contested, best-funded spaces in AI right now

- **Reducto** has raised $108M (a16z, Benchmark, First Round) for document parsing and extraction, and powers document workloads for Harvey, Rogo, and Scale AI.
- **Hebbia** raised $130M at a $700M valuation for exactly the "multi-agent, every-answer-cited" workflow.
- Add Rogo, Daloopa, AlphaSense, LlamaParse, Databricks' `ai_parse_document`, and incumbents (Textract, Azure Document Intelligence, Google Document AI, Ocrolus for bank statements).

> A generic "evidence harness for finance" deck will sound like ten others. You need a *wedge*, not a platform.

### (b) Anthropic has already shipped most of the "harness" — and outsources the part you would build

Their May 5, 2026 release put out ten finance agent templates:

| Template | Category |
|----------|----------|
| Pitch builder | IB / deal |
| Meeting preparer | Research |
| Earnings reviewer | Research |
| Model builder | Quant / analysis |
| Market researcher | Research |
| KYC screener | Compliance |
| Valuation reviewer | Deal |
| General ledger reconciler | Finance ops |
| Month-end closer | Finance ops |
| Statement auditor | Finance ops |

Each combines task-specific skills, governed data connectors, and subagents. The Managed Agent versions ship with long-running sessions for multi-hour deal closes, per-tool permissions, managed credential vaults, and full audit logs, and every output is staged for human sign-off — the agents do not post to the ledger, execute transactions, or approve onboarding.

**What they don't build is the deterministic structured-data layer.** They reach it through connectors — FactSet, S&P Capital IQ, MSCI, PitchBook, Morningstar, LSEG, and Daloopa, plus a Moody's MCP app. The fact that Anthropic *partners* for Daloopa rather than building it is simultaneously the proof that the wedge has value and the warning that standardized-filing extraction is already occupied.

### (c) Therefore the realistic paths are partnership/build-on, not acquisition

Anthropic is a model + platform company and not historically acquisitive. "Get acquired by Anthropic" is an *outcome*, not a *strategy*. The strategies that actually work:

1. Build a best-in-class **financial extraction + validation MCP server / connector** and enter the Anthropic ecosystem the way Daloopa and Moody's did — position it as the trust layer their pitch / credit / GL agents *call* when a number must be right.
2. Build a **standalone product** for a specific finance segment, with Claude underneath.
3. Ship a **Cowork plugin / Skill bundle** in their marketplace.

> If the extraction layer genuinely becomes the thing Anthropic's finance agents depend on, acquisition tends to follow on its own — but you get there by being indispensable, not by pitching a deck.

---

## 4. What to Actually Build

**Pick one workflow where mistakes are expensive, documents are repetitive, and incumbents are weak.**

The strongest candidate from everything above:

> **Private-credit covenant extraction + monitoring**

Rationale:
- High pain, high accuracy bar
- Deterministic checks: leverage = debt/EBITDA, interest coverage, liquidity
- Not as crowded as bank statements (Ocrolus) or standardized filings (Daloopa / Capital IQ)

Fund / portfolio-statement reconciliation (qty × price ≈ market value; opening + credits − debits = closing) is a close second.

**How to build the differentiator:**

Build a real validation engine — rule checks, cell-level / bounding-box citations, confidence scores, and an **abstention + human-review queue** ("conflicting evidence / not found / needs review"), not an agent that double-checks itself.

**How to prove it:**

Run ParseBench, or build your own covenant-extraction eval, and lead the pitch with the accuracy number. In a space this crowded, a defensible benchmark is worth more than the architecture diagram.

---

> **Next step:** This analysis can be turned into either (a) a tight one-page thesis — the reframed "trust layer for finance agents" narrative — or (b) a short investor/partner deck outline with the benchmark evidence built in. The covenant-monitoring wedge can also be pressure-tested specifically if that is the direction to lean.
