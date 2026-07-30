# Neutral Classification of Chapters 4–6

## Scope and evidence convention

This classification consolidates the supplied extracts for stock/ETF mean reversion, currency/futures mean reversion, and interday momentum. It is a research inventory, not a recommendation or priority ranking. The extracts report textbook proposals and historical backtests; none is independently established here. Labels distinguish **Textbook proposal**, **Reported textbook result**, **Classifier inference**, and **Not supported by this batch**.

## Classification map

| Class | Consolidated content |
|---|---|
| Foundation | Time-series versus cross-sectional effects; stationarity and cointegration boundaries; executable exposure construction; futures spot/roll decomposition; signal, sizing, and P&L separation |
| Transferable methods | Nonoverlapping tests; rolling train/test estimation; lagged signals and positions; staggered holdings; cost/financing/carry accounting; point-in-time universes and synchronized prices |
| Concrete directions | ETF/basket and seasonal stock mean reversion; cross-sectional stock reversal; FX cross-rate mean reversion; futures calendar/intermarket spreads; time-series and cross-sectional momentum; roll-return relative value |
| Frontier | High-frequency index arbitrage; sentiment/fund-flow momentum; large point-in-time basket construction |
| Shared capabilities | Point-in-time market data, portfolio accounting, contract/quote normalization, execution simulation, borrow/margin/financing models, robust validation |

## Foundational knowledge

- **Textbook proposal:** Time-series mean reversion concerns a series reverting relative to its own history; cross-sectional mean reversion concerns members reverting toward the basket return. Tests designed for the former do not establish the latter. [Chapter 4](04-mean-reversion-of-stocks-and-etfs.md)
- **Textbook proposal:** Single-stock pairs are structurally fragile because firm-specific changes can break an estimated relationship. Diversifying many such pairs does not guarantee protection when a broken pair can dominate gains. ETF baskets and diversified component baskets reduce company-specific and stock-borrowing risk, but their relationships can also change. [Chapter 4](04-mean-reversion-of-stocks-and-etfs.md)
- **Textbook proposal:** A nonstationary daily series can exhibit mean reversion within a defined intraday season. A gap reversal therefore tests a time-window-specific liquidity-pressure hypothesis, not long-run price stationarity. [Chapter 4](04-mean-reversion-of-stocks-and-etfs.md)
- **Textbook proposal:** Currency portfolio weights are meaningful only after quote orientation and capital value are made consistent. Carry is part of total return: log cross-rate change plus base-currency interest less quote-currency interest for the applicable rollover interval. [Chapter 5](05-mean-reversion-of-currencies-and-futures.md)
- **Textbook proposal:** In the source's constant-return futures model, total return is spot return plus roll return, while curve slope identifies roll return. A same-underlying long-far/short-near equal-market-value log spread cancels spot in the model and exposes the maturity difference times roll return. The model is conditional and explicitly unsuitable for some underlyings, including VX. [Chapter 5](05-mean-reversion-of-currencies-and-futures.md)
- **Textbook proposal:** A calendar spread is not mean reverting merely because both legs share an underlying; its roll-return process must be stationary or slowly varying. Conversely, persistent roll-return sign offers an economic mechanism for futures momentum. [Chapters 5](05-mean-reversion-of-currencies-and-futures.md) and [6](06-interday-momentum-strategies.md)
- **Textbook proposal:** Time-series momentum asks whether an instrument's own past return predicts its future return; cross-sectional momentum asks whether relative winners continue to outperform relative losers. A directional signal, a cross-sectional rank, staggered capital allocation, and hedge construction are distinct design decisions. [Chapter 6](06-interday-momentum-strategies.md)
- **Textbook proposal:** Gross statistical opportunity and net executable return are different objects. Borrow availability, recalls, bid/offer depth, primary versus consolidated prices, closing-time mismatch, margin, leverage, financing, carry, and contract settlement can determine whether a historical signal is realizable. [Chapters 4–6](04-mean-reversion-of-stocks-and-etfs.md)

