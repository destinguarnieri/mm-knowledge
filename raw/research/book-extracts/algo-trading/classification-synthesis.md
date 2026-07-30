# Neutral Classification Synthesis: Algorithmic Trading

## Scope and evidence convention

This synthesis deduplicates the classifications for all eight extracted chapters of *Algorithmic Trading: Winning Strategies and Their Rationale*. It is a neutral research inventory, not a recommendation, proof of current profitability, or Money Machine priority ranking. It uses only the supplied extracts.

- **Textbook proposal:** a mechanism, rule, parameter, or claim made by the source.
- **Reported textbook result:** a historical result reported in the extracts; it still requires replication.
- **Classifier inference:** a research implication derived by combining supplied material.
- **Not supported by this book intake:** a plausible claim the extracts do not establish.

## Classification map

| Class | Consolidated contents |
|---|---|
| Foundation | Executable backtests; time-series versus cross-sectional effects; stationarity, cointegration, and half-life; spot/roll/carry decomposition; exposure, leverage, drawdown, and path dependence |
| Methods | Point-in-time and synchronized data; complementary statistical screens; nonoverlapping and walk-forward tests; realistic cost and fill models; signal/sizing/execution separation; log-growth and drawdown stress |
| Directions | Stationary-series and portfolio reversion; seasonal and cross-sectional reversal; currency/futures relative value; interday and intraday momentum; event and flow continuation; leverage and loss-path controls |
| Capabilities | Market-data integrity, instrument/accounting semantics, research-to-live parity, execution simulation, portfolio/risk engines, and experiment governance |
| Frontier | Adaptive state-space relative value, high-frequency index/microstructure research, large point-in-time baskets, and joint tail/liquidity/leverage modelling |
| Validation risk | Leakage, overfit, fragile relations, source-era data and rules, gross-to-net failure, leverage estimation error, rare crises, and ambiguous source formulas |

## Foundational knowledge

### Research evidence and implementation

- **Textbook proposal:** A backtest is a simulation of precise trading instructions. Price field, event time, session boundary, trigger, order type, leg synchronization, borrow, margin, roll, and fill assumptions can change the result.
- **Textbook proposal:** Historical significance is conditional evidence, not a guarantee. More observations improve precision but do not eliminate regime change or selection bias.
- **Classifier inference:** Statistical opportunity, forecast quality, portfolio construction, executable return, and risk control are distinct layers. A valid signal can fail after sizing or costs; an attractive backtest can be manufactured by infeasible prices or exposure.
- **Classifier inference:** Reusing the tested code for automated execution can reduce implementation drift, but live reconciliation and bad-data defenses remain necessary.

### Mean reversion and relative value

- **Textbook proposal:** Time-series mean reversion concerns a series relative to its own history; cross-sectional reversal concerns members relative to a basket. Evidence for one does not establish the other.
- **Textbook proposal:** The source connects mean reversion with stationarity through level dependence and sublinear variance scaling. For the simplified mean-reverting process, $t_{1/2}=-\log(2)/\lambda$ converts a negative regression coefficient into a decay horizon measured in the regression's sampling units. ADF, variance-ratio/Hurst behavior, and half-life provide complementary diagnostics, not a guaranteed strategy.
- **Textbook proposal / classifier inference:** Nonstationary instruments can form a stationary portfolio. CADF addresses a pair; Johansen addresses larger systems. Cointegration can decay, and statistical weights do not automatically define a bounded, self-financing trade.
- **Textbook proposal:** Price spreads, log-price relations, and ratios imply different exposure semantics. The representation must match the intended shares or relative market values and be evaluated separately from the trade rule.
- **Textbook proposal:** Single-stock pairs are described as fragile to company-specific change. ETF and diversified component baskets reduce some idiosyncratic and borrow risk but do not guarantee stable relationships.
- **Textbook proposal:** Currency relative value requires consistent quote orientation, common-value weights, carry, conversion, and rollover accounting. Futures relative value requires contract/multiplier, maturity, settlement, curve, and roll semantics.

### Momentum and event continuation

