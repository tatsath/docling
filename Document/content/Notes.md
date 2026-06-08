# Solution Architecture & Validation Engine Specification
### Assembled document-intelligence stacks for hedge funds — six production options, mapped to AWS / Azure / Microsoft 365 / cloud-agnostic, with a dedicated validation engine

---

## 0. The mental model (one diagram, in words)

Every option below is the **same six-layer pipeline**. What changes is *which vendor/platform fills each layer* and *where the validation lives*. The agent goes on **top**, not at the bottom — the fund's core mistake (via Cowork) is using the agent *as* the retrieval engine.

```
                 ┌─────────────────────────────────────────────┐
   Analyst  ───► │  LAYER 6: AGENT / ORCHESTRATION SURFACE       │  Claude Code / Cowork /
   question      │  (plan, decompose, synthesize, draft)          │  Managed Agent / Copilot Studio
                 └───────────────────────┬─────────────────────-─┘
                                         │ sends only validated, compact evidence
                 ┌───────────────────────▼─────────────────────-─┐
                 │  LAYER 5: VALIDATION ENGINE  ◄── YOUR IP        │  faithfulness + finance rules
                 │  (faithfulness, rule checks, abstention, cite)  │  + abstention + human queue
                 └───────────────────────▲─────────────────────-─┘
                 ┌───────────────────────┴─────────────────────-─┐
                 │  LAYER 4: GENERATION (strong model)            │  Claude Opus
                 └───────────────────────▲─────────────────────-─┘
                 ┌───────────────────────┴─────────────────────-─┐
                 │  LAYER 3: HYBRID RETRIEVAL + RERANK            │  vector + BM25 → cross-encoder
                 └───────────────────────▲─────────────────────-─┘
                 ┌───────────────────────┴─────────────────────-─┐
                 │  LAYER 2: CONTEXTUAL CHUNKING + DUAL INDEX     │  Contextual Retrieval + Qdrant/OpenSearch/AI Search
                 └───────────────────────▲─────────────────────-─┘
                 ┌───────────────────────┴─────────────────────-─┐
   Documents ──► │  LAYER 1: PARSING (structure-preserving)       │  Reducto / Unsiloed / LandingAI ADE
                 └─────────────────────────────────────────────┘

   ONE-TIME (per document): Layers 1–2.   PER QUERY (cheap/fast): Layers 3–6.
```