## Transferable research methods

- Use rolling or explicitly separated training and test periods for eigenvectors, hedge ratios, half-lives, thresholds, and horizon selection. Treat a parameter search followed by evaluation on the same observations as data-snooping exposure.
- When testing look-back return against holding-period return, subsample so the paired observations do not overlap: advance by the larger horizon. Report effect size and uncertainty, not only the best correlation or p-value.
- Lag every input that would not have been known at decision time. Distinguish official prices used to describe a signal from prices actually available for entry; the official open cannot both reveal a gap and be the guaranteed fill.
- Separate signal validation from portfolio construction. Examples include normalized dollar-neutral deviation weights for cross-sectional reversal, common-quote currency capital weights, contract-multiplier-adjusted intermarket hedges, and daily staggered momentum tranches.
- Evaluate executable total return after spread, commissions, financing, borrow, rollover interest, roll/settlement handling, and local-currency conversion. Preserve both gross and net results so signal failure can be distinguished from implementation failure.
- Use point-in-time membership and complete delisted histories for stock-universe tests. Synchronize timestamps and market closes before fitting intermarket relationships.
- For futures, inspect whether log prices are approximately linear across the selected maturities before applying the source's spot/roll model. Test the stationarity and half-life of estimated roll return rather than assuming it.
- Use meaningful nulls and ablations: unfiltered gaps; random or zero exposure; lagged total-return versus roll-return signals; equal-weight or unhedged portfolios; fixed versus rolling hedge ratios; price-only versus carry-inclusive FX returns; and pre-cost versus net results.
- Stress structural breaks, forced deleveraging, short-covering, crowding, changing correlations, and rare broken relationships. Average Sharpe alone does not characterize the tail shape or long losing stretches.

## Concrete research directions

### 1. Diversified ETF or component-basket mean reversion

- **Textbook basis:** ETF pairs/triplets are proposed as more robust than single-stock pairs; a worked workflow screens SPY components, forms an equal-capital log-price basket, estimates cointegration with SPY, and trades the spread. [Chapter 4](04-mean-reversion-of-stocks-and-etfs.md)
- **Core hypothesis/question:** Does stable shared exposure produce an out-of-sample stationary spread after realistic rebalancing and trading costs?
- **Applicable markets:** Closely related ETFs; an ETF versus a selected subset of its constituent stocks.
- **Required data:** Point-in-time constituents, adjusted component and ETF prices, synchronized executable quotes, corporate actions, costs, and rebalance records.
- **Candidate methods/rules:** Rolling cointegration screen and hedge estimation; equal-capital daily-rebalanced log basket; source example uses 2007 training, 98 retained stocks, and a five-day lookback as source defaults.
- **Meaningful baselines:** Single-stock pairs; ETF-only pairs; full index replication; fixed hedge ratio; no-trade spread.
- **Evaluation design:** Freeze selection and hedge weights before each test window; compare relationship survival, gross/net P&L, turnover, constituent churn, and sensitivity to stale or consolidated prices.
- **Major failure modes:** Selection and survivorship bias, unstable shared exposure, multiple testing, corporate events, asynchronous prices, and basket execution costs.
- **Continue only if:** Stationarity and net returns persist across genuinely held-out periods and membership regimes without dependence on a few relationships; otherwise narrow to more structurally linked baskets or reject.

### 2. Intraday stock gap reversal

