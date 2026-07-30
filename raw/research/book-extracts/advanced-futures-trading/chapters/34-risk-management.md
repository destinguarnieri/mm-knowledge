# Tactic Four: Risk Management

## Purpose and central argument

Risk management is a core part of every trading strategy, not merely an institutional function. The book’s position-sizing methods already target expected risk, but this does not guarantee protection against margin stress, temporarily extreme portfolio risk, volatility jumps, adverse correlation changes, excessive leverage, erroneous orders, or operational over-trading. This tactic adds systematic, exogenous guard rails that can only reduce—not increase—the strategy’s intended positions.

The immediate practical objective is to avoid margin calls. More generally, the chapter advocates measurable controls with predefined trigger levels, actions, and reversal conditions.

## 1. Margin problems

### Why they matter

For futures and other leveraged derivatives, a margin call indicates that the risk-management process has already failed. Margin can rise abruptly during market events: the author’s February 2018 example was the VIX doubling in one day during a sharp US equity decline, followed by dramatic increases in VIX and VSTOXX futures margin.

### Required risk-management process

Every process should specify:

1. A quantity that can be measured regularly.
2. A level at which action is taken.
3. The action.
4. The condition for reversing the action.

For margin, measure margin usage daily. With an expected risk target \(\tau=20\%\), the prior chapter’s directional-futures example expects average margin usage of about 30% of account value. The illustrative policy becomes concerned above 50% and acts at 60% (twice the average); normal trading resumes below 50%.

> **Capital condition:** This assumes the trading account is fully capitalised. If it is undercapitalised and margin is tight, the first step should be to transfer spare capital into it.

### Specific versus generic action

- **Specific action:** cut or close the positions with the largest margin requirements until margin falls to a tolerable level (e.g., 50%). This creates tracking error relative to the intended portfolio.
- **Generic action:** reduce every optimal position by the same ratio. Example: at 75% margin usage, reduce all optimal positions by one third, taking initial margin to 50% of account value.

For Strategy 25 (dynamic optimisation), margin-constrained instruments may instead receive position limits and the optimiser can redistribute capital to less margin-intensive markets.

## 2. Exogenous risk overlay

The portfolio construction used since Strategy 4 can meet the long-run average risk target \(\tau\) while still taking excessively risky positions on particular days. The remedy is a systematic **risk overlay** outside the trading strategy.

It receives the strategy’s optimal positions and produces a **position multiplier** \(M\):

- \(M=1\): no change.
- \(0\le M<1\): multiply every optimal position by \(M\).
- \(M>1\) is disallowed: the overlay never adds risk beyond the original strategy.

Mapped to the four-step process: measure the multiplier; act when it is below one; multiply all positions by it; reverse when it returns to one.

The final multiplier is the lowest of four risk-specific multipliers:

\[
M_{final}=\min(M_{portfolio},M_{jump},M_{corr},M_{leverage})\le1.
\]

Each control follows the same construction for a linearly scaling risk quantity \(X\): estimate \(X\); take its 99th-percentile backtest value as \(X_{max}\); if \(X>X_{max}\), scale all positions so that \(X=X_{max}\). This works only where multiplying every position by a constant multiplies \(X\) by that constant. The 99th percentile is intentionally a compromise: frequent activation distorts the base strategy, while rare activation offers little protection. Four uncorrelated 1%-active controls would be active in aggregate about 4% of the time (roughly two weeks a year).

## 3. Estimated portfolio risk multiplier

### What can make daily expected risk unusually high

- Forecasts are unusually strong (the one listed legitimate reason for higher risk).
- Same-signed positions become temporarily highly correlated despite historically uncorrelated returns.
- Opposite-signed positions become temporarily anti-correlated despite historically high correlation.
- Highly correlated instruments that normally have opposite-signed positions become same-signed.
- Highly anti-correlated instruments that normally have same-signed positions become differently signed.

The last four effects are unintended by-products of targeting long-run, rather than daily, strategy risk. Their combination can create high expected risk without high forecast conviction.

### Formula and definitions

Expected annualised percentage portfolio standard deviation is:

\[
\sigma_{p}=\sqrt{\mathbf w\,\Sigma\,\mathbf w^{\mathsf T}}.
\]

