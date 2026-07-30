# Strategy Three — Buy and Hold with Variable Risk Scaling

## Purpose and central argument

Strategy three keeps the buy-and-hold exposure of strategy two but replaces its fixed instrument-risk estimate with a regularly updated volatility forecast. The central claim is that volatility clusters enough that recent volatility usefully forecasts near-term risk. Scaling the position inversely to that forecast produces materially steadier realised risk and thinner return tails, although it does not create a large standalone performance improvement and it raises turnover/costs.

The chapter is educational rather than a recommendation to trade it alone: its 20% target is described as too high for the strategy's observed median Sharpe ratio.

## Strategy definition and operating plan

- **Instrument:** any instrument expected to have a positive risk premium that also passes minimum-capital, liquidity, and cost thresholds.
- **Position:** long the current *rounded* number of contracts `N` calculated below; update as price and volatility estimate change.
- **Risk estimate:** exponentially weighted annualised standard deviation of percentage returns using a 32-business-day span, then blend it with a ten-year average:

  \[
  \sigma_t^{blend}=0.3(\text{ten-year average of }\sigma_t)+0.7\sigma_t
  \]

- **Other elements:** identical to strategy two (the chapter does not reproduce them here).

## Volatility forecasting

### Why it is forecastable

Volatility clusters: low-volatility periods tend to follow low-volatility periods and vice versa. The chapter states that standard deviation estimated from roughly the last month of returns forecasts near-term (days/weeks) standard deviation well. This is contrasted with returns, which it says are hard to forecast.

### Simple moving-window estimator

For a window of `N` returns, the chapter gives:

\[
\bar r_t=\frac{1}{N}r_t+\frac{1}{N}r_{t-1}+\cdots+\frac{1}{N}r_{t-N+1}
\]

\[
\sigma(N)_t=\sqrt{\frac{1}{N}(r_t-\bar r_t)^2+\frac{1}{N}(r_{t-1}-\bar r_t)^2+\cdots+\frac{1}{N}(r_{t-N+1}-\bar r_t)^2}
\]

- `r_t`: return at time `t`; use percentage returns for annualised percentage risk `\sigma_%`, and price changes for daily price-change risk `\sigma_p`.
- `\bar r_t`: moving-average return over the window ending at `t`.
- `N`: number of observations; approximately 22 business days is one month.
- `\sigma(N)_t`: standard-deviation estimate from that window.
- For `\sigma_%`, annualise the estimate by multiplying by 16. For `\sigma_p`, do not annualise under this stated convention.

**Limitation:** equal weights make a one-month estimator noisy: a large return can cause a discrete change when it drops out of the window. A longer window lowers turnover but reduces forecasting power; the chapter reports that using three months rather than one lowers predictability by about 40%, measured by the `R²` of realised next-40-day standard deviation on the forecast.

### EWMA estimator

The proposed smoothing method is an exponentially weighted moving average (EWMA):

\[
\bar r_t^{EWMA}=\lambda r_t+\lambda(1-\lambda)r_{t-1}+\lambda(1-\lambda)^2r_{t-2}+\cdots
\]

\[
\sigma_t^{EWMA}=\sqrt{\lambda(r_t-\bar r_t)^2+\lambda(1-\lambda)(r_{t-1}-\bar r_t)^2+\lambda(1-\lambda)^2(r_{t-2}-\bar r_t)^2+\cdots}
\]

- `\lambda`: exponential decay/weight parameter. Higher `\lambda` puts more weight on recent data and is equivalent to a shorter SMA window.
- `\bar r_t^{EWMA}` and `\sigma_t^{EWMA}`: exponentially weighted mean and standard deviation.
- The displayed variance expression uses `\bar r_t` in each term; the source does not explicitly distinguish whether this is the EWMA mean, so this reference preserves its notation.

Use a **span** `N` to parameterise `\lambda`:

\[
\lambda=\frac{2}{N+1}
\]

