# Cross-Market Classification Synthesis: Hands-On AI Trading

## Purpose

This synthesis maps the textbook into reusable knowledge and research directions using only the extracted chapters as source material.

The material is evaluated across equities, options, futures, FX, crypto, and multi-asset portfolios. Difficulty, data requirements, and evidentiary weakness are recorded without treating them as reasons to erase an idea.

## Classification Key

| Classification | Meaning |
|---|---|
| Foundational knowledge | Concepts needed to reason correctly about markets, data, modeling, execution, and risk. |
| Transferable research method | A reusable investigation or validation technique. |
| Concrete research direction | A falsifiable strategy, model, or workflow suitable for an empirical study. |
| Strategic capability | Infrastructure or organizational competence that supports many research programs. |
| Frontier/high-complexity direction | A serious longer-horizon program with demanding data, modeling, or operational requirements. |
| Vendor/platform-specific | An implementation example whose general concept may transfer but whose details are tied to a provider. |
| Claim requiring independent validation | A reported result, formula, narrative, or recommendation that should not be accepted without replication. |

## Foundational Knowledge

### Market and instrument mechanics

- Limit-order books, liquidity, market impact, adverse selection, spreads, partial fills, and execution uncertainty.
- Durable instrument identity, corporate actions, delistings, futures rolls, contract multipliers, expiry, settlement, exercise, assignment, margin, borrow, and funding.
- Differences among equities, options, futures, FX, crypto, and fragmented multi-venue markets.
- Point-in-time market data, late reports, corrections, revisions, and the distinction between analytical and executable prices.

### Research validity

- Define the objective, target, horizon, universe, constraints, features, benchmark, and falsifier before modeling.
- Use chronological evaluation, point-in-time availability, correct warm-up behavior, and train-only preprocessing.
- Control look-ahead, survivorship, universe-membership, revision, corporate-action, and overlapping-label leakage.
- Include fees, spreads, slippage, impact, financing, borrow, funding, turnover, capacity, and failure to fill.
- Prefer simple baselines, ablations, parameter sensitivity, stress periods, influential-trade analysis, and untouched final tests.

### Modeling vocabulary

- Regression, classification, ranking, clustering, dimensionality reduction, time-series models, neural networks, transformer forecasting, and reinforcement learning.
- Stationarity, fractional differentiation, cointegration, regime detection, calibration, probabilistic performance measures, and feature importance.
- Risk-aware evaluation using drawdown, tail loss, turnover, concentration, stability, and economic value—not predictive accuracy alone.

## Transferable Research Methods

1. **Point-in-time dataset construction:** preserve source arrival, revision, membership, identity, and model-version history.
2. **Causal preprocessing:** fit imputation, scaling, feature selection, and transformations only on information available at the decision time.
3. **Model ladder:** begin with transparent linear/rule-based baselines, then justify trees, deep learning, RL, or conditional optimization through incremental evidence.
4. **Robustness harness:** parameter surfaces, Remove/Replace/Reduce tests, walk-forward evaluation, cost stress, regime slices, and alternate specifications.
5. **Event-study discipline:** predeclare event, mechanism, timestamps, reaction window, control group, latency, and tradability.
6. **Cross-sectional validation:** reconstruct membership, include delistings, test monotonic ranked buckets, capacity, and turnover.
7. **Sequential-policy evaluation:** compare learned policies with strong deterministic controls under realistic replay, partial fills, latency, and hard risk constraints.
8. **Grounded language-model evaluation:** separate retrieval quality, extraction accuracy, analyst productivity, predictive value, and trading returns into distinct tests.

## Concrete Research Directions

### Predictive signals and supervised learning

- Next-period return or direction prediction using technical, macroeconomic, fundamental, sentiment, and cross-market features.
- Regime classification using volatility, trend, liquidity, correlation, macro state, or hidden-state models.
- Corrective AI/meta-labeling that vetoes or resizes an existing decision based on its conditional probability of success.
- Cross-sectional ranking for stock, contract, token, or strategy selection using regularized regression, trees, ranking losses, and calibrated classifiers.
- Temporal CNN, recurrent, transformer, and pretrained time-series forecasting compared with naive, linear, and classical time-series baselines.
- LLM-derived sentiment, event, theme, risk, or structured-fact features evaluated independently of the generative workflow that produces them.

### Relative value and market structure

- Cointegration and error-correction trades among related equities, ETFs, futures, FX crosses, crypto assets, or venues.
- PCA/residual statistical arbitrage with strict controls for universe selection, changing relationships, and multiple testing.
- Cross-venue and fragmented-market arbitrage with synchronized depth, conservative multi-leg fills, inventory constraints, funding/borrow, and outage scenarios.
- ML-based pair selection, clustering of economically related instruments, and representation learning for candidate discovery.
- Informed-flow/adverse-selection detection using order-flow imbalance, point processes, sequence models, or calibrated toxicity probabilities.
- Cost-aware order timing and execution optimization, including delayed-limit policies and implementation-shortfall prediction.

### Events, alternatives, and text

- Timestamp-rigorous studies of corporate, regulatory, macroeconomic, weather, shipping, geolocation, protocol, security, or sentiment events.
- Fundamental and alternative-data factor research with original availability timestamps and matched controls.
- News summarization and classification pipelines that preserve document versions, publication/receipt times, entity mapping, and passage-level support.
- Generative-AI hypothesis discovery evaluated by research yield and false-discovery rate rather than fluency or note volume.

### Portfolio construction and risk

