# Strategy Six: Slow Trend Following, Long and Short

## Purpose and central argument

Strategy six extends the prior slow trend filter from a long-or-flat rule into an always-invested long/short rule. It holds a volatility-scaled long position during a sustained uptrend and a volatility-scaled short position during a sustained downtrend. The chapter argues that this makes it possible to profit in falling markets and can create a substantial diversification benefit at the portfolio level, even though the average single-instrument historical result is weaker than a long-only benchmark.

> **Strategy statement:** Trade one or more instruments with positions scaled for a variable risk estimate; go long after a long uptrend and short after a downtrend.

The chapter treats trend-following return itself as a risk premium, rather than merely the long-only risk premia emphasized through strategy four.

## Rule and implementation

### Inputs and slow trend filter

Use the **back-adjusted price** \(p\) to calculate two exponentially weighted moving averages (EWMAs):

\[
\operatorname{EWMA}(N=64,\lambda=0.031)_t
=0.031p_t+0.031(1-0.031)p_{t-1}+0.031(1-0.031)^2p_{t-2}+\ldots
\]

\[
\operatorname{EWMA}(N=256,\lambda=0.0078)_t
=0.0078p_t+0.0078(1-0.0078)p_{t-1}+0.0078(1-0.0078)^2p_{t-2}+\ldots
\]

\[
\operatorname{EWMAC}(64,256)_t=
\operatorname{EWMA}(N=64)_t-\operatorname{EWMA}(N=256)_t
\]

| Symbol / term | Meaning supplied in the chapter | Domain / condition |
|---|---|---|
| \(p_t\) | Back-adjusted price at time \(t\) | Price series; business-day observation in the plan |
| \(t\) | Time index | Current date/observation |
| \(N\) | EWMA span | 64 or 256 business days |
| \(\lambda\) | EWMA decay parameter | 0.031 for 64-day EWMA; 0.0078 for 256-day EWMA |
| EWMAC(64,256) | Difference between the fast and slow EWMAs | Trend signal |

**Direction rule:**

- Go long if \(\operatorname{EWMAC}(64,256)>0\), equivalently EWMA(64) is above EWMA(256).
- Go short if \(\operatorname{EWMAC}(64,256)<0\), equivalently EWMA(64) is below EWMA(256).
- If the two moving averages are exactly equal, hold no position (footnote 104).

### Position sizing

The position is recalculated daily at the current optimal level:

\[
N_{i,t}=
\frac{\operatorname{Sign}(\mathrm{trend})_t\times \mathrm{Capital}\times \mathrm{IDM}\times \mathrm{Weight}_i\times \tau}
{\mathrm{Multiplier}_i\times \mathrm{Price}_{i,t}\times \mathrm{FX}_{i,t}\times \sigma_{\%,i,t}}
\]

| Symbol / term | Meaning supplied in the chapter | Notes / condition |
|---|---|---|
| \(N_{i,t}\) | Number of contracts for instrument \(i\) at time \(t\) | Rounded current optimal value in the trading plan |
| \(\operatorname{Sign}(\mathrm{trend})_t\) | Trend direction | Positive = long; negative = short; zero when averages equal |
| Capital | Capital | Updated when determining the optimal position |
| IDM | Instrument diversification multiplier | Chapter later states it is calculated from sub-strategy correlations and rises as diversification rises |
| \(\mathrm{Weight}_i\) | Weight of instrument \(i\) | Not further defined in this chapter |
| \(\tau\) | Target-risk term | Label/specific units are not further defined in this chapter |
| \(\mathrm{Multiplier}_i\) | Contract multiplier for instrument \(i\) | Used in denominator |
| \(\mathrm{Price}_{i,t}\) | Price | Updated daily |
| \(\mathrm{FX}_{i,t}\) | FX value | Updated daily |
| \(\sigma_{\%,i,t}\) | Standard-deviation estimate in percent | Updated daily; variable risk estimate |

**Execution procedure:**

