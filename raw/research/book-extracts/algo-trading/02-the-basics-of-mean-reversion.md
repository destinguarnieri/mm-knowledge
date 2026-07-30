---
title: "The Basics of Mean Reversion"
chapter: 2
source: "Algorithmic Trading: Winning Strategies and Their Rationale"
status: "needs-review"
---

# Chapter 2: The Basics of Mean Reversion

## Chapter Overview

This chapter develops time-series mean reversion as a trading property, distinguishes it from cross-sectional mean reversion, and gives tests and constructions for finding it. It covers ADF, Hurst/variance-ratio, half-life, cointegration (CADF and Johansen), then shows linear mean-reverting strategies on a series and on a stationary portfolio. Source: pp. 39–62.

## Learning Objectives

- Distinguish time-series from cross-sectional mean reversion. Source: pp. 39–41.
- Test a series with ADF and variance-ratio methods; interpret Hurst exponent and half-life. Source: pp. 41–48.
- Form and test stationary portfolios through cointegration. Source: pp. 50–58.
- Backtest a basic linear mean-reverting position rule. Source: pp. 48–50, 58–60.

## Key Concepts

### Time-series versus cross-sectional mean reversion

The chapter addresses time-series mean reversion: a series tends to move back toward its own mean. Cross-sectional mean reversion instead concerns instrument returns reverting to a basket’s cumulative return; short-term relative returns are serially anticorrelated. The latter is deferred to the stock/ETF chapter. Source: p. 41.

### Mean reversion, stationarity, and Hurst exponent

Mean reversion and stationarity are equivalent views of this class of series but motivate different tests. A stationary log-price series has variance growing sublinearly with time, approximated by $\tau^{2H}$; $H<0.5$ indicates stationarity, while $H=0.5$ is a geometric random walk. Stationary here does not require range-bound prices or $H=0$. Source: p. 41.

### ADF test

ADF asks whether the current level predicts the next change. Rejecting $\lambda=0$ means the series is not a random walk; for expected mean reversion, the test statistic must be negative and more negative than the relevant critical value. Source: p. 42.

### Half-life

Half-life translates the mean-reversion coefficient into the time needed for a displacement to decay by half: $t_{1/2}=-\log(2)/\lambda$ for negative $\lambda$. The chapter uses it as a practical complement to stringent stationarity tests and to select a strategy lookback. A positive $\lambda$ does not describe mean reversion; a negative value close to zero implies a long half-life and few expected round trips. Source: pp. 46–48.

### Cointegration

While individual financial price series are commonly nonstationary, a weighted portfolio may be stationary. Cointegration identifies such combinations. CADF is applied to two series; Johansen handles more than two and determines the number of independent cointegrating relations and corresponding eigenvectors. Source: pp. 50–58.

## Mathematical Formulas

### ADF regression

**Formula**

$$
\Delta y(t)=\lambda y(t-1)+\mu+\beta t+\alpha_1\Delta y(t-1)+\cdots+\alpha_k\Delta y(t-k)+\epsilon_t
$$

**Variables**

- $y(t)$ — price series at time $t$.
- $\Delta y(t)=y(t)-y(t-1)$ — one-period price change.
- $\lambda$ — level-dependence / mean-reversion coefficient.
- $\mu$ — constant.
- $\beta t$ — deterministic drift term.
- $\alpha_j$ — lagged-change coefficients.
- $\epsilon_t$ — residual/noise term.

**Purpose:** tests $\lambda=0$; rejection indicates dependence of the next change on the current level. **Conditions and assumptions:** critical values depend on sample size and whether nonzero mean or drift is assumed; the chapter simplifies with $\beta=0$ in practical trading. **Interpretation:** a negative $λ is required for expected mean reversion. **Source:** p. 42.

### Variance scaling

**Formula:** $\operatorname{Var}[\log y(t+\tau)-\log y(t)]\approx\tau^{2H}$.

**Variables:** $\tau$ is the separation between measurements; $H$ is the Hurst exponent. **Purpose:** tests whether variance grows more slowly than random-walk variance. **Conditions:** $H<0.5$ signals stationarity; $H=0.5$ is geometric random walk. **Source:** p. 41.

### Ornstein–Uhlenbeck approximation

