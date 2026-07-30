---
title: "Implementing Mean Reversion Strategies"
chapter: 3
source: "Algorithmic Trading: Winning Strategies and Their Rationale"
status: "extracted"
---

# Chapter 3: Implementing Mean Reversion Strategies

## Chapter Overview

This chapter turns the prior chapter’s tests and linear demonstrations into tradable design choices: price spreads, log-price spreads, and ratios; Bollinger-band entries/exits; scaling-in; dynamic hedge-ratio estimation by Kalman filter; and data-error control. It explicitly warns that the book’s prototype backtests omit transaction costs and may use look-ahead bias for simplicity; readers must remove those flaws in production research. Source: pp. 63–85.

## Learning Objectives

- Choose a portfolio representation consistent with intended share or market-value exposure. Source: pp. 64–66.
- Implement bounded-capital Bollinger-band rules and understand scaling-in tradeoffs. Source: pp. 70–74.
- Use a Kalman filter to update a mean and hedge ratio without arbitrary rolling-window cutoff. Source: pp. 75–82.
- Detect and control data errors especially dangerous to spread strategies. Source: pp. 83–85.

## Key Concepts

### Price, log-price, and ratio signals

A price-spread portfolio uses price weights/hedge ratios. It fixes numbers of shares during a trade. Log-price cointegration instead corresponds to fixed relative market values. A ratio can be a useful signal, particularly for currency pairs, but may not be stationary when a true cointegrating relation is absent. Source: pp. 64–69, 85.

### Bollinger bands

The previous linear rule has no capital limit because deviation from a moving average is unbounded. A Bollinger-band strategy enters only beyond `entryZscore` standard deviations and exits at `exitZscore`, with `exitZscore < entryZscore`; it holds zero or one long/short unit, simplifying allocation and risk control. Source: pp. 70–71.

### Scaling-in

Scaling-in uses multiple entry/exit levels rather than a single entry. The chapter notes that its apparent common-sense appeal is challenged by research, yet it may help live trading when volatility and probabilities change. Source: pp. 72–74, 85.

### Kalman filter

The Kalman filter is an optimal linear estimator of hidden state given observations under linear, Gaussian-noise assumptions; it minimizes mean squared estimation error. Here it continuously estimates spread mean and hedge ratio, avoiding abrupt rolling-window changes. Source: pp. 75–77.

### Data-error risk

Small errors in legs of a spread can make a mean-reverting backtest look better by creating artificial reversion, while momentum is generally not inflated in the same way. Live bad ticks can still trigger wrong trades. Source: pp. 83–85.

## Mathematical Formulas

### Stationary price portfolio and pair spread

$$y=h_1y_1+h_2y_2+\cdots+h_ny_n$$

$$y=y_1-hy_2$$

**Variables:** $y$ is the constructed stationary portfolio price; $y_i$ constituent prices; $h_i$ share weights/hedge ratios; $h$ pair hedge ratio. **Purpose:** construct a tradable stationary portfolio. **Conditions:** weights are from regression or Johansen eigenvectors; the minus sign anticipates long/short pair exposure. **Source:** p. 64.

### Log-price portfolio

$$\log(q)=h_1\log(y_1)+h_2\log(y_2)+\cdots+h_n\log(y_n)$$

**Variables:** $q$ is the log-price-based portfolio measure; $y_i$ are prices; $h_i$ are hedge ratios. **Purpose:** form a relation consistent with fixed constituent market values. **Source:** p. 64.

### Kalman forecast/update equations

$$\hat\beta(t|t-1)=\hat\beta(t-1|t-1)$$
$$R(t|t-1)=R(t-1|t-1)+V_w$$
$$\hat y(t)=x(t)\hat\beta(t|t-1)$$
$$Q(t)=x(t)'R(t|t-1)x(t)+V_e$$
$$e(t)=y(t)-x(t)\hat\beta(t|t-1)$$
$$\hat\beta(t|t)=\hat\beta(t|t-1)+K(t)e(t)$$
$$R(t|t)=R(t|t-1)-K(t)x(t)R(t|t-1)$$
$$K(t)=R(t|t-1)x(t)/Q(t)$$

**Variables:** $y$ observable price; $x$ observation vector; $\beta$ hidden state (spread mean and hedge ratio in this application); $R$ state-estimation-error covariance; $V_w,V_e$ state and measurement noise variances; $Q$ forecast-error variance; $e$ forecast error; $K$ Kalman gain. **Purpose:** sequentially update hedge ratio and mean. **Conditions:** linear observation/state relations and Gaussian zero-mean noises; initialization given as $\hat\beta(1|0)=0$, $R(0|0)=0$. **Interpretation:** observations shift the previous state estimate by gain times surprise. **Source:** Box 3.1, pp. 77–78.

### Market-making mean update

$$y(t)=m(t)+\epsilon(t)$$
$$m(t)=m(t-1)+\omega(t-1)$$
$$m(t|t)=m(t|t-1)+K(t)[y(t)-m(t|t-1)]$$
$$Q(t)=\operatorname{Var}(m(t))+V_e$$
$$K(t)=R(t|t-1)/(R(t|t-1)+V_e)$$
$$R(t|t)=(1-K(t))R(t|t-1)$$

