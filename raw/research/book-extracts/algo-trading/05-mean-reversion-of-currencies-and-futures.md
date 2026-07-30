---
title: "Mean Reversion of Currencies and Futures"
chapter: 5
source: "Algorithmic Trading: Winning Strategies and Their Rationale"
status: "extracted"
---

# Chapter 5: Mean Reversion of Currencies and Futures

## Chapter Overview

Currencies and futures are primarily momentum domains, so mean reversion is exceptional. The chapter identifies currency cross-rates, futures calendar spreads, and selected intermarket spreads as exceptions. It emphasizes quote-currency consistency, rollover interest, and a futures-price model that decomposes total return into spot and roll return. **Source: pp. 107–108**

## Learning Objectives

* Construct and measure currency cross-rate portfolios correctly. **Source: pp. 108–112**
* Incorporate rollover interest in currency returns. **Source: pp. 112–115**
* Use the spot/roll framework to understand calendar spreads and selected intermarket spreads. **Source: pp. 116–132**

## Key Concepts

### Currency cross-rates and common quote currency

For AUD.ZAR, AUD is base and ZAR quote; 9.58 means 9.58 ZAR per AUD. A synthetic cross may be formed as USD.ZAR/USD.AUD. For a Johansen eigenvector to represent capital weights, candidate currency series must use the same quote currency: the chapter therefore tests AUD.USD and CAD.USD rather than USD.AUD and USD.CAD. Live trades must invert a quote/order where necessary. Realized P&L in nonlocal currencies should be regularly converted into the investor’s local currency. **Source: pp. 108–110**

### Rollover interest

Holding a cross-rate earns/pays the differential between base- and quote-currency interest rates. For a USD investor, this carry affects total return; weekly rollover conventions can require three days’ interest on particular weekdays. **Source: pp. 112–115**

### Futures calendar spreads

A calendar spread is long one expiration and short another for the same underlying. Its log-value signal depends on roll return, not spot price. Calendar spreads are not automatically mean reverting: the roll-return process must itself be stationary/slowly varying. **Source: pp. 122–126**

### Intermarket spreads

Closely related futures may be tested as candidate portfolios, but synchronizing prices and respecting different contract specifications are necessary. The chapter discusses the 3:2:1 crack spread and an ES–VX relationship; it warns that relationships can be regime-dependent. **Source: pp. 127–132**

## Mathematical Formulas

### Currency portfolio return with common USD quote

**Formula**

$$
r(t+1)=\frac{n_1y_{1,U}(t)r_1(t+1)+n_2y_{2,U}(t)r_2(t+1)}{|n_1|y_{1,U}(t)+|n_2|y_{2,U}(t)}
\tag{5.1}
$$
$$
r_i(t+1)=\frac{y_{i,U}(t+1)-y_{i,U}(t)}{y_{i,U}(t)}
\tag{5.2}
$$

**Variables:** `$n_i$` units of currency `$B_i$`; `$y_{i,U}$` quote of `$B_i.USD$`; `$r_i$` one-period return; `$r$` portfolio return. **Purpose:** dollar-value-weight currency positions consistently. **Conditions:** common quote USD and dollar-valued exposures. **Interpretation:** returns are weighted by absolute current USD market value. **Source: pp. 109–110**

### USD-base portfolio return

**Formula**

$$
r(t+1)=\frac{n'_1r_1(t+1)+n'_2r_2(t+1)}{|n'_1|+|n'_2|},\qquad
r_i(t+1)=\frac{y_{U,i}(t+1)-y_{U,i}(t)}{y_{U,i}(t)}
\tag{5.3–5.4}
$$

`$n'_i$` are USD.Q units and `$y_{U,i}$` is USD.Q quote. The simplification follows because one unit of USD.Q is worth one U.S. dollar. The author notes these percentage-return equations are not strictly correct for longer horizons, motivating log returns. **Source: pp. 110–111**

### Cross-rate return and rollover adjustment

