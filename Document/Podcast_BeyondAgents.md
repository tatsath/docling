# Podcast Material: Beyond the Black Box — Interpreting Agentic AI Tool Use

## Suggested podcast title

**Before the Agent Acts: Why Tool-Using AI Needs Internal Monitoring**

Alternative titles:

- **Beyond Logs: Looking Inside AI Agents Before They Act**
- **The Missing Layer in Agentic AI: Internal Tool-Use Intelligence**
- **Why AI Agents Need a Warning Light Before Tool Execution**
- **From Black-Box Agents to Interpretable Action**

---

# Core podcast thesis

AI agents are no longer just chatbots. They are starting to call tools, retrieve financial data, write files, send messages, authenticate, execute code, and act across enterprise workflows.

But most enterprise monitoring still happens from the outside: prompts, logs, traces, outputs, evals, and dashboards.

That is not enough.

The important question is not only:

> What did the agent do?

The deeper question is:

> What was the model internally preparing to do before it acted?

This paper studies that exact moment: the **tool-decision boundary**.

---

# The 9 main podcast points and hooks

## 1. Agents are becoming infrastructure, not experiments

**Hook:**  
"Agents are moving from demo land into workflow land."

AI agents are now being adopted across industries. They are not limited to tech companies or research labs. They are being used in finance, customer service, operations, coding, research, compliance, marketing, and enterprise automation.

The risk is that adoption is moving faster than understanding.

The moment an agent can call tools, it is no longer just generating text. It is taking actions.

That changes the entire problem.

**Simple line to say:**

<span style="color: red">"Once a model can call a tool, it stops being just a text generator. It becomes part of the operational workflow."</span>

---

## 2. Financial agents are useful, but not yet reliable enough

**Hook:**  
"Sixty percent accuracy may be impressive for a benchmark, but it is not enough for real money."

Finance is a perfect example of the gap.

Financial agents can read reports, retrieve market data, summarize fundamentals, calculate portfolio metrics, and answer analyst-style questions. But current financial-agent benchmarks still show that even top models are far from enterprise-grade reliability.

In high-stakes finance, 60–65% accuracy is not a production comfort zone.

It means the model is useful, but it still needs oversight, verification, and internal monitoring.

**Simple line to say:**

<span style="color: red">"In finance, being impressive is not enough. The model must be dependable, explainable, and controllable."</span>

---

## 3. The real failure point is the tool-decision boundary

**Hook:**  
"The most important moment is just before the agent clicks the button."

Agents fail in three very practical ways:

1. They miss a tool call when a tool is needed.
2. They call a tool unnecessarily when no tool is needed.
3. They call a risky tool without enough checks.

This is the practical heart of the paper.

The paper is not asking a vague interpretability question. It is asking a concrete operational question:

> At this step, should the agent call a tool or not?

And then:

> If it calls a tool, how consequential or risky is that action?

**Simple line to say:**

<span style="color: red">"The tool boundary is where reasoning turns into action. That is where monitoring matters most."</span>

---

## 4. Logs tell you what happened. They do not tell you why it was forming

**Hook:**  
"Logs are CCTV footage. They are not an MRI."

Most current observability tools show:

- the prompt
- the output
- the tool call
- the trace
- the latency
- the cost
- the error after it happened

That is useful, but it is mostly after-action evidence.

The problem is that in long-horizon agents, an early mistake can change the rest of the trajectory. If the first tool call is wrong, every later step may be contaminated by that wrong context.

So we need pre-action visibility.

**Simple line to say:**

<span style="color: red">"Observability shows the footprint. Interpretability tries to understand the foot before it steps."</span>

---

## 5. The paper's core move: read the model before action

**Hook:**  
"Don't wait for the tool call. Read the model state before the tool call."

The paper takes multi-step agent trajectories and turns them into decision points. At each decision point, the framework looks at the model's internal state before the next action.

It then asks two questions:

- **Tool-Need Probe:** does the model internally signal that a tool is needed?
- **Tool-Risk Probe:** if a tool is involved, does the next action look low, medium, or high risk?

The key is that the model is inspected before execution, not after.

**Simple line to say:**

<span style="color: red">"We are moving from post-mortem observability to pre-action monitoring."</span>

---

## 6. The toolkit: probes are predictors, SAEs are microscopes

**Hook:**  
"Probe is the warning light. SAE is the microscope."

The paper combines two tools.

First, **linear probes**. These are lightweight predictors trained on internal model representations. In simple terms, they ask:

> Is the model internally representing tool need or tool risk?

Second, **Sparse Autoencoders**, or SAEs. These decompose dense activations into more interpretable sparse features. In simple terms, they help ask:

> Which internal concepts or features are driving this signal?

The power is the combination:

- probes give prediction
- SAEs give interpretability
- feature rankings show what matters
- ablation tests whether the features are actually important

**Simple line to say:**

<span style="color: red">"A probe tells you there is a signal. An SAE helps you inspect what the signal is made of."</span>

