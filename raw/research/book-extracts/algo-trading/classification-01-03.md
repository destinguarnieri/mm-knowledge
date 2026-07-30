# Neutral Classification of Chapters 1–3

## Scope and evidence convention

This classification condenses Chapters 1–3 into a research inventory covering credible backtesting, time-series mean-reversion diagnostics and portfolio construction, and bounded implementation. It uses only the supplied extracts and does not independently establish any textbook claim, historical result, parameter, or causal explanation.

- **Textbook proposal:** a mechanism, rule, parameter, or claim made by the source.
- **Reported textbook result:** a historical result reported in the extracts; it still requires replication.
- **Classifier inference:** a research implication derived by combining supplied material.
- **Not supported by this batch:** a plausible claim that these chapters do not establish.

## Classification map

| Class | Consolidated contents |
|---|---|
| Foundation | Executable backtest specification; stationarity, mean reversion, half-life, and cointegration; portfolio-representation semantics; conditional value of historical evidence |
| Methods | Bias-aware backtesting; significance and randomized-null testing; ADF, variance-ratio/Hurst, CADF, and Johansen screening; out-of-sample validation; transaction-cost and data-quality controls |
| Directions | Screen and trade a single mean-reverting series; construct stationary pairs or portfolios; compare spread/log-spread/ratio signals; compare bounded bands, scaling-in, and dynamic Kalman estimates |
| Shared capabilities | Point-in-time market data, synchronized multi-market data, borrow/cost/execution models, research-to-production code parity, portfolio accounting, and monitoring |
| High complexity | Dynamic state-space hedge ratios/fair value and multi-asset cointegrating portfolios |
| Validation risk | Regime instability, leakage/overfit, artificial reversion from bad ticks, non-executable prices, unlimited exposure, and source-era instrument/platform assumptions |

## Foundational knowledge

- **Textbook proposal:** A backtest is an implementation-level simulation, not merely a return calculation. Price field, session boundary, order type, trigger convention, fill logic, borrow availability, and synchronization of legs can change the result.
- **Textbook proposal:** Even a correctly built and statistically significant historical test is conditional evidence; regime change can invalidate it. More observations or round trips can improve statistical precision without establishing future persistence.
- **Textbook proposal:** Time-series mean reversion concerns a series returning toward its own mean. It is distinct from cross-sectional mean reversion, which these chapters define but defer.
- **Textbook proposal:** The batch treats stationarity and mean reversion as related views tested through level dependence and sublinear variance growth. In its convention, variance scales approximately as $\tau^{2H}$, with $H<0.5$ indicating stationarity and $H=0.5$ a geometric random walk. Stationarity does not imply a fixed price range or $H=0$.
- **Textbook proposal:** ADF tests whether current level helps predict the next change. Under the source's simplified Ornstein–Uhlenbeck interpretation, a negative coefficient $\lambda$ gives the portable decay horizon $t_{1/2}=-\log(2)/\lambda$; a positive $\lambda$ does not describe mean reversion, while a negative value close to zero implies a long half-life and few expected round trips. The half-life can suggest a strategy lookback even when an ADF test does not reject a zero coefficient at the source's stated confidence threshold.
- **Textbook proposal:** Nonstationary constituent prices can form a stationary weighted portfolio. CADF addresses pairs; Johansen addresses multiple series and can yield several independent cointegrating relations and associated weight vectors.
- **Textbook proposal:** Representation determines exposure. A price spread corresponds to fixed share quantities during a trade; a log-price relation corresponds to fixed relative market values; a ratio is another possible signal but is not necessarily stationary.
- **Classifier inference:** Signal definition, position sizing, and executable portfolio construction must be tested as separate layers. A stationary statistic is not automatically a self-financing or capital-bounded trade.

## Transferable research methods

