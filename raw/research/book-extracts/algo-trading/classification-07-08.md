# Neutral Classification of Chapters 7–8

## Scope and evidence convention

This file condenses the supplied extracts for Chapters 7–8 into a research inventory covering intraday momentum and risk management. It does not establish that any proposed mechanism, parameter, historical result, or causal account remains valid. The following labels distinguish provenance:

- **Textbook proposal:** a mechanism, rule, parameter, or claim made by the source.
- **Reported textbook result:** a historical result reported in the extracts; it still requires replication.
- **Classifier inference:** a research implication derived by combining or generalizing supplied material.
- **Not supported by this batch:** a plausible claim that these chapters do not establish.

## Classification map

| Class | Consolidated inventory |
|---|---|
| Foundational knowledge | Short-horizon continuation mechanisms; event-time integrity; order-book versus executed-flow information; constant leverage and ruin; gross versus net exposure; nonlinear drawdown; path-dependent protection |
| Transferable methods | Lagged volatility-scaled triggers; timestamp-safe event studies; net executable backtests; average-log-growth sizing; constrained portfolio allocation; simulated-versus-historical drawdown stress; strategy-specific risk gating |
| Concrete directions | Opening-gap continuation; announcement drift; leveraged-ETF close rebalancing; order-flow/quote imbalance; leverage and portfolio sizing; drawdown controls; leading risk indicators |
| Frontier / high complexity | Execution-sensitive microstructure research; joint tail, leverage, liquidity, and path-risk modelling |
| Strategic capabilities | Point-in-time event data; intraday and order-book data; execution/cost simulation; portfolio risk engine; reproducible stress and sensitivity testing |
| Validation risk | Old and narrow samples, source defaults, look-ahead bias, distributional assumptions, rare-crisis samples, instrument conventions, execution feasibility, OCR ambiguity |

## Foundational knowledge

- **Textbook proposal:** Intraday continuation may arise from slow news diffusion, fund rebalancing, stop cascades, displayed liquidity imbalance, or signed transaction flow. These are distinct causal stories and should not be treated as interchangeable evidence for one generic momentum effect.
- A breakout signal is directional, while leverage, portfolio allocation, CPPI, and stops govern exposure or loss paths. Forecast quality and sizing quality therefore require separate evaluation.
- Event-time integrity is part of the signal definition. A date-only earnings record cannot establish whether information was available before the intended opening trade.
- Displayed bid/ask size is cancellable intent; signed order flow describes executed transactions. Either may be strategic or incomplete, and neither by itself establishes informed trading.
- **Textbook proposal:** Constant leverage requires reducing exposure after losses and increasing it after gains. Equity reaching zero makes compounded growth minus 100%, so avoiding ruin is a hard constraint rather than an ordinary performance penalty.
- Gross leverage is the sum of absolute portfolio exposures relative to equity, not net long-minus-short exposure. Portfolio covariance affects allocation even when individual strategy forecasts are unchanged.
- Maximum drawdown is path-dependent and nonlinear in leverage. Halving leverage need not halve drawdown, and two allocations with similar average returns can have materially different loss paths.
- CPPI differs from merely applying a lower fixed leverage to the whole account: its trading subaccount shrinks after losses and is replenished only at a new high-water mark. Stops and CPPI cannot guarantee protection across gaps, closures, suspensions, or liquidity vacuums.
- A leading risk indicator is strategy-specific. The same market state may be adverse for one strategy and favorable for another.

## Transferable research methods

