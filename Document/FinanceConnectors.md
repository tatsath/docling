# Finance Data & MCP: Cost, the Free Path, and the Open-Source Harness Thesis

A first-principles companion to the connector catalogue. Three questions answered: what does each data source actually cost, how far can you get for zero, and does the "open-source harness plus local models, skip Rogo and Anthropic" idea hold up. Then a sector-by-sector breakdown for banking, insurance, and hedge funds, and the two workflows you care about (assemble a document from MCP inputs, and read Excel well).

> **Sourcing and honesty:** Enterprise vendors hide list prices, so the numbers below are triangulated from vendor-comparison sites, Wall Street Oasis (WSO) threads, and press. Treat them as ranges, not quotes. Anything marked "per WSO" or "reported" is practitioner chatter, not an official rate. Get a real quote before you budget. None of this is financial or procurement advice.

---

## Part 1. Cost for each source (approximate)

### Tier A. Enterprise terminals and data (the expensive layer)

| Source | Approx. cost / seat / yr | Notes | Link |
|---|---|---|---|
| Bloomberg Terminal | $31,980 single; ~$28,320 multi; down to ~$22,660 at 50+ seats | 2-yr minimum; 6.5% jump for 2025 contracts. B-PIPE / SAPI API adds ~$50,000+. Per costbench / godeldiscount 2026. | https://www.bloomberg.com/professional/ |
| FactSet | $12,000–$18,000 typical; modular up to ~$50,000 | Modular pricing; you pay for components. Buy-side favourite for Excel integration. | https://www.factset.com/ |
| S&P Capital IQ Pro | $12,000–$30,000 | "Most expensive but most trusted data" per WSO. M&A, fundamentals, credit. | https://www.spglobal.com/market-intelligence/ |
| LSEG Workspace (ex-Refinitiv Eikon) | ~$4,000 stripped to $22,000+ full | Reuters news, FX, fixed income, rates. | https://www.lseg.com/ |
| PitchBook | under $10,000 per WSO; some quotes $15,000–$25,000 | Private capital (PE/VC) deals. WSO: private-company data "often unreliable." | https://pitchbook.com/ |
| Preqin | under $10,000 per WSO | Alternatives / private markets data. | https://www.preqin.com/ |
| Morningstar Direct | ~$20,000 first seat; ~$11,000 second; ~$9,500 additional | 2016 baseline +15–25%; institutional pricing confidential. Funds / ETFs / portfolio analytics. | https://www.morningstar.com/products/direct |
| Daloopa | Not public; free trial; per-seat for analysts | Source-linked fundamentals + KPIs, 99%+ accuracy, 5,500+ tickers, Excel add-in, "Scout" agent. Raised $103M. | https://daloopa.com/ |
| Moody's (ratings / analytics / Orbis) | Enterprise, custom | Credit ratings + risk on 600M+ companies; KYC entity data. | https://www.moodys.com/ |
| MSCI | Enterprise, custom | Indexes, ESG, factor and risk analytics. Index licensing often $20,000+ and scales hard. | https://www.msci.com/ |
| Verisk (incl. ISO, cat modeling) | Enterprise, custom (large six to seven figures) | Insurance risk, actuarial, claims, catastrophe data. Core of the insurance data world. | https://www.verisk.com/ |
| MT Newswires / Aiera / Chronograph / IBISWorld / Third Bridge / SS&C IntraLinks | Enterprise, custom | News, transcripts, PE monitoring, industry research, expert network, deal rooms. | — |

A single fundamental-equity analyst's "serious" stack (one terminal + CapIQ + PitchBook + Daloopa) lands around **$40,000–$70,000 per seat per year** before alt-data. That is the number the cheap stack is competing against.

---

### Tier B. Affordable analyst tools (public pricing)

