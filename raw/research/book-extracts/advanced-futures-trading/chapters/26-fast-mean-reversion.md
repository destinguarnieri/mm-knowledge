# Strategy 26 — Fast mean reversion

## Purpose and central claim

This is an hourly-data futures strategy designed to capture price mean reversion over a holding period of a few days (in practice, turnover is roughly 140 times per year before the smarter-execution treatment). It takes a long position when the current price is below a short-horizon equilibrium and a short position when it is above it. The key implementation contribution is to use one-lot limit orders at prices implied by adjacent target positions, using market orders only when the actual position has fallen more than one contract behind the rounded optimum. This substantially reduces spread costs, but does not eliminate commissions, gap risk, capacity limits, or the strategy's severe negative-skew risk.

The chapter's broader argument is explicitly speculative: markets do **not** appear to be fractal in the sense that the same strategy works at every time scale. The author's evidence-based examples suggest different regions favour trend or mean reversion; the chapter tests the "few days" mean-reversion region. It does **not** establish that the proposed alternating pattern holds everywhere.

## Context: time scale and market behaviour

The author contrasts the strategy with earlier daily strategies, which typically hold for weeks and deliberately avoid high trading costs. This chapter uses hourly data, which the author considers sufficient to test strategies with one- or two-day holding periods, but not high-frequency trading (HFT).

| Horizon / frequency | Behaviour stated or hypothesised in the chapter |
|---|---|
| Multi-year | Mean reversion works, though slow-horizon value results are not statistically significant. |
| Several months to one year | Trend following works, but less well than at faster trend horizons. |
| Several weeks to several months | Trend works extremely well. |
| Several days to one week | Trend weakens (especially EWMAC2 relative to slower variants), even before costs. |
| A few days | Mean reversion is hypothesised, and this chapter finds it. |
| A few hours | Trend is hypothesised, but the author could not find a viable hourly-data strategy. |
| Less than a second | Mean reversion works well in HFT. |

The author could not reproduce viable sub-day trend strategies: tested strategies had low or negative returns before costs, even without the usual one-hour fill lag. A possible trend effect may only become clear at a frequency too fast to test accurately with hourly data. The execution method in this chapter is unsuitable for trend strategies because they must pay the full execution spread.

> **Boundary:** This is not an HFT strategy. The author has hourly history only from January 2013—just under ten years at the time of writing—rather than up to 50 years of daily history.

## Model and forecast

### Inputs and timing

- Use a series of **daily back-adjusted futures prices** \(p_t\), indexed to weekdays, to calculate equilibrium.
- Use the **current hourly price** for the trading signal and backtest.
- The equilibrium and daily volatility estimate are calculated daily and used during the following day. The chapter says this avoids variable overnight-gap treatment and allows an overnight calculation plus a lightweight intraday process.
- The equilibrium EWMA span is five weekdays (about one week). The choice was deliberately arbitrary—not backtested—to avoid overfitting; nearby spans were checked for robustness. Multiple spans are not combined because their variants are highly correlated and are harder to trade together.

### Equations

\[
\mathrm{Equilibrium}_t = \operatorname{EWMA}_{\mathrm{span}=5}(p_{t-1},p_{t-2},p_{t-3},\ldots)
\]

\[
\mathrm{RawForecast}_t = \mathrm{Equilibrium}_t-p_t
\]

\[
\sigma_{p,t}=\frac{p_t\,\sigma_{\%,t}}{16}
\]

\[
\mathrm{RiskAdjustedForecast}_t=\frac{\mathrm{RawForecast}_t}{\sigma_{p,t}}
\]

\[
\mathrm{ScaledForecast}_t=9.3\times\mathrm{RiskAdjustedForecast}_t
\]

\[
\mathrm{CappedForecast}_t=\max\left(\min(\mathrm{ScaledForecast}_t,20),-20\right)
\]

