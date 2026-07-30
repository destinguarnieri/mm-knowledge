# Strategy seven: Slow trend following with trend strength

## Purpose and central argument

Strategy seven extends the slow long/short trend filter of strategy six. Rather than holding the same risk-adjusted position whenever the fast EWMA is above (or below) the slow EWMA, it estimates **trend strength** and scales the position accordingly. The chapter calls that estimate a **forecast**: a value proportional to expected risk-adjusted return. It argues that a mature, low-volatility trend deserves more exposure than a newly forming, weak, or broken trend.

The strategy trades one or more instruments using a variable risk estimate and a variable forecast. A positive forecast produces a long position; a negative forecast produces a short position. Absolute forecast size controls position magnitude, subject to a cap of 20.

## Starting problem: sign alone loses information

Figure 29 plots the S&P 500 micro future with the 64-day fast and 256-day slow EWMAs around the 2020 COVID-19 crash. With the preceding slow trend-filter rule, the system is long with the same expected risk on all of these dates because fast EWMA is above slow EWMA:

- **1 April 2019:** price has recently moved sideways and an uptrend is beginning.
- **25 January 2020:** a solid upward trend has persisted for months.
- **19 March 2020:** the index has already fallen 1,000 points; the WHO has declared a pandemic, there are several thousand US cases, and a US national emergency has been declared. The prior rule does not close its long position until the next day.

The author notes that a faster crossover could have gone short before 20 March (addressed in the next strategy), but the more subtle issue is that the above states should not carry equal exposure. The January trend is strong; the April trend is new; the March long signal is nearly exhausted.

## Core concepts and definitions

### EWMA crossover / EWMAC

The chapter's slow trend rule is **EWMAC(64,256)**: the 64-day fast exponentially weighted moving average less the 256-day slow EWMA.

\[
\operatorname{EWMAC}(64,256) = \operatorname{EWMA}(64) - \operatorname{EWMA}(256)
\]

The raw crossover is positive in an uptrend and negative in a downtrend. By itself it is not comparable across history or instruments:

- Prices rise over time; for the S&P 500 a 10-point gap at about 400 in 1985 is not comparable with a 100-point gap when the index exceeds 4,000.
- Volatility changes through time; a 100-point gap in early 2020 was less remarkable when the index was moving more than 100 points daily.

### Forecast and trading rule

A **forecast** is formally defined as a value *proportional to an expected risk-adjusted return*, hence proportional to an expected Sharpe ratio. A **trading rule** is anything that produces a forecast.

Risk-adjusting a forecast makes values comparable through time and across instruments, allowing pooled results when fitting/calibrating strategies. Forecast sign gives direction; forecast magnitude gives conviction and scales exposure.

### Daily price volatility

For a crossover expressed in price points, use \(\sigma_p\), the standard deviation in **daily price units**, not percentage units or annualised percentage points:

\[
\sigma_p = \frac{\text{Price}\times\sigma_\%}{16}
\]

where \(\sigma_\%\) is annualised percentage risk and 16 is the chapter's annual-to-daily conversion constant. The author says daily versus annualised standard deviation here is less important because it only changes the scale, but uses daily for consistency. A price-unit standard deviation is essential because the numerator is in price points.

## Forecast construction

### 1. Calculate a raw forecast

For an EWMA trend rule:

\[
\text{Raw forecast} = \frac{\text{Fast EWMA} - \text{Slow EWMA}}{\sigma_p}
\]

- Numerator: crossover in price points.
- \(\sigma_p\): daily price standard deviation above, in the same price-unit domain.
- A positive result implies long; a negative result implies short.

### 2. Estimate its average absolute value

Run a backtest, plot the raw forecast through time, and measure its average absolute value. For a more accurate estimate, measure the average for many instruments and average those estimates; risk adjustment makes this pooling valid.

The author prefers estimating this empirically rather than deriving an expected value from return-distribution assumptions, which are usually unrealistic. To avoid in-sample cheating in a backtest, use a purely backward-looking rolling forecast-scalar estimate. The book's reported backtests do that; it supplies fixed scalars for implementation because they are relatively stable over time.

### 3. Scale to a common forecast scale

The target average absolute forecast is 10:

\[
\text{Scaled forecast} = \text{Raw forecast}\times
\frac{10}{\operatorname{Average}(|\text{Raw forecast}|)}
\]

Define the **forecast scalar** as:

\[
\text{Forecast scalar} = \frac{10}{\operatorname{Average}(|\text{Raw forecast}|)}
\]

so:

\[
\text{Scaled forecast} = \text{Raw forecast}\times\text{Forecast scalar}
\]

The chapter states that the estimated scalar for the **EWMAC(16,64)** trading rule is approximately 1.9. It also presents a displayed formula reading

\[
\text{Scaled forecast}=\left[\frac{\operatorname{EWMA}(64)-\operatorname{EWMA}(16)}{\sigma_p}\right]\times1.9.
\]

**Source inconsistency to preserve:** the surrounding discussion and the strategy plan specify EWMAC(64,256), while this displayed formula and its immediately preceding scalar statement specify EWMAC(16,64), and reverse the usual fast-minus-slow order if read literally. The chapter does not reconcile this. Do not assume that 1.9 is the scalar for EWMAC(64,256); use the strategy-plan specification and obtain/verify the correct scalar before implementation.

The author uses average absolute value rather than standard deviation because standard deviation first subtracts the mean. For a forecast with a long/short bias (trend filters often have a long bias because many instruments rose historically), this makes standard deviation smaller relative to average absolute value. The mathematical difference that standard deviation is the square root of average squared value whereas average absolute value averages magnitudes is described as less important.

### Interpretation examples (S&P 500)

- **1 April 2019:** forecast below 5; position is less than half normal.
- **28 January 2020:** forecast about 20; position is twice normal.
- **19 March 2020:** forecast below 1; position is about one-tenth normal and could round to zero unless capital allocated to the instrument is large.

Figure 31 shows EWMAC(64,256) scaled forecasts for the S&P 500. Its realised average absolute value is about 10.5, not exactly 10, because the scalar was estimated across many instruments. With ample history the author expects an individual instrument to be close to target. A single-instrument bull-market sample can be biased; VIX-like forecast distributions can have high kurtosis. These are reasons to estimate scalars across multiple instruments.

## Position sizing

The chapter applies one position-sizing equation across instruments and strategies because forecasts share a common interpretation:

\[
N_i = \frac{\text{Scaled forecast}_{i,t}\times\text{Capital}\times\text{IDM}\times\text{Weight}_i\times\tau}
{10\times\text{Multiplier}_i\times\text{Price}_{i,t}\times\text{FX}_{i,t}\times\sigma_{\%,i,t}}
\]