Half life is the historical point by which half the moving-average weight has been used. For an SMA it is half the window length. A 32-day EWMA has approximately the same 11-day half life as a 22-day SMA; therefore use `\lambda=0.06061` (`N=32`). The chapter says values roughly around 0.06 are suitable; much shorter spans increase costs, while much longer spans lose forecast efficacy.

### Blend short-run clustering with long-run mean reversion

Short-run volatility clustering coexists with long-run mean reversion. A pure recent-risk estimate can become very low in calm periods, which would lead to a very large position just before a crisis. The solution is the blend shown in the operating plan: 0.7 current EWMA risk plus 0.3 ten-year average risk. The cited basis for the weights is a regression of future standard deviation on current and historical estimates; the author says the estimates were stable across time/instruments and backward-looking retesting did not harm results. The slow component also damps estimate changes and trading costs.

## Position sizing

\[
N_t=\frac{\text{Capital}_t\times\tau}{\text{Multiplier}\times\text{Price}_t\times FX_t\times\sigma_{%,t}}
\]

- `N_t`: contracts at time `t`, rounded for actual trading.
- `Capital_t`: account capital.
- `\tau`: annual risk target (20% in the examples).
- `Multiplier`: futures-contract multiplier in instrument currency per price point.
- `Price_t`: current futures price.
- `FX_t`: exchange rate needed to express the contract risk in the account currency (1 when the same currency).
- `\sigma_{%,t}`: current **blended**, annualised standard deviation of percentage returns, expressed as a decimal.

For an S&P 500 micro future (`Multiplier=5`, `FX=1`, `Capital=$100,000`, `\tau=0.20`):

\[
N_t=\frac{100{,}000\times0.20}{5\times\text{Price}_t\times1\times\sigma_{%,t}}
=\frac{25{,}000}{\text{Price}_t\sigma_{%,t}}
\]

Higher forecast volatility cuts the position; calmer conditions increase leverage. Figure 16 shows the same broad price-driven pattern as fixed-risk strategy two, but 1987’s volatility spike sharply cuts the position despite the falling price.

## Risk-adjusted costs

### Definition

Risk-adjusted cost is the expected-return reduction due to costs divided by estimated annual risk: a Sharpe-ratio unit with costs in the numerator.

\[
SR=\frac{\text{annual mean excess return}}{\text{annualised standard deviation}},\qquad
\text{Cost in SR terms}=\frac{\text{annual cost}}{\text{annualised standard deviation}}
\]

Example: 10% expected excess return, 20% standard deviation, and 1% annual cost gives pre-cost SR `0.50`, post-cost SR `0.45`, and cost `0.05` SR units (`0.50-0.45`).

This method uses today’s prices, spreads, commissions, and risk to estimate historical-backtest costs. It is explicitly an approximation, but is intended to assess real-money feasibility in the current environment. It makes results comparable across account sizes and instruments. It is not strictly account-size independent for very large institutions, which must estimate market impact rather than top-of-book spread.

### Per-trade calculation

\[
\text{Spread cost (points)}=\frac{\text{Offer}-\text{Bid}}{2}
\]
\[
\text{Spread cost (currency)}=\text{Multiplier}\times\text{spread cost (points)}
=\text{Tick value}\times\frac{\text{spread (ticks)}}{2}
\]
\[
\text{Total cost/trade (currency)}=\text{spread cost (currency)}+\text{commission/contract}
\]
\[
\text{Total cost/trade (\%)}=\frac{\text{total cost/trade (currency)}}{\text{Price}\times\text{Multiplier}}
\]
\[
\text{Risk-adjusted cost/trade}=\frac{\text{total cost/trade (\%)}}{\sigma_\%}
\]

The half-spread assumption applies to smaller traders who can fill at the top of the order book; large institutions must assess market impact.

**Worked S&P micro example:** bid 4503.25, offer 4503.30, multiplier 5, commission $0.25, price 4500, `\sigma_%=16%`. Spread cost is 0.125 points = $0.625; total cost is $0.875. Thus `0.875/(5×4500)=0.0039%`, and risk-adjusted cost/trade is `0.0039%/16%=0.000243` SR units.

### Annual cost and turnover

