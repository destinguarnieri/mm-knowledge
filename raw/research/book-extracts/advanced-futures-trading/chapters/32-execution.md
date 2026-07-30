# Tactic Two: Execution

## Purpose and central argument

This chapter addresses the second of the author's two ways to improve trading results: **pay less in trading costs**. Earlier parts of the book focused chiefly on making more money before costs, while also constraining turnover with a trading-frequency “speed limit,” forecast smoothing, and position buffering. Here the author treats the cost of an individual trade as something that can be measured and reduced through smarter execution.

The baseline assumption is a market order filled at the best bid or ask: for a small order, this produces a spread cost of half the bid–ask spread, plus brokerage commissions. The chapter argues that costs can be reduced by measuring them well, avoiding thin-liquidity periods, adapting order size/frequency for large participation, and selectively using execution algorithms or, for fast directional strategies, pre-positioned limit-order ladders.

> The source frames the overall principle as: make more money before costs; pay less in trading costs.

## Core concepts and definitions

| Term | Meaning in this chapter |
|---|---|
| Bid–ask spread | Difference between the best bid and best ask. For a small market order, expected spread cost is half this difference, measured from the mid price to the bid or ask. |
| Mid price | The midpoint of bid and ask; the reference for measuring expected and realized fill costs. |
| Spread cost | Cost associated with executing away from the mid price. A small market order is assumed to incur half the quoted spread. |
| Market order | Order intended to execute immediately. For small orders its cost is known (half-spread); it almost always executes, but always pays the half-spread. |
| Limit order | Order constrained to a stated price. It may be cheaper than a market order—filling at best bid when buying or best offer when selling gives a negative spread cost—but both cost and execution time are uncertain. |
| Passive execution | In the author’s algorithm, initially place a buy limit at the current best bid or a sell limit at the current best ask, hoping for a favorable fill. |
| Aggressive execution | In the author’s algorithm, place/update the limit at current best offer for a buy or current best bid for a sell, seeking prompt execution while paying the spread. |
| Execution algorithm / algo | A process that chooses between passive and aggressive execution. It can be self-built, supplied by brokers/banks/third parties, or substituted by a human execution trader. |
| Permanent price impact | Price movement caused by the trader’s sustained participation; e.g., repeated one-lot buys can push price above where it would otherwise have been. |
| Level two data | Order-book data beyond the best bid/offer, suggested as a proxy for estimating costs of larger orders. |
| Ladder | Series of orders left in the order book at different prices. For the mean-reversion case here: sell limits above current price and buy limits below it. |

## Measuring and modelling costs

### Three data sources

1. **Regularly sampled spreads** throughout the day, including instruments not currently traded. Expected cost = half the sampled spread (mid-to-bid or mid-to-ask).
2. **Spread at order submission**: half the spread present when the order is sent, along with order size.
3. **Actual fill spread**: difference between the mid price and actual execution price, along with order size.

Sources 1 and 2 are broadly comparable, but submitted orders may be concentrated at the author’s habitual execution times. Regular sampling is not subject to that timing bias. Source 3 is more realistic for large funds that cannot always trade at the top of the book.

### How the measurements are used

- For an untraded instrument, sampled spreads estimate risk-adjusted cost, whether the instrument is cheap enough to trade, and which rule variants satisfy the speed limit.
- For a traded instrument, the expected spread is an ongoing composite: **average sampled spread from source 1 plus the higher of the expected and realized trade-time figures from sources 2 and 3**. The higher trade-time value is used because an execution algorithm can sometimes improve on the quoted bid–ask spread.
- The source notes that expected trading cost is also a direct input to the author’s version of strategy twenty-five, dynamic optimisation.
- Comparing source 2 with source 3 measures execution-algorithm efficacy.
- Actual fill spreads can reveal effects of trade size and frequency; this is especially important for institutional traders.
- Cost by hour and weekday can identify relatively cheap or expensive trading periods.
- If a long enough own trading history exists, actual spreads and commissions could be used in backtests rather than historical extrapolation of current costs.

### Quantitative relationships and notation

The chapter gives no generalized algebraic model or formal derivation. Its stated relationships are:

| Relationship | Variables / conditions |
|---|---|
| Expected spread cost for a small market order = half the bid–ask spread | Spread is best ask minus best bid; equivalently mid-to-ask for a buy or mid-to-bid for a sell. Applies to small orders assumed to execute at the top of book. |
| Expected traded-instrument spread = mean(source 1) + max(source 2, source 3) | Source 1 = sampled half-spread; source 2 = half-spread at order; source 3 = actual mid-to-fill difference. This is the author’s operational modelling rule. |
| Participation rate = contracts to trade / daily volume | Example: 1,000 VIX contracts in 24 hours is described as roughly 1.5% of daily volume. |
| Order interval = trading-day seconds / number of orders | Example: approximately 28,000 seconds in an eight-hour day; 1,000 one-contract orders imply one every 28 seconds. |

**Units/domains:** prices and spreads are in an instrument’s price units/ticks; order size is contracts; time is seconds/minutes/hours; participation is a percentage of daily volume; reported costs are percentages of capital. The half-spread assumption is explicitly not reliable for a large order or meaningful share of daily volume.

## When to trade: liquidity and timing

Liquidity and costs vary over time. The author does not claim that fine timing optimization will greatly lower costs, but says it can prevent obvious mistakes in predictably thin markets.

- In US equities, open and close are active. In many futures markets, however, open and close can be thin and wide; wait about 30 minutes after opening and stop about 30 minutes before close.
- Around-the-clock futures still have liquidity cycles. A US future is generally less liquid overnight than in its daytime session.
- Avoid shortly before or after major economic releases (examples: nonfarm payrolls and crop reports) and release of election results: liquidity may be thin and price moves sharp.
- During exchange-open holiday periods, consider lower maximum order sizes rather than stopping the strategy entirely. US holidays can reduce liquidity in other open markets; product-specific holidays matter too (a Japanese holiday can reduce JPY/USD FX-futures trading).
- Large institutions should avoid a fixed daily execution time, because quicker traders can recognize the pattern and front-run it.

### Figure 95 — sampled Eurodollar spreads by hour

**Caption/source:** “90% percentile of sampled bid-ask spread for Eurodollar futures by hour of day (UTC time zone).” The plotted bars cover UTC hours 0, 6, 8–17. The chart shows the largest displayed 90th-percentile spreads at 0 UTC (about 0.0093) and 6/9 UTC (about 0.0088–0.0090), with lower values around 10 and 14 UTC (about 0.0050). It supports the text’s warning that overnight trading has higher spreads. The y-axis unit is not labeled in the supplied figure, so its exact price-unit interpretation is **unclear from the source**.

## How often to trade and how large

For large institutional orders, neither extreme is attractive: one contract every 28 seconds nor a single 1,000-contract order. The chapter uses buying 1,000 VIX contracts within 24 hours—roughly 1.5% of daily volume—as an example. It offers intermediate illustrative schedules: 10 contracts every 280 seconds or 100 every 2,800 seconds (about 45 minutes), but does not claim an optimum.

A single 1,000-contract market buy cannot be assumed to pay half the spread; at the time of writing, only 100 VIX contracts were available at the best ask. Conversely, even one-lot trades totaling 1.5% of daily volume may cost more than half-spread, because persistent buying can create permanent impact.

Once costs depend on order size and participation, the following choices must be made jointly rather than independently:

- Which instruments are cheap enough and liquid enough to trade.
- Which trading-rule variations can be used.
- What instrument weight to allocate.

Higher instrument weight increases volume participation and may require removing higher-turnover rules. The recommended empirical target is a function estimating expected bid–ask spread for a specified trade size and fraction of daily volume. Experimenting with actual order sizes supplies the data; level-two order-book data may be used as an estimate if large live experiments are too costly.

**Warning:** do not extrapolate costs to sizes larger than those actually traded. Once participation becomes significant, costs may rise nonlinearly and unpredictably.

## Execution algorithms

### Order-type trade-off

| Order type | Advantages | Disadvantages |
|---|---|---|
| Market order | Known small-order cost (half-spread); almost always executes. | Always pays half the bid–ask spread. |
| Limit order | May be cheaper; a buy filled at best bid or a sell filled at best offer is effectively paid to trade (negative spread cost). | Cost and execution time unknown; if price moves away before fill, may be much costlier than a market order. |

Basic algos switch between passive limit orders and aggressive, market-like execution. More complex algorithms may condition the decision on many factors.

### Routes to market and evaluation

The available routes are: build an algo; use broker, bank, or third-party algos (Quantitative Brokers is named); use a human execution trader; or use multiple routes. The author suggests random allocation of orders across routes to create natural experiments, then comparing costs. With sufficient data, this can yield conditional rules such as which algo has the greatest chance of best fill for a specified instrument, order size, and time window.

### Author’s simple execution algorithm