**Formula**

$$
r_i(t+1)=\log y_{i,Q_i}(t+1)-\log y_{i,Q_i}(t)
\tag{5.5}
$$
$$
r(t+1)=\log y_{B,Q}(t+1)-\log y_{B,Q}(t)+\log(1+i_B(t))-\log(1+i_Q(t))
\tag{5.6}
$$

`$y_{B,Q}$` is base/quote cross-rate; `$i_B,i_Q$` are applicable base and quote rates. **Purpose:** add carry to log price change. **Condition:** rates must correspond to the holding/rollover interval. **Interpretation:** appreciation plus base interest less quote interest is the excess return. **Source: pp. 111–114**

### Constant spot/roll futures model

**Formula**

$$F(t,T)=S(t)\exp(\gamma(t-T))\tag{5.7}$$
$$S(t)=ce^{\alpha t}\tag{5.8}$$
$$F(t,T)=ce^{\alpha t}\exp(\gamma(t-T))\tag{5.9}$$
$$\frac{\partial\log F(t,T)}{\partial t}=\alpha+\gamma,\qquad-\frac{\partial\log F(t,T)}{\partial T}=\gamma\tag{5.10–5.11}$$

`$F(t,T)$` is futures price at time `$t$` expiring `$T$`; `$S(t)$` spot; `$c$` initial scale; `$\alpha$` spot return; `$\gamma$` roll return. **Purpose:** state total return as spot plus roll return and forward-curve slope as roll return. **Assumptions:** constant `$\alpha$` and `$\gamma$`; approximation may fail over widely separated maturities or for nonstandard underlyings. **Source: pp. 118–121**

### ES–VX fitted stationary relationship

$$
ES\times50=-0.3906\times VX\times1{,}000+\$77{,}150
\tag{5.11 as printed}
$$

The source labels this Equation 5.11 even though the preceding futures derivative relation is also labeled 5.11 in the supplied text; this numbering inconsistency is preserved. Contract multipliers are 50 for ES and 1,000 for VX. **Purpose:** a fitted price relationship used to form an ES/VX stationary portfolio. **Source: p. 131**

## Methods and Procedures

### Example 5.1: AUD/CAD cointegration

Use AUD.USD and CAD.USD, estimate capital weights with Johansen testing on rolling training data, generate a mean-reversion signal, and compute returns with dollar-value weighting. Exclude the initial 250-day training period from performance. **Source: pp. 109–112**

### Example 5.2: AUD.CAD with rollover

Compute AUD and CAD daily rates, triple the appropriate weekday’s rate for weekend settlement, calculate a moving-average deviation `$z$`, and trade opposite its lagged sign while including log price change plus the interest differential. **Source: pp. 113–115**

### Example 5.3: estimating spot and roll returns

Regress log reconstructed spot against time for `$\alpha$`. On each date, regress log prices of five consecutive nearby contracts against maturity index; annualize `$\gamma$` as `-12` times the slope. Check linearity of log futures values versus maturity before relying on the model. **Source: pp. 119–122**

### Example 5.4: CL calendar-spread mean reversion

Estimate daily `$\gamma$`, regress `$\Delta\gamma$` on lagged `$\gamma$` to obtain half-life `$-\log(2)/\beta$`, and use that rounded half-life as Z-score lookback. Construct far/near contracts 12 months apart, avoiding expiration windows, then reverse the spread direction when Z-score is positive. The reported CL gamma half-life is about 36 days; reported Jan. 2, 2008–Aug. 13, 2012 result: unlevered APR 8.3%, Sharpe 1.3. **Source: pp. 123–126**

## Derivations and Proofs

Substituting the exponential spot process (5.8) into (5.7) yields (5.9). Differentiating log price with respect to time gives total return `$\alpha+\gamma$`; negative maturity derivative gives `$\gamma$`. Thus a long-far/short-near equal-market-value log calendar spread is `$\gamma(T_1-T_2)$`, with `$T_2>T_1$`, so spot cancels. **Source: pp. 118–123**