| Symbol | Definition / units |
|---|---|
| \(\sigma_p\) | Expected annualised percentage standard deviation of portfolio returns. |
| \(\mathbf w\) | Vector of signed position weights. |
| \(\Sigma\) | Covariance matrix of **percentage instrument returns**, not sub-strategy returns; annualised consistently with \(\sigma_p\). |
| \(N_i\) | Number of futures contracts in instrument \(i\), signed. |
| \(m_i\) | Futures contract multiplier for instrument \(i\). |
| \(P_i\) | Futures price. |
| \(FX_i\) | FX conversion rate into capital currency. |
| \(C\) | Capital / account value. |

The instrument weight is:

\[
w_i=\frac{N_i m_iP_iFX_i}{C}.
\]

It is positive for a long and negative for a short. Matrix multiplication is performed inside the square root.

**Covariance-estimation note:** The method is described as not very sensitive to the covariance estimate. The author permits simple or exponentially weighted covariance (about a six-month span), or separately estimated annualised \(\sigma_{\%}\) and correlations. His correlation estimate uses weekly returns (to reduce bias from different market closing times) and an exponentially weighted six-month span; Appendix B is referenced.

### Calibration and multiplier

For Strategy 11 (carry and trend) on the Jumbo portfolio, Figure 97 plots this expected-risk time series. More diversification makes risk properties more stable and lowers the maximum; earlier backtest periods have fewer instruments, explaining why the maximum falls over time.

The author uses the last 20 years to measure the 99th-percentile standard deviation. Strategy 11 produced 28%, but the chosen maximum is 30%, exactly 1.5 times \(\tau=20\%\):

\[
M_{portfolio}=\min\left(1,\frac{0.30}{\sigma_p}\right).
\]

At \(\sigma_p=15\%\), \(M_{portfolio}=1\). At \(\sigma_p=45\%\), \(M_{portfolio}=0.6666\), stated as cutting positions by two-thirds. Financial returns are non-Gaussian: expected risk tends to undershoot the target even while realised risk is close to it. Less diversified strategies may need a higher standard-deviation limit.

## 4. Jump risk multiplier

Financial returns are non-Gaussian, so estimated standard deviations can change rapidly. The Strategy 3 blend of long- and short-run volatility estimates avoids allowing a currently low estimate to fall too far below long-run average, but is blunt and does not fully address instruments with especially bad tails.

### Construction

1. Measure annualised standard deviation from percentage returns for every instrument.
2. For each instrument, calculate the 99th percentile of its historical standard-deviation distribution (ideally backward-looking in a backtest). These values will be very high.
3. Build \(\Sigma_{jump}\) with those 99th-percentile standard deviations and the original estimated correlations of percentage returns.
4. Calculate:

\[
\sigma_{p,jump}=\sqrt{\mathbf w\,\Sigma_{jump}\,\mathbf w^{\mathsf T}},\qquad
M_{jump}=\min\left(1,\frac{0.75}{\sigma_{p,jump}}\right).
\]

\(\Sigma_{jump}\) is a covariance matrix using shocked (99th-percentile) individual standard deviations while retaining the original correlation estimates. Figure 98 shows the Strategy 11 jump-risk series; it is much higher than Figure 97. Its last-20-years 99th percentile was just above 76%; the selected maximum is 75%, or 3.75 times the 20% target.

## 5. Correlation shock risk multiplier

This protects against positions and correlations “ganging up.” The example is large long positions in US 10-year bonds and S&amp;P 500 futures: their historically near-zero return correlation can spike upward during a coordinated selloff. The author cites summer 2021 and spring 2022 as real examples.

For an instrument \(i\), its portfolio-risk contribution is:

\[
Risk_i=w_i\sigma_{\%,i},
\]

where \(\sigma_{\%,i}\) is estimated annualised percentage standard deviation. If every held-instrument correlation moved to whichever of \(+1\) or \(-1\) is currently worst for the portfolio, shocked portfolio risk is:

\[
\sigma_{p,corr}=\sum_i |Risk_i|.
\]

Figure 99 plots this quantity for Strategy 11. It is a worst-case-correlation analogue to jump risk’s worst-case-standard-deviation construction. The historical 99th percentile was just above 67%; the chosen maximum is 65% (3.25 times \(\tau=20\%\)):

\[
M_{corr}=\min\left(1,\frac{0.65}{\sigma_{p,corr}}\right).
\]

## 6. Leverage risk multiplier

Leverage is a crude but transparent risk measure. If leverage is 100%, all positions are long, and every instrument price goes to zero overnight, the loss is exactly 100% of capital. However, leverage cannot be compared cleanly across instruments: low-risk Eurodollar futures can require roughly 18× leverage for a 20% risk target, whereas Bitcoin can require less than 1×.

