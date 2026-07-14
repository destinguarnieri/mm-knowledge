---
title: "Applied Machine Learning"
chapter: 6
source: "Hands-On AI Trading with Python, QuantConnect, and AWS"
source_file: "/Users/destinguarnieri/Desktop/Hands-On AI Trading with Python QuantConnect and AWS.epub/OPS/c006.xhtml"
status: "extracted"
---

# Chapter 6: Applied Machine Learning

## Overview

This chapter is a portfolio of 19 applied machine-learning studies rather than a single linear lesson. It moves from research notebooks to complete trading systems and covers regression, classification, preprocessing, PCA, clustering, hidden-state models, SVMs, regularized regression, tree models, temporal CNNs, Gaussian Naive Bayes, GPT-4, Amazon Chronos, and FinBERT. Across asset classes, the repeated engineering pattern is: define a tradable target; assemble point-in-time features and labels; train on trailing data; schedule retraining; convert predictions into bounded portfolio weights or execution decisions; persist model state when necessary; and test parameter sensitivity, crisis behavior, costs, and live/backtest differences. Source: pp. 143–280.

## Learning Objectives (inferred)

- Translate a prediction problem into features, labels, training cadence, and trading rules.
- Compare ML methods according to data shape, interpretability, nonlinearity, computational cost, and overfitting risk.
- Apply preprocessing, dimensionality reduction, clustering, classification, regression, and pretrained foundation models.
- Avoid leakage when constructing future-return labels and using pretrained models.
- Integrate models with universe selection, consolidators, scheduled training, Object Store persistence, options/futures mechanics, and portfolio optimization.
- Interpret sensitivity plots and operational limitations rather than relying on one headline backtest. Source: pp. 143–280.

## Applied Examples

### Example 1 — ML Trend Scanning with MLFinLab

**Objective and type.** Classify BTCUSD as downtrend/no-trend/uptrend in an easy research notebook using MLFinLab trend scanning, then invest in the detected primary trend. Source: pp. 143–148.

**Data, target, and model.** Input is the BTCUSD close series. For each observation, the method fits linear regressions over candidate lookbacks within a 20-point window, chooses the regression whose slope has the largest absolute t-statistic, and labels the sign as −1, 0, or +1. Returned fields include label start/index, strongest-trend end `t1`, t-value, period return, and sign bin. Source: pp. 144–145.

**Trading design.** Recompute and rebalance daily; hold 100% BTC when the trend is upward and otherwise 100% cash. Accuracy compares predicted signs with the next daily close-change sign. Source: pp. 146–148.

**Results and limitations.** Directional accuracy is 51.2%, only slightly better than chance, yet the strategy equity exceeds buy-and-hold in the shown test. This demonstrates that classification accuracy alone does not determine trading value: conditional payoff and avoided drawdowns matter. The selected lookback and retrospective trend endpoint can create timing sensitivity and must be implemented without leaking future closes. Figures 6.1–6.3 show labeled trends, strategy versus benchmark, and observed versus predicted log price. Source: pp. 145, 147–148.

### Example 2 — Factor Preprocessing Techniques for Regime Detection

**Objective.** Compare raw, stationary, standardized, and PCA-transformed factors for classifying whether SPY's next weekly open-to-open return is positive. Source: pp. 148–154.

**Data and design.** Daily SPY data span January 1, 2000–January 1, 2024. Factors are deliberately random, with one made nonstationary. A LightGBM multiclass classifier is trained on the first 75% and evaluated on the remaining 25%; the text's summary table calls the model a random forest, an internal inconsistency. Labels are 1 for positive future weekly return, otherwise 0. Stationarity is checked with augmented Dickey–Fuller; transformations include fractional differentiation, zero-mean/unit-variance scaling, and PCA. Source: pp. 148–153.

**Results.** OOS accuracy: raw 0.6101; stationary 0.5849; standardized 0.5882; PCA 0.5962. None improves on raw because the factors are random; preprocessing choice is data-specific. Figures 6.4–6.9 account for label direction/count and predicted class probabilities under each transformation; the result table is `ch6_unnum6`. Source: pp. 149–154.

**Limitations.** Random factors make this a pipeline demonstration, not evidence of tradable predictability. Standardization is needed before PCA and for comparing differently scaled inputs; stationarity transformations should not be presumed beneficial. Source: pp. 151–154.

### Example 3 — Reversion vs. Trending: Strategy Selection by Classification

**Objective.** Predict whether the next day favors momentum or reversal and switch between SPY and TLT. Source: pp. 154–158.

**Features and target.** Four standardized features describe the volatility regime: 21-day SPY RSI; 21-day ATR normalized by 21-day price SMA; 21-day standard deviation of daily SPY returns; and VIX. Kenneth French momentum and short-term reversal factor series determine label 1 (momentum favored) or 0 (reversion favored). Source: pp. 155–157.

