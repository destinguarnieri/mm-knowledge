# Strategy Four — Buy and Hold Portfolio with Variable Risk Position Sizing

## Purpose and central argument

Strategy four extends strategy three’s long-only, variable-risk position sizing from one futures instrument to a **portfolio**. Split capital into instrument-level sub-strategies, each a version of strategy three. Since each sub-strategy targets approximately the same risk, an instrument’s capital allocation is also its intended share of portfolio risk. A portfolio accesses diversified risk premia, reduces dependence on any one instrument, and can use futures leverage to restore the desired overall risk after diversification reduces it.

The strategy is intentionally agnostic about forecasting returns: subject to liquidity, trading-cost, and minimum-capital constraints, it is long the selected instruments. The historical results benefit from the fact that most instruments in the author’s data set rose over the preceding 50 years; that historical tailwind may not recur.

## Strategy definition and operating rule

**Strategy four:** buy and hold a portfolio of instruments, each with its position scaled using a variable risk estimate.

All elements not changed below are identical to strategy three. For every selected instrument, calculate a risk-scaled long futures position; apply its instrument weight and the portfolio’s instrument diversification multiplier (IDM); round to tradable contracts.

### Position-sizing equations

The source presents its equations as images; their mathematical transcription is below. Symbols and units are preserved or made explicit from the surrounding text.

Baseline strategy-three sizing:

\[
N_i = \frac{C\,\tau}{M_i P_i F_i\sigma_{\%,i}}
\]

Strategy-four sizing:

\[
N_i = \frac{C\,w_i\,\tau}{M_i P_i F_i\sigma_{\%,i}}
\]

After correcting for portfolio diversification:

\[
N_i = \frac{C\,IDM\,w_i\,\tau}{M_i P_i F_i\sigma_{\%,i}}
\]

Where:

| Symbol | Meaning | Units / conditions |
|---|---|---|
| \(N_i\) | Number of futures contracts for instrument \(i\) | Contracts; subsequently rounded to an executable whole number. |
| \(C\) | Total trading capital | Account-currency amount. |
| \(w_i\) | Instrument weight | Fraction of total capital/risk allocation; weights are non-negative and should sum to 1 across the portfolio. |
| \(\tau\) | Annual risk target | Annualized standard-deviation fraction, e.g. 0.20 for 20%. |
| \(IDM\) | Instrument diversification multiplier | Dimensionless, normally >1 for a diversified portfolio; used to gear the whole portfolio back to its target risk. |
| \(M_i\) | Futures contract multiplier | Underlying/currency value per quoted price unit. |
| \(P_i\) | Futures price | Instrument quote units. |
| \(F_i\) | FX rate | Account-currency conversion factor for instrument \(i\). |
| \(\sigma_{\%,i}\) | Variable estimate of current percentage risk | Annualized return standard deviation, as a decimal. |

**Worked risk-parity sizing example.** With \(C=\$1{,}000{,}000\), \(\tau=20\%\), and \(w=0.50\) for each leg:

\[
N_{S\&P500}=\frac{1{,}000{,}000(0.50)(0.20)}{5(4500)(1)(0.16)}=27.8\Rightarrow28
\]

\[
N_{US10}=\frac{1{,}000{,}000(0.50)(0.20)}{1000(130)(1)(0.08)}=9.62\Rightarrow10
\]

## Why diversification changes risk

A conventional 60% equity / 40% bond cash allocation can concentrate roughly 75% of risk in equities when their annualized standard deviations are about 16% and 8%, respectively. Cash allocation adjusted for those risk levels would place only 42% in equities, but it would lower expected return. Futures allow a risk-parity allocation to be levered to the desired risk/return level instead.

In the two-instrument example, equal 50% instrument weights produced individual risks of 11.5% and 10.0%, roughly half the 20% target because each sub-strategy receives half the capital. The aggregate risk was 15.1%, not ~20%, because the sub-strategy-return correlation was effectively zero (−0.004). Mean returns add, whereas volatility does not add linearly when returns are not perfectly correlated, improving aggregate Sharpe ratio.