Portfolio leverage is:

\[
L=\sum_i|w_i|.
\]

Figure 100 shows Strategy 11 leverage rising over time because of more instruments, a growing IDM, and newer instruments with lower standard deviation than the earlier mostly high-risk commodity set. Using the 99th percentile since 2000 gives a maximum just over 20; the selected cap is 20:

\[
M_{leverage}=\min\left(1,\frac{20}{L}\right).
\]

The author considers 20 high but wants the control to activate infrequently. Limits depend greatly on the instrument mix. A more complex variant would measure and limit leverage by asset class.

## 7. Final overlay implementation and observed effect

Apply \(M_{final}\) to **unrounded** optimal positions, then buffer normally. For Strategy 25, apply it before dynamic optimisation. For Part Four strategies, apply it before the trading day begins to avoid unusual limit-order behaviour. It may be suitable for Part Five relative-value strategies, but leverage-multiplier calibration requires care.

Figure 101 shows Strategy 11’s risk scalar. It activates just under 5% of the time, consistent with four 99th-percentile controls. Periods where each had the largest effect:

- Late 2017–early 2018: jump-risk multiplier; volatility was very low and VIX approached single digits.
- 2012: leverage multiplier; very low interest-rate and bond volatility increased leverage.
- Late 2008: estimated portfolio-risk multiplier; sub-prime-related financial crisis.
- Many earlier periods, notably around 1980: correlation-risk multiplier; commodity markets became highly correlated.

The multiplier did not affect either the 2020 COVID-19 equity crash or the early-2022 Ukraine invasion.

### Table 171 — Strategy 11, extended data

| Metric | No risk multiplier | After risk multiplier |
|---|---:|---:|
| Mean annual return | 27.3% | 27.2% |
| Costs | −0.9% | −0.9% |
| Average drawdown | −8.7% | −8.6% |
| Standard deviation | 20.7% | 20.5% |
| Sharpe ratio | 1.32 | 1.33 |
| Turnover | 50.3 | 50.0 |
| Skew | 0.59 | 0.55 |
| Lower tail | 1.88 | 1.84 |
| Upper tail | 1.75 | 1.71 |
| Alpha | 22.7% | 22.6% |
| Beta | 0.33 | 0.33 |

The author’s interpretation: always-equal-or-smaller positions slightly reduce both return and volatility, leaving Sharpe effectively unchanged. The effect is small because the overlay is inactive 95% of the time. Skew is marginally worse, tails slightly better, and the added winding down/up does not add turnover or trading costs.

## 8. Instruments that are too safe to trade

Standard sizing increases leverage when instrument return volatility falls. This reduces minimum capital needs but can become dangerous.

### Eurodollar illustration

The March 2022 Eurodollar contract had barely moved since April 2020; its standard deviation was about 0.0153% daily or 0.245% annually. The Strategy 2 volatility ratio \(\tau/\sigma_{\%}\) then implies \(20\%/0.245\%=81.6\). With $100,000 capital, this requires more than $8 million of Eurodollar notional exposure (more than 30 contracts).

At 80× leverage, a 1.25% price move would wipe out capital. Low standard deviation makes that unlikely, not impossible; non-Gaussian risk is omitted from the standard-deviation measure, and higher leverage raises risk-adjusted costs. A portfolio-wide target cannot sensibly use a different risk target for every instrument.

Long/short volatility blending helps temporarily low volatility but not permanently low volatility. The preferred answer is to avoid very-low-volatility instruments.

### Minimum-volatility screen

At the maximum absolute forecast of 20, a position’s leverage ratio is:

\[
L_i=\frac{2\,IDM\,Weight_i\,\tau}{\sigma_{\%,i}}.
\]

Rearranging for a maximum permitted leverage ratio \(L_{max}\):

\[
\sigma_{\%,i,min}=\frac{2\,IDM\,Weight_i\,\tau}{L_{max}}.
\]

| Symbol | Definition |
|---|---|
| \(IDM\) | Instrument diversification multiplier. |
| \(Weight_i\) | Instrument weight. |
| \(\tau\) | Portfolio risk target. |
| \(\sigma_{\%,i}\) | Annualised percentage standard deviation of instrument \(i\). |
| \(L_i, L_{max}\) | Instrument leverage ratio and chosen maximum. |