**Model and testing.** Keras sequential neural network: four inputs, an 8-neuron dense layer, and one sigmoid output. Adam minimizes binary cross-entropy over 100 epochs. The model is trained once before the backtest. In-sample accuracy is 55.48%; OOS is 52.77%, versus 54.4% SPY up-days over 2014–2024 and 50% random guessing. The weak OOS result suggests better inputs or architecture, not production readiness. Source: pp. 155–157.

**Trading rules.** Rebalance at each market open: 100% SPY for predicted momentum, otherwise 100% TLT. RSI/ATR use built-in indicators; return volatility is custom. Source: pp. 157–158.

### Example 4 — Alpha by Hidden Markov Models

**Objective.** Use a two-state Markov-switching regression on trailing three years of daily SPY returns to classify low- versus high-volatility regimes, then compare three allocations. Train daily one minute after open and rebalance immediately. Source: pp. 158–170.

**Regime context.** The descriptive chart annualizes rolling 21-day return volatility; values below the 25th percentile are low-volatility and above the 75th percentile high-volatility. The actual model label is state 0/1 from Markov regression, not simply the chart threshold. Source: pp. 159–160.

**Algorithms.** (1) Low volatility: 100% SPY; high: 100% TLT. (2) Low: short one SPY straddle; high: long one SPY straddle. (3) same regime rule using SPX index-option straddles. A straddle combines same-strike, same-expiry call and put; long benefits from a sufficiently large move, while short earns premium if movement remains small. Source: pp. 160–162.

**Implementation and limits.** Fit `MarkovRegression` with two regimes and switching variance. Option code selects contracts, constructs strategies, tracks fills/remaining legs, and handles assignment; European-style SPX removes early-exercise cleanup needed for American-style SPY options. Options introduce expiry, spreads, margin, assignment, and path-dependent loss risks not captured by regime accuracy alone. Figures 6.10–6.17 cover regimes, payoff, and two performance sheets per algorithm. Source: pp. 159–170.

### Example 5 — FX SVM Wavelet Forecasting

**Objective.** Forecast each forex pair's next close by decomposing prices into wavelet components, predicting each component with SVR, and reconstructing the signal. Trade EURJPY, GBPUSD, AUDCAD, and NZDCHF; EURUSD is benchmark. Source: pp. 170–175.

**Model.** Symlet-10 (`sym10`) wavelet, three levels, 152 observations, denoising scale 0.5. Approximation coefficients are retained; detail coefficients are thresholded. Each coefficient series is split into rolling 10-value samples, and SVR hyperparameters are grid-searched over `C=[.05,.1,.5,1,5,10]` and `epsilon=[.001,.005,.01,.05,.1]` using negative MSE. One-step forecasts replace the last coefficient before inverse reconstruction. Source: pp. 171–175.

**Trading.** Retrain on each daily bar. Expected return is forecast/current close − 1; trade only above `weight_threshold=0.005`, scaling ideal weight by leverage 20. Source: pp. 172–173.

**Results/limits.** Period sensitivity tests 63–189 days by 21; Sharpe peaks near eight months but varies sharply between neighboring periods, and thresholds above 0.004 generally fare better. The instability warns against trusting the optimum. Figures 6.18–6.19. Source: p. 174.

### Example 6 — Dividend Harvesting Selection of High-Yield Assets

**Objective.** Predict next dividend yield and weight the highest-yield opportunities. Universe: top 100 QQQ constituents by ETF weight, refreshed monthly. Source: pp. 175–181.

**Features/model.** Decision-tree regressor using P/E, revenue growth, free-cash-flow/operating-cash-flow, dividend payout ratio, and current ratio; label is dividend yield (dividend per share / share price). Per-symbol state contains five years of factor/label history and its model. Source: pp. 176–180.

**Portfolio.** Train 30 minutes before open on the first trading day monthly and rebalance afterward. Weight each asset by predicted yield divided by the sum of positive predicted yields. Dividend receipts are charted and logged. Source: pp. 177–180.

**Results/limits.** Sharpe spans 0.476–0.617, improves with larger universes, and is more sensitive to universe size than 4–8 year lookback. All tested combinations are positive. Sparse dividends, changing company policy, tree instability, and price-driven yield traps limit inference. Figures 6.20–6.21. Source: p. 180.

### Example 7 — Effect of Positive-Negative Splits

**Objective.** Predict three-day post-announcement return for technology stocks undergoing splits, then trade the predicted direction. Source: pp. 181–184.

**Data/model.** Morningstar technology universe; multiple linear regression features are announced split factor and one-month XLK sector return. Train monthly at midnight using four years of split and price history. Source: pp. 181–184.