- **Textbook proposal:** Time-series momentum asks whether an instrument's own past return predicts its future return; cross-sectional momentum asks whether relative winners keep outperforming losers.
- **Textbook proposal:** Persistent futures roll-return sign can supply a momentum mechanism, while stationary roll return can support calendar-spread reversion. Neither property should be assumed from a shared underlying alone.
- **Textbook proposal / classifier inference:** Intraday continuation mechanisms proposed by the source include slow information diffusion, forced rebalancing, stop cascades, displayed-book imbalance, and executed order flow. These are separate hypotheses, not interchangeable proof.
- **Classifier inference:** Event-time availability is part of the signal. A date-only announcement record cannot justify a pre-open trade, and an official open cannot both reveal the signal and be assumed as a guaranteed fill.

### Portfolio construction and risk

- **Classifier inference:** Direction, rank, hedge, position size, staggered holding, leverage, and protection are separate decisions.
- **Textbook proposal:** Constant leverage forces exposure down after losses and up after gains. Gross exposure, not net long-minus-short exposure, is the relevant leverage quantity in a hedged portfolio.
- **Textbook proposal:** Kelly and average-log-growth sizing aim to maximize compounded growth under estimated return distributions. Ruin is a hard boundary; estimation error, nonstationarity, fat tails, serial dependence, financing, and broker constraints can dominate the mathematical optimum.
- **Textbook proposal:** Maximum drawdown is path-dependent and nonlinear in leverage. Historical paths preserve observed dependence but offer few tail events; simulations provide more paths but inherit model misspecification.
- **Textbook proposal:** CPPI changes exposure path by reserving cash and allowing the trading subaccount to shrink after losses. Stops and CPPI cannot guarantee protection through gaps, closures, suspensions, or liquidity vacuums.
- **Textbook proposal:** A leading risk indicator is specific to a strategy-indicator pair; the same state can help one strategy and hurt another.

## Transferable research methods

The following consolidated workflow is **classifier inference** grounded in the supplied chapter methods; it is not evidence that any strategy works.

1. **Executable specification:** Predefine data fields, availability time, sessions, signals, order logic, sizing, exits, fills, synchronization, and accounting before evaluating performance.
2. **Data and universe hygiene:** Use point-in-time memberships, delistings, corporate actions, borrow histories, quote sources, contract mappings, full curves, rollover schedules, and synchronized multi-market timestamps.
3. **Complementary diagnostics:** Combine ADF, variance-ratio/Hurst, $t_{1/2}=-\log(2)/\lambda$ for $\lambda<0$, CADF/Johansen, and direct trading evaluation. Interpret null tests correctly and retain non-rejections as narrowing evidence.
4. **Causal chronology:** Lag all inputs and positions. Fit hedge ratios, eigenvectors, half-lives, thresholds, covariance, and distribution parameters only on prior data.
5. **Independent observations:** When relating look-back and holding-period returns, remove overlap by advancing observations by at least the larger horizon.
6. **Evidence separation:** Report signal or relation stability, forecast quality, gross P&L, cost attribution, executable net P&L, and risk-path behavior separately.
7. **Meaningful controls:** Use no-trade and randomized signals; fixed versus adaptive estimates; sign-only versus threshold rules; price-only versus carry/roll-inclusive return; unhedged versus hedged exposure; and static versus dynamic risk controls.
8. **Walk-forward robustness:** Reserve untouched periods, inspect parameter neighborhoods, retest across regimes and instruments, count independent events/trades, and preserve negative results.
9. **Execution realism:** Include spread, commissions, slippage, bid/ask depth, queue priority, latency, partial fills, auctions, legging, capacity, financing, borrow/recalls, margin, rolls, and gap risk where applicable.
10. **Sizing and stress:** Compare unit, capped, fractional-Kelly, directly constrained, and drawdown-calibrated allocations under pessimistic means, covariance shifts, fat tails, serial losses, gaps, closures, and liquidity failure.

## Concrete research directions

The direction definitions and continue/reject gates below are **classifier inference** assembled from textbook proposals, reported results, and preserved source limitations.

### Mean reversion and relative value