$$
dy(t)=(\lambda y(t-1)+\mu)dt+d\epsilon
$$

**Variables:** $dy(t)$ is infinitesimal price change; $dt$ time increment; $\lambda,\mu$ are as above; $d\epsilon$ is Gaussian noise. **Purpose:** continuous-time interpretation of ADF for half-life. **Conditions:** drift and lagged differences are ignored. **Source:** p. 46.

### Expected mean-reversion path

$$
E[y(t)]=y_0\exp(\lambda t)-\frac{\mu}{\lambda}\left(1-\exp(\lambda t)\right)
$$

**Variables:** $y_0$ is the initial value; $\lambda<0$ is the mean-reversion coefficient; $-\mu/\lambda$ is the long-run expected level under the simplified process. **Purpose:** shows exponential decay toward $-\mu/\lambda$. **Conditions:** follows the simplified Ornstein–Uhlenbeck form above. **Source:** p. 46, Equation 2.6.

### Half-life of mean reversion

$$
t_{1/2}=-\frac{\log(2)}{\lambda}
$$

**Variables:** $t_{1/2}$ is measured in the sampling interval of the regression; $\lambda$ is estimated by regressing $\Delta y(t)$ on $y(t-1)$ with an intercept. **Purpose:** converts the decay coefficient into the time for an expected displacement to halve. **Conditions:** $\lambda$ must be negative for a positive mean-reversion half-life; a value close to zero produces a very long horizon. **Source:** pp. 46–48.

### Johansen multivariate ADF form

$$
\Delta Y(t)=\Lambda Y(t-1)+M+A_1\Delta Y(t-1)+\cdots+A_k\Delta Y(t-k)+\epsilon_t
$$

**Variables:** $Y$ is a vector of prices; $\Lambda$ and $A_j$ are matrices; $M$ is a constant vector; $\epsilon_t$ residual vector. **Purpose:** test cointegration among multiple series. **Conditions:** chapter assumes no deterministic drift for a stationary portfolio. **Interpretation:** if $\Lambda=0$, there is no cointegration. **Source:** p. 54.

## Methods and Procedures

### Screening a series

1. Run ADF on the price series and inspect whether $\lambda/SE(\lambda)$ rejects $\lambda=0$. Source: p. 42.
2. Run a variance-ratio test on log prices; interpret its null as random walk. Source: pp. 45–46.
3. Estimate half-life to judge trading practicality and choose lookback. Source: pp. 46–48.
4. Backtest a strategy only after these tests; the preliminary tests use every bar and often have greater statistical significance than sparse round-trip results. Source: p. 50.

### Building a stationary portfolio

1. Seek economically or statistically related prices. Source: pp. 50–54.
2. Use CADF for a pair and test the residual/portfolio for stationarity. Source: pp. 51–54.
3. For more than two series, run Johansen; examine Trace and Eigen statistics, cointegrating relations, and eigenvectors. Source: pp. 54–58.
4. Select a stationary portfolio/eigenvector, then estimate its mean-reversion behavior and trade it. Source: pp. 58–60.

## Derivations and Proofs

The half-life discussion drops drift and lagged differences from the discrete ADF equation, yielding the Ornstein–Uhlenbeck form. Its expected path decays exponentially at rate $\lambda$ toward $-\mu/\lambda$; solving $\exp(\lambda t)=1/2$ gives $t_{1/2}=-\log(2)/\lambda$. Source: pp. 46–48.

## Worked Examples

### Example 2.1: USD.CAD ADF

The chapter applies MATLAB ADF tooling to USD.CAD to demonstrate rejection testing for mean reversion. Source: pp. 42–44.

### Example 2.3: USD.CAD variance ratio

Using `vratiotest(log(y))`, the reported output is $h=0$ and $pValue=0.367281$: the random-walk null cannot be rejected; the text describes this as about a 37% chance of random walk. Source: p. 46.

### Example 2.4: USD.CAD half-life

The source regresses $y(t)-y(t-1)$ on $y(t-1)$ plus an intercept and computes `halflife=-log(2)/regress_results.beta(1)`. The reported USD.CAD half-life is about 115 days. The example presents this as a practical horizon diagnostic even though the prior stationarity test did not reach 90% certainty. Source: pp. 46–48.