1. Write the proposed strategy as precise executable rules: data fields, timestamps, sessions, order type, signal timing, sizing, exits, and leg synchronization.
2. Audit data conventions and feasibility before evaluating returns: corporate actions, survivorship, primary versus consolidated prices, venue-dependent quotes, futures rolls/settlements, executable closes, borrow, and contemporaneous spread legs.
3. Screen the candidate series with complementary tests rather than one diagnostic alone: ADF for level dependence, variance-ratio/Hurst behavior for scaling, and half-life for practical horizon. For portfolios, use CADF or Johansen and retest the constructed combination.
4. Separate model selection from evaluation with out-of-sample testing or cross-validation. Prefer simpler models where additional complexity is not supported.
5. Evaluate both statistical and trading evidence. The chapter proposes Gaussian-null statistics and Monte Carlo/randomized-signal nulls, while warning that $P(R\mid H_0)$ is not $P(H_0\mid R)$.
6. Model realizability: transaction costs, bid/ask execution, borrow, capital limits, portfolio granularity, and live bad-tick behavior. Compare gross and net results explicitly.
7. Preserve research-to-production parity where feasible by adapting the tested implementation into automated execution, while monitoring live divergence.
8. Use negative diagnostics to narrow rather than overinterpret a direction. Failure to reject random walk is not proof that no trading rule can work; passing stationarity does not identify a profitable parameterization.

## Concrete research directions

### 1. Single-series time-series mean reversion

- **Textbook basis:** ADF, variance-ratio/Hurst, half-life, and a linear position illustration.
- **Core hypothesis/question:** Does a candidate price or log-price series show stable, exploitable negative level dependence at a practical horizon?
- **Applicable markets:** The extracts demonstrate currency screening and describe the method generically for financial series.
- **Required data:** Point-in-time prices at the intended trading frequency, executable price fields, session conventions, and cost inputs.
- **Candidate methods/rules:** Screen with ADF and variance ratio; estimate $\lambda$ by regressing $\Delta y_t$ on $y_{t-1}$ with an intercept; for $\lambda<0$, compute $t_{1/2}=-\log(2)/\lambda$ in the regression's sampling units. Compare a half-life-derived lookback with training-only alternatives, then test a bounded mean-reversion rule. The unbounded linear rule is an illustration, not a production design.
- **Meaningful baselines:** Random-walk null; no-trade; simple fixed-lookback bounded bands; the same rule with randomized signals.
- **Evaluation design:** Fix conventions before testing; select parameters only on training data; report screening uncertainty and out-of-sample gross/net trading evidence; examine regime stability and sufficient independent trades.
- **Major failure modes:** Non-rejection mistaken for proof, in-sample parameter reuse, sparse trades, non-executable prices, omitted costs, regime shifts, and unlimited capital in linear sizing.
- **Continue only if:** Complementary diagnostics and out-of-sample, cost-aware trading results support a stable horizon without relying on unbounded exposure. Narrow or reject the tested specification if evidence disappears after leakage, cost, or capital corrections.

### 2. Cointegrated pair or multi-asset portfolio mean reversion

- **Textbook basis:** CADF for pairs, Johansen for larger baskets, and trading a stationary weighted portfolio.
- **Core hypothesis/question:** Can related nonstationary instruments form a stable, executable stationary combination whose reversion survives realistic implementation?
- **Applicable markets:** The extracts use ETF pairs and a three-ETF basket; the method is framed more generally.
- **Required data:** Synchronized constituent prices, point-in-time universe and instrument metadata, corporate-action handling, executable leg prices, borrow availability, costs, and portfolio weights.
- **Candidate methods/rules:** Estimate pair residuals with CADF or multi-asset eigenvectors with Johansen; test stationarity and half-life of the constructed portfolio; trade with bounded entry/exit rules.
- **Meaningful baselines:** No cointegration/random-walk null; static equal-weight or economically motivated weights; simpler pair versus larger basket; fixed versus re-estimated weights.
- **Evaluation design:** Fit weights only on training data; test relation and strategy on later data; synchronize legs; distinguish statistical spread stability from achievable portfolio P&L; stress borrow, costs, and relation breakdown.
- **Major failure modes:** Cointegration decay, data snooping across combinations, asynchronous closes, nontradable settlement data, unstable weights, short-sale constraints, legging risk, and confusion between statistical weights and executable exposure.
- **Continue only if:** The relation persists out of sample and produces net, bounded-capital performance under executable synchronized prices. Narrow basket size or reject the relation if stability depends on in-sample selection or infeasible legs.

### 3. Portfolio-representation comparison: spread, log spread, and ratio

