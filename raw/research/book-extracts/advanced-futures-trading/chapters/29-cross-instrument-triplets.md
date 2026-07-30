# Strategy Twenty-Nine: Cross Instrument Triplets

## Purpose and central argument

A **triplet** is a synthetic relative-value instrument built from three underlying futures. It extends a two-instrument spread by using two instruments to hedge a middle/base instrument. The chapter develops its definition, pricing, hedging ratios, sizing, capital and cost calculations, then tests simple trend and carry rules on three familiar examples.

The central conclusion is cautious: triplets are a “supercharged” spread. Their lower hedged-price volatility demands materially more gross leverage, raises costs and tail risk, and—except perhaps for the oil crack—produces underwhelming trend/carry results that can remain highly correlated with the middle underlying instrument.

> **Scope warning from the author:** Triplets worsen the leverage, cost, minimum-capital, and operational difficulties of spread trading. They are not appropriate without sufficient cash, skill, and tolerance for the risk.

## Core definition and interpretation

### Structure

A triplet written `Xa/b/Yc` is:

\[
X\text{ long }a \; - \;1\text{ short }b \; + \;Y\text{ long }c.
\]

- `a` and `c` are the **wings**.
- `b` is the **body**, the middle/base instrument.
- `X:1:Y` are the price/hedge ratios.
- A triplet is also called a **butterfly**.

The stated convention defines the base direction as short `b`, long `a` and `c`. Reverse every leg for the opposite direction. Being **long the butterfly** means expecting the price spread between the middle instrument and the two outer instruments to widen.

For fixed-income butterflies, the footnote makes the economic interpretation explicit: because bond prices and yields move inversely, a long US 2y/5y/10y butterfly expects the 5-year US interest rate to rise relative to the 2- and 10-year rates—making the yield curve more concave (“curvier”).

### Synthetic price

The chapter first recalls the two-instrument spread price:

\[
p^s = R p_a - p_b.
\]

For the triplet:

\[
p^t = Xp_a + Yp_c - p_b.
\]

| Symbol | Meaning | Units/domain |
|---|---|---|
| \(p^s\) | synthetic spread price | price points |
| \(p^t\) | synthetic triplet price | price points |
| \(p_a,p_b,p_c\) | prices of legs `a`, `b`, `c` | each leg's quoted price points |
| \(R\) | two-leg spread ratio | dimensionless |
| \(X,Y\) | triplet wing weights | dimensionless |

### Running US-yield example

Set `a` = US 2-year bond future, `b` = US 5-year, `c` = US 10-year. This ordering maximises the adjacent pair correlations \((a,b)\) and \((b,c)\). With \(X=1.5\), \(Y=0.25\), the instrument is `1.5US2/US5/0.25US10`.

Using the displayed prices \(p_a=105\), \(p_b=112\), \(p_c=118\):

\[
p^t=(1.5\times105)+(0.25\times118)-112=75.
\]

## Calculation framework

### 1. Set hedge weights

The preceding spread strategy selected its ratio to minimise expected spread-price standard deviation:

\[
R=\frac{\rho\sigma_b}{\sigma_a}.
\]

The source text appears to contain a typographical duplication when describing the two standard deviations; the formula and surrounding discussion indicate \(\sigma_a\) and \(\sigma_b\).

For a triplet, allocate half of `b`’s hedging work to each wing:

\[
X=\frac{\rho_{a,b}\sigma_b}{2\sigma_a},\qquad
Y=\frac{\rho_{b,c}\sigma_b}{2\sigma_c}.
\]

If \(\rho_{a,b}\) and \(\rho_{b,c}\) are very similar, the author permits the correlation-free approximation:

\[
X=\frac{\sigma_b}{2\sigma_a},\qquad
Y=\frac{\sigma_b}{2\sigma_c}.
\]

| Symbol | Meaning | Condition |
|---|---|---|
| \(\sigma_i\) | daily standard deviation of price differences for instrument \(i\) | same sample/price-difference basis across legs |
| \(\rho_{a,b},\rho_{b,c}\) | correlations of price differences for adjacent legs | use full expressions when the two correlations differ materially |

**Example.** \(\rho_{a,b}=0.92\), \(\rho_{b,c}=0.96\); \(\sigma_a=0.14\), \(\sigma_b=0.38\), \(\sigma_c=0.57\):

\[
X=\frac{0.92\times0.38}{2\times0.14}=1.25\approx1.50,\qquad
Y=\frac{0.96\times0.38}{2\times0.57}=0.32\approx0.25.
\]

The values are deliberately rounded; `Y` is lowered to 0.25 and `X` raised to 1.5, with the latter supporting practical contract ratios later.

### 2. Size the body position and derive wings

Size the short body position \(N_b\) using the same risk-targeting method as strategy 28:

\[
N_b=\frac{\text{Scaled forecast}\times\text{Capital}\times\text{Weight}\times\text{IDM}\times\tau}
{10\times\text{Multiplier}_b\times\text{FX rate}_b\times\sigma_t\times16}.
\]

\(\sigma_t\) is the standard deviation of daily returns of the triplet price. For relative value the author recommends a lower risk target, \(\tau=10\%\).

Convert that body count into the two wing counts:

\[
N_a=N_b\frac{X\,\text{Multiplier}_b\,\text{FX rate}_b}{\text{Multiplier}_a\,\text{FX rate}_a},\qquad
N_c=N_b\frac{Y\,\text{Multiplier}_b\,\text{FX rate}_b}{\text{Multiplier}_c\,\text{FX rate}_c}.
\]

The signs follow the triplet convention: when `b` is short, `a` and `c` are long, and vice versa.

| Symbol | Meaning |
|---|---|
| \(N_a,N_b,N_c\) | contracts in legs `a`, `b`, `c` |
| Capital | trading capital, in base currency |
| Weight | portfolio allocation weight for the triplet |
| IDM | instrument-diversification multiplier |
| \(\tau\) | annual risk target (author suggests 10% here) |
| Multiplier\(_i\) | futures contract multiplier for leg \(i\) |
| FX rate\(_i\) | conversion rate from the leg's currency into the base currency |
| Scaled forecast | forecast after the book's scaling convention |
| 10, 16 | fixed scaling constants retained from the strategy-28 sizing formula |

**Worked sizing example.** With $500,000 capital, \(\tau=10\%\), Weight = IDM = 1, scaled forecast = +10, \(\sigma_t=0.089\), and 5-year multiplier = 1,000:

\[
N_b=\frac{10\times500{,}000\times1\times1\times0.10}{10\times1{,}000\times1\times0.089\times16}=35.1.
\]

The position is **short 35.1 US 5-year futures**. With US 2-year multiplier 2,000, US 5/10-year multipliers 1,000, all FX rates 1:

\[
N_a=35.1\times0.75=+26.3,\qquad N_c=35.1\times0.25=+8.8.
\]

### 3. Measure notional exposure

For each leg:

\[
\text{Notional exposure (base currency)}=p_i\times\text{Multiplier}_i\times\text{FX rate}_i.
\]

Table 155 illustrates that a lower-volatility hedge requires more gross exposure at the same $500,000 capital and 10% risk target.

| Instrument / position | 2y contracts | 5y contracts | 10y contracts | Total absolute notional |
|---|---:|---:|---:|---:|
| US 2-year outright | 11.6 | — | — | $2,300,000 |
| US 5-year outright | — | 8.2 | — | $920,000 |
| US 10-year outright | — | — | 5.5 | $650,000 |
| `1.5US5/US10` spread | — | +39.3 | −19.7 | $6,700,000 |
| `1.5US2/US5/0.25US10` triplet | +26.3 | −35.1 | +8.8 | $10,400,000 |

### 4. Minimum capital

The chapter gives:

\[
\text{Minimum capital for 4 contracts}=\frac{4\times\text{Multiplier}_b\times\text{FX rate}_b\times\sigma_t\times16}{\text{IDM}\times\text{Weight}\times\tau}.
\]

This initial result assumes both \(N_a/N_b\) and \(N_c/N_b\) are integers. If either is fractional, multiply the required capital by the ratio needed to make all three contract holdings integral.

In the worked example, the unadjusted amount is:

\[
\frac{4\times1{,}000\times1\times0.089\times16}{1\times1\times0.10}=\$56{,}960.
\]

But \(N_a/N_b=0.75\) and \(N_c/N_b=0.25\), so multiply by 4: just over **$200,000** minimum capital.

### 5. Risk-adjust trading costs

For one contract of an individual leg:

\[
\text{Spread cost (price points)}=\frac{\text{Bid}-\text{Offer}}{2},
\]
\[
\text{Spread cost (currency)}=\text{Futures multiplier}\times\text{Spread cost (price points)},
\]
\[
\text{Cost per contract}=\text{Spread cost (currency)}+\text{Commission per contract}.
\]

Convert `a` and `c` costs to `b`’s FX basis and scale by contracts per body contract:

\[
C_a=\frac{N_a}{N_b}\,C_{a,\text{contract}}\frac{\text{FX rate}_a}{\text{FX rate}_b},\quad
C_b=C_{b,\text{contract}},\quad
C_c=\frac{N_c}{N_b}\,C_{c,\text{contract}}\frac{\text{FX rate}_c}{\text{FX rate}_b}.
\]

\[
C_{\text{total}}=C_a+C_b+C_c,
\qquad
\text{Risk-adjusted cost per trade}=\frac{C_{\text{total}}}{\sigma_t\times16\times\text{Multiplier}_b}.
\]

