# Strategy ten: Basic carry

## Purpose and central claim

This chapter turns the expected **carry** embedded in a futures curve into a risk-adjusted trading forecast. The strategy trades one or more futures with variable-risk position sizing, going long or short in proportion to a capped, smoothed carry forecast. Carry is a distinct risk premium from trend: it can be predicted independently, is typically cheaper to trade than trend, and is only moderately correlated with it (0.36 in the author's strategy-nine/ten comparison). It is not free money: positive carry compensates for risks and can be negatively skewed, especially in volatility and some FX positions. Broad diversification materially improves that profile.

**Strategy rule:** Trade instruments meeting capital, liquidity, and cost thresholds; scale variable-risk positions according to a combined forecast from multiple smoothed carry forecasts. All non-carry mechanics (optimal position, daily trading, buffering, and portfolio construction) are as in strategy nine.

## What carry is

For a futures position:

\[
\text{Excess return}=\text{spot return}+\text{carry}.
\]

Carry is the excess-return component beyond the change in the underlying spot price. Back-adjusted futures prices cumulate historical excess returns and therefore contain both spot and carry; this chapter seeks to forecast carry separately.

### Sources by asset class

| Asset class | Excess-return decomposition | Normal implication / qualification |
|---|---|---|
| Equity index | spot return + dividends − interest | Carry may be positive or negative depending on dividends versus funding cost. |
| Bonds | spot return + yield − repo rate | Usually positive because longer bond yields are normally above short-term repo; may be negative with an inverted yield curve. The treatment omits bond *roll down*, which many bond traders consider carry. |
| FX | spot return + deposit rate − borrowing rate | A long GBPUSD is described as borrowing USD, converting to GBP, and depositing GBP. G10 carry is usually small; EM currency carry versus USD is often materially positive. Forward-rate details are intentionally ignored. |
| STIR and volatility futures | spot return + current spot price − futures price | A downward-sloping curve normally gives positive carry. STIR spot is the short rate; volatility-futures spot is equity-option implied volatility. |
| Metals | spot return − borrowing cost − storage costs | Normally negative unless negative rates exceed storage costs. Metals have no yield and physical storage/insurance costs. |
| Energy and agriculture | spot return − borrowing cost − storage costs + convenience yield | On average negative carry/upward curves, but can be positive for long periods. Convenience yield reflects expected future supply/demand and can have either sign. |

**Curve terminology:** downward-sloping futures curve / positive carry is commonly called *backwardation*; upward-sloping curve / negative carry is *contango*.

### Illustrative STIR derivation

With a hypothetical Eurodollar curve of 99 at expiry, then 98, 97, 96… for successive three-month expiries, price equals \(100-\text{interest rate}\). If the expiring contract/spot rate stays 1%, a contract bought at 98 expires at 99: the $1 gain is carry because spot did not move. The author assumes equal-length three-month periods solely for exposition. Eurodollar futures were due to switch from LIBOR to SOFR in July 2023 (a source-era note).

### Carry is compensation, not arbitrage profit

If a future is bought at 98 while spot is 99, a $1 expected carry gain is erased by a $1 adverse spot move (*spot drag*). Positive-carry EM FX illustrates the compensation: sudden severe depreciation is the adverse event for which the carry investor is effectively supplying insurance. The backtest later reports about $1.15 of realised return per $1 of expected carry, but this is an historical result, not a guarantee.

## Measuring expected carry

Spot-versus-future comparison is conceptually direct but operationally unattractive: spot data are difficult for many assets (notably commodities), must be time-synchronised, and add cost/complexity. Use two exchange-traded futures instead.

### Raw carry

Preferred, when the held contract is not the first contract:

\[
RC=P_{near}-P_{held}.
\]

Alternative, when the held contract is the first/front contract and no nearer contract exists, assuming a constant curve gradient:

\[
RC=P_{held}-P_{far}.
\]

Here \(P_{near}\), \(P_{held}\), and \(P_{far}\) are same-day closing prices of the nearer, held, and further-out contract respectively; \(RC\) is price units accrued between the two expiries if the relevant spot price is unchanged. Same-exchange closes are synchronised. A quoted second-contract price is usually available even when it is illiquid; in the worst case an accurate reading is available at rolls.

**Examples (November 2021):**

* S&P 500 micro December 2021 (front) 4578.50 and March 2022 4572.00: \(RC=4578.50-4572.00=6.50\).
* Held WTI December 2022 at 62.09 and nearer November 2022 at 62.61: \(RC=62.61-62.09=0.52\). Holding distant December crude is a simplifying approximation noted for later treatment.

### Annualise and risk-adjust

\[
\Delta T=\frac{|\text{months between contract expiries}|}{12},\qquad ARC=\frac{RC}{\Delta T}.
\]

\(\Delta T\) is years between expiries (an approximation in months, rather than exact days); \(ARC\) is annualised raw carry in price units/year. Thus S&P \(6.50/0.25=26.0\), and crude \(0.52/0.083333=6.24\).

Risk-adjusted carry (the raw carry forecast) can be calculated two equivalent ways:

\[
C=\frac{ARC}{\sigma_p\sqrt{16}},\qquad C=\frac{ARC}{\sigma_\%\,P_{held}}.
\]

* \(C\): expected carry in Sharpe-ratio (SR) units; therefore also the expected-SR forecast.
* \(\sigma_p\): estimated **daily** standard deviation of price changes, price units/day; \(\sqrt{16}\) annualises it using the book's 16 trading-day-per-month convention.
* \(\sigma_\%\): estimated **annual** return volatility as a decimal; \(P_{held}\) converts it to annual price-unit volatility.
* \(ARC\), \(P_{held}\): defined above. Use the contemporaneously traded contract price in a backtest, **not** a back-adjusted price.

With 16% annual S&P volatility and 28% crude volatility: \(26/(0.16\times4578)=0.035\); \(6.24/(0.28\times62.09)=0.358\). Despite the smaller price-unit carry, crude has more than ten times the risk-adjusted carry.

## Forecast construction and trading procedure

1. Compute \(RC\), using the preferred near-versus-held method when possible; otherwise front-versus-far.
2. Compute \(\Delta T\), \(ARC\), and risk-adjusted carry \(C\) above. Treat \(C\) as the raw carry forecast.
3. For each span \(N\in\{5,20,60,120\}\) business days, calculate \(SC_{i,N,t}=EWMA_N(C_{i,t})\). Longer spans reduce noise/costs but are less reactive. Natural Gas and correctly measured seasonal contracts may need short spans so they adjust after rolls; longer spans suit most others and also smooth persistent measurement-seasonality errors.
4. Scale every span with scalar 30: \(F_{i,N,t}=30\,SC_{i,N,t}\). This targets average absolute scaled forecast 10: the sample-wide average absolute unscaled carry is about 0.33. A common scalar deliberately preserves lower risk where carry itself is persistently weak.
5. Cap each forecast: \(f_{i,N,t}=\max(\min(F_{i,N,t},20),-20)\).
6. Only retain rule variations affordable for the instrument:
\[
\text{instrument turnover}<\frac{0.15-(\text{cost per trade}\times\text{rolls/year})}{\text{cost per trade}}.
\]
7. Equal-weight the retained capped forecasts, \(RF_{i,t}=\sum_jw_{i,j}f_{i,j,t}\), then apply forecast-diversification multiplier \(FDM_i\): \(CF_{i,t}=RF_{i,t}\times FDM_i\). Cap again at ±20.
8. Feed the capped combined forecast into the strategy-nine position-sizing and buffering equations, construct the optimal position, and trade daily as required.

**Units and limits:** price differences and \(ARC\) are price units; \(C\), smoothed/scaled/capped forecasts, MAC, AMR, and SR are dimensionless SR units. The stated span, scalar, cap, cost rule, FDMs, and 20% risk target are the chapter's implementation choices, not universal constants.

## Noise, seasonality, and instrument-specific failure modes

Raw curve differences are noisy, creating needless turnover. Buffering (strategy eight) and EWMA smoothing address this. Four selected spans are roughly one week, month, quarter, and six months; intermediate spans (e.g. 40 days) are highly correlated with neighbours, and still longer spans did not materially lower cost or improve performance.

* **S&P 500:** sparse historical second-contract data made pre-2000 forecasts blocky; post-2000 estimates are jumpy, with some 2019 noise attributed to poor data. The intended broad signal was short until roughly 2009, then long except 2018–19.
* **Natural Gas:** holding a couple of months ahead permits the more accurate nearer-versus-held method. Carry is persistently negative in May/October and near zero/slightly positive in January/July, consistent with seasonal supply/demand and difficult storage. A fixed December contract is preferred for seasonal commodities where liquid; WTI is traded December-only and so avoids this visible pattern.
* **Bund/Bobl/Bono:** front-versus-second-contract estimation creates quarterly sign flips. For Bund, March/September estimates are strongly positive and June/December negative, while the author says true carry is the reverse; new cheapest-to-deliver bonds issued semi-annually drive this. This is a systematic wrong-sign estimate.
* **Eurostoxx:** March-versus-June is biased high because many constituents pay their largest dividend in April; June is biased low. The issue affects equity futures except total-return DAX30, and is more visible where dividends are annual/semi-annual (especially outside the US).

Possible but deliberately omitted fixes are seasonal-component adjustment, asset-specific bond-yield-curve methods, or avoiding carry in affected assets. Robust systems should tolerate some bad data rather than require perfect cleaning.

## Combining carry spans

Average annual turnover by span: Carry5 5.75, Carry20 3.12, Carry60 1.82, Carry120 1.22. Most of 102 sampled instruments can afford all four; three can afford only the slowest three and four none because rolling consumes the full cost budget.

| Retained variations | Equal forecast weight | FDM |
|---|---:|---:|
| 5, 20, 60, 120 | 0.25 | 1.04 |
| 20, 60, 120 | 0.333 | 1.03 |
| 60, 120 | 0.5 | 1.02 |
| 120 only | 1.0 | 1.0 |

The low FDMs reflect very high return correlations: 5/20 0.96, 5/60 0.89, 5/120 0.84, 20/60 0.94, 20/120 0.89, and 60/120 0.96 (average correlation 0.90–0.93). Equal weighting is retained: although edge spans can be a little less correlated, the diversification gain from changing weights is small.

### Evidence on span choice

Aggregated Jumbo-portfolio results (with buffering/scaling) are very similar: mean annual return 18.9%, 18.3%, 18.5%, 17.7%; costs −1.0%, −0.9%, −0.8%, −0.7%; SR 0.87, 0.87, 0.89, 0.87; and turnover 28.5, 20.7, 16.2, 13.2 for 5/20/60/120 respectively. Daily/weekly/annual skew is mostly slightly negative or near zero, while monthly skew is positive for each span (0.57, 0.35, 0.08, 0.24). Median after-cost SRs across all instruments are 0.27–0.28. The chapter finds no compelling basis to depart from equal weights, including in assets with known seasonal-measurement errors; apparent exceptions are small samples and may be data mining.

## Performance interpretation

For each asset class, **MAC** (median absolute carry) is the median expected SR of carry: reverse the scaling by dividing average scaled forecast by 30, then take the absolute median. **AMR** (adjusted mean return) is annual return divided by the 20% risk target—not realised volatility. \(\%\text{ carry realised}=AMR/MAC\). MAC is carry's SR “promised”; AMR its SR “delivered.” Unlike most forecasts, carry can be compared directly because it is itself expected SR, not merely proportional to it.

Median-instrument results across financial asset classes report that carry strength and realised volatility differ systematically because a common scalar makes positions larger where carry is stronger. Across the source's median instrument, carry delivers 115% of promised carry. Energy and agriculture are the exceptions below 100%, plausibly connected to seasonality. Footnote source averages of absolute unscaled forecasts differ substantially: agriculture 0.82, bonds 0.73, equities 0.17, FX 0.44, metals 0.24, energy 0.72, volatility 1.46.

Carry positions also have persistent directional causes: bonds/equities are usually long; metals usually short. The author nevertheless keeps equal instrument weights rather than asserting performance differences can be reliably identified.

### Jumbo portfolio comparison (Table 48)

| Metric | Long only (strategy 4) | Multiple trend (strategy 9) | Carry (strategy 10) |
|---|---:|---:|---:|
| Mean annual return | 15.4% | 25.2% | 19.7% |
| Costs | −0.8% | −1.2% | −0.8% |
| Average drawdown | −24.7% | −11.2% | −18.6% |
| Standard deviation | 18.2% | 22.2% | 20.8% |
| Sharpe ratio | 0.85 | 1.14 | 0.94 |
| Turnover | 20.7 | 62.9 | 19.2 |
| Skew (monthly) | −0.04 | 0.98 | 0.41 |
| Lower / upper tail | 1.44 / 1.24 | 1.99 / 1.81 | 1.57 / 1.49 |
| Alpha | 0 | 18.8% | 19.1% |
| Beta | 1.0 | 0.43 | 0.06 |

At individual-instrument level skew is generally negative and especially bad in volatility because the strategy is mostly short a positive-skew asset. At aggregate level, uncorrelated crises (FX depreciation, volatility spikes, flights from risk, weather) diversify: carry skew is −0.01 daily, −0.01 weekly, 0.41 monthly, 0.16 annual. The historical carry portfolio lost −8.5% in 2007 and gained 17.9% in 2008. Carry is cheaper than trend and has lower beta/more alpha, but its SR is lower. The cumulative chart shows no profits since late 2017; the author judges this drawdown not exceptionally long/deep against the backtest.

## Figures and what they communicate

* **Figures 39–43:** raw carry forecasts for S&P, WTI, Natural Gas, Bund, and Eurostoxx. They show data sparsity/noise, commodity seasonality, and systematic seasonal measurement errors—not merely smooth economic carry.
* **Figure 44:** cumulative Jumbo returns for long-only benchmark, multiple trend, and multiple carry; it supports the claim of distinct behaviour and a recent carry drawdown.
* **Strategy-ten trading-plan figures:** visually restate the executable procedure: eligible instruments; cost test; four spans; raw-carry choice; annualisation, risk adjustment, smoothing/scaling/capping; equal-weight combination, FDM, and final cap.

## Warnings and boundary conditions

* Curve carry is conditional on unchanged spot; it does not remove spot risk.
* Front-versus-far estimation assumes a constant futures-curve gradient and can be systematically wrong where contract seasonality or delivery mechanics distort adjacent prices.
* All inputs must be aligned to the contract actually traded at the time; do not calculate this on back-adjusted prices.
* Smoothing trades responsiveness for lower turnover and may not cure a fundamentally wrong estimate.
* Results are a backtest with the author's data, cost model, buffering, risk target, asset coverage, and definitions; they are descriptive, not a performance promise.

## Connections and key takeaways

* **Strategy 1:** excess-return decomposition, back-adjusted prices, fixed-month crude treatment, and long-only comparator.
* **Strategy 7:** a forecast is proportional to expected risk-adjusted return; carry is unusually an expected SR directly.
* **Strategy 8:** buffering to manage trading cost.
* **Strategy 9:** variable-risk sizing, multiple-rule combination, cost test, FDM, forecast capping, and the trend comparator.
* **Strategy 11:** combines trend and carry; preferred source-era allocation is 60% trend / 40% carry (not derived in this chapter).

**Bottom line:** estimate carry from the futures curve, annualise and risk-adjust it, smooth and cap several affordable spans, combine them with near-unity FDM, and deploy via the existing variable-risk framework. Do it as a diversified risk-premium sleeve, not as a presumed free return.

## Glossary

**Carry:** excess return beyond spot return. **Spot drag:** adverse spot movement that offsets carry. **Raw carry / annualised raw carry:** contract-price spread before / after converting to a yearly rate. **Convenience yield:** value/market expectation attached to immediate commodity availability. **Repo rate:** short-term bond-financing rate. **Futures curve:** prices across expiries. **Backwardation / contango:** downward / upward futures curve, conventionally positive / negative carry. **EWMA:** exponentially weighted moving average. **Forecast scalar:** multiplier turning an SR-unit forecast into the book's forecast scale. **FDM:** forecast diversification multiplier. **MAC:** median absolute carry, the promised expected SR. **AMR:** annual return divided by 20% risk target. **Tail ratio:** lower/upper-tail statistic used alongside skew.

## Source limitations

All extracted formulas, tables, figures, and claims are from the assigned chapter only. Formula glyphs were verified from the chapter's equation and trading-plan images; the chapter does not define every pre-existing strategy-nine sizing/buffering variable, so those mechanics are referenced rather than reconstructed.
