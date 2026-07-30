# Strategy 27 — Safer fast mean reversion

## Purpose and central argument

Strategy 27 modifies the pure fast mean-reversion approach in Strategy 26 to retain fast, intraday mean-reversion trades while reducing its tendency to suffer badly in sharp trends and high-volatility regimes. It does this with two changes:

1. **Trend forecast overlay:** trade the mean-reversion forecast only when it has the same sign as a slower trend forecast (EWMAC 16,64). This amounts to buying dips in an uptrend and selling rallies in a downtrend.
2. **Volatility forecast multiplier:** reduce the forecast—and therefore the position—when current volatility is high relative to its own long-run history.

The author’s stated result is a strategy that is more profitable and safer than pure mean reversion. The chapter emphasizes, however, that the particularly high backtested portfolio Sharpe ratio should not be taken at face value.

## Why the changes are needed

Pure mean reversion trades against the current trend: as price falls farther below equilibrium it keeps buying, and as price rises above equilibrium it keeps selling. This makes it a useful diversifier beside trend strategies, but creates “catching a falling knife” losses and heavily negative skew.

A conventional stop loss is rejected here because its threshold and re-entry rule are subjective. It also introduces **path dependence**: the current forecast depends on the previous day’s forecast, making the backtest more complex and less intuitive.

Mean reversion also performs poorly when risk/volatility rises. The chapter points to COVID-19 and the invasion of Ukraine as painful periods for the original strategy.

## Model and calculations

### 1. Base fast mean-reversion forecast

Use a five-period exponentially weighted moving average (EWMA) as equilibrium:

\[
\text{Equilibrium}_t = \operatorname{EWMA}_{\text{span}=5}(p_t,p_{t-1},p_{t-2},\ldots)
\]

\[
\text{Raw forecast}_t = \text{Equilibrium}_t - p_t
\]

\[
\sigma_p = p_t\,\sigma_\%/16
\]

\[
\text{Risk-adjusted forecast}_t=\text{Raw forecast}_t/\sigma_p
\]

Where:

- \(p_t\): current price at time \(t\).
- \(p_{t-1}, p_{t-2},\ldots\): earlier prices.
- \(\sigma_\%\): percentage-volatility estimate; the chapter’s trading plan refers to a variable risk estimate, but this chapter does not restate its exact estimation formula.
- \(\sigma_p\): price-volatility quantity used to normalize the raw forecast.
- “Span = 5”: the equilibrium EWMA parameter.

**Interpretation:** when price is below equilibrium, the raw/risk-adjusted mean-reversion forecast is positive (long); when price is above equilibrium, it is negative (short).

### 2. Trend forecast overlay

Calculate an **EWMAC 16,64** forecast using daily data. If its sign differs from the sign of the risk-adjusted mean-reversion forecast, set the mean-reversion forecast to zero. The author uses this single EWMAC rule for simplicity, while stating that in principle any trend rule or combination of rules could be used.

Operationally:

1. Compute the risk-adjusted mean-reversion forecast.
2. Compute the daily EWMAC16,64 trend forecast.
3. If their signs agree, retain the mean-reversion forecast.
4. If their signs conflict, replace the mean-reversion forecast with zero.

In an uptrend, this permits longs below equilibrium but blocks shorts above equilibrium. In a downtrend, the mirror image applies: it blocks longs below equilibrium and permits shorts above equilibrium. If an initially upward-trending market sells off, the strategy may initially remain long; after roughly a week—depending on the price path—the EWMAC can become negative, which closes the conflicting long. The overlay therefore substitutes for an explicit stop loss.

**Trade-off:** the overlay changes mean reversion’s relationship with trend strategies from fairly negative correlation to modestly positive correlation. In exchange, the chapter reports better standalone performance and safety.

### 3. Relative-volatility multiplier

For market \(i\), let \(\sigma_{i,t}\) be the current estimated percentage standard deviation of returns, measured using the method from Strategy 3. Assuming 256 business days per year, define relative volatility as current volatility divided by its rolling ten-year average:

\[
V_{i,t}=\sigma_{i,t}/\operatorname{mean}(\sigma_{i,t-2560},\sigma_{i,t-2559},\ldots,\sigma_{i,t})
\]

Compute the historical quantile of the current relative-volatility value:

\[
Q_{i,t}=\operatorname{Quantile}\bigl(V_{i,t}\text{ in distribution}(V_{i,0},\ldots,V_{i,t})\bigr)
\]

Then calculate a smoothed volatility multiplier:

\[
M_{i,t}=\operatorname{EWMA}_{10}(2-1.5Q_{i,t})
\]

\[
\text{Modified risk-adjusted forecast}_{i,t}
=\text{Raw risk-adjusted forecast}_{i,t}\times M_{i,t}
\]

Where:

- \(i\): market/instrument.
- \(t\): time.
- \(V_{i,t}\): relative volatility.
- \(Q_{i,t}\): quantile of relative volatility in the instrument’s observed history; it ranges from 0 (lowest observed value) to 1 (highest), with 0.5 the median.
- \(M_{i,t}\): volatility forecast multiplier.
- \(\operatorname{EWMA}_{10}\): EWMA with span 10.

Because the unsmoothed expression \(2-1.5Q\) declines as \(Q\) rises, higher relative volatility reduces \(M\) and hence reduces the forecast. The chapter does not separately state the attained numerical range after EWMA smoothing.

### 4. Scaling, position, and execution prices

After the trend overlay and volatility multiplier, apply a forecast scalar. The overlay turns the strategy off about half the time, so the author estimates a higher scalar of approximately **20**. Cap the forecast, calculate optimal position, and use the low-cost execution method of Strategy 26.

\[
N_t=\left\{[M_t\times\text{Scalar}\times(\text{Equilibrium}_t-p_t)/\sigma_p]/10\right\}\times\text{Average position}_t
\]

\[
\text{Average position}
=\text{Capital}\times\text{IDM}\times\text{Weight}_i\times\tau
/ (\text{Multiplier}\times p_t\times\text{FX}_t\times\sigma_{\%,t})
\]

Given current position \(C\), calculate the limit prices:

\[
\text{Buy limit price}_t
=\text{Equilibrium}_t-[(C+1)\times10\times\sigma_p/(\text{Scalar}\times M_t\times\text{Average position}_t)]
\]

\[
\text{Sell limit price}_t
=\text{Equilibrium}_t-[(C-1)\times10\times\sigma_p/(\text{Scalar}\times M_t\times\text{Average position}_t)]
\]

Where:

- \(N_t\): optimal position (identified as such by the surrounding text).
- \(C\): current position.
- \(M_t\): volatility multiplier at time \(t\).
- **Scalar**: forecast scalar; estimated near 20 in this strategy.
- **Average position**: baseline position size, calculated by the displayed equation.
- **Capital, IDM, Weight\(_i\), \(\tau\), Multiplier, FX\(_t\)**: used in the displayed average-position equation, but not defined in this chapter; their exact definitions/units must be taken from the referenced earlier material rather than inferred here.

## Trading plan (as presented)

- **Strategy:** go long or short one or more instruments using a variable risk estimate and a forecast based on fast mean reversion, a trend overlay, and a volatility-level multiplier.
- **Risk-adjusted forecast:** begin with Strategy 26’s five-span equilibrium/mean-reversion forecast and normalize it by \(\sigma_p\).
- **Trend overlay:** calculate daily EWMAC16,64; if it has a different sign than the risk-adjusted mean-reversion forecast, set the mean-reversion forecast to zero.
- **Volatility multiplier:** compute \(V\), historical quantile \(Q\), then \(M\) as above; multiply the raw risk-adjusted forecast by \(M\).
- **Scaled forecast:** multiply the modified risk-adjusted forecast by a forecast scalar of 20.
- **Remaining stages:** identical to Strategy 26, including forecast capping, optimal-position calculation, and execution methodology.

## Performance evidence

All tables below use hourly data since January 2013 unless otherwise noted.

### Table 132 — Median instrument performance, financial asset classes

| Metric | Equity | Vol | FX | Bond |
|---|---:|---:|---:|---:|
| Mean annual return | 9.8% | 16.3% | 10.0% | 18.3% |
| Costs (commission) | −0.6% | −1.2% | −0.7% | −0.7% |
| Average drawdown | −8.4% | −11.4% | −7.8% | −3.9% |
| Standard deviation | 21.5% | 27.1% | 18.3% | 18.4% |
| Sharpe ratio | 0.43 | 0.60 | 0.54 | 1.00 |
| Turnover | 81.3 | 68.4 | 92.1 | 77.6 |
| Skew | −0.77 | −2.41 | −0.27 | −0.11 |
| Lower tail | 5.77 | 10.85 | 4.52 | 4.10 |
| Upper tail | 1.92 | 2.83 | 2.22 | 2.32 |

