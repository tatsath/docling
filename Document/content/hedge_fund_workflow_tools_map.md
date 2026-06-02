# Hedge Fund Workflows & Tools — Exhaustive Map
### Every major workflow, its components, the tools at each stage, what's being merged, and where an integrator adds value

**How to read this.** Each workflow is broken into its **lifecycle components** (e.g. research → validation → execution). Under each component is the **tool inventory** — incumbents, data vendors, and open-source. The recurring pattern across all of them: **tools are strong at producing an output, weak at proving it.** That gap (validation, source-cited numbers, cross-source reconciliation) is the integrator's wedge — consistent with the "evidence harness" thesis (the agent/tool is the workflow layer; the validated evidence layer is the trust layer, and the trust layer is the moat).

---

## WORKFLOW 1 — Quantitative / Systematic Trading

The most pipeline-like workflow: idea → data → signal → backtest → **validation** → execution → monitoring. Validation is a first-class stage here (overfitting is the enemy).

### 1.1 Data sourcing & management
- **Market/reference data:** [Bloomberg](https://www.bloomberg.com/professional/) (B-PIPE real-time feed, [BQL](https://www.liminfo.com/reference/bloombergref) query language, Data License), [LSEG/Refinitiv](https://www.lseg.com/en/data-analytics) (Tick History, Real-Time), [FactSet](https://www.factset.com/), [ICE Data Services](https://www.ice.com/market-data), [Polygon](https://polygon.io/), [Databento](https://databento.com/), [Tiingo](https://www.tiingo.com/).
- **Time-series database:** **[kdb+/KX](https://kx.com/)** (the quant standard for tick data), [ArcticDB](https://github.com/man-group/ArcticDB) (Man Group, open-source), [InfluxDB](https://www.influxdata.com/), [TimescaleDB](https://www.timescale.com/), [ClickHouse](https://clickhouse.com/).
- **Alt data:** [YipitData](https://www.yipitdata.com/) (consumer transactions), [M Science](https://mscience.com/), [Thinknum](https://www.thinknum.com/) (web-scraped: jobs, listings), [Quandl/Nasdaq Data Link](https://data.nasdaq.com/), [Earnest Analytics](https://www.earnestanalytics.com/), [Similarweb](https://www.similarweb.com/), orbital/geospatial vendors.
- **Data cleaning/validation vendors:** [YipitData and Quandl offer standardized, validated datasets](https://daloopa.com/blog/analyst-best-practices/the-growing-impact-of-alternative-data-on-hedge-fund-performance); funds also audit vendors for GDPR/CCPA compliance.

### 1.2 Research & signal development
- **Research environments:** [Jupyter](https://jupyter.org/), **[Bloomberg BQuant / BQNT](https://professional.bloomberg.com/products/bloomberg-terminal/research/bquant/)** (Jupyter + BQL + 17,000+ data items inside the Terminal, publishable as Launchpad apps), [Deepnote](https://deepnote.com/), [Hex](https://hex.tech/), [Zerve](https://www.zerve.ai/), [MATLAB](https://www.mathworks.com/products/matlab.html) (still strong for options pricing / econometrics).
- **Core libraries:** [NumPy](https://numpy.org/), [pandas](https://pandas.pydata.org/), [scipy](https://scipy.org/), [scikit-learn](https://scikit-learn.org/), [statsmodels](https://www.statsmodels.org/), [PyTorch](https://pytorch.org/)/[TensorFlow](https://www.tensorflow.org/) (ML signals), [Polars](https://pola.rs/) (fast dataframes).
- **Factor/portfolio research:** [Zipline-Reloaded](https://github.com/stefan-jansen/zipline-reloaded) **Pipeline API** (uniquely expressive for long/short equity factor research with dynamic universes), [Alphalens](https://github.com/stefan-jansen/alphalens-reloaded) (factor analysis), [quantstats](https://github.com/ranaroussi/quantstats) (tearsheets).

### 1.3 Backtesting (the engine)
- **Vectorized (fast research-phase screening):** **[vectorbt](https://github.com/polakowo/vectorbt)** (Numba-compiled, orders-of-magnitude speedup) / **[vectorbt PRO](https://vectorbt.pro/)**, [Backtesting.py](https://kernc.github.io/backtesting.py/).
- **Event-driven (realistic simulation):** **[Backtrader](https://www.backtrader.com/)**, **[Zipline-Reloaded](https://github.com/stefan-jansen/zipline-reloaded)**, **[QSTrader](https://github.com/mhallsmoore/qstrader)**.
- **Execution-realistic / HFT-grade:** **[NautilusTrader](https://nautilustrader.io/)** (order types, latency, sequencing, order-book depth — survives the jump to live), [Lean Engine](https://github.com/QuantConnect/Lean) (local).
- **Unified platform (research + backtest + live):** **[QuantConnect / LEAN](https://www.quantconnect.com/)** (multi-asset, managed + co-located live, 20+ broker integrations, EMSX Net's 1,300 liquidity providers; has an agentic assistant, "Mia"). Bloomberg BQuant for Terminal-resident equity backtests.
- **Curated catalog:** the [`awesome-systematic-trading`](https://github.com/edarchimbaud/awesome-systematic-trading) repo (~97 libraries) is the navigation map; per its own guidance — research speed → vectorbt, realistic sim → Backtesting.py/Backtrader, production HFT → NautilusTrader, crypto → [Freqtrade](https://www.freqtrade.io/)/[Jesse](https://jesse.trade/).

### 1.4 Validation (the moat stage — anti-overfitting)
- **Statistical:** walk-forward analysis, out-of-sample/holdout, combinatorial purged cross-validation (López de Prado), deflated Sharpe, PBO (probability of backtest overfitting).
- **Tools:** custom code mostly; [quantstats](https://github.com/ranaroussi/quantstats) and [Alphalens](https://github.com/stefan-jansen/alphalens-reloaded) for diagnostics; some teams use [MLflow](https://mlflow.org/) / [Weights & Biases](https://wandb.ai/) for experiment tracking and reproducibility.
- **The honest problem (Reddit/practitioner consensus):** the bottleneck is *not* alpha generation — it's iteration speed, validation rigor, and the [gap between what the backtest claims and what live execution delivers](https://www.zerve.ai/blog/backtesting-platforms-for-quant-funds). Reproducibility (can the chart be regenerated when data changes? can the choices be defended?) is the real differentiator.

### 1.5 Execution & OMS/EMS
- **EMS (execution):** [Bloomberg EMSX](https://www.bloomberg.com/professional/products/trading/sell-side/execution-management/), [SS&C Eze EMS](https://www.ezesoft.com/), [Virtu](https://www.virtu.com/), [FlexTrade](https://flextrade.com/), [TradingScreen](https://www.tradingscreen.com/).
- **Broker APIs (smaller funds):** [Interactive Brokers](https://www.interactivebrokers.com/) ([ib_insync](https://github.com/erdewit/ib_insync)), [Alpaca](https://alpaca.markets/), [ccxt](https://github.com/ccxt/ccxt) (crypto multi-exchange).
- **OMS:** see Workflow 4 (shared with discretionary).

### 1.6 Post-trade & TCA
- [**Bloomberg BTCA**](https://www.bloomberg.com/professional/products/trading/post-trade-services/btca/) (Transaction Cost Analysis — works across Bloomberg or third-party EMS/OMS, queryable via BQL/Python, exportable to PowerBI), [Virtu/ITG TCA](https://www.virtu.com/solutions/analytics/), [Abel Noser](https://www.abelnoser.com/), [big xyt](https://www.bigxyt.com/).

---

## WORKFLOW 2 — Fundamental / Discretionary Buy-Side (Public Equity, L/S)

Less pipeline, more judgment: idea sourcing → diligence → modeling → thesis → **thesis validation** → monitoring → decision.

### 2.1 Idea generation & screening
- [Bloomberg](https://www.bloomberg.com/professional/) (EQS equity screening, ANR analyst ratings), [FactSet](https://www.factset.com/), [S&P Capital IQ](https://www.spglobal.com/marketintelligence/en/solutions/sp-capital-iq-platform), [Koyfin](https://www.koyfin.com/), **[AlphaSense](https://www.alpha-sense.com/)** (thematic monitoring across public content).

### 2.2 Document research & diligence
- **AI-native research:** **[AlphaSense + Tegus](https://www.alpha-sense.com/)** (search across 500M+ docs — filings, 1,000+ broker-research sources, 240,000+ expert-call transcripts, news; agentic primers/SWOT; surpassed $500M ARR Oct 2025), **[Hebbia](https://www.hebbia.com/)** (multi-doc synthesis, "Generative Grid"), **[Rogo](https://www.rogo.ai/)**, **[Brightwave](https://www.brightwave.io/)**, **[Finster AI](https://www.finster.ai/)**, **[Samaya AI](https://www.samaya.ai/)**.
- **Expert networks ("Big Five"):** [AlphaSense-Tegus](https://www.alpha-sense.com/), [GLG](https://glginsights.com/), [Third Bridge](https://www.thirdbridge.com/), [AlphaSights](https://www.alphasights.com/), [Guidepoint](https://www.guidepoint.com/). ([Third Bridge is opening up](https://intuitionlabs.ai/articles/alphasense-alternatives-market-research) — integrations with Anthropic, Finster, Samaya, Rogo — vs. the walled-garden incumbents.)
- **Fundamental data (model-ready):** **[Daloopa](https://daloopa.com/)** (source-linked standardized fundamentals, MCP-exposed), [Canalyst](https://www.alpha-sense.com/) (now AlphaSense), FactSet, Capital IQ, Koyfin.

### 2.3 Financial modeling
- [Excel](https://www.microsoft.com/en-us/microsoft-365/excel) (still the universal substrate), with add-ins: Bloomberg (BDP/BDH/BDS formulas), Capital IQ, FactSet, [Daloopa](https://daloopa.com/) (auto-populate models from filings), [Macabacus](https://macabacus.com/), Daloopa Scout (Excel agent).

### 2.4 Thesis development & validation
- **Thesis pressure-testing:** [**LinqAlpha Devil's Advocate**](https://linqalpha.com/) — decomposes a thesis into assumptions, retrieves counterevidence from the user's *own* uploaded docs, generates source-linked rebuttals ([multi-agent on Claude via Bedrock; 5–10x manual speed](https://aws.amazon.com/blogs/machine-learning/how-linqalpha-assesses-investment-theses-using-devils-advocate-on-amazon-bedrock)). This is *reasoning validation* (anti-confirmation-bias), distinct from numerical validation.
- IC memo tools, internal wikis ([Notion](https://www.notion.so/), [Obsidian](https://obsidian.md/)).

### 2.5 Portfolio & risk monitoring
- Bloomberg [**PORT**](https://professional.bloomberg.com/products/bloomberg-terminal/portfolio-analytics/) (AI-enhanced portfolio & risk analytics), [**MARS**](https://www.bloomberg.com/professional/products/risk/) (Multi-Asset Risk System, stress/scenario), **MAC3** (multi-asset factor model), [**MSCI Barra**](https://www.msci.com/our-solutions/analytics/equity-factor-models) (factor models — Global/US Total Market Equity), [Axioma (Qontigo/SimCorp)](https://www.simcorp.com/en/products/axioma), [Northfield](https://www.northinfo.com/).

### 2.6 Output generation
- Investor decks, IC memos, LP letters — increasingly AI-drafted (LinqAlpha deck generation, internal Claude/Cowork workflows).

---

## WORKFLOW 3 — Private Credit / Direct Lending

Document-heavy, deterministic-number-critical, repetitive: origination → underwriting → **extraction/spreading** → covenant setup → **ongoing monitoring/validation** → reporting.

### 3.1 Deal sourcing & origination
- **Deal sourcing & origination:** [DealCloud](https://www.intapp.com/dealcloud/) (CRM for private markets), [Affinity](https://www.affinity.co/), internal pipelines.

### 3.2 Underwriting & document extraction
- **Specialized AI extractors:** **[Alkymi Private Credit](https://www.alkymi.io/)** (Data Inbox; extracts principal, rates, amortization, covenant ratios, borrower financials from Loan Agent Notices, Compliance Certificates, Financial Statements; **built-in cross-validation reconciling notices vs. agreement terms and validating leverage/coverage vs. covenants**), **[Cardo AI](https://cardoai.com/)** (ingests financials, computes EBITDA/leverage/ICR, real-time covenant tracking + full audit trail), **[V7 Go](https://www.v7labs.com/go)** (extracts covenants/default provisions/amendments at claimed 99%), **[Uptiq](https://uptiq.ai/)**, **[73 Strings](https://www.73strings.com/)** (99%+, SOC1/SOC2), **[Built](https://www.getbuilt.com/)** ($317B+ real-estate credit).
- **General parsers (assemble-your-own):** [Reducto](https://reducto.ai/), [Unsiloed](https://www.unsiloed.ai/), [LandingAI ADE](https://landing.ai/) (MCP-exposed), [Docling](https://github.com/docling-project/docling).

### 3.3 Covenant setup & monitoring (the validation core)
- Numerical rule validation: leverage = debt/EBITDA, ICR = EBITDA/interest, DSCR, LTV, headroom vs. threshold, tracked quarter-over-quarter.
- The incumbents above all do versions of this; the gap is the *bespoke* long tail (non-standard covenant definitions, adjusted-EBITDA add-backs in footnotes, one-off facility structures).

### 3.4 Portfolio management & reporting
- Allvue, Solovis, FIS, eFront (BlackRock), Clearwater; LP reporting and fund admin (see Workflow 4).

---

## WORKFLOW 4 — Operations / Middle & Back Office (cross-strategy)

The plumbing under every strategy: OMS/PMS → compliance → IBOR/accounting → reconciliation → fund admin → reporting.

### 4.1 OMS / PMS / EMS (front-to-back platforms)
- **Enfusion** (cloud-native front-to-back; now part of **Clearwater Analytics** — unified PM/OMS/IBOR/risk/reporting; strong at standardization, lighter on bespoke customization).
- **SS&C Eze** — modular **Eze Investment Suite**: Eze OMS, Eze EMS, **Eze Eclipse** (cloud front-to-back, single dataset).
- **Charles River (CRD, State Street)** — institutional IMS.
- **Others (Greenwich PMS/OMS list):** [Enfusion](https://www.enfusion.com/), [SS&C Eze Eclipse](https://www.ezesoft.com/), [FactSet](https://www.factset.com/) (incl. AlphaDesk), [LiquidityBook](https://www.liquiditybook.com/), [Nirvana](https://www.nirvanasolutions.com/), [Pinnakl](https://www.pinnakl.com/), [Limina](https://www.limina.com/), plus Athena/internal.

### 4.2 Compliance (pre- & post-trade)
- Built into OMS ([Eze](https://www.ezesoft.com/), [CRD](https://www.crd.com/), [Bloomberg AIM](https://www.bloomberg.com/professional/products/trading/buy-side/order-management-system-aim/) pre-trade compliance); [MSCI/Barra factor-limit checks at point of trade](https://www.ezesoft.com/insights/blog/strategic-tilts-managing-factor-exposure-real-time) (Eze+MSCI real-time factor exposure); Bloomberg **[Vault](https://www.bloomberg.com/professional/products/compliance/)**, **BRRS** (Regulatory Reporting).

### 4.3 IBOR / accounting / reconciliation
- [Clearwater Analytics](https://clearwateranalytics.com/), Enfusion IBOR, [SS&C](https://www.ssctech.com/), [Geneva (Advent)](https://www.advent.com/products/geneva), [FIS](https://www.fisglobal.com/); reconciliation engines ([Duco](https://du.co/), [SmartStream](https://www.smartstream-stp.com/), [Gresham](https://www.greshamtech.com/)).

### 4.4 Fund administration
- [SS&C GlobeOp](https://www.ssctech.com/solutions/global-fund-administration), [Citco](https://www.citco.com/), [NAV Consulting](https://www.navconsulting.net/), [Northern Trust](https://www.northerntrust.com/), [State Street](https://www.statestreet.com/); NAV calculation, investor allocations, capital accounts.

### 4.5 Risk & reporting (enterprise)
- Bloomberg PORT/MARS/MAC3, [MSCI RiskMetrics/Barra](https://www.msci.com/our-solutions/analytics), [Axioma](https://www.simcorp.com/en/products/axioma); regulatory (Form PF, AIFMD) via SS&C, Bloomberg BRRS.

---

## WORKFLOW 5 — Bloomberg as a cross-cutting spine (reference)

Because the user asked specifically, the Bloomberg stack mapped to where it sits:

| Bloomberg product | Layer | Workflow |
|---|---|---|
| **Terminal** (DES, GP, FA, EQS, ANR, N, TOP) | Research/data | 1, 2 |
| **BQL** (Bloomberg Query Language) | Programmatic data | 1, 2 |
| **B-PIPE** | Real-time feed | 1 |
| **Data License / BDP-BDH-BDS** | Bulk + Excel data | 1, 2, 3 |
| **BQuant / BQNT** | Python research + backtest | 1, 2 |
| **AIM** (Asset & Investment Manager) | OMS / front-to-back | 1, 2, 4 |
| **EMSX** | Execution | 1, 2 |
| **PORT** | Portfolio & risk analytics | 2, 4 |
| **MARS** | Multi-asset risk, stress | 2, 4 |
| **MAC3** | Multi-asset factor model | 2, 4 |
| **BTCA** | Transaction cost analysis | 1 |
| **TOMS** | Sell-side fixed-income OMS | (sell-side) |
| **Vault / BRRS** | Compliance / reg reporting | 4 |

The strategic point: Bloomberg is trying to be the *whole* spine (data → research → execution → risk → compliance). Most funds still run a **best-of-breed mix** — Bloomberg data + a separate OMS (Eze/Enfusion) + separate risk (MSCI) + separate AI research (AlphaSense) — which is precisely why integration is a standing problem.

---

## What's actually being merged (integration patterns observed)

1. **Data vendor → OMS (real-time):** SS&C Eze embeds **MSCI Barra** factor coefficients directly into Eze OMS for pre-trade factor-exposure checks. Pattern: risk model fused into the execution path.
2. **TCA across any EMS/OMS:** Bloomberg **BTCA** ingests from Bloomberg *or* third-party EMS/OMS — a vendor-neutral analytics layer over heterogeneous execution.
3. **Research platform → expert content:** AlphaSense **absorbed Tegus/Canalyst/BamSEC**; expert networks (Third Bridge) **integrate into AI platforms** (Anthropic, Rogo, Finster). Pattern: content + synthesis converging.
4. **Front-to-back consolidation:** **Enfusion → Clearwater**; SS&C Eze Eclipse — single dataset across PM/OMS/IBOR/reporting. Pattern: collapse the silos into one platform.
5. **Fundamental data → model (MCP/agent):** **Daloopa MCP** feeds Claude/ChatGPT; Daloopa Scout auto-populates Excel. Pattern: structured data piped straight into the analyst's tool via agent protocol.
6. **Agentic assistants inside platforms:** QuantConnect **Mia**, Bloomberg BQuant publishing, FactSet AI Document Search (85,000-user beta, Mar 2026). Pattern: an agent layer bolted onto each incumbent.

The meta-pattern: **everyone is bolting an agent and consolidating data, but the cross-platform "trusted number with its source" layer is still missing** — each platform validates within its own walls, not across the messy mix a real fund runs.

---

## The integrator wedge (aligned to the evidence-harness thesis)

Across all five workflows, the same structural truth holds: **the tools generate outputs; they do not prove them across sources.** That is the integrator's space. Concretely:

1. **Quant:** the gap is backtest-vs-live and reproducibility/validation rigor — not another backtester. An integrator adds the validation harness (walk-forward discipline, experiment tracking, defensible reproducibility) and wires data → research → execution cleanly.
2. **Fundamental:** the gap is *trusted, source-cited numbers* feeding the model and *thesis validation* — assembling Daloopa/AlphaSense + a validation layer, not rebuilding research search.
3. **Private credit:** the gap is the *bespoke* document long tail and portable validation — where Alkymi/Cardo (standing platforms) are weakest, and where a file-first, validation-first engine fits.
4. **Ops:** the gap is reconciliation and cross-system data cohesion — exactly what funds complain about when running Bloomberg + Eze + MSCI + AlphaSense.

**The consistent integrator play:** be the **validation + orchestration layer that sits across the best-of-breed mix a fund already runs**, encoding finance-specific rule checks, source-cited numbers, abstention, and cross-source reconciliation — delivered model-and-platform-agnostic (MCP/API) so it plugs into Bloomberg/Eze/Enfusion/AlphaSense/Cowork rather than replacing them. The edge is never the pipeline (commodity); it is the *domain judgment encoded as validation rules* + the *specific workflow you know best* + the *trust earned serving real funds*.

**Where to start:** the workflow with (a) expensive mistakes, (b) repetitive documents, (c) weak incumbent validation, and (d) a mix of systems no one has stitched. Private-credit bespoke monitoring and fundamental "trusted-number" feeds score highest; pure quant backtesting is the most commoditized and the hardest to differentiate in.
