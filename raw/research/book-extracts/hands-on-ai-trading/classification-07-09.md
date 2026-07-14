# Neutral Classification of Chapters 7–9

## Scope and evidence convention

This classification uses only the three supplied chapter extracts. It is market- and venue-neutral: applicability is assessed across listed and OTC derivatives, equities, ETFs, futures, FX, cryptoassets, multi-asset portfolios, and strategy portfolios where the required observations and executable instruments exist.

- **Textbook claim** means the extract explicitly states or reports it.
- **Inference** means a research implication derived from the extract, not demonstrated by it.
- Categories overlap. A topic may be foundational, a reusable method, and a concrete or frontier research direction.
- Reported backtests, anecdotes, generated answers, vendor results, and historical prices are not treated as independently established facts.

## Classification map

| Material | Classification | Evidence assessment |
|---|---|---|
| BSM/GBM delta hedging, discrete replication, frictions, volatility smile/skew, stochastic-volatility alternatives | Foundational knowledge | Standard conceptual scaffold in the extract; several displayed/code formulas contain acknowledged inconsistencies and must not be copied without checking. |
| State/action/reward design; simulation pretraining; real-data refinement; train/validation/OOS/forward testing | Foundational knowledge; transferable research method | Strong reusable workflow; the particular implementation is only illustrative. |
| Two-stage RL hedging | Concrete research direction; strategic capability; frontier/high-complexity direction when expanded to realistic books | Genuine hypothesis, but chapter evidence is a short, single-asset demonstration rather than broad superiority. |
| Corrective AI/meta-labeling | Concrete research direction; strategic capability | Plausible second-stage risk gate. Reported FX improvement excludes costs and depends on unavailable licensed features/API. |
| Point-in-time feature engineering; conversion of cross-sectional characteristics into long-short time-series factors | Foundational knowledge; transferable research method; strategic capability | Broadly reusable, subject to filing availability, identity, survivorship, and construction controls. |
| Conditional Parameter Optimization | Concrete research direction; strategic capability; frontier/high-complexity direction as control space grows | Clear conditional-ranking formulation; one reported ETF example has unusually high Sharpe and unresolved cost/robustness questions. |
| Conditional Portfolio Optimization | Concrete research direction; strategic capability; frontier/high-complexity direction | Coherent learning-to-rank allocation framework. Evidence is largely author/vendor/client supplied and not independently replicated in the extract. |
| Equal weight, inverse volatility/risk parity, Markowitz/tangency, minimum variance, static/grid and rolling optimization | Foundational knowledge; meaningful baselines | Necessary comparators, not straw men; constraints and horizons must be identical. |
| LLM model selection, prompting, hallucination controls, abstention, cost/quality evaluation | Foundational knowledge; transferable research method | Useful workflow. Model/service descriptions and costs are historically dated. |
| RAG over research documents | Concrete research direction; strategic capability | Demonstrated as a research-productivity workflow, not as autonomous alpha. Retrieval and source verification remain decisive. |
| LLM summarization, comparison, Q&A, classification, and structured thesis generation | Concrete research direction; strategic capability | The examples show usefulness and also truncation, omission, unsupported authority, and internal contradiction. |
| Text sentiment/theme extraction as a trading input | Concrete research direction; frontier/high-complexity direction | Explicitly proposed only as input to a separately tested signal; no return evidence is supplied in these extracts. |
| Generative-AI-assisted research workflow and breadth expansion | Concrete research direction; strategic capability | Immediate claim is analyst throughput. Conversion of throughput into returns is unproven. |
| Learned option-pricing kernel implied by an advanced hedge policy; end-to-end PnL/Q-learning; large multi-instrument RL books | Frontier/high-complexity direction | Mentioned as advanced/early-stage; requires substantially more data, simulation realism, compute, and validation than shown. |
| QuantConnect/PyTorch implementation; QTS Corrective AI/CPO API; EBS data; AWS S3/Kendra/SageMaker Canvas/Bedrock/Amazon Q; named contemporary LLMs | Vendor/platform-specific | Examples of implementation, not essential definitions of the methods. Licensed data/services prevent full reproduction of some results. |
| Crisis-alpha timing anecdote and ~80% gross return; corrected FX metrics; CPO tables and claimed live uplift; AI hedge superiority on the displayed path; LLM-produced recommendations/targets/numbers; claim that broader LLM research creates alpha | Claim requiring independent validation | Retrospective, cost-free, vendor/client-supplied, short-path, generated, or otherwise insufficiently controlled evidence. |