- **Textbook basis:** Buy stocks opening below prior low by one lagged 90-day volatility unit, require price above a lagged 20-day moving average, rank gaps, buy up to ten, and exit at the close. A mirror short rule is also reported. [Chapter 4](04-mean-reversion-of-stocks-and-etfs.md)
- **Core hypothesis/question:** Are extreme openings without evidence of adverse longer-term information temporary liquidity/panic pressure that reverses intraday?
- **Applicable markets:** Liquid equities in a point-in-time large-cap universe; long and short variants must be evaluated separately.
- **Required data:** Historical membership, primary-market auction/quote data, open/low/close histories, pre-open indications if used, borrow availability, uptick restrictions, fees, and spread/slippage.
- **Candidate methods/rules:** Source defaults above; test filter, threshold, rank, capacity, and executable entry variants without treating them as constants.
- **Meaningful baselines:** Unfiltered gap reversal; random qualifying stocks; market-adjusted intraday return; no ranking; long-only versus short-only.
- **Evaluation design:** Generate decisions only from available pre-entry information; simulate auction or post-open fills; segment suspected news days; report fill rate, capacity, turnover, and net P&L.
- **Major failure modes:** Official-open leakage, adverse-news selection, survivorship bias, NBBO depth, short recalls/constraints, and omitted costs. **Reported textbook result:** The long result reportedly decayed after 2009; the higher-return short result had steeper drawdowns and tighter implementation constraints.
- **Continue only if:** The effect survives point-in-time, executable, net testing and is not concentrated in unfillable opens or adverse-news events; otherwise narrow the window/filter or reject.

### 3. Cross-sectional stock reversal

- **Textbook basis:** Opposite-sign deviations from the equal-weight universe return are normalized to unit gross exposure; variants use prior close-to-close or overnight returns and earn next-day or intraday returns. [Chapter 4](04-mean-reversion-of-stocks-and-etfs.md)
- **Core hypothesis/question:** Do relative winners and losers reverse over the next specified horizon after common movement is removed?
- **Applicable markets:** Broad liquid equity baskets.
- **Required data:** Point-in-time universe, adjusted daily and intraday prices, executable close/open data, borrow and cost data.
- **Candidate methods/rules:** Portable weight rule: negative demeaned return divided by the sum of absolute demeaned returns; apply returns to lagged weights. Compare close-to-close and overnight-to-intraday specifications.
- **Meaningful baselines:** Equal-weight market-neutral portfolio; rank-based reversal; raw versus market-adjusted returns; no overnight variable.
- **Evaluation design:** Walk forward with lagged weights, sector/exposure diagnostics, capacity and turnover analysis, and separate signal from auction execution.
- **Major failure modes:** Universe bias, hidden common exposures, crowding, close/open non-executability, short constraints, and transaction-cost dominance.
- **Continue only if:** Net relative reversal is stable across universes and periods after exposure and execution controls; reject variants whose edge disappears under lagged executable pricing.

### 4. Carry-aware currency cross-rate mean reversion

- **Textbook basis:** The source constructs candidate relationships in a common USD quote, estimates Johansen weights, converts signals to executable quote orientations, and includes base-minus-quote rollover interest. [Chapter 5](05-mean-reversion-of-currencies-and-futures.md)
- **Core hypothesis/question:** Does a properly valued currency relationship revert after carry and conversion are included?
- **Applicable markets:** Currency crosses with a plausible shared economic exposure, including synthetic crosses.
- **Required data:** Synchronized bid/ask quotes, quote conventions, point-in-time interest/rollover schedules, weekday treatment, conversion rates, and leverage/margin terms.
- **Candidate methods/rules:** Rolling Johansen estimate using common quote currency; log-return mean-reversion signal; carry-inclusive P&L. The source's 250-day initial training and weekday triple-roll convention are defaults requiring venue-specific validation.
- **Meaningful baselines:** Price-only P&L; no-cointegration carry trade; fixed versus rolling weights; directly quoted versus synthetic execution.
- **Evaluation design:** Lock estimates before each test period and reconcile every leg in investor-local currency; attribute return to price, carry, conversion, and costs.
- **Major failure modes:** Incorrect base/quote inversion, mismatched capital units, stale interest conventions, synthetic-leg slippage, multi-currency P&L, leverage, and relationship breakdown.
- **Continue only if:** The relationship and net local-currency return survive correct quote, carry, and execution accounting out of sample; otherwise reject the apparent statistical spread.