1. **Single-series time-series reversion:** Screen a candidate with complementary stationarity/decay diagnostics, then test a capital-bounded rule against random-walk, no-trade, randomized-signal, and simple fixed-band baselines. Continue only if training-only parameter selection yields stable out-of-sample net evidence without unbounded exposure.
2. **Stationary pairs and diversified portfolios:** Fit CADF/Johansen or economically specified relations on synchronized training data; compare simple pairs, ETF baskets, and component baskets. Continue only if the relationship and executable net P&L survive held-out membership and regime changes without dependence on infeasible legs or a few relations.
3. **Spread/log-spread/ratio representation:** Compare representations under matched gross exposure and cost assumptions. Continue only if the chosen form has a defensible exposure meaning and does not manufacture apparent stationarity.
4. **Bounded bands and dynamic estimates:** Compare fixed or rolling bounded entry/exit rules, scaling-in, and sequential Kalman estimates. Evaluate forecast improvement separately from turnover and net P&L; retain complexity only if it adds stable held-out value.
5. **Seasonal and cross-sectional equity reversal:** Test intraday gap reversal and demeaned relative-return reversal with point-in-time universes, auction-aware fills, borrow, sector/exposure controls, and costs. The long gap result's reported post-2009 decay and the short variant's steeper drawdown are narrowing evidence.
6. **Carry-aware FX relative value:** Normalize quotes and capital, include rollover interest and local-currency conversion, and compare price-only, carry-only, fixed-weight, and rolling-cointegration baselines. Reject apparent spreads that disappear under correct conversion, carry, or synthetic execution.
7. **Futures calendar and intermarket spreads:** Validate curve form, roll-return stationarity, multipliers, maturity alignment, and synchronized closes before trading. Compare economic fixed ratios with fitted hedges and reject relationships dependent on one estimation era.

### Directional and cross-sectional momentum

8. **Interday time-series momentum:** Test independent look-back/holding pairs and staggered sign-based positions on untouched data. Compare total-return and roll-return signals, then stress reversal tails, leverage, contract stitching, and costs.
9. **Roll-return and cross-sectional relative momentum:** Rank instruments or isolate future-versus-underlying/proxy return while attributing spot, roll, financing, basis, and hedge P&L. The reported GLD–GC gross opportunity being largely offset by financing is a preserved negative boundary.
10. **Volatility-scaled opening-gap continuation:** Test same-session continuation beyond a lagged-volatility-adjusted prior range with explicit session and executable-open semantics. Compare sign-only, unscaled breakout, unconditional open-to-close, and symmetric gap-reversion controls.
11. **Timestamp-safe announcement drift:** Test event-specific opening reactions only when announcement availability is established before entry. Use matched non-event gaps and ex ante sizing. The reported negative overnight PEAD return narrows rather than supports a multiday extension.
12. **Leveraged-fund rebalance continuation:** Estimate whether predicted close rebalance demand adds information beyond generic late-day momentum, after investor-flow offsets, auction costs, capacity, and current fund mechanics.
13. **Order-flow and quote imbalance:** Compare displayed, cancellation-aware, and executed-flow features with strict event-time replay. Continue only if predictive lift survives conservative fill, latency, queue, fee, and adverse-selection assumptions. Deceptive quote flipping and stop hunting are operational hazards, not nominated strategies.

### Portfolio, leverage, and protection

14. **Robust leverage and constrained allocation:** Compare full and fractional Kelly, bounded log-growth optimization, direct gross-leverage-constrained allocation, equal risk/capital, and unit leverage. Continue only if the result stays feasible under conservative estimation and tail scenarios.
15. **Drawdown controls:** Compare lower fixed leverage, CPPI, position stops with re-entry, and strategy shutdown under identical unseen paths. Evaluate growth, drawdown, time underwater, breach severity, turnover, and recovery; do not claim guaranteed gap protection.
16. **Strategy-specific leading risk indicators:** Predeclare a small set of lagged indicators and whether they predict return, volatility, or drawdown. Require forward or nested validation and multiple-testing control. The source's opposite VIX associations across two strategies prohibit universal interpretation.

## Strategic capabilities

The capabilities below are **classifier inference** from shared requirements across the classified directions.