**Initial passive order**

- Buy: set limit price to current best bid.
- Sell: set limit price to current best ask.

**Switch to aggressive execution when any one of these occurs:**

1. **Adverse price move:** mid rises while buying, or mid falls while selling.
2. **Order-book size imbalance:** for a buy, bid-side size exceeds ask-side size by more than 5×, interpreted as buying pressure likely to cause an imminent adverse move. (The source only explicitly specifies the buy-side case.)
3. **Timeout:** more than five minutes since initial order placement.

**Aggressive mode:** set limit to best offer when buying or best bid when selling, and remain aggressive until filled.

If an imbalance/timeout is detected and acted on quickly, the fill should be at the same price as an initial market order: no cost benefit or penalty. If reaction is late, or price has already moved adversely, the trader chases price and can do worse than an initial market order.

### Worked execution example

Assume an imaginary market with tick size **0.01** and initial inside spread **100.01 bid / 100.02 ask**.

1. A market buy would pay **100.02**.
2. The algorithm instead submits a passive buy limit at **100.01**.
3. A book imbalance appears, so it switches to aggressive mode and raises the buy limit to the then-best offer, **100.02**.
4. Before fill, the inside spread moves to **100.02 / 100.03**. The aggressive algorithm updates its buy limit to **100.03**.
5. Best case: fill at 100.03, one tick worse than the original market buy. Worse cases: the price continues away faster than orders can be updated, or gaps upward multiple ticks before fill.

The resulting payoff profile is described as **negatively skewed**: frequent steady gains when passive fills are paid to trade, offset by occasional large losses when passive mode fails and fill price becomes much worse.

### Figure 96 — author’s empirical result

**Caption/source:** cumulative costs as a percentage of capital for the author’s trading system, September 2020–April 2022; x-axis = internal order ID. The figure has three plotted series:

- Light gray: cumulative hypothetical bid–ask spread cost if market orders had always been used.
- Dark gray: total actual incurred spread cost.
- Black: cumulative algo cost/profit (the saving attributable to the algo).

Over the roughly 20-month sample, the market-order benchmark cost is stated as just over **3.6%** of capital, actual spread cost around **3.0%**, and the difference/algo contribution around **0.6%** of capital. The author summarizes this as reducing costs by around one sixth. The visible chart lines corroborate this direction; exact chart readings beyond the stated figures should not be inferred.

## Special case: fast directional strategies — limit-order ladders

The author says the preceding execution algo cannot be used for fast directional strategies in Part Four because those strategies mostly use limit orders. A modification of the previously described strategy-twenty-six process is to preserve old unfilled limits and add new ones, creating a ladder rather than continually modifying an existing order.

### Starting state

| Item | Price and action |
|---|---|
| Sell limit | 133.046875 — sell 1, moving to short 13 contracts |
| Current price and position | 133.00 — short 12 |
| Buy limit | 132.96875 — buy 1, moving to short 11 |

The price then rises to 133.078125, filling the sell order and leaving the position short 13. The implied next sell for position −14 is 133.09375; the corresponding buy for position −12 is 133.015625.

### Two approaches after the fill

**Original approach:** modify the outstanding buy limit from 132.96875 to 133.015625, while adding the sell at 133.09375.

**Ladder approach:** leave the original buy at 132.96875 and add a new buy at 133.015625, while adding the sell at 133.09375. The resulting orders cover positions/levels on both sides:

| Order | Price | Intended position after fill |
|---|---:|---:|
| New sell | 133.09375 | short 14 |
| New buy | 133.015625 | short 12 |
| Existing buy | 132.96875 | short 11 |

If price then trades down to 133.00, filling the new buy and returning to short 12, the original buy remains in place. Add a new sell at 133.046875 for short 13; keep the sell at 133.09375 for short 14 and the existing buy at 132.96875 for short 11.

### Operating implication

In fast markets, a ladder reduces the need for an execution algorithm to react immediately to fills. All limits required for possible positions during a day can be pre-calculated and placed when the market opens. Maintenance then consists of replacing orders above or below the point where existing orders fill.

### Constraints, risks, and capital limit

- Order modification/cancellation may have different fees; the optimal approach must account for them.
- Visible resting orders reveal information that high-frequency traders can use. This may be less material for retail traders.
- More capital makes optimal-position increments closer in price. Leaving old orders can therefore create dozens or hundreds of visible orders.