Correlation is only an imperfect, linear approximation to co-movement. Aggregate skew and lower-tail measures were roughly averages of the individual values, implying both strategies can still suffer in the same market environments; diversification did improve upper tail in this example. Correlation of *trading sub-strategy returns* is not necessarily correlation of the underlying instruments; the difference becomes greater for complex long/short strategies, and strategy correlations are generally lower than underlying-return correlations.

### IDM

The **IDM** is chosen to make expected aggregate risk equal \(\tau\). A rough realized-backtest estimate is:

\[
IDM \approx \frac{\text{target risk}}{\text{realized aggregate risk}}
\]

For risk parity, \(20\%/15.1\%=1.32\). Multiplying all positions by 1.32 lifted aggregate standard deviation to 19.9% and mean return to 15.7%. Leverage also scaled average drawdown, turnover, and costs; Sharpe ratio and other risk-adjusted measures were unchanged apart from rounding effects. The chapter notes the required leverage varied from 1.5 to 6.0, making a non-futures implementation difficult; ETFs above 2× leverage are difficult to obtain and characterized as particularly dangerous.

**Important limitation:** IDM depends on time-varying correlations and on the available instrument set. A single full-backtest IDM is weak in-sample fitting and will generally be too high early (fewer instruments) and too low later. The book’s later backtests instead use rolling, backward-looking IDM estimates.

## Strategy variations

### Risk parity

Allocate 50% each to S&P 500 micro futures and US 10-year bond futures, then apply the position formula. It demonstrates equal expected risk allocation across equity and bond sub-strategies, not equal notional cash exposure.

| Metric | S&P 500 | US 10-year | Aggregate, no IDM | Aggregate, IDM 1.32 |
|---|---:|---:|---:|---:|
| Mean annual return | 6.2% | 5.6% | 11.8% | 15.7% |
| Mean annual costs | −0.03% | −0.17% | −0.20% | −0.26% |
| Average drawdown | −9.4% | −7.5% | −6.9% | −9.0% |
| Standard deviation | 11.5% | 10.0% | 15.1% | 19.9% |
| Sharpe ratio | 0.54 | 0.56 | 0.79 | 0.79 |
| Turnover | 2.3 | 5.0 | 5.1 | 6.8 |

With IDM, the individual results were: S&P 500 return 8.3%, costs −0.04%, drawdown −12.4%, volatility 15.2%, SR 0.54, turnover 5.1; US 10-year return 7.5%, costs −0.23%, drawdown −9.7%, volatility 13.2%, SR 0.57, turnover 5.0. Table 12 additionally reports skew/lower-tail/upper-tail: S&P −0.68/1.76/1.21; US 10-year −0.07/1.28/1.19; aggregate −0.20/1.60/1.31. Figure 21 compares the two strategy-three account curves with the aggregate risk-parity curve and visually communicates the benefit of aggregation.

### All Weather

Risk parity’s strong historic performance is attributed to equity/bond repricing (lower rates and higher P/E ratios) and their unusually low correlation in a low-inflation, risk-appetite-driven era. The source warns that elevated inflation can hurt bonds and equities together and raise their correlation, as in the 1970s. Add instruments with possible inflation sensitivity.

A typical cash-weight All Weather recipe is 30% US stocks, 40% long Treasuries, 15% intermediate Treasuries, 7.5% diversified commodities, and 7.5% gold. The author’s **instrument/risk weights** instead are:

- 25% S&P 500 micro futures.
- 25% bonds: 12.5% US 10-year and 12.5% US 5-year futures.
- 25% diversified commodities: 12.5% WTI Crude Oil mini and 12.5% Corn futures.
- 25% Gold micro futures.

Construct this by splitting into four equal asset-class buckets, then splitting bonds and commodities again. With IDM 1.81, aggregate volatility was 19.1%, close to the 20% target. The extra diversification did not beat risk parity historically: crude, gold, and especially corn had lower SRs, depressing the aggregate; proponents may nevertheless expect future equity/bond returns to be lower and commodities/gold to benefit under inflation.

