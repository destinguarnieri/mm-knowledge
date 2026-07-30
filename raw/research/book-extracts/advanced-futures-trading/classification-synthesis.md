# Classification Synthesis: Advanced Futures Trading Strategies

## Purpose

This synthesis condenses the 38 extracted files (`00`–`37`) into a research-ready map. It preserves portable mechanisms, evaluation methods, implementation constraints, negative evidence and open validation risk. It does not treat the author's backtests, chosen parameters or 102-instrument universe as independently validated evidence or current Money Machine priorities.

## Classification key

| Classification | Meaning |
|---|---|
| Foundational knowledge | Mechanics required to reason correctly about systematic futures strategies. |
| Transferable research method | A reusable specification, test or validation technique. |
| Concrete research direction | A falsifiable signal, portfolio or execution study. |
| Strategic capability | Shared infrastructure needed by multiple studies; not an automatic build recommendation. |
| Frontier/high-complexity | A direction with unusual capital, data, execution or operational demands. |
| Source-specific | Author, broker, contract, parameter or source-era detail that is not portable as stated. |
| Independent-validation claim | A result or rule that must be replicated before use. |

## Foundational knowledge

### Futures lifecycle and price semantics

- Futures exposure lives in dated contracts with multiplier, currency, expiry, settlement, delivery and margin rules. Continuous exposure requires explicit contract choice and rolling.
- Keep analytical series separate from execution data. A back-adjusted series is useful for signals and excess-return histories, but current dated-contract prices are required for notional, cash P&L and orders.
- Carry, spot movement and roll adjustment are distinct. Their definitions vary by asset class and curve position.
- Synthetic spreads and triplets can have low measured volatility but high gross leverage, leg risk and nonlinear tails.

### Risk, capital and portfolio construction

- Position sizing starts from capital and a risk budget, not from an arbitrary contract count. Current price, multiplier, FX, volatility and integer rounding jointly determine executable exposure.
- Volatility targeting stabilizes expected risk but does not remove jump, correlation, liquidity, leverage or model risk.
- Portfolio diversification comes from imperfect correlation across instruments and mechanisms. A multiplier used to restore risk after diversification also restores leverage.
- Contract granularity creates capital thresholds. When independent rounding destroys a broad portfolio, integer optimization may approximate the ideal risk exposure.
- Initial margin is not a risk budget. Free cash must absorb variation margin; compounding policy controls how risk evolves with account equity.

### Forecast architecture

- A portable rule separates raw signal, risk normalization, scalar, cap, rule combination, portfolio weight, position sizing, buffering and execution.
- Comparable forecasts can be combined across horizons and styles only after consistent scaling. Diversification multipliers correct the shrinkage from imperfectly correlated forecasts; a final cap limits extreme exposure.
- Trend is a divergent mechanism; carry and mean reversion are convergent. Cross-sectional signals remove or compare against a peer reference; they are not automatically market neutral.
- Signal value and portfolio value differ. A weak standalone rule can help only when low correlation survives costs and stress.

### Execution and controls

- Trading speed, cost, liquidity, size and signal horizon are a joint constraint.
- Passive execution reduces average spread only by accepting uncertain completion and adverse-selection tails.
- Risk overlays sit outside alpha logic and should only reduce positions. Hard position/trade limits protect against both markets and software errors.

## Transferable research methods

1. **Point-in-time contract-chain reconstruction:** preserve dated prices, rolls, multipliers, FX, liquidity, FND/delivery and settlement.
2. **Risk-first executable sizing:** derive unrounded risk exposure, then quantify integer rounding, margin and capital-cohort effects.
3. **Forecast normalization and reliability:** normalize raw signals by contemporaneous risk, calibrate without leakage, cap extremes and verify forecast-return monotonicity.
4. **Cost-speed eligibility:** estimate risk-adjusted cost per trade and turnover, then exclude rule/instrument combinations that cannot clear a predeclared net hurdle.
5. **Mechanism-first ensembles:** allocate among distinct styles before distributing weight among parameter variants; avoid giving extra weight to a style merely because it has more variants.
6. **Representation ablations:** compare adjusted price, synthetic spot, normalized price, common asset-class price and relative price while keeping downstream mechanics fixed.
7. **Incremental-complexity gate:** accept a refinement only when it improves a simple baseline or the full portfolio by a material, stable amount.
8. **Granularity-aware portfolio comparison:** test static subsets, independent rounding and covariance-aware integer optimization across realistic capital levels.
9. **Execution-sensitive replay:** include decision timestamps, latency, gaps, non-fills, partial fills, spread, commission, impact and capacity; require forward shadow evidence for fast rules.
10. **Stress and tail decomposition:** isolate volatility jumps, correlation convergence, leverage, negative skew, margin escalation and influential crises.
11. **Negative-result retention:** record when a refinement fails or when hedging removes the premium; do not let the final inventory contain only winners.

