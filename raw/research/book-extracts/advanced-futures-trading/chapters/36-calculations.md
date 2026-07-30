# Appendix B — Calculations

## Purpose and scope

This appendix specifies the calculations used across the book: how to construct and maintain a back-adjusted futures price series; which standard-deviation and correlation estimates to use for particular tasks; turnover calculations; and forecast/instrument diversification multipliers. It also specifies covariance construction for portfolio-risk applications.

The appendix is procedural. Its examples use closing prices and business-day observations unless a different frequency is stated.

## 1. Back-adjusting a futures price series

### Objective

Create one continuous price history from successive dated futures contracts while removing discontinuities caused solely by rolling from one expiry to the next. The series is formed **backwards** from the most recent contract: each older contract is shifted by the roll-price difference so that it agrees with the newer adjusted series on the roll date.

### Inputs and roll-date choice

- Dated contracts: `A`, `B`, `C` (and subsequently `D`), ordered from older to newer.
- A price history for each contract.
- A roll date for each adjacent pair: a date on which both contracts have prices.
- The appendix’s example chooses the only A→B overlap, 7 January 2022, and the latest B→C overlap, 10 January 2022. In real markets overlap may last weeks/months; in some markets a roll can be possible on only one date.

#### Raw worked-example data

| Date | A | B | C |
|---|---:|---:|---:|
| 2 Jan 2022 | 100.0 | — | — |
| 3 Jan | 100.2 | — | — |
| 6 Jan | 100.3 | — | — |
| 7 Jan | 99.9 | 100.2 | — |
| 8 Jan | — | 99.9 | — |
| 9 Jan | — | 98.7 | 99.1 |
| 10 Jan | — | 99.0 | 99.5 |
| 13 Jan | — | — | 99.9 |
| 14 Jan | — | — | 100.1 |

### Initial-series procedure

1. Start at the final available date and copy prices of the newest contract into the back-adjusted series, moving backward until its roll date. In the example, C supplies 99.5 (10 Jan), 99.9 (13 Jan), and 100.1 (14 Jan).
2. At the B→C roll date, calculate the difference **newer minus older**:

   \[
   \Delta_{B\to C}=P_C(10\text{ Jan})-P_B(10\text{ Jan})=99.5-99.0=0.5.
   \]

3. Add that difference to **every relevant B price**. This makes B consistent with C on the roll date: `99.0 + 0.5 = 99.5`.
4. Copy the adjusted B values into the back-adjusted series for the dates before/through the B→C roll. The example yields B-adjusted values 100.7 (7 Jan), 100.4 (8 Jan), and 99.2 (9 Jan); the roll-date value is 99.5.
5. At the A→B roll date, compare the existing back-adjusted value with raw A:

   \[
   \Delta_{A\to B}=P_{\mathrm{BA}}(7\text{ Jan})-P_A(7\text{ Jan})=100.7-99.9=0.8.
   \]

6. Add 0.8 to every A price and copy the results into the back-adjusted series: 100.8 (2 Jan), 101.0 (3 Jan), 101.1 (6 Jan), and 100.7 (7 Jan).
7. Repeat backwards until the oldest contract in the available history has been adjusted.

#### Resulting series in the example

| Date | Back-adjusted price |
|---|---:|
| 2 Jan | 100.8 |
| 3 Jan | 101.0 |
| 6 Jan | 101.1 |
| 7 Jan | 100.7 |
| 8 Jan | 100.4 |
| 9 Jan | 99.2 |
| 10 Jan | 99.5 |
| 13 Jan | 99.9 |
| 14 Jan | 100.1 |

### Keeping the series current

**Key property:** the current back-adjusted price equals the price of the dated contract currently being traded. Thus, on ordinary days append the currently held contract’s new price directly. Example: C is 101.6 on 15 January, so the new back-adjusted observation is also 101.6.

When rolling C to D on 16 January, C = 101.0 and D = 101.5. Calculate:

\[
\Delta_{C\to D}=101.5-101.0=0.5.
\]

Then add 0.5 to the **entire existing** back-adjusted series; its 16 January observation becomes 101.5, matching D. The old series is discarded and subsequent D prices are appended to the new series.

Example revisions include 100.8→101.3 (2 Jan), 99.2→99.7 (9 Jan), 101.6→102.1 (15 Jan), and 101.0→101.5 (16 Jan).