**Trading.** At split warnings, exclude XLK, predict return, and open only positive predicted trades. Maximum four concurrent positions, 25% capital each; adjust quantity when the split occurs and exit after `hold_duration`. Source: pp. 182–184.

**Results/limits.** Three-day hold gives the highest Sharpe; all tested holding/lookback combinations have Sharpe ≥0.7 and outperform XLK in the shown backtest. Split events are sparse, selection/corporate-action timing is critical, and the prose says “liquidates after 1 week” while configured optimum is three days. Figures 6.22–6.23. Source: p. 183.

### Example 8 — Stop Loss Based on Historical Volatility and Drawdown Recovery

**Objective.** Compare downside protection for KO: fixed stop, LASSO-predicted stop, and LASSO-selected put protection. Source: pp. 184–197.

**Model.** VIX, trailing ATR, and trailing return standard deviation predict the weekly low return (week open to minimum low over five sessions). LASSO selects factors and regularizes correlated inputs. Train two minutes after open on the first trading day weekly. Source: pp. 185–187.

**Algorithms.** Each buys $100,000 KO weekly. (1) stop at 95% of entry and liquidate leftovers next week; (2) stop $0.01 below predicted low; (3) replace stop with a put below predicted low. Hold 100% KO exposure. The common model enables comparison, but option premium, strike availability, expiry, spread, and exercise make algorithm 3 economically different. Figures 6.24–6.29 provide performance/sensitivity for all three. Source: pp. 187–190.

### Example 9 — ML Trading Pairs Selection

**Objective.** Discover candidate equity pairs through PCA, OPTICS clustering, cointegration, Hurst exponent, half-life, and mean-cross frequency. This is selection research, not a complete traded portfolio. Source: pp. 197–207.

**Data/process.** Select securities trading January 3, 2024; retrieve about three years of closes; drop incomplete histories, leaving 927; standardize daily returns; reduce to three PCs; cluster the 3-D exposures with OPTICS. Within each cluster, examine every pair. Source: pp. 197–201.

**Four filters.** (1) bidirectional Engle–Granger tests and retain the lower statistic with p≤1%; (2) spread Hurst exponent <0.5; (3) half-life strictly between one day and one year; (4) at least 12 mean crossings/year, 36 total. Of 1,357 pairs, 1,315 fail cointegration, then 11 fail Hurst; 30 candidates remain. Source: pp. 201–207.

**Limits.** Multiple testing, same-date universe survivorship, pair instability, estimated hedge-ratio error, execution costs, borrow, and crowding remain. Figures 6.30–6.34 show PC space, clusters, filter attrition, and each candidate pair/spread. Eleven unnumbered diagnostic figures (`newfig6_1`, `newfig6_3`–`newfig6_14`) are individual candidate pair/spread panels supporting Figure 6.34. Source: pp. 199–207.

### Example 10 — Stock Selection through Clustering Fundamental Data

**Objective.** Rank future one-month equity returns using PCA-compressed fundamentals and LightGBM LambdaRank. Source: pp. 207–213.

**Data/model.** Monthly select 100 most liquid fundamental equities; standardize up to 100 factors, discard assets with fewer than 20 usable factors, retain five PCs, and label each asset by its cross-sectional rank of 22-trading-day forward return. `LGBMRanker` models nonlinear interactions; groups correspond to rebalance dates. Source: pp. 208–213.

**Trading/results.** Choose top ten predictions and equal-weight 10%; train monthly and rebalance one minute after open. Parameters: liquid universe 100, final 10, 365-day lookback, five PCs. Smallest final universe and component counts give best tested Sharpe; changing PCs 3→4 at universe five drops Sharpe 0.45→0.09, showing sensitivity. Figures 6.35–6.36. Source: p. 211.

### Example 11 — Inverse Volatility Rank and Allocate to Futures Contracts

**Objective.** Forecast next-week opening-return volatility and allocate more to lower-volatility front-month futures. Source: pp. 213–220.

**Universe/features.** VIX; S&P, Nasdaq, and Dow E-minis; Brent, gasoline, heating oil, natural gas; corn, oats, soybeans, wheat. Ridge features: three-month closing-return volatility, ATR, and open interest; label is future opening-return volatility. Ridge addresses collinearity and shrinks unstable coefficients. Source: pp. 214–219.

**Portfolio.** Train weekly two minutes after open; weight is described as `3 / sigma / sum(sigma) / contract_multiplier`. Factor 3 is empirical: 1 leaves trades below the minimum-order-margin threshold, while larger values risk margin calls. Parameters use three-month ATR/std and 365-day training set. Source: pp. 215–219.

**Results/limits.** Six-month indicators generally yield highest Sharpe, three-month lowest; all tested combinations profitable. Roll/mapping, multiplier scaling, margin, cross-contract covariance, and the unusual normalization formula require scrutiny. Figures 6.37–6.38. Source: pp. 217–218.