1. Calculate the two EWMAs and determine the trend sign.
2. Update capital, price, FX, and the standard-deviation estimate; calculate the optimal position and round it to contracts.
3. In an uptrend, hold the positive/long position; in a downtrend, hold the same risk-scaled magnitude short.
4. Trade as needed each day to reach the updated optimum, and roll as required.
5. Keep the position open, making small daily adjustments as price, FX, and risk change. When the filter reverses, close/reverse into the opposite-direction position sized from the then-current \(N\).

### Figure 27 — S&P 500 micro-futures position sizing

The chart plots the strategy-six position over roughly 1983–2021. It is positive in bullish regimes and negative in bearish regimes. The chapter says the absolute size is effectively identical to strategy three’s volatility-targeted position; the key difference is the sign supplied by the trend filter. Large early swings and negative holdings demonstrate that the strategy can reverse, while later magnitude changes show continuous risk/price-based resizing.

## Relationship to stop losses

A conventional stop loss closes a long after a specified retracement from a high, or a short after a specified retracement from a low. Properly calibrated, it can close a position at roughly the same time that this trend filter recognizes a reversal.

The author prefers one trend rule for both entry and exit because it is simpler and automatically adapts position size as trends strengthen or weaken. The author reports that an earlier book’s backtests found slightly better performance from replacing a separate stop loss with a single opening/closing rule.

An optional stop-loss variant is permitted:

1. Enter in the direction of the trend-filter sign.
2. Exit when the stop loss is hit.
3. Re-enter only after the trend filter reverses—immediately or after days/weeks.

**Warnings:** A stop that is too tight exits before a trend is exhausted; one too loose holds after reversal. Stops should scale with current instrument volatility. The chapter refers readers elsewhere for calibration to a particular trend length; it does not give that calibration here.

## Backtest results

### Table 21 — Average instrument: long-only benchmarks vs. long/short filter

The strategy profiles differ: strategy four is always long, strategy five is long or flat, and strategy six is always long or short. Thus raw return and standard deviation are hard to compare across all three; the chapter regards strategy four and six as the more directly comparable pair because both always have positions.

| Statistic | Strategy 4: no trend filter, long only | Strategy 5: trend filter, long only | Strategy 6: trend filter, long/short |
|---|---:|---:|---:|
| Mean annual return | 6.9% | 5.6% | 4.8% |
| Costs | −0.3% | −0.23% | −0.34% |
| Average drawdown | −18.7% | −20.2% | −25.4% |
| Standard deviation | 20.9% | 17.2% | 20.9% |
| Sharpe ratio | 0.32 | 0.32 | 0.21 |
| Turnover | 2.7 | 5.8 | 7.0 |
| Skew | −0.09 | −0.07 | −0.01 |
| Lower tail | 1.56 | 1.60 | 1.53 |
| Upper tail | 1.29 | 1.26 | 1.31 |

For the average instrument, permitting shorts mostly harms historical return, consistent with the data set’s generally rising instruments. Since strategy six always holds a position, standard deviation is almost identical to strategy four rather than lower, and drawdowns are worse. It does modestly better in the distribution tails.

### Tables 22–23 — Median strategy-six performance by asset class

| Statistic | Equity | Vol | FX | Bond |
|---|---:|---:|---:|---:|
| Mean annual return | 3.0% | −0.5% | 3.4% | 5.6% |
| Costs | −0.3% | −1.3% | −0.4% | −0.4% |
| Average drawdown | −20.1% | −31.7% | −37.9% | −20.5% |
| Standard deviation | 21.1% | 21.8% | 20.5% | 20.7% |
| Sharpe ratio | 0.15 | −0.02 | 0.17 | 0.27 |
| Turnover | 7.2 | 6.5 | 6.7 | 6.9 |
| Skew | −0.19 | −2.15 | −0.15 | −0.01 |
| Lower tail | 1.65 | 2.07 | 1.54 | 1.51 |
| Upper tail | 1.21 | 1.37 | 1.37 | 1.30 |

