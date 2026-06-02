# Knowledge Base — AI in Hedge Funds, RIAs & Asset Management
### The consultant/integrator's reference: who the players are, what's being bought, what practitioners actually say, and how to position

**Purpose.** A single reference to consult from when advising or integrating for investment firms. It maps the *vendor and startup landscape* across every segment (institutional research, document AI, private credit, RIA/wealth, infrastructure), the *buyer reality*, the *practitioner signal*, and the *integrator playbook*. Pair it with the companion docs: `solution_architecture_spec.md` (the build options + validation engine), `benchmark_plan.md` (the proof artifact), and `hedge_fund_workflow_tools_map.md` (the workflow-by-workflow tool map).

**The thesis that runs through all of it (your "evidence harness").** The model/agent is the *workflow* layer. The validated, source-cited evidence layer is the *trust* layer. In finance the trust layer is the moat. Every category below is strong at producing output and weak at proving it — and the proving is where an integrator with finance judgment adds value that doesn't commoditize.

---

## PART 1 — The market context

- The space is loud and well-funded. NY-based AI research startups alone [raised ~$700M in the year to Dec 2025](https://yellow.com/news/wall-street-embraces-ai-new-york-startups-raise-dollar700-million-for-research-tools); [Hebbia](https://www.hebbia.com/) is reportedly valued ~$700M with customers like Charlesbank and Oak Hill Advisors paying "tens of thousands to millions"; [Rogo](https://www.rogo.ai/) was valued at $350M (Thrive, Khosla).
- On the wealth side, [generative-AI adoption among advisors jumped ~11 points in a year, and the T3 survey went from tracking one AI notetaker to fourteen](https://wealthtechtoday.com/2026/05/08/ai-notetakers-financial-advisors-2026/); [Jump and Zocks together raised >$170M](https://wealthtechtoday.com/2026/05/08/ai-notetakers-financial-advisors-2026/).
- The structural truth across both: **content exclusivity is eroding** (research providers partner directly with AI platforms), so the durable value is shifting from *having the data* to *trusted synthesis + validation on a firm's own data*.

---

## PART 2 — The startup & vendor census (by category, with links)

### 2.1 AI-native research & synthesis (institutional)
The most crowded category. All do document Q&A / synthesis / drafting; they differ on content access and depth.
- **[Hebbia](https://www.hebbia.com/)** — Matrix grid, "Full Attention" / ISD; multi-doc synthesis & diligence; user-uploaded docs + [integrations with FactSet, PitchBook, S&P Capital IQ, Preqin](https://www.hebbia.com/resources/financial-research-platforms). Strong synthesis, weaker on structured/Excel data.
- **[AlphaSense](https://www.alpha-sense.com/)** (+ [Tegus](https://www.tegus.com/)) — market intelligence over 500M+ docs incl. 1,000+ broker-research sources & 240,000+ expert transcripts; $500M+ ARR; agentic diligence workflows.
- **[Rogo](https://www.rogo.ai/)** — purpose-built for investment banking; research synthesis, doc Q&A, data retrieval; serves IB, hedge funds, PE, asset management.
- **[Brightwave](https://www.brightwave.io/)** — private-markets / research synthesis from a corpus of news, filings, transcripts, sell-side research; founded by ex-Databricks/Meta/Goldman engineers; ~$21M raised.
- **[Finster AI](https://www.finster.ai/)** — UK→US; drafts investment memos, research, client materials for IBs & asset managers; ~$15M raised; ex-Morgan Stanley COO.
- **[Samaya AI](https://www.samaya.ai/)** — knowledge-agent platform for financial services.
- **[BlueFlame AI](https://www.blueflame.ai/)** — generative AI specifically for alternative asset managers.
- **Smaller/emerging:** [AgentSmyth](https://www.agentsmyth.com/), [ModelML](https://www.modelml.com/), [ProSights](https://www.prosights.co/), [Pints AI](https://www.pints.ai/), [Quilr](https://www.quilr.ai/).
- **Buy-side specialist:** [LinqAlpha](https://linqalpha.com/) — domain-specialized multi-agent for 170+ institutional investors; Devil's Advocate (thesis pressure-testing), company screener, primers, catalyst mapping.

### 2.2 Document parsing / extraction (the layer you'd assemble on)
- **[Reducto](https://reducto.ai/)** — parsing + extraction, official MCP, 3B+ pages, multi-pass agentic OCR, bounding-box citations; powers Harvey, Rogo, Scale.
- **[Unsiloed AI](https://www.unsiloed.ai/)** — vision-first dual-stream parsing, schema-conditioned with cross-field constraints, word-level citations; Fortune-150 banks.
- **[LandingAI (ADE)](https://landing.ai/)** — layout-aware extraction over MCP with page indexes + bounding boxes.
- **[Daloopa](https://daloopa.com/)** — pre-built source-linked public-company fundamentals (5,500+ tickers, 14yr); MCP-exposed; FinRetrieval benchmark.
- **[Extend](https://www.extend.ai/)**, **[V7 Go](https://www.v7labs.com/go)**, **[Ocrolus](https://www.ocrolus.com/)** (bank statements), **[Hyperscience](https://www.hyperscience.com/)**, **[Instabase](https://instabase.com/)** — document-AI / IDP players.
- **Open-source parsers:** [Unstructured](https://github.com/Unstructured-IO/unstructured) (30+ formats), [Docling](https://github.com/docling-project/docling) (IBM), [Marker](https://github.com/VikParuchuri/marker), [MarkItDown](https://github.com/microsoft/markitdown) (Microsoft), [Apache Tika](https://tika.apache.org/).

### 2.3 Private credit / direct lending
- **[Alkymi](https://www.alkymi.io/)** — Private Credit product; extraction + built-in cross-validation of covenant ratios.
- **[Cardo AI](https://cardoai.com/)** — private-debt servicing/monitoring; EBITDA/leverage/ICR computation, real-time covenant tracking + audit trail.
- **[73 Strings](https://www.73strings.com/)** — private-markets valuation & monitoring; 99%+ accuracy, SOC1/SOC2.
- **[Uptiq](https://uptiq.ai/)**, **[Built](https://www.getbuilt.com/)** (real-estate credit), **[V7 Go](https://www.v7labs.com/go)** (covenant extraction).
- **Portfolio admin:** [Allvue](https://www.allvuesystems.com/), [Solovis](https://www.solovis.com/), [eFront](https://www.efront.com/).

### 2.4 RIA / wealth management (a distinct, fast-moving ecosystem)
Tracked weekly by [Kitces #AdvisorTech](https://www.kitces.com/blog/) and the [Ezra Group / WealthTech Today](https://wealthtechtoday.com/) reports.
- **AI notetakers / "advisor OS":** **[Jump](https://jump.ai/)** (claims ~1 in 10 US advisors; meeting prep, NL search, doc extraction), **[Zocks](https://www.zocks.io/)** (meeting capture → structured data → CRM automation, forms/intake), [Pulse360](https://www.pulse360.com/), [Zeplyn](https://www.zeplyn.ai/), [Finmate AI](https://finmate.ai/), [Contio (MeetingOS)](https://www.kitces.com/blog/the-latest-in-financial-advisortech-march-2026-altruist-jump-zocks-ria-custodian/).
- **CRM (RIA-specific):** [Wealthbox](https://www.wealthbox.com/), [Redtail](https://corporate.redtailtechnology.com/), [Practifi](https://www.practifi.com/), [Salesforce Financial Services Cloud](https://www.salesforce.com/financial-services/), [Altitude](https://gainaltitude.ai/).
- **Portfolio management / reporting (PMS):** [Orion](https://orion.com/), [Black Diamond (SS&C Advent)](https://www.advent.com/products/black-diamond), [Addepar](https://addepar.com/), [Tamarac (Envestnet)](https://www.envestnet.com/), [Panoramix](https://www.panoramixinc.com/).
- **Financial planning:** [eMoney](https://emoneyadvisor.com/), [MoneyGuidePro (Envestnet)](https://www.moneyguide.com/), [RightCapital](https://www.rightcapital.com/), [Wealth.com](https://www.wealth.com/) (estate), [Nitrogen](https://nitrogenwealth.com/) (risk/proposal).
- **Custodians (with AI moving in):** [Schwab](https://www.schwab.com/), [Fidelity](https://www.fidelity.com/), [Pershing (BNY)](https://www.pershing.com/), **[Altruist](https://altruist.com/)** (Hazel AI tax planning).
- **Note the dynamic:** standalone notetakers (Jump/Zocks) outran CRM-native ones; [tax planning is the next commoditizing wave](https://www.kitces.com/blog/the-latest-in-financial-advisortech-march-2026-altruist-jump-zocks-ria-custodian/). The meeting layer is becoming the "control plane" for the advisor stack.

### 2.5 Institutional infrastructure (the incumbents you integrate around)
- **Data terminals:** [Bloomberg](https://www.bloomberg.com/professional/), [LSEG/Refinitiv](https://www.lseg.com/), [FactSet](https://www.factset.com/), [S&P Capital IQ](https://www.spglobal.com/marketintelligence/), [Morningstar Direct](https://www.morningstar.com/products/direct) (+ [PitchBook](https://pitchbook.com/) private markets), [Koyfin](https://www.koyfin.com/).
- **OMS/EMS/PMS:** [Enfusion (Clearwater)](https://www.enfusion.com/), [SS&C Eze](https://www.ezesoft.com/), [Charles River (State Street)](https://www.crd.com/), [Bloomberg AIM](https://www.bloomberg.com/professional/products/trading/buy-side/order-management-system-aim/).
- **Risk:** [MSCI Barra/RiskMetrics](https://www.msci.com/our-solutions/analytics), [Axioma (SimCorp)](https://www.simcorp.com/en/products/axioma), [Northfield](https://www.northinfo.com/), Bloomberg [PORT/MARS](https://www.bloomberg.com/professional/products/risk/).
- **Quant/backtest:** [QuantConnect/LEAN](https://www.quantconnect.com/), [vectorbt](https://vectorbt.pro/), [NautilusTrader](https://nautilustrader.io/), [Backtrader](https://www.backtrader.com/), [Zipline-Reloaded](https://github.com/stefan-jansen/zipline-reloaded), [kdb+/KX](https://kx.com/).
- **Alt data:** [YipitData](https://www.yipitdata.com/), [M Science](https://mscience.com/), [Thinknum](https://www.thinknum.com/), [Earnest](https://www.earnestanalytics.com/), [Similarweb](https://www.similarweb.com/).
- **Fund admin / ops:** [SS&C GlobeOp](https://www.ssctech.com/), [Citco](https://www.citco.com/), [Northern Trust](https://www.northerntrust.com/), [State Street](https://www.statestreet.com/); reconciliation [Duco](https://du.co/), [SmartStream](https://www.smartstream-stp.com/), [Gresham](https://www.greshamtech.com/).
- **Vendor-platform AI:** [Anthropic Claude for Financial Services](https://www.anthropic.com/solutions/financial-services), [FactSet AI Document Search](https://www.factset.com/), QuantConnect "Mia", Robinhood "Cortex" (retail), [Arta AI](https://artafinance.com/) (retail/UHNW).

### 2.6 The open-source assembly kit (what an integrator builds with)
- **Turnkey RAG platforms:** [RAGFlow](https://github.com/infiniflow/ragflow), [R2R](https://github.com/SciPhi-AI/R2R), [Morphik](https://github.com/morphik-org/morphik-core), [RAG-Anything](https://github.com/HKUDS/RAG-Anything), [Onyx](https://github.com/onyx-dot-app/onyx), [Verba](https://github.com/weaviate/Verba), [Dify](https://github.com/langgenius/dify), [Haystack](https://github.com/deepset-ai/haystack).
- **Orchestration / framework:** [LlamaIndex](https://www.llamaindex.ai/), [LangChain/LangGraph](https://www.langchain.com/langgraph) — both [connect to external APIs, databases, and MCP servers natively](https://medium.com/@pedroazevedo6/build-llamaindex-agents-with-mcp-connector-69df32d95508).
- **Vector DBs:** [Qdrant](https://qdrant.tech/), [Weaviate](https://weaviate.io/), [pgvector](https://github.com/pgvector/pgvector), [Milvus](https://milvus.io/).
- **Reranking:** [Cohere Rerank](https://cohere.com/rerank) (API), [bge-reranker-v2](https://huggingface.co/BAAI/bge-reranker-v2-m3) / [RAGatouille](https://github.com/AnswerDotAI/RAGatouille) (ColBERT, open).
- **Retrieval technique:** [Anthropic Contextual Retrieval](https://www.anthropic.com/news/contextual-retrieval).
- **Validation / eval:** [RAGAS](https://github.com/explodinggradients/ragas), [TruLens](https://github.com/truera/trulens), [DeepEval](https://github.com/confident-ai/deepeval), [Arize Phoenix](https://github.com/Arize-ai/phoenix).
- **Catalog/navigation:** [RAGHub](https://github.com/Andrew-Jang/RAGHub), [awesome-systematic-trading](https://github.com/edarchimbaud/awesome-systematic-trading).

---

## PART 3 — What practitioners actually say (Reddit & analyst signal)

- **Quant (r/quant, r/algotrading, practitioner blogs):** the bottleneck is *not* alpha generation — it's [iteration speed, validation rigor, and the gap between backtest and live execution](https://www.zerve.ai/blog/backtesting-platforms-for-quant-funds). Reproducibility and defensible choices matter more than another backtester. Zipline is widely seen as [aging/under-maintained](https://forextester.com/blog/backtrader-alternatives/); vectorbt for speed, NautilusTrader for execution realism.
- **Document AI / RAG (r/Rag, r/LocalLLaMA, practitioner posts):** parsers self-report [85–95% on clean docs, 70–85% on scanned/low-quality](https://dev.to/melek_messoussi_651bf64f4/i-built-a-production-ready-document-parser-for-rag-apps-that-actually-handles-complex-tables-full-3lgn); the universal advice is **always validate before production** and **don't trust naive top-k** for hard questions. Tables and footnotes are where everything breaks.
- **Validation reality:** [Stanford measured 17–33% hallucination across leading legal-RAG tools](https://galileo.ai/blog/rag-evaluation-tools); [other research up to 40% even when the right info was retrieved](https://www.getmaxim.ai/articles/rag-evaluation-a-complete-guide-for-2025/). The whole industry is weak at exactly what funds say they care about — that's the opening.
- **RIA (Kitces, Ezra Group):** [70% of RIAs now use AI for meeting documentation](https://jump.ai/advisor-trends/artificial-intelligence/jump-vs-zocks) — the #1 use case; adoption (not features) decides success; advisors abandon anything that adds steps.
- **Cowork / live-agent cost:** practitioners flag [high usage-quota consumption and slower-than-Claude-Code performance](https://aimaker.substack.com/p/claude-cowork-review-agentic-ai-guide) — the live-reading-as-retrieval anti-pattern.

---

## PART 4 — The buyer landscape (who you'd sell to, and how they buy)

| Buyer | What they run today | Pain | How they buy |
|---|---|---|---|
| **Quant / systematic fund** | kdb+, in-house backtest, Bloomberg/LSEG data | backtest↔live gap, reproducibility | technical, eng-led, fast if value is proven |
| **Fundamental L/S hedge fund** | Bloomberg + AlphaSense + Excel + internal notes | trusted numbers into models; thesis rigor | analyst-driven; trial → adopt; trust matters |
| **Private credit fund** | Email + Excel + DealCloud + a point tool | bespoke covenant docs; wrong number = loss | ops/credit-led; values audit trail & SOC2 |
| **RIA / wealth firm** | CRM + PMS + planning + notetaker | meeting→CRM ops; capacity; compliance | principal-led; low-code; price-sensitive |
| **Asset manager (long-only)** | Front-to-back (Enfusion/Eze/CRD) + risk | data cohesion; reconciliation | procurement-heavy; long cycle; needs certs |

Universal procurement gates for institutional buyers: **SOC 2, data lineage, redundancy/SLA, references, indemnification, data ownership.** Incumbents spent years earning this trust — it's a barrier *and* the reason an integrator who handles it is valued.

---

## PART 5 — The integrator consulting playbook (aligned to your blogs)

Your edge is **not** the pipeline (commodity) — it's *finance judgment encoded as validation*, *depth in one workflow*, and *trust earned serving real funds*. The playbook:

### Step 1 — Lead with forward-deployed consulting, not a product
Mirror the model that's working (e.g. [StarterStack embeds engineers and cuts false alerts ~70%](https://www.blog.brightcoding.dev/2026/05/22/stop-wasting-hours-hunting-quant-tools-awesome-systematic-trading-has-97-libraries)). Go into a fund, assemble the right commodity stack on *their* infrastructure (AWS/Azure/air-gapped — see `solution_architecture_spec.md`), encode *their* finance rules, and prove it against their current workflow with the [head-to-head benchmark](./benchmark_plan.md). Low capital, immediate revenue, and you discover where the repeated pain is.

### Step 2 — Pick ONE workflow where you have an edge
Score each on: (a) expensive mistakes, (b) repetitive documents, (c) weak incumbent validation, (d) un-stitched systems. Highest scorers: **private-credit bespoke covenant monitoring** and **fundamental "trusted-number" feeds**. Avoid pure quant backtesting (commoditized) and horizontal "files→answers" (Glean/Hebbia/Unstructured own it).

### Step 3 — Build the validation layer as the IP
The five-layer validation engine (parser-level → retrieval → faithfulness → **finance rules** → abstention + human queue) from `solution_architecture_spec.md` §3. The finance rule layer (leverage, ICR, tie-outs, unit/period normalization, covenant math) is the only defensible code — no OSS does it.

### Step 4 — Prove it with a benchmark, on their documents
In this market the demo beats the deck. Lead with: *"On your own N documents — baseline answered X, flagged none of its errors; assembled stack answered Y, cited every number, flagged the rest — at Zx lower cost, Wx faster."*

### Step 5 — Productize narrowly, only after consulting reveals the repeatable workflow
Package the one repeated thing as a thin, model-and-platform-agnostic **MCP server / connector** that plugs into Claude/Cowork/Bedrock/Copilot — the verification primitive the incumbents call when a number must be exact. De-risked by real customers by the time you build it.

### Positioning line (for your blogs / pitch)
*"The next wave of AI in finance won't be won by agents alone. It will be won by evidence harnesses that make agents trustworthy. I assemble best-in-class parsing and retrieval into your platform, and I build the financial validation and audit layer the off-the-shelf tools don't — so your analysts get source-cited, rule-checked, abstention-aware numbers, not a confident guess."*

---

## PART 6 — Honest risks (so you go in clear-eyed)

1. **The pipeline is commoditizing** — RAGFlow/Morphik exist, Contextual Retrieval is published, rerankers are open. Selling "I set up RAG" = consultant competing on price. Defense: depth + proprietary benchmark + a compounding data asset (a growing library of covenant structures / templates / observed breaches, the way [Daloopa's verified data points are a durable moat](https://daloopa.com/how-our-ai-works)).
2. **Niches are filling** — covenant monitoring already has Alkymi/Cardo/73 Strings/V7 with funding + SOC2. Enter via the *bespoke long tail* and the *file-first/ephemeral* angle they serve poorly, or an adjacent under-served niche.
3. **"Sell to Anthropic" is an outcome, not a plan** — be the indispensable private-docs evidence layer their finance agents call (the way Daloopa/Moody's are connectors); acquisition interest follows on its own.
4. **Trust/procurement is slow** — budget for SOC 2 and long institutional cycles; this is why consulting-first (faster revenue, builds the references) beats product-first.

---

## PART 7 — Quick-reference link index

**Benchmarks/research:** [OfficeQA Pro](https://arxiv.org/abs/2603.08655) · [ParseBench](https://www.llamaindex.ai/blog/parsebench) · [FinRetrieval/Daloopa](https://daloopa.com/) · [MCP-vs-RAG study](https://arxiv.org/pdf/2603.27752)
**Anthropic:** [Contextual Retrieval](https://www.anthropic.com/news/contextual-retrieval) · [Claude for Financial Services](https://www.anthropic.com/solutions/financial-services) · [Claude Cowork](https://www.anthropic.com/product/claude-cowork) · [PDF token docs](https://platform.claude.com/docs/en/build-with-claude/pdf-support)
**Research AI:** [Hebbia](https://www.hebbia.com/) · [AlphaSense](https://www.alpha-sense.com/) · [Rogo](https://www.rogo.ai/) · [Brightwave](https://www.brightwave.io/) · [Finster](https://www.finster.ai/) · [LinqAlpha](https://linqalpha.com/) · [BlueFlame](https://www.blueflame.ai/)
**Parsing:** [Reducto](https://reducto.ai/) · [Unsiloed](https://www.unsiloed.ai/) · [LandingAI](https://landing.ai/) · [Daloopa](https://daloopa.com/) · [Unstructured](https://github.com/Unstructured-IO/unstructured) · [Docling](https://github.com/docling-project/docling)
**Private credit:** [Alkymi](https://www.alkymi.io/) · [Cardo AI](https://cardoai.com/) · [73 Strings](https://www.73strings.com/) · [V7 Go](https://www.v7labs.com/go) · [Built](https://www.getbuilt.com/)
**RIA/wealth:** [Jump](https://jump.ai/) · [Zocks](https://www.zocks.io/) · [Orion](https://orion.com/) · [Addepar](https://addepar.com/) · [Altruist](https://altruist.com/) · [Kitces AdvisorTech](https://www.kitces.com/blog/) · [WealthTech Today](https://wealthtechtoday.com/)
**Infra:** [Bloomberg](https://www.bloomberg.com/professional/) · [Enfusion](https://www.enfusion.com/) · [SS&C Eze](https://www.ezesoft.com/) · [Charles River](https://www.crd.com/) · [MSCI](https://www.msci.com/) · [QuantConnect](https://www.quantconnect.com/) · [kdb+/KX](https://kx.com/)
**OSS RAG:** [RAGFlow](https://github.com/infiniflow/ragflow) · [R2R](https://github.com/SciPhi-AI/R2R) · [Morphik](https://github.com/morphik-org/morphik-core) · [RAG-Anything](https://github.com/HKUDS/RAG-Anything) · [LlamaIndex](https://www.llamaindex.ai/) · [LangGraph](https://www.langchain.com/langgraph) · [RAGAS](https://github.com/explodinggradients/ragas) · [RAGHub](https://github.com/Andrew-Jang/RAGHub)