### Example 12 — Trading Costs Optimization

**Objective.** Delay BTCUSD liquidation until a decision-tree model predicts below-normal cost per dollar. Source: pp. 220–228.

**Features/label.** Absolute quantity, ATR, average daily volume, `(ask-bid)/bid`, and top-of-book dollar size predict realized commission plus slippage. A custom spread-slippage model proxies market-order cost. Source: pp. 221–224.

**Experiment.** Benchmark buys 10 BTC at midnight and liquidates at 01:00 daily, recording fills. Candidate also buys at midnight, then waits between 01:00 and 23:59 for predicted cost/dollar below the trailing 10-day average; force-liquidate at 23:59 and tag time-limit orders. Train monthly after enough samples; persist fills as benchmark/candidate CSVs. Source: pp. 222–228.

**Result/limits.** Delayed fills before the time limit save $36,260.20 in the study. Figures 6.39–6.42 show learning-related cost decline, saved-cost distributions, delay duration, and forced exits. Comparing asynchronous fills introduces price-risk/opportunity-cost exposure; a spread-based simulated slippage model can make realized savings circular. Source: pp. 224–228.

### Example 13 — PCA Statistical Arbitrage

**Objective.** Find stocks whose standardized log returns fall materially below PCA-factor expectations and buy for mean reversion. Source: pp. 228–233.

**Data/model.** Monthly universe: 100 most liquid stocks priced above $5. Standardized log returns are reduced to three PCs; per-stock OLS predicts standardized log return. The latest residual z-score is the signal. Source: pp. 229–232.

**Trading/results.** Select residual z<−1.5 and weight opposite the deviation, normalized across positions; retrain/rebalance monthly just after open. Tested Sharpe peaks at three PCs and 126-day lookback; 3–4 month lookbacks generally weakest; all combinations profitable. Default lookback is 63 days, threshold 1.5. Adjusted price history is required. Figures 6.43–6.44. Source: pp. 231–232.

### Example 14 — Temporal CNN Prediction

**Objective.** Predict weekly direction—up, down, stationary—from trailing OHLCV for the three largest QQQ constituents. Source: pp. 233–242.

**Model.** Input is 15 days × five OHLCV variables. Parallel 1-D convolution branches capture long-, mid-, and short-term patterns; concatenate, flatten, and output three one-hot classes with categorical cross-entropy. Labels derive from future change in a five-day rolling-average close around a stationarity threshold. StandardScaler is fitted through a temporary 2-D representation; training uses 20 epochs for demonstration. Source: pp. 234–241.

**Trading.** Train Monday/first trading day at 09:00; trade two minutes after open. Ignore stationary or confidence≤55%; assign +confidence for up and −confidence for down, then normalize absolute weights to ≤1. Split handling rebuilds data correctly. Source: pp. 237–242.

**Results/limits.** Sharpe generally improves with more training samples, but most combinations are unprofitable. Defaults: 500 samples, universe three. Larger universes make backtests exceed an hour. Figure 6.45 is architecture; Figures 6.46–6.47 performance and sensitivity. Source: pp. 236, 239–240.

### Example 15 — Gaussian Classifier for Direction Prediction

**Objective.** Use GNB to classify 22-session future technology-stock return sign as −1/0/+1. Source: pp. 242–250.

**Features/model.** For each asset, four days of engineered returns—intraday open-to-close and overnight open-to-open sign—feed an interpretable Gaussian/conditional-independence classifier. Weekly universe: ten largest Morningstar technology stocks. Source: pp. 242–249.

**Trading/results.** Train at 09:00 on first trading day weekly; two minutes after open, equal-weight only +1 predictions. Defaults: four days/sample, 100 samples, ten assets. All tested combinations profitable; Sharpe best at universe five, likely because feature dimension/noise grows with assets. Figures 6.48–6.49. Source: pp. 243–245.

**Implementation.** Daily consolidators build feature/label histories and warm them on additions; splits force dataset reinitialization. Live mode pickles models, loads at initialization, updates during training, and saves at algorithm end. GNB's Gaussian and independence assumptions may not fit market returns. Source: pp. 245–250.

### Example 16 — LLM Summarization of Tiingo News Articles

**Objective.** Ask GPT-4 to aggregate hourly TSLA news sentiment on a −10…+10 scale, then trade changes in sentiment. Source: pp. 250–256.

**Research/data.** TiingoNews articles from November 1, 2023–March 1, 2024 are grouped by date/hour and deduplicated. Hourly batches reduce API calls and smooth scores. Research writes date-partitioned CSVs (`hour`, sentiment, article volume) to Object Store; a custom data class injects them into the backtest. Source: pp. 250–255.