Example: \(IDM=1.5\), \(Weight_i=10\%\), \(\tau=20\%\), \(L_{max}=4\) gives \(\sigma_{\%,i,min}=1.5\%\) annually. Exclude instruments currently below that threshold. Exclusion is an implicit unsupported bet that omitted instruments will underperform, but very-low-volatility instruments may be too costly to trade anyway.

If volatility falls after acceptance, alternatives are: set position limits (and consider permanent removal if the limit is repeatedly hit); reduce instrument weights (also an unsupported relative-performance bet); or, for Eurodollars and some other futures, trade further out the curve where volatility is higher. The latter was the author’s AHL solution.

## 9. Position limits

Position limits are hard maximum contract holdings. Their first purpose is operational protection: the author recounts an AHL implementation error where a KRWUSD scaling constant of 100,000 was mistakenly applied to orders, turning a 10-contract Korean 10-year bond-futures order into one million contracts—about $100 billion notional. Automated systems lack a human sanity check.

Other purposes:

- Targeted control of leverage, more specific than the portfolio-level leverage multiplier.
- For large institutions, ensuring that a position is not so large a share of the market that it cannot be liquidated quickly.

Calculate separate limits for these purposes and use the most conservative.

### 9.1 Limit at maximum forecast

With forecasts capped at absolute 20, the standard position formula and its corresponding maximum are:

\[
N_i=\frac{ScaledForecast_i\,C\,IDM\,Weight_i\,\tau}{10\,m_iP_iFX_i\sigma_{\%,i}},
\]

\[
N_{i,max\,forecast}=\frac{2C\,IDM\,Weight_i\,\tau}{m_iP_iFX_i\sigma_{\%,i}}.
\]

The factor 2 reflects the maximum forecast of 20 under the formula’s forecast scaling. \(ScaledForecast_i\) is the strategy’s scaled forecast; all other symbols retain definitions above.

Example: Eurodollar futures with \(C=\$500,000\), \(IDM=2.0\), \(Weight=10\%\), \(\tau=20\%\), \(P=97\), \(m=\$2,500\), \(FX=1\), and \(\sigma_{\%}=1.1\%\) annual gives:

\[
N_{max\,forecast}=\frac{2(500{,}000)(2)(0.1)(0.2)}{(2{,}500)(97)(1)(0.011)}=15\text{ contracts}.
\]

Because price and risk vary daily, add 50% if limits are not reviewed daily: 22.5, rounded to **23 contracts**.

### 9.2 Limit for maximum leverage

For one instrument:

\[
L_i=\frac{N_i\times \text{notional exposure per contract}}{C},
\]

so the contract limit is:

\[
N_{i,max\,leverage}=\frac{L_{i,max}C}{m_iP_iFX_i}.
\]

With the Eurodollar inputs above and an instrument-level leverage maximum of 2:

\[
N_{max\,leverage}=\frac{2(500{,}000)}{(2{,}500)(97)(1)}=4.1,
\]

treated as **4 contracts**. This is below the 15-contract maximum-forecast result. Consequently, beyond forecast \(20\times4/15=5.333\), the position cannot increase; the instrument is effectively too safe to trade and should be down-weighted or removed.

### 9.3 Limit as a share of open interest

Minimum trading volume alone is insufficient: an instrument can trade high daily volume with little open interest because of scalpers or day traders. Large accounts may require their chosen-expiry position to remain at or below, for example, 1% of open interest.

In the example, June 2025 Eurodollar open interest of about 160,000 contracts implies a 1% limit of **1,600 contracts**. If this is the binding limit, reduce the instrument weight.

### 9.4 Final position limit and use

Use:

\[
N_{i,limit}=\min(N_{max\,forecast},N_{max\,leverage},N_{max\,open\,interest}).
\]

For the example, the values are 23, 4, and 1,600; use **4 contracts** (the source contains a typographical “contacts” in this sentence).

Use limits as hard automated-system guard rails or discretionary alerts. For institutional backtests, recompute historic limits from historic prices, risk, FX rates, and related inputs—do not apply a fixed contemporary limit. If an instrument repeatedly breaches its limit in a backtest, reduce its instrument weight.

### Dynamic optimisation exception (Strategy 25)

Do not calculate maximum-forecast limits from actual instrument weights. With 100 instruments and $500,000 capital, optimisation may hold only 10–20 instruments; average actual weights around 1% would make limits much too small. Still impose limits: trend strategies can concentrate risk in one or two instruments, exposing idiosyncratic jump risk. Substitute a nominal weight such as 10% or 20%, thereby limiting an individual instrument’s concentration to 10% or 20% of the average total risk budget. Position limits may also be added as optimisation constraints.

