# Neutral Classification of Chapters 31–37

## Scope and evidence convention

This batch covers deployability: expiry choice and rolling, execution, cash/compounding, portfolio risk overlays, calculation conventions, external resources and the author's instrument universe. It contributes operational foundations and controls rather than new alpha directions.

## Foundational knowledge

- A futures instrument is a chain of dated contracts. Expiry selection, roll timing and roll execution are one lifecycle decision governed first by liquidity and delivery constraints.
- Front contracts can be liquid but introduce delivery, settlement, jump, carry-measurement and frequent-roll risks. Further expiries can reduce some of those risks while adding others.
- Expected trading cost should combine regularly sampled spreads, submission-time conditions and realized mid-to-fill outcomes. Market impact and participation matter when size is material.
- Passive execution exchanges lower average spread cost for uncertain completion and negatively skewed adverse-move risk.
- Free cash supports variation margin; initial margin is not a rational position-sizing budget. Fully capitalized notional risk and broker margin usage are different concepts.
- Fixed-capital live trading eventually creates inconsistent risk. Full compounding keeps target risk proportional to equity; high-watermark/partial compounding supports withdrawals while limiting risk growth.
- A risk overlay must only reduce base-strategy positions. Each control needs a measurement, trigger, action and reversal condition defined before stress.
- Back-adjustment, volatility, correlation, covariance, turnover, FDM and IDM conventions are parts of the strategy specification and can materially change results.

## Transferable research and implementation methods

1. **Contract-chain realism:** apply point-in-time liquidity screens, first-notice/delivery constraints, expiry-specific volatility and simultaneous roll mechanics in both backtest and live logic.
2. **Execution measurement loop:** record sampled half-spread, order-time spread, size, midprice, actual fill and latency; compare expected with realized cost by instrument and time.
3. **Bounded passive-to-aggressive execution:** predefine switching conditions based on adverse movement, book imbalance or timeout; evaluate completion and tail cost, not average spread alone.
4. **Capital-policy simulation:** distinguish fixed, full and high-watermark compounding; model withdrawals, FX margin funding, cash yield, margin calls and liquidation.
5. **Downside-only risk overlay:** take the minimum multiplier across portfolio-risk, jump-risk, correlation-shock and leverage controls, with hard position/trade limits outside the model.
6. **Calculation-contract tests:** keep reference examples for roll adjustment, EWMA risk, covariance, turnover and diversification multipliers; test negative prices, missing contracts and warm-up.

## Concrete research directions

### 1. Expiry and roll-policy comparison

- **Core hypothesis/question:** Can a liquidity-first expiry/roll policy reduce cost and lifecycle risk without degrading signal exposure?
- **Required data:** dated-contract quotes/volume/open interest, expiry/FND/settlement, spread combinations, multipliers and signal state.
- **Baselines:** fixed front-month roll; five-days-before-expiry; liquidity-triggered roll; passive roll through ordinary turnover.
- **Evaluation design:** executable rolls, missed/partial fills, delivery exclusions, expiry-specific volatility and signal discontinuity.
- **Continue only if:** benefits persist across instruments and do not depend on source-era thresholds or impossible hindsight liquidity.

### 2. Execution-policy benchmark

- **Core hypothesis/question:** Does passive-first execution lower implementation shortfall without unacceptable non-fill or adverse-move tails?
- **Baselines:** immediate market, fixed passive timeout, participation schedule and simple urgency rules.
- **Evaluation design:** order-level replay and forward shadow logs; stratify by size, liquidity, time and signal urgency.
- **Continue only if:** total cost distribution and completion reliability improve, not merely average quoted spread.

### 3. Exogenous portfolio-risk overlay

- **Core hypothesis/question:** Do downside-only multipliers reduce catastrophic/margin outcomes without erasing the strategy's convexity or creating procyclical liquidation?
- **Baselines:** base strategy; margin-only control; leverage cap; each multiplier separately.
- **Evaluation design:** historical and synthetic volatility/correlation jumps, liquidity stress, trigger/reversal hysteresis and tracking error.
- **Continue only if:** severe loss/margin risk falls across varied shocks while normal-regime drag remains bounded.

## Strategic capabilities

- Futures security master with expiry, FND, settlement, multiplier, currency, venue and broker mapping.
- Contract-chain/liquidity store and combination-order execution support.
- Order-level transaction-cost analytics and immutable fill records.
- Cash, margin, FX, compounding and withdrawal ledger.
- Independent pre-trade position/trade limits and portfolio risk overlay.
- Shared, versioned quantitative calculation library with reference fixtures.

## Source-specific material

The author's broker codes, 102-instrument Jumbo list, first-data years, exchange selections, website links, broker/vendor list, VIX examples, fixed thresholds and personal cash practices are references, not current specifications. Appendix A is a source-discovery list; Appendix C is an author-specific universe snapshot.

## Claims requiring independent validation

- Liquidity and USD-risk-volume thresholds, timing windows, book-imbalance trigger, five-minute timeout, margin percentages and risk-overlay percentiles.
- Current contract specifications, delivery rules, broker margin, exchange codes, data availability, commissions and website/vendor status.
- Reported cost reduction and risk-overlay performance.
- FDM/IDM lookup values and all statistical-estimation choices in Appendix B.

## Source files

`chapters/31-contract-selection-and-rolling.md` through `chapters/37-jumbo-portfolio.md`.