> **Source-data note:** in the source’s 16 January rebasing table, the 6 January row labels the old back-adjusted price as `101.1` but prints the calculation `100.1 + 0.5 = 101.6`. The displayed result is consistent with 101.1 + 0.5; the intermediate `100.1` appears to be a typographical inconsistency, so it has not been treated as a separate calculation rule.

### Assumptions, constraints, and practical cautions

- The procedure uses closing-price differences at selected roll dates.
- A valid roll date requires prices for both adjacent contracts.
- Choice of roll date matters when multiple overlaps exist; the example uses the latest eligible date for B→C.
- Build historical adjustments in reverse; maintaining the series after a new roll requires shifting all previous back-adjusted observations.
- A back-adjusted value is not necessarily the price of an older historical contract; it is the shifted continuous-series value.

## 2. Standard-deviation estimation

### Which estimate to use

| Use case | Return/price input | Estimator and treatment |
|---|---|---|
| Trading-strategy performance analysis | Daily percentage strategy returns: daily P/L divided by trading capital at the day’s start | Simple standard deviation; annualise daily result ×16. Backtests normally use non-compounded returns, so trading capital is fixed. |
| Strategy 2 position sizing (`σ%`) | Daily back-adjusted prices `p_t` and held-contract price `p^*_t` | Simple standard deviation on all available backtest returns; annualise ×16. Alternative: use the position-sizing estimate used by other strategies and take its last value. |
| All other directional-strategy position sizing (`σ%`) | `p_t` and `p^*_t` | Exponentially weighted standard deviation, 32-day span, blended with slower estimate; annualise ×16. |
| Risk-adjusted cost per trade | — | Use the all-other-directional-strategies position-sizing estimate. |
| Minimum capital | — | Use the all-other-directional-strategies position-sizing estimate. |
| Risk-adjusting forecasts / daily price standard deviation (`σ_p`) | Daily back-adjusted prices `p_t` | Exponentially weighted standard deviation, 32-day span, blended with slower estimate; **do not annualise**. |
| Historical cost adjustment (`σ_p`) | — | Use the risk-adjusting-forecasts daily price-standard-deviation estimate. |
| Relative-value strategies (`σ_p`) | Synthetic daily back-adjusted price `p_t`, constructed from weights and individual-instrument back-adjusted prices | Exponentially weighted standard deviation, 32-day span, blended with slower estimate; **do not annualise**. |

For position sizing and dynamic optimisation, percentage returns are:

\[
r_t=\frac{p_t-p_{t-1}}{p^*_{t-1}}.
\]

In live trading the currently held contract price equals the current back-adjusted price; in a backtest it represents the contract held historically. For price standard deviation, use price changes rather than percentage returns:

\[
r_t=p_t-p_{t-1}.
\]

### Negative-price exception

Percentage returns ordinarily divide by the price of the currently held contract rather than the back-adjusted price because the latter may be near zero or negative. A current contract price can nevertheless be negative (the appendix cites WTI crude oil futures in March 2020). In that case:

1. Estimate price standard deviation `σ_p`, which does not divide by current price.
2. Derive percentage standard deviation using an arbitrary positive reference price `P&`:

   \[
   \sigma_{\%}=16\times \sigma_p\div P\&.
   \]

3. Choose `P&` as a recent “normal” positive price or perhaps a multi-year average price.

The appendix notes that the same price is usually multiplied by the standard-deviation estimate in, for example, position sizing; using the same `P&` in both locations makes it cancel.

### Simple standard deviation

For return observations `r_1, …, r_T`, first calculate their mean:

\[
r^*=\frac{1}{T}r_T+\frac{1}{T}r_{T-1}+\frac{1}{T}r_{T-2}+\cdots+\frac{1}{T}r_0.
\]

Then calculate:

\[
\sigma=\sqrt{\frac{1}{T}(r_T-r^*)^2+\frac{1}{T}(r_{T-1}-r^*)^2+\frac{1}{T}(r_{T-2}-r^*)^2+\cdots+\frac{1}{T}(r_1-r^*)^2}.
\]

`σ` is a daily standard deviation. When annualisation is required, and under assumptions discussed earlier in the book, multiply it by 16.

> **Indexing note:** the surrounding text calls the observations `r_1, …, r_T`, while the displayed mean formula begins at `r_T` and ends at `r_0` (and the variance formula ends at `r_1`). This apparent endpoint inconsistency is reproduced in the formula transcription; the source does not explain it further.