\[
\text{Holding cost}=c\times\text{rolls/year}\times2
\]
\[
\text{Transaction cost}=c\times\text{turnover}
\]
\[
\text{Annual risk-adjusted cost}=\text{holding cost}+\text{transaction cost}
\]

`c` is risk-adjusted cost/trade. The factor two conservatively charges both legs of each roll. **Source ambiguity:** the image for the final equation appears to label the second term “holding cost,” but the surrounding text and arithmetic establish that it is transaction cost.

With quarterly rolls and `c=0.000243`, holding cost is `0.000243×4×2=0.00194`. With turnover 6, transaction cost is `0.000243×6=0.00145`; annual cost is `0.0034` SR units.

Turnover means the number of times the **average position** is traded, not a contract count. In the 2021 S&P micro backtest with $100,000 and 20% target: 60 contracts traded / 9.3 average contracts = 6.5. Full-backtest turnover is 5.1; it was conservatively rounded to 6 for the example. Figure 17 (rolling six-month estimate, excluding the four annual roll trades) stays roughly 4–6 and shows no trend. Assumptions are that backtest turnover persists and current risk-adjusted cost remains accurate; recalculate costs regularly. The simple calculation requires an always-on position and a well-defined average position.

### Cost comparison (Table 8, SR units/trade)

| Expensive | Cost | Cheap | Cost |
|---|---:|---|---:|
| Milk (Commodity) | 0.083 | S&P 500 micro/mini (Equity) | 0.00024 |
| Cheese (Commodity) | 0.028 | NASDAQ micro/mini (Equity) | 0.00038 |
| US 2-year (Bond) | 0.024 | Dow Jones (Equity) | 0.00045 |
| German 2-year (Bond) | 0.023 | Russell 2000 (Equity) | 0.00078 |
| Rice (Commodity) | 0.022 | Gas-Last (Energy) | 0.00081 |
| VSTOXX (Volatility) | 0.020 | Henry Hub Gas (Energy) | 0.00081 |
| Iron (Metal) | 0.019 | Gold micro (Metal) | 0.00083 |
| Italian 3-year (Bond) | 0.015 | Nikkei (Equity) | 0.00092 |

Costs are based on values at the time of writing and must be recalculated with current broker commissions/spreads. In the absence of commissions, a different multiplier has no effect on risk-adjusted cost; micro and mini S&P/NASDAQ costs are correspondingly near-identical.

## Evidence on realised risk and performance

Figures 15/18 show that strategy two averaged about 25% risk against a 20% target, but ranged below 8% in 2017 and above 50% in 1987, 2008, and 2020. Variable targeting keeps the two-month rolling standard deviation mostly 15–25%. In the surprise 1987 event it reached 60% (still more than 3× target) versus strategy two briefly reaching 6× target. In late 2008: fixed >100% versus variable 22%; early-2020: 62% versus 28%. Average risk is 22.8% for variable versus 25.0% fixed; unlike fixed strategy two’s whole-backtest fitted estimate, strategy three’s estimate is updated backward-looking.

Figure 19 shows more stable daily returns. The mechanism is that sustained high-volatility periods are rescaled toward typical daily risk. It cannot eliminate shocks or transition-period errors; the footnote explains that volatility-of-volatility otherwise produces kurtosis/fat tails (even a possible bimodal distribution across high/low regimes).

### Table 9 — S&P 500 micro: fixed vs variable risk

| Measure | Strategy 2 fixed | Strategy 3 variable |
|---|---:|---:|
| Mean annual return | 12.1% | 12.2% |
| Annual costs | −0.04% | −0.06% |
| Average drawdown | −16.9% | −18.8% |
| Standard deviation | 25.0% | 22.8% |
| Sharpe ratio | 0.48 | 0.54 |
| Skew | −0.47 | −0.68 |
| Lower tail | 2.21 | 1.76 |
| Upper tail | 1.79 | 1.21 |

Variable risk has slightly higher return/lower risk and higher SR, but higher costs, worse average drawdown, and worse skew. The source attributes worse skew to fewer bad days whose remaining negative returns are comparatively worse, even though better in absolute magnitude. Robust percentile tail measures show reduced fat tails on both sides.

