# Strategy Nine — Multiple Trend Following Rules

## Purpose and central argument

This strategy improves a single-speed EWMAC trend system by combining several trend filters with different horizons. Although their returns are correlated, they are not perfectly correlated; diversification across filter speeds can improve performance and risk characteristics relative to any one speed, including the individually strongest EWMAC(16,64) filter.

**Strategy definition:** trade one or more eligible instruments, scale positions using a variable risk estimate, calculate forecasts from several trend-filter speeds, and size the position from their combined forecast.

The strategy uses EWMAC filters, equal forecast weights among the filters that are cheap enough to trade for each instrument, a forecast diversification multiplier (FDM), a final ±20 cap, then the prior strategy’s position-sizing and buffering process.

## Scope, dependencies, and assumptions

- Uses the same position sizing, risk estimate, forecast scaling, cap, buffers, capital, FX conversion, multiplier, instrument weights, and instrument diversification multiplier (IDM) as Strategy Eight unless explicitly replaced here.
- The volatility estimate remains the exponentially weighted standard deviation used since Strategy Three: 35-day span, blended with the current estimate and a very-long moving average. The book argues one estimate is appropriate for all filter speeds: 10–50-day spans work reasonably across horizons, with optimum around 30–35 days.
- Results cited are backtests. The “Jumbo” portfolio is the book’s aggregate portfolio. Past filter performance is not treated as sufficient reason to optimize heavily on it.
- Correlation is only a linear co-movement measure. The author notes actual diversification can be greater, particularly for trend rules.

## Core concepts and definitions

| Term | Meaning in this strategy |
|---|---|
| EWMA(N) | Exponentially weighted moving average of back-adjusted price with an N-business-day span. |
| EWMAC(N,4N), abbreviated EWMACN | Fast EWMA(N) minus slow EWMA(4N). |
| Raw forecast | Risk-normalized EWMAC crossover. |
| Forecast scalar | Filter-specific constant that calibrates the average absolute forecast to 10. Same across instruments. |
| Capped forecast | Scaled individual forecast limited to [-20, +20]. |
| Forecast weight | Non-negative weight on an individual capped forecast; weights for an instrument sum to 1. |
| Raw combined forecast | Weighted average of individual capped forecasts. |
| FDM | Forecast diversification multiplier; restores scale lost because forecasts are imperfectly correlated. |
| IDM | Instrument diversification multiplier from earlier strategies; corrects diversification across instruments. |
| Turnover | Annual turnover of the average position; estimated through backtesting and similar across instruments for a rule. |
| Speed limit | Maximum risk-adjusted trading cost permitted when choosing rules; 0.15 SR units here. |

## Filter universe and design boundaries

The selected filters are EWMAC(2,8), (4,16), (8,32), (16,64), (32,128), and (64,256). EWMAC(64,256) was Strategy Seven; EWMAC(16,64) was Strategy Eight.

The fast span is one-quarter of the slow span. Ratios from 2 to 6 perform similarly, but variants with a common fast span and different ratios would be highly correlated. Intermediate pairs such as EWMAC(12,48) are omitted because the chosen series is already highly correlated; more granular filters add insufficient diversification.

EWMAC(1,4) is excluded: even EWMAC(2,8) is too expensive for almost all futures. (An EWMA(1) is simply the last price, not an average.) Slower-than-EWMAC64 rules become too correlated with long-only and generate too few trades to assess incremental value.

### Forecast scalars (Table 29)

| Filter | Scalar |
|---|---:|
| EWMAC2 | 12.10 |
| EWMAC4 | 8.53 |
| EWMAC8 | 5.95 |
| EWMAC16 | 4.10 |
| EWMAC32 | 2.79 |
| EWMAC64 | 1.91 |

Successive scalars (doubling the span) have a ratio of roughly √2.

## Calculation and trading procedure

### 1. Compute each EWMAC forecast

For instrument *i*, time *t*, and filter variation *j* (where its fast span is *N*):

\[
\alpha = \frac{2}{N+1}
\]
\[
EWMA(N)_{i,t}=\alpha p_{i,t}+\alpha(1-\alpha)p_{i,t-1}+\alpha(1-\alpha)^2p_{i,t-2}+\cdots
\]
\[
RawForecast_{j,i,t}=\frac{FastEWMA_{j,i,t}-SlowEWMA_{j,i,t}}{\sigma_{i,t}}
\]