### 5. Futures calendar-spread roll-return mean reversion

- **Textbook basis:** Estimate curve slope/roll return from several consecutive maturities, estimate its half-life, form a fixed-maturity-distance far/near spread, avoid expiry windows, and trade against roll-return Z-score. The CL example uses contracts 12 months apart and a reported roughly 36-day half-life. [Chapter 5](05-mean-reversion-of-currencies-and-futures.md)
- **Core hypothesis/question:** Is roll return for a chosen underlying sufficiently stationary and tradable for calendar-spread mean reversion?
- **Applicable markets:** Same-underlying futures whose term structure approximately fits the source model.
- **Required data:** Point-in-time full curves, contract specifications/multipliers, expiry calendars, synchronized prices, rolls, margins, and spread execution costs.
- **Candidate methods/rules:** Cross-maturity log-price regression for annualized roll return; lagged autoregression for half-life; Z-score reversal with expiry avoidance. All maturity gaps and lookbacks are test parameters.
- **Meaningful baselines:** Naive near/far spread; fixed calendar-spread hold; total-return mean reversion; alternative maturity gaps.
- **Evaluation design:** Validate curve linearity and roll-return stationarity first; then walk forward through multiple curve regimes with explicit contract rolls and net P&L.
- **Major failure modes:** Nonlinear or nonstandard curve, unstable half-life, expiry contamination, liquidity migration, multiplier errors, and regime change. **Negative boundary:** Calendar spreads without stationary roll return are not supported as mean-reversion candidates.
- **Continue only if:** The roll process remains sufficiently stable and net spread returns generalize across roll cycles and regimes; otherwise narrow to another maturity region or reject.

### 6. Related-futures intermarket mean reversion

- **Textbook basis:** The source discusses multiplier-aware crack-spread and fitted ES–VX relationships while warning about timestamp and regime dependence. [Chapter 5](05-mean-reversion-of-currencies-and-futures.md)
- **Core hypothesis/question:** Does a structurally related, contract-value-normalized portfolio remain stationary out of sample?
- **Applicable markets:** Related commodity transformations and equity/volatility futures.
- **Required data:** Synchronized contract prices, multipliers, maturity mappings, settlement rules, and executable spreads.
- **Candidate methods/rules:** Economically specified ratios such as the source's 3:2:1 crack spread; rolling or frozen fitted hedge relationships. Preserve the printed ES–VX relation and duplicated equation number as a source inconsistency, not a corrected formula.
- **Meaningful baselines:** Economic fixed ratio versus fitted ratio; unsynchronized versus synchronized closes; constituent calendar spreads.
- **Evaluation design:** Estimate only in training windows, test relationship survival by regime, and attribute errors to fit versus execution.
- **Major failure modes:** Spurious or changing linkage, mismatched maturities/closes, contract-size errors, and a hedge fit that does not transfer.
- **Continue only if:** Stationarity and net performance survive held-out regimes and synchronization choices; reject relationships dependent on one fitted era.

### 7. Time-series momentum with price or roll-return signals

- **Textbook basis:** Test nonoverlapping past/future returns, then trade the sign of an L-day price change through H staggered daily tranches. The source also proposes persistent roll-return sign as a cleaner futures signal than total return. [Chapter 6](06-interday-momentum-strategies.md)
- **Core hypothesis/question:** Does past direction—or lagged curve slope—predict future return out of sample for a given instrument?
- **Applicable markets:** Futures, especially where a persistent term structure supplies a mechanism.
- **Required data:** Continuous and individual-contract histories, complete curves for roll signals, executable prices, rolls, multipliers, margin, and costs.
- **Candidate methods/rules:** Correlation/p-value grid with independent pairs; sign rule; daily 1/H allocation held H days; positive/negative roll thresholds. TU 250/25 and other reported horizons are source-selected defaults, not constants.
- **Meaningful baselines:** Zero or random sign; simple lagged total return; roll-only signal; buy-and-hold; volatility-unscaled versus comparable exposure.
- **Evaluation design:** Separate horizon selection from evaluation, count independent observations, walk forward across instruments/regimes, and stress leverage and crash periods.
- **Major failure modes:** Few independent long-horizon samples, multiple testing, leverage, contract stitching, crowding, regime decay, long losing stretches, and sharp reversal/momentum crash.
- **Continue only if:** Predictive effect and net strategy return persist on untouched data with acceptable reversal tails; otherwise narrow horizons/instruments or reject.