| Statistic | Metals | Energy | Ags |
|---|---:|---:|---:|
| Mean annual return | 12.3% | 5.1% | 4.3% |
| Costs | −0.4% | −0.4% | −0.3% |
| Average drawdown | −20.8% | −37.5% | −38.1% |
| Standard deviation | 22.1% | 21.7% | 20.7% |
| Sharpe ratio | 0.53 | 0.26 | 0.21 |
| Turnover | 6.8 | 6.9 | 7.1 |
| Skew | 0.28 | 0.10 | 0.12 |
| Lower tail | 1.67 | 1.43 | 1.40 |
| Upper tail | 1.56 | 1.31 | 1.38 |

The author’s reading of these results:

- Standard deviations and turnover are effectively identical across asset classes, implying consistent risk targeting and a consistent turnover profile.
- Costs differ slightly because per-trade costs differ by instrument.
- Drawdowns partially converge across asset classes: they worsen where strategy four had smaller drawdowns (for example bonds) and improve where strategy three had high drawdowns (for example volatility).
- Sharpe ratios improve except in equities and bonds, whose historical long-only performance was exceptionally strong.
- Volatility assets improve strikingly because the rule changes a persistent long-vol exposure into a mostly short one. The major exception was the 2020 COVID-19 selloff, when a short-vol position was caught as volatility spiked.
- Average skew and lower tails improve except for volatility assets. The chapter attributes their negative skew to replacing a long positive-skew position with a long/short position biased short.

### Table 24 — Aggregate 102-instrument Jumbo portfolio

The Jumbo portfolio comprises 102 instruments and uses $50 million notional capital so minimum-capital issues do not affect any instrument (footnote 105).

| Statistic | Strategy 4: no trend filter | Strategy 5: long-only trend filter | Strategy 6: long/short trend filter |
|---|---:|---:|---:|
| Mean annual return | 15.4% | 16.4% | 18.5% |
| Costs | −0.8% | −0.7% | −1.1% |
| Average drawdown | −24.7% | −10.4% | −10.7% |
| Standard deviation | 18.2% | 14.8% | 18.4% |
| Sharpe ratio | 0.85 | 1.11 | 1.01 |
| Turnover | 20.7 | 24.1 | 31.6 |
| Skew | −0.04 | 0.22 | 0.16 |
| Lower tail | 1.44 | 1.64 | 1.48 |
| Upper tail | 1.24 | 1.39 | 1.30 |

At the aggregate level, strategy six has higher average return than strategies four and five. Relative to strategy four, its Sharpe ratio, skew, and tail ratios are better; relative to strategy five, its risk and costs are higher because it is always invested. Its turnover and costs exceed strategy four because filter reversals add large trades in addition to daily resizing trades.

### Figure 28 — Cumulated returns, strategy six vs. strategy four

The chart plots cumulative percentage returns for the Jumbo portfolio. The long/short-filter series ends materially above the no-filter benchmark. The chapter highlights the early-1980s period: strategy four suffered a severe drawdown when commodity and FX markets—then much of the portfolio—fell, whereas strategy six could short those falling instruments and prosper.

## Why the aggregate improves: diversification

There is a superficially contradictory pattern when comparing strategy six with strategy four: average individual return, drawdown, and Sharpe ratio are worse (table 21), but all three are better for the aggregate portfolio (table 24). Different available history lengths can contribute: equal-weighted median instrument results weight every instrument equally, while aggregate returns effectively weight instruments with longer histories more. The author investigated this and found it explains only a small part of the difference.

The primary explanation is greater diversification in the long/short portfolio. Even two highly correlated markets can have different trend signals and opposing position signs. The chapter’s example is 2020: S&P 500’s signal turned negative while more lockdown-resilient NASDAQ technology stocks remained positive; after the crash, the system was short S&P 500 and long NASDAQ for many weeks. Their subsystem return correlation was therefore negative over that period, reducing average correlation over time.

The IDM measures diversification from sub-strategy correlations: lower average correlation means higher IDM. The Jumbo IDM is **2.46** for long-only strategy four and **2.89** for dynamic long/short strategy six. The author cautions that the performance improvement is not fully explained by this difference, so linear correlation is an imperfect measure of the diversification supplied by trend filters or other trading rules. The full Jumbo portfolio is limited to institutional traders or very wealthy individuals, but the chapter expects a reasonably diversified smaller portfolio to capture most of the available benefit.

## Formal relative-performance assessment