*p* is back-adjusted price and \(\sigma_{i,t}\) is the current standard-deviation/risk estimate. The numerator is a price difference; division risk-normalizes it.

For scalar \(s_j\):

\[
ScaledForecast_{j,i,t}=RawForecast_{j,i,t}\times s_j
\]
\[
f_{j,i,t}=\max(\min(ScaledForecast_{j,i,t},20),-20)
\]

Thus \(f_{j,i,t}\) is an individual capped forecast. Individual scaled forecasts target mean absolute value 10 and are capped at ±20.

### 2. Choose tradable filters by cost

For a rule variation:

\[
AnnualRiskAdjustedCosts=TransactionCosts+HoldingCosts
\]
\[
TransactionCosts=CostPerTrade\times AnnualTurnover
\]
\[
HoldingCosts=CostPerTrade\times RollsPerYear\times2
\]

The factor 2 assumes two separate trades and two sets of trading costs for each roll. Retain a rule only when annual risk-adjusted costs are below 0.15 SR units:

\[
Turnover < \frac{0.15-(CostPerTrade\times RollsPerYear\times2)}{CostPerTrade}
\]

The printed trading-plan image instead shows one roll-cost term (without ×2), and the worked Eurodollar calculation uses that version. This is an internal source inconsistency; it is flagged rather than resolved here.

**Why 0.15 rather than the 0.10 instrument speed limit:** the combined forecast’s average cost will be below the most expensive component’s cost, and buffering slows realized trading.

| Average annual turnover (Table 35) | Value |
|---|---:|
| EWMAC2 | 98.5 |
| EWMAC4 | 50.2 |
| EWMAC8 | 25.4 |
| EWMAC16 | 13.2 |
| EWMAC32 | 7.6 |
| EWMAC64 | 5.2 |

For the Jumbo portfolio, instruments eligible at turnover 1/year, 10, 25, 50, 75, 100, 150, and 300 are respectively 101, 96, 67, 42, 22, 11, 4, and 1 (Table 34). At cost per trade 0.0088 SR units and four Eurodollar rolls/year, the worked image calculates maximum turnover 13.0; therefore only EWMAC32 and EWMAC64 qualify. A low-cost quarterly S&P 500 micro future can use all six. If no variation qualifies, the instrument cannot be traded in this strategy.

Across 102 Jumbo instruments: 5 qualify for no filters; 1 for one; 11 for two; 24 for three; 21 for four; 29 for five; 11 for all six.

### 3. Allocate forecast weights

The preferred combination point is a **weighted average of capped forecasts**—not raw forecasts, positions, or separately traded systems. Capping before averaging prevents a temporarily huge single forecast dominating the result. For an instrument’s eligible filters:

\[
RawCombinedForecast_{i,t}=\sum_jw_{i,j}f_{j,i,t},\quad \sum_jw_{i,j}=1,\quad w_{i,j}\ge0
\]

The author’s top-down “handcrafting” method is:

1. Allocate across styles according to preference.
2. Allocate equally across rules within each style.
3. Allocate equally across variations within each rule.

Here there is one divergent style, trend-following EWMAC is its only rule, and the remaining variations receive equal weights. Examples: five qualifying filters → 20% each; EWMAC32 and 64 only → 50% each; all six → 1/6 = 16.667% each.

Negative weights are not used. The footnote notes that a reliably losing rule might instead be reframed in the opposite direction; doing so can itself introduce overfitting.

### 4. Restore forecast scale and cap again

The average of unperfectly correlated forecasts has lower magnitude. For example, equal-weighting all six S&P micro forecasts produces mean absolute value 7.5, versus 10 for every individual forecast. Apply the FDM:

\[
ScaledCombinedForecast_{i,t}=RawCombinedForecast_{i,t}\times FDM_i
\]
\[
CappedCombinedForecast_{i,t}=\max(\min(ScaledCombinedForecast_{i,t},20),-20)
\]

Final capping is necessary because FDM can push the combined forecast above ±20.

| Eligible set (Table 36) | Equal weight per rule | FDM |
|---|---:|---:|
| 2, 4, 8, 16, 32, 64 | 0.167 | 1.26 |
| 4, 8, 16, 32, 64 | 0.200 | 1.19 |
| 8, 16, 32, 64 | 0.250 | 1.13 |
| 16, 32, 64 | 0.333 | 1.08 |
| 32, 64 | 0.500 | 1.03 |
| 64 | 1.000 | 1.00 |