- Adaptive cross-asset allocation using volatility, correlation, macro state, sentiment, shrinkage covariance, and regime models.
- Conditional Portfolio Optimization: ranking feasible allocations by forward portfolio quality conditional on current state.
- Strategy ensembles spanning momentum, mean reversion, carry, defensive, event-driven, relative-value, and volatility components.
- Dynamic alpha allocation with explicit quarantine, decay detection, retirement, reactivation, capacity, and correlation controls.
- Volatility-aware sizing, stop design, drawdown recovery, crisis behavior, and tail-risk overlays.
- Conditional Parameter Optimization: selecting among strategy controls using contemporaneous state rather than one unconditional optimum.

### Derivatives and volatility

- Implied-versus-realized volatility studies and regime-conditioned option structures such as straddles or spreads.
- Discrete, transaction-cost-aware option hedging across equities, indexes, ETFs, commodities, rates, FX, and crypto options.
- Structured-product and multi-option-book hedging under stochastic volatility, jumps, liquidity changes, and inventory constraints.
- Forecasting and controlling Greeks, hedge bands, rebalance timing, tail loss, and execution cost as joint objectives.

## Frontier and High-Complexity Programs

### Reinforcement learning for hedging

Investigate whether a policy pretrained on theoretical delta targets and refined on realized cost-aware outcomes can outperform implementable delta and hedge-band baselines. A credible program requires synchronized option and underlying data, executable costs, multiple assets and regimes, simulator falsification, tail-risk objectives, and prolonged forward evaluation.

### Reinforcement learning for execution

Study parent-order placement, timing, routing, and urgency using event-level book and fill data. Offline RL, imitation learning, contextual bandits, and constrained actor–critic methods should be judged against VWAP, TWAP, participation, static limit schedules, and simple adaptive urgency rules.

### Conditional optimization systems

Generalize CPO from a small fixed parameter set to high-dimensional strategy controls or portfolio weights. The central research problem is whether a model can rank feasible controls under current state without exploiting noise in a combinatorial candidate set.

### Multi-alpha adaptive allocation

Build allocators that learn changing alpha quality, correlation, capacity, and decay while preventing performance chasing and survivor-only libraries. This combines online learning, Bayesian state models, constrained bandits, risk allocation, and governance.

### Advanced learned hedging and pricing

Explore risk-sensitive or distributional RL for multi-option books, cross-hedging, transaction costs, inventory, and possible learned pricing kernels. This demands validated stochastic-volatility/jump/liquidity simulators and hard operational constraints.

### Generative investment intelligence

Create point-in-time RAG and structured extraction systems for filings, transcripts, reports, macro releases, research, and news. Evaluate retrieval recall, citation precision, numeric accuracy, completeness, contradiction, abstention, analyst time, and downstream signal value separately.

## Strategic Capabilities

- Point-in-time data and model-vintage layer.
- Cross-asset security master and lifecycle accounting.
- Executable-price, cost, latency, capacity, and partial-fill simulator.
- Bias-safe historical universe engine.
- Derivatives chain, lifecycle, Greeks, margin, and settlement support.
- Alternative-data and text provenance layer.
- Robustness, walk-forward, stress, and model-comparison harness.
- Multi-strategy performance, exposure, capacity, and retirement ledger.
- Experiment registry with hypotheses, versions, baselines, falsifiers, and untouched tests.
- Research observability and reproducible model/prompt/data lineage.

These are capability categories, not an instruction to build all of them. Each becomes justified only when a research program actually requires it.

## Vendor and Platform Examples

Treat QuantConnect, AWS/SageMaker/Kendra/Bedrock, PredictNow/QTS, Tiingo, FinBERT, Chronos, MLFinLab, and named LLMs as implementation examples. Preserve the transferable method while independently checking current APIs, licensing, costs, data rights, model versions, and reproducibility.

## Claims Requiring Independent Validation

- Reported strategy, Corrective AI, CPO, Conditional Portfolio Optimization, and RL performance—especially unusually high Sharpe values or retrospective crisis narratives.
- Any comparison lacking identical exposure, cash, leverage, costs, capacity, or constraints.
- Model claims based on synthetic data, one asset, one path, one period, or reused test sets.
- Generated investment recommendations, target prices, facts, formulas, and citations without passage-level support.
- Mathematical expressions flagged in the extracts as malformed, inconsistent, or ambiguously encoded.
- The proposition that better forecasting, more research throughput, or richer generated summaries necessarily produces tradable alpha.
- Historical model leaderboards, token pricing, cloud costs, and vendor feature claims.

## One-Sheet Architecture

The eventual one-sheet should not be a ranked list tied to one experiment. A better structure is:

1. **Research foundations:** data integrity, economic objective, costs, baselines, chronology, and validation.
2. **Signal families:** price/technical, fundamental, macro, alternative/text, event, flow, relative value, and volatility.
3. **Model families:** linear/statistical, tree ensembles, clustering/manifold, deep time-series, LLM/NLP, conditional optimization, and RL.
4. **Decision layers:** universe selection, signal, sizing, entry filtering, execution, exit/risk, allocation, and strategy retirement.
5. **Market coverage:** equities, options, futures, FX, crypto, and multi-asset portfolios.
6. **Evidence ladder:** textbook claim → reproducible baseline → chronological OOS → cross-market/regime replication → realistic execution → forward/live evidence.
7. **Research portfolio:** near-term reproducible studies, medium-term capability-dependent studies, and frontier programs.

## Source Files

- [Chapters 1–3 classification](classification-01-03.md)
- [Chapters 4–6 classification](classification-04-06.md)
- [Chapters 7–9 classification](classification-07-09.md)
- [Chapter extraction index](README.md)