## 10. Trade limits

Trade limits control **operational** rather than market risk. An automated system could overtrade because of price movements, bad data, a strategy flaw, or a software bug.

Set hard per-instrument trade limits, e.g. four S&P 500 micro futures daily or 20 weekly. Once reached, block further trades unless manually overridden. Manual traders should at least treat a breach as an investigation signal.

Derive limits from position limits by estimating the normal fraction of maximum position traded daily:

- Parts One–Three: rule of thumb, no more than one third of maximum position per day.
- Fast Part Four strategies: use a much higher figure, around twice the maximum position daily.

With the Eurodollar 4-contract position limit, one third is slightly above one; round up to a **2-contract daily** limit. For large institutions, compare maximum daily trade with typical daily volume. If excessive, drop the instrument, reduce its weight, or remove high-turnover rule variations.

Liquidation time can be estimated as position limit divided by trade limit. Example: a 12-contract position limit and four-contract daily trade limit permits exit in three days.

## Warnings, assumptions, and edge cases

- Controls relying on proportional scaling require \(X\) to scale linearly with an equal scaling of all positions.
- Four 99th-percentile overlays are not guaranteed to be independent; the 4% aggregate-activation statement assumes uncorrelated controls.
- Risk estimates and standard deviation do not capture all non-Gaussian/tail risk.
- The author explicitly calls the percentile threshold partly arbitrary; calibration is strategy- and diversification-dependent.
- Low volatility is not automatically safe; it can mechanically produce destabilising leverage and costly trading.
- Portfolio-level leverage does not substitute for instrument-level limits.
- Position caps can deliberately prevent participation in stronger forecasts; that trade-off may expose an instrument selection/weighting issue.
- Dynamic optimisation changes the correct weight input for maximum-forecast caps.
- Applying the overlay at the wrong stage can cause execution artefacts (particularly Part Four limit orders).

## Explicit connections

- **Strategy 2:** volatility ratio \(\tau/\sigma_{\%}\), risk target, and maximum-loss framing.
- **Strategy 3:** volatility blending, instrument selection, and minimum volume.
- **Strategy 4 onward:** portfolio construction that introduces long-run rather than daily risk targeting.
- **Strategy 11:** carry-and-trend benchmark used for Figures 97–101 and Table 171.
- **Strategy 25:** dynamic optimisation; special order of overlay application and position-limit treatment.
- **Part Four:** apply overlay before the trading day; fast strategies require larger daily trade limits.
- **Part Five:** possible overlay use with special leverage calibration care.
- **Appendix B:** covariance/correlation estimation details.
- **Rolling and contract selection tactics:** moving farther out the curve to obtain higher volatility.

## Glossary

- **Margin call:** broker demand for funds/position reduction after margin stress.
- **Margin usage:** initial margin as a share of account value.
- **Specific / generic risk action:** intervention in selected positions / equal proportional reduction of all positions.
- **Risk overlay:** systematic layer outside a strategy that scales intended positions down.
- **Position multiplier (risk scalar):** number from zero to one applied to unrounded optimal positions.
- **Position weight:** signed notional exposure divided by capital.
- **Covariance matrix:** matrix of percentage-instrument-return covariances.
- **Jump risk:** risk measured after replacing individual volatilities with their 99th-percentile values.
- **Correlation shock risk:** risk under adverse \(\pm1\) correlations, represented by sum of absolute instrument risk contributions.
- **Leverage:** total absolute position weights, i.e. gross notional exposure as a multiple of capital.
- **IDM:** instrument diversification multiplier.
- **Open interest:** outstanding contracts in a chosen futures expiry.
- **Position limit / trade limit:** maximum holding / maximum permitted trading amount over a stated period.

## Key takeaways

1. Define every risk control before stress: measurement, trigger, response, and reversal.
2. Preserve the base portfolio’s structure where possible by proportionally scaling all positions, rather than reacting only to selected contracts.
3. Use the minimum of expected-risk, jump-risk, correlation-shock, and leverage multipliers; it is a downside-only overlay.
4. Screen or constrain low-volatility instruments because volatility targeting can imply extreme leverage.
5. Put hard position and trade limits around automated execution; they are essential safeguards against both market concentration and operational error.