---

## 7. The result is not just prediction — it is interpretable prediction

**Hook:**  
"Prediction alone is not enough. You want to know what concept caused the prediction."

This is the most important technical-business bridge.

The paper does not only predict tool need. It also surfaces the features and layers associated with tool decisions.

The strongest signals concentrate in later layers, which is intuitive because the model is closer to committing to an action.

The paper also finds interpretable feature patterns:

- numerical and formal-language features for tool need
- authentication, password, account, and security-related features for risk
- finance-specific tool-need movements in multi-step traces
- low-risk behavior in calculator-style financial scenarios

This means the system is not just outputting a black-box score. It is giving internal evidence.

**Simple line to say:**

<span style="color: red">"The goal is not just to say 'risk is high.' The goal is to say which internal features made risk high."</span>

---

## 8. Ablation is the causality check

**Hook:**  
"Switch off the feature and see if the warning light changes."

A major issue in interpretability is fake correlation.

Just because a feature activates during risky behavior does not mean it matters. It may simply be correlated.

That is why ablation matters.

The paper suppresses top-ranked sparse features and checks whether the probe's prediction changes. If removing a small set of features sharply reduces the tool-need probability or flips the prediction, that is stronger evidence that those features are functionally important to the readout.

This is what takes the work beyond a dashboard.

**Simple line to say:**

<span style="color: red">"Correlation says a feature was present. Ablation asks whether the feature mattered."</span>

---

## 9. Enterprise value: pre-action control, reproducibility, and auditability

**Hook:**  
"Enterprises do not only need better agents. They need accountable agents."

This work matters because enterprise AI needs more than impressive demos.

It needs:

- earlier warning before tool execution
- fewer missed tool calls
- fewer unnecessary tool calls
- better risk-tiering of external actions
- better root-cause diagnosis
- internal evidence for audits
- more deterministic oversight
- reproducible signals instead of only probabilistic text outputs

LLMs often produce probabilistic, variable outputs. But a probe-based internal monitor can create a more stable diagnostic signal: at this decision point, with this threshold, the monitor says tool needed or not; low, medium, or high risk.

That is valuable for regulated environments.

**Simple line to say:**

<span style="color: red">"The business value is not only accuracy. It is earlier intervention, cleaner audit trails, and less guesswork."</span>

---

# Suggested 10-minute podcast script

## Opening: 60 seconds

AI agents are moving very quickly from demos to real workflows. They are no longer just chatbots that answer questions. They can call APIs, retrieve financial data, write files, send messages, authenticate users, execute code, and coordinate multi-step tasks.

That means the safety and reliability problem changes.

When a model only writes text, we can evaluate the answer after the fact. But when a model calls a tool, the action can affect the environment. It can change a file, trigger a workflow, send information, or create downstream consequences.

So the key question becomes: can we understand what the model is preparing to do before it acts?

That is the problem my paper focuses on.

---

## Section 1: Why agent tool use is the right problem

The most important boundary in agentic AI is the tool-decision boundary.

At every step, the agent has to decide: should I answer directly, or should I call a tool?

That sounds simple, but it creates several failure modes.

The agent may miss a tool call when it should have used one. It may call a tool unnecessarily and increase cost or complexity. Or it may call a risky tool without proper checks.

In long-horizon agents, one early mistake can reshape the whole trajectory. If the first tool call is wrong, the later context can be wrong. Then the agent is not just making one mistake; it is building on top of a mistake.

That is why post-hoc logs are not enough.

Logs tell you what happened. They do not tell you what the model was internally forming before it happened.

---

## Section 2: Why outside-in observability is incomplete

Most enterprise tools today observe the agent from outside.

They show prompts, outputs, traces, latency, cost, tool calls, and error logs. These are useful. I am not arguing against observability.

But observability is mostly external. It shows the surface.

The deeper question is whether the model had already internally recognized that a tool was needed, whether it was uncertain, or whether it was drifting toward a risky action.

That information may not appear in the final output.

This is where mechanistic interpretability becomes useful. It gives us a way to inspect model internals — activations, sparse features, hidden states — and ask whether there are internal signals before the model acts.

---

## Section 3: What the paper does

The paper builds a pre-action internal monitoring framework for tool-using agents.

We take multi-step agent trajectories and convert them into decision points. At each point, we look only at the context available before the next action. Then we read the model's internal activations.

The framework uses two probes.

The first is the Tool-Need Probe. It predicts whether a tool is needed at that step.

The second is the Tool-Risk Probe. If a tool is involved, it predicts whether the next tool action is low, medium, or high risk.

The important part is that these probes operate on SAE features, not just raw activations. That means we are not only predicting. We are also trying to understand which sparse features and layers are carrying the signal.

---

## Section 4: Probe plus SAE

The easiest way to explain the toolkit is this:

<span style="color: red">A probe is the predictor.  
An SAE is the microscope.  
The probe says: there is a signal here.  
The SAE helps us inspect what that signal is made of.</span>