- Define intraday sessions explicitly by instrument, including open, close, overnight interval, timestamp zone, and tradable price. Lag volatility estimates and all other features to prevent leakage.
- Express breakout and event thresholds in volatility units, then test the threshold as a source default rather than a universal constant. Compare against no-threshold, sign-only, fixed-price, and simple prior-range baselines.
- Build event studies from point-in-time announcement timestamps. Enforce an information cutoff, distinguish after-close from before-open announcements, and audit ambiguous or missing times.
- Separate gross signal return from executable net return. Model spread, commission, slippage, queue position, partial fills, cancellation, latency, capacity, and forced liquidation where relevant.
- Evaluate signal and holding-period alternatives without assuming an effect remains multiday. The supplied extract reports that some previously longer-lived event effects shortened to intraday.
- For leverage, optimize average log wealth, `g(f) = mean[log(1 + fR)]`, subject to `1 + fR > 0`, broker constraints, and drawdown tolerances. Under the source's Gaussian approximation, single-strategy Kelly is `f = m/s²`; for multiple portfolios it is `F = C⁻¹M`.
- Treat Kelly output as an estimate under strong assumptions, not an instruction. Compare full, fractional, capped, and constrained-optimal allocations under parameter error and nonstationarity.
- Compare two imperfect drawdown lenses: simulations provide more paths but depend on the fitted distribution and may omit serial dependence; historical paths preserve realized dependence but provide few tail observations.
- When testing CPPI, fixed leverage, or strategy stops, compare pathwise exposure and recovery rules rather than only terminal return. Keep one-strategy and multistrategy implementations distinct.
- Test leading indicators separately per strategy with out-of-sample or forward evidence. Rare crises make threshold selection and feature searches especially prone to data snooping.
- Preserve negative findings as boundaries: no significant tested EURUSD momentum around the cited macro events; negative average overnight PEAD returns in the cited sample; proportional scaling of a capped Kelly vector was suboptimal in the source example; one VIX threshold had opposite associations for two strategies.

## Concrete research directions

### 1. Volatility-scaled opening-gap continuation

- **Textbook basis:** **Textbook proposal:** Enter long when the open exceeds the prior high by a lagged-volatility threshold, short below the prior low by the symmetric threshold, and exit at the same close. The source default uses a 90-day close-to-close volatility and `z = 0.1`.
- **Core hypothesis/question:** Does an opening move beyond the prior range predict same-session continuation after executable costs?
- **Applicable markets:** The extract applies it to FSTX futures and GBPUSD; broader portability is **not supported by this batch**.
- **Required data:** Daily or session-aligned OHLC, lagged volatility inputs, explicit market/session definitions, and cost/execution data.
- **Candidate methods/rules:** Reproduce the source rule; vary volatility window, threshold, direction, and exit time; keep currency open/close conventions explicit.
- **Meaningful baselines:** Open-to-close unconditional return, gap sign only, prior-range break without volatility scaling, and a symmetric gap mean-reversion rule.
- **Evaluation design:** Point-in-time walk-forward tests by instrument and regime, with trade count, long/short decomposition, gross/net returns, drawdowns, and sensitivity to session boundary and threshold.
- **Major failure modes:** Open-price infeasibility, stale or misaligned sessions, threshold selection bias, stop-cascade story not generalizing, sparse independent events, and regime decay.
- **Continue only if:** The effect is directionally stable across reasonable definitions and remains positive net of realistic opening execution costs; narrow to the instruments or sessions where it survives, otherwise reject.

### 2. Timestamp-safe post-announcement intraday drift

- **Textbook basis:** **Textbook proposal:** For earnings released after the prior close and before the current open, trade in the direction of an opening gap of at least `0.5` times its lagged 90-day standard deviation and exit at the close. The cited test divides exposure by 30, a maximum selected with acknowledged look-ahead bias.
- **Core hypothesis/question:** Does the market's abnormal opening reaction to a known pre-open corporate event continue through the session?
- **Applicable markets:** The extract tests S&P 500 stocks and discusses earnings, guidance, analyst changes, operating metrics, M&A, and index changes. Each event family requires a separate test.
- **Required data:** Survivorship-aware point-in-time universe, announcement timestamps and types, adjusted intraday prices, volume/liquidity, and executable open/close prices.
- **Candidate methods/rules:** Reproduce earnings-gap continuation; replace the fixed 30-position divisor with ex ante capital allocation; compare same-day and longer exits without pooling event types.
- **Meaningful baselines:** All event names, gap direction without an event filter, matched non-event gaps, market/sector-adjusted returns, and no overnight hold.
- **Evaluation design:** Timestamp audit; event-day walk-forward test; overlap and clustering controls; separate surprise proxy, gap magnitude, announcement timing, liquidity, and market-state strata; report gross and net performance.
- **Major failure modes:** Date-only data, post-open leakage, universe bias, event-type heterogeneity, crowding, opening slippage, leverage extrapolation, and choosing portfolio normalization from the full sample.
- **Continue only if:** The result survives strict availability cutoffs, ex ante sizing, matched-gap baselines, and current net-cost replication. The cited negative overnight return narrows rather than supports an overnight extension.

### 3. Leveraged-ETF close-rebalancing continuation

