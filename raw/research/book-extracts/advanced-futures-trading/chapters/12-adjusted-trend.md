# Strategy twelve: Adjusted trend

## Purpose and central argument

Trend forecasts from exponentially weighted moving-average crossover (EWMAC) filters are useful expected risk-adjusted returns, but their predictive relationship with subsequent returns weakens—and sometimes reverses—at extreme forecast values. This strategy replaces ordinary forecast capping for selected EWMAC speeds with symmetric mappings intended to reduce exposure at extremes while preserving the forecast scale. The author’s final judgment is **not to trade this strategy**: modest performance changes do not justify its additional complexity.

## Strategy definition

Apply a probability-of-reversal adjustment to the forecast of any strategy using EWMAC trend filters and position sizing based on a capped forecast. The adjustment is applied after the forecast has been scaled, and it replaces the ordinary forecast-capping stage.

## Background: forecast versus realised risk-adjusted return

- A forecast is an expected risk-adjusted return. A linear forecast-and-cap scheme assumes that trend strength is linearly related to expected risk-adjusted return up to the normal cap of -20 or +20.
- The analysis pools data from all 102 instruments in the Jumbo portfolio because risk-adjusted returns can be compared directly across instruments. Initial scatter plots use scaled but **uncapped** forecasts.
- Realised return horizons are tailored to rule turnover rather than held constant. With 256 business days per year, the holding-period estimate is:

  \[
  H = \lceil 256/T \rceil
  \]

  where \(H\) is the forward return horizon in business days and \(T\) is annual turnover (times/year). For EWMAC2, \(256/98.5=2.6\), so the analysis uses the next 3 daily returns; for EWMAC64, \(256/5.2=49.2\), so it uses 50 days.
- Returns are normalized using the **risk estimated when the forecast was made**, because position size is set from that estimate. Using realized risk over the horizon would downplay volatility increases; for EWMAC2, a standard deviation estimated from only three daily observations would also be very noisy.

## Evidence and interpretation

### Forecast bins and uncertainty

Figure 47 replaces an unreadable point cloud with 30 equal-frequency forecast bins (3.33% each). Each cross communicates:

- horizontal span: forecast range in the bin;
- horizontal/vertical intersection: median forecast for the bin;
- vertical center: median realized risk-adjusted return;
- vertical span: median return plus/minus \(2\omega\), where \(\omega\) is the sampling error of that bin’s risk-adjusted return.

The text’s description of the extreme negative EWMAC2 bin says forecasts range roughly from -71 (truncated) to -21 and have median subsequent risk-adjusted return about 0.077 (range 0.044–0.11), versus about 0.05 in the next bin (-21 to -19). Thus a forecast of -30 should not necessarily be made 50% more bearish than -20; in the pooled evidence, it had a more positive subsequent median return. Extreme +30 forecasts likewise did not have a higher median return than +20 forecasts. Only about 6% of EWMAC(2,8) forecasts have absolute value over 20, supporting capping under high uncertainty.

### Results by EWMAC speed

- **EWMAC2:** positive forecast/return relationship only roughly between -5 and +5. Outside that range, the effect becomes mean reversion.
- **Progressively slower filters:** the mean-reversion effect disappears and the response becomes more linear.
- **EWMAC64:** trend works to a point, but the response above +10 becomes muddled; there is no comparable effect for negative forecasts.
- These patterns accord with Strategy 9’s performance results: filters with clearer linear response, such as EWMAC16, have better return statistics; EWMAC2 is the weakest variation even before costs.
- **Equities-only check (Figure 53):** EWMAC2 and EWMAC4 show a strong rebound after a strong negative trend, without a symmetric response to strong positive trends. VIX-like volatility markets show the opposite: a strong positive VIX trend tends to be followed by a sharp fall.

### Volatility interpretation and constraints