This matters because enterprises do not only want a scalar risk score. They want to understand why the system flagged something.

Was it because the model saw numerical reasoning? Was it because it recognized a financial retrieval task? Was it because authentication or account-management concepts were active? Was it because the next action involved a write or external consequence?

That is the difference between black-box monitoring and interpretable monitoring.

---

## Section 5: Main findings

The paper evaluates this on GPT-OSS 20B and Gemma 3 27B.

The Tool-Need Probe is the stronger and more stable signal. It shows that models do contain readable internal signals about whether a tool is needed.

The Tool-Risk Probe is also useful, especially once a tool call is already in play. It can help distinguish low-risk retrieval actions from more consequential actions like authentication, outbound communication, or execution.

Another important finding is that the strongest tool-decision signals appear in later layers. That makes intuitive sense. These are the layers closer to the model's final commitment before action.

The feature analysis is also important. The top features are not random tensors. Many are interpretable: numerical data, formal language, authentication, usernames, passwords, security management, account-related concepts, and similar patterns.

So the paper shows not only that the model has an internal signal, but also that the signal can be inspected.

---

## Section 6: Finance example

Finance is a natural domain for this because financial agents often need to retrieve data, calculate values, compare fundamentals, summarize filings, and reason across multiple steps.

In the paper's financial examples, the Tool-Need Probe rises on steps where external financial retrieval or calculation is needed and falls on follow-up turns where no new tool call is required.

That is the kind of behavior you want in a real enterprise setting.

You do not want an agent reflexively calling tools on every step. You also do not want it skipping tools when fresh or external data is required.

The right behavior is selective tool use.

The agent should invoke tools when epistemically necessary — when it actually needs external information or computation — not simply because a tool exists.

---

## Section 7: Why ablation matters

A big concern in this kind of work is whether we are only finding correlations.

Maybe a feature lights up during a tool call, but it does not actually matter.

That is why the paper uses ablation.

We take top-ranked sparse features, suppress them, and re-run the probe. If the probe confidence drops sharply or the prediction flips, that suggests those features are functionally important to the readout.

This is not a full proof of the whole model circuit. But it is stronger than just saying: "we saw a pattern."

The analogy is simple: if you switch off a component and the signal changes, that component mattered to the diagnostic system.

---

## Section 8: Why this matters for enterprises

The enterprise value is very practical.

First, this can act as a pre-action warning layer.

Before an agent executes a tool, the monitor can ask: does the internal state match the expected action? Is a tool needed? Is the action risky? Should a human review this?

Second, it helps with root-cause analysis.

Instead of only saying, "the agent failed," we can ask which internal features and layers were associated with the failure.

Third, it supports auditability.

For regulated industries, logs alone may not be enough. You may need evidence that you monitored the model before action, detected risk states, and had a policy for escalation.

Fourth, it supports reproducibility.

LLM outputs can vary. But internal probes can create more stable diagnostic signals around specific decision boundaries.

So this is not just research curiosity. It is a step toward operational internal observability.

---

## Section 9: Limitations and honest caveats

This field is still early.

The paper studies two open-weight models. Broader portability across architectures, scales, and post-training recipes needs more work.

Risk labels are also heuristic. Low, medium, and high risk are useful operational categories, but industries will need sharper risk taxonomies.

Runtime monitoring can also be computationally tricky. Capturing activations, encoding them through SAEs, and running probes at every step is not free. The best near-term use case may be selective monitoring at high-value decision points rather than monitoring every token everywhere.

And closed-source models remain harder because we usually do not get direct access to internal activations.

So the right claim is not: we fully understand agentic models.

The right claim is: there are useful internal signals at the action boundary, and we can begin turning those signals into practical monitoring tools.

---

## Closing: 60 seconds

The future of AI agents will not be solved only by better prompts, bigger models, or more logs.

We need a deeper layer.

Agents need to be monitored before they act, not only after they fail.

This paper shows that tool decisions leave readable traces inside model states before external execution. By combining probes and sparse autoencoders, we can detect tool need, estimate action risk, inspect the features behind the signal, and test feature importance through ablation.

That is the broader direction: moving from black-box agents to interpretable, monitored, and eventually controllable agents.

The big message is simple:

> <span style="color: red">If AI agents are going to act in the real world, we need to understand what they are forming internally before they act.</span>

---

# Short memory hooks

- **Workflow land:** agents are no longer demos; they are entering enterprise workflows.
- **Before the click:** the key moment is before tool execution.
- **CCTV vs MRI:** logs show what happened; internals show what was forming.
- **Warning light:** probes detect tool need and tool risk.
- **Microscope:** SAEs reveal the features behind the signal.
- **Switch test:** ablation checks whether the feature actually matters.
- **Selective tool use:** the agent should call tools when necessary, not reflexively.
- **Interpretable prediction:** not just what the model predicts, but why.
- **Audit trail:** enterprises need evidence, not vibes.
- **Pre-action monitoring:** the future is monitoring agents before they act.