## Worked Examples

* **Example 5.1:** currency-pair mean reversion using common USD quote; source stresses correct conversion of a CAD.USD order to an executable USD.CAD order. **Source: pp. 109–112**
* **Example 5.2:** AUD.CAD pair with rollover-rate adjustment. **Source: pp. 113–115**
* **Example 5.3:** estimates annualized `$\gamma$` for CL (Nov. 22, 2004–Aug. 13, 2012) and plots it. **Source: pp. 119–121**
* **Example 5.4:** rolls 12-month CL calendar spreads while avoiding expiration and applies linear mean reversion to `$\gamma$`. **Source: pp. 123–126**

## Figures and Tables

* **Figures 5.1–5.3:** currency and futures-curve illustrations; Figures 5.2–5.3 explain log prices across maturities and contango/backwardation. **Source: pp. 116–118**
* **Figures 5.4–5.5; Table 5.1:** regression/roll-return diagnostics and annualized average spot/roll returns for futures. **Source: pp. 120–122**
* **Figures 5.6–5.8:** VIX/VX behavior and CL/VX calendar-spread strategy curves. **Source: pp. 122–127**
* **Figures 5.9–5.12:** crack spread, ES/VX regimes, fitted stationary portfolio, and ES–VX mean-reversion returns. **Source: pp. 128–132**

## Applications

Potential uses are cointegrated commodity currencies, mean-reverting calendar-spread roll returns, and selected intermarket spreads such as ES/VX. The text treats them as exceptions demanding empirical tests, not generic futures-pair rules. **Source: pp. 107–132**

## Assumptions, Limitations, and Edge Cases

Currency leverage is high and double-edged; synthetic crosses create multi-currency P&L. The constant-return futures model may fail, especially for VX and distant contracts. Calendar spread stationarity depends on `$\gamma$`, and related markets can diverge in a regime change. Price timestamps/closing times must be synchronized. **Source: pp. 108–109, 121–123, 127–132**

## Common Mistakes and Warnings

* Testing/investing currency series whose point movements lack the same dollar value. **Source: pp. 107, 109–110**
* Ignoring rollover interest and weekday triple rollover. **Source: pp. 112–115**
* Calling any same-underlying calendar spread mean reverting without testing roll return. **Source: pp. 122–123**
* Applying Equation 5.7 to VX. **Source: pp. 126–127**

## Key Takeaways

Mean reversion in currencies/futures is narrow and structural. Correct units, carry, contract maturity, and roll-return behavior matter as much as a statistical signal. **Source: pp. 107–132**

## Glossary

| Term | Definition | Source |
|---|---|---|
| Base / quote currency | First / second currency in a quoted cross-rate. | p. 108 |
| Rollover interest | Interest differential earned or paid for holding a currency position. | pp. 112–114 |
| Contango / backwardation | Futures-curve configurations tied to negative / positive roll return in the model. | pp. 116–121 |
| Calendar spread | Long and short contracts on one underlying with different expirations. | p. 123 |
| Crack spread | Long 3 CL, short 2 RB, short 1 HO in the example. | pp. 128–129 |

## Connections to Other Chapters

Uses Chapter 2’s ADF/half-life and linear mean-reversion machinery, Chapter 3’s log-price/rebalancing treatment, and sets up Chapter 6’s momentum treatment of persistent roll returns. **Source: pp. 111, 123–126, 122**

## Open Questions or Extraction Issues

The PDF’s Equation 5.11 numbering is duplicated in the extracted pages; the source formula is retained as printed. Full code blocks and numeric table rows are summarized, not transcribed line-for-line.

## Quality-control checklist

- [x] Entire assigned chapter examined; major sections, examples, tables, and figures represented.
- [x] Important formulas include symbols, purpose, conditions, interpretation, and locators.
- [x] Output is limited to Chapter 5; source ambiguity is explicitly flagged.
