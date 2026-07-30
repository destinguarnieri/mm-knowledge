# Strategy Five: Slow Trend Following, Long Only

## Purpose and central argument

Strategy Five adds a slow long-only trend filter to Strategy Four's dynamically risk-scaled, long-only futures portfolio. Its premise is simple: hold a long position only while the instrument is in an established long-term uptrend; otherwise hold no position. The intended benefit is avoiding instruments that are temporarily or persistently falling. The trade-off is that the strategy cannot profit from a downtrend because it does not short.

The chapter uses a 64/256-business-day exponentially weighted moving-average crossover (EWMAC) as the trend filter. The author argues that, while results depend on the comparison and portfolio level, the filter can materially reduce drawdowns and improve aggregated-portfolio risk-adjusted performance. Dynamic resizing is preferred over keeping a fixed position after entry.

## Strategy definition

> Buy and hold a portfolio of one or more instruments when they have been in a long uptrend, each with positions scaled for a variable risk estimate.

All elements other than the trend filter are identical to Strategy Four. The chapter describes Strategy Four as a portfolio of sub-strategies, each trading Strategy Three for a different instrument.

## Inputs, notation, and units

| Symbol / term | Meaning in this chapter | Units / conditions |
|---|---|---|
| \(p_t\) | Back-adjusted futures price at time \(t\) | Price units; use back-adjusted prices for the trend calculation |
| \(N\) | EWMA span in business days | 64 or 256 days for the specified slow filter |
| \(\lambda\) | EWMA decay/weight parameter | Dimensionless; derived from span \(N\) |
| \(\operatorname{EWMA}(\lambda)_t\) | Exponentially weighted moving average at \(t\) | Price units |
| \(\operatorname{EWMAC}(64,256)_t\) | 64-span EWMA minus 256-span EWMA | Price units; positive signals uptrend |
| \(N_i\) | Optimal number of contracts for instrument \(i\) | Contracts; then rounded to a tradable number |
| Capital | Current account capital | Account currency |
| IDM | Instrument diversification multiplier | Dimensionless; inherited from Strategy Four |
| \(\mathrm{Weight}_{i,t}\) | Instrument weight at time \(t\) | Dimensionless |
| \(\tau\) | Risk target | Annualised risk target; e.g. 20% in the S&P 500 example |
| \(\mathrm{Multiplier}_i\) | Futures contract multiplier | Contract-specific value per price point |
| \(\mathrm{Price}_{i,t}\) | Current futures price | Price units |
| \(\mathrm{FX}_{i,t}\) | Exchange-rate conversion factor | Account-currency conversion factor |
| \(\sigma_{\%,i,t}\) | Estimated annualised percentage standard deviation | Percentage/decimal; variable risk estimate used in sizing |
| \(\sigma_p\) | Daily standard deviation calculated from price differences | Price units per day; used for historical cost adjustment, not \(\sigma_\%\) |

## Trend identification

### Initial simple-moving-average idea

The chapter first introduces a 256-business-day (approximately 12-month) simple moving average (SMA):

\[
\operatorname{MA}(256)_t = \frac{p_{t-255}+p_{t-254}+\cdots+p_{t-1}+p_t}{256}.
\]

If \(p_t\) is above this average, the market is called an uptrend. On the S&P 500 micro future this identifies broad bear markets, but it switches too frequently in short-lived disruptions: from October 2018 through March 2019, the indicator changes the long/not-long decision 14 times.

The smoother two-average version computes:

\[
\operatorname{MA}(64)_t = \frac{p_{t-63}+p_{t-62}+\cdots+p_{t-1}+p_t}{64},
\]

and goes or remains long when

\[
\operatorname{MA}(64)_t > \operatorname{MA}(256)_t.
\]

In this SMA crossover (MAC), the faster 64-day average crossing below the slower 256-day average closes the long. For example, the S&P 500 chart indicates a close in late 2000 and a re-entry in mid-2003. The author considers MAC adequate for slow trends, but says it produces too many short-lived reversals for faster trends.

### Why exponential weighting

An SMA gives every observation in its window equal weight. Therefore, when a large historical return exits the window, the average can shift abruptly; shorter windows amplify this issue because each day has more weight. An EWMA puts greater weight on recent prices and reduces an older large move gradually, rather than dropping it on one day.

The general EWMA is:

\[
\operatorname{EWMA}(\lambda)_t = \lambda p_t + \lambda(1-\lambda)p_{t-1} + \lambda(1-\lambda)^2p_{t-2}+\cdots.
\]

For a span of \(N\) days:

\[
\lambda = \frac{2}{N+1}.
\]

A higher \(\lambda\) behaves like a shorter SMA window: it assigns more weight to recent prices. The term *span* follows the Pandas implementation of exponential weighting.

### Specified slow EWMAC