## Transferable research methods

1. **Theory or trusted-policy prior, then empirical correction.** Prime a model on a stable structural target or existing decision, then learn bounded adjustments from point-in-time outcomes. This joins the RL hedge and Corrective AI ideas.
2. **Conditional decision surfaces.** Put candidate controls or weights and contemporaneous environment features in the same row, label with a forward objective, score feasible candidates at inference, and choose the best-ranked candidate.
3. **Ranking before calibration.** For parameter and portfolio choice, evaluate whether the model orders candidates correctly; accurate numeric Sharpe or return prediction is not required.
4. **Point-in-time feature discipline.** Shift filings to actual availability, preserve changing universes and ticker identity, avoid survivorship, synchronize prices, and forward-fill only after release.
5. **Constraint-aware comparison.** Apply identical exposure, cash, turnover, rebalance, cost, universe, and horizon assumptions to learned and conventional methods.
6. **Chronological evaluation.** Separate training, validation, untouched OOS, and forward/paper periods; repeat across regimes, instruments, and decision dates.
7. **Grounded language-model evaluation.** Define representative private tasks, compare prompts/models on a rubric, add retrieval when answers depend on a corpus, require abstention and source support, and audit every number and cross-turn claim.
8. **Escalate complexity empirically.** For language tasks: prompt, then RAG, then exceptional fine-tuning. For hedging: bounded theoretical targets before unregularized PnL learning. These are textbook recommendations, not universal laws.

## Concrete and frontier research directions

### 1. Two-stage RL hedging

**Classification:** concrete; strategic capability; frontier when extended beyond a small single-option policy.

- **Core hypothesis/question:** Can a policy primed on structural delta targets and refined on realized, cost-aware outcomes reduce hedging loss/risk versus implementable hedge rules under discrete trading and changing conditions?
- **Applicable markets:** equity/index/ETF/commodity/rates/FX/crypto options; OTC options and structured notes where reliable marks and executable hedge instruments exist. Extension to option combinations and books is plausible but not demonstrated.
- **Required data:** synchronized underlying and option quotes/trades, strikes, expiries, rates, contract terms, spreads, fees, liquidity/volume, hedge fills, inventory, rolls, and point-in-time state variables; a simulator covering plausible price, volatility, jump, liquidity, and cost processes.
- **Candidate methods/models:** delta-imitation policy network followed by low-rate empirical refinement; stochastic policies; alternative GBM or stochastic-volatility simulators; finite-difference targets where analytic Greeks do not exist; regularized/clipped Q-learning or direct PnL methods only with sufficient data and compute.
- **Meaningful baselines:** no rebalance/static hedge, current or lagged analytic delta, discrete delta, numerical delta, simple underhedge rule, and cost-aware deterministic bands; compare against the unrefined simulation policy.
- **Evaluation design:** chronological, contract-level OOS and forward tests across underlyings, strikes, maturities, volatility/liquidity regimes, and roll events; identical rebalance rules and costs; report mean PnL, downside loss, variance, tail loss, turnover, slippage, inventory and model drift. Ablate theoretical pretraining, empirical refinement, prior position, and added state features.
- **Major failure modes:** simulator misspecification/unknown unknowns; recent-window overfit; sparse option histories; look-ahead; nonstationarity; roll discontinuities; unstable wealth normalization; a commission sign lacking absolute turnover; objective mismatch between downside-only ReLU and variance; incorrect BSM code; action uncertainty or bounds that do not map to executable positions.
- **Continue if:** improvements survive realistic costs and multiple untouched assets/regimes, remain stable under simulator and reward perturbations, beat simple cost-aware delta policies on downside/tail risk without unacceptable turnover, and persist in forward tests with interpretable state-conditional attribution.
- **Textbook claim vs inference:** The chapter reports superior cumulative wealth on one displayed AAPL path and says the learned hedge tracks below delta. **Inference:** this warrants replication, not a conclusion that RL hedging is generally superior.