**Trading/results.** Rebalance hourly after open: flat/increasing sentiment triggers 100% long even if still negative; negative and decreasing triggers 100% short. A rate-of-change indicator tracks direction. Strategy Sharpe 1.695 versus −0.06 for TSLA buy-and-hold in this short sample. Figures 6.50–6.51. Source: pp. 251–256.

**Limits.** Very short, single-stock sample; prompt/model-version nondeterminism; API cost/latency; article timestamp/duplication; and preprocessing performed outside event-time simulation all threaten reproducibility and leakage control. Source: pp. 250–256.

### Example 17 — Head-and-Shoulders Pattern Matching with CNN

**Objective.** Train a 1-D CNN on synthetic head-and-shoulders patterns and random walks, then detect the pattern in USDCAD. Source: pp. 256–265.

**Model/training.** Each sample has 25 points. Conv1D uses 32 filters, kernel 5, ReLU; max-pool size 2; flatten; sigmoid output. Generate 100,000 noisy positive patterns from seven key vertices plus interpolated points and 100,000 random-walk negatives; alternate classes, standardize, split 80/20, and train once. Test accuracy is 99.9% on synthetic data, which does not establish real-market generalization. Source: pp. 257–265.

**Trading.** For each daily close, test lookbacks 25–100 days in steps of 10, downsample each to 25 points, standardize, and infer. If any class-1 confidence ≥ threshold, short $10,000 USDCAD and hold ten days. Source: pp. 258–261.

**Results.** All tested confidence/holding combinations profitable; Sharpe rises with holding period and falls with confidence threshold, likely because trades become sparse. Defaults: max 100, step 10, confidence .8, hold 10. Figure 6.52 defines pattern/neckline; Figures 6.53–6.54 results; Figure 6.55 synthetic sample. Source: pp. 256, 261–264.

### Example 18 — Amazon Chronos Model

**Objective.** Forecast three months (63 trading days) of prices for five liquid S&P 500 constituents with `amazon/chronos-t5-tiny`, then maximize forecast Sharpe under long-only full-investment constraints. Compare base and monthly fine-tuned models. Source: pp. 265–272.

**Data/design.** Select top five liquid SPY constituents monthly; use one year of daily closes. Base model needs no training; fine-tuned version trains at midnight on the month's first trading day. Rebalance quarterly using median forecasts from the predictive distribution. Source: pp. 266–271.

**Optimization.** SciPy SLSQP minimizes negative forecast Sharpe subject to weights summing to one and each in [0,1]. Risk-free rate is the FOMC primary credit rate. Alternatives mentioned: ARIMA, Prophet, LSTM, SVM, XGBoost. Source: pp. 267–272.

**Limits/results.** Figures 6.56–6.57 cover base and 6.58–6.59 fine-tuned performance/crisis plots. A pretrained model may contain post–January 1, 2019 data, causing look-ahead. Median paths suppress forecast uncertainty; Sharpe assumes distributional stability and ignores tail risk. Source: pp. 268–270.

### Example 19 — FinBERT Model

**Objective.** Score news with `ProsusAI/finbert`, choose the most volatile among the top ten liquid S&P 500 stocks monthly, and trade aggregated sentiment. Compare pretrained and monthly fine-tuned models. Source: pp. 272–280.

**Model/data.** Each article yields positive/neutral/negative probabilities. Base model analyzes ten days of TiingoNews. Fine-tuning uses 30 days of news and closes; daily returns' strongest 75% positive and strongest 75% negative observations become corresponding labels, with the remainder neutral. Recent articles receive exponentially greater aggregation weight. Source: pp. 273–280.

**Trading.** Rebalance monthly at midnight: if aggregate positive probability exceeds negative, hold 100% long; otherwise short 25%. Base requires no training; fine-tuned model retrains monthly. Random seeds should be fixed for split, initialization, and training reproducibility. Source: pp. 274–280.

**Limits/results.** FinBERT is cheaper/faster and finance-specific versus general GPT-4, but less nuanced. Figures 6.60–6.61 cover base and 6.62–6.63 fine-tuned results. Pretrained cutoff can leak future information; 30 days is a small fine-tuning sample; return-derived article labels conflate news effect with all other daily drivers. Source: pp. 273–280.

## Mathematical Formulas and Quantitative Relationships

### Trend-scanning selection

For lookback $L=20$, regress future closes on $l=0,\ldots,L-1$ for candidate endpoints and select

$$j^*=\arg\max_j |t(\hat\beta_j)|,\qquad y=\operatorname{sign}(t(\hat\beta_{j^*})).$$

$\hat\beta_j$ is the fitted time slope and its t-statistic measures significance; $y\in\{-1,0,1\}$ is trend direction. Exact zero handling and candidate-window range depend on the library. Source: pp. 144–145.

### Wavelet input length

The source solves the relationship