## Concrete research directions

### Directional risk premia and portfolio foundations

- **Volatility-targeted diversified futures portfolio:** compare fixed-contract, fixed-notional, equal-risk and dynamically risk-scaled portfolios with realistic rolls, costs and granularity.
- **Risk-premium baseline:** independently establish which directional futures premia remain positive after current carry, financing, margin and tail costs.
- **Capital-constrained portfolio approximation:** compare static instrument selection with covariance-aware integer optimization for small accounts.

### Trend family

- **Cost-filtered multi-speed EWMAC:** test whether a fixed family of horizons improves robustness beyond strong single-speed baselines.
- **Trend strength versus sign:** test whether normalized magnitude contains incremental information beyond direction.
- **Alternative representations:** ordinary, normalized-price, asset-class, synthetic-spot, breakout and acceleration trend should be treated as ablations or correlated additions, not independent proof of many alphas.
- **Volatility-conditioned trend:** test whether relative-volatility state predicts signal quality beyond existing inverse-volatility sizing.

### Carry and curve family

- **Directional carry:** replicate asset-specific carry across curve points, roll conventions and seasonal regimes.
- **Trend–carry ensemble:** test broad, predeclared style weights and attribute hidden long beta, curve exposure and crisis behavior.
- **Cross-sectional carry:** test within-class relative carry as a small diversifier, with directional carry as the primary baseline.
- **Carry-measurement refinement:** pursue seasonal or spot-aware corrections only where ordinary curve carry is demonstrably biased; the source's broad refinements did not improve results.

### Relative and cross-sectional signals

- **Cross-sectional momentum:** compare directional and market-neutral implementations with point-in-time class membership and monotonic rank tests.
- **Long-horizon relative value:** test multi-year mean reversion using several horizons and long independent histories; statistical power is inherently limited.
- **Skew premium:** test robust tail measures, outlier sensitivity and compensation across multiple crash episodes.

### Fast strategies and execution

- **Fast mean reversion:** require conservative limit-fill and gap models plus forward shadow execution.
- **Trend/volatility-gated mean reversion:** separately test each safety overlay and its interaction rather than accepting the source's unusually strong combined result.
- **Expiry/roll policy:** compare liquidity-first expiry selection, roll timing and passive versus explicit roll execution.
- **Passive-first execution:** benchmark total implementation-shortfall distribution and completion reliability against immediate and schedule-based baselines.

### Multi-leg relative value

- **Cross-instrument spreads and butterflies:** test only economically identified relationships with synchronized legs, time-varying hedge ratios and correlation-break stress.
- **Calendar spreads/triplets:** treat them as curve-shape trades; evaluate synchronized rolling, combination liquidity, high gross leverage and crisis equilibrium shifts.
- The source's tested trend and carry implementations were mostly weak. The retained question is whether a narrower mechanism or faster trend-aligned mean reversion works—not a presumption that generic RV has edge.

### Portfolio risk controls

- **Downside-only overlay:** compare margin, expected-risk, jump, correlation-shock and leverage multipliers separately and jointly under historical and synthetic stress.
- **Hard operational limits:** validate position, leverage, open-interest and trade-size limits independently from statistical forecasts.

## Negative and mixed findings

- Nonlinear mappings of extreme trend forecasts added complexity without compelling net benefit.
- Synthetic-spot trend improved attribution but weakened standalone trend.
- More elaborate seasonal/long-horizon carry estimation did not improve the reported results.
- Normalized trend was almost a substitute for ordinary trend; asset-class trend reduced aggregate within-class diversification.
- Cross-sectional momentum, cross-sectional carry, value and several alternative trend rules were weak standalone and justified only as bounded diversification hypotheses.
- Generic spread, triplet and calendar trend/carry results were underwhelming; low synthetic volatility concealed leverage and tail risk.
- The reported fast mean-reversion portfolio evidence is short and execution-model dependent.

## Frontier / high-complexity programs