### Exponentially weighted standard deviation (EWMA)

For daily returns `r_0, …, r_t`, the exponentially weighted mean is:

\[
r^*(\lambda)_t=\lambda r_t+\lambda(1-\lambda)r_{t-1}+\lambda(1-\lambda)^2r_{t-2}+\cdots.
\]

The corresponding estimate is:

\[
\sigma_{\exp}(\lambda)_t=\sqrt{\lambda(r_t-r_t^*)^2+\lambda(1-\lambda)(r_{t-1}-r_t^*)^2+\lambda(1-\lambda)^2(r_{t-2}-r_t^*)^2+\cdots}.
\]

Specify the EWMA with a span of `N` days using:

\[
\lambda=\frac{2}{N+1}.
\]

### Fast/slow blend

Given the current estimate `σ_t`, the appendix’s blended estimate is:

\[
\sigma_{\text{blend},t}=0.3\,(\text{ten-year average of }\sigma_t)+0.7\sigma_t.
\]

### Symbols and conditions

| Symbol | Meaning / domain |
|---|---|
| `p_t` | Daily back-adjusted price at time `t`; also a synthetic price for the relative-value use case. |
| `p_t^*` | Price of the currently held futures contract at `t`; denominator is its prior-day value for percentage return. |
| `r_t` | Daily return at `t`: a percentage return for relevant position-sizing uses, or a price change for `σ_p`. |
| `T` | Number/index range of return observations used by the simple estimate. |
| `r^*`, `r_t^*` | Simple mean and time-`t` EWMA mean, respectively. |
| `σ`, `σ%`, `σ_p` | Daily standard deviation; percentage standard deviation; and price standard deviation, respectively. |
| `λ` | EWMA decay parameter, derived from span `N`. |
| `N` | EWMA span in days. |
| `P&` | Arbitrary positive reference price for handling negative current prices. The source uses an ampersand as its superscript/reference marker. |

## 3. Correlation estimation

Correlations are needed to estimate an IDM or FDM and to calculate forecast or instrument weights other than by handcrafting. The appendix uses all available data because the trading strategies’ behaviour is expected to remain relatively stable. For instrument correlations, weekly data avoids matching problems caused by markets closing at different times.

| Purpose | Data and frequency | Estimation protocol |
|---|---|---|
| Fixed instrument weights and IDM | Weekly returns for the instrument sub-strategy, assuming its instrument weight and IDM are each 1 | Use all available data; floor negative correlations at zero. |
| Variable instrument weights and IDM in a backtest | Same weekly instrument-sub-strategy returns | Recalculate yearly, using all historical data available to that date; floor negative correlations at zero. |
| Forecast weights and FDM | Forecast values for each trading-rule variation, **not trading returns** | Use all available data; floor negatives at zero. Prefer pooled data: stack each instrument’s `T_j × N` forecast-value matrix into one correlation-estimation dataset. `T_j` is the number of observations for instrument `i`. |

## 4. Covariance estimation

Portfolio-risk estimation is used for strategy 25 and tactic 4. Rather than directly estimating covariance from data, calculate standard deviations and correlations separately, because their predictability differs, then combine them.

- Correlations: exponentially weighted estimate with a six-month span.
- Standard deviations: the 32-day span already specified.
- For dynamic optimisation, first convert daily percentage returns to weekly returns (either add daily percentage returns through the week or estimate directly from weekly closing prices). Estimate correlation with either a 25-week EWMA span or an equally weighted 52-week rolling window.

Given a vector of standard deviations `σ` and correlation matrix `ρ`:

\[
\Sigma=\sigma\mathbin{.}\rho\mathbin{.}\sigma^T.
\]

Here `Σ` is the covariance matrix, `.` denotes dot multiplication, and `T` denotes transpose.

For risk management tactic 4:

- **Portfolio risk estimate:** use the same method as dynamic optimisation.
- **Portfolio risk jump estimate:** use the same method, but replace the standard-deviation estimate with the 99th-percentile historical estimate of standard deviation.

## 5. Backtest turnover calculation

Turnover is a diagnostic used for crude cost calculations and for deciding whether an instrument can be used with a given trading-rule variation.

### Forecast turnover

For a scaled backtested forecast `f_t` calculated on each business day:

\[
\text{annualised forecast turnover}=256\times\operatorname{Mean}\left(\frac{|f_t-f_{t-1}|}{10},\frac{|f_{t-1}-f_{t-2}|}{10},\ldots\right).
\]

The divisor 10 is used because scaled forecasts have a target average absolute value of 10. Average forecast-turnover estimates across instruments.

### Position turnover

For a backtested contracts position `p_t` calculated daily on business days:

\[
\text{annualised position turnover}=256\times\operatorname{Mean}\left(\frac{|p_t-p_{t-1}|}{p^*_{t-1}},\frac{|p_{t-1}-p_{t-2}|}{p^*_{t-2}},\ldots\right).
\]

`p_t^*` is the average position — for example, the position in that instrument when the forecast is `+10`.

## 6. Forecast diversification multiplier (FDM)

For `N` trading-rule variations, an `N × N` forecast-value correlation matrix `ρ`, and a forecast-weight vector `w` of length `N` that sums to 1:

\[
\mathrm{FDM}=\frac{1}{\sqrt{w\mathbin{.}\rho\mathbin{.}w^T}}.
\]

- Use correlations of forecast **values**, not returns from trading one forecast.
- Floor negative correlations at zero before calculation; otherwise the multiplier can be dangerously inflated.
- Cap FDM at 2.
- In backtests, recompute the correlation matrix annually using all available historical data to that point.
- Apply an EWMA to the FDM to avoid abrupt yearly position changes; a 30-day span is suggested.
- If multiple instruments use the same rules and forecast weights, calculate one common FDM by pooling/stacking their forecast-value matrices as described in the correlation section.

## 7. Instrument diversification multiplier (IDM)

For `N` instruments, an `N × N` correlation matrix `ρ` of instrument sub-strategy returns, and an instrument-weight vector `w` of length `N` that sums to 1:

\[
\mathrm{IDM}=\frac{1}{\sqrt{w\mathbin{.}\rho\mathbin{.}w^T}}.
\]

- Floor negative correlations at zero before calculation.
- Cap IDM at 2.5 to avoid excessive leverage in highly diversified portfolios. The appendix warns that this cap will undershoot the expected risk target.
- For backtests, estimate the matrix annually from all data available up to each annual calculation point.
- Smooth IDM with an EWMA (suggested 30-day span) to avoid sharp annual position changes.

## Key cautions and takeaways

- A roll creates a level adjustment to preserve continuity; the sign is newer contract minus older contract, and adjustment proceeds backward for historical construction.
- Current back-adjusted prices equal the currently traded dated-contract price until the next roll, but rolling requires rebasing every historical back-adjusted value.
- Do not divide by a negative or unsuitable current price for percentage-volatility estimation; switch to price volatility and a consistently used positive reference price.
- Annualise only where instructed: daily standard deviations for the stated percentage-volatility/performance uses are multiplied by 16; `σ_p` estimates are not annualised.
- Use weekly returns for instrument correlations; use forecast values, not returns, for FDM correlations.
- Flooring negative correlations and capping FDM/IDM are explicit safeguards against artificial diversification and excess leverage.

## Glossary

- **Back-adjustment** — shifting older contract prices so a continuous series matches newer-contract prices at rolls.
- **Back-adjusted price** — the continuous, roll-adjusted price series.
- **Dated contract** — a futures contract with a specific expiry.
- **Roll date** — date selected to switch from one expiry to the next, requiring both prices.
- **EWMA / exponentially weighted moving average** — recursively weighted estimate that gives more weight to recent observations.
- **Span** — EWMA time parameter `N`, converted to `λ = 2/(N+1)`.
- **`σ%` / `σ_p`** — percentage and price standard deviation, respectively.
- **Correlation matrix (`ρ`)** — square matrix of pairwise correlations.
- **Covariance matrix (`Σ`)** — covariance derived here from standard deviations and correlations.
- **FDM / IDM** — forecast and instrument diversification multipliers.
- **Turnover** — annualised average absolute day-to-day forecast or position change, scaled as specified.

## Explicit connections in the source

- Strategy 2 uses the simple `σ%` estimate for position sizing.
- Other directional strategies use the 32-day EWMA/blended `σ%` estimate.
- Strategy 25 (dynamic optimisation) and tactic 4 (risk management) use covariance/portfolio-risk calculations.
- The appendix refers to assumptions for annualisation and other standard-deviation context discussed earlier in the book; those prior discussions are not reproduced here.