### 2. Corrective AI / meta-labeling

**Classification:** concrete; strategic capability.

- **Core hypothesis/question:** Can a secondary model estimate when a primary decision is likely to be harmful and veto or resize it, improving net risk-adjusted outcomes without needing to rediscover the primary edge?
- **Applicable markets:** any timestamped primary signal—FX, futures, equities, ETFs, options, crypto, execution decisions, or strategy activation—provided secondary features are available before action.
- **Required data:** primary signals and sizes, realized forward outcomes at the true decision horizon, point-in-time cross-market/technical/fundamental/flow features, execution costs, rejected-trade counterfactuals, and changing universe metadata.
- **Candidate methods/models:** gradient-boosted trees, boosted/random forests, calibrated classifiers, survival or quantile models, and probability-to-size mappings; threshold gate, continuous resize, or abstention policy.
- **Meaningful baselines:** unfiltered primary strategy, random veto with equal participation, constant participation/size reduction, simple volatility/drawdown filters, logistic regression, and threshold choices set only on validation data.
- **Evaluation design:** purged chronological splits around overlapping labels; costs and latency included; measure net return, Sharpe, drawdown, tail loss, turnover, coverage, precision/recall on losing decisions, calibration, and opportunity cost of vetoed winners; test threshold sensitivity and feature ablations across regimes.
- **Major failure modes:** label leakage, selection bias, class imbalance, threshold mining, unobservable counterfactual fills, removing rare convex winners, duplicated exposure across features, regime shift, and a secondary model that merely reduces gross risk.
- **Continue if:** risk improvement exceeds what equal de-risking achieves, calibration and value persist after costs across multiple periods/markets, veto logic is stable, and forward results confirm that filtered losses outweigh foregone winners.
- **Textbook claim vs inference:** The extract reports a cost-free EUR/USD Sharpe increase from 0.88 to 1.29 and lower drawdown using proprietary inputs. The crisis-timing story and production outcomes are retrospective claims. **Inference:** the method is testable and broadly transferable, but those figures do not validate it independently.

### 3. Conditional Parameter Optimization

**Classification:** concrete; strategic capability; frontier as parameter dimension, frequency, and state complexity rise.

- **Core hypothesis/question:** Do contemporaneous market features rank feasible strategy parameter sets better than fixed, expanding, or rolling historical optimization?
- **Applicable markets:** any rule-based strategy with explicit controls across equities, ETFs, futures, FX, options, crypto, spreads, and execution algorithms.
- **Required data:** point-in-time environment features; candidate parameter tuples; primary strategy returns/fills for every candidate and decision horizon; fees, spreads and impact; synchronized asset histories.
- **Candidate methods/models:** boosted trees/random forests, regularized nonlinear regressors or rankers, pairwise/listwise learning-to-rank, contextual bandits after offline validation, and constrained candidate search/intelligent sampling.
- **Meaningful baselines:** fixed in-sample optimum, expanding and rolling/walk-forward optimization, robust/default parameters, simple regime rules, random candidate selection, and an unconditional model using controls without environment features.
- **Evaluation design:** nested chronological tuning; all candidate outcomes generated without leakage; untouched OOS regimes and markets; include costs caused by parameter switching; compare return, Sharpe, Calmar, drawdown, turnover, ranking correlation/regret, and stability. Stress grid density and objective horizon.
- **Major failure modes:** multiple testing across candidates, dependence among rows sharing the same date, local maxima, state-feature leakage, weak regime recurrence, argmax exploitation of model error, excessive switching, and infeasible exhaustive search.
- **Continue if:** conditional selection reduces OOS regret versus robust fixed and rolling controls after switching costs, ranking generalizes across periods/instruments, and results survive candidate-grid, label-horizon, and feature perturbations.
- **Textbook claim vs inference:** The GLD–GDX example reports 19.77% versus 17.29% annual return and very high Sharpes (12.325 versus 11.947). The extract itself notes unresolved cost and robustness implications. **Inference:** the formulation merits controlled replication; the reported magnitude should not anchor expectations.

### 4. Conditional Portfolio Optimization

**Classification:** concrete; strategic capability; frontier/high-complexity.