### 8. Roll-return relative value and cross-sectional momentum

- **Textbook basis:** The source proposes future-versus-underlying/proxy positions conditioned on contango or backwardation, a one-day VX–ES rule, and ranking futures or stocks into staggered long-winner/short-loser baskets. [Chapter 6](06-interday-momentum-strategies.md)
- **Core hypothesis/question:** Can persistent roll return or relative performance be isolated from common spot/factor movement and monetized after financing?
- **Applicable markets:** Futures with underlyings or ETF proxies; volatility/equity futures; broad commodity or equity universes.
- **Required data:** Full term structures, spot/proxy/ETF prices, synchronized closes, financing and borrow, multipliers, factor/residual returns for equities, and universe histories.
- **Candidate methods/rules:** Long backwardation/short contango; future-versus-proxy hedge; source VX threshold of 0.1 point times days to settlement and multiplier-aware hedge; 252-day ranks, top/bottom baskets, and 25 staggered holdings as source defaults.
- **Meaningful baselines:** Unhedged futures momentum; price rank versus roll rank; equal-weight long/short; no-financing gross result; fixed versus rolling hedge ratio.
- **Evaluation design:** Attribute spot, roll, financing, basis, and hedge P&L separately; use held-out periods and multiple regimes; verify that long/short common exposures actually cancel.
- **Major failure modes:** Proxy basis, financing offset, close-time mismatch, settlement timing, unstable hedge ratio, crowded ranks, short constraints, and crash reversals. **Reported textbook result / negative finding:** The apparent GLD–GC gross opportunity was largely offset by GLD financing; the stock cross-sectional result covered only a short interval.
- **Continue only if:** Net return remains after financing and basis risk, and is not merely unhedged spot/factor exposure or a short-sample artifact; otherwise narrow to directly hedgeable markets or reject.

## Frontier / high-complexity directions

- **High-frequency index arbitrage — Textbook proposal:** Exploit lag between primary-only index calculations and component prices. It requires direct feeds, millisecond monitoring, basket execution, and realistic queue/latency modelling. **Classifier inference:** This is operationally distinct from the daily ETF/component direction and should be evaluated as execution research, not inferred from daily backtests. [Chapter 4](04-mean-reversion-of-stocks-and-etfs.md)
- **Information- and flow-conditioned equity momentum — Textbook proposal:** Use news sentiment or institutional purchase pressure as factors for residual cross-sectional momentum. The batch gives candidate mechanisms but no complete data specification or validated model. [Chapter 6](06-interday-momentum-strategies.md)
- **Large point-in-time constituent or multi-market baskets — Classifier inference:** Robustly reproducing the proposed basket effects requires historical membership, delistings, corporate actions, borrow, synchronized venues, and capacity-aware execution at scale; the extracts do not demonstrate that full stack.

## Strategic capabilities

- Point-in-time equity universes, corporate actions, delistings, and historical constituent membership.
- Primary-auction, consolidated, intraday quote, and synchronized multi-market data with explicit availability timestamps.
- Currency quote normalization, synthetic-cross execution, carry schedules, and local-currency P&L reconciliation.
- Futures curve reconstruction, maturity mapping, multiplier normalization, expiry avoidance, roll accounting, and settlement calendars.
- Portfolio engine separating signals, hedge/size rules, lagged positions, staggered vintages, gross exposure, and return attribution.
- Realistic cost and feasibility models covering bid/ask, slippage, depth, borrow/recalls, short-sale rules, financing, margin, and leverage.
- Walk-forward research controls for multiple testing, independent observations, parameter stability, structural breaks, and tail/crowding scenarios.