- **Textbook basis:** **Textbook proposal:** Constant-leverage funds mechanically add same-direction exposure near the close after a large index move. The source example trades DRN in the final 15 minutes after a move beyond plus or minus 2%, then exits at the close.
- **Core hypothesis/question:** Is predictable rebalance demand large enough to generate executable late-day continuation, conditional on offsetting investor flows?
- **Applicable markets:** Leveraged long and inverse funds and their underlying exposures; the literal test is DRN.
- **Required data:** Intraday fund and underlying prices, fund leverage/objective, assets or flow proxies, rebalance timing, closing-auction data, spread, volume, and costs.
- **Candidate methods/rules:** Reproduce the 2%/15-minute rule; estimate required rebalance demand; stratify by move size, fund exposure, investor flows, and auction conditions.
- **Meaningful baselines:** Same late-day move without relevant leveraged-fund exposure, unleveraged fund controls, sign-only continuation, and auction-only execution.
- **Evaluation design:** Walk-forward test across funds and days; distinguish forecast from attainable fill; evaluate capacity and whether flow estimates improve the fixed threshold.
- **Major failure modes:** Short and dated sample, offsetting subscriptions/redemptions, changing fund assets or mechanics, endogeneity, auction impact, and decay through competition.
- **Continue only if:** Predicted rebalance pressure adds out-of-sample information beyond generic late-day momentum and survives realistic auction or pre-close execution; otherwise narrow to measurable high-pressure cases or reject.

### 4. Order-flow and quote-imbalance signals

- **Textbook basis:** **Textbook proposal:** Large bid/ask imbalance or signed executed flow may predict the next price move because urgent informed trading affects quotes. The extract also describes ratio trades and quote matching, alongside deceptive flipping and stop hunting.
- **Core hypothesis/question:** Do observable imbalance measures predict short-horizon returns strongly enough to exceed spread, fees, adverse selection, and queue costs?
- **Applicable markets:** Transparent order-book markets; currency futures are suggested where dealer spot transaction reporting is insufficient.
- **Required data:** Sequenced depth, trades, aggressor-side classification, order additions/cancellations, tick size, queue state, latency, fees, and fills.
- **Candidate methods/rules:** Predictive models using displayed imbalance, cancellation-aware imbalance, and signed flow over lagged windows; evaluate passive and aggressive execution separately.
- **Meaningful baselines:** Last-price direction, spread and depth alone, random queue entry, and zero-signal market making.
- **Evaluation design:** Event-time forward validation with strict causality, replay or fill simulation, latency perturbation, capacity limits, and full cost accounting.
- **Major failure modes:** Spoof-like displayed liquidity, trapped quotes, canceled supporting bids, incomplete transaction feeds, misclassified trade direction, unwanted large fills, and speed competition driving net edge toward zero.
- **Continue only if:** Predictive lift remains after cancellation-aware features and conservative fill/cost assumptions. The deceptive tactics described by the source are recorded as hazards, not endorsed research implementations.

### 5. Leverage and constrained portfolio allocation

- **Textbook basis:** **Textbook proposal:** Maximize compounded log growth with constant leverage; use Gaussian Kelly only under its assumptions, numerical optimization for fitted non-Gaussian returns, or historical returns with explicit data-snooping caution. Under a gross-leverage cap, proportional scaling of an unconstrained Kelly vector need not maximize growth.
- **Core hypothesis/question:** What exposure maximizes robust compounded growth without unacceptable ruin, drawdown, or broker-constraint risk under estimation uncertainty?
- **Applicable markets:** Any strategy with a return series; the relevant return is the strategy return, not the underlying market-price return.
- **Required data:** Net strategy returns, covariance across strategies, risk-free-rate convention, leverage and margin rules, and enough history or defensible simulated scenarios to assess tails.
- **Candidate methods/rules:** Full/fractional Kelly; bounded average-log-growth optimization; covariance-aware allocation; direct constrained optimization; sensitivity to mean, variance, tails, and correlation.
- **Meaningful baselines:** Unit leverage, equal risk or equal capital, capped proportional Kelly, half-Kelly, and allocation to the strongest single strategy under the same cap.
- **Evaluation design:** Estimate only on past data; evaluate forward growth, ruin probability, gross exposure, turnover, drawdown, and sensitivity to pessimistic parameter shifts and extreme losses.
- **Major failure modes:** Nonstationarity, mean/covariance error, fat tails, invalid fitted distributions, serial dependence, hidden gross leverage, financing omission, historical optimizer overfit, and optimizer regions where `1 + fR <= 0`.
- **Continue only if:** The allocation remains feasible and materially preferable across conservative estimation and tail scenarios; reduce leverage when overestimation can cause ruin even if underestimation sacrifices growth.