- **Core hypothesis/question:** Can a model rank feasible allocations by forward portfolio quality conditional on current market state more robustly than history-only allocation rules?
- **Applicable markets:** equity/ETF/crypto/multi-asset portfolios, futures or FX books, and portfolios of strategies; value may be limited for truly factor-neutral books with little conditionable regime exposure.
- **Required data:** point-in-time component returns and membership, feasible sampled weights, forward horizon portfolio outcomes, market/regime features, cash/proxy returns, constraints, turnover, spreads/impact, and optional proprietary features.
- **Candidate methods/models:** nonlinear regression or ranking models on state-plus-weight controls, intelligent/constrained sampling, pairwise/listwise rankers, robust/quantile objectives, Expected Shortfall or UPI labels in addition to Sharpe.
- **Meaningful baselines:** equal weight, inverse volatility/risk parity, tangency/Markowitz, minimum variance, static strategic allocation, prior allocation/no trade, and simple regime-based cash rules—all under identical constraints.
- **Evaluation design:** rolling decision simulation with training strictly before allocation; changing membership; nested choice of horizon/objective; realistic costs and capacity; report net return, Sharpe, drawdown, tail risk, turnover, concentration, constraint activity, ranking regret and allocation stability. Evaluate multiple universes and crisis/non-crisis periods and test whether gains are only cash timing.
- **Major failure modes:** combinatorial search, correlated candidate samples, noisy forward Sharpe labels, covariance/regime breaks, model-error exploitation by argmax, constraint mismatch, hindsight narratives, universe survivorship, and defensive performance driven solely by a looser cash cap.
- **Continue if:** it beats reasonable ex-ante baselines rather than only a weak comparator, adds value under equal cash/exposure constraints and after costs, rankings and allocations are stable, gains recur across universes/horizons, and forward evidence supports rather than merely narrates regime adaptation.
- **Textbook claim vs inference:** The extract reports favorable results for several portfolios, one case where equal weight wins OOS, and claimed post-deployment uplift. These are largely author/vendor/client results without independent replication. **Inference:** breadth of examples raises plausibility but not evidentiary independence.

### 5. LLM/RAG investment-research system

**Classification:** concrete; strategic capability; frontier when used for autonomous multi-source reasoning or decisions.

- **Core hypothesis/question:** Can grounded retrieval plus structured generation increase research coverage and accuracy per analyst-hour without increasing unsupported conclusions or omissions?
- **Applicable markets:** especially disclosure-rich equities, credit, funds, and issuers; also macro, commodities, rates, FX and crypto where timestamped authoritative text corpora exist.
- **Required data:** point-in-time filings, transcripts, presentations, reports, industry documents and metadata; document versions, permissions and timestamps; passage-level relevance/answer labels; expert-created evaluation questions and supported answers.
- **Candidate methods/models:** instruct LLMs, embeddings plus vector/hybrid retrieval, reranking, chunking, grounded answer schemas, citations, abstention, low-temperature decoding, multi-stage extraction/verification, and fine-tuning only if prompt/RAG evaluation shows a durable gap.
- **Meaningful baselines:** keyword/BM25 search, manual analyst search, extractive summaries, single-context LLM without retrieval, generic prompting, and smaller/cheaper models evaluated on the same tasks.
- **Evaluation design:** blinded expert rubric over factual support, retrieval recall, citation precision, numerical/date/unit accuracy, completeness, contradiction rate, abstention quality, latency, total cost, and analyst time saved; preserve point-in-time corpora and test adversarial, table-heavy, ambiguous, missing-evidence, long-document and multi-turn cases.
- **Major failure modes:** failed retrieval, stale or permission-inappropriate documents, PDF/table extraction loss, hallucination, authoritative persona overstatement, context truncation, multi-turn error propagation, benchmark-to-domain mismatch, high idle infrastructure cost, and unsupported recommendations.
- **Continue if:** it measurably improves time-to-supported-answer or coverage while meeting strict factual/citation thresholds, errors are detectable and bounded, abstention works, and experts prefer or accept outputs in blinded tests at sustainable cost.
- **Textbook claim vs inference:** The examples show richer summaries and comparisons after better prompts/RAG, but also truncation and a Marriott/Hyatt contradiction; passage support for every generated number is absent. **Inference:** productivity is the first valid target; excess returns require a separate downstream study.