### Table 133 — Median instrument performance, commodity asset classes

| Metric | Metals | Energy | Ags | Median |
|---|---:|---:|---:|---:|
| Mean annual return | 8.7% | 9.2% | 8.5% | 10.2% |
| Costs (commission) | −0.6% | −0.2% | −1.0% | −0.6% |
| Average drawdown | −11.5% | −9.1% | −12.5% | −8.1% |
| Standard deviation | 18.7% | 19.7% | 18.7% | 19.5% |
| Sharpe ratio | 0.43 | 0.47 | 0.46 | 0.54 |
| Turnover | 83.0 | 83.6 | 83.9 | 81.9 |
| Skew | −0.74 | −0.65 | −0.94 | −0.57 |
| Lower tail | 5.42 | 4.91 | 5.12 | 5.08 |
| Upper tail | 1.98 | 2.64 | 2.35 | 2.12 |

The chapter compares these with Strategy 26’s Tables 129–130 (pages 432–433). It reports that median monthly skew across all instruments improved from −0.82 to −0.57, and the overall median Sharpe ratio rose from 0.41 to 0.54. Both tails worsened, which the author attributes to switching the strategy off about half the time and roughly doubling the forecast scalar, making returns more extreme.

### Table 134 — Aggregate Jumbo portfolio since 2013

| Metric | Multiple trend (S9) | Carry (S10) | Fast mean reversion (S26) | Safer fast mean reversion (S27) |
|---|---:|---:|---:|---:|
| Mean annual return | 13.8% | 8.7% | 17.6% | 31.6% |
| Costs | −1.1% | −0.7% | −3.1%* | −1.9%* |
| Average drawdown | −15.0% | −10.2% | −7.3% | −2.0% |
| Standard deviation | 17.5% | 15.3% | 22.0% | 14.8% |
| Sharpe ratio | 0.79 | 0.56 | 0.80 | 2.14 |
| Turnover | 40.6 | 10.5 | 39.2 | 65.7 |
| Skew | 0.20 | −0.31 | −1.46 | 1.36 |
| Lower tail | 2.96 | 2.06 | 2.74 | 2.29 |
| Upper tail | 2.01 | 1.33 | 1.98 | 2.13 |

\*Costs for fast strategies are commission only; they exclude spread costs on market orders.

The portfolio’s monthly skew is positive, which the author attributes to diversification: negative-skew events in individual assets were not significantly correlated in this roughly ten-year backtest. This should not be overread: reported skew is 0.25 for daily returns, −0.36 for weekly returns, and −0.06 for annual returns. The author would be surprised if its true skew were materially more positive than trend’s, though the worst negative skew from Strategy 26 has been removed.

The forecast overlay lowers average position and thus raises turnover (turnover is a multiple of average position), while trading only about half the time lowers costs. Costs do not quite halve because positions must also be closed when the trend forecast flips to the opposite sign.

### Figure 83 — What it communicates

The figure plots cumulative account curves from 2013 to 2022 for original mean reversion (Strategy 26) and safer mean reversion (Strategy 27). The two are broadly similar through 2019. The safer version holds up materially better in early 2020 and rises substantially above the original through 2021–2022; the chapter specifically identifies early 2020 and Q1 2022 as high-volatility periods with clear improvement.

### Table 135 — Return correlations since 2013

|  | Trend (S9) | Carry (S10) | Trend + carry (S11) | Mean reversion (S26) | Safer mean reversion (S27) |
|---|---:|---:|---:|---:|---:|
| Trend (S9) | 1 | 0.15 | 0.88 | −0.24 | 0.34 |
| Carry (S10) |  | 1 | 0.50 | 0.08 | 0.01 |
| Trend + carry (S11) |  |  | 1 | −0.15 | 0.33 |
| Mean reversion (S26) |  |  |  | 1 | 0.43 |
| Safer mean reversion (S27) |  |  |  |  | 1 |

