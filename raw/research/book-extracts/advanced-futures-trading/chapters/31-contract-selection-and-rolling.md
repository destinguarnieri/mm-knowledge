# Tactic One: Contract Selection and Rolling

## Purpose and central argument

A futures instrument is a set of dated contracts, not a perpetual position. To approximate a continuing exposure, a trader must choose an expiry, decide when to replace it, and choose the execution method for that replacement (the **roll**). The chapter’s central argument is that expiry choice and rolling should be driven first by liquidity and delivery constraints, then by risk, seasonality, carry measurement, and trading cost. Where there is a choice, the author generally prefers contracts away from the front of the curve, subject to liquidity.

The chapter uses VIX futures as its main example and treats the following as three linked decisions:

1. Which expiry to hold.
2. When to roll to a new expiry.
3. How to execute that roll.

## Core vocabulary

- **Expiry / contract month / delivery month:** A particular dated futures contract.
- **Front contract:** The nearest-expiring contract.
- **Roll:** Replacing exposure in one expiry with equivalent exposure in another.
- **Liquidity:** Tradability, assessed here with average daily contract volume and average daily USD risk volume.
- **Open interest:** Outstanding futures positions; reported as a descriptive characteristic in Table 169.
- **USD risk volume:** Daily volume expressed in risk-scaled US-dollar terms.
- **Volatility term structure:** The pattern of annualised standard deviations across maturities.
- **Samuelson effect:** The name used here for VIX’s typical pattern of high volatility at the front contract that gradually declines with maturity.
- **Back-adjusted price:** A continuous series constructed from consecutive futures expiries; it underlies the trend forecast discussed in the chapter.
- **Raw carry / roll yield:** A carry measure derived from relative futures prices; a risk-adjusted roll yield supplies the carry forecast.
- **First notice date (FND):** The earliest date a long holder may be notified to take physical delivery; commonly several days before expiry.
- **Spread trade:** A one-order transaction exchanging one futures expiry for another.
- **Passive rolling:** Moving exposure through ordinary position-increasing and position-reducing trades rather than an explicit roll order.
- **Natural close:** A passive-roll special case in which the strategy closes its entire current position before it reopens in the next expiry.
- **Relative value (RV) calendar spread:** Equal-and-opposite positions in different expiries of the same instrument.

## Choosing an expiry

### 1. Apply liquidity filters first

An illiquid expiry is dangerous even if it has other advantages: it is likely to be more expensive because fewer participants imply wider spreads. Exclude an expiry if it fails either threshold:

- Average daily volume: at least **100 contracts per day**.
- Average daily USD risk volume: at least **$1.25 million per day**.

The source states that volumes for these calculations are averaged over the last 30 days.

### USD-risk-volume formula

\[
\text{Average daily volume in USD risk}
= \text{FX rate} \times \text{average daily volume} \times \sigma_{\%} \times \text{price} \times \text{futures multiplier}
\]

| Symbol / input | Meaning and units |
|---|---|
| FX rate | Conversion factor into USD; use where required by the contract currency. |
| Average daily volume | Contracts traded per day, averaged over 30 days in the author’s calculations. |
| \(\sigma_{\%}\) | Annualised standard deviation of percentage returns, expressed as a decimal in the formula. |
| Price | Futures price, in the contract’s price units. |
| Futures multiplier | Dollar value represented by one price-unit movement for one contract. |
| Output | US-dollar risk volume per day. |

**Conditions:** Apply the filters separately to every potential expiry, then consider only expiries that pass. This formula is presented for screening liquidity in risk terms; the chapter does not provide a derivation.

### VIX example: quoted characteristics (May 2022)

Table 169 communicates that VIX liquidity and open interest fall sharply into later expiries; it also gives the contemporaneous spot VIX of 28.48.

| Expiry | Price | Daily volume | Open interest |
|---|---:|---:|---:|
| June 2022 | 29.45 | 67,000 | 123,000 |
| July 2022 | 30.13 | 33,200 | 59,000 |
| August 2022 | 30.11 | 10,400 | 48,000 |
| September 2022 | 30.15 | 7,000 | 21,000 |
| October 2022 | 30.10 | 5,500 | 13,400 |
| November 2022 | 29.55 | 3,000 | 9,500 |
| December 2022 | 28.60 | 1,100 | 4,900 |
| January 2023 | 28.95 | 30 | 217 |
| February 2023 | 29.125 | 0 | 0 |

For VIX, the futures multiplier used is **$1,000**. Table 170 adds risk scaling and shows that January and February 2023 fail both minimums.