Variables (using the source's notation):

| Symbol / field | Meaning and applicable units |
|---|---|
| \(N_i\) | Current optimal number of contracts for instrument \(i\), then rounded for trading. Sign determines long/short. |
| \(i\) | Instrument index. |
| \(t\) | Time index; source shows this subscript on forecast, price, FX, and risk fields. |
| Scaled forecast\(_{i,t}\) | Dimensionless common-scale forecast; average absolute target 10. |
| Capital | Trading capital. |
| IDM | Instrument diversification multiplier (defined in earlier strategy material; not redefined in this chapter). |
| Weight\(_i\) | Instrument weight (also inherited from strategy six). |
| \(\tau\) | Risk-target parameter shown in the formula; its definition is inherited from earlier strategies and not restated here. |
| Multiplier\(_i\) | Contract multiplier. |
| Price\(_{i,t}\) | Current instrument price. |
| FX\(_{i,t}\) | Current FX conversion factor. |
| \(\sigma_{\%,i,t}\) | Percentage risk/standard-deviation estimate used by the overall position-sizing rule. |
| 10 | Normalising constant: a forecast of +10 or −10 produces the earlier strategies' average-sized position. |

Thus, forecast > 0 means long and forecast < 0 means short. At absolute forecast 10 the position has ordinary size; below 10 it is smaller and above 10 it is larger. Substituting the scaled-forecast construction makes position proportional to \(1/\sigma_{\%,i,t}^2\), a mean-variance-optimisation familiar result noted by the author.

Figure 32 shows the forecast and contract position from late 2019 through early 2020 for $100,000 capital. The position is tiny in early April, larger by late January, then is cut as both risk rises and forecast falls. The exposure is reduced ahead of the ensuing selloff. Unlike strategies five and six, the strategy does not make one huge reversal trade in late March: it closes gradually as forecast declines over prior weeks.

## Cap forecasts before sizing

Scaled forecasts can reach two or three times their average (20–30), producing positions over three times earlier strategy positions and concentrating risk in high-forecast instruments. The chapter sets the maximum permissible absolute forecast to **20**, so no position exceeds twice normal size:

\[
\text{Capped forecast}_{i,t}=
\max\left(\min(\text{Scaled forecast}_{i,t},+20),-20\right)
\]

Use the same position formula with Capped forecast in place of Scaled forecast:

\[
N_i = \frac{\text{Capped forecast}_{i,t}\times\text{Capital}\times\text{IDM}\times\text{Weight}_i\times\tau}
{10\times\text{Multiplier}_i\times\text{Price}_{i,t}\times\text{FX}_{i,t}\times\sigma_{\%,i,t}}
\]

The author says additional reasons for capping are deferred to Part Two. An explicit practical warning is that large long S&P 500 exposure entering January 2020 was, in hindsight, a bad idea.

## Trading plan / procedure

All elements not listed here are identical to strategy six.

1. Calculate EWMAs using the strategy-six method.
2. Use trading rule **EWMAC(64,256)**.
3. Calculate raw forecast: \((\operatorname{EWMA}(64) - \operatorname{EWMA}(256))/\sigma_p\).
4. Multiply raw forecast by the applicable forecast scalar to obtain the scaled forecast. The visual plan shows 1.9, but see the source inconsistency above.
5. Cap scaled forecast to the closed interval \([-20,+20]\).
6. Calculate the current optimal contract position using the capped-forecast equation and round it.
7. Update forecast, capital, price, FX, and standard-deviation estimates; trade as needed to reach the optimal long or short position; roll contracts as required.

## Evidence and backtest evaluation

### Table 25 — median/average instrument comparison

The source labels Table 25 “Performance of average instrument, long only, trend filter and with forecasts,” while its narrative calls it the median instrument. Values are reproduced exactly.

| Measure | Strategy 4: long only | Strategy 6: slow trend filter long/short | Strategy 7: slow trend filter with forecasts |
|---|---:|---:|---:|
| Mean annual return | 6.9% | 4.8% | 4.1% |
| Costs | −0.3% | −0.3% | −0.3% |
| Average drawdown | −18.7% | −25.4% | −31.2% |
| Standard deviation | 20.9% | 20.9% | 22.9% |
| Sharpe ratio | 0.32 | 0.21 | 0.18 |
| Turnover | 2.7 | 7.0 | 8.9 |
| Skew | −0.09 | −0.01 | 0.18 |
| Lower tail | 1.56 | 1.53 | 3.80 |
| Upper tail | 1.29 | 1.31 | 3.09 |

Interpretation: results are “slightly disappointing.” More forecast-adjustment trades create a modest turnover increase. Reversal closing trades are smaller, so costs do not materially change. Most other statistics worsen, except skew.

### Table 26 — Jumbo portfolio comparison

The table caption repeats “Performance of average instrument…” although the surrounding text says it reports aggregate Jumbo-portfolio figures; this is a source-caption inconsistency.

| Measure | Strategy 4: long only | Strategy 6: slow trend filter long/short | Strategy 7: slow trend filter with forecasts |
|---|---:|---:|---:|
| Mean annual return | 15.4% | 18.5% | 21.6% |
| Costs | −0.8% | −1.1% | −1.2% |
| Average drawdown | −24.7% | −10.7% | −15.9% |
| Standard deviation | 18.2% | 18.4% | 22.5% |
| Sharpe ratio | 0.85 | 1.01 | 0.96 |
| Turnover | 20.7 | 31.6 | 40.1 |
| Skew | −0.04 | 0.16 | −0.33 |
| Lower tail | 1.44 | 1.48 | 1.90 |
| Upper tail | 1.24 | 1.30 | 1.62 |

Aggregate return improves with forecasts, but Sharpe ratio declines slightly from strategy six and risk statistics are described as “a little uglier.”

### Long-bias adjustment

Historical backtests can favour strategies with a long bias when many instruments have risen. To adjust, the author regresses monthly aggregate Jumbo-portfolio strategy-seven return \(y_t\) on strategy-four benchmark return \(x_t\):

\[
y_t = 1.17\% + 0.51x_t + \varepsilon_t
\]

- \(y_t\): monthly aggregate return of Jumbo portfolio trading strategy seven.
- \(x_t\): strategy-four benchmark return.
- 1.17%: regression alpha per month.
- 0.51: exposure/slope coefficient on the benchmark.
- \(\varepsilon_t\): regression residual/error term.

The 1.17% monthly alpha modestly improves on strategy six's 1.13%. After correcting for differing long-only exposure, forecast scaling “looks pretty good,” though the author does not treat it as conclusive.

## Costs, constraints, and edge cases

- The book's backtested costs rise slightly because forecast scaling adds adjustment trades.
- For institutional traders, gradual reduction may lower real costs materially because market-impact costs are nonlinear; closing an entire large position in one day can be especially expensive. With purely linear costs, costs would probably be unchanged.
- A forecast under one can yield an optimal fractional contract that rounds to zero.
- Do not calibrate with a future-informed scalar during a backtest; use backward-looking rolling estimates.
- Price-unit volatility must match the price-unit crossover in raw-forecast calculation.
- Pool multiple instruments for scalar estimation to reduce sample-specific bias and high-kurtosis problems.
- Never allow absolute forecast over 20 under this strategy's rule.

## Figures and what they communicate

| Figure | Content / implication |
|---|---|
| 29 | S&P 500 micro future with 64-day and 256-day EWMAs around the COVID crash; a simple positive crossover remains long across materially different trend-strength regimes. |
| 30 | EWMAC(64,256) crossover history for the S&P 500; unadjusted crossover magnitude varies with price level and volatility. |
| 31 | Scaled EWMAC(64,256) forecast history for the S&P 500; values are centered on an average absolute scale near 10, with occasional much larger values. |
| 32 | Scaled forecast and contract position in late 2019/early 2020; shows large January exposure then gradual forecast/risk-driven reduction before the selloff. |
| Strategy seven plan | Inputs, formulas, capped forecast, position sizing, update-and-trade decision process. |

## Conclusions and implications

Forecasts represent trade conviction: longer-lived, lower-volatility trends are more convincing than newly established, weak/choppy ones. The chapter reports only marginal direct benefits for this slow trend rule, but retains forecasting because:

- it works better for faster trend filters and other strategies (evidence deferred);
- common-scale forecast strength facilitates combining strategies in strategy nine;
- it may reduce institutional trading costs despite a modest retail-cost increase.

The broader promise is a diversified collection of strategies rather than a single strategy. The next strategy adds a faster trend-following filter; strategy nine addresses combination; strategy twelve (Part Two) is cited for empirical research on conviction/forecasting.

## Glossary

- **Capped forecast:** scaled forecast limited to \([-20,+20]\).
- **Crossover / EWMAC:** fast EWMA minus slow EWMA; the trend-rule signal.
- **EWMA:** exponentially weighted moving average.
- **Forecast:** value proportional to expected risk-adjusted return / expected Sharpe ratio.
- **Forecast scalar:** \(10/\operatorname{Average}(|\text{raw forecast}|)\), used to put forecasts on a common scale.
- **IDM:** instrument diversification multiplier; inherited from earlier strategies.
- **Raw forecast:** risk-adjusted crossover before common-scale calibration.
- **Scaled forecast:** raw forecast multiplied by forecast scalar, targeted to average absolute value 10.
- **Trading rule:** any method that produces a forecast.
- **Trend strength:** the magnitude/conviction of an estimated trend, represented by the forecast.

## Explicit chapter connections

- **Strategy six:** supplies the otherwise identical framework, EWMA calculations, and the prior long/short slow trend filter; its long-bias regression method is reused.
- **Next strategy / strategy eight:** faster EWMA crossover and a method to reduce extra retail trading costs.
- **Strategy nine:** combines different strategies using common-scale forecasts.
- **Strategy twelve, Part Two:** empirical evidence for forecasting/conviction.
- **Appendix B:** further details on deriving daily price volatility from \(\sigma_\%\).