$$\log_2\!\left(\frac{n}{w-1}\right)=d$$

for input length $n$, with Symlet-10 wavelet length $w=20$ and decomposition depth $d=3$, yielding the implemented $n=152$ under the library's sizing convention. The XHTML prose formatting is ambiguous, so this transcription should be checked against code/library boundary rules. Source: p. 171.

### Expected-return trading threshold

$$\hat r_{t+1}=\frac{\hat P_{t+1}}{P_t}-1.$$

Trade when $\hat r_{t+1}>0.005$ and scale by leverage 20. Source: pp. 172–173.

### Dividend yield and proportional allocation

$$DY_i=\frac{DPS_i}{P_i},\qquad w_i=\frac{\widehat{DY}_i}{\sum_j\widehat{DY}_j}.$$

$DPS_i$ is dividend/share, $P_i$ price, and $w_i$ portfolio weight. Negative/zero prediction handling is not specified. Source: pp. 176–177.

### Spread percentage and cost per dollar

$$s=\frac{ask-bid}{bid},\qquad c_d=\frac{\widehat{commission+slippage}}{|Q|P}.$$

The candidate executes when predicted $c_d$ is below the trailing ten-day realized average. Source: pp. 221–224.

### Beta-neutral pair spread diagnostics

For cointegrated prices $A_t,B_t$, estimate $A_t=\alpha+\beta B_t+\epsilon_t$ and treat $\epsilon_t$ as spread. Require Engle–Granger p≤1%, Hurst $H<0.5$, $1$ day $<t_{1/2}<1$ year, and ≥12 mean crossings/year. Source: pp. 201–204.

### PCA residual z-score

$$z_{i,t}=\frac{\epsilon_{i,t}-\bar\epsilon_i}{s_{\epsilon_i}}.$$

Buy candidates with $z_{i,t}<-1.5$ and weight opposite the deviation, anticipating mean reversion. Source: pp. 229–232.

### Futures inverse-volatility allocation

$$w_i=\frac{3}{\hat\sigma_i\sum_j\hat\sigma_j M_i}.$$

$\hat\sigma_i$ is predicted next-week opening volatility and $M_i$ contract multiplier. The numerator 3 is an empirical exposure scale. As printed, this is not the conventional normalized inverse-volatility formula; verify dimensional and gross-exposure behavior. Source: pp. 215–216.

### Chronos portfolio optimization (all 8 MathML nodes)

$$
\max_{\mathbf w}\left(\frac{R_p-R_f}{\sigma_p}\right)
$$

subject to

$$
\sum_i w_i=1,\qquad 0\le w_i\le1.
$$

- $R_p$: portfolio return implied by forecast paths.
- $R_f$: risk-free rate, represented by the FOMC primary credit rate.
- $\sigma_p$: standard deviation of portfolio returns.
- $w_i$: asset weights.

Purpose: maximize forecast risk-adjusted return while remaining fully invested, long-only. Implementation minimizes the negative objective with SLSQP. The eight MathML nodes comprise the objective, two constraints, and four standalone symbol definitions. Source: pp. 267–268.

## Cross-Example Methods and Implementation Patterns

1. **Time-safe labels:** calculate future returns, shift them backward only for training alignment, and discard trailing NaNs; never expose shifted labels at inference time.
2. **Scheduled retraining:** match cadence to signal horizon—daily for regimes/execution, weekly for risk and direction, monthly for fundamentals/sentiment, quarterly for long forecasts.
3. **Per-security state:** encapsulate indicators, histories, consolidators, and models; rebuild on splits and universe changes.
4. **Preprocessing:** test stationarity; standardize before PCA/CNN training; fit transformations only on training data; forward-fill only when economically valid.
5. **Model persistence:** use Object Store/pickle for expensive trained models and diagnostic CSVs; version models and restore state in live mode.
6. **Prediction-to-portfolio mapping:** threshold weak predictions, normalize weights, cap leverage/gross exposure, respect contract multipliers and option assignment.
7. **Evaluation:** compare to an economically relevant benchmark, report OOS performance, inspect crisis periods and parameter neighborhoods, and account for costs and delayed execution. Source: pp. 143–280.

## Figures and Tables Completeness Registry

### Numbered figures