### Example 2.5: Linear mean-reversion lookback

The source rounds the estimated half-life and uses it as the moving-average and moving-standard-deviation lookback. Position market value is set to the negative price Z-score, and the position is lagged when computing daily P&L. The reported cumulative P&L is positive but has a large drawdown; transaction costs are omitted, and the half-life/lookback choice introduces look-ahead bias in this example. Source: pp. 48–50.

### Example 2.6: EWA–EWC CADF

The CADF statistic is reported as $-3.64346635$, more negative than the 5% critical value $-3.359$, so EWA and EWC are judged cointegrating at 95% certainty. Source: p. 54.

### Examples 2.7–2.8: Johansen portfolio and linear strategy

The chapter extends EWA/EWC with IGE, uses Johansen statistics/eigenvectors to choose a stationary portfolio, and backtests a linear mean-reversion rule on it. Source: pp. 55–60.

## Figures and Tables

- Table/figures in Examples 2.1–2.8 report test output, regression/cointegration relations, and strategy results; they illustrate that statistical tests precede trading-rule evaluation. Source: pp. 42–60.

## Applications

Mean-reversion screening of currencies and portfolios; pair/portfolio construction from related ETFs; choice of trading lookback from half-life. Source: pp. 42–60.

## Assumptions, Limitations, and Edge Cases

- ADF/variance-ratio are demanding (the text cites at least 90% certainty), whereas trading may be profitable with less certainty. Source: p. 46.
- Half-life is meaningful as a positive decay horizon only when the estimated $\lambda$ is negative. A near-zero negative estimate produces a long horizon and correspondingly few expected round trips. Source: pp. 46–48.
- The source suggests a lookback equal to the half-life or a small multiple of it as a natural strategy time scale, but this is a textbook proposal rather than an independently validated universal rule. Source: pp. 47–48.
- Passing a stationarity test does not identify a profitable parameterization; it supports eventual discoverability of one. Source: p. 50.
- The simple linear example uses in-sample data for half-life/lookback and has no cap on portfolio market value; the author does not recommend it as a practical strategy. Source: p. 50.
- Cointegration may fail over time. Source: pp. 59–60.

## Common Mistakes and Warnings

- Confusing stationarity with price variance independent of time. Source: p. 41.
- Treating a non-rejection of random walk as proof that trading is impossible. Source: pp. 46–50.
- Using a linear illustration with unlimited capital as a production strategy. Source: p. 50.
- Treating individual nonstationary prices as the only possible tradable objects rather than testing portfolios. Source: p. 50.

## Key Takeaways

Mean-reversion research begins with properties of the price series or portfolio: level dependence, subdiffusive variance, half-life, and cointegration. ADF, variance ratio, CADF, and Johansen provide complementary evidence; a practical strategy then needs risk-aware implementation beyond the chapter’s linear demonstrations. Source: pp. 41–62.

## Glossary

| Term | Definition | Source |
|---|---|---|
| ADF | Test of whether a series’ next change depends on its current level. | p. 42 |
| Hurst exponent | Variance-scaling exponent; below 0.5 indicates stationarity here. | p. 41 |
| Half-life | Time associated with decay of a mean-reverting displacement. | pp. 46–48 |
| Cointegration | Stationarity of a constructed portfolio of otherwise nonstationary prices. | p. 50 |
| CADF | Cointegration ADF test for a pair. | pp. 51–54 |

## Connections to Other Chapters

- Cross-sectional mean reversion is deferred to Chapter 4. Source: p. 41.
- The simple linear position rule is made more practical in Chapter 3; Chapter 5 contains another practical version. Source: p. 50.

## Open Questions or Extraction Issues

- Mathematical notation is transcribed from the PDF text layer; the residual symbol in equations may be visually ambiguous in the source extraction.
- The current extraction jumps from Example 2.1 to Example 2.3, so Example 2.2 has not been reconciled against the source.
- This file predates the source-coverage inventory requirement in the extraction prompt. A full equation/example/figure/table reconciliation is still required before restoring `status: "extracted"`.

## Quality-control checklist

- [x] Entire chapter range examined (pp. 39–62)
- [x] Major headings, tests, formulas, examples, limitations, and connections represented
- [x] Formula variables and conditions stated
- [x] Source locators included