A trend forecast is the difference between two smoothed prices divided by the standard deviation of price changes. An unusually large forecast can therefore arise from a large price trend, unusually low recent volatility, or their interaction.

- Equity drawdowns commonly coincide with greater risk, which tends to suppress extreme negative forecasts; smooth bull markets more often generate extreme positive forecasts.
- Risk-on and risk-off instruments can display opposite patterns. The pooled symmetric mean reversion of fast filters may be the combination of opposing effects plus instruments without a clear pattern.
- The equity-only estimates are not statistically strong: their vertical uncertainty intervals mostly overlap. The author therefore advises **against asset-class-specific**, and especially single-instrument, forecast adjustments.
- Any global adjustment should be simple and symmetric. Separate adjustments for trend strength and volatility are tempting, but the author defers direct control of volatility’s profitability effect to Strategy 13.

## Forecast mappings

Let \(F\) be the original **scaled** EWMAC forecast, before normal capping. The resulting values below are the adjusted/capped forecast used for position sizing. Forecast units are the book’s forecast scale; no physical units apply.

### Mapping choice

| Filter | Replacement for normal cap | Rationale stated in chapter |
|---|---|---|
| EWMAC2 | Double V | Extreme fast-trend forecasts exhibit mean reversion. |
| EWMAC4 | Scale and cap at absolute 15 | Extreme response is weaker than linear forecast scaling. |
| EWMAC64 | Scale and cap at absolute 15 | Positive forecasts above +10 have a muddled response. |
| All others | No change | Evidence does not support an adjustment. |

### EWMAC2: double-V mapping

\[
f_{DV}(F)=
\begin{cases}
0,&F<-20\\
-40-2F,&-20\le F<-10\\
2F,&-10\le F\le+10\\
40-2F,&+10<F\le+20\\
0,&F>+20
\end{cases}
\]

At modest values this doubles the otherwise used forecast. The multiplier preserves the target average absolute forecast value; without it, the mapping would have the wrong scaling and too low an average absolute forecast. Its cost is higher trading turnover/costs. At extreme values the mapping reduces exposure to zero rather than continuing in the trend direction.

### EWMAC4 and EWMAC64: scale-and-cap mapping

\[
f_{SC}(F)=
\begin{cases}
-18.75,&F<-15\\
1.25F,&-15\le F\le+15\\
18.75,&F>+15
\end{cases}
\]

The threshold is an absolute original forecast of 15 instead of the usual 20. Both the forecast and threshold outcome are multiplied by 1.25 to preserve forecast scaling: \(15\times1.25=18.75\).

## Implementation procedure

1. Generate and scale each EWMAC forecast as in the existing trend system.
2. Before ordinary capping, identify its EWMAC speed.
3. For EWMAC2, substitute \(f_{DV}(F)\); for EWMAC4/EWMAC64, substitute \(f_{SC}(F)\); leave other speeds unchanged.
4. Use the resulting capped adjusted forecast to size the position under the existing system.
5. Keep the adjustment global/symmetric; do not fit separate rules by asset class or instrument from this evidence.
6. Assess trading costs: EWMAC2 is typically too expensive for most markets, so stand-alone results exaggerate its practical relevance.

## Figures and what they show

| Item | Content and implication |
|---|---|
| Figure 46 | Raw EWMAC2 scatter of uncapped forecast versus following three-day realized risk-adjusted return, pooled across instruments; too dense to interpret directly. |
| Figure 47 | Same EWMAC2 relationship as 30 binned crosses; extreme forecasts have wide uncertainty and non-monotonic results, motivating capping. |
| Figure 48 | Capped EWMAC2 plot; positive relationship mainly confined to approximately -5 to +5. |
| Figures 49–52 | Corresponding capped plots for EWMAC4, EWMAC8, EWMAC32, and EWMAC64. Slower filters are more linear, while EWMAC64 weakens above +10. |
| Figure 53 | Six EWMAC speeds pooled across equity instruments using four buckets; fast filters show a strong rebound after extreme negative trends, but uncertainty is too high for robust asset-class-specific fitting. |
| “The role of volatility” box | Explains why forecast magnitude combines trend and recent volatility and why asymmetrical cross-asset adjustments are risky. |
| Strategy 12 trading-plan graphic | States that the adjustments apply wherever one or more trend filters size positions using a capped forecast. The graphic contains no additional legible text in the XHTML extraction. |