### Execution-aware fast strategies

Hourly or finer strategies require event-level orders and fills, conservative counterfactual execution, automated state management, capacity limits and forward shadow/live-small evidence.

### Capital-constrained broad-universe optimization

Dynamic integer optimization can preserve diversification but depends on robust covariance, transaction-cost, margin and concentration controls. Greedy results should be checked against exact solutions on small cases.

### Multi-leg RV portfolio

A serious program requires synchronized contract chains, combination-order execution, roll orchestration, hedge recalibration, nonlinear tail/margin stress and an economically constrained candidate universe.

## Strategic capabilities

- Point-in-time futures security master and contract-chain/lifecycle store.
- Separate analytical continuous series and executable dated-contract data.
- Versioned signal/forecast pipeline with normalization, scalar, cap, FDM, IDM, buffer and position audit trail.
- Risk, covariance, FX, margin, cash and integer-position engine.
- Roll-, cost-, latency-, partial-fill- and impact-aware simulator.
- Order-level execution analytics and forward shadow recorder.
- Multi-leg synthetic instrument engine.
- Stress harness for volatility, jump, correlation, leverage, liquidity and margin shocks.
- Experiment registry preserving source proposal, preregistered variation set, baselines, costs, falsifier and untouched test.

These are capability categories. Build only the smallest capability required by an active evidence question.

## Source-specific material

Treat the following as historical/reference inputs: the author's 102-instrument Jumbo universe; broker codes and chosen exchanges; source-era first-data years, contract facts, costs and liquidity; named vendors/websites; 20% risk target; 32/35-day volatility spans; 30/70 blend; EWMAC horizon family; forecast scale 10 and cap 20; 0.15 Sharpe-unit speed limit; FDM/IDM tables; allocation percentages; liquidity/margin/execution thresholds; and personal compounding practices.

## Claims requiring independent validation

1. Every reported strategy Sharpe, skew, drawdown, alpha, diversification gain and asset-class comparison.
2. All causal narratives for trend, carry, skew, value, breakout, volatility regimes and mean reversion.
3. The stability of forecast scalars, caps, FDM/IDM and style weights across time and universe.
4. Instrument eligibility, contract specifications, delivery/settlement, liquidity, costs, margin and data availability.
5. Passive-order fills, execution-algorithm savings and the fast-strategy results built on them.
6. Relative-value hedge stability and any conclusion drawn from a small set of spreads/triplets/calendars.
7. Risk-overlay thresholds and the proposition that historical 99th-percentile controls protect future tail states.
8. Generalization from the author's broad daily futures universe to a narrower venue, asset set, bar frequency or capital level.

## One-sheet architecture

1. **Contract truth:** identity, expiry, roll, settlement, multiplier, currency and executable price.
2. **Signal:** trend, carry, relative/cross-sectional, mean reversion or tail statistic.
3. **Forecast transformation:** risk normalization, scalar, cap, smoothing and ensemble.
4. **Portfolio:** instrument/style weights, diversification multipliers, integer optimization and capital.
5. **Execution:** buffer, urgency, order type, fills, impact, roll and capacity.
6. **Risk:** margin, jump, correlation, leverage, liquidity and hard limits.
7. **Evidence ladder:** textbook proposal → reproduced gross baseline → point-in-time net backtest → alternate universe/regime → realistic execution → forward shadow → authorized live evidence.

## Broad one-sheet nominations by theme

- Multi-speed trend versus breakout/acceleration representation ablation.
- Directional carry across curve points and roll conventions.
- Trend–carry fixed versus volatility-conditioned allocation.
- Fast mean reversion with conservative fill modelling; trend and volatility gates as separate ablations.
- Capital-cohort comparison of static subset, rounding and dynamic integer optimization.
- Expiry/roll-policy and passive-first execution benchmark.
- Cross-sectional momentum/carry/value as bounded portfolio diversifiers.
- Economically identified spread/calendar RV under synchronized execution and correlation stress.
- Downside-only portfolio-risk overlay under historical and synthetic shocks.

These are research inventory items, not current priority recommendations.

## Source files

- [Chapters 00–07 classification](classification-00-07.md)
- [Chapters 08–15 classification](classification-08-15.md)
- [Chapters 16–23 classification](classification-16-23.md)
- [Chapters 24–30 classification](classification-24-30.md)
- [Chapters 31–37 classification](classification-31-37.md)
- [Chapter extraction index](README.md)