| Source | Cost | What you get | Link |
|---|---|---|---|
| Koyfin (Teams) | ~$1,188 / yr | Leading low-cost Bloomberg-lite; screening, charting, fundamentals. | https://www.koyfin.com/ |
| YCharts | ~$3,600–$6,000 / yr (reported) | Fundamental analysis, visualisations, advisor-friendly. | https://ycharts.com/ |
| TradingView (Premium + data) | ~$800 / yr | Charting, retail data feeds. | https://www.tradingview.com/ |
| Godel Terminal | ~$996 / yr annual | Terminal-style UI at ~1/32 of Bloomberg. | https://www.godelterminal.com/ |
| Morningstar Investor (retail) | ~$249 / yr | Retail version of Morningstar; funds / ETFs. | https://www.morningstar.com/products/investor |

---

### Tier C. Developer / API data with MCP servers (public pricing, sign up in minutes)

| Source | Free tier | Paid | What you get | Link |
|---|---|---|---|---|
| Alpha Vantage (official MCP) | 25 req/day | $49.99–$249.99 / mo | Stocks, FX, crypto, 50+ indicators; NASDAQ-licensed. Real-time US data needs $99.99+. | https://mcp.alphavantage.co/ |
| Polygon.io / "Massive" (MCP) | ~5 req/min | ~$29–$199 / mo | Tick data, WebSocket streaming, low-latency US equities. | https://polygon.io/ |
| Financial Modeling Prep (hosted MCP) | Free key | ~$22–$99+ / mo | Fundamentals, SEC EDGAR data, earnings, ratios. | https://site.financialmodelingprep.com/developer/docs/mcp-server |
| Twelve Data (MCP) | Free tier | Low-cost paid | Global equities, FX, crypto, indicators. | https://twelvedata.com/ |
| Finnhub (community MCP) | 60 req/min | Low-cost paid | Real-time quotes + cheap alt-data: congressional trading, insider, lobbying, sentiment. | https://finnhub.io/ |
| Financial Datasets (MCP) | Limited free | Paid plans | Statements, prices, news; built for AI agents. | https://github.com/financial-datasets/mcp-server |

---

### Tier D. Free / open-source ($0, plus any paid keys you add)

| Source | Cost | What you get | Link |
|---|---|---|---|
| OpenBB Platform / ODP MCP | $0 | The hub: equities, fixed income, macro, options, ETF flows, CFTC; wraps free and paid providers. | https://github.com/OpenBB-finance/OpenBB |
| yfinance MCP (multiple builds) | $0 | Yahoo data: prices, fundamentals, options, news, screeners. Best build ~30 tools. | https://github.com/hachecito/yfinance-market-mcp |
| SEC EDGAR MCP | $0 | All public filings (10-K, 10-Q, 8-K, 13F). | https://github.com/stefanoamorelli/sec-edgar-mcp |
| FRED / Federal Reserve (via OpenBB) | $0 | Treasury rates, yield curve, macro series. | https://fred.stlouisfed.org/ |
| Local portfolio-analysis MCP | $0 | 25 skills, 102 tools, 15 adapters, no API key. | https://github.com/TensorBlock/awesome-mcp-servers/blob/main/docs/finance--crypto.md |

---

## Part 2. Can you get everything free? The honest ceiling

Short answer: you can build a genuinely useful research agent for $0, and you can run a real personal or prototype workflow on it. You cannot get the institutional layer free, because that layer is exactly what the money buys.

**What $0 gets you** (OpenBB + yfinance + SEC EDGAR + FRED + a local model):

- Public US large-cap fundamentals, filings, prices, and macro.
- A full agent loop: pull data via MCP, reason, assemble a document.
- Enough to learn, prototype, do personal investing, and generate ideas on liquid names.

**What $0 cannot get you, at any quality:**