| Metric | S&P | US 10y | US 5y | Crude | Corn | Gold | Aggregate |
|---|---:|---:|---:|---:|---:|---:|---:|
| Mean annual net return | 5.2% | 2.8% | 2.8% | 1.8% | 0.0% | 2.0% | 14.7% |
| Mean annual costs | −0.03% | −0.09% | −0.07% | −0.09% | −0.03% | −0.04% | −0.34% |
| Average drawdown | −9.2% | −3.2% | −3.3% | −7.2% | −14.3% | −23.8% | −10.2% |
| Standard deviation | 10.1% | 4.6% | 4.6% | 5.0% | 4.8% | 10.1% | 19.1% |
| Sharpe ratio | 0.52 | 0.60 | 0.61 | 0.36 | 0.00 | 0.19 | 0.77 |
| Turnover | 5.2 | 5.1 | 5.1 | 5.1 | 5.0 | 5.3 | 9.3 |
| Skew | −0.48 | −0.04 | −0.01 | −0.22 | 0.11 | 0.47 | −0.26 |
| Lower tail | 1.83 | 1.39 | 1.42 | 1.57 | 1.40 | 1.72 | 1.50 |
| Upper tail | 1.21 | 1.27 | 1.34 | 1.28 | 1.55 | 1.52 | 1.21 |

The S&P and US-10-year figures differ slightly from earlier results because this backtest begins later to accommodate the shorter histories of US 5-year and crude futures.

## Generalized risk-premia portfolio

### Instrument eligibility and capital constraint

Use strategy-three selection criteria:

- Risk-adjusted cost below 0.01 SR units.
- Average daily volume at least 100 contracts and annualized dollar standard deviation above $1.5 million.
- At least four contracts can be held with available capital.

For instrument \(i\), the required capital to hold four contracts is:

\[
C_{min,i}=\frac{4M_iP_iF_i\sigma_{\%,i}}{IDM\,w_i\,\tau}
\]

This is higher than strategy three because only \(w_i\) of capital is allocated to an instrument. Example: if strategy three needs $50,000 for four contracts, two equal-weight instruments require $100,000 with IDM=1; IDM=1.3 reduces this to $83,333, still above $50,000.

### Setting weights: principles and handcrafting algorithm

Unlike conventional asset allocation, these are allocations of risk capital to equal-risk sub-strategies, so the author says only a correlation matrix of sub-strategy returns is needed—not a covariance matrix. With reasonable \(\tau\), futures leverage means no efficient-frontier tradeoff is required: choose weights, then apply IDM, subject to margin. Negative weights are prohibited because loss-expected sub-strategies should not be traded.

Potential weight drivers are pre-cost SR, costs, and correlation/diversification. The chapter dismisses estimating relative pre-cost SRs (except poor volatility instruments such as VIX/VSTOXX) for lack of evidence; screens out high-cost instruments so cost optimization is negligible; and says minimum-capital requirements should be checked but should not drive weights. For example, forcing weights from 50/50 to 40/60 merely to accommodate a $60k-minimum instrument makes an unsupported return bet; modest changes may be acceptable, extreme ones are not.

**Handcrafting procedure:**

1. Divide eligible instruments into asset classes and give each asset class an equal share of 100% weight.
2. Within each class, divide instruments into similar groups and give each group an equal fraction of that class’s share.
3. Within each group, divide weight equally among instruments.
4. Add intermediate layers as appropriate; groupings are subjective and can differ by class.

Suggested classes/groups: Agricultural (grain, index, meats, softs); Bonds and interest rates (government bonds, short-term rates, swaps); Equity (US, European, Asian); FX (developed, emerging, cross); Metals (crypto, industrial, precious); Energies (gas, crude oil, products); and Volatility (US, European, Asian). The author explicitly notes classifications can be changed—for example, crypto may be FX or its own sector.

**Worked allocation illustration:** For 16 instruments across seven asset classes, first allocate 14.3% to each class. Divide agricultural into grains and softs (7.14% each), bonds/rates into government bonds and interest rates (7.14% each), equity into American and European (7.14% each), metals into precious and industrial (7.14% each); classes with a sole instrument stay at 14.3%. Final examples: each of three government-bond futures gets 2.38%; Coffee and Orange Juice get 3.57% each; NASDAQ gets 7.14%; NOKUSD, Ethanol, and VIX each get 14.3%.

### IDM approximation by instrument count

| Instruments | IDM | Instruments | IDM |
|---|---:|---|---:|
| 1 | 1.00 | 2 | 1.20 |
| 3 | 1.48 | 4 | 1.56 |
| 5 | 1.70 | 6 | 1.90 |
| 7 | 2.10 | 8–14 | 2.20 |
| 15–24 | 2.30 | 25–29 | 2.40 |
| 30+ | 2.50 | | |