## Source-specific material

- S&P 500/SPY constituent examples, the 2007 training split, 98 selected stocks, and five-day lookback are worked-example choices, not portable constants.
- The buy-on-gap defaults—90-day volatility, one-standard-deviation threshold, 20-day moving average, and maximum ten positions—and its 2006–2012 reported results are source-era specifications.
- AUD.USD/CAD.USD and AUD.CAD examples, 250-day training, and weekday triple rollover require current venue/instrument confirmation.
- CL five-contract slope regression, 12-month spread, roughly 36-day reported half-life, and the 2008–2012 historical result are source-specific.
- The 3:2:1 crack spread, ES multiplier 50, VX multiplier 1,000, fitted coefficient -0.3906, intercept $77,150, and VX threshold rule are instrument- and era-specific. The source duplicates Equation 5.11; this classification does not silently renumber it.
- TU 250/25, the reported BR/HG/TU horizon choices and results, the 52-market universe description, stock top/bottom 50 rule, 252-day lookback, and 25-day holding are source examples.
- GLD–GC, XLE–USO, S&P DTI, and the cited historical figures/web resources are illustrative artifacts, not evidence of current accessibility or efficacy.

## Claims requiring independent validation

- Every reported APR, Sharpe ratio, drawdown, correlation, p-value, half-life, equity curve, and claimed decay or regime behavior.
- Stability of ETF, component-basket, currency, calendar-spread, crack-spread, and ES–VX relationships outside their estimation eras.
- The causal stories that gaps reflect liquidity pressure, roll-sign persistence drives momentum, information diffuses slowly, fund flows force continuation, or high-frequency traders create momentum.
- All fixed horizons, Z-scores, thresholds, ranks, basket sizes, hedge ratios, factor choices, and curve-linearization assumptions.
- Current index membership histories, exchange/auction behavior, NBBO capacity, borrow/recall availability, alternative-uptick restrictions, margins, financing rates, rollover conventions, contract specifications, multipliers, and settlement rules.
- Whether primary/consolidated prices and cross-market closing times correspond to executable decisions and fills.
- **Not supported by this batch:** Any claim that the historically strongest variant will remain strongest; that stock-pair cointegration, calendar spreads, or related futures are generically stationary; that financing-free roll arbitrage exists; that diversification prevents momentum crashes or broken-pair losses; or that any reported pre-cost result is live-tradable.

## Broad one-sheet nominations by theme

- **Seasonal liquidity reversal:** Gap-reversal mechanism, information filter, auction execution, borrow/capacity, and point-in-time validation.
- **Diversified statistical spreads:** ETF/component basket construction, relationship survival, hedge estimation, and break detection.
- **Cross-sectional equity effects:** Relative reversal versus momentum, overnight/intraday decomposition, exposure controls, and implementation costs.
- **Currency relative value:** Quote orientation, common-value weights, carry-inclusive returns, synthetic execution, and conversion risk.
- **Futures term structure:** Spot/roll decomposition, curve diagnostics, calendar-spread mean reversion, and roll-sign momentum.
- **Intermarket relative value:** Economic versus fitted hedge ratios, synchronization, contract normalization, and regime dependence.
- **Momentum evidence and tails:** Independent horizon tests, staggered positions, multiple-testing controls, crowding, and crash behavior.
- **Execution frontier:** Primary-index latency, direct feeds, basket execution, and millisecond-level feasibility.

## Source files

- [Chapter 4 — Mean Reversion of Stocks and ETFs](04-mean-reversion-of-stocks-and-etfs.md)
- [Chapter 5 — Mean Reversion of Currencies and Futures](05-mean-reversion-of-currencies-and-futures.md)
- [Chapter 6 — Interday Momentum Strategies](06-interday-momentum-strategies.md)
