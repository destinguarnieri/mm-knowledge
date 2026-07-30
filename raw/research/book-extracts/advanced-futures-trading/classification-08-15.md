# Neutral Classification of Chapters 08–15

## Scope and evidence convention

This batch covers faster and multi-speed trend, directional carry, combined style portfolios, and four proposed signal refinements. Historical comparisons are reported textbook results, not validated findings.

## Foundational knowledge

- Signal speed, turnover and trading cost form one design constraint: a rule is not portable to an instrument merely because its gross forecast is useful.
- Forecasts can be combined only after comparable risk normalization and scaling. Correlated rules require a diversification adjustment followed by a final cap.
- Trend is divergent; carry is convergent and compensates for bearing curve-related risks. Combining them diversifies mechanisms, not merely parameters.
- Futures carry depends on asset-class mechanics and curve location. A generic front/next comparison can mismeasure the carry actually earned.
- Extreme signal values are sparse and noisy. Capping is a robustness control, not proof that the forecast-return relationship is linear below the cap.

## Transferable research methods

1. **Multi-horizon ensemble:** predefine a family of doubled lookbacks, exclude variants that breach an instrument-specific cost speed limit, equal-weight survivors, then apply FDM and cap.
2. **Mechanism-level diversification:** allocate first among economic styles (for example trend and carry), then among rule variants, rather than allowing a style with more parameter variants to dominate.
3. **Forecast reliability curves:** bucket scaled forecasts against later risk-adjusted returns using horizons matched to turnover; inspect uncertainty and nonlinearity before adding mappings.
4. **Incremental-complexity test:** compare a proposed adjustment against the plain rule and the full diversified portfolio. Reject complexity that produces only fragile or economically trivial change.
5. **Regime conditioning without hard labels:** transform a backward-looking, instrument-relative state variable into a continuous multiplier, then test whether it adds value beyond existing risk scaling.
6. **Return decomposition:** separate spot and carry components before attributing a trend signal or claiming diversification.

## Concrete research directions

### 1. Cost-filtered multi-speed trend

- **Textbook basis:** combine EWMAC speeds from very fast to slow; keep only those whose expected annual cost is below a fixed Sharpe-unit budget.
- **Core hypothesis/question:** Does horizon diversification improve net trend capture and robustness beyond the best single speed?
- **Required data:** point-in-time adjusted prices, dated-contract costs and turnover by rule/instrument.
- **Baselines:** EWMAC(16,64), EWMAC(64,256), equal-weight all speeds and a simple sign rule.
- **Evaluation design:** frozen horizon family, instrument-specific eligibility, later-period and cost-stress tests, crisis contribution and cap/scalar sensitivity.
- **Continue only if:** the ensemble beats or stabilizes strong single-speed baselines net of costs without relying on hindsight rule weights.

### 2. Directional carry across futures curves

- **Textbook basis:** annualize a contract-price carry estimate, divide by annualized price-change risk, smooth at multiple horizons, scale, cap and combine.
- **Core hypothesis/question:** Which curve premia are persistent and diversifying after accurate expiry selection, rolls and tail costs?
- **Applicable markets:** rates, FX, equities, volatility, metals, energy and agriculture, with asset-specific carry definitions.
- **Baselines:** no carry; spot/underlying return; simple front-next roll yield; trend-only.
- **Major failure modes:** seasonal curves, incorrect spot proxy, unstable contract gradient, negative skew, expiry mismatch and source-era funding assumptions.
- **Continue only if:** net carry survives alternate curve points, roll rules and seasonal treatments across multiple instruments and regimes.

### 3. Trend–carry style allocation

- **Textbook basis:** combine normalized trend and carry forecasts, illustrated with 60%/40% top-level weights.
- **Core hypothesis/question:** Does economic-style diversification improve portfolio tails and consistency over either style alone?
- **Evaluation design:** freeze top-level weights before the final test; compare equal style weights, risk-based weights and the source mix; decompose exposures and crisis outcomes.
- **Continue only if:** improvement persists across reasonable weights and is not a disguised increase in one asset class or premium.

### 4. Volatility-conditioned trend

- **Textbook basis:** scale trend forecasts by a smoothed function of current volatility relative to its ten-year history; the source reports improvement for trend but not carry.
- **Core hypothesis/question:** Does relative volatility forecast trend quality beyond the effect already captured by inverse-volatility position sizing?
- **Baselines:** unconditioned trend; hard high-volatility exclusion; volatility scaling alone; carry conditioned identically.
- **Major failure modes:** double-counting volatility, regime scarcity, missed crisis trends and a fitted quantile mapping.
- **Continue only if:** the overlay improves later-period net performance and risk across multiple volatility events while retaining meaningful crisis convexity.

### 5. Spot-isolated trend and carry attribution

- **Textbook basis:** recursively subtract estimated accrued carry from adjusted-price changes and apply EWMAC to the resulting synthetic spot.
- **Core hypothesis/question:** Does removing carry from trend improve attribution or portfolio diversification enough to offset weaker standalone trend?
- **Baselines:** ordinary adjusted-price trend; carry alone; ordinary trend plus carry.
- **Continue only if:** the blend improves out-of-sample diversification, tail behavior or interpretability under alternate carry estimates.

### 6. Better carry measurement

- **Textbook basis:** nearer-contract comparisons, seasonal adjustment for front-month holdings, or longer-horizon comparisons for fixed seasonal expiries.
- **Core hypothesis/question:** Does a more faithful estimate of realized carry improve signal quality enough to justify data and operational complexity?
- **Reported textbook result:** tested seasonal and long-horizon refinements did not improve results materially.
- **Decision:** narrow to instruments where ordinary carry is demonstrably biased; do not generalize the extra machinery by default.

## Negative or mixed findings retained

- Nonlinear reversal mappings for extreme EWMAC forecasts added complexity with small or adverse net effects; the source recommends against Strategy 12.
- Synthetic-spot trend was weaker standalone, although potentially useful for attribution and diversification.
- More accurate/seasonal carry adjustments did not justify their complexity in the reported tests.

## Strategic capabilities

- Multi-rule forecast normalization, eligibility, weighting, FDM and cap pipeline.
- Curve-aware futures data with synchronized expiries, spot/carry decomposition and seasonal diagnostics.
- Forecast reliability and monotonicity evaluation with turnover-matched horizons.
- Style/exposure attribution that distinguishes trend, carry, spot and implicit long beta.

## Claims requiring independent validation

All source scalars, horizons, 0.15 Sharpe-unit speed limit, FDM values, selected 60/40 and 40/60 mixes, volatility-regime mapping and reported portfolio results require replication. Asset-class carry formulas and contract conventions require current instrument-level verification.

## Source files

`chapters/08-fast-trend-following-long-short-trend-strength.md` through `chapters/15-accurate-carry.md`.