The chapter argues that long-only strategy four has been flattered by unusually good historic equity and bond performance since the late 1970s, tied to secular declines in inflation and interest rates and a repricing of equity risk. It gives US equity P/E as an example, rising from about 10 in the mid-1970s to nearly 40 when the chapter was written. Therefore, raw historical comparison is not the preferred assessment for future relative value.

Using monthly aggregate returns, regress strategy-six return \(y\) on strategy-four return \(x\):

\[
y_t=\alpha+\beta x_t+\epsilon_t
\]

| Symbol | Meaning supplied in the chapter |
|---|---|
| \(y_t\) | Monthly aggregate return of Jumbo portfolio strategy six |
| \(x_t\) | Monthly return of benchmark strategy four |
| \(\alpha\) | Regression alpha, estimated by minimizing squared errors |
| \(\beta\) | Regression beta; indicates return co-movement; a positive value indicates positive correlation |
| \(\epsilon_t\) | Regression error; squared errors are minimized |

Results: \(\beta=+0.34\), expected because the average instrument was in an uptrend for much of the backtest. \(\alpha=1.13\%\) per month and is highly statistically significant. The author interprets this as over 13% annually of additional returns beyond the benchmark. The reported t-statistic is **9.6**; the footnote states that about 2 is normally regarded as statistically significant, and describes 9.6 as, in theory, less than a one-in-a-zillion chance that the estimated alpha is truly negative. Daily and weekly regressions fit more poorly, but their estimated alpha is even higher (footnote 106).

## Constraints, caveats, and edge cases

- This is a historical backtest, not a guarantee. The author attributes the mixed individual-instrument outcome largely to a scarcity of falling markets since the early 1980s.
- Long-only outcomes in equities and bonds may not repeat, because their historical returns reflected secular macro trends and equity-risk repricing.
- Strategy six remains exposed at all times except the exact-EWMA tie case. It does not gain the reduced risk from strategy five’s flat periods.
- Reversals increase turnover and trading costs.
- Short-vol exposure can be severely harmed by a volatility spike; 2020 is the named example.
- Risk scaling controls position magnitude, not the correctness of the trend signal or the severity of a sudden reversal.
- The chapter does not specify the precise calculation of \(\tau\), \(\mathrm{Weight}_i\), or IDM beyond the information stated above; it directs that all other elements are identical to strategy four.

## Conclusion and links to other chapters

Long/short trend following allows profits in falling markets. Its historical success is qualified at the single-instrument level, but the author argues it is materially stronger after correcting for the unusually favorable long-only backdrop via regression, and particularly valuable in a diversified portfolio.

Explicit chapter connections:

- **Strategy three:** strategy-six absolute position magnitude is like strategy three’s volatility-targeted position; tables 22–23 are compared with strategy-three tables 10–11.
- **Strategy four:** all other trading-plan elements are identical; it is the always-long benchmark used in tables 21 and 24 and in the regression.
- **Strategy five:** supplies the original slow trend filter; unlike strategy five’s long-or-flat posture, strategy six is long or short.
- **Strategy seven:** introduces quantified forecasts of future risk-adjusted returns, used to size positions and combine disparate rules. All remaining strategies use forecasts.

## Glossary

- **Back-adjusted price:** the price series specified as the input to the EWMAs.
- **EWMA:** exponentially weighted moving average.
- **EWMAC:** difference between fast and slow EWMAs.
- **Slow trend filter:** 64/256 business-day EWMAC direction rule.
- **Trend reversal:** change of filter sign, triggering a reversal of position direction.
- **Variable risk estimate / \(\sigma_\%\):** current standard-deviation estimate used in sizing.
- **IDM (instrument diversification multiplier):** diversification measure calculated from sub-strategy correlations.
- **Turnover:** reported trading activity measure; units are not defined in this chapter.
- **Sharpe ratio (SR):** risk-adjusted performance measure used in the reported tables; formula is not given here.
- **Skew, lower tail, upper tail:** distribution statistics reported in the tables; exact formulas are not supplied in this chapter.
- **Alpha / beta:** regression intercept/excess component and co-movement coefficient, respectively.