### 6. Drawdown controls: leverage reduction, CPPI, and stops

- **Textbook basis:** **Textbook proposal:** Calibrate leverage against drawdown paths; use CPPI to reserve `1-D` of equity as cash and trade a `D` subaccount, resetting only at new highs; use position stops for re-enterable trades and prefer CPPI over a strategy-level stop for account protection.
- **Core hypothesis/question:** Which control best limits realized loss paths while preserving acceptable growth for a given strategy's holding period and failure modes?
- **Applicable markets:** Single-strategy accounts for the source CPPI rule; position stops apply where exits are executable. Multistrategy CPPI is explicitly cautioned against because winners can subsidize a failing strategy.
- **Required data:** Strategy returns at the intended rebalancing frequency, intraday adverse excursions for position stops, gap/closure scenarios, liquidity, and execution constraints.
- **Candidate methods/rules:** Fixed fractional leverage, simulated or historical drawdown-calibrated leverage, CPPI by chosen `D`, position stops with re-entry, and de facto momentum exits when signals reverse.
- **Meaningful baselines:** Uncontrolled fixed leverage, lower fixed leverage `fD`, no stop, and simple strategy shutdown thresholds.
- **Evaluation design:** Pathwise scenario tests including serial losses, gaps, closures, liquidity vacuums, and recovery; measure growth, maximum drawdown, time underwater, turnover, and breach severity.
- **Major failure modes:** Nonlinear leverage/drawdown relation, simulated-path misspecification, sparse historical tails, gap-through stops, suspended markets, costly protection, CPPI exhaustion, and survivorship bias when selecting mean-reversion stops from observed history.
- **Continue only if:** The control reduces breach frequency or severity in unseen and stressed paths without relying on impossible fills. No method should be represented as a guaranteed gap or closure hedge.

### 7. Strategy-specific leading risk indicators

- **Textbook basis:** **Textbook proposal:** Condition future strategy risk on lagged indicators such as VIX, TED spread, HYG, MXN, ONN/OFF, commodity inputs, Baltic Dry Index, or high-frequency order flow.
- **Core hypothesis/question:** Does a pre-specified lagged indicator forecast next-period loss or alter expected strategy return enough to justify exposure changes?
- **Applicable markets:** Only the strategy-indicator pair tested; universality is **not supported by this batch**.
- **Required data:** Point-in-time indicator histories, strategy returns, release/publication timing where relevant, and enough stress episodes for evaluation.
- **Candidate methods/rules:** Predeclared thresholds, continuous risk scaling, or indicator-conditioned leverage; compare economic-state and direct market/microstructure indicators separately.
- **Meaningful baselines:** Unconditioned strategy, contemporaneous volatility scaling, shuffled indicator, and simple lagged strategy volatility.
- **Evaluation design:** Nested or forward validation with few candidate indicators, crisis holdouts, multiple-testing accounting, and separate prediction of return, volatility, and drawdown.
- **Major failure modes:** Rare crises, threshold mining, contemporaneous rather than leading information, strategy-specific sign reversal, revised data, and inability of financial indicators to anticipate nonfinancial shocks.
- **Continue only if:** The relationship is available before the trade, repeats out of sample, and improves net risk-adjusted outcomes after search penalties. The source's opposite VIX associations require pair-specific conclusions.

## Frontier / high-complexity directions

- **Execution-grade microstructure research:** Reconstruct queues and cancellations to distinguish forecastable order pressure from fills actually attainable at a trader's latency and priority. This requires detailed data, costly simulation, and continual adaptation. Deliberately deceptive flipping and stop-triggering mechanics present operational and conduct hazards; this inventory does not nominate them for implementation.
- **Joint tail, leverage, liquidity, and path-risk model:** Combine non-Gaussian return generation, serial dependence, cross-strategy covariance, leverage constraints, gaps, closures, and liquidity-dependent execution. **Classifier inference:** this would test where mathematically attractive leverage or CPPI paths fail under realistic market access. The chapters provide components but do not establish a validated joint model.

## Strategic capabilities