### 6. Text signals and generative-AI research workflows

**Classification:** concrete; strategic capability; frontier/high-complexity when linked to trading or autonomous research generation.

- **Core hypothesis/question:** (a) Do point-in-time LLM-extracted sentiment, themes, changes, risks, or structured facts add incremental predictive information? (b) Can generative workflows propose, organize, and monitor research hypotheses more efficiently without inflating false discovery?
- **Applicable markets:** news/disclosure-sensitive equities and credit, macro/FX/rates, commodities, crypto, options/volatility, and cross-asset event studies.
- **Required data:** timestamped raw text and release/receipt times, entity/instrument mappings, revisions, source provenance, contemporaneous prices/liquidity, structured labels or expert annotations, and a full log of prompts/models/retrieval context.
- **Candidate methods/models:** zero/few-shot classifiers, embeddings, domain models, RAG extraction, schema-constrained LLM output, ensemble disagreement, change detection, event studies, and conventional predictive models using text features alongside non-text controls.
- **Meaningful baselines:** lexicons, bag-of-words/TF-IDF, simple sentiment classifiers, source/event fixed effects, price-only/fundamental-only models, random or lagged text features, and human-coded samples.
- **Evaluation design:** timestamp-faithful event studies and purged walk-forward backtests; freeze prompts/model versions per test block; separate extraction accuracy from return prediction; control multiple hypotheses; include costs, latency and tradability; report incremental information coefficient, calibration, decay, turnover, net returns, and robustness by source/event/market.
- **Major failure modes:** publication/receipt leakage, entity errors, duplicated stories, revisions, prompt drift, model upgrades, narrative hindsight, label contamination from future price language, correlated tests, hallucinated facts, and converting eloquence into unjustified conviction.
- **Continue if:** extraction is reproducible and source-supported, features add stable incremental value over simple text and market baselines in untouched periods, economics survive latency/costs, and hypothesis yield improves without a higher false-discovery rate.
- **Textbook claim vs inference:** The extract explicitly suggests sentiment/theme classification before inclusion in a separately tested signal and frames generative AI as a research-throughput tool. It does not demonstrate signal alpha. **Inference:** both signal extraction and hypothesis-workflow value are legitimate, separate research questions.

### 7. Advanced learned hedging/pricing and autonomous decision systems

**Classification:** frontier/high-complexity.

- **Core hypothesis/question:** Can richer policies trained on realistic dynamics jointly learn hedging, transaction-cost control, inventory management, and possibly a pricing kernel that generalizes across instruments and regimes?
- **Applicable markets:** multi-option books, structured products, OTC derivatives, high-frequency liquid derivatives, and cross-hedged books.
- **Required data:** book-level states, full option surfaces, order books/fills, funding/margin, cross-impact, counterparty/contract details, rare-stress history, and validated multi-factor/jump/liquidity simulators.
- **Candidate methods/models:** actor–critic or clipped/regularized Q-learning, distributional/offline RL, constrained or risk-sensitive RL, recurrent/transformer policies, stochastic-volatility/jump simulators, and model-based RL.
- **Meaningful baselines:** desk hedge rules, Greek-neutral and banded hedges, stochastic-control solutions where tractable, supervised delta policies, and simpler two-stage policies.
- **Evaluation design:** simulator falsification, historical replay, nested OOS across products, stress/scenario tests, paper portfolios, limits on inventory/turnover/tail risk, and continuous state-conditional attribution; validate any implied prices independently.
- **Major failure modes:** simulator exploitation, extrapolation, rare-event blindness, partial observability, off-policy bias, nonstationarity, reward hacking, unsafe actions, excessive compute/data demand, and inability to explain failures.
- **Continue if:** policies remain superior under multiple plausible simulators and real replay, respect hard constraints, improve tail/cost outcomes rather than merely average PnL, and survive prolonged forward testing.
- **Textbook claim vs inference:** The chapter says industrial hedging can require large data/compute, notes clipped Q-learning, and suggests advanced policies may imply pricing kernels. **Inference:** this is a serious long-horizon program, not supported by the small demonstration alone.

## Vendor/platform-specific material