## Backtest results

### Table 57 — EWMAC2, aggregate Jumbo portfolio

| Metric | Unadjusted | Double V adjusted |
|---|---:|---:|
| Mean annual return (gross) | 13.0% | 12.6% |
| Mean annual return (net) | 3.5% | -4.5% |
| Costs | -9.3% | -16.7% |
| Average drawdown | -161.7% | -171.4% |
| Standard deviation | 22.9% | 20.5% |
| Sharpe ratio | 0.15 | -0.22 |
| Turnover | 381 | 704 |
| Skew | 1.32 | 0.07 |
| Lower tail | 1.94 | 1.43 |
| Upper tail | 2.28 | 1.61 |
| Annualised alpha (gross) | 10.2% | 10.9% |
| Annualised alpha (net) | 0.9% | -5.8% |
| Beta | 0.17 | 0.08 |

Interpretation: gross alpha improves slightly, but gross return falls and costs explode; net return, net alpha, Sharpe, drawdown, and distributional tail measures worsen.

### Table 58 — EWMAC4 and EWMAC64, aggregate Jumbo portfolio

| Metric | EWMAC4 unadj. | EWMAC4 adj. | EWMAC64 unadj. | EWMAC64 adj. |
|---|---:|---:|---:|---:|
| Mean annual return (gross) | 19.6% | 21.5% | 22.5% | 25.3% |
| Mean annual return (net) | 14.8% | 16.2% | 21.5% | 24.2% |
| Costs | -4.7% | -5.3% | -1.0% | -1.1% |
| Average drawdown | -23.1% | -23.7% | -16.0% | -17.2% |
| Standard deviation | 23.1% | 24.9% | 22.3% | 24.4% |
| Sharpe ratio | 0.64 | 0.65 | 0.96 | 0.95 |
| Turnover | 195 | 220 | 27.5 | 28.5 |
| Skew | 0.75 | 1.38 | 0.61 | 0.47 |
| Lower tail | 1.98 | 1.85 | 1.90 | 1.77 |
| Upper tail | 2.15 | 1.99 | 1.63 | 1.63 |
| Annualised alpha (gross) | 15.9% | 17.5% | 14.6% | 15.9% |
| Annualised alpha (net) | 11.2% | 12.3% | 13.6% | 14.8% |
| Beta | 0.25 | 0.27 | 0.53 | 0.56 |

Interpretation: EWMAC4 shows a slightly higher Sharpe (0.64 to 0.65); EWMAC64’s risk-adjusted performance falls slightly (Sharpe 0.96 to 0.95) despite improved alpha.

### Table 59 — Full Strategy 11 Jumbo portfolio

Strategy 11 combines carry and trend and assigns each instrument only to rules tradable without excessive cost. The EWMAC2 adjustment affects only 11 instruments and has 10% forecast weight in those, producing no aggregate effect by itself.

| Metric | Strategy 11 unadj. | Adjust EWMAC2 | Adjust EWMAC4, 64 | Adjust all 2, 4, 64 |
|---|---:|---:|---:|---:|
| Mean annual return | 26.5% | 26.5% | 27.1% | 27.3% |
| Costs | -1.1% | -1.1% | -1.1% | -1.1% |
| Average drawdown | -8.9% | -8.9% | -9.0% | -9.1% |
| Standard deviation | 20.9% | 20.9% | 21.2% | 21.2% |
| Sharpe ratio | 1.27 | 1.27 | 1.27 | 1.29 |
| Turnover | 46.5 | 46.5 | 47.3 | 45.6 |
| Skew | 0.76 | 0.76 | 0.70 | 0.70 |
| Lower tail | 1.86 | 1.86 | 1.82 | 1.84 |
| Upper tail | 1.75 | 1.75 | 1.71 | 1.70 |
| Alpha | 22.3% | 22.3% | 22.5% | 22.6% |
| Beta | 0.30 | 0.30 | 0.32 | 0.33 |