**Large-capital example:** with $50 million, initial position is short 1,168 contracts. The buy limit calculated from an optimal position of 1,167 contracts is 132.999, less than one tick below 133. To obtain 132.984375, one tick below 133, use an optimal position of 1,132. This requires a buy limit for **1,168 − 1,132 = 36 contracts** one tick below price, and a **32-contract** sell one tick above price. The author warns that many visible 30-plus-contract limits one tick apart invite HFT attention. Hence this strategy has an upper deployable-capital limit; if order sizes exceed a few contracts, carefully limit instrument weight. The source footnote adds that someone buying more or selling several contracts per tick may consider order types not visible in the book.

### Overnight orders

Limit orders normally cancel automatically at day end, though longer-lived orders can be created. The author’s conclusion is to avoid leaving the ladder active overnight.

Reason: in a cited strategy-twenty-seven scenario, next-day price opens sharply at 134.5 while current position is short 12 and optimal position short 25. The recommended action is immediately sell 13 as a standard market order, probably one tick below 134.5. A ladder left from 133.00 to 134.50 would instead have filled at around 133.75 on average—worse. Keeping the ladder would only help if price jumped to 134.5 at the open and then returned to 133 before a market order could be sent.

## Procedures and implementation checklist

1. Collect continuous sampled bid–ask spreads, order-time spreads/sizes, and actual mid-to-fill spreads/sizes.
2. Establish expected costs for prospective instruments and verify rule turnover against the speed limit.
3. For active instruments, update expected costs using the chapter’s composite modelling rule; monitor actual-versus-expected execution.
4. Avoid predictable thin-liquidity windows and lower maximum order sizes in holiday conditions as needed.
5. If participation is meaningful, estimate cost as a function of trade size and daily-volume share; do not presume linearity.
6. Test execution routes by randomized allocation where feasible, measuring comparable orders.
7. For the simple algo, begin passive; switch permanently to aggressive mode upon adverse movement, stated imbalance, or five-minute timeout.
8. For fast directional limit-order strategies, decide whether a same-day ladder’s reduced reaction-time requirement is worth fee and information-leakage costs; constrain capital/weight if order sizes become conspicuous.
9. Default to cancelling ladder orders overnight.

## Warnings and edge cases

- A quoted half-spread is only a small-order baseline and does not include commissions in the chapter’s cost discussion.
- A limit order is not automatically cheap: delayed/non-fill risk can turn it into an expensive chase.
- Passive/aggressive switching carries negative skew, not a guaranteed steady improvement.
- The stated imbalance trigger is asymmetric in the source: only the buying case is explicitly defined; do not invent a sell-side threshold rule.
- Level-two modelling is only an estimate, particularly at untraded large sizes.
- Costs can cease to be linear or predictable at significant participation.
- Time-of-day optimization is presented as protection against bad timing, not as a promise of major cost reduction.
- Visible ladders disclose intent and can become operationally impractical at large capital.
- Overnight ladder exposure may cause fills far inferior to a next-session market response.

## Connections to other chapters

- **Part One:** speed limit on trading frequency, risk-adjusted cost, forecast smoothing, position buffering, and the earlier assumption that trading costs could be treated independently of size/weight.
- **Strategy twenty-five:** dynamic optimisation uses expected trading cost directly (footnote).
- **Part Four:** fast directional strategies primarily use limit orders, so the standard execution algo is not applicable.
- **Strategy twenty-six:** source of the initial limit-order example and the process modified into a ladder.
- **Strategy twenty-seven:** source of the overnight-gap example supporting cancellation of resting ladders.

## Glossary candidates

Aggressive execution; adverse price movement; bid; bid–ask spread; brokerage commission; daily volume; execution algorithm; fill; half-spread; imbalance; level two data; limit order; liquidity; market order; mid price; negative spread cost; order book; passive execution; permanent price impact; participation rate; risk-adjusted cost; speed limit; spread cost; timeout; trading ladder.

## Key takeaways

- Execution costs should be explicitly measured from sampled markets, submission-time conditions, and realized fills.
- Cost, liquidity, order size, trade frequency, rule choice, and instrument weight interact once a trader is a material part of volume.
- Passive limit-first execution can lower average spread costs, but can lose sharply when prices run away; its payoff is negatively skewed.
- The author’s simple algo uses a passive initial limit and switches on adverse move, >5:1 stated buy-side book imbalance, or five-minute timeout.
- Same-day limit ladders can reduce fill-reaction demands for fast directional strategies, but they create fees, visibility, and scale constraints; the author recommends against leaving them overnight.