| Symbol / term | Definition, units, and conditions |
|---|---|
| \(p_t\) | Back-adjusted futures price. In the equilibrium equation, \(p_{t-1}\) is the last available **daily closing** price. In the raw forecast, it is the current intraday/hourly price. Price units are the futures price quotation. |
| \(\mathrm{Equilibrium}_t\) | Five-day-span EWMA of prior daily prices; same price units as \(p\). |
| \(\sigma_{\%,t}\) | Annual standard deviation of percentage returns, expressed as a decimal (e.g. 6% = 0.06). |
| \(\sigma_{p,t}\) | Daily standard deviation in price units. The factor 16 converts annual to daily volatility as used by the author. It should use the previous day’s close of the currently traded futures contract. |
| 9.3 | Estimated forecast scalar. |
| \(\pm20\) | Absolute cap on the scaled forecast. |

A price below equilibrium produces a positive forecast and long bias; a price above equilibrium produces a negative forecast and short bias. The strategy uses **no buffering**: it should always hold the rounded optimal position. The author states that buffering would decimate mean-reversion profitability.

### Figure 81: equilibrium and hourly US 10-year futures price

The figure plots hourly price in grey and the daily-updated equilibrium in black during the 2020 COVID-19 panic. The equilibrium is smoother and lags price. When price exceeds equilibrium the strategy is short; when it falls below, it is long. The example shows a persistent losing short from late February, then dip-buying on 13 March, rally-selling a few days later, and another dip-buy around 19 March. It illustrates both the intended mechanism and the danger of a persistent adverse move.

## Position sizing

The forecast requires neither combination with other forecasts nor any special cap beyond \(\pm20\), so it enters the standard position-sizing framework directly:

\[
N_t=\frac{\mathrm{CappedForecast}_t\times \mathrm{Capital}\times\mathrm{IDM}\times\mathrm{Weight}_i\times\tau}{10\times\mathrm{Multiplier}_i\times p_t\times FX_t\times\sigma_{\%,t}}
\]

Equivalently, separate the forecast scaling from the \(+10\) reference forecast:

\[
N_t=\frac{\mathrm{CappedForecast}_t}{10}\times\mathrm{AveragePosition}_t
\]

\[
\mathrm{AveragePosition}_t=\frac{\mathrm{Capital}\times\mathrm{IDM}\times\mathrm{Weight}_i\times\tau}{\mathrm{Multiplier}_i\times p_t\times FX_t\times\sigma_{\%,t}}
\]

| Variable | Meaning |
|---|---|
| \(N_t\) | Unrounded target number of futures contracts; round to an executable integer. |
| Capital | Trading capital in base currency. |
| IDM | Instrument diversification multiplier. |
| \(\mathrm{Weight}_i\) | Portfolio weight of instrument \(i\). |
| \(\tau\) | Annual risk target (20% in the worked example). |
| \(\mathrm{Multiplier}_i\) | Futures contract multiplier. |
| \(FX_t\) | Exchange rate converting the instrument’s P&L into base currency. |
| \(p_t\), \(\sigma_{\%,t}\) | As defined above. |

## Worked US 10-year bond-future example

At an early-March-2020 point: equilibrium = 132.5, current price = 133, and \(\sigma_\%=6\%\).

\[
\mathrm{RawForecast}=132.5-133=-0.5
\]

\[
\sigma_p=133\times0.06/16=0.4987
\]

\[
\mathrm{RiskAdjustedForecast}=-0.5/0.4987=-1.0025
\]

\[
\mathrm{ScaledForecast}=-1.0025\times9.3=-9.32
\]

For one instrument with \(\mathrm{Weight}=\mathrm{IDM}=FX=1\), capital $500,000, multiplier 1,000, and \(\tau=20\%\):

\[
\mathrm{AveragePosition}=\frac{500000\times1\times1\times0.2}{1000\times133\times1\times0.06}=12.53
\]

\[
N=(-9.32/10)\times12.53=-11.68
\]

The executable target is therefore **short 12 contracts**.

## Smart limit-order execution

### Principle

For a mean-reversion signal, the price that requires a more-short target is higher; the price that requires a less-short target is lower. Solve the target-position equation after substituting the forecast formula:

\[
N_t=\left[\frac{9.3(\mathrm{Equilibrium}_t-p_t)}{\sigma_{p,t}\times10}\right]\times\mathrm{AveragePosition}_t
\]