For perfectly correlated rules FDM is 1; for *N* mutually uncorrelated rules it is √*N*. With six uncorrelated rules it would be 2.45, not 1.26, showing the selected filters remain substantially correlated.

### 5. Size, buffer, and trade the position

\[
N_{i,t}=\frac{CappedCombinedForecast_{i,t}\times Capital\times IDM\times Weight_i\times \tau}{10\times Multiplier_i\times Price_{i,t}\times FX_{i,t}\times \sigma_{i,t}}
\]

*N* is the unrounded optimal contract position; \(\tau\) is the portfolio risk target; *Multiplier* is the futures contract multiplier; *Weight* is the instrument weight; *FX* converts contract value into capital currency. Units resolve to contracts.

Buffer width:

\[
B_{i,t}=\frac{0.1\times Capital\times IDM\times Weight_i\times\tau}{Multiplier_i\times Price_{i,t}\times FX_{i,t}\times\sigma_{i,t}}
\]

\[
LowerBuffer=round(N-B),\quad UpperBuffer=round(N+B)
\]

For current integer position \(C_{i,t}\): no trade if lower ≤ C ≤ upper; buy \(Upper-C\) if C is below lower; sell \(C-Upper\) if C is above upper.

## Diversification and weight-selection evidence

Return correlations decline as filters become farther apart. Adjacent filters are roughly 0.87–0.89; filters two steps apart around 0.64; EWMAC2 versus 64 is 0.12. Average correlation versus the other filters is: EWMAC2 0.45, 4 0.60, 8 0.69, 16 0.68, 32 0.60, 64 0.46 (Table 33). A diversification-only optimization would therefore have a U shape: more allocation to fastest and slowest filters, less to middle speeds.

The author nevertheless uses equal weights after cost exclusion, to avoid fitting historical performance. Costs and correlations are more defensible inputs than full-history pre-cost Sharpe ratios: costs do not depend on backtest returns, and turnover/correlations can in principle be estimated rolling, theoretically, or from a small data segment.

## Performance of individual filters

Aggregate Jumbo statistics with buffering and forecast scaling (Tables 30–31):

| Measure | EWMAC2 | 4 | 8 | 16 | 32 | 64 |
|---|---:|---:|---:|---:|---:|---:|
| Gross mean annual return | 13.0% | 19.6% | 24.1% | 25.8% | 24.4% | 22.5% |
| Net mean annual return | 3.5% | 14.8% | 21.5% | 24.1% | 23.2% | 21.5% |
| Costs | -9.3% | -4.7% | -2.5% | -1.7% | -1.2% | -1.0% |
| Average drawdown | -161.7% | -23.1% | -13.0% | -11.4% | -13.4% | -16.0% |
| Standard deviation | 22.9% | 23.1% | 23.3% | 22.7% | 22.7% | 22.3% |
| Sharpe ratio | 0.15 | 0.64 | 0.92 | 1.06 | 1.02 | 0.96 |
| Turnover | 381 | 195 | 97.9 | 60.5 | 35.3 | 27.5 |
| Monthly skew | 1.32 | 0.75 | 1.48 | 0.81 | 0.75 | 0.61 |
| Net alpha | 0.9% | 11.2% | 16.9% | 17.6% | 16.2% | 13.6% |
| Beta to Strategy Four long-only | 0.17 | 0.25 | 0.32 | 0.38 | 0.48 | 0.53 |

EWMAC16 is the strongest individual historical filter by outright return and alpha. Fast rules have extreme turnover/cost; EWMAC2 appears to lose money net in the full universe, but may be viable in unusually cheap instruments. Slower filters have higher long-only beta because they are more often persistently long instruments that generally rise, such as bonds.

The expected positive trend skew appears at a measurement horizon commensurate with holding period: fast filters show it daily/weekly sooner, slower filters mostly monthly/annual. The chapter’s daily/weekly/monthly/annual skew values are: EWMAC2 0.37/0.94/1.32/1.09; 4 0.46/0.75/1.53/1.27; 8 0.26/0.60/1.48/1.10; 16 -0.08/0.02/0.92/1.44; 32 -0.22/-0.13/0.75/0.94; 64 -0.34/-0.18/0.61/0.66 (Table 32).