### Median results across 102 eligible instruments (Tables 10–11)

| Measure | Equity | Vol | FX | Bond | Metals | Energy | Ags | Overall median |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| Mean annual return | 9.6% | −8.7% | 1.7% | 12.1% | 6.9% | 5.9% | 1.3% | 6.9% |
| Costs | −0.2% | −1.1% | −0.3% | −0.3% | −0.3% | −0.3% | −0.3% | −0.3% |
| Turnover | 3.3 | 3.4 | 2.4 | 2.9 | 2.6 | 2.3 | 2.1 | 2.7 |
| Average drawdown | −12.9% | −87.5% | −41.2% | −14.5% | −52.0% | −36.7% | −52.7% | −18.7% |
| Standard deviation | 21.1% | 21.9% | 20.5% | 20.7% | 22.1% | 21.7% | 20.7% | 20.9% |
| Sharpe ratio | 0.46 | −0.40 | 0.09 | 0.59 | 0.32 | 0.27 | 0.07 | 0.32 |
| Skew | −0.33 | 1.43 | −0.10 | −0.08 | 0.46 | 0.07 | 0.43 | −0.09 |
| Lower tail | 1.76 | 1.20 | 1.55 | 1.52 | 1.66 | 1.42 | 1.36 | 1.56 |
| Upper tail | 1.17 | 2.58 | 1.38 | 1.27 | 1.55 | 1.29 | 1.46 | 1.29 |

Versus strategy two, the chapter reports slightly lower standard deviation/slightly higher mean return, mostly unchanged SR (lower for agricultural markets), higher turnover/cost, lower lower- and upper-tail ratios, less-negative skew, and a large fall in the positive skew of volatility futures.

## Choosing instruments: capital, costs, performance, liquidity

### Risk target warning

The stated half-Kelly rule of thumb is `\tau = 0.5 × expected SR`. A 20% target is therefore appropriate only if expected SR is at least 0.40. The median is 0.32, and only equity and bonds exceed 0.40 in the displayed asset-class results; the author cautions that their historical secular repricing may not repeat. Use a target lower than 20% if trading this strategy alone.

### Minimum capital

To start with four contracts and leave room to adjust:

\[
\text{Minimum capital}_{4}=\frac{4\times\text{Multiplier}\times\text{Price}\times FX\times\sigma_\%}{\tau}
\]

Risk can double overnight, requiring a halving of position. Low minimum capital often coincides with expensive risk-adjusted trading: riskier contracts lower the capital formula but raise cost because `\sigma_%` is in the denominator of risk-adjusted cost. Spreads, commissions, multipliers, and price also matter.

### Do not select on historical SR alone

Figure 20 plots each instrument’s historical strategy-three SR with approximate 95% error bars. Wider bars mean less history. Nearly all bars overlap, so apparent differences are generally not statistically significant; non-overlap would be required to make that claim. The standard deviation of an SR estimate is:

\[
\sqrt{\frac{1+0.5SR^2}{N}}
\]

where `N` is number of data points. The figure’s bars are two standard deviations on either side of the mean estimate. Even significance would not ensure repeatability (the chapter cites bond performance driven by a secular decline in rates).

### Cost speed limit

Choose the highest post-cost SR: maximise pre-cost SR and minimise cost. Because pre-cost comparisons are not decisive, use a **trading speed limit**: spend no more than one-third of likely pre-cost SR on cost, retaining at least two-thirds. For estimated pre-cost SR ≈0.30, annual risk-adjusted cost must be `<0.10`:

\[
(\text{rolls/year}\times2+\text{turnover})\times c<0.10
\]

With quarterly rolls and turnover ≈3: `(4×2+3)c<0.10`, hence `c<0.0091`; round down to a maximum of **0.01 SR units/trade**. Later strategies can have greater turnover/monthly rolls and require a lower limit.

### Liquidity tests