- **Real-time licensed market data.** Exchanges, FINRA, and the SEC regulate this; free tiers are end-of-day or delayed. Real-time is a licensing cost, not a software cost.
- **Private-company financials.** PitchBook, Capital IQ, and Daloopa exist because this data is assembled by hand. There is no free mirror.
- **Credit ratings and risk scores** (Moody's, S&P, MSCI). Proprietary, licensed.
- **Institutional-grade fundamentals with audit trails.** Daloopa's 99% accuracy is 3.5M+ human hours of data ops. You cannot reproduce that with a model.
- **Insurance actuarial / catastrophe / claims data** (Verisk, RMS). This is the whole business of those firms.
- **Commercial redistribution rights.** This is the trap. Yahoo Finance data via yfinance is not licensed for commercial redistribution, and most free API tiers prohibit production or commercial use. A compliance team will flag a fund or bank shipping product on free-tier scraped data. Free is fine for internal research and prototypes; it is a legal problem the moment you productise or redistribute.

**The realistic free-path verdict:** free for learning, personal use, prototyping, and internal idea generation on public US names. Not free for anything real-time, private, alt-data-driven, redistributed, or regulated. The correct posture is *"free for the 80% that is public and slow, pay only for the 20% where quality or licensing is non-negotiable."*

---

## Part 3. The thesis stress-tested: open-source harness + local models, skip Rogo and Anthropic

Your instinct is half right, and the half that is right is the important half. Let me separate what is true from what is wishful.

### Where the thesis holds

The orchestration / harness layer is genuinely replaceable with open source. In 2026 the pieces all exist and are production-grade:

- **Orchestration frameworks:** LangGraph, AutoGen, Letta, Smolagents, PydanticAI. Smolagents and PydanticAI make zero assumptions about external services, making them the easiest fit for air-gapped financial workloads.
- **LLM gateways for governance and routing, self-hosted:** LiteLLM, Bifrost (Apache 2.0). These give you audit trails, budgets, failover, and keep prompts inside your perimeter.
- **Local model serving:** vLLM for high-throughput inference.
- **Local models:** Llama 3.3, Qwen 2.5 / 3.6 (MCP-native tool use, long context), Mistral.
- **MCP servers:** every source in Tier D, self-hosted, full source transparency, "no sensitive data leaves your control."

The air-gapped pattern is already documented for financial and defense workloads: open-source framework + locally hosted model + vector store + observability, no outbound internet. So the data-access plus orchestration plus document-generation pipeline that Rogo and Anthropic's finance templates perform is, architecturally, reproducible. For a security- or sovereignty-driven buyer (a bank that will not send data to a third party), this is not just viable — it is the preferred design.

### Where the thesis breaks

Three things money buys that you cannot self-host away:

1. **Frontier model reasoning on hard finance tasks.** This is measurable, not vibes. On the Vals AI Finance Agent benchmark, Claude Opus 4.7 scored 64.37%, ahead of GPT-5.5 (59.96%) and Gemini 3.1 Pro (59.72%). Local open models sit well below the frontier on multi-step financial reasoning. The fix is a hybrid: local model for the bulk (extraction, formatting, summarisation), frontier model via API for the hard reasoning step. You do not have to choose all-local or all-cloud.

2. **The proprietary data, which is the actual moat — not the harness.** Rogo and Anthropic are not valuable because of their orchestration; they are valuable because they sit on top of FactSet, Capital IQ, Daloopa, and the rest. Replacing the harness does nothing about the data. If your use case needs private-company data, credit ratings, real-time feeds, or audit-grade fundamentals, you are paying Tier A no matter whose harness runs on top. The harness is the cheap part of the stack. The data is the expensive part, and open source does not touch it.

3. **The compliance and trust surface.** "The harness" is not only orchestration. Anthropic's finance product bundles governed connectors, credential vaults, per-tool permissions, audit logs, human sign-off, and a SOC 2 posture. Self-hosting means you rebuild and own all of that, plus the regulatory burden: the SEC Division of Examinations is reviewing the accuracy of firms' AI claims, FINRA flags hallucination as a core risk, and the EU AI Act obligations land in August 2026. Self-hosting helps data residency; it does not remove the compliance work — it transfers it to you.

### The synthesis

Open-source harness, yes. Local models for the bulk, yes. But:

- Add a frontier model via API for the reasoning-hard steps. Route through a self-hosted gateway (LiteLLM) to keep audit and cost control.
- Use free and cheap data (Tier C and D) for everything public and slow.
- Pay for exactly one or two Tier A sources only where quality or licensing is non-negotiable for your specific use case. Daloopa is the usual answer for fundamentals because the value is "the number is right, with a citation."
- The thing you build and own is the validation, abstention, and audit layer that none of the off-the-shelf tools package for a niche. That is the defensible part, not the plumbing.

> **In one line:** You can fire the harness, but you cannot fire the data or the frontier model or the compliance work. Build the harness, rent the brain for the hard parts, and buy only the data that has no free equivalent.

---

## Part 4. Sector-by-sector: data needed and approximate cost

Each sector buys a different slice. Here is what the work actually requires, what is free-substitutable, and the rough seat cost.

### Banking (investment and corporate banking)

**Data needed:**

- Company fundamentals and filings: FactSet / Capital IQ / Daloopa, plus SEC EDGAR (free).
- M&A and private deal data: PitchBook / Capital IQ.
- Credit ratings and risk: Moody's / S&P.
- Real-time markets, rates, FX: Bloomberg / LSEG.
- KYC / AML and entity data: Moody's Orbis / LSEG World-Check.
- News and transcripts: MT Newswires / Bloomberg / Aiera.
- Internal documents: Egnyte / SharePoint.

**Approximate cost:** Heavy. A single banking-analyst seat stack (one terminal + Capital IQ + PitchBook) is roughly $40,000–$70,000 per year, plus KYC and compliance data licences. Banks run enterprise contracts in the millions.

**Free-substitutable:** Public-company research (EDGAR + FRED + yfinance) only. Nothing free covers private deals, credit ratings, KYC, or real-time licensed data. Banking is the least free-friendly sector — and the heaviest compliance load — which is also why the self-hosted, data-sovereign angle resonates most here.

---

### Insurance

**Data needed:**

- Risk, actuarial, and rating data: Verisk / ISO.
- Catastrophe modeling: Verisk / Moody's RMS.
- Credit and counterparty risk: Moody's / S&P.
- Economic and macro: FRED (free), Moody's Analytics.
- Claims and fraud data: Verisk.
- Asset-management-side market data: FactSet / Bloomberg.
- Regulatory filings: SEC EDGAR (free), NAIC.

**Approximate cost:** Verisk and RMS are enterprise, custom, typically large six to seven figures annually. The actuarial and catastrophe data is the product, so there is no cheap tier.

**Free-substitutable:** Macro (FRED) and public filings (EDGAR) are free. The core actuarial, catastrophe, and claims data has no free equivalent. The AI opportunity in insurance is less about market data and more about document-heavy workflows (claims, underwriting submissions, policy documents), which plays directly to the two workflows below.

---

### Hedge fund (varies sharply by strategy)

- **Fundamental long/short equity:** FactSet / Capital IQ + Daloopa (fundamentals and KPIs) + transcripts (Aiera / AlphaSense) + alt-data. Seat stack roughly $30,000–$60,000.
- **Quant / systematic:** Real-time and historical tick data (Bloomberg B-PIPE / Polygon / LSEG), reference data, alt-data. Cheap entry via Finnhub (congressional and insider data) and Polygon; serious historical tick is expensive. A quant fund's data bill runs into the hundreds of thousands to millions.
- **Credit / private credit:** PitchBook + Chronograph + Moody's + private documents.
- **Global macro:** Bloomberg / LSEG for rates and FX, plus FRED (free) for macro series.

**Free-substitutable:** A fundamental analyst gets surprisingly far on US large-caps with OpenBB + yfinance + SEC EDGAR + FRED for idea generation. It fails on real-time, private, alt-data, and anything traded at scale. Hedge funds are the most strategy-dependent: a fundamental fund can prototype cheaply, a quant fund cannot.

---

### One-line sector summary

| Sector | Cheapest credible entry | The thing with no free substitute |
|---|---|---|
| Banking | EDGAR + FRED for public research | KYC, real-time, private deals, credit ratings |
| Insurance | EDGAR + FRED + document workflows | Actuarial, catastrophe, claims data (Verisk/RMS) |
| Hedge fund (fundamental) | OpenBB + yfinance + EDGAR + FRED + one paid API | Real-time, alt-data, private fundamentals |
| Hedge fund (quant) | Polygon + Finnhub for prototyping | Historical tick, low-latency licensed feeds |

---

## Part 5. The two workflows you actually care about

You named the real product: assemble and update a document from many MCP inputs, and read Excel well. Both are buildable open-source, with one genuine hard part.

### Workflow 1: Pre-prepare and update a document from MCP inputs

This is exactly what Anthropic's pitch builder and earnings reviewer do, and it is reproducible:

- **Inputs:** MCP servers (OpenBB, SEC EDGAR, FRED, plus one paid data source if needed) supply the numbers and text.
- **Orchestration:** LangGraph or PydanticAI runs the pull-reason-write loop.
- **Model:** Local for extraction and formatting, frontier via API for the analytical narrative.
- **Output generation:** python-docx for Word, python-pptx for PowerPoint, openpyxl for Excel, or markdown to PDF. These are deterministic and reliable for generation.
- **"Update the document"** is the same loop pointed at an existing file: re-pull the data, diff, rewrite the changed cells or sections. Daloopa's one-click Excel update is the commercial version of this; it is replicable for public data.

This workflow is the strong, near-term, buildable product. It is mostly solved engineering, not research.

### Workflow 2: Read Excel well

This is the genuinely hard part, and worth being clear-eyed about. Naive approaches (dump the sheet to text, hand it to a model) fail on real financial models because of merged cells, formulas, multiple tabs, and formatting. The robust pattern:

- **Parse structure deterministically first.** openpyxl exposes cells, formulas, named ranges, and merged regions; pandas handles clean tabular blocks. Do not let the model guess structure it can read exactly.
- **Feed the model a structured representation** (cell coordinates, formula graph, labelled ranges), not raw text. The model reasons over structure; it does not reconstruct it.
- **Keep the deterministic layer authoritative for numbers,** and use the model for interpretation and narrative.

The polished commercial versions are Claude for Excel and the Daloopa Excel add-in. Open source gets you roughly 80% there with openpyxl plus a careful prompt; cell-level fidelity on complex, formula-heavy models is where it still breaks — and where a validation layer (does the extracted number reconcile?) earns its keep. This is, not coincidentally, the same validation-and-abstention layer that is the defensible wedge across the whole thesis.

---

## Bottom line

- **Cost:** A serious analyst seat is $40,000–$70,000 a year of data; the cheap APIs are $0–$250 a month; free open source is real but capped.
- **Free path:** Great for public, slow, internal, prototype work; illegal or impossible for real-time, private, alt-data, and redistributed work.
- **The thesis:** Fire the harness (open source it), rent the brain for hard reasoning (frontier API through a self-hosted gateway), buy only the data with no free substitute, and build the validation and audit layer yourself — because that is the part nobody packages for your niche.
- **Sectors:** Banking is the least free-friendly and most compliance-heavy (best fit for the data-sovereign pitch); insurance is document-workflow-driven; hedge funds split hard between cheap-to-prototype fundamental and expensive-to-run quant.
- **Product:** The document-assembly workflow is buildable now; reading Excel well is the hard 20% and the place your validation layer becomes the moat.