**Variables:** $m$ hidden mean; $y$ observed price; $\epsilon,\omega$ measurement/state noise; other symbols as above. **Purpose:** dynamically estimate expected price and uncertainty. **Source:** pp. 82–83.

## Methods and Procedures

### Implementing bounded mean reversion

1. Estimate a spread/log-spread/ratio and confirm its mean-reversion rationale. Source: pp. 64–69.
2. Compute rolling mean and standard deviation using a selected lookback; the text permits optimizing on training data or using half-life. Source: p. 70.
3. Enter only beyond `entryZscore`; exit at the narrower `exitZscore`. $0$ means exit at current mean; $-entryZscore$ exits beyond the opposite band. Source: p. 70.
4. Constrain exposure to one long/short unit unless deliberately using scaling-in. Source: p. 70.
5. Include costs, proper out-of-sample parameter selection, and data cleaning in real implementation. Source: pp. 63–64, 83–85.

### Kalman-filter hedge ratio

1. Define observable variable, hidden variable, state-transition model, and observation model. Source: pp. 75–76.
2. Specify measurement and state noise covariance. Source: pp. 76–78.
3. Predict state/covariance, observe price, compute forecast error and gain, then update state/covariance each bar. Source: Box 3.1, pp. 77–78.

## Derivations and Proofs

The text motivates the Kalman specification from linear state and measurement relations, Gaussian noise, and minimum mean-square error; Box 3.1 supplies the recursive equations rather than a proof. Source: pp. 75–78.

## Worked Examples

### Example 3.1: GLD–USO representations

The example compares price spread, log price spread, and ratio for GLD–USO, applies linear mean reversion, and discusses changing hedge ratio. The sample ratio code uses a 20-period lookback and standardized deviation to set paired positions. Source: pp. 67–70.

### Example 3.2: Bollinger-band GLD–USO

The example replaces the linear rule with a Bollinger-band mean-reversion strategy. Source: pp. 71–72.

### Example 3.3: Kalman-filter mean reversion

The example applies the dynamic filter to hedge ratio/mean estimation and then determines entry and exit signals. Source: pp. 78–81.

## Figures and Tables

- Box 3.1, “The Iterative Equations of the Kalman Filter,” defines predictions, forecast variance/error, gain, and updates. Source: pp. 77–78.
- Example result figures compare GLD–USO signal representations and strategy behavior; Kalman figures show dynamic estimates and forecast-error standard deviation. Source: pp. 67–81.

## Applications

- Pair trading with fixed shares, fixed market values, or currency ratios. Source: pp. 64–69.
- Capital-bounded band trading with explicit entry/exit thresholds. Source: p. 70.
- Dynamic fair-value estimation / market making from latest price (and, as summarized, trade price and size). Source: pp. 82–85.

## Assumptions, Limitations, and Edge Cases

- Backtests shown omit transaction costs and may contain look-ahead bias from fitting and testing on the same data; these are pedagogical simplifications, not endorsed production practice. Source: pp. 63–64.
- Linear exposure can require unlimited capital. Source: p. 70.
- Kalman optimality is conditional on its linear/Gaussian model assumptions. Source: pp. 75–76.
- Rolling estimates can jump when an old observation leaves and a new one enters. Source: p. 75.

## Common Mistakes and Warnings

- Using price-weighted hedge ratios when fixed market value is the actual mandate, or vice versa. Source: pp. 64–66.
- Optimizing band parameters on the same sample used for performance claims. Source: pp. 63–64, 70.
- Ignoring costs, data errors, or live bad ticks. Source: pp. 63–64, 83–85.
- Assuming a backtest-improving data error is harmless. Spread strategies are especially sensitive. Source: pp. 83–85.

## Key Takeaways

Mean-reversion implementation must specify the portfolio representation, bounded entry/exit logic, parameter-estimation method, and data-quality controls. Bollinger bands make the linear idea tradable with explicit capital control; Kalman filtering offers a dynamic alternative to abrupt rolling estimates, but remains model-dependent. Source: pp. 63–85.

## Glossary

| Term | Definition | Source |
|---|---|---|
| Hedge ratio | Weight/number of shares assigned to a constituent in a spread. | p. 64 |
| Bollinger band | Mean and standard-deviation thresholds used for entry/exit. | p. 70 |
| Scaling-in | Use of multiple position-entry/exit levels. | pp. 72–74 |
| Kalman gain | Weight applied to the forecast error in state update. | p. 77 |
| Forecast error | Difference between observed price and predicted observation. | p. 77 |

## Connections to Other Chapters

- Uses Chapter 2’s cointegration, half-life, and linear mean-reversion framework. Source: pp. 63–64.
- Reiterates Chapter 1’s transaction-cost, look-ahead, and data-quality warnings. Source: pp. 63–64.

## Open Questions or Extraction Issues

- Equations use PDF text-layer notation; transpose notation $x(t)'$ and noise glyphs should be checked visually if typesetting needs to match the printed page exactly.

## Quality-control checklist

- [x] Entire chapter range examined (pp. 63–85)
- [x] Major methods, examples, Box 3.1 equations, warnings, and key points represented
- [x] Formula variables and validity conditions supplied
- [x] Source locators included