These are only for a relatively diversified set; they are invalid for, for example, 30 equity futures.

## Automated instrument-selection algorithm

The aim is the best tradeoff between diversification and costs while satisfying minimum capital for every chosen instrument. It is not practical by hand and requires code (the author says implementation is available on the book website).

1. Define possible instruments: exclude markets that are legally unavailable or fail cost/liquidity thresholds. Do not pre-filter on minimum capital.
2. Choose the first instrument. Assume a likely final portfolio size to set provisional \(w\) and IDM (example: ten equal-weight instruments: \(w=10\%\), IDM=2.2). Compute each candidate’s four-contract minimum capital; discard candidates above available capital; choose the remaining candidate with lowest risk-adjusted cost.
3. Estimate current portfolio SR. Assume the same notional pre-cost annual \(SR^*\) for every instrument and equal turnover \(T\). Then:

\[
SR_i=SR^*-T c_i
\]
\[
\mu_i=\tau[SR^*-Tc_i]
\]
\[
\mu_{i,p}=w_i\,IDM\,\tau[SR^*-Tc_i]
\]
\[
\mu_p=\sum_i w_i\,IDM\,\tau[SR^*-Tc_i]
\]
\[
\sigma_p=IDM\,\tau\sqrt{\mathbf w\Sigma\mathbf w^{\prime}}
\]
\[
SR_p=\frac{\sum_iw_i[SR^*-Tc_i]}{\sqrt{\mathbf w\Sigma\mathbf w^{\prime}}}
\]

Here \(c_i\) is instrument \(i\)’s risk-adjusted cost, \(T\) is estimated turnover, \(\mu\) is expected annual mean return, \(\mathbf w\) is the vector of weights, and \(\Sigma\) is the correlation matrix of sub-strategy returns. Matrix multiplication occurs inside the square root. IDM and \(\tau\) cancel from SR, as SR should be invariant to leverage and risk target. For one instrument the expression simplifies to \(SR^*-Tc_i\). The source’s strategy-three example uses \(SR^*=0.3\) and \(T\approx7.0\) (turnover about three times yearly plus quarterly rolls). Do **not** substitute a given instrument’s realized backtested SR: the chapter warns against it.
4. For each unselected instrument, build a trial portfolio, allocate weights (handcrafted or equal-weight approximation), estimate IDM, reject it if any constituent fails four-contract minimum capital, and calculate expected trial SR.
5. Add the candidate with the highest eligible trial SR. If none is eligible, stop.
6. Stop if the new current-portfolio expected SR is more than 10% below the highest current-portfolio SR seen. A small fall is permitted because SR can dip before rising on subsequent additions.

Example selections stated in the chapter: at $100,000, the algorithm selected 16 markets—Korean KOSPI; NASDAQ micro; Gold micro; Eurodollar; Korean 3-year/10-year; US 2-year; German 2-year Schatz; Italian 10-year BTP; Lean hogs; JPY/USD, MXP/USD, GBP/USD, NZD/USD; Henry Hub Natural Gas mini; WTI Crude mini. At $500,000 it selected 27 instruments; at $1m, 36.

## Jumbo portfolio test

The **Jumbo portfolio** contains 102 liquid, sufficiently low-cost instruments with at least one year of data and assumes $50m so minimum capital is not binding. Weights are handcrafted; final rolling IDM is 2.47. Its class counts are Agricultural 13, Bonds/Rates 21, Equity 34, FX 17, Metals/Crypto 9, Energies 6, Volatility 2. Data-history counts: 18 have ≥40 years, 28 >30, 40 >20, 65 >10, and 87 >5.

| Metric | Median individual instrument | Aggregated Jumbo |
|---|---:|---:|
| Mean annual return | 6.9% | 15.4% |
| Mean annual costs | −0.3% | −0.8% |
| Average drawdown | −18.7% | −24.7% |
| Standard deviation | 20.9% | 18.2% |
| Sharpe ratio | 0.32 | 0.85 |
| Turnover | 2.7 | 20.7 |
| Skew | −0.09 | −0.04 |
| Lower tail | 1.56 | 1.44 |
| Upper tail | 1.29 | 1.24 |