\[
p_t=\mathrm{Equilibrium}_t-\frac{N_t\times10\times\sigma_{p,t}}{9.3\times\mathrm{AveragePosition}_t}
\]

This inversion lets the trader place limit orders at the price which would make the adjacent position optimal. Limit fills are assumed to pay commission but no spread cost, subject to the backtest and capacity assumptions below.

### Example: orders around short 12

For a buy that changes current \(-12\) to \(-11\):

\[
p=132.5-\frac{-11\times10\times0.4987}{9.3\times12.53}=132.97
\]

US 10-year futures trade in ticks of \(1/64=0.015625\), so the limit is **132.96875**. The sell limit for target \(-13\) is **133.046875** (unrounded calculation: 133.05).

| Order | Price | Result if filled |
|---|---:|---|
| Sell limit | 133.046875 | Sell 1; become short 13 |
| Current price / position | 133.00 | Short 12 |
| Buy limit | 132.96875 | Buy 1; become short 11 |

If the following hour reaches 133.078125, the sell fills and the position becomes short 13. Recalculate both adjacent orders: sell one to reach \(-14\) at 133.09375 and modify the buy to reach \(-12\) at 133.015625.

### Forecast-cap rule

At current price 134.5 with the same equilibrium and volatility:

\[
\mathrm{RawForecast}=-2.0,\quad \mathrm{RiskAdjustedForecast}=-4.01,\quad \mathrm{ScaledForecast}=-37.3
\]

Cap this at \(-20\): \(N=(-20/10)\times12.53=-25.06\), i.e. short 25 contracts. The buy limit can seek target \(-24\) (133.53125 after tick rounding); there is **no sell limit**, because the capped forecast forbids getting shorter. Symmetrically:

- if scaled forecast \(\le -20\): no sell limit order;
- if scaled forecast \(\ge +20\): no buy limit order.

### Operational algorithm

1. Before/at the day’s intraday process, use the precomputed daily equilibrium and volatility with current price to compute scaled forecast, capped forecast, average position, unrounded target, and rounded target.
2. If the rounded target is more than one contract from current position, send an immediate **market order** for the difference.
3. Otherwise, unless blocked by the forecast-cap rule, place a **buy limit** for one contract using current position \(C\):

   \[
   p_{buy}=\mathrm{Equilibrium}-\frac{(C+1)\times10\times\sigma_p}{\mathrm{Scalar}\times\mathrm{AveragePosition}}
   \]

4. Unless blocked by the forecast-cap rule, place a **sell limit** for one contract:

   \[
   p_{sell}=\mathrm{Equilibrium}-\frac{(C-1)\times10\times\sigma_p}{\mathrm{Scalar}\times\mathrm{AveragePosition}}
   \]

5. If a buy fills, create a new buy order and modify the sell order to the correct price. If a sell fills, create a new sell order and modify the buy order.
6. Cancel **all** limit orders at the end of the day. Do not leave them overnight.
7. On a gap/open that makes target more than one contract away, immediately use a market order to restore the rounded optimal position. Example: a next-day open at 134.5 from short 12 implies short 25, so sell 13 at market.

## Backtest assumptions, constraints, and errors to avoid

### Assumptions used in the hourly backtest

- A submitted limit order fills **one hour later at its limit price** if the next price is lower than the limit for a buy, or higher than the limit for a sell.
- Market orders also have a one-hour lag and use the author’s normal bid-ask-spread assumptions.
- All orders pay commissions; market orders additionally pay their assumed spread cost.
- Commissions and spreads are historically deflated under the author’s normal methodology.

### Important limitations

- A small trader may reasonably assume a one-lot, sufficiently spaced limit order fills when the historical price crosses it, **only in a sufficiently liquid market**. That assumption is not valid at large size.
- Large visible limit orders can change other participants’ behaviour. The chapter gives an extreme example of a large buy one tick below best bid: it can prompt offers/bids to rise and make the fill less likely. Deliberately placing orders without intent to fill to move prices is described as spoofing and against market regulations.
- Greater capital bunches adjacent one-lot orders together; at still greater capital they become multi-lot. In the $50m version of the US 10-year example, a one-tick-below buy would need 36 contracts and a one-tick-above sell 32. Such sizes may induce reactions. This is a **capacity constraint** of fast trading, not a loophole removed by using limits.
- Never assume 24-hour trading or no discontinuous gaps. Overnight orders are especially unsafe; cancel them.
- No buffering is an intentional property, not an omission. Slowing the strategy materially damages performance according to the author.