- Point-in-time market, universe, event, corporate-action, borrow, and model-availability data.
- Stable instrument identity plus equity, currency, futures-curve, contract, multiplier, expiry, settlement, carry, and conversion semantics.
- Research-to-execution code parity with live decision/fill reconciliation and bad-tick handling.
- Multi-leg portfolio accounting that distinguishes signal units, shares, market value, gross/net exposure, carry, financing, roll, hedge, and local-currency P&L.
- Execution simulator for bid/ask, depth, auctions, queue priority, latency, partial fills, legging, capacity, gaps, closures, and liquidity vacuums.
- Reproducible walk-forward, resampling, nonoverlap, multiple-testing, parameter-sensitivity, and regime-break harnesses.
- Portfolio risk engine for constrained allocation, constant/fractional leverage, covariance, drawdown, CPPI, stops, broker/margin rules, and pathwise stress.

These are capability categories, not automatic build recommendations.

## Frontier / high-complexity directions

- **Adaptive state-space relative value:** Combine dynamic hidden fair value or hedge-ratio estimates with bounded trading. This requires explicit observation/state models, covariance discipline, data-error defenses, and execution evidence beyond smoother estimates.
- **High-frequency index and microstructure research:** Primary-versus-consolidated index latency, component-basket arbitrage, queue reconstruction, and order-flow prediction require direct sequenced feeds, millisecond replay, realistic fills, capacity limits, and continual adaptation.
- **Large point-in-time baskets:** Reproducing broad constituent and cross-market effects requires historical membership, delistings, corporate actions, borrow, synchronized venues, and scalable execution.
- **Information- and flow-conditioned momentum:** News sentiment, institutional flows, and event-specific continuation are proposed mechanisms but lack a complete, validated data/model specification in the extracts.
- **Joint tail, leverage, liquidity, and path-risk modelling:** A serious program would combine non-Gaussian returns, serial dependence, covariance shifts, leverage limits, gaps, closures, and liquidity-dependent execution. The chapters supply components, not a validated joint model.

## Source-specific material

- Named examples—USD.CAD, EWA/EWC/IGE, GLD/USO, SPY components, AUD/CAD crosses, CL calendars, crack spreads, ES/VX, TU, GBPUSD, FSTX, DRN, BGU, and TNA—identify historical demonstrations, not preferred current instruments.
- MATLAB tooling, FxOne, named websites/data series, primary/consolidated-price conventions, source-era session times, contract multipliers, fund objectives, exchange rules, borrow conditions, margins, financing rates, and commissions require current verification.
- Source defaults—including 5-, 20-, 25-, 90-, 200-, 250-, and 252-day windows; fixed Z-score/volatility thresholds; basket sizes; holding periods; maturity gaps; triple-roll conventions; VIX 35; the 30-position divisor; and half-Kelly—are candidate test inputs, not constants.
- The source duplicates Equation 5.11. Chapter 8 Equation 8.4 is unreadable in the extract, and Equation 8.3 retains an OCR verification warning. No formula is silently repaired here.

## Claims requiring independent validation

- Every reported return, Sharpe ratio, drawdown, growth rate, optimal leverage, correlation, p-value, half-life, cointegration result, equity curve, regime narrative, or decay claim.
- The source's phrasing of `p = 0.367281` as roughly a 37% “chance of random walk”; its own methodological warning distinguishes likelihood under a null from posterior probability of the null.
- All critical values, lag conventions, deterministic terms, Hurst interpretations, cointegration weights, curve-linearization assumptions, state-space parameters, and fitted distribution choices.
- Stability and economic rationale of every single-series, pair, basket, cross-rate, calendar, intermarket, momentum, gap, event, rebalance, imbalance, or risk-indicator relationship.
- Current costs, financing, carry, borrow, capacity, margin, leverage, settlement, roll, fund-flow, auction, session, quote, and executable-price assumptions.
- Causal stories involving liquidity pressure, information diffusion, roll persistence, forced rebalancing, stop cascades, informed flow, crowding, or risk indicators.
- **Not supported by this book intake:** current live profitability; a preferred market, timeframe, representation, parameter, or strategy; universal protection from Kelly fractions, CPPI, stops, or risk indicators; or superiority of the historically best variant.