Cost calculations assume fills at half the bid–ask spread. The author rejects markets below 100 contracts/day (a one-contract order is then over 1% of average volume) and notes institutions should use a higher threshold. Measure volume on the most-active expiry and average it over the last 20 business days; do not sum contracts across expiries. Also use:

\[
\text{Average daily volume in USD risk}=FX\times\text{average daily volume}\times\sigma_p\times\text{Price}\times\text{Multiplier}
\]

`\sigma_p` is daily price-change risk. The author’s own minimum is $1.25m/day in USD-risk terms; it depends on trade size and acceptable share of daily volume. Other sensible requirements include minimum open interest.

### S&P 500 e-mini vs micro e-mini

Both have volumes over 500,000/day and costs about 0.00024 SR units. The micro multiplier is $5 versus $50 for the e-mini, so the micro needs less capital and permits more granular sizing. Select micro unless a mini/micro fails liquidity or cost thresholds; then a larger contract may be necessary if capital permits.

## Figures and tables: what they communicate

- **Figure 15:** fixed-risk strategy two has highly variable rolling realised risk despite acceptable average risk.
- **Figures 16–17:** variable-risk position shrinks in volatility spikes; non-roll turnover is reasonably stable around 4–6/year.
- **Table 8:** trading costs vary enormously across instruments and must be current-data checked.
- **Figures 18–19 / Table 9:** variable scaling improves risk targeting and percentile tails, but not every conventional metric.
- **Tables 10–11:** across eligible markets, median risk stays close to the 20% target; standalone return/SR varies substantially by class.
- **Figure 20:** observed cross-instrument SR dispersion is largely indistinguishable once sampling uncertainty is included.

## Key constraints, errors to avoid, and takeaways

- Do not treat recent volatility as a perfect forecast: abrupt shocks can overshoot target badly.
- Do not use an overly reactive volatility estimate; it raises turnover. Do not make it too slow; forecasting ability deteriorates.
- Do not size with only a low short-run estimate; the blend guards against oversized calm-before-crisis exposure.
- Do not assume historical currency costs were constant. Risk-adjusted present-day costs are a practical proxy, not literal historical costs.
- Do not use the simple turnover-cost calculation for strategies without a continuous/well-defined average position; the chapter points to strategy five for a more general method.
- Do not rely on a historical SR ranking when the confidence intervals overlap.
- Do not ignore cost, capital, or liquidity just because a contract has a favourable historical result.

The chapter concludes that variable scaling is mainly valuable for stable risk and reduced fat tails, not for the major performance boost created by introducing risk targeting in strategy two. Instrument selection is a balance between cost and minimum capital, and strategy four introduces diversification across multiple instruments.

## Glossary

- **Annualised standard deviation (`\sigma_%`):** annual risk measure from percentage returns.
- **EWMA:** exponentially weighted moving average/standard deviation, downweighting older observations.
- **Half life:** historical distance at which half a moving average’s weight has been used.
- **Span:** EWMA parameterisation related to `\lambda` by `2/(N+1)`.
- **Risk target (`\tau`):** desired annualised portfolio-risk level.
- **Risk-adjusted cost:** cost expressed in Sharpe-ratio units.
- **Turnover:** annual contracts traded divided by average position, i.e. times the average position is turned over.
- **Holding cost:** roll cost for maintaining a futures position.
- **Transaction cost:** cost from non-roll position adjustments.
- **Lower/upper tail ratio:** percentile-based measures used here to assess fat tails.
- **Speed limit:** maximum annual cost set at one-third of likely pre-cost SR.
- **USD risk volume:** liquidity measure incorporating contract risk, price, multiplier, FX, and daily volume.

## Explicit chapter connections

- **Strategy one:** original contract-level commission/spread cost approach.
- **Strategy two:** fixed-risk position formula, minimum capital, fixed-risk performance tables/figures, and half-Kelly target-risk discussion.
- **Strategy four:** alternative of trading multiple instruments.
- **Strategy five:** more general backtested-cost calculation for non-continuous position patterns.
- **Strategy nine:** warning that frequent historical strategies may have faced higher past costs.
- **Appendix B:** precise turnover calculation and EWMA standard-deviation implementation.