- **6.1–6.3 (pp. 145–148):** trend segments; strategy/benchmark equity; predictions versus observed log BTC price.
- **6.4–6.9 (pp. 149–153):** SPY future-return labels/counts and probability series for raw, stationary, standardized, and PCA factors.
- **6.10–6.17 (pp. 159–164):** SPY volatility regimes, straddle payoff, and performance/monthly/crisis sheets for HMM Algorithms 1–3.
- **6.18–6.19 (p. 174):** FX SVM-wavelet performance and sensitivity.
- **6.20–6.21 (p. 180):** dividend model performance and universe/lookback sensitivity.
- **6.22–6.23 (p. 183):** split-event strategy performance and hold/lookback sensitivity.
- **6.24–6.29 (pp. 188–190):** performance/crisis/sensitivity pairs for fixed stop, predicted stop, and put hedge.
- **6.30–6.34 (pp. 199–207):** PCA coordinates, OPTICS clusters, pair-filter attrition, and candidate prices/spreads.
- **6.35–6.36 (p. 211):** PCA/LambdaRank performance and component/universe sensitivity.
- **6.37–6.38 (pp. 217–218):** futures inverse-volatility performance and lookback sensitivity.
- **6.39–6.42 (pp. 224–228):** cost learning, savings distributions, delay durations, and time-limit fills.
- **6.43–6.44 (p. 232):** PCA statistical-arbitrage performance and component/lookback sensitivity.
- **6.45 (p. 236):** three-branch temporal CNN architecture.
- **6.46–6.47 (p. 239):** temporal CNN performance and sample/universe sensitivity.
- **6.48–6.49 (p. 245):** GNB performance and feature/universe sensitivity.
- **6.50–6.51 (p. 252):** GPT-4 sentiment performance and monthly returns.
- **6.52 (p. 256):** head-and-shoulders geometry and neckline entry.
- **6.53–6.55 (p. 261):** CNN pattern strategy results and synthetic positive sample.
- **6.56–6.59 (pp. 268–270):** Chronos base/fine-tuned performance and crisis sheets.
- **6.60–6.63 (p. 275):** FinBERT base/fine-tuned performance and crisis sheets.

### Unnumbered figure elements

The source contains 58 `<figure>` elements used as tables: each example's metadata, model, portfolio, parameter, and result blocks, including IDs `ch6_unnum1`–`ch6_unnum26`, `ch6_unnum29`–`ch6_unnum31`, and `ch1_unnum1`–`ch1_unnum27` (the numbering gap/duplicate prefix is in the EPUB). Their decision-useful contents are integrated into Examples 1–19 above. Eleven additional image-only pair diagnostics—`newfig6_1`, `newfig6_3`–`newfig6_14`—show the detected candidates' two prices and normalized spread and are grouped under Example 9/Figure 6.34. Together with the 63 numbered figures, these account for all 132 `<figure>` elements. Source: pp. 143–280.

## Applications

- Regime switching across equities, bonds, and volatility options.
- Cross-sectional dividend, fundamental-rank, and statistical-arbitrage portfolios.
- Futures risk balancing and forex forecasting.
- Event trading around stock splits and chart patterns.
- Dynamic stops and option-based downside protection.
- Cost-aware order timing.
- News sentiment through hosted and local language models.
- Foundation-model forecasting with constrained portfolio optimization. Source: pp. 143–280.

## Assumptions, Limitations, and Edge Cases

- Accuracy can be barely above chance while trading returns improve, and high synthetic accuracy may fail in real data.
- Random-factor preprocessing demonstrations are not evidence of alpha.
- Financial series are nonstationary; model relationships, clusters, cointegration, and regimes decay.
- PCA components change with universe and sample; their economic interpretation is approximate.
- Forward labels, adjusted prices, news release times, and pretrained-model cutoff dates are major leakage surfaces.
- Options require liquidity, premium, expiry, assignment/exercise, and margin modeling; a predicted regime does not guarantee profitable realized volatility.
- Futures require mapping/rolling and multiplier-aware, margin-safe quantities.
- Sharpe optimization assumes stable moments and can underweight tail risk.
- News labels derived from same-day returns are noisy causal proxies.
- Fine-tuning on 30 days or model fitting on sparse dividends/splits may be statistically weak.
- Sensitivity plots repeatedly show narrow or unstable optima; parameter choices should favor plateaus.
- Delaying execution to save spread can add adverse price movement and opportunity cost. Source: pp. 143–280.

## Common Mistakes and Warnings

- Fitting scalers/PCA on the complete dataset before splitting.
- Treating shifted future labels as available trading data.
- Optimizing classification accuracy without evaluating payoff distribution.
- Assuming a pretrained HuggingFace model is safe for an earlier backtest.
- Ignoring splits when maintaining price-derived features.
- Letting universe size expand feature dimensions beyond sample capacity.
- Treating a backtest's slippage proxy as independent proof of execution savings.
- Using a single best sensitivity cell rather than checking neighboring values.
- Equating a low-volatility state with guaranteed bullish returns.
- Applying synthetic-pattern accuracy directly to live market confidence.
- Omitting random seeds, model/version metadata, or persisted live state. Source: pp. 143–280.

## Key Takeaways