- Point-in-time event store with normalized time zones, explicit pre-trade availability, and event-type provenance.
- Intraday market-data pipeline with stable session definitions; for microstructure work, sequenced depth, trades, cancellations, and queue reconstruction.
- Execution and cost simulator covering spreads, fees, slippage, partial fills, queue priority, latency, auctions, gaps, and liquidity failures.
- Portfolio risk engine supporting constant gross leverage, covariance-aware constrained allocation, average-log-growth optimization, fractional sizing, and broker/margin limits.
- Pathwise stress framework comparing historical and simulated sequences, serial-loss scenarios, tail shocks, closures, CPPI, and stop behavior.
- Reproducible walk-forward and sensitivity-testing framework that preserves negative results and separates forecast, sizing, execution, and protection layers.

## Source-specific material

- FSTX opening-gap and VIX examples; GBPUSD's stated 5:00 p.m. ET close and 5:00 a.m. ET London open; and the reported sample periods/results are literal source-era examples, not portable market facts.
- The PEAD example uses S&P 500 stocks, AMC/BMO labels, a `0.5` volatility threshold, 90-day window, and 30-position divisor. The final value is explicitly selected from the sample maximum and carries look-ahead bias.
- DRN's plus/minus 2% trigger 15 minutes before the close, and BGU/TNA leverage/NAV discussion, are named-product examples whose current mechanics are not established here.
- The pro-rata ratio trade, tick-based quote-matching mechanics, and commission-versus-spread condition depend on venue rules, tick size, priority, and source-era costs.
- The Pearson type-4 fit, 100,000 simulated returns, optimizer brackets, and cited leverage estimates are worked-example choices.
- VIX above 35, TED defined using three-month LIBOR minus three-month T-bills, and the named indicator list are source-era specifications requiring current definition and availability checks.

## Claims requiring independent validation

- Every reported APR, Sharpe ratio, growth rate, optimal leverage, drawdown, and CPPI simulation result in the extracts.
- The persistence and tradability of stop-cascade, news-diffusion, leveraged-ETF-rebalancing, bid/ask-imbalance, and order-flow effects.
- Source defaults: 90-day volatility windows, `z = 0.1`, `0.5`-standard-deviation event gaps, 30-position normalization, DRN's 2% trigger and 15-minute horizon, VIX 35, half-Kelly, and stop placement beyond maximum observed intraday drawdown.
- The Gaussian Kelly approximation, stationarity of future strategy returns, Pearson four-moment adequacy, and any assumption that simulated or historical paths represent worst-case losses.
- Instrument rules, leverage objectives, fund flows/assets, session definitions, announcement timestamps, index composition, venue priority, tick sizes, commission schedules, margin constraints, and executable opening/closing prices.
- The reported shortening of some multiday event effects to intraday; older GBPUSD macro momentum lasting at least 10 minutes; and the reported lack of significant EURUSD momentum for tested macro events.
- The causal interpretation of indicator relationships. The source reports VIX above 35 as unfavorable for FSTX gap momentum but favorable for a stock buy-on-gap strategy; neither association establishes causality or portability.
- **Not supported by this batch:** that full Kelly, half-Kelly, CPPI, stops, any risk indicator, or any intraday signal is universally optimal or sufficient protection.
- Equation 8.4 is unreadable in the supplied extraction and must not be reconstructed from this batch. Equation 8.3 also carries an OCR verification warning in the source extract.

## Broad one-sheet nominations by theme

- **Intraday continuation:** Opening-gap momentum across explicit session definitions, with mean-reversion as a directional baseline.
- **Event research:** Timestamp-safe earnings-gap drift, including the negative overnight-extension boundary.
- **Flow mechanics:** Leveraged-ETF rebalance pressure versus generic late-day momentum and investor-flow offsets.
- **Microstructure:** Cancellation-aware order-flow/quote-imbalance prediction with conservative fill simulation.
- **Growth sizing:** Robust fractional and constrained Kelly under parameter and tail uncertainty.
- **Drawdown engineering:** Fixed leverage versus CPPI versus executable stops under gaps and serial-loss paths.
- **Risk conditioning:** Strategy-specific leading indicators with rare-event and multiple-testing controls.

These are broad research inventory themes, not current priorities or recommendations.

## Source files

- [Chapter 7: Intraday Momentum Strategies](07-intraday-momentum-strategies.md)
- [Chapter 8: Risk Management](08-risk-management.md)