## Tradable universe and cost screen

The strategy’s direct turnover is stated as about 140 per year and its holding period as less than two weekdays. The smart-limit tactic reduces costs, but a normal risk-adjusted-cost speed-limit calculation is technically inapplicable to a mixture of limits and markets. As an approximation, use assumed turnover 45 and the ordinary cost-per-trade measure:

\[
\mathrm{MaximumTurnover}=\frac{0.15-(\mathrm{CostPerTrade}\times\mathrm{RollsPerYear})}{\mathrm{CostPerTrade}}
\]

The screen requires maximum turnover at least 45. In the author’s Jumbo portfolio, 18 instruments fail and 84 remain. The trading plan also phrases the admissibility rule as costs below 3% per year assuming \(\tau=20\%\), plus minimum-capital and liquidity thresholds. Earlier, without the execution improvement, only a handful meet the normal speed limit—mostly CAC40, Dow Jones, NASDAQ micro, Russell 2000, S&P 500 micro, and Gold micro.

## Performance evidence (hourly data since January 2013)

Costs in Tables 129–130 are **commissions only** for display, not spread costs. The reported mean returns are still post-cost returns: they include market-order spread costs. Therefore these tables cannot be directly compared with prior same-type tables.

### Table 129 — median financial-instrument performance

| Metric | Equity | Vol | FX | Bond |
|---|---:|---:|---:|---:|
| Mean annual return | 15.0% | 23.5% | 17.1% | 11.4% |
| Costs (commission) | −1.0% | −2.3% | −1.2% | −1.3% |
| Average drawdown | −9.9% | −16.0% | −7.6% | −8.9% |
| Standard deviation | 27.4% | 31.3% | 23.5% | 26.1% |
| Sharpe ratio | 0.54 | 0.75 | 0.73 | 0.44 |
| Turnover | 57.4 | 49.1 | 63.9 | 53.0 |
| Skew | −0.96 | −2.31 | −0.34 | −0.65 |
| Lower tail | 3.35 | 4.20 | 2.95 | 3.38 |
| Upper tail | 1.78 | 2.17 | 1.79 | 1.86 |

### Table 130 — median commodity-instrument performance

| Metric | Metals | Energy | Ags | Median |
|---|---:|---:|---:|---:|
| Mean annual return | 6.1% | 0.6% | −1.6% | 10.7% |
| Costs (commission) | −1.0% | −0.3% | −1.8% | −1.0% |
| Average drawdown | −13.6% | −15.8% | −36.1% | −11.0% |
| Standard deviation | 26.2% | 28.1% | 26.1% | 26.4% |
| Sharpe ratio | 0.19 | 0.04 | −0.06 | 0.41 |
| Turnover | 59.4 | 57.1 | 59.4 | 57.4 |
| Skew | −0.74 | −1.00 | −0.92 | −0.82 |
| Lower tail | 4.30 | 3.29 | 3.21 | 3.35 |
| Upper tail | 1.68 | 1.93 | 1.99 | 1.86 |

The author calls the 0.41 average/median Sharpe ratio extremely good for an individual instrument, but notes the limited eight-year sample. Financials outperform commodities in these tables, but the author cautions against selecting only financials: cross-instrument performance differences are rarely statistically significant.

### Table 131 — aggregate Jumbo portfolio since 2013

| Metric | Strategy 9: multiple trend | Strategy 10: carry | Strategy 26: fast mean reversion |
|---|---:|---:|---:|
| Mean annual return | 13.8% | 8.7% | 17.6% |
| Costs | −1.1% | −0.7% | −3.1% |
| Average drawdown | −15.0% | −10.2% | −7.3% |
| Standard deviation | 17.5% | 15.3% | 22.0% |
| Sharpe ratio | 0.79 | 0.56 | 0.80 |
| Turnover | 40.6 | 10.5 | 39.2 |
| Skew | 0.20 | −0.31 | −1.46 |
| Lower tail | 2.96 | 2.06 | 2.74 |
| Upper tail | 2.01 | 1.33 | 1.98 |