1. A useful trading ML system is the whole pipeline—data timing, feature/label construction, training, allocation, execution, persistence, and monitoring—not merely a fitted estimator.
2. Match the model to data: regularized linear models for correlated interpretable features, trees/rankers for nonlinear tables, CNNs for local temporal shapes, HMMs for hidden regimes, and pretrained models where cutoff and cost are controlled.
3. OOS evaluation, sensitivity stability, and economic benchmarks matter more than in-sample fit.
4. Prediction confidence must be translated into exposure under explicit leverage, liquidity, margin, and cost constraints.
5. Foundation and language models reduce feature engineering but add version, leakage, compute, and reproducibility risks.
6. Many examples are educational prototypes; weak OOS accuracy, synthetic training, short samples, and unstable parameters should prevent automatic production use. Source: pp. 143–280.

## Glossary

| Term | Definition | Source |
|---|---|---|
| ADF test | Test for a unit root/nonstationarity. | p. 152 |
| Chronos | Pretrained probabilistic time-series forecasting model. | pp. 265–272 |
| Cointegration | Stable long-run relation among individually nonstationary series. | pp. 201–204 |
| CNN | Neural network using sliding convolution filters to extract local patterns. | pp. 234–237 |
| FinBERT | BERT variant specialized for financial sentiment. | pp. 272–280 |
| GNB | Gaussian Naive Bayes classifier assuming conditionally independent Gaussian features. | pp. 242–250 |
| Half-life | Expected time for a spread deviation to decay halfway toward its mean. | pp. 203–204 |
| Hurst exponent | Long-memory statistic; below .5 indicates mean-reverting tendency. | pp. 202–203 |
| LASSO | Regression with coefficient penalty that can set weak features to zero. | pp. 185–187 |
| LambdaRank | Ranking objective used to learn relative item ordering. | pp. 208–213 |
| Markov regime | Latent state whose transition depends on the prior state. | pp. 158–162 |
| OPTICS | Density-based clustering that can identify clusters with varying density. | pp. 199–201 |
| PCA | Orthogonal transformation concentrating variance into principal components. | pp. 151–153, 197–213 |
| PSR | Not used directly here; performance instead relies mainly on Sharpe and sensitivity plots. | chapter-wide |
| Ridge regression | L2-regularized regression that shrinks correlated coefficients. | pp. 214–219 |
| Straddle | Same-strike/expiry call-plus-put combination. | pp. 160–161 |
| SVR | Support-vector regression, including nonlinear kernel relationships. | pp. 170–175 |
| Wavelet decomposition | Multiscale breakdown into approximation/detail coefficients. | pp. 170–175 |

## Connections to Other Chapters

- Chapter 2 supplies the research/backtest, parameter-sensitivity, regime, universe, indicator, and margin foundations applied here.
- Earlier ML theory is operationalized through these 19 end-to-end examples.
- QuantConnect/AWS deployment concepts are anticipated by Object Store persistence, scheduled training, model serialization, and hosted-model integration. Source: pp. 143–280.

## Completeness Audit

- **Chapter span read:** print pages 143–280, full `c006.xhtml`.
- **Examples:** 19/19 represented with objective, data/universe, features/target, model, training/rebalance design, trading rule, parameters/results where supplied, limitations, and implementation notes.
- **MathML:** 8/8 nodes converted; they form one Chronos Sharpe objective, two constraints, and four symbol definitions.
- **Numbered figures:** 63/63, Figures 6.1–6.63, represented in the registry and example narratives.
- **Figure elements:** 132/132 accounted for: 63 numbered figures, 58 table figures, 11 unnumbered pair diagnostics.
- **Tables:** all 58 table-wrapped figures accounted for through the table-ID registry and their contents incorporated by example.
- **Headings:** all Example 1–19 Summary, Motivation, Model, Trading Universe, Portfolio Construction, Trading Logic, Tearsheet, and Implementation Insights sections present where the source supplies them; nested Algorithm 1–3 and Trading subsections are incorporated into Examples 4 and 15.

## Extraction Issues

- Example 2's metadata calls the classifier a “multiclass random forest,” while implementation uses LightGBM; both are preserved.
- Example 5's wavelet length equation is typographically ambiguous in extracted prose; the implemented result `len(data)=152` is authoritative for the example.
- Example 7 alternates between “one week” and the optimized/default three-day holding period.
- Example 11 prints an unconventional inverse-volatility weighting expression; it should be verified dimensionally before reuse.
- The EPUB reuses table-ID prefixes (`ch6_unnum*`, then `ch1_unnum*`) and omits some sequential IDs; this is source structure, not an extraction omission.
- Several tearsheets provide qualitative sensitivity statements but no machine-readable full metric tables; the extraction does not infer missing returns, drawdowns, or Sharpe values from pixels.
- Pretrained Chronos and FinBERT training cutoffs are not documented, so the chapter explicitly warns that tests beginning January 1, 2019 may contain look-ahead bias.