The required slow filter uses back-adjusted prices:

\[
\operatorname{EWMA}(64)_t = 0.031p_t + 0.031(1-0.031)p_{t-1}+0.031(1-0.031)^2p_{t-2}+\cdots
\]

\[
\operatorname{EWMA}(256)_t = 0.0078p_t + 0.0078(1-0.0078)p_{t-1}+0.0078(1-0.0078)^2p_{t-2}+\cdots
\]

\[
\operatorname{EWMAC}(64,256)_t = \operatorname{EWMA}(64)_t - \operatorname{EWMA}(256)_t.
\]

**Decision rule:** go/stay long if \(\operatorname{EWMAC}(64,256)_t>0\), equivalently if the 64-span EWMA is above the 256-span EWMA. Otherwise remain flat (or close any existing long).

The cited 0.031 and 0.0078 values are approximations to the spans' corresponding \(\lambda\) values. The author reports that EWMAC outperforms corresponding MAC in his analysis, especially for fast filters.

### Parameter constraints and caveats

- The shorter/longer moving-average-length ratio need not be exact. The author's research says ratios from 2 to 6 produce statistically indistinguishable results on real and artificial data; a too-short fast average causes frequent reversals, while a too-long one reacts slowly.
- The chapter uses 64/256 because 256 is \(2^8\), creating a powers-of-two speed series: 64/256, 32/128, 16/64, 8/32, and so on.
- A 64-day EWMA is not exactly equivalent to a 64-day SMA: an EWMA span of 92 days has nearly the same half-life as a 64-day SMA. The author keeps powers-of-two spans for convenience and says the 64-span and 92-span versions are highly correlated with very similar performance.
- Back-adjusted prices avoid discontinuities at futures rolls. This matters more for shorter trends. A stated consequence is that an instrument with positive carry is more likely to appear in an uptrend; ramifications are deferred to later in the book.
- The stated superiority claim is analysis-specific, not a universal proof. A footnote gives a later fast, long/short example (Strategy Eight) where matched-half-life EWMAC doubles Sharpe ratio and reduces both costs and turnover by one third relative to MAC.

## Position management and trading procedure

The trend filter acts as an on/off switch on the daily dynamically sized position from Strategy Four. The unrounded optimal contract count is:

\[
N_i = \frac{\mathrm{Capital}\times\mathrm{IDM}\times\mathrm{Weight}_{i,t}\times\tau}
{\mathrm{Multiplier}_i\times\mathrm{Price}_{i,t}\times\mathrm{FX}_{i,t}\times\sigma_{\%,i,t}}.
\]

The strategy uses the current rounded value of \(N_i\).

### Daily algorithm

1. Use the back-adjusted price history to calculate the 64-business-day-span and 256-business-day-span EWMAs.
2. Determine trend state: uptrend if \(\operatorname{EWMA}(64)>\operatorname{EWMA}(256)\); otherwise downtrend.
3. If in an uptrend, calculate the current optimal long position from the formula above, using current capital, price, FX rate, and \(\sigma_\%\); trade as required to reach it.
4. While the uptrend persists, resize day by day as the optimal position changes. The principal driver is \(\sigma_\%\), with price, FX, and capital also affecting the size.
5. Roll futures contracts as required.
6. If the trend is down, set the optimal position to zero: close any long and do not reopen until an uptrend is re-established.

## Figures and what they communicate

| Item | Description / takeaway |
|---|---|
| Figure 23 — 12-month moving average on S&P 500 price | Overlays the 12-month average on roughly 20 years of S&P 500 micro-future prices. It is mostly an uptrend, except the early 2000s and 2008–09, with shorter bear markets including March 2020. |
| Figure 24 — Two moving averages on S&P 500 | Shows fast and slow averages without raw price. A late-2000 fast-below-slow crossover closes the position; a mid-2003 crossover reopens it. Severe bear markets become clear and the strategy changes position less than once per year, though some uncertain short periods remain. |
| Figure 25 — S&P 500 positions under Strategy Five | With $100,000 capital and a 20% annualised risk target, positions largely follow unfiltered Strategy Four's positions, except that downward trends temporarily close the trade. |
| Figure 26 — Cumulative Jumbo-portfolio performance with/without filter | The filter avoids most of the early-1980s deep drawdown by reducing positions in falling markets. The chapter notes that Strategy Five substantially undershoots a 20% expected risk target because it spends considerable time flat; levering it to 20% would make it look better in this comparison. |

## Historical trading costs in backtests

For Strategies One through Four, risk-adjusted costs are presented as a sufficient approximation in historical backtests: estimate total turnover of an average position, add roll trades, and multiply by risk-adjusted cost per trade. That shortcut is unsuitable here because Strategy Five is sometimes flat and produces an unusual trade pattern—large entry/exit trades at trend switches plus many small resizing trades.