- **Textbook basis:** The GLD–USO example compares price spread, log-price spread, and ratio signals and explains their different exposure meanings.
- **Core hypothesis/question:** Which representation matches the intended share or market-value mandate and produces the most stable executable signal without manufacturing stationarity?
- **Applicable markets:** Pairs generally; the source particularly notes ratios for currency pairs and demonstrates ETFs.
- **Required data:** Synchronized prices, representation-consistent positions, cost and borrow inputs, and point-in-time estimates of hedge ratios.
- **Candidate methods/rules:** Compare fixed-share price spreads, fixed-relative-value log relations, and ratios under the same bounded entry/exit framework.
- **Meaningful baselines:** Each representation against the others; fixed hedge ratio; no-trade/random-walk null.
- **Evaluation design:** Evaluate signal diagnostics separately from portfolio P&L; hold capital and cost assumptions comparable; test stability and trade feasibility out of sample.
- **Major failure modes:** Representation/sizing mismatch, assuming a ratio is stationary, look-ahead in hedge ratios, incomparable gross exposures, and artificial reversion from leg errors.
- **Continue only if:** The selected representation has a defensible exposure interpretation and retains out-of-sample, cost-aware evidence under comparable risk and capital constraints.

### 4. Bounded band entry/exit and scaling policy

- **Textbook basis:** Bollinger-band entry beyond `entryZscore`, exit at a narrower `exitZscore`, and optional multi-level scaling-in.
- **Core hypothesis/question:** Can explicit thresholds bound capital and improve net execution relative to linear exposure, and does scaling-in add value after controlling risk?
- **Applicable markets:** Any screened mean-reverting single series, pair, or stationary portfolio in the batch.
- **Required data:** Signal history, rolling or otherwise point-in-time mean/volatility estimates, executable prices, costs, and exposure accounting.
- **Candidate methods/rules:** Hold zero or one long/short unit; enter beyond a source-default standardized threshold and exit at a narrower threshold. Compare with multiple entry/exit levels. A source example uses a 20-period ratio lookback; it is not universal.
- **Meaningful baselines:** Unbounded linear sizing; single-level bands; no scaling; no-trade.
- **Evaluation design:** Select lookback and thresholds on training data, then compare turnover, tail exposure, capital usage, and net out-of-sample performance under common risk limits.
- **Major failure modes:** Same-sample optimization, volatility-estimation instability, repeated entry into a breaking relation, cost-heavy turnover, and assuming intuitive scaling must help.
- **Continue only if:** Bounded rules retain net evidence and acceptable capital use out of sample; retain scaling only if it improves the chosen risk/net-return criteria rather than merely an in-sample curve.

### 5. Dynamic hedge ratio and mean estimation

- **Textbook basis:** A Kalman filter updates hidden spread mean and hedge ratio sequentially, avoiding abrupt rolling-window cutoffs.
- **Core hypothesis/question:** Does a dynamic linear state estimate improve forecast and executable net performance over simpler fixed or rolling estimates?
- **Applicable markets:** Pair spreads and the source's fair-value/market-making formulation.
- **Required data:** Sequential synchronized observations, explicit state and measurement models, state/measurement noise covariances, costs, and benchmark estimates.
- **Candidate methods/rules:** Recursive predict/update equations for hidden mean and hedge ratio; trade forecast errors relative to their estimated uncertainty.
- **Meaningful baselines:** Static hedge ratio/mean; rolling-window estimates; bounded fixed-band strategy.
- **Evaluation design:** Set all covariance and initialization choices without future data; compare forecast quality separately from trading quality; test sensitivity to non-Gaussian errors, changing noise assumptions, costs, and bad ticks.
- **Major failure modes:** Violated linear/Gaussian assumptions, tuned covariances, initialization artifacts, dynamic overtrading, erroneous observations, and confusing smoother estimates with better P&L.
- **Continue only if:** It adds stable out-of-sample forecast or net trading value beyond simpler estimators after complexity, turnover, and data-error sensitivity are charged.

## Frontier / high-complexity directions

- **Dynamic fair-value / market-making state estimation:** The source extends Kalman updates to a hidden mean inferred from observed prices and mentions trade price/size in its summary. A serious program would require a precise observation model, live data-quality defenses, execution evaluation, and evidence beyond the pedagogical equations. **Not supported by this batch:** profitable market making or sufficiency of the stated inputs.
- **Adaptive multi-asset cointegration:** Combining Johansen portfolio construction with dynamic parameter estimation is a plausible **classifier inference**, but these chapters do not test that combined system. Complexity includes combination search, stability, portfolio granularity, synchronized execution, and changing weights.

