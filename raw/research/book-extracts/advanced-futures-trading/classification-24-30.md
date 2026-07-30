# Neutral Classification of Chapters 24–30

## Scope and evidence convention

This batch moves from a worked signal-research case study into capital-constrained portfolio optimization, hourly mean reversion, and two- or three-leg relative-value trading. It includes the book's strongest warnings about execution-model risk, leverage hidden by low synthetic volatility, and short samples.

## Foundational knowledge

- A candidate statistic is not a strategy until it is robustly measured, normalized to expected risk-adjusted return, smoothed where appropriate, scaled, capped, costed, sized and evaluated in a portfolio.
- A low-volatility synthetic spread can require very high gross leverage. Hedging outright direction may remove risk premia while leaving basis, correlation, liquidity and tail risk.
- Relative-value spreads, butterflies and calendars are multi-leg instruments whose executable hedge ratios, integer contracts, synchronized rolls and joint fills matter more than a clean synthetic series suggests.
- Intraday mean reversion couples signal and execution: passive orders can create apparent alpha that disappears under non-fill, gap and adverse-selection assumptions.
- Portfolio rounding is an optimization problem when capital is small relative to contract granularity. The objective should be tracking the ideal risk exposure, not simply rounding every leg independently.

## Transferable research methods

1. **Idea-to-forecast pipeline:** quantify an economic hypothesis; perturb inputs to test robustness; predefine parameter families; normalize, smooth, scale and cap; then test standalone and incremental value.
2. **Covariance-aware integer approximation:** minimize tracking error between ideal and executable integer portfolios, with explicit transaction-cost penalty and portfolio-level no-trade buffer.
3. **Execution-sensitive replay:** model signal timestamps, one-period latency, passive-order non-fills, gaps, partial fills, commissions and volume/capacity before accepting fast-strategy results.
4. **Synthetic-instrument audit:** derive leg ratios from multiplier, FX and risk units; compute gross exposure, correlation sensitivity, tail risk, minimum capital and two-/three-leg costs.
5. **Mechanism-specific baselines:** compare spreads against outright trades, triplets against spreads, calendars against cross-instrument RV, and safer mean reversion against both pure mean reversion and trend.
6. **Negative-result retention:** treat unprofitable carry/trend in spreads or triplets as evidence that hedging may remove the premium, not as a reason to omit the research record.

## Concrete research directions

### 1. Skew-premium forecast

- **Textbook basis:** buy instruments with more negative recent return skew and short positive-skew instruments; combine several three-to-twelve-month windows.
- **Core hypothesis/question:** Are investors compensated for bearing negative skew in a way that survives outlier sensitivity and crises?
- **Baselines:** no signal; unconditional long risk premia; robust tail measures; randomly signed exposure with matched risk.
- **Evaluation design:** point-in-time rolling moments, perturbation tests, outlier leave-one-out, crisis attribution and alternative robust estimators.
- **Major failure modes:** unstable sample skew, crash concentration, circular risk-premium story and pooled scalar overfit.
- **Continue only if:** the forecast is stable to small data changes and earns net compensation across multiple independent tail episodes.

### 2. Dynamic integer portfolio optimization

- **Textbook basis:** greedily choose integer contracts that minimize covariance-aware tracking error to a broad unrounded portfolio, penalize costs and buffer at portfolio level.
- **Core hypothesis/question:** Can small capital capture more broad-universe diversification than static subset selection?
- **Baselines:** per-instrument rounding, static instrument subset, nearest-integer positions and mixed-integer/global optimization on small cases.
- **Evaluation design:** capital cohorts, tracking error, net turnover, concentration, covariance error, proxy substitution and stress liquidity.
- **Continue only if:** executable portfolios preserve material diversification net of added turnover and remain stable to covariance/cost estimation error.

### 3. Fast mean reversion with realistic passive execution

- **Textbook basis:** compare hourly price with a daily five-day EWMA equilibrium; use one-lot limit ladders and market catch-up only when position error exceeds one contract.
- **Core hypothesis/question:** Does multi-day mean reversion survive fills, gaps, commissions and capacity?
- **Required data:** timestamped hourly or finer quotes/trades, dated contracts, order-book/fill assumptions and current costs.
- **Baselines:** market-order mean reversion, no fill advantage, simple reversal, and matched-turnover trend.
- **Major failure modes:** optimistic limit fills, post-signal pricing, short 2013-era sample, negative skew and automation failure.
- **Continue only if:** results remain positive under conservative non-fill/adverse-selection models and forward shadow execution.

### 4. Trend- and volatility-gated mean reversion

- **Textbook basis:** trade only dips aligned with slower trend and reduce exposure during high relative volatility.
- **Core hypothesis/question:** Do trend agreement and volatility conditioning reduce falling-knife losses without selecting the source sample's crises?
- **Baselines:** pure mean reversion; trend alone; each gate separately; hard stop with explicit re-entry.
- **Continue only if:** both overlays show incremental later-period value and performance survives stricter execution models.

### 5. Cross-instrument and calendar relative value

- **Textbook basis:** build two-leg spreads and three-leg butterflies from related futures; test trend and carry; extend the construction across expiries of one market.
- **Core hypothesis/question:** Are curve, basis or relative-price moves predictable enough to overcome gross leverage, leg risk and multi-leg cost?
- **Applicable markets:** economically linked rates, commodities and sufficiently liquid calendar curves.
- **Baselines:** outright rules, static beta/duration hedges, no-trade cost bands, simple equilibrium reversion and exchange-listed combination orders.
- **Evaluation design:** synchronized dated-contract replay, time-varying hedge ratios, joint/partial fill scenarios, roll constraints, correlation breaks, margin and tail stress.
- **Reported textbook result:** tested trend/carry spreads and triplets were generally weaker than outright trades; calendar trend was episodic and carry unconvincing.
- **Continue only if:** a specific economically identified relationship survives conservative leg execution and stress, rather than a mined set of combinations.

## Frontier / high-complexity directions

- **Execution-aware intraday mean reversion:** requires automated order state, conservative fill simulation and forward shadow evidence.
- **Capital-constrained broad-universe optimizer:** requires reliable covariance, costs, integer optimization, margin and live position controls.
- **Multi-leg RV portfolio:** requires synchronized contract data, combination execution, hedge maintenance and nonlinear tail/margin modelling.

## Strategic capabilities

- Integer portfolio optimizer with transparent tracking-error and cost decomposition.
- Event-aware order/fill simulator and forward shadow-execution recorder.
- Synthetic spread/triplet builder with multiplier, FX, covariance, margin and roll accounting.
- Robust-statistic and input-perturbation test harness.

## Claims requiring independent validation

The source's skew premium, hourly mean-reversion results, exceptional safer-strategy Sharpe, greedy optimizer performance, correlation/volatility estimates, hedge ratios, cost assumptions and claims about which horizons trend or mean-revert all require replication. The book's limited spread/triplet/calendar sample cannot establish broad absence or presence of edge.

## Source files

`chapters/24-skew-case-study.md` through `chapters/30-calendar-trading-strategies.md`.