Instead, deduct an account-currency cost for every contract traded in the backtest. Adjust the current per-contract cost to the relevant historical period with daily price-difference volatility:

\[
\text{Historical trading cost} = \text{Current cost}\times
\frac{\text{Historical }\sigma_p}{\text{Current }\sigma_p}.
\]

Estimate \(\sigma_p\) using the usual exponentially weighted standard-deviation estimator previously used since Strategy Three, applied to price differences. Do **not** use annualised percentage volatility \(\sigma_\%\) for this adjustment.

### Worked cost example: S&P 500 micro future

- Current cost: $0.875 per contract, including commission and spread.
- Current assumed S&P 500 price: 4,500; annualised standard deviation: 16%. Daily price-standard-deviation estimate: \(4500\times16\%\div16=45\).
- October 1990 assumed price: about 500; annualised standard deviation: about 10%. Daily price-standard-deviation estimate: \(500\times10\%\div16=3.125\).
- Historical per-contract cost: \($0.875\times(3.125\div45)=\$0.061\).

If annualised percentage volatility is unchanged, this preserves trading cost as a percentage of notional contract value. If it changes, cost changes with volatility, matching the earlier constant-risk-adjusted-cost assumption. A common alternative normalises only for price changes, effectively holding costs at a fixed percentage of notional value. The chapter considers that probably acceptable for commissions but not for spreads, which tend to widen in more volatile markets.

**Warning:** all historical-cost calculations are approximations. Historical retail trading costs were likely higher; accurate historical cost data are unavailable. The author recommends particular distrust of backtested costs for high-turnover strategies.

## Performance evidence

### Table 18 — S&P 500 micro future

Comparison uses Strategy Four without a filter versus Strategy Five with it. The filter reduces risk and average drawdown but also lowers return; turnover rises because of lower average position size and added entry/exit transactions. Despite that, average annual costs are unchanged because the filtered strategy has no-trading periods.

| Measure | Strategy Four (no trend filter) | Strategy Five (trend filter) |
|---|---:|---:|
| Mean annual return | 12.1% | 9.6% |
| Costs | −0.06% | −0.06% |
| Average drawdown | −18.8% | −12.8% |
| Standard deviation | 22.8% | 19.5% |
| Sharpe ratio | 0.54 | 0.49 |
| Turnover | 2.34 | 6.4 |
| Skew | −0.68 | −0.57 |
| Lower tail | 1.76 | 1.85 |
| Upper tail | 1.21 | 1.18 |

The author cautions that a continuously invested strategy and a strategy that is sometimes flat have materially different return profiles; simple means and Sharpe ratios alone are difficult bases for declaring a winner. Selection ultimately depends on preferences.

### Table 19 — Median instrument across the data set

| Measure | Strategy Four (no trend filter) | Strategy Five (trend filter) |
|---|---:|---:|
| Mean annual return | 6.9% | 5.6% |
| Costs | −0.30% | −0.23% |
| Average drawdown | −18.7% | −20.2% |
| Standard deviation | 20.9% | 17.2% |
| Sharpe ratio | 0.32 | 0.32 |
| Turnover | 2.7 | 5.8 |
| Skew | −0.09 | −0.07 |
| Lower tail | 1.56 | 1.60 |
| Upper tail | 1.29 | 1.26 |

Across instruments, the change is less dramatic than in the S&P 500 alone. The author states that dynamically sized Strategy Five has identical risk-adjusted performance to Strategy Three without a filter; because it is invested only part of the time, both return and risk are a little lower.

### Table 20 — Aggregated Jumbo portfolio

The Jumbo backtest aggregates 102 instruments using $50 million notional capital so that no instrument has a minimum-capital problem. Unlike the median-instrument result, adding the filter improves both risk and return; the author notes that tails look somewhat worse, while average drawdown falls by about two-thirds.

| Measure | Strategy Four (no trend filter) | Strategy Five (trend filter) |
|---|---:|---:|
| Mean annual return | 15.4% | 16.4% |
| Costs | −0.8% | −0.7% |
| Average drawdown | −24.7% | −10.4% |
| Standard deviation | 18.2% | 14.8% |
| Sharpe ratio | 0.85 | 1.11 |
| Turnover | 20.7 | 24.1 |
| Skew | −0.04 | 0.22 |
| Lower tail | 1.44 | 1.64 |
| Upper tail | 1.24 | 1.39 |

## Dynamic versus static position management

### Definitions

- **Dynamic method:** after opening, continually adjust the position to maintain the current risk-scaled optimal size.
- **Static method:** once an uptrend opens a position, keep the same number of contracts (apart from rolling) until the trend turns down; then close. At the next uptrend, calculate a new size from then-current volatility.
- **Intermediate variation:** resize on rolls. Its performance is expected to lie between static and dynamic.