For fast mean reversion, costs here are commissions only; trend and carry costs include commissions and spreads. Despite the higher displayed cost, Strategy 26 is comparable with trend by Sharpe ratio and slightly better than carry, but has worse skew. Its correlation is about **−0.28 with trend** and **+0.15 with carry**, implying diversification potential.

### Figure 82: account-curve interpretation

Over the hourly-data period, trend and mean reversion achieve similar overall performance by markedly different paths. Mean reversion exhibits negative skew: prolonged steady gains, followed by a COVID-panic crash in 2020, and underperformance beginning in early 2022 amid elevated risk following Russia’s invasion of Ukraine. Trend exhibits positive skew: brief strong gains followed by slow declines; it tends to perform better when mean reversion suffers (March 2020, Q1 2022, late 2014, and H2 2017).

## Combining with other strategies

Do **not** combine its forecast mechanically with daily strategies. Fast mean reversion uses continuous prices, no buffer, and intraday limits; earlier daily strategies use daily data, buffering, and market orders. Daily strategies have slower alpha decay and can be executed leisurely; this one cannot.

Options stated by the chapter:

1. Trade separate accounts: simple P&L attribution, but inefficient margin and account costs.
2. Trade in the same account: potentially lower margin and account costs when positions are imperfectly correlated; attribution remains possible if trades are tagged to strategies.
3. Net orders before execution: each morning generate but hold daily-system orders; run intraday mean reversion and net opposing orders; execute unnetted daily orders late in the day. Efficient but operationally complex and makes profitability attribution harder.
4. Reserve selected instruments for mean reversion and leave others to daily systems. Select for lowest risk-adjusted commission cost and acceptable minimum capital, not merely because an asset class had superior in-sample results. With Strategy 25 dynamic optimisation, impose zero-position constraints on instruments reserved for mean reversion.

## Warnings and conclusion

- The strategy can hold losing positions and "catch falling knives" as price continues against it; the author urges extreme caution.
- Negative skew and poor lower-tail measures are an expected property: steady profits can be punctuated by large losses.
- Its relatively favourable average drawdown does not make the tail-risk profile benign.
- The next chapter is explicitly presented as a way to make it safer and improve performance while retaining much of its diversifying quality.

## Glossary

- **Alpha decay:** how quickly a strategy’s signal/opportunity loses value; daily strategies have slower alpha decay than this fast strategy.
- **Back-adjusted futures price:** futures price series adjusted across rolls, used here for the daily equilibrium.
- **Buffering:** trading only when a target deviation is sufficiently large; intentionally not used here.
- **Capacity constraint:** performance deterioration at larger capital because fast orders become clustered/large and influence market behaviour or cannot be filled as assumed.
- **Equilibrium:** five-day EWMA reference price to which price is expected to return.
- **Forecast scalar:** multiplier converting risk-adjusted forecast to the desired forecast scale; 9.3 here.
- **Limit order:** order executed at a specified price or better; assumed not to incur execution spread in the small-trader backtest model.
- **Market order:** immediate execution order; modelled with bid-ask spread cost.
- **Mean reversion:** expectation that price returns toward equilibrium; above equilibrium is bearish, below is bullish.
- **Negative skew:** long series of modest gains with occasional large losses; central risk characteristic here.
- **Risk-adjusted forecast:** raw equilibrium-price deviation divided by daily price volatility.
- **Turnover:** frequency/amount of trading, used in the cost/speed screen.

## Explicit chapter connections

- **Strategy 9:** all unspecified trading-plan stages are identical; it is also the comparison trend strategy and source of the standard position-sizing framework.
- **Strategy 10:** carry comparison in Table 131.
- **Strategy 22:** slow, multi-year value mean reversion used in the time-scale discussion.
- **Strategy 25:** dynamic optimisation can reserve instruments for fast mean reversion through zero-position constraints.
- **Next chapter (Strategy 27):** promised improvement to safety/performance while retaining diversification; no details are supplied here.