## Strategic capabilities

- Reproducible, point-in-time backtesting with explicit order, price-field, timestamp, and session semantics.
- Research-to-automated-execution code parity plus live reconciliation of expected and actual decisions.
- Multi-asset data synchronization; corporate-action, futures-roll, settlement, quote-source, and survivorship controls.
- Borrow, transaction-cost, bid/ask, fill, legging, and capital/granularity models.
- Statistical testing and resampling, including critical-value conventions and correct null interpretation.
- Training/validation/test separation, experiment tracking, and resistance to repeated-combination data snooping.
- Portfolio representation and accounting that distinguishes shares, market values, gross exposure, and signal units.
- Bad-tick detection and response, especially for spreads where errors can manufacture apparent reversion.

## Source-specific material

- Historical examples use USD.CAD, EWA–EWC, EWA/EWC/IGE, and GLD–USO. These identify demonstrations, not preferred contemporary instruments.
- **Reported textbook result:** USD.CAD variance-ratio output is `h=0`, `pValue=0.367281`; the extract says the random-walk null was not rejected.
- **Reported textbook result:** The source's regression example gives USD.CAD a half-life of about 115 days, then uses the rounded half-life as the lookback for a linear Z-score strategy. The reported P&L is positive with a large drawdown; transaction costs are omitted and the example's half-life/lookback selection uses future sample information.
- **Reported textbook result:** EWA–EWC CADF statistic is reported as `-3.64346635` versus a 5% critical value of `-3.359`, interpreted by the source as cointegration at 95% certainty.
- MATLAB functions/code, FxOne, named market sessions, and source-era venue/instrument conventions are literal implementation context, not portable defaults.
- The GLD–USO ratio illustration uses a 20-period lookback. Entry/exit Z-scores and Kalman initialization/noise choices are proposed test inputs, not constants.

## Claims requiring independent validation

- All reported stationarity, cointegration, and strategy results, including the USD.CAD and ETF examples.
- The source's phrasing of a variance-ratio p-value as an approximately “37% chance of random walk”; the batch itself warns against confusing likelihood under a null with posterior probability of the null.
- ADF/variance-ratio critical values, confidence conventions, sample requirements, deterministic terms, lag choices, and formula transcription.
- The equivalence and practical interpretation of stationarity, mean reversion, and the stated Hurst thresholds for each intended series and sampling design.
- The estimated $\lambda$, the reported USD.CAD half-life of about 115 days, half-life or a small multiple as a lookback selector, fixed thresholds, the 20-period example, scaling-in claims, and any optimized band parameters.
- Cointegrating weights, relation persistence, economic rationale, and whether ratio/log/price representations are stationary and executable.
- Kalman model assumptions, covariance choices, initialization, claimed optimality conditions, and any performance advantage over rolling estimates.
- Costs, borrow availability, market/session rules, contract rolls and settlements, quote source, order behavior, and executable price availability under current conditions.
- The claim that small leg errors tend to inflate mean-reversion backtests more than momentum results, although the operational hazard from bad ticks remains directly relevant as a test requirement.
- **Not supported by this batch:** current profitability, live robustness, a preferred market or representation, universal parameter values, or superiority of the historically best variant.

## Broad one-sheet nominations by theme

- **Research validity:** Executable backtest specification and evidence ladder from diagnostic tests through out-of-sample net and live results.
- **Mean-reversion discovery:** ADF, variance scaling, half-life, CADF, and Johansen as complementary screens with explicit nulls and failure interpretations.
- **Portfolio semantics:** Price spread versus log spread versus ratio, separating signal units from shares, market values, and capital.
- **Bounded implementation:** Band entries/exits, scaling policy, turnover, and capital limits.
- **Adaptive estimation:** Fixed/rolling estimates versus Kalman state updates, with forecast and execution quality evaluated separately.
- **Operational integrity:** Timestamp synchronization, borrow, transaction costs, nontradable prices, bad ticks, and research-to-live parity.

## Source files

- [Chapter 1: Backtesting and Automated Execution](./01-backtesting-and-automated-execution.md)
- [Chapter 2: The Basics of Mean Reversion](./02-the-basics-of-mean-reversion.md)
- [Chapter 3: Implementing Mean Reversion Strategies](./03-implementing-mean-reversion-strategies.md)