The safer strategy remains relatively low-correlated with carry and trend, but it is more correlated with them than original mean reversion.

## Caveats, constraints, and implementation risks

- **Do not trust the 2.14 backtested Sharpe ratio without skepticism.** The author’s standing policy is not to trust a backtested Sharpe ratio above 2.
- The sample is just under ten years, shorter than desired and potentially unusually favorable.
- Backtesting continuously trading limit orders from hourly data is difficult; modeling assumptions or code errors may inflate results.
- The trend overlay began in the author’s initial more complex test; EWMAC16 was stated to be chosen arbitrarily rather than fitted, but was already known to be profitable. The volatility multiplier was added later, though it was taken unchanged from Strategy 13.
- Fast intraday execution places many orders and can lose a significant amount in a very short time. The author considers full automation almost essential and advises careful testing and monitoring.
- The strategy needs substantial capital to trade the aggregate Jumbo portfolio and realize its diversification benefits. The author estimates about **$50 million**; with fewer instruments, unattractive single-instrument skew cannot be diversified away.
- Dynamic optimization from Strategy 24 cannot be used; the full minimum capital is needed for every instrument traded.
- Capacity is limited relative to the slower strategies, so it is also problematic for multi-billion-dollar funds.

## Portfolio implications and allocation examples

The author would use Strategy 27 alongside a daily strategy incorporating carry and trend, plus other Part Two/Three strategies—not as an all-in allocation.

- Following the book’s 40% convention for convergent strategies, the author would allocate at most **20%** to this mean-reversion strategy.
- The stated allocation maximizing Sharpe ratio and alpha is about **85%** to safer mean reversion and 15% to Strategy 11. Because 60% of Strategy 11 is divergent trend, the divergent share is \(0.6\times0.15=0.09\), leaving 91% of the combined allocation in convergent strategies.
- A 50% allocation to Strategy 27 still has excellent Sharpe and less-scary skew, but the blend remains 70% convergent.
- Footnote comparison: a 50/50 portfolio of Strategy 11 and safer mean reversion has Sharpe 1.89 versus 1.65 using original mean reversion; monthly skew is 0.59 versus −0.29.

## Connections to other chapters

- **Strategy 26:** supplies the base fast mean-reversion forecast, caps/position/execution stages, and the original strategy used in comparison.
- **Part One / EWMAC16:** supplies the EWMAC 16,64 trend rule.
- **Strategy 3:** supplies the percentage-volatility estimation method.
- **Strategy 13 (Part Two):** supplies the high-volatility forecast-reduction methodology without further changes.
- **Strategy 24:** dynamic optimization cannot be applied here.
- **Strategies 9, 10, and 11:** multiple trend, carry, and their combined portfolio are comparison and allocation components.

## Glossary

- **Convergent strategy:** a strategy type that tends to profit from convergence/reversion; the chapter classifies mean reversion and carry as convergent.
- **Divergent strategy:** a strategy type that tends to profit from persistent moves; the chapter classifies trend as divergent.
- **EWMAC16,64:** the daily fast/slow EWMA cross-over trend forecast used as the overlay.
- **Equilibrium:** five-span EWMA of recent prices used as the mean-reversion reference level.
- **Forecast overlay:** a rule that suppresses the mean-reversion forecast when its sign conflicts with the trend forecast.
- **Forecast scalar:** scaling factor for the forecast; approximately 20 here.
- **Path dependence:** current forecast depends on its earlier value.
- **Relative volatility:** current percentage volatility divided by its rolling ten-year average.
- **Skew:** distribution asymmetry; the chapter focuses on the undesirable negative skew of pure mean reversion.
- **Volatility forecast multiplier:** \(M\), the smoothed multiplier that reduces forecasts in high relative-volatility states.

## Key takeaways

- The strategy does not use a hard stop; the slower trend overlay exits a mean-reversion position once the trend signal conflicts with it.
- It intentionally trades only mean-reversion moves aligned with the prevailing trend: buy dips in uptrends and sell rallies in downtrends.
- Volatility conditioning reduces exposure when the environment is historically volatile.
- The reported results materially improve skew and Sharpe ratio, but the exceptional aggregate Sharpe ratio carries strong sample, execution-model, and fitting caveats.
- Implementation requires automation, careful cost-aware testing, monitoring, capital, and sufficient diversification.
