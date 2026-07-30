---
title: "Mean Reversion of Stocks and ETFs"
chapter: 4
source: "Algorithmic Trading: Winning Strategies and Their Rationale"
status: "extracted"
---

# Chapter 4: Mean Reversion of Stocks and ETFs

## Chapter Overview

Stocks offer many apparent mean-reversion opportunities, but ordinary stock pairs are fragile: individual stocks are generally nonstationary and pairs can lose cointegration after company-specific changes. The chapter contrasts time-series with cross-sectional mean reversion, favors ETF pairs/triplets and diversified baskets over single stock pairs, and develops intraday seasonal and cross-sectional stock strategies. Reported backtests exclude transaction costs and use survivorship-biased stock universes. **Source: pp. 87–88**

## Learning Objectives

* Explain why stock-pair cointegration is unreliable out of sample. **Source: pp. 89–91**
* Apply ETF/basket, intraday gap, ETF-component, and linear long-short approaches. **Source: pp. 91–106**
* Recognize implementation bias from changing index membership, consolidated prices, shorting, and execution timing. **Source: pp. 88–90, 95**

## Key Concepts

### Time-series versus cross-sectional mean reversion

Time-series mean reversion concerns a series reverting toward a mean based on its own history. Cross-sectional mean reversion concerns cumulative returns of instruments in a basket reverting toward the basket cumulative return; the usual time-series tests are largely irrelevant to it. Stock prices may resemble geometric random walks in the long run while exhibiting short-term/seasonal mean reversion when there is no stock-specific news. **Source: pp. 87–88**

### Difficulties of stock pairs

Even economically similar stocks seldom remain cointegrated out of sample. A firm’s management or competitive circumstances can change independently. Diversifying across pairs does not cure the problem when rare broken pairs create losses greater than gains of the good pairs. Short-sale recalls can force loss-making cover transactions (a short squeeze); the alternative uptick rule can restrict short market orders after its circuit breaker. Small NBBO sizes also make intraday fills difficult. **Source: pp. 89–91**

### ETF pairs and triplets

ETF baskets diversify company-specific risk and avoid stock borrowing constraints. Closely related country/sector ETFs may cointegrate, but shared exposure must be genuine and stable; the chapter cautions that correlations/cointegration can change. **Source: pp. 91–92**

### Intraday seasonal mean reversion

A price process that is not mean reverting on daily bars can mean-revert strongly in a defined intraday window. The buy-on-gap model treats an excessive opening decline as liquidity/panic pressure likely to fade; a longer-term moving-average filter rejects stocks more likely to have bad news. **Source: pp. 92–96**

## Mathematical Formulas

### Buy-on-gap entry and return calculations

**Formula**

$$
\operatorname{buyPrice}_{t,i}=L_{t-1,i}(1-z\sigma_{90,t-1,i})
$$

$$
\operatorname{retGap}_{t,i}=\frac{O_{t,i}-L_{t-1,i}}{L_{t-1,i}},\qquad
\operatorname{retO2C}_{t,i}=\frac{C_{t,i}-O_{t,i}}{O_{t,i}}
$$

**Variables**

* `$L$`, `$O$`, `$C$` — prior low, current open, and current close price.
* `$z$` — entry Z-score (1 in the example).
* `$\sigma_{90}$` — 90-day standard deviation of close-to-close returns.
* `$t$`, `$i$` — day and stock.

**Purpose:** identify a one-standard-deviation gap below the previous low and calculate open-to-close profit. **Conditions and assumptions:** inputs are aligned daily open/low/close arrays; execution cannot literally use the official open after observing it. **Interpretation:** buy only stocks opening below the threshold, then close the position at the market close. **Source: pp. 93–94**

### Linear cross-sectional long-short weights

**Formula**

$$
w_i=-\frac{r_i-\langle r_j\rangle}{\sum_k\left|r_k-\langle r_j\rangle\right|}
\tag{4.1}
$$

**Variables:** `$w_i$` is stock `$i$`’s capital weight; `$r_i$` its daily return; `$\langle r_j\rangle$` the equal-weighted universe return; `$k,j$` index universe members. **Purpose:** short relative winners and buy relative losers with gross absolute weight normalized to one. **Conditions:** uses a chosen stock universe and lagged weights for return calculation. **Interpretation:** it is a cross-sectional, not a cointegration-based, bet that relative returns reverse. **Source: pp. 102–104**

## Methods and Procedures

### Buy-on-gap model

1. Compute 90-day close-to-close volatility and a 20-day close moving average, each lagged one day.
2. Select stocks whose opening price is below the prior-low threshold and above the 20-day moving average.
3. Rank qualifying stocks by gap return; buy up to the 10 lowest.
4. Liquidate at the close; divide portfolio P&L by the maximum position count. **Source: pp. 93–94**

Example 4.1 reports APR 8.7% and Sharpe 1.5 for May 11, 2006–April 24, 2012. The mirror short-on-gap version reported APR 46% and Sharpe 1.27, but with steeper drawdowns and short-sale constraints. **Source: pp. 94–96**

### ETF/component-stock arbitrage

1. On a training set, run a Johansen test on each stock with SPY; retain stocks passing the stated test criterion.
2. Form an equal-capital, daily-rebalanced long portfolio of retained stocks, represented by the sum of log prices.
3. Confirm that this portfolio and SPY cointegrate; estimate the resulting eigenvector/weights.
4. Apply the Chapter 2 linear mean-reversion strategy out of sample using the log market value. The example used 2007 training data, found 98 qualifying stocks, and a five-day lookback. **Source: pp. 97–101**