The displayed source writes the bid–offer expression as `(Bid − Offer)/2`; in conventional quoting order this can be negative. Preserve the source expression but treat the sign convention as needing verification in implementation.

## Candidate instruments and examples

Triplets are available in fixed income, equities, and commodities. The author excludes FX (for reasons set out in strategy 28) and volatility (only two liquid instruments in the dataset). These are examples only, **not endorsements** or evidence of high backtested Sharpe ratios.

| Asset class | `a` | `b` | `c` | \(\rho(a,b)\) | \(\rho(b,c)\) |
|---|---|---|---|---:|---:|
| Fixed income | US 2-year | US 5-year | US 10-year | .92 | .96 |
| Fixed income | US 10-year | US 20-year | US 30-year | .92 | .96 |
| Fixed income | German Schatz (2y) | German Bund (10y) | German Buxl (30y) | .81 | .88 |
| Fixed income | Japanese JGB (10y) | US 10-year | German Bund (10y) | .59 | .79 |
| Fixed income | Italian BTP (10y) | German Bund (10y) | French OAT (10y) | .79 | .83 |
| Equity | S&P 400 (mid cap) | S&P 500 (large cap) | Russell 2000 (small cap) | .89 | .84 |
| Equity | EU Auto | Eurostoxx 50 | EU Utilities | .73 | .54 |
| Equity | DAX 30 | Eurostoxx 50 | CAC 40 | .97 | .97 |
| Commodity | Soy Oil | Soybeans | Soy Meal | .65 | .68 |
| Commodity | Butter | Milk | Cheese | .46 | .87 |
| Commodity | Wheat | Corn | Oats | .64 | .42 |
| Commodity | Silver | Gold | Platinum | .79 | .57 |
| Commodity | Gasoline | WTI Crude | Heating Oil | .96 | .90 |

The detailed tests use:

- **US yield butterfly:** US 2-, 5-, and 10-year futures; a curvature bet.
- **Soy crush triplet:** soy meal, soybeans, soy oil; soybeans are inputs to meal and oil.
- **Oil crack triplet:** gasoline, WTI crude, heating oil; crude is refined into the products (and others).

Soy crush and oil crack are commonly called “spreads,” but the author calls them triplets for consistent nomenclature. Soy and oil use industry-standard ratios; US yield uses blended empirical estimates from the last 10 years and duration weights, to account for the unusual rate environment of that decade.

| Example | X | Y | \(N_a/N_b\) | \(N_c/N_b\) | Risk-adjusted cost | Minimum capital |
|---|---:|---:|---:|---:|---:|---:|
| US yield | 1.5 | .25 | .75 | .25 | .0118 | $172,000 |
| Soy crush | .5 | 3.0 | .25 | .25 | .00169 | $1,900,000 |
| Oil crack | 6 | 6 | .142857 | .142857 | .000856 | $850,000 |

Figures 86–88 plot the synthetic prices of the soy crush, US-yield, and oil-crack triplets respectively. All use `index` on the horizontal axis. Figure 86 (roughly 1986–2022) has a pronounced long decline with sharp disturbances, particularly around 2008 and 2012–13; Figure 87 covers roughly 2000–2022 and moves within about 74–81; Figure 88 covers roughly 1992–2022 and includes a very sharp 2008 trough. These figures communicate that the constructed prices are changing, volatile time series rather than stable constants. The chapter provides no further caption-level interpretation.

## Tested rules and results

### Trend: EWMAC16

The chapter tests one trend rule, **EWMAC16**, as an indicative—not definitive—probe of triplet characteristics.

| Metric | US yield | Soy crush | Oil crack |
|---|---:|---:|---:|
| Mean annual return | −0.7% | 1.6% | 5.8% |
| Costs | −1.13% | −0.3% | −0.1% |
| Average drawdown | −30.5% | −32.8% | −12.6% |
| Standard deviation | 9.6% | 11.6% | 12.7% |
| Sharpe ratio | −.07 | .14 | .46 |
| Turnover | 13.0 | 14.5 | 14.7 |
| Skew | 1.20 | 1.26 | 1.14 |
| Lower tail | 4.16 | 3.97 | 3.72 |
| Upper tail | 4.25 | 4.01 | 3.65 |
| Correlation with directional strategy on `b` | .36 | .96 | .92 |

Trend return before costs is slightly positive for two triplets and extremely good for oil crack, but this is only three instruments under one rule. Skew is positive, as in spreads, while tail measures are very high. Diversification versus trading directional `b` is decent for US yield, but almost absent for both commodity triplets.

### Carry: carry60

Raw carry must be calculated from the synthetic price at two maturities:

\[
\text{Raw carry}=(Xp_a^{\text{current}}+Yp_c^{\text{current}}-p_b^{\text{current}})
-(Xp_a^{\text{further}}+Yp_c^{\text{further}}-p_b^{\text{further}}),
\]