**Why this is cheap and fast vs Cowork:** Cowork re-ingests raw PDFs into context every task ([100k–1M+ tokens, incl. vision tokens](https://platform.claude.com/docs/en/build-with-claude/pdf-support), with agent-loop and sub-agent multipliers). The pipeline parses once, indexes once, then sends ~3–10k tokens of the *exact right evidence* per query.

**Why this is accurate:** structured parsing ([worth a measured +16% in grounded-reasoning benchmarks](https://arxiv.org/abs/2603.08655)), contextual chunking + reranking ([cuts retrieval failures ~67%](https://www.anthropic.com/news/contextual-retrieval)), and the validation engine that the agent-only approach has no equivalent of.

---

## 1. Priority order of the stack (applies to ALL options)

Build/fix in this order — each layer's value depends on the one before it:

1. **Parsing** — fix first; garbage in = garbage out. Biggest single accuracy lever.
2. **Contextual chunking + indexing** — cheapest high-leverage win (~$1/M doc tokens, ~67% retrieval-failure reduction when combined with rerank).
3. **Hybrid retrieval + reranking** — biggest accuracy lever after parsing.
4. **Generation** with a strong model on compact evidence — where cost collapses.
5. **Validation engine** — what makes it audit-grade; the differentiator.
6. **Agent surface + orchestration** — the flexible analyst layer, on top.

---

## 2. The six options — exhaustive

### Option A — AWS Bedrock-native
**For:** funds already running on AWS.

| Layer | Component |
|---|---|
| 1 Parse | [Reducto](https://reducto.ai/) or [LandingAI ADE](https://landing.ai/) (NOT Bedrock's default chunker — it mangles financial tables) |
| 2 Index | [Bedrock Knowledge Bases](https://aws.amazon.com/blogs/machine-learning/amazon-bedrock-knowledge-bases-now-supports-hybrid-search/) → OpenSearch Serverless (managed chunk/embed/store) |
| 3 Retrieve | Bedrock KB [hybrid search](https://aws.amazon.com/blogs/machine-learning/amazon-bedrock-knowledge-bases-now-supports-hybrid-search/) (semantic + BM25) → [Cohere Rerank](https://cohere.com/rerank) (on Bedrock) |
| 4 Generate | [Claude (Opus) via Bedrock](https://aws.amazon.com/bedrock/claude/) |
| 5 Validate | Bedrock Guardrails + your faithfulness + finance rule layer |
| 6 Agent | Claude Code / Cowork / Bedrock Agents |

**Data flow:** docs → S3 → Reducto parse → KB ingest (chunk/embed → OpenSearch) → query: hybrid retrieve → Cohere rerank → Claude on Bedrock → validation → agent.
**Pros:** managed RAG (no vector-DB ops), native S3/SharePoint/Salesforce connectors, Claude is first-class on Bedrock, VPC + private networking, this *is* [LinqAlpha's real architecture](https://aws.amazon.com/blogs/machine-learning/how-linqalpha-assesses-investment-theses-using-devils-advocate-on-amazon-bedrock) (Textract → OpenSearch → Claude on Bedrock).
**Cons:** KB schema is proprietary (lock-in — migration = re-chunk/re-embed/re-validate); default parsing is weak so you must front it with Reducto; Guardrails alone is not a finance validation layer.
**Effort:** Low–Med. **Cost:** $$. **Accuracy:** High (parser-dependent). **Speed:** Fast.

---

### Option B — Azure AI Search-native
**For:** funds on Azure but not deeply tied to M365 desktop apps.

| Layer | Component |
|---|---|
| 1 Parse | [Azure AI Document Intelligence](https://azure.microsoft.com/en-us/products/ai-services/ai-document-intelligence) (or Reducto for the hard docs) |
| 2 Index | [Azure AI Search](https://azure.microsoft.com/en-us/products/ai-services/ai-search) index |
| 3 Retrieve | Azure AI Search [hybrid](https://learn.microsoft.com/en-us/azure/search/hybrid-search-overview) (vector + BM25 + semantic reranking, single query) |
| 4 Generate | Azure OpenAI or Claude |
| 5 Validate | [Azure AI Foundry evals](https://learn.microsoft.com/en-us/azure/ai-foundry/concepts/evaluation-approach-gen-ai) (groundedness) + your finance rule layer |
| 6 Agent | Claude Code / Cowork, or Copilot Studio (see Option F) |

**Data flow:** docs → Doc Intelligence parse → AI Search index → query: hybrid + semantic rerank (one call) → generation → validation → agent. SharePoint connector auto-ingests; Entra ID managed identity means credentials never touch code.
**Pros:** hybrid + semantic rerank + BM25 in a single query out of the box; tight SharePoint/M365 ingestion; Purview classification for compliance pipelines; strong governance.
**Cons:** Doc Intelligence is good but not best-in-class on dense financial tables (swap in Reducto); AI Search index is proprietary (lock-in); Claude is not native (use Azure OpenAI models or call Claude externally).
**Effort:** Low–Med. **Cost:** $$. **Accuracy:** High (parser-dependent). **Speed:** Fast.

---

### Option C — Best-of-breed assembled (FLAGSHIP)
**For:** accuracy-maximalist funds with an eng team, wanting full control and no black box. Deployable in their VPC.

| Layer | Component |
|---|---|
| 1 Parse | [Unsiloed](https://www.unsiloed.ai/) or [Reducto](https://reducto.ai/) via MCP/API (best on dense tables; bounding boxes; schema-conditioned w/ cross-field constraints) |
| 2 Index | [Contextual Retrieval](https://www.anthropic.com/news/contextual-retrieval) (prepend per-chunk context) → [Qdrant](https://qdrant.tech/)/[Weaviate](https://weaviate.io/)/[pgvector](https://github.com/pgvector/pgvector) + BM25 index; [Voyage](https://www.voyageai.com/) or Gemini embeddings |
| 3 Retrieve | Hybrid (vector + BM25) → [Cohere Rerank](https://cohere.com/rerank) or open [bge-reranker-v2](https://huggingface.co/BAAI/bge-reranker-v2-m3) / Qwen (150 → ~20) |
| 4 Generate | Claude Opus on the ~20 reranked chunks |
| 5 Validate | **Full validation engine (Section 3)** — yours, owned, finance-specific |
| 6 Agent | Claude Code / Cowork / Managed Agent, orchestrated by [LlamaIndex](https://www.llamaindex.ai/) + [LangGraph](https://www.langchain.com/langgraph) |

**Data flow:** docs → Unsiloed parse (structured MD/JSON + bboxes + confidence) → contextualize each chunk → dual index → query: hybrid retrieve → rerank → Claude Opus → full validation (faithfulness + rules + abstention) → cited answer + review queue → agent.
**Pros:** every layer best-in-class; nothing is a black box; you own and tune the validation logic (the differentiator); portable across clouds; the architecture you can defend line-by-line to a CIO.
**Cons:** most build effort; you operate the vector DB and orchestration; requires the fund to trust an assembled (vs single-vendor) system — counter with the benchmark.
**Effort:** High. **Cost:** $$$. **Accuracy:** **Highest.** **Speed:** Fast.

---

### Option D — RAGFlow / open-source platform
**For:** data-sovereignty / air-gapped funds that won't send documents to any third-party API.

| Layer | Component |
|---|---|
| 1 Parse | [RAGFlow](https://github.com/infiniflow/ragflow)'s built-in visual/layout parsing (+ Reducto/Unsiloed or self-hosted [Docling](https://github.com/docling-project/docling) for hardest docs) |
| 2 Index | RAGFlow converged context engine (chunk/embed/store) |
| 3 Retrieve | RAGFlow hybrid retrieval + reranking |
| 4 Generate | Claude (via API) or a self-hosted open model |
| 5 Validate | Your finance rule layer + open eval (RAGAS / Phoenix) |
| 6 Agent | RAGFlow agent templates, or Claude Code / Cowork on top |

**Pros:** self-hosted / air-gapped; RAGFlow fuses RAG + agents with finance-relevant visual page understanding and pre-built templates; lower licensing cost; full data control.
**Cons:** higher ops burden (you run it); open-model generation may trail Claude Opus on hard reasoning; needs the same validation layer bolted on.
**Effort:** Med–High. **Cost:** $ (+ops). **Accuracy:** High. **Speed:** Med–Fast.

> Alternatives in this slot: **[R2R](https://github.com/SciPhi-AI/R2R)** (production RAG + agentic reasoning + GraphRAG), **[LlamaIndex](https://www.llamaindex.ai/) + [LangGraph](https://www.langchain.com/langgraph)** (composable, max flexibility), **[Onyx](https://github.com/onyx-dot-app/onyx)** (open enterprise search with connectors + permissions). RAGFlow is the fastest path to a working self-hosted demo.

---

### Option E — Hebbia (buy, don't build)
**For:** no eng team, wants it working next week, budget is no object, primary need is multi-doc synthesis/diligence.

**Methodology (from their ["Goodbye RAG" engineering post](https://www.hebbia.com/blog/goodbye-rag-how-hebbia-solved-information-retrieval-for-llms)):** [Hebbia](https://www.hebbia.com/) explicitly abandoned top-k retrieval for hard questions. Their approach is **"Full Attention"** — instead of retrieving a few chunks, they chunk the document, then in **parallel across all chunks** identify the components that need attention, then synthesize a single answer, then reverse-engineer highlights, with hallucination mitigation via **token-level log-likelihoods and text heuristics**. For multi-doc, they concatenate attention-needy components across all docs; the Matrix Agent treats the whole grid of answers as the domain and applies the same framework. Crucially, they admit **document *retrieval* still uses classical hybrid search** — the innovation is in *understanding/synthesis*, and they call themselves "grossly unsatisfied" with their retrieval layer.

**Implication:** Hebbia trades **cost for recall**. By reading much more of the corpus per query (rather than betting on a top-k retrieve), it rarely "misses" relevant context — that's the accuracy win on T3/T4 reasoning queries. The price is far higher token/compute consumption per query and enterprise (seven-figure-class) pricing.

**Pros:** fastest time-to-value; polished spreadsheet (Matrix) UI analysts already understand; finance-tuned templates (credit-agreement abstractor, VDR screener); strongest on compound/conditional reasoning ("what looks like a lie in this earnings call," "what loopholes exist in this NDA"); full citation trails, RBAC, SSO, audit logs.
**Cons:** expensive; you don't control the validation logic (you trust theirs); on *exact numbers from messy private docs* it carries the same probabilistic-reading ceiling as any LLM-read system (great at synthesis, not deterministic covenant math); a closed platform you can't tune or deploy air-gapped.
**Effort:** Very low. **Cost:** $$$$. **Accuracy:** High on synthesis; ceiling on exact extraction. **Speed:** Med.

---

### Option F — Microsoft Copilot Studio (agent surface for M365 shops)
**For:** Microsoft 365 houses wanting a low-code agent layer their own staff can maintain. **This is a Layer-6 option, not a full stack** — it replaces the agent surface, and ideally sits on Option B's retrieval underneath.

**Methodology:** Copilot Studio's **[generative orchestration](https://learn.microsoft.com/en-us/microsoft-copilot-studio/guidance/generative-orchestration)** uses an LLM-driven **orchestrator/planner** that turns a user message into a structured multi-step plan, selecting tools, topics, knowledge sources, and child agents, executing with policy guardrails (e.g., approval for sensitive actions). It grounds answers via a **[knowledge layer](https://learn.microsoft.com/en-us/microsoft-copilot-studio/knowledge-copilot-studio)** — SharePoint, Dataverse, websites, and (with a semantic index + M365 Copilot license) "Work IQ" for better SharePoint retrieval — returning **citations and metadata**. Admins can require citations on all responses, set moderation levels, and restrict which knowledge sources are accessible per topic.

**How to use it in the plan:** Copilot Studio is the **low-code orchestration/chat surface** for non-technical analysts in an M365 fund. But its native grounding (SharePoint semantic index) is *general-purpose* and will NOT give audit-grade financial extraction on its own. So:
- **Good:** as the conversational front-end and workflow trigger (create ticket, look up holding, schedule, route approval).
- **Insufficient alone:** for covenant math / exact extraction. **Wire your validated pipeline (Option B/C) in as a custom knowledge source or tool/action**, so Copilot Studio orchestrates while your engine supplies the rule-checked, cited numbers.

**Pros:** low-code (fund staff maintain it); deep M365/Teams/SharePoint/Outlook integration; built-in governance, DLP, citation enforcement; fast to stand up for non-engineers.
**Cons:** native retrieval is general-purpose, not finance-grade; less control over the retrieval/validation internals; best as a surface over a real pipeline, not as the pipeline.
**Effort:** Low. **Cost:** $$ (M365 licensing). **Accuracy:** depends entirely on the knowledge layer behind it. **Speed:** Fast.

---

## 3. The Validation Engine (Layer 5) — your IP, specified

This is what the off-the-shelf tools don't package for finance, and what funds say they care about most. Five sub-layers:

### 5.1 Parser-level validation (cheapest place to catch errors)
- Use parsers that self-correct and cite: [Reducto's multi-pass agentic OCR](https://docs.reducto.ai/overview); [Unsiloed's schema-conditioned outputs](https://www.unsiloed.ai/) with **cross-field constraints** (totals must match line items; references must resolve).
- Capture per-field **confidence scores** and **bounding boxes** at parse time.

### 5.2 Retrieval-level validation
- Track **top-k recall** and **citation precision** (production targets: recall ≥85%, citation precision ≥90%).
- Flag queries where retrieval confidence is low → escalate rather than answer.

### 5.3 Generation-level validation (the hallucination guard — core)
- **Claim-decomposition faithfulness:** break the answer into individually verifiable claims; check each against retrieved context; label **entailed / contradicted / baseless**; map each back to the source span.
- Tools off the shelf: **[RAGAS](https://github.com/explodinggradients/ragas)** (faithfulness, relevance), **[TruLens](https://github.com/truera/trulens)** (traceability), **[DeepEval](https://github.com/confident-ai/deepeval)**, **[Arize Phoenix](https://github.com/Arize-ai/phoenix)** (observability); NLI models for entailment. [LLM-as-judge ensembles reach >85% correlation with human review; specialized eval models (e.g. Galileo Luna-2) run ~$0.02/M tokens, ~150ms](https://galileo.ai/blog/rag-evaluation-tools) — cheap enough to run inline.
- **Pass/fail gate:** [faithfulness ≥0.85; below 0.80 → do not surface, route to review](https://customgpt.ai/rag-evaluation-metrics/).

### 5.4 Domain rule validation (FINANCE-SPECIFIC — the differentiator)
Deterministic checks no generic tool runs. Enumerated:
- **Leverage:** net leverage = (total debt − cash) / LTM EBITDA
- **Interest coverage:** ICR = EBITDA / interest expense
- **Bank statement tie-out:** opening + credits − debits = closing
- **Balance sheet:** assets = liabilities + equity
- **Portfolio:** quantity × price ≈ market value (within tolerance)
- **Segments:** Σ segment values = reported total
- **Margins:** EBITDA margin = EBITDA / revenue (sanity bounds)
- **Unit normalization:** detect and reconcile thousands / millions / billions
- **Period reconciliation:** FY vs Q vs LTM vs YTD consistency
- **Cross-source:** annual report vs investor deck vs prior model — flag disagreements
- **Covenant headroom:** computed ratio vs contractual threshold; track quarter-over-quarter

Any value failing a check is **flagged regardless of model confidence.** A covenant or leverage error is not a harmless hallucination — it's a loss.

### 5.5 Abstention + human-in-the-loop (what makes it audit-grade)
Classify every output into one of:
- **Verified** — answer + citation, all rule checks pass, faithfulness ≥ threshold
- **Partially verified** — answer with caveats / one check soft-failed
- **Conflicting evidence** — sources disagree; show both
- **Not found** — evidence absent; do not fabricate
- **Needs human review** — low confidence / rule failure → **review queue**

> The product promise to the fund: *not* "the agent answered," but *"every number is Verified with a source cell, or it's flagged."* A flagged unknown beats a confident error — that is the entire value proposition in regulated finance.

---

## 4. Platform-mapped recommendation (what to tell each fund)

| Fund profile | Recommend | Agent surface |
|---|---|---|
| On AWS, wants production fast | **Option A** (+ your validation layer) | Claude Code / Cowork |
| Microsoft 365 house | **Option B** retrieval + **Option F** surface | Copilot Studio over your pipeline |
| Accuracy-first, has eng team, wants control | **Option C** (flagship) | Claude Code / Managed Agent |
| Data-sovereignty / air-gapped | **Option D** | RAGFlow / Claude Code |
| No eng team, budget no object, synthesis-first | **Option E** (Hebbia) | Hebbia Matrix |
| **All of them** | **Add the validation engine (Section 3)** | — |

**Lock-in caution to give clients:** the managed RAG layer (Bedrock KB / Azure AI Search / Vertex) is the most proprietary component — migration means re-chunk, re-embed, re-validate. Keep **parsing choice and the validation engine portable** even when retrieval is cloud-native. That's both a hedge and a selling point (you're not locking them in).

---

## 5. Your positioning (one line)

*"I assemble best-in-class parsing and retrieval into your platform — AWS, Azure, or air-gapped — and I build the financial validation and audit layer the off-the-shelf tools don't. Your analysts get source-cited, rule-checked, abstention-aware numbers, not a confident guess."*

---

## 6. References & Sources

*Every link is clickable and annotated with the specific claim / section it supports. Grouped by topic. All figures should be re-verified against primary sources before external use; benchmark numbers and pricing change.*

### Benchmarks & research
- **OfficeQA Pro** (Databricks AI Research, Mar 2026) — https://arxiv.org/abs/2603.08655 — frontier agents 34.1% on document corpus; **+16.1% relative gain from structured parsing** (§0 diagram, Priority 1 parsing). Code: https://github.com/databricks/officeqa
- **ParseBench** (LlamaIndex, Apr 2026) — https://arxiv.org/abs/2604.08538 — five parsing dimensions (tables, charts, faithfulness, formatting, grounding); no method strong across all. Blog: https://www.llamaindex.ai/blog/parsebench · Leaderboard: https://www.parsebench.ai/
- **RT4CHART** (claim-decomposition faithfulness; entailed / contradicted / baseless) — https://arxiv.org/pdf/2603.27752 (§5.3 generation validation)
- **FACTUM** (citation-hallucination detection in long-form RAG) — https://arxiv.org/pdf/2601.05866 (§5.3)

### Cost & token mechanics (Cowork / Claude PDF handling)
- **Anthropic — PDF support docs** — https://platform.claude.com/docs/en/build-with-claude/pdf-support — **1,500–3,000 tokens/page; each page also processed as an image** (§0 "why cheap vs Cowork")
- **Anthropic — Vision docs** — https://platform.claude.com/docs/en/build-with-claude/vision — image token counts; high-res 4,784 vs 1,568 tokens/image
- **Anthropic — Pricing** — https://platform.claude.com/docs/en/about-claude/pricing — model rates; Managed Agent session pricing
- **Token-limit explainer** — https://limitededitionjonathan.substack.com/p/why-you-keep-hitting-claudes-usage — a 50-page PDF = 75k–150k tokens just to load
- **Simon Willison — Claude token counts** — https://simonwillison.net/2026/apr/20/claude-token-counts/ — measured PDF token multipliers
- **API pricing breakdown (cached RAG-query cost example)** — https://pecollective.com/tools/anthropic-api-pricing/

### Contextual Retrieval (Priority 2 / §5)
- Originally published by **Anthropic** ("Introducing Contextual Retrieval"). Figures — **35% / 49% / 67% retrieval-failure reduction; ~$1.02 per million doc tokens** — verified in:
  - DataCamp implementation guide — https://www.datacamp.com/tutorial/contextual-retrieval-anthropic
  - CO/AI summary — https://getcoai.com/news/anthropic-introduces-contextual-retrieval-to-boost-accuracy-of-rag-systems/
  - AI system design guide (when to use it for financial docs) — https://github.com/ombharatiya/ai-system-design-guide/blob/main/06-retrieval-systems/10-contextual-retrieval.md

### Parsers (Layer 1)
- **Reducto** — site https://reducto.ai/ · docs (**official MCP, 3B+ pages, Studio citation viewer, bounding boxes**) https://docs.reducto.ai/overview · Elastic blog (agentic OCR multipass; *"parsing isn't the end goal, search is"*) https://www.elastic.co/search-labs/blog/unstructured-documents-reducto-parsing-elasticsearch · YC https://www.ycombinator.com/companies/reducto · Series B funding https://www.prnewswire.com/news-releases/reducto-raises-75m-series-b-to-define-the-future-of-ai-document-intelligence-302581462.html
- **Unsiloed** — site (**dual-stream content+layout, schema-conditioned cross-field constraints, word-level citations**) https://www.unsiloed.ai/ · YC ("LLMs weak at deterministic extraction") https://www.ycombinator.com/companies/unsiloed-ai
- **LandingAI ADE** — MCP + layout-aware (page indexes, bounding boxes) https://landing.ai/developers/bringing-vision-into-reasoning-with-mcp-building-real-agentic-ai · financial services https://landing.ai/solutions/financial-services
- **LlamaParse** — financial extraction (page-level citations) https://www.llamaindex.ai/services/financial-data-extraction-tool · **accuracy note (85–95% clean / 70–85% scanned)** https://dev.to/melek_messoussi_651bf64f4/i-built-a-production-ready-document-parser-for-rag-apps-that-actually-handles-complex-tables-full-3lgn
- **Parser comparisons** — Firecrawl https://www.firecrawl.dev/blog/best-pdf-parsers · Reducto comparison https://llms.reducto.ai/document-parser-comparison

### Retrieval frameworks — open source (Options C, D; Layers 2–6)
- **RAGFlow** (GitHub) — https://github.com/infiniflow/ragflow — RAG + agents, visual page understanding, templates (Option D)
- **Best OSS RAG frameworks** — Firecrawl https://www.firecrawl.dev/blog/best-open-source-rag-frameworks · apidog https://apidog.com/blog/best-open-source-rag-frameworks/
- **Agentic RAG (R2R, RAGFlow for finance)** — cake.ai https://www.cake.ai/blog/best-open-source-agentic-rag
- **Top OSS frameworks (LangChain / LlamaIndex / LangGraph)** — https://medium.com/@techlatest.net/top-10-open-source-rag-frameworks-power-your-ai-with-grounded-answers-c0c253b185c9

### Cloud platforms (Options A, B)
- **Enterprise RAG comparison** (Bedrock KB hybrid + S3/SharePoint/Salesforce connectors) — https://atlan.com/know/enterprise-rag-platforms-comparison/
- **AWS Bedrock Knowledge Bases — hybrid search** — https://aws.amazon.com/blogs/machine-learning/amazon-bedrock-knowledge-bases-now-supports-hybrid-search/
- **AWS Bedrock KB — managed RAG (single-doc)** — https://aws.amazon.com/blogs/machine-learning/knowledge-bases-in-amazon-bedrock-now-simplifies-asking-questions-on-a-single-document
- **Azure AI Search vs Bedrock** (hybrid + semantic rerank + BM25 in one query; SharePoint connector; Entra ID; managed-RAG **lock-in**) — https://myengineeringpath.dev/tools/azure-vs-bedrock/ · https://myengineeringpath.dev/tools/cloud-ai-platforms/

### Microsoft Copilot Studio (Option F)
- **Generative orchestration** (orchestrator/planner, knowledge layer, citations) — https://learn.microsoft.com/en-us/microsoft-copilot-studio/guidance/generative-orchestration
- **Knowledge sources** (SharePoint, Dataverse, web, Work IQ semantic index) — https://learn.microsoft.com/en-us/microsoft-copilot-studio/knowledge-copilot-studio
- **Orchestrate agent behavior with generative AI** — https://learn.microsoft.com/en-us/microsoft-copilot-studio/advanced-generative-actions
- **SharePoint grounding** — https://learn.microsoft.com/en-us/microsoft-copilot-studio/nlu-generative-answers-sharepoint-onedrive
- **Enterprise guide** (admin controls: require citations, moderation levels, per-source restriction) — https://www.epcgroup.net/microsoft-copilot-studio-enterprise-chatbot-guide-2026

### Validation & evaluation (Layer 5)
- **Galileo** (Stanford **17–33%** legal-RAG hallucination; LLM-as-judge **>85%** human correlation; Luna-2 **~$0.02/M, ~152ms**) — https://galileo.ai/blog/rag-evaluation-tools
- **Deepchecks** (RAGAS / TruLens / DeepEval / Arize Phoenix; NLI entailment; faithfulness) — https://deepchecks.com/rag-evaluation-metrics-answer-relevancy-faithfulness-accuracy/
- **CustomGPT** (production rubric: recall ≥85%, citation precision ≥90%, groundedness gates) — https://customgpt.ai/rag-evaluation-metrics/
- **Maxim** (Stanford up-to-**40%** hallucination even with correct retrieval) — https://www.getmaxim.ai/articles/rag-evaluation-a-complete-guide-for-2025/

### Competitor architectures
- **Hebbia** — *"Goodbye RAG"* (Full Attention; log-likelihood + heuristic validation; **retrieval still classical hybrid search**; daily annotations data moat) — https://www.hebbia.com/blog/goodbye-rag-how-hebbia-solved-information-retrieval-for-llms · Sacra profile (ISD, Matrix, valuation/funding) — https://sacra.com/c/hebbia/ · Multi-agent redesign — https://www.hebbia.com/blog/divide-and-conquer-hebbias-multi-agent-redesign · Inside the research agent (ISD audit trail) — https://www.hebbia.com/blog/inside-hebbias-deeper-research-agent
- **LinqAlpha** — AWS architecture (**Textract → OpenSearch → Claude on Bedrock**) — https://aws.amazon.com/blogs/machine-learning/how-linqalpha-assesses-investment-theses-using-devils-advocate-on-amazon-bedrock · three-tier data stack — https://www.getlinq.com/Blog/introducing-linqalpha-api-for-hedge-funds-and-asset-managers
- **Daloopa** — how it works (source-linked, **5,500 tickers, 14yr history**) — https://daloopa.com/how-our-ai-works · https://daloopa.com/ · profile (founders/funding/traceability) — https://idp-software.com/vendors/daloopa/

### Anthropic finance agents & Cowork (context)
- **Anthropic finance agents** (10 templates; connectors incl. FactSet / S&P Capital IQ / Daloopa / Moody's; credential vaults, audit logs, per-tool permissions, human sign-off) — Markets Media https://www.marketsmedia.com/anthropic-introduces-agents-for-financial-services/ · how2shout https://www.how2shout.com/news/anthropic-claude-agent-templates-financial-services-microsoft-365.html · GitHub repo https://github.com/anthropics/financial-services
- **Claude Cowork architecture** (same engine as Claude Code; long-context, sub-agents, VM isolation) — Tensorlake https://www.tensorlake.ai/blog/claude-cowork-architecture-overview · long-context-vs-RAG https://claudecn.com/en/blog/claude-cowork-architecture/ · review (high quota, slower) https://aimaker.substack.com/p/claude-cowork-review-agentic-ai-guide · Anthropic product page https://www.anthropic.com/product/claude-cowork