- **QuantConnect and PyTorch:** implementation environment for the AAPL hedge and CPO backtest integration.
- **QTS proprietary services, premium APIs, engineered features, and licensed EBS data:** essential to the reported Corrective AI/CPO examples as presented; lack of access prevents full replication.
- **AWS S3, Kendra, SageMaker Canvas/JumpStart, Bedrock, and Amazon Q Business:** one RAG/deployment stack. The conceptual RAG workflow is portable.
- **ChatGPT, Gemini, Claude, Llama, Mistral and named leaderboards:** historical model-selection examples, not durable rankings.
- **June 2024 token prices and always-on AWS monthly costs:** historical budgeting examples only, requiring current independent pricing before use.

## Claims requiring independent validation

1. Corrective AI's crisis timing, roughly 80% gross return anecdote, EUR/USD improvement, and any implication of production reliability.
2. CPO performance tables, unusually high spread-strategy Sharpes, ex-post regime explanations, the claim that a larger cash cap would turn MESH positive, and reported post-deployment monthly uplift.
3. The displayed RL hedge's superiority, the economic explanation for systematic underhedging, and any general claim that the small policy is “effective.”
4. Generated Marriott/Hyatt facts, recommendations and price target where passage-level support is unavailable; the extract itself documents contradiction and truncation.
5. Claims that larger/newer models generally outperform, that a fine-tuned small model can match a larger model, or that a particular prompting sequence is better for a target workflow; these are hypotheses to benchmark on the actual task.
6. The proposition that more research throughput, wider coverage, richer summaries, or LLM-generated insight produces trading alpha. Productivity and returns are distinct outcomes.
7. Any direct reuse of the chapter's printed BSM `d1`, Heston-style process, structured-note payoff, commission term, cash constraints, or malformed EMA/variance notation, because the extracts flag mathematical or encoding inconsistencies.

## Broad one-sheet nominations by theme

These are nominations by research theme, not a priority ranking.

### Adaptive risk and hedging

- Theory-primed, empirically refined RL hedge versus cost-aware discrete delta and band policies.
- Reward and cost-definition audit for learned hedging: downside loss, variance, tail risk, turnover, and roll handling.
- Cross-product generalization of hedge policies across underlyings, strikes, maturities, and option structures.
- Frontier: constrained book-level RL and independently validated learned pricing kernels.

### Decision correction and regime conditioning

- Corrective AI gate/resize study against equal de-risking and simple volatility filters.
- Conditional parameter ranking versus fixed, expanding, and rolling optimization.
- Feature-value study: point-in-time fundamentals, hedge factors, technicals, flow, and regime alarms.
- Stability study of candidate ranking, switching costs, and argmax model-error exploitation.

### Portfolio construction

- Conditional allocation versus equal weight, inverse volatility, tangency, minimum variance, and simple defensive rules under identical constraints.
- Ranking objectives: forward Sharpe versus Expected Shortfall, UPI, drawdown, or multi-objective utility.
- Cash-cap, turnover, concentration, and membership sensitivity.
- Cross-universe validation for asset portfolios and portfolios of strategies.

### Grounded investment intelligence

- Point-in-time RAG benchmark for filings, transcripts, reports, tables, and contradictory evidence.
- Research-Q&A and summarization evaluation centered on citation accuracy, completeness, abstention, and analyst time saved.
- Competitive/thesis comparison with explicit evidence schemas and cross-turn consistency checks.
- Model/prompt/retrieval/cost frontier using representative proprietary tasks rather than generic leaderboard rank.

### Text-derived signals

- Timestamp-faithful extraction of sentiment, themes, risks, metric changes, and management language.
- Incremental-value tests against lexicon, bag-of-words, conventional classifier, and non-text baselines.
- Signal decay, latency, duplication, entity resolution, and model-version robustness.
- Separation of extraction quality, predictive information, and executable net performance.

### Generative research process

- LLM-assisted hypothesis generation with a preregistered validation queue and false-discovery accounting.
- Structured evidence synthesis and monitoring workflows that preserve provenance and force abstention.
- Human-plus-model versus human-only research throughput and decision-quality experiments.
- Governance study for reproducibility across prompts, retrieval corpora, model updates, and multi-turn sessions.