| Expiry | Price | \(\sigma_{\%}\) | Daily volume | USD risk volume |
|---|---:|---:|---:|---:|
| June 2022 | 29.45 | 66.8% | 67,000 | $1,320m |
| July 2022 | 30.13 | 51.5% | 33,200 | $510m |
| August 2022 | 30.11 | 43.9% | 10,400 | $140m |
| September 2022 | 30.15 | 36.1% | 7,000 | $75m |
| October 2022 | 30.10 | 31.7% | 5,500 | $52m |
| November 2022 | 29.55 | 30.5% | 3,000 | $27.1m |
| December 2022 | 28.60 | 30.0% | 1,100 | $9.4m |
| January 2023 | 28.95 | 29.6% | 30 | $270,000 |
| February 2023 | 29.125 | 29.3% | 0 | $0 |

Liquidity does not always decline smoothly with maturity. In full-sized WTI Crude Oil, June and December contracts in successive years have better volume and open interest than other months. Gold lists extra expiries to keep the nearest three months available, but the author says its practical liquid choices are the core February, April, June, August, October, and December contracts.

### 2. Evaluate risk by expiry, not just instrument

Different expiries of the same instrument can have materially different risk.

- VIX usually has high annualised standard deviation in the front contract, declining further out: the Samuelson effect.
- In the stated Eurodollar example, volatility rises sharply through the first four quarterly maturities and then declines. The pattern is not fixed: in much of the low-rate 2010s, it instead rose monotonically far into the curve; a near, close Federal Reserve decision can make the front contract the most volatile.
- Known future events—crop reports, elections, economic announcements—can distort volatility in selected expiries.

The author’s trade-off is:

- Higher volatility: lower leverage and lower risk-adjusted trading costs.
- Lower volatility: lower minimum capital.

The stated preference is for higher volatility, but standard deviation alone is insufficient. Tail risk, skew, and jumpiness can matter; kurtosis or the author’s tail-ratio statistics may quantify them. Front interest-rate contracts can jump because rate expectations change in 25-basis-point increments; front VIX is also affected disproportionately by jumpy spot VIX. Therefore, despite high standard deviation, the author generally avoids the first VIX expiry.

### 3. Account for seasonality and carry measurement

Agricultural and energy futures can be seasonal. Holding the first or second contract throughout the year can make the carry experienced by the instrument seasonal. Where liquidity permits, hold a fixed calendar-month expiry instead; examples are the next December full-sized WTI contract and many Corn and Wheat positions. Henry Hub Natural Gas is cited as a case where insufficient distant liquidity prevents this approach.

The more precise raw-carry method (linked explicitly to Strategy Ten) compares the held contract with a nearer contract. It cannot be used when holding the front contract. If forced to hold the first expiry, use the less precise method that compares it with a farther-out expiry.

### 4. Respect settlement and delivery constraints

VIX is cash settled: at expiry, cash equals the difference between final settlement and the entry price, though variation margin will generally already have credited or debited most of it. Cash settlement is described as standard for equity indexes, STIR futures such as Eurodollar, and volatility futures.

Most bond, foreign-exchange, and physical-commodity futures are physically settled. A long may have to take delivery; a short may have to transfer or arrange delivery. Brokers commonly force-close positions nearing expiry. For physically settled contracts, do not merely plan around expiry: close several days before FND, because a long holder can be notified for delivery from that date.

Cash settlement does not eliminate expiry risk: settlement is measured over a short window and can be susceptible to manipulation, especially in thin markets. A cited note says even liquid futures have been manipulated; Eurodollar’s historical LIBOR settlement mechanism is offered as an example.

### 5. Reduce roll frequency where appropriate

Rolling costs spreads and commissions. A farther-out contract can reduce the number of rolls. The author’s Eurodollar example:

1. Liquid quarterly contracts extend roughly six years.
2. Avoid the first year because of lower volatility and undesirable tail risk; avoid beyond three years because standard deviation is then somewhat too low.
3. This leaves a usable one-to-three-year window.
4. Initially trade a contract about three years out (June 2025 in the example).
5. After three months, begin passively rolling into June 2027.
6. In May 2024, when June 2025 has about one year remaining, explicitly roll any residual June 2025 position into June 2027.

Worst case: a two-year rather than quarterly roll cycle. A two-year calendar spread may have a wider bid–ask spread than a three-month spread, but reducing the count of rolls by eight is expected to save more over time. Caveat: with a steep volatility term structure, the new contract’s character—including its standard deviation—can change abruptly.

Holding two or more expiries is permitted and can make rolling gradual, reduce concentration in a delivery month, and help a large fund stay below per-expiry regulatory position limits. It adds operational complexity.

### Chapter rules of thumb