or equivalently:

\[
\text{Raw carry}=(Xp_a^{\text{nearer}}+Yp_c^{\text{nearer}}-p_b^{\text{nearer}})
-(Xp_a^{\text{current}}+Yp_c^{\text{current}}-p_b^{\text{current}}).
\]

`current`, `nearer`, and `further` are the contract-maturity labels used by the source; no further definition is given in this chapter.

| Metric | US yield | Soy crush | Oil crack |
|---|---:|---:|---:|
| Mean annual return | 2.8% | 1.3% | 7.9% |
| Costs | −0.8% | −0.1% | −0.1% |
| Average drawdown | −15.3% | −28.9% | −9.4% |
| Standard deviation | 14.5% | 15.2% | 12.8% |
| Sharpe ratio | .19 | .09 | .62 |
| Turnover | 10.0 | 7.3 | 7.1 |
| Skew | −.07 | .07 | .85 |
| Lower tail | 2.35 | 2.55 | 2.61 |
| Upper tail | 2.63 | 2.50 | 2.92 |
| Correlation with directional carry on `b` | .23 | .96 | .75 |

Oil crack is again the standout and has positive skew—unusual for carry—but it remains meaningfully correlated (.75) with directional WTI carry. Soy crush is even more correlated (.96) with outright soybeans.

## Practical procedure / trading plan

1. Define `a`, `b`, `c` in the `Xa/b/Yc` convention; confirm that `b` is the body and `a`,`c` the wings.
2. Estimate adjacent price-difference volatilities and correlations; calculate \(X,Y\), using the simplified weights only when adjacent correlations are very similar.
3. Form the synthetic triplet price \(Xp_a+Yp_c-p_b\).
4. Estimate daily return volatility \(\sigma_t\) of that synthetic price.
5. Apply the risk-sizing equation to the `b` position (author suggests 10% risk target for relative value), then translate into `a` and `c` contracts using multipliers and FX rates.
6. Check gross notional exposure, minimum capital, contract integrality, and three-leg transaction costs before trading.
7. Apply the selected signal to the synthetic price; for carry, use the modified three-leg raw-carry formula.
8. Execute and manage the remaining stages exactly as in **strategy 28**. The source includes three trading-plan images but their details are not text-accessible in the XHTML; the explicit text says all other stages are identical to strategy 28.

## Constraints, warnings, and edge cases

- Hedged volatility is not free: it mechanically implies much higher gross leverage and capital/margin demands.
- Costs apply across three markets, and the risk-adjusted cost must include each scaled leg.
- Contract ratios must be executable as integers; otherwise scale minimum capital up to the least practical integer combination.
- Accurate three-leg execution is difficult; fast mean reversion would require near-simultaneous limit-order fills in three markets.
- The examples are a limited sample and are not recommendations or robust evidence of generic profitability.
- Commodity triplets may not provide the desired diversification despite being relative-value structures.
- Relative prices may stay near equilibrium in the short/medium term, but systematic production-cost shifts can move that equilibrium.

## Conclusions and implications

Mean reversion might seem intuitively attractive: yield curves cannot sustain unusual shapes indefinitely, and soy/oil product prices should relate to production costs. Yet trend does not show the strongly negative performance expected if mean reversion were clearly optimal at the tested horizon. A fast mean-reversion version of strategy 26 might work, but practical execution is exceptionally difficult.

The evidence examined supports a restrained conclusion: trend and carry are broadly disappointing and strongly tied to underlying instruments, with the possible exception of the oil crack. The increased leverage, costs, and tail risk make triplets operationally and financially more demanding than ordinary spreads.

## Glossary

- **Triplet / butterfly:** three-leg synthetic relative-value instrument `Xa/b/Yc`.
- **Body:** middle/base leg `b`.
- **Wings:** outer legs `a` and `c`.
- **Synthetic price:** weighted three-leg price \(Xp_a+Yp_c-p_b\).
- **Hedge ratio / weights:** \(X,Y\), the wing quantities relative to one body unit.
- **Risk-adjusted cost:** total scaled three-leg cost divided by the chapter's risk-scaling denominator.
- **EWMAC16:** the single trend-following rule tested in the chapter; its internal definition is not repeated here.
- **carry60:** the single carry rule tested; its internal definition is not repeated here.
- **Soy crush:** production relationship between soybeans and soy meal/oil.
- **Oil crack:** refinery relationship between WTI crude and gasoline/heating oil.

## Explicit links to other chapters

- **Strategy 28:** source of the two-leg spread framework, the base risk-sizing, minimum-capital, and cost methods, FX exclusion rationale, and the remaining trading-plan steps.
- **Strategy 26:** named as a possible fast mean-reversion approach, though not tested here.
- **Strategy 8:** cited for additional spread information omitted from the triplet example tables.