Diversification increases SR/returns, improves skew, and reduces tail magnitudes, but average drawdown is worse because correlation does not capture extreme co-movement. Costs rise with the extra leverage; turnover rises mainly because there are many more instruments, not proportionally in costs. Figure 22 shows strong performance apart from a large early-1980s drawdown, when only 22 instruments were live and agricultural/currency/metals exposure was concentrated; those groups suffered during monetary tightening after their 1970s inflation performance.

The Jumbo results represent an institutional fund of at least $50m, while a single arbitrary instrument represents the other extreme. A retail portfolio of roughly 5–20 instruments should lie between them. The test excludes futures that were formerly liquid/cheap but are not now, and excludes delisted contracts such as pork belly futures; the author acknowledges potential survivorship bias, while judging it less severe in futures than in small-cap equities. A version that shorts VIX/VSTOXX would have slightly higher SR and slightly worse skew/lower percentile ratio, but only 5.4% of total weight is volatility, so the aggregate impact is small.

## Risk target by portfolio breadth

The chapter relates target risk to roughly half expected SR (half theoretical Kelly leverage). Its 20% annual volatility target is prudent only for expected SR ≥0.40. A single instrument’s Jumbo-median SR of 0.32 does not support 20%; the source recommends:

- One instrument: 10% target risk.
- Two to six instruments: interpolate from 10% to 20%.
- 20% only with at least one instrument from each of the seven specified asset classes.
- Up to 25% only with at least two instruments from each class; do not exceed 25%.

Despite an aggregate historical SR of 0.85 (and a suggestion that 0.85/2 = 42.5% could follow mechanically), the author is wary: strategy four is long-only and its SR is upward-biased by historical trends unlikely to repeat. The author personally uses roughly a 25% risk target despite a backtested SR above 1.0.

## Warnings, assumptions, and edge cases

- Backtests and weight selection do not establish that one instrument’s pre-cost performance will persist; do not overweight based on observed backtested SR.
- Costs can be ignored for *weight optimization* only after applying the 0.01-SR-unit cost screen. The chapter’s extreme two-instrument example says optimal 55/45 vs. equal 50/50 reduces expected annual return by only 0.06% when one instrument has zero costs and the other costs 0.01 SR units per trade.
- The selection algorithm assumes identical notional pre-cost SRs and equal turnover. Its estimates are decision heuristics, not a full backtest.
- Do not use generic IDM-count values for a concentrated portfolio; calculate/roll IDM using historical information where possible.
- Do not confuse cash weights (e.g., the published All Weather recipe) with this chapter’s risk/instrument weights.
- Ensure margin remains feasible; leverage is described as workable only for non-excessive risk targets.
- Long-only volatility strategies can be expected to lose money. Excluding loss-making systems only because of a negative pre-cost SR can itself overfit; high costs provide a more defensible exclusion reason.

## Connections and glossary

**Connections:** Strategy three supplies variable-risk sizing, instrument cost/liquidity screens, and the rest of the trading plan. Strategy two supplied risk-target calibration. Appendix B explains IDM calculation. The next chapter moves from long-only investing to return forecasting so instruments are not always held long. The chapter also references the efficient frontier, CAPM market portfolio, Kelly criterion, and *Systematic Trading* for broader optimization discussion.

**Glossary:** asset class; cash weight; correlation matrix; covariance matrix; efficient frontier; futures multiplier; IDM/instrument diversification multiplier; instrument weight; long-only; minimum capital; risk allocation/risk capital; risk-adjusted cost; risk parity; Sharpe ratio (SR); sub-strategy; target risk \(\tau\); turnover; variable risk estimate; volatility targeting; Jumbo portfolio.

## Key takeaways

1. Allocate instrument weights to equal-risk, volatility-scaled sub-strategies; use IDM to restore total portfolio risk after diversification.
2. Favor broad, cross-asset diversification, but do not mistake low linear correlation for protection from joint drawdowns.
3. Screen costs, liquidity, and minimum capital; use structured asset-class diversification rather than fragile return forecasts to set weights.
4. Scale risk conservatively with portfolio breadth and treat the historic long-only result as potentially optimistic.