## Historical behavior, cautions, and figures

- **Figure 35:** all speeds did similarly until about 1990; slower filters continued doing well thereafter while EWMAC2 and 4 flatlined, and EWMAC2 lost money.
- **Figure 36:** EWMAC2 gross performance was strong to 1990 and roughly flat afterward except COVID; costs widened materially after 1990. Possible explanations: fast trend stopped working, historical costs are understated, newer instruments are costlier/less suitable, or fast gross returns occur only in costly instruments. The book finds evidence for the first three, not the fourth.
- Using historical pre-cost performance to drop filters is in-sample fitting. Dropping only EWMAC2 for live trading could be defensible; the author would keep EWMAC4, but retains both in this chapter’s analysis so backtests remain realistic.
- **Figure 37:** equal-weighted six-filter S&P micro forecast rarely reaches extremes; only simultaneous +20 signals can average to +20 before FDM.
- **Figure 38:** since 2014 Strategy Eight weakened while Strategy Seven improved; Strategy Nine continued doing well by holding both and other speeds.
- Strategy Nine lost money in 2009, 2015, 2016, and 2018. Its worst backtest year was -12% in 2018; losses are described as smaller than gains because of positive skew. Returns appear lower since 2010; the author says that is insufficient evidence to declare trend following “dead” and recommends diversifying beyond it.

## Aggregate results and practical implications

| Jumbo aggregate metric (Table 39) | Long only (S4) | Slow trend (S7) | Fast trend (S8) | Multiple trend (S9) |
|---|---:|---:|---:|---:|
| Mean annual return | 15.4% | 21.5% | 24.1% | **25.2%** |
| Costs | -0.8% | -1.0% | -1.7% | -1.2% |
| Average drawdown | -24.7% | -16.0% | -11.4% | **-11.2%** |
| Standard deviation | 18.2% | 22.3% | 22.7% | 22.2% |
| Sharpe ratio | 0.85 | 0.96 | 1.06 | **1.14** |
| Turnover | 20.7 | 27.5 | 60.5 | 62.9 |
| Skew | -0.04 | 0.61 | 0.81 | **0.98** |
| Alpha | 0 | 13.6% | 17.6% | **18.8%** |
| Beta | 1.00 | 0.53 | 0.38 | 0.43 |

The multiple-speed strategy improves almost every measure relative to either single-speed trend version; beta lies between slow and fast trend while alpha exceeds both. Median individual-instrument performance is generally good, with positive skew and somewhat fat left tails. The volatility asset class is especially transformed: it retains positive skew while posting SR above 0.5, though there are only two instruments. Equities perform relatively poorly and worsen with faster filters; changing equity forecast or instrument weights might be an overfit and is deferred to Part Two.

## Conclusion and connections

Trend following is presented as a core CTA strategy: profitable in the backtest, positively skewed, and often helpful in generally poor markets (the text cites 2008 and early 2022). Strategy Nine’s contribution is not a new signal family but robust diversification across a range of EWMAC speeds, cost-filtered per instrument and normalized with FDM.

The next chapter/Strategy Ten introduces carry, the first non-trend rule and an example of a **convergent** strategy. Trend following is **divergent**: it profits when markets move away from equilibrium. The book’s larger direction is to diversify beyond trend following across strategies as well as instruments.

## Glossary

- **Alpha / beta:** regression measures relative to the Strategy Four long-only benchmark.
- **Back-adjusted price:** price series used in EWMA calculations.
- **Buffer:** no-trade band around the optimal unrounded contract position.
- **Convergent strategy:** profits from movement toward equilibrium (carry is the forthcoming example).
- **Divergent strategy:** profits as markets diverge from equilibrium (trend following).
- **EWMAC:** exponentially weighted moving-average crossover.
- **Forecast diversification multiplier (FDM):** multiplier correcting the scale loss of combined, imperfectly correlated forecasts.
- **Forecast scalar:** calibration constant so a filter’s mean absolute forecast is 10.
- **Forecast weight:** nonnegative per-filter allocation that sums to one for an instrument.
- **IDM:** instrument diversification multiplier.
- **Risk-adjusted cost:** trading/holding cost expressed in SR units.
- **Speed limit:** threshold used to exclude too-expensive instrument/rule combinations.
- **Turnover:** annualized trading of the average position.