### Author's comparison

| Topic | Static versus dynamic finding |
|---|---|
| Turnover and costs | Static is plainly lower, because there is no trading after entry. However, the author says average-return improvements from dynamic sizing are usually many multiples of its added costs. |
| Average return, standard deviation, Sharpe ratio | For both average instruments and aggregated Jumbo portfolios, dynamic is almost always a clear winner on these measures. Static standard deviation can be much higher. |
| Leverage | Positions are identically sized at inception of a static trade, when the filter changes sign. Afterwards dynamic strategies use less leverage on average because they cut positions as risk rises. The author does not advocate adding leverage to dynamic strategies merely to match static risk, saying unlevered dynamic sizing does a good job of meeting the risk target. |
| Average drawdown and lower tail | The author's analysis suggests dynamic is nearly always better. |
| Upper tail and skew | Static sometimes improves these, especially in aggregated statistics, because an unreduced position captures more of a sharp winning spike. The same mechanism makes fat left tails more likely. Improvements are neither universal nor significant enough, in the author's view, to justify static sizing. |

One cited distortion is a large one-off static-strategy return spike from the Hunt brothers' 1980 attempt to corner the silver market, which affected the metals complex and severely distorted the aggregate strategy's risk profile. The author says static skew looks somewhat more favorable when measured trade-by-trade rather than using daily returns, but does not find that persuasive.

## Practical implications, boundaries, and warnings

- This is **long-only** trend following. In a falling market it can avoid losses, but it cannot obtain the full trend-following benefit available to a futures trader who can also short.
- Trend signals can reverse temporarily; even the slow crossover has a few short-lived uncertain periods.
- The strategy's realised risk can be below its nominal target because it is frequently flat. Do not compare it mechanically with an always-invested strategy without accounting for the different exposure profile.
- Use dynamic sizing when following the author's recommendation; fixed contract counts preserve exposure through volatility spikes and can worsen standard deviation, drawdown, and lower-tail behavior.
- For historical simulation, cost every trade rather than applying an average-turnover shortcut. Treat modeled historical costs cautiously, particularly at high turnover.

## Conclusion and takeaways

1. A 64/256 EWMAC on back-adjusted prices provides the chapter's slow uptrend filter.
2. When the fast EWMA exceeds the slow EWMA, hold the dynamically risk-scaled long; otherwise hold zero.
3. Exponential weighting avoids abrupt changes caused by observations leaving an SMA window and is said to be especially beneficial for faster filters.
4. On a single S&P 500 micro future, filtering lowered return and risk; across the median instrument it preserved Sharpe ratio while lowering return/risk; in the 102-instrument Jumbo portfolio it improved return, risk, drawdown, and Sharpe ratio in the reported test.
5. The author prefers dynamically resizing positions over static sizing despite dynamic's higher trading activity and costs.
6. The next chapter extends the idea by going long and short, which the author says adds performance potential unavailable to a long-only filter.

## Glossary

- **Back-adjusted futures price:** Futures price series adjusted to be smooth across rolls; used for trend calculations.
- **Dynamic position sizing:** Continuous resizing of an open position to its current risk-scaled optimum.
- **EWMA:** Exponentially weighted moving average, with larger weight assigned to recent observations.
- **EWMAC:** Exponentially weighted moving-average crossover; here, fast EWMA minus slow EWMA.
- **MAC:** Simple moving-average crossover.
- **Positive carry:** Mentioned as making an instrument more likely to appear in an uptrend when back-adjusted prices are used; detailed implications are deferred.
- **Risk-adjusted cost:** Trading-cost concept intended to remain comparable across risk/volatility conditions.
- **Static position management:** Hold the entry contract count unchanged until the trend reverses, apart from rolls.
- **Trend filter:** Rule that enables a long position in an uptrend and disables it in a downtrend.
- **Turnover:** Trading activity associated with adjusting, opening, closing, and rolling positions.

## Explicit connections to other chapters / strategies

- **Strategy Three:** supplies the risk-adjusted cost framework and the usual EW standard-deviation estimate; Strategy Four is effectively a portfolio of Strategy Three instances.
- **Strategy Four:** supplies all non-filter elements and the dynamic position-sizing equation. Strategy Five is Strategy Four plus an on/off trend switch.
- **Strategy Eight:** cited as a fast long/short trend-filter example in which EWMAC versus matched-half-life MAC reportedly doubles Sharpe ratio while reducing costs and turnover.
- **Next chapter (Strategy Six):** adds shorting to capture downtrends as well as avoid them.

## Source completeness note

All equations, rules, tables, captions, examples, and footnotes contained in the supplied Strategy Five XHTML were extracted. Figure images were interpreted only from their captions and accompanying text; no numerical chart values beyond those supplied in text/tables are inferred.