### Cross-sectional linear long-short models

Calculate each stock’s return, subtract equal-weight market return, normalize the opposite-signed deviations according to Equation 4.1, and apply next-day returns to lagged weights. Example 4.3 uses close-to-close returns; Example 4.4 ranks overnight open-versus-prior-close returns and earns intraday close-versus-open returns. The chapter suggests adding a variable such as previous close-to-open return to capture the opening effect. **Source: pp. 102–106**

## Derivations and Proofs

The chapter gives no formal proof. Its reasoning is that equal-capital daily rebalancing makes a basket’s log market value a sum of component log prices, enabling the cointegration test; the cross-sectional rule makes weights sum to zero in relative-return space and scales gross exposure. **Source: pp. 97–104**

## Worked Examples

### Example 4.1: Buy-on-Gap Model on SPX Stocks

Uses `op`, `lo`, and `cl` as `$T\times N$` arrays, `topN=10`, `entryZscore=1`, and `lookback=20`. It selects finite-data stocks opening below the threshold but above the lagged moving average, buys the most negative gaps, then computes open-to-close P&L. **Source: pp. 94–95**

### Example 4.2: SPY versus component stocks

Uses an SPX universe and SPY closes on matching dates. It separates 2007 training from later test data, removes missing observations per test, screens with Johansen tests, retests the equal-capital basket, then trades the log basket/SPY spread. **Source: pp. 97–101**

### Examples 4.3–4.4: Linear long-short stock models

Example 4.3 applies Equation 4.1 to close-to-close returns. Example 4.4 uses overnight returns to set weights and same-day open-to-close returns for P&L. **Source: pp. 102–106**

## Figures and Tables

* **Figure 4.1 — Cumulative Returns of Buy-on-Gap Model:** illustrates the long-only equity curve and the reported decay after 2009 for a traded version lacking rule 2. **Source: pp. 94–95**
* **Figure 4.2 — Cumulative Returns of Short-on-Gap Model:** shows the short-only variant’s higher reported return but steeper drawdown. **Source: pp. 95–96**
* **Box 4.1 — High-Frequency Index Arbitrage:** explains index lag from primary-only trade inputs and seconds-level updates; exploiting it needs direct feeds and millisecond monitoring. **Source: p. 97**
* **Figure 4.3 — SPY/component arbitrage cumulative returns:** reported performance of Example 4.2. **Source: p. 101**
* **Figure 4.4 — Linear long-short model cumulative returns:** reported performance of Example 4.3. **Source: p. 104**

## Applications

Use ETF pairs/triplets where diversification and no borrowing constraint help; use carefully selected constituent subsets rather than fully replicated index arbitrage; use seasonal opening effects or cross-sectional baskets when single pairs are unreliable. **Source: pp. 91–106**

## Assumptions, Limitations, and Edge Cases

Historical S&P 500 composition changes, and proper survivorship-bias-free testing needs historical membership data. Consolidated historical opens/closes can differ from fills at primary-exchange MOO/LOO/MOC/LOC orders. The official open cannot both generate a signal and fill it; pre-open prices add signal noise. Results omit transaction costs, and short-only approaches face borrow/uptick risk. **Source: pp. 88, 90, 95–96**

## Common Mistakes and Warnings

* Treating in-sample pair cointegration as durable out-of-sample cointegration. **Source: p. 89**
* Ignoring bad-news moves when applying a mean-reversion rule. **Source: pp. 93–94**
* Assuming index arbitrage is accessible without high-frequency data/execution. **Source: pp. 96–97**
* Backtesting with current membership or consolidated prices as though they were executable primary-market prices. **Source: pp. 88, 95**

## Key Takeaways

Stocks provide abundant but crowded and execution-sensitive mean-reversion effects. Favor diversification, filters that separate liquidity pressure from information, and cross-sectional baskets; regard all reported results as pre-cost and potentially survivorship biased. **Source: pp. 87–106**

## Glossary

| Term | Definition | Source |
|---|---|---|
| Cross-sectional mean reversion | Basket members’ cumulative returns reverting to the basket return. | p. 88 |
| Short squeeze | Forced cover of a recalled short, typically at an unfavorable price. | p. 90 |
| NBBO | National best bid and offer; its small displayed sizes impede intraday fills. | p. 90 |
| Seasonal mean reversion | Mean reversion confined to a particular short time window. | p. 96 |
| Index arbitrage | Trading discrepancy between an index/ETF/future and a component basket. | pp. 96–101 |

## Connections to Other Chapters

Builds on Chapter 2’s stationarity/linear mean-reversion framework and Chapter 3’s portfolio construction and log-price rebalancing discussion. It points to Chapter 1 for price-source/asynchronicity issues and Chapter 7 for news-driven momentum. **Source: pp. 88, 93, 95, 100**

## Open Questions or Extraction Issues

No source pages are missing in the supplied PDF. Numerical performance values are textbook backtest claims, not independently verified; full MATLAB listings are summarized rather than reproduced verbatim.

## Quality-control checklist

- [x] Entire assigned chapter examined; headings, methods, examples, and key points represented.
- [x] Important formulas, variables, source locators, assumptions, and warnings retained.
- [x] Output is limited to Chapter 4; no outside information added.