The EWMAC4/64-only and all-adjustments variants show small gains, but the author calls neither result compelling.

## Warnings, edge cases, and limitations

- Do not infer robust causal explanations from folklore such as a “dead cat bounce”; different asset classes can have opposite behavior.
- Do not use asset-class-specific effects here: estimates become too noisy, and fitting one instrument is described as futile.
- A symmetric global adjustment is a robustness constraint, not evidence that all asset classes are symmetric.
- Extreme forecasts are rare and uncertainty intervals overlap substantially; this is the core argument for capping rather than extrapolating linear sizing.
- The double-V mapping deliberately increases activity for modest EWMAC2 forecasts and can sharply raise costs.
- Stand-alone results run each filter on every Jumbo instrument, an assumption the author says would not be used in practice; EWMAC2 is particularly too expensive for most markets.
- An alternative implementation—trading momentum alongside a rare extreme-momentum position that offsets momentum exposure—looks nearly identical in aggregate, but trades too rarely to assess its individual performance well.

## Connections to other chapters

- **Part One:** introduces scaling positions; this chapter addresses the added reversal risk when calm strong trends create especially large positions.
- **Strategy 7:** introduced forecast-based trend sizing and forecast capping; this chapter supplies empirical justification for capping/adjustment.
- **Strategy 9:** supplies EWMAC variants and their return statistics (tables 30–31); this chapter’s response plots explain their relative performance.
- **Strategy 11:** provides the realistic carry-and-trend mixed system used in Table 59.
- **Strategy 13:** will control directly for the impact of volatility levels on trading-rule profitability.

## Key takeaways

1. Forecast magnitude does not reliably imply proportionally higher expected return at extreme values.
2. Forecast capping is defensible because extremes are rare, noisy, and can exhibit mean reversion.
3. The chapter’s simple symmetric mappings are double-V for EWMAC2 and scale-and-cap at 15 (with 1.25 scaling) for EWMAC4 and EWMAC64.
4. Backtests show only small or mixed benefits, while double-V substantially worsens EWMAC2 net economics through cost.
5. The author does not recommend implementing Strategy 12 despite its use in some quantitative futures hedge funds.

## Glossary

- **EWMAC:** exponentially weighted moving-average crossover trend filter.
- **Forecast:** expected risk-adjusted return used for position sizing.
- **Scaled forecast:** forecast rescaled to the system’s desired forecast magnitude before capping.
- **Forecast capping:** limiting forecast magnitude to prevent exposure from rising indefinitely.
- **Double-V mapping:** EWMAC2 replacement mapping that doubles modest forecasts, tapers them to zero between absolute 10 and 20, and is zero beyond absolute 20.
- **Scale-and-cap mapping:** mapping that multiplies forecasts by 1.25 and caps output at +/-18.75 once original forecast magnitude exceeds 15.
- **Turnover:** annual trading frequency used to infer holding period.
- **Realised risk-adjusted return:** forward return normalized by estimated risk at forecast formation.
- **Mean reversion:** tendency for price to move opposite a preceding extreme move.
- **Dead cat bounce:** temporary rebound after a sharp/prolonged decline; cited as folklore, not as a verified causal explanation.
- **Omega (\(\omega\)):** sampling error of the risk-adjusted return in a forecast bin; Figure 47 uncertainty spans +/-2omega.
- **Jumbo portfolio:** the book’s dataset/portfolio of more than 100 instruments (102 in the pooled analysis).