## Preserved negative and mixed findings

- The reported USD.CAD variance-ratio test did not reject random walk; non-rejection does not prove no strategy can work.
- The source nevertheless reports a USD.CAD half-life of about 115 days from the fitted $\lambda$ and uses it as a linear-strategy lookback. That result uses the sample being evaluated, omits transaction costs, and produces positive reported P&L with a large drawdown.
- Passing stationarity does not identify a profitable rule, and the source's linear mean-reversion illustration permits unlimited capital.
- The prototype mean-reversion code intentionally omits transaction costs and uses look-ahead in places; its results are demonstrations, not production evidence.
- Single-stock pairs and fitted intermarket relationships can break; diversification does not guarantee protection when a broken relation dominates.
- The reported long stock gap-reversal result decayed after 2009; the short variant had steeper drawdowns and tighter execution constraints.
- A calendar spread is not necessarily mean reverting. VX is explicitly outside the source's simple constant-return curve model.
- The reported GLD–GC gross opportunity was largely offset by financing, and the reported stock cross-sectional momentum sample was short.
- The tested EURUSD macro-event momentum was reportedly insignificant, while the cited overnight PEAD return was negative.
- Displayed liquidity can be canceled or deceptive; microstructure forecastability does not establish attainable fills.
- Proportional scaling of an unconstrained Kelly vector was suboptimal in the source example. Drawdown did not scale linearly with leverage.
- Stops and CPPI cannot protect through every gap, closure, suspension, or liquidity vacuum. Risk-indicator signs differed by strategy.

## Evidence ladder

1. **Textbook proposal or reported result:** A mechanism, rule, parameter, diagnostic, or historical outcome exists in the extracts.
2. **Faithful reproduction:** Recreate the source result and identify ambiguities, coding assumptions, and data dependencies.
3. **Bias-corrected baseline:** Remove look-ahead, survivorship, overlap, synchronization, representation, and parameter-selection defects.
4. **Executable net backtest:** Add bid/ask, fees, slippage, financing, carry, borrow, rolls, latency, partial fills, capacity, and realistic sizing.
5. **Untouched chronological evidence:** Evaluate fixed decisions on unseen data with independent events/trades and prespecified criteria.
6. **Cross-regime and cross-instrument replication:** Test whether the mechanism survives different periods, instruments, definitions, and stress conditions.
7. **Forward execution evidence — classifier inference:** Verify data arrival, decisions, orders, fills, reconciliation, and operational failure handling before treating a backtest as operational evidence.
8. **Bounded live evidence — classifier inference:** Judge realized net P&L and risk under current costs and operations. Nothing in this intake reaches this rung.

## Broad one-sheet nominations by theme

- **Research validity:** Executable specification, point-in-time data, null interpretation, independent samples, walk-forward gates, and research-to-live parity.
- **Stationary relationships:** Single-series diagnostics, pair/basket cointegration, representation semantics, bounded bands, and break detection.
- **Seasonal and cross-sectional effects:** Gap reversal/continuation, announcement drift, relative reversal, and relative momentum with auction and universe controls.
- **Currency and futures structure:** Quote normalization, carry, spot/roll decomposition, calendar/intermarket spreads, and roll-sign momentum.
- **Directional momentum:** Price and roll-return horizons, staggered holdings, reversal tails, and post-crisis/regime decay.
- **Flow and execution:** Leveraged-fund rebalance pressure, order-flow/quote imbalance, primary-index latency, queueing, and conservative fills.
- **Portfolio and risk:** Gross exposure, constrained/fractional Kelly, drawdown calibration, CPPI, stops, and strategy-specific leading indicators.
- **Evidence ladder:** Textbook statement through faithful reproduction, bias correction, executable net tests, untouched replication, and forward/live evidence.

These nominations define a broad research inventory. They do not establish current priorities.

## Source files

- [Chapters 1–3 classification](classification-01-03.md)
- [Chapters 4–6 classification](classification-04-06.md)
- [Chapters 7–8 classification](classification-07-08.md)
- [Chapter extraction index](README.md)