- Trade only liquid expiries; in many financial futures and metals, this leaves only the front contract.
- When there is a choice, avoid the front if possible: carry is less accurate, prices can be jumpy, and delivery or settlement-manipulation risks rise.
- Prefer the second, third, fourth, or later expiry when feasible; risk properties can improve and rolling is less frequent.
- Where relevant, use a fixed calendar month to remove seasonality from the back-adjusted price.
- Consider multiple months for large positions.

## Choosing expiries by forecast: a deliberately optional complication

For a wide expiry set, one could choose the contract with the largest combined forecast. The author explains why this is awkward:

- **Trend:** Trend is based on a back-adjusted series made from consecutive expiries. Contract-by-contract trend selection would be limited to very short trends unless each contract had been liquid for at least a year, preferably longer.
- **Carry:** It may make sense to choose the expiry with the greatest absolute risk-adjusted roll yield. In the VIX curve of Table 170, carry is described as strongly positive in front, lower in second, then negative for subsequent expiries. If carry alone were traded, December 2022 would be selected and shorted because it has the largest absolute (negative) carry forecast.
- **Combined trend and carry:** If trend requires a short, December 2022 fits; if trend is long, the front contract’s highest positive carry would fit. Yet accurate front-contract carry needs spot, so the second contract is a possible compromise.

The author ultimately keeps contract selection simple and ignores this factor.

## When to roll

Use the same selection criteria that set the initial expiry.

- **If forced to hold the front:** Roll into the second contract as soon as it is liquid. This is usually a few days before front expiry, but may be only immediately before expiry (Korean bonds are cited). For physically settled contracts, exit before FND, not merely before expiry.
- **If holding the second:** Roll to the following contract once liquid, and certainly before the current front expires. Example: holding July 2022 VIX, August is liquid enough but has lower standard deviation; waiting may be reasonable, but the roll must occur before June expires so July does not become front month.
- **If holding farther out:** Choose a systematic cadence (quarterly to remain around three years out), a low-frequency approach (up to a couple years), or an intermediate six- or twelve-month cadence.
- **If holding a fixed calendar month:** Exit before it becomes front, if not earlier. Example: leave December 2022 WTI at least a few days before November 2022 expires, preserving accurate carry measurement.

### Backtest realism warning

The chapter’s hedge-fund anecdote reports that moving US bond-futures roll dates from just-before-expiry to before FND altered the back-adjusted series: the revised curve had a slightly lower upward gradient and return. The inferred explanation is a small premium paid to those able to hold a long position through delivery risk. The lesson is to use realistic historical roll calendars rather than assuming infeasible execution.

## How to roll

| Method | Procedure | Benefits | Constraints / risks |
|---|---|---|---|
| Individual legs | Close current expiry and separately open equal size in new expiry. | Simple. | Pays two bid–ask costs; executions may not coincide, leaving double exposure if close fails or zero exposure if open fails. Avoid if possible; if unavoidable, trade in tranches and avoid just before the close. |
| Spread trade | Submit the calendar spread as a single market order. | Both legs execute together; broadly expected to cost about half of two separate trades. Some markets (e.g., S&P 500 futures) have smaller spread-market ticks, making it cheaper still. | Requires a liquid spread market. Usually available; Eurodollar spreads may be more liquid than outrights, but not always. |
| Passive roll | Close/reduce in the current month; open/increase in the next month as normal trading signals occur. | No extra roll-only trading, so the roll itself costs nothing. | Can begin only when next month is liquid. Time may be insufficient to complete it; residual current-month exposure may still need a spread or separate legs. Forecasts remain calculated from current-month prices while holdings blend months, creating minimal stated basis risk. |
| Natural close | At a strategy-driven complete close, switch trading to next expiry before any new position opens. | Avoids multi-month complexity. | Requires timing luck and daily review of fully closed instruments. |
| Let expire, then reopen | For a cash-settled future, let it settle and open next expiry the following day. | One opening trade rather than a close-plus-open; potentially halves trading cost. | Only cash settled; use only when savings outweigh being flat between settlement and reopening. |

### Passive rolling across multiple months

For a three-month holding (June, July, August 2022): make closing trades in June and opening trades in August, with no July trades. Once June is fully closed, make closing trades in July and opening trades in September. The same pattern generalises to any number of held months.

### Physical-delivery exception noted for FX futures

With a multi-currency account, it can be operationally straightforward to deliver or take delivery of currencies: expiry creates a credit in one currency and a loan in another, then a spot FX transaction removes them. The source cautions that transaction costs and possible interest until spot settlement mean this is unlikely to be cheaper than rolling, though it can make sense in some circumstances.

## Risk, position sizing, and rolls

Positions scale inversely with standard deviation. The chapter’s calculation is:

\[
N_{\text{new}} = N_{\text{old}}\frac{\sigma_{\text{old}}}{\sigma_{\text{new}}}
= 100\frac{0.51}{0.44}=115.9\approx116
\]

| Symbol | Meaning |
|---|---|
| \(N_{\text{old}}\) | Current number of contracts (100 in the illustration). |
| \(N_{\text{new}}\) | Risk-equivalent contract count after rolling. |
| \(\sigma_{\text{old}}\) | Annualised standard deviation of the former expiry (just over 51% for July 2022 VIX). |
| \(\sigma_{\text{new}}\) | Annualised standard deviation of the new expiry (about 44% for August 2022 VIX in the worked illustration). |

Thus the theoretical new position is 116 contracts, about 16 above the original 100. The table elsewhere reports August at 43.9%; the narrative rounds it to 44%.

With a linear volatility term structure, the *current* standard deviation rises as a held contract ages, drops abruptly at the roll into a more distant expiry, then repeats: a sawtooth. Direct position sizing on that current value would also be sawtoothed. The author does not do that, because daily-data current-volatility estimates are too noisy. Instead use an exponentially weighted rolling volatility estimate; its sawtooth is much shallower. A simple rolling window longer than one month would eliminate the sawtooth; combining recent and long-run volatility further reduces it. In the illustration, the residual change is only a few contracts for a 100-contract position; with fewer than eight VIX contracts, rounding means no observable change. The issue is greatest at the front of VIX and Eurodollar curves, where volatility changes are larger.

## Special cases

### Dynamic optimisation (Strategy Twenty-Five; Part Three)

To implement expiry-then-reopen, constrain the optimiser so it generates no trade in the instrument. After expiry, update current positions to zero; the optimiser may reopen in the new month or allocate risk elsewhere. Constraints can also prevent new positions in an expiry that will soon expire when the successor is still illiquid, avoiding an immediate costly roll and allowing risk to move to other instruments.

### Fast directional strategies (Part Four)

High trading frequency makes passive rolling more likely to complete. But multi-month holdings make limit-price calculations more complex because prices must match each expiry. The author prefers waiting for the strategy to close, then switching to the next expiry before a new position; fast strategies should not remain closed long.

### Relative-value strategies (Part Five)

For cross-instrument RV, coordinate rolls across instruments if possible. Calendar spreads and triplets within one instrument are harder. A Eurodollar RV spread with opposite June 2023 and December 2023 legs requires two simultaneous spread rolls—June to July and December to March 2024—or potentially a four-leg order, whose specific liquidity may be difficult. Adjacent expiries add operational complexity: rolling a July/August 2022 VIX spread into August/September means August is simultaneously the old leg for one side and the new leg for the other.

## Figures, tables, and source limitations

- **Table 169:** VIX expiry price, volume, and open interest as of May 2022; spot VIX 28.48. Reproduced above.
- **Table 170:** VIX price, annualised percentage standard deviation, daily contract volume, and USD risk volume; demonstrates the liquidity filters. Reproduced above.
- **Formula image (USD risk volume):** Transcribed above. The EPUB encodes it as an image rather than semantic text.
- **Formula image (position adjustment):** Transcribed above. The rendered equation visually uses the inverse-volatility ratio shown; its source image is legible.
- Several divider images are present in the EPUB but convey no substantive information beyond section separation.

## Connections explicitly made to other parts of the book

- **Strategy Three:** liquidity criteria used to filter expiries.
- **Strategy Ten:** seasonality and two raw-carry calculation methods.
- **Strategy Eleven:** combined carry-and-trend forecasting.
- **Strategy Twenty-Five / Part Three:** dynamic optimisation constraints.
- **Part Four:** fast directional strategies.
- **Part Five:** RV strategies and the VIX-spread example.

## Key takeaways

1. Treat expiry selection, roll timing, and roll execution as one operational problem.
2. Screen each expiry for liquidity before considering its apparent attractiveness.
3. Front contracts are often necessary but have recurrent drawbacks: delivery/FND exposure, poorer carry measurement, jump risk, settlement risk, and more frequent rolls.
4. Further-out liquid expiries can improve properties and lower roll frequency, but may introduce distinct volatility, tail-risk, or liquidity characteristics.
5. Prefer a liquid spread roll to separate legs; use passive rolling where normal turnover can complete it.
6. Make backtests obey actual delivery and roll constraints, or their returns can be overstated.
7. Rolling can alter volatility and the risk-equivalent position; smoothed volatility estimation makes that effect usually small, not nonexistent.
