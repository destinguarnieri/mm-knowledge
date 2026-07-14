# Neutral Classification of Chapters 4–6

## Scope and classification rules

This classification uses only the supplied extracts for Chapters 4–6. “Textbook claim” means the extracts state or demonstrate it. “Classifier inference” means a proposed interpretation, extension, baseline, or validation standard supplied by this classification.

Labels are non-exclusive:

- **Foundational knowledge (FK):** durable concepts needed to reason correctly.
- **Transferable research method (TRM):** reusable research or evaluation procedure.
- **Concrete research direction (CRD):** a testable market hypothesis with a plausible experiment.
- **Strategic capability (SC):** reusable system capability enabling multiple research programs.
- **Frontier/high-complexity direction (FHC):** potentially valuable but unusually data-, compute-, integration-, or validation-intensive.
- **Vendor/platform-specific (VPS):** depends materially on a named API, library, model, data vendor, or platform mechanism.
- **Claim requiring independent validation (CIV):** numerical, causal, generalization, or production-readiness claim not established by the extract alone.

## Chapter 4 — dataset preparation

### Foundational knowledge

**Textbook claims.** Dataset integrity constrains downstream performance; EDA reveals distributions, anomalies, and assumptions; missing values and outliers can bias results but extreme observations may be genuine market events; scaling choice depends on the model; stationarity concerns stability of mean, variance, and autocorrelation; cointegration concerns a stationary linear combination of nonstationary series; feature selection and PCA can reduce redundancy and overfit; train, validation, and test sets serve different purposes.

**Classifier inference.** These are cross-asset foundations for equities, ETFs, rates, FX, futures, commodities, options-derived series, crypto, credit, and mixed macro/alternative datasets. They should be treated as controls on inference, not mechanical recipes.

### Transferable research methods

- **Data audit:** provenance, timestamp semantics, missingness mechanism, duplicates, corporate actions/rolls, anomalous events, and availability at decision time. The extract explicitly covers reliable sourcing, missingness, errors, and anomalies; point-in-time and market-mechanics checks are classifier inferences.
- **Missing-data experiment:** compare deletion, mean/median/mode, KNN, and MICE; assess the imputed distribution and downstream effect. CIV applies whenever an imputation is assumed harmless.
- **Outlier experiment:** separate bad ticks/errors from real tail events; compare removal, transform, and capping. CIV applies to fixed z-score or IQR thresholds in heavy-tailed, heteroskedastic markets.
- **Feature transformation:** rolling features, categorical encoding, interactions, normalization, and standardization, fitted on training data only. Leakage-safe fitting is a classifier inference consistent with the extracts’ warnings.
- **Stationarity ladder:** raw, log, detrended, ordinary-differenced, and fractionally differentiated representations; compare both stationarity and retained forecasting value. ADF p-values and the demonstrated fractional-differencing cutoff are CIV under repeated testing and structural breaks.
- **Relative-value screening:** Engle–Granger plus spread diagnostics. Cointegration is CRD-enabling, not itself evidence of a profitable trade.
- **Feature-selection tournament:** correlation pruning, tree importance, RFE/SelectFromModel, LASSO-like sparsity, and PCA; compare stability across time and folds, not merely one fitted importance vector.
- **Validation:** chronological holdouts and rolling/expanding walk-forward tests for temporal markets. The extract explains ordinary split and k-fold mechanics; the preference for time-respecting validation is classifier inference.

### Strategic capabilities

Point-in-time dataset assembly; transformation pipelines fitted without leakage; data-quality reporting; feature lineage; chronological split generation; imputation/outlier sensitivity; stationarity and cointegration diagnostics; feature-stability reporting; and reproducible dataset snapshots. Sweetviz is VPS; pandas and scikit-learn examples are implementation choices rather than conceptual requirements.

## Chapter 5 — model-family classification

All major families receive a fair reading below. “Applicable markets” is broad unless the target or data form narrows it.

| Family | Labels | Textbook claim | Classifier inference and fair-use reading |
|---|---|---|---|
| Linear regression | FK, TRM, CRD | Interpretable continuous prediction; sensitive to misspecification/outliers. | Essential baseline for returns, prices, rates, vol, costs, exposures, and event response across liquid markets. |
| Polynomial regression | FK, CRD | Captures nonlinear curvature but can overfit as degree grows. | Use only against linear/spline/tree baselines with nested tuning. |
| LASSO | TRM, CRD, SC | L1 shrinkage can set coefficients to zero. | Useful for sparse factor/event/risk models; selection stability under correlated predictors is CIV. |
| Ridge | TRM, CRD, SC | L2 shrinkage stabilizes correlated predictors without exact selection. | Strong baseline for collinear cross-asset risk and volatility features. |
| Markov-switching dynamic regression | CRD, SC, FHC | Latent regimes can have different regression/variance parameters. | Suitable for volatility, liquidity, correlation, inflation, or trend regimes; economic interpretation of states is CIV. |
| Decision-tree regression | CRD, SC | Nonlinear, interpretable threshold rules; prone to overfit. | Useful for tabular fundamentals, events, risk, and costs; compare to linear and ensemble baselines. |
| SVR + wavelets | CRD, FHC | Kernels fit nonlinear relationships; wavelets represent multiscale nonstationary signals. | Plausible for FX, rates, commodities, crypto, or intraday signals; decomposition choices and neighbor-parameter optima require strong stability tests. |
| Random forest / LightGBM multiclass | CRD, SC | Ensembles capture nonlinear classification and expose importance. | General tabular classifier for direction, regime, distress, or action; the extract’s LightGBM `rf` implementation is VPS and must not be conflated with a generic random forest. |
| Logistic regression | FK, TRM, CRD | Probabilistic classifier with linear log-odds; ROC/AUC, precision, recall, and F1 expose different errors. | Mandatory calibrated baseline for directional/event/default labels; threshold by utility, not accuracy alone. |
| Hidden Markov model | CRD, SC, FHC | Observations are emitted by latent states with probabilistic transitions. | Reusable regime capability across asset classes; state number, persistence, and mapping to economics require independent validation. |
| Gaussian Naive Bayes | FK, TRM, CRD | Fast probabilistic classifier assuming conditional independence and Gaussian class likelihoods. | Useful cheap baseline; financial return features commonly challenge both assumptions. |
| CNN / CNN-LSTM | CRD, SC, FHC | Learns local and sequential structure but needs data, compute, tuning, and overfit controls. | Candidate for multivariate bars, order flow, volatility surfaces, or patterns; compare to simple lag models and trees on identical information. |
| LGBRanker / LambdaRank | CRD, SC, FHC | Learns within-group orderings and optimizes ranking quality such as NDCG. | Natural cross-sectional security/contract ranking capability; group definition and portfolio utility matter more than score fit alone. |
| OPTICS | TRM, CRD, SC | Density clustering discovers varying-density clusters and noise without fixed cluster count. | Useful for regime, peer, anomaly, and pair-candidate discovery; cluster stability and economic meaning are CIV. |
| GPT-family language model | CRD, SC, FHC, VPS, CIV | Can summarize and classify unstructured financial language; example uses OpenAI structured JSON sentiment. | Research direction spans news, filings, transcripts, compliance, and event extraction; model/version, prompt, timestamps, cost, and reproducibility are first-class experimental variables. |
| Chronos | CRD, SC, FHC, VPS, CIV | Pretrained tokenized probabilistic time-series forecasting with sampled futures/quantiles. | Compare against naive, statistical, and supervised forecasting across prices, returns, volatility, spreads, and demand-like financial series; cutoff contamination must be ruled out. |
| FinBERT | CRD, SC, FHC, VPS, CIV | Finance-specialized BERT sentiment model for news/reports/social text. | Strong domain baseline for text signals, but probability calibration, cutoff, label quality, and incremental value over lexicons/general LLMs require testing. |

Across families, model choice, preprocessing, held-out tuning, task-appropriate metrics, learning curves, and inspection of errors are FK/TRM. OpenAI, Amazon Chronos, FinBERT/Hugging Face, LightGBM, sklearn, statsmodels, Keras, PyWavelets, and associated APIs are VPS. Synthetic example scores and qualitative finance applicability are CIV when extrapolated to real markets.

## Chapter 6 — 19 applied research directions

Each entry separates the extract’s proposal/results from the classifier’s recommended research framing.

### 1. Trend scanning

**Labels:** CRD, TRM, VPS (MLFinLab), CIV. **Textbook:** label BTCUSD down/flat/up by the slope with greatest absolute t-statistic over candidate horizons; daily long BTC only in uptrends; 51.2% direction accuracy, yet shown equity beats buy-and-hold. **Hypothesis/question (inference):** does adaptive trend-horizon selection improve risk-adjusted exposure versus fixed-horizon trend rules? **Markets:** crypto, equity indices, FX, futures, rates, commodities, liquid single assets. **Data:** point-in-time OHLC/returns, trading calendar, costs/funding where relevant. **Methods:** trend scanning, linear slopes/t-stats, possibly regularized multiclass models. **Baselines:** cash/buy-and-hold, sign of 1-day return, moving-average crossover, fixed 20/60/120-day momentum, volatility-scaled trend. **Evaluation:** walk-forward labels with decision-time-safe endpoints; turnover/costs; payoff by class; drawdown and regime slices; horizon sensitivity. **Failure modes:** retrospective endpoint leakage, repeated horizon selection, churn, crash reversals, benchmark mismatch. **Continue if:** net OOS improvement is stable across assets, horizons, and adjacent parameters and comes from repeatable payoff asymmetry rather than one avoided episode.

### 2. Preprocessing for regime/direction classification

**Labels:** TRM, CRD, CIV. **Textbook:** raw, stationary, standardized, and PCA-transformed random factors classify next-week SPY sign; raw accuracy is highest, and random factors make this a pipeline demonstration. **Question:** which preprocessing preserves genuine predictive information under nonstationarity? **Markets:** all time-series and cross-sectional markets. **Data:** real point-in-time candidate features plus forward labels. **Methods:** ADF, fractional differencing, scaling, PCA, LightGBM. **Baselines:** majority class, raw features, logistic/ridge, shuffled-label control. **Evaluation:** transformations fit within rolling training windows; compare discrimination, calibration, trading utility, and feature stability; multiple seeds. **Failure modes:** leakage, PCA instability, arbitrary stationarity thresholds, spurious accuracy, class drift. **Continue if:** a transformation improves net OOS utility consistently across folds without relying on random or post hoc factors.

### 3. Momentum-versus-reversal strategy selection

**Labels:** CRD, SC, FHC, CIV. **Textbook:** a small neural network uses RSI, normalized ATR, return volatility, and VIX to choose SPY or TLT; OOS accuracy 52.77%, below the cited SPY up-day rate. **Hypothesis:** observable volatility/liquidity states predict whether momentum or reversal has superior next-period payoff. **Markets:** equities, indices, FX, futures, crypto, rates; cross-asset defensive substitutes. **Data:** returns, volatility/liquidity features, point-in-time factor returns, candidate strategy P&Ls. **Methods:** logistic regression, trees/boosting, HMM, calibrated neural net. **Baselines:** always momentum, always reversal, equal blend, volatility rule, simple logistic model. **Evaluation:** label the *relative net payoff* of the two strategies; nested walk-forward tuning; switching costs; probability-conditioned allocation. **Failure modes:** noisy proxy labels, asset-substitution effects, class imbalance, overtrading, noncausal factor publication. **Continue if:** classifier adds stable net value over the best static/blended baseline across assets and regimes with calibrated confidence.

### 4. Latent volatility regimes and allocation/options

**Labels:** CRD, SC, FHC, CIV. **Textbook:** two-state Markov switching on trailing SPY returns drives SPY/TLT allocation or long/short SPY/SPX straddles; options add expiry, spread, margin, assignment, and path risk. **Hypothesis:** latent variance-state probabilities forecast relative returns or realized-versus-implied volatility sufficiently to alter exposure. **Markets:** equity/index, rates, FX, commodities, crypto; options where liquid. **Data:** returns, realized and implied vol, option chains/Greeks/quotes, rates/dividends, fills. **Methods:** Markov switching, HMM, change-point models, volatility forecasts. **Baselines:** realized-vol thresholds, VIX/implied-vol rules, GARCH, static allocation, unconditional long/short straddle. **Evaluation:** expanding walk-forward estimation, state-label alignment, probability rather than hard-state rules, full option lifecycle and tail stress. **Failure modes:** label switching, unstable transitions, state/economic mismatch, vol-risk premium overwhelming direction, short-gamma blowups, poor fills. **Continue if:** state probabilities forecast economically relevant outcomes and improve net tail-aware results across multiple underlyings and crises.

### 5. Wavelet-SVR forecasting

**Labels:** CRD, FHC, CIV. **Textbook:** decompose four FX pairs with Symlet-10, forecast coefficients using grid-searched SVR, reconstruct next close, and lever signals above a threshold; neighboring lookback results are unstable. **Hypothesis:** multiscale decomposition improves forecastability beyond raw-lag models. **Markets:** FX, rates, commodities, crypto, index futures, possibly volatility. **Data:** clean evenly sampled prices/returns, spreads, financing. **Methods:** wavelets + SVR; alternative wavelets/depths. **Baselines:** random walk, AR/ARIMA, linear/ridge lags, raw SVR, moving average, no denoising. **Evaluation:** nested rolling tuning, directional and level errors, net P&L, parameter surfaces, cross-pair transfer. **Failure modes:** boundary artifacts, noncausal filtering, level-forecast illusion, leverage amplification, multiple searches, regime decay. **Continue if:** gains survive causal reconstruction, costs, adjacent parameters, and multiple pairs versus raw SVR and naive forecasts.

### 6. Dividend-yield forecasting and selection

**Labels:** CRD, SC, CIV. **Textbook:** a decision tree predicts dividend yield from five fundamentals for large QQQ constituents and weights positive forecasts; shown Sharpe is positive and universe-sensitive. **Hypothesis:** point-in-time fundamentals predict future sustainable dividend yield/total return beyond current yield. **Markets:** dividend-paying equities, REITs, possibly preferreds. **Data:** point-in-time fundamentals, announced/paid dividends, prices, revisions, corporate actions, delistings. **Methods:** trees/boosting, linear/ridge, survival/cut models, ranking. **Baselines:** current yield, dividend-growth/value screens, equal weight, dividend index. **Evaluation:** vintage-safe walk-forward universe, total return after taxes/costs, cuts and yield-trap subgroups, sector-neutral variants. **Failure modes:** restatements, sparse labels, survivorship, price-driven high yield, concentration, tax effects. **Continue if:** forecasts improve dividend sustainability and net total return over simple yield/value rules across sectors and cycles.

### 7. Stock-split event response

**Labels:** CRD, CIV. **Textbook:** linear regression uses split factor and sector return to predict three-day technology-stock post-announcement returns; displayed combinations exceed 0.7 Sharpe, with a prose/configuration holding-period inconsistency. **Hypothesis:** split terms and pre-event context predict post-announcement abnormal returns. **Markets:** equities; analogous corporate actions elsewhere. **Data:** exact announcement/effective timestamps, split terms, adjusted/unadjusted prices, sector/market returns, liquidity/news. **Methods:** linear/ridge, event-study regression, trees, treatment-effect analysis. **Baselines:** no trade, equal-weight all splits, market/sector-adjusted event drift, sign-free event basket. **Evaluation:** event-time OOS split, sparse-event uncertainty, abnormal returns, transaction costs, announcement versus effective-date separation. **Failure modes:** timestamp leakage, small samples, selection bias, overlapping news, corporate-action adjustment errors. **Continue if:** abnormal net returns persist across eras, sectors, and unseen events with confidence intervals robust to clustering.

### 8. Predicted downside and hedge selection

**Labels:** CRD, SC, FHC, CIV. **Textbook:** LASSO predicts weekly low return from VIX, ATR, and volatility; compare fixed stop, predicted stop, and put hedge on KO. **Hypothesis:** conditional downside-distribution forecasts improve risk-adjusted outcomes versus fixed risk rules, and can choose between stops and options. **Markets:** equities, ETFs, futures, FX, crypto; options overlays where available. **Data:** OHLC paths, volatility/implied vol, gap data, option quotes/Greeks, fills. **Methods:** LASSO/ridge, quantile regression, conformal intervals, tree quantiles. **Baselines:** no hedge, fixed-percent/ATR/trailing stops, constant protective put, volatility targeting. **Evaluation:** walk-forward tail calibration, expected shortfall/drawdown, gap/slippage modeling, option premium and exercise, matched exposure. **Failure modes:** predicting extrema is noisy, stop execution gaps, hedge drag, volatility-surface leakage, incomparable payoff profiles. **Continue if:** tail losses improve after all costs without unacceptable return drag across assets and stress periods, with calibrated downside coverage.

### 9. Pair discovery pipeline

**Labels:** TRM, CRD, SC, FHC, CIV. **Textbook:** standardize returns, reduce 927 equities to three PCs, cluster with OPTICS, then filter pairs by bidirectional Engle–Granger, Hurst, half-life, and crossings; 30 remain, but no traded portfolio is tested. **Hypothesis:** economically similar, statistically stable pairs yield net mean-reversion opportunities. **Markets:** equities/ETFs, futures curves, rates, FX, commodities, crypto, related options/implied-vol series. **Data:** point-in-time universes, prices, borrow/funding, corporate actions/rolls, quotes. **Methods:** PCA/OPTICS, cointegration, sparse/VECM or dynamic hedge ratios. **Baselines:** sector/industry peers, correlation screen, random within-cluster pairs, distance pairs. **Evaluation:** universe formed historically; discovery/train/trade separation; multiple-testing correction; rolling re-estimation; actual entry/exit portfolio with borrow/costs/capacity. **Failure modes:** survivorship, p-hacking, structural breaks, hedge-ratio error, crowding, short constraints. **Continue if:** candidate formation predicts stable OOS spreads and a diversified net portfolio beats simple peer-pair baselines across formation dates.

### 10. Fundamental cross-sectional ranking

**Labels:** CRD, SC, FHC, CIV. **Textbook:** standardize up to 100 factors, retain five PCs, and use LambdaRank to rank 22-day forward equity returns; results are highly sensitive to PC count/universe. **Hypothesis:** nonlinear ranking of point-in-time fundamentals improves top-decile returns versus linear factor composites. **Markets:** equities, credit issuers, ETFs, futures/crypto where fundamental-like features exist. **Data:** vintage-safe fundamentals, classifications, prices, liquidity, delistings. **Methods:** PCA + LambdaRank/LightGBM; linear ranker, ridge, trees. **Baselines:** equal weight, value/quality/momentum composites, linear regression/ranking, no PCA. **Evaluation:** monthly purged walk-forward groups, IC/NDCG and portfolio spread, sector/beta neutrality, turnover/cost/capacity, parameter plateaus. **Failure modes:** restatement/look-ahead, PCA instability, group leakage, universe bias, nonlinear overfit. **Continue if:** rank IC and net top-minus-bottom or long-only utility remain stable across eras, universes, component counts, and neutralizations.

### 11. Forecasted-volatility futures allocation

**Labels:** CRD, SC, FHC, CIV. **Textbook:** ridge predicts next-week opening volatility from realized volatility, ATR, and open interest across index, energy, grain, and VIX futures; an unconventional multiplier-aware formula with empirical factor 3 allocates exposure. **Hypothesis:** predicted rather than trailing volatility improves risk balance and drawdown control. **Markets:** futures across asset classes; transferable to forwards/spot with leverage. **Data:** continuous and contract-level prices, rolls, open interest, multipliers, margins, spreads. **Methods:** ridge, HAR/GARCH, tree volatility forecasts, covariance-aware risk parity. **Baselines:** equal risk, inverse trailing vol, equal notional, covariance risk parity. **Evaluation:** contract-correct walk-forward simulation, roll and margin, forecast loss plus portfolio risk, dimensional audit of weights, stress correlations. **Failure modes:** bad normalization, roll leakage, covariance omission, VIX asymmetry, margin calls, volatility spikes. **Continue if:** a dimensionally sound rule lowers realized risk/drawdown or improves net utility across contracts and crises versus inverse trailing vol.

### 12. Learned execution timing

**Labels:** CRD, SC, FHC, CIV. **Textbook:** a decision tree delays BTCUSD liquidation until predicted cost per dollar is below a trailing average; reported simulated savings are $36,260.20, but asynchronous fills add price risk and the slippage proxy may make savings circular. **Hypothesis:** short-horizon liquidity features can choose execution time to reduce implementation shortfall without adding larger timing loss. **Markets:** crypto, equities, futures, FX, options—any venue with sufficiently rich quotes/fills. **Data:** event-time order book, trades, own orders/fills, fees/rebates, latency, parent-order constraints. **Methods:** trees/boosting, survival/hazard models, contextual bandits or RL only after supervised baselines. **Baselines:** immediate market, fixed schedule, limit with timeout, TWAP/VWAP, simple spread threshold. **Evaluation:** common arrival-price shortfall, counterfactual or randomized replay, fill probability, adverse selection, opportunity cost, capacity and latency. **Failure modes:** simulator circularity, fill-selection bias, nonstationary microstructure, unfilled orders, market impact, leakage from realized cost. **Continue if:** out-of-sample or randomized live-like evidence lowers total shortfall—not just quoted spread—across sizes, regimes, and venues.

### 13. PCA residual statistical arbitrage

**Labels:** CRD, SC, FHC, CIV. **Textbook:** PCA factors explain standardized log returns; buy stocks with residual z-score below −1.5; displayed parameter combinations are profitable with a peak near three PCs/126 days. **Hypothesis:** extreme idiosyncratic residuals mean-revert after controlling for common factors. **Markets:** equities, ETFs, futures, rates, FX, crypto baskets. **Data:** point-in-time constituents, adjusted prices, borrow/costs, factor exposures. **Methods:** PCA/OLS, robust or rolling PCA, sparse factor models, Kalman residuals. **Baselines:** market/sector residual reversal, simple short-term reversal, equal-weight, random residual tails. **Evaluation:** rolling formation/trading separation, long-short and long-only variants, neutrality, decay curve, turnover/cost/borrow, crisis/crowding tests. **Failure modes:** PCA rotation, residuals containing news, momentum crashes, survivor/universe bias, one-sided exposure. **Continue if:** residual tails show repeatable OOS mean reversion and diversified net alpha beyond ordinary reversal and sector neutralization.

### 14. Temporal CNN direction classification

**Labels:** CRD, SC, FHC, CIV. **Textbook:** parallel Conv1D branches classify weekly up/down/stationary from 15 days of OHLCV for three large QQQ names; most tested combinations lose money despite more-sample improvement. **Hypothesis:** multiscale local bar patterns add direction information beyond engineered lags. **Markets:** liquid equities, ETFs, futures, FX, crypto; intraday variants if microstructure is modeled. **Data:** point-in-time OHLCV, adjustments/rolls, costs. **Methods:** temporal CNN, CNN-LSTM/TCN; calibrated class probabilities. **Baselines:** majority class, logistic/ridge on lagged returns, tree boosting, momentum/reversal, 1-D single-branch CNN. **Evaluation:** purged walk-forward by asset/time, probability calibration, class/payoff utility, ablations, seeds, compute-normalized comparison. **Failure modes:** tiny universe, overlapping-label leakage, scale artifacts, regime decay, architecture search overfit, low interpretability. **Continue if:** multiple seeds and unseen assets show stable net improvement and ablations identify incremental temporal information.

### 15. Gaussian direction classifier

**Labels:** CRD, TRM, SC, CIV. **Textbook:** GNB uses four days of intraday and overnight return-sign features to classify 22-session technology-stock return sign; displayed combinations are profitable, while Gaussian/independence assumptions may fail. **Hypothesis:** simple recent return decomposition contains robust cross-sectional direction information. **Markets:** equities and other sessionized assets; continuous markets with analogous interval decomposition. **Data:** adjusted open/close histories, exact session calendars, universe history. **Methods:** GNB; optional calibrated or nonparametric naive Bayes. **Baselines:** prior/majority, momentum, logistic regression, empirical frequency table, tree. **Evaluation:** weekly point-in-time walk-forward, per-class calibration, asset-clustered uncertainty, feature/universe sensitivity, costs. **Failure modes:** overlapping long-horizon labels, dependence/non-Gaussianity, universe expansion increasing noise, splits, class imbalance. **Continue if:** the cheap model adds stable net value over simple momentum/logistic baselines across sectors and periods with calibrated probabilities.

### 16. General-LLM news aggregation

**Labels:** CRD, SC, FHC, VPS (GPT-4, Tiingo), CIV. **Textbook:** hourly TSLA news is deduplicated and summarized to −10…+10 sentiment; changes drive long/short exposure; Sharpe 1.695 over a very short sample, with nondeterminism, cost, latency, timestamp, and preprocessing risks. **Hypothesis:** event-time LLM aggregation captures incremental news impact beyond price and lexical sentiment. **Markets:** equities, credit, rates, FX, commodities, crypto, prediction/event markets. **Data:** licensed timestamped text, revisions, entity links, prices/quotes, model/prompt/version logs. **Methods:** structured LLM extraction/sentiment, embeddings, event taxonomy, retrieval. **Baselines:** no news, bag-of-words/lexicon, FinBERT, headline-count surprise, price-only model. **Evaluation:** strict publish-time replay, frozen prompts/models, cross-asset/date holdouts, deterministic schema validation, cost/latency, event studies and portfolio tests. **Failure modes:** contamination, hallucination, duplicated/stale news, prompt drift, single-name selection, causal confounding. **Continue if:** frozen OOS evaluation shows incremental net value over FinBERT/lexicons/price controls across many events and instruments.

### 17. Synthetic pattern CNN

**Labels:** CRD, FHC, CIV. **Textbook:** a CNN trained on 100,000 synthetic head-and-shoulders patterns and 100,000 random walks achieves 99.9% synthetic test accuracy and shorts USDCAD on detections; synthetic accuracy does not establish real generalization. **Hypothesis:** shape models trained with realistic simulation can identify price configurations with conditional forward returns. **Markets:** FX, equities, futures, crypto, rates. **Data:** real historical windows, independently labeled/weakly labeled patterns, synthetic generator calibrated to real noise, costs. **Methods:** CNN, template/dynamic-time-warp matching, shapelets, self-supervised embeddings. **Baselines:** random signals with matched frequency, rule-based neckline pattern, simple return/volatility features, template correlation. **Evaluation:** synthetic-to-real domain split, hand-audited detections, event-time returns, frequency-matched baselines, multiple pairs/assets, augmentation ablations. **Failure modes:** domain gap, arbitrary pattern definition, multiple lookback searches, sparse trades, holding-period confounding. **Continue if:** real-data precision and net conditional returns exceed frequency-matched rules across unseen markets, not merely synthetic accuracy.

### 18. Pretrained probabilistic forecasting and allocation

**Labels:** CRD, SC, FHC, VPS (Amazon Chronos), CIV. **Textbook:** `chronos-t5-tiny` forecasts 63 days for five liquid S&P constituents; median paths feed long-only forecast-Sharpe optimization; base and monthly fine-tuned variants risk pretrained cutoff leakage and suppressed uncertainty. **Hypothesis:** pretrained probabilistic forecasters improve return/distribution forecasts and portfolio decisions with limited local training. **Markets:** equities, ETFs, futures, FX, crypto, rates, volatility/spreads. **Data:** cutoff-safe histories, covariates if supported, full forecast samples, costs and risk-free series. **Methods:** Chronos base/fine-tuned; distribution-aware optimization. **Baselines:** last value/drift, historical mean, ARIMA/ETS, Prophet, ridge/XGBoost/LSTM, equal weight and minimum variance. **Evaluation:** post-cutoff or uncontaminated assets, rolling-origin probabilistic scores and portfolio utility, quantile calibration, tail scenarios, optimization error decomposition. **Failure modes:** pretraining leakage, price-level forecasting without return skill, unstable moments, optimizer concentration, ignored tails/costs. **Continue if:** cutoff-clean forecasts improve proper scoring rules and conservative net portfolio utility over naive/statistical models across markets and origins.

### 19. FinBERT sentiment trading

**Labels:** CRD, SC, FHC, VPS (FinBERT, Tiingo), CIV. **Textbook:** FinBERT probabilities are recency-weighted; the most volatile of ten liquid S&P stocks is traded long 100% or short 25%; base and 30-day fine-tuned variants face cutoff and noisy return-derived-label risks. **Hypothesis:** domain sentiment probabilities predict event-time abnormal returns, and carefully labeled fine-tuning adds value. **Markets:** equities, credit, sector ETFs, possibly commodities/rates where text is financial. **Data:** exact-time news, entity/event labels, returns and controls, frozen model cutoff/version. **Methods:** base/fine-tuned FinBERT, calibration, multitask/event classification. **Baselines:** lexicon, logistic bag-of-words, general LLM, price momentum, base versus fine-tuned model. **Evaluation:** event-time and portfolio OOS tests, cutoff-safe periods, probability calibration, cross-company/sector splits, label-window sensitivity, costs. **Failure modes:** same-day labels conflate drivers, tiny fine-tune set, leakage, volatility selection bias, sentiment aggregation hiding disagreement. **Continue if:** incremental, calibrated abnormal-return signal persists across companies/events and beats text and price baselines after costs.

## Cross-cutting strategic capabilities suggested by the extracts

These are classifier inferences, supported by repeated textbook patterns:

1. **Point-in-time multimodal data plane:** prices, fundamentals, macro, news, corporate actions, derivatives, futures metadata, and event-time market data with vintage/cutoff tracking.
2. **Leakage-resistant research harness:** rolling/expanding splits, purging for overlapping labels, transformations fit inside folds, pretrained-model cutoff registry, and negative/shuffled controls.
3. **Model and feature registry:** versions, seeds, hyperparameters, training windows, state persistence, calibration, and reproducible inference contracts.
4. **Prediction-to-portfolio layer:** confidence thresholds, ranking/group semantics, leverage and gross caps, multipliers, covariance, liquidity, margin, borrow, and options lifecycle.
5. **Economic evaluation layer:** relevant benchmarks, costs, turnover, implementation shortfall, crisis slices, sensitivity neighborhoods, multiple-testing controls, and uncertainty intervals.
6. **Cross-sectional research engine:** point-in-time universes, PCA/factor residuals, clustering, ranking, pair discovery, and neutralization.
7. **Regime and risk engine:** HMM/Markov models, volatility/downside forecasts, scenario probabilities, and state-aware allocations/hedges.
8. **Text/foundation-model lab:** timestamp-safe corpora, frozen model versions, structured-output validation, cutoff audits, fine-tuning, calibration, latency/cost tracking, and conventional baselines.
9. **Execution research environment:** event-time quotes/orders/fills, market-impact and opportunity-cost accounting, replay/counterfactual tests, and timeout/fill-risk modeling.

## Textbook claims that especially require independent validation

- Any shown backtest Sharpe, profitability, benchmark outperformance, cost saving, or “all tested combinations profitable” result.
- The inference that accuracy slightly above chance, high AUC, or high synthetic accuracy implies tradability.
- Fixed ADF, cointegration, Hurst, correlation, z-score, PCA-variance, confidence, or trading thresholds as portable constants.
- Economic interpretation and persistence of statistical regimes or clusters.
- Stability of cointegrated pairs, PCA residuals, ranks, factor importances, and selected LASSO variables.
- Benefits of fractional differentiation, preprocessing, wavelets, deep models, fine-tuning, or foundation models relative to simpler baselines.
- Any pretrained-model backtest whose training cutoff is unknown.
- The printed futures allocation formula’s dimensional and exposure behavior.
- Simulated execution savings when the cost label and simulator share assumptions.
- Production suitability of vendor APIs, serialization mechanisms, or platform scheduling merely because an example runs.

## Broad one-sheet nominations by theme (not current priority)

### Trend, direction, and tactical allocation

- Adaptive trend scanning versus fixed-horizon trend baselines.
- Momentum-versus-reversal meta-classification using relative strategy payoff labels.
- Simple GNB/logistic/tree direction baselines before temporal CNN escalation.
- Wavelet-SVR multiscale forecasting with causal-filter and stability audits.

### Regimes, volatility, and downside

- Markov/HMM state probabilities for allocation and volatility forecasting.
- Predicted downside quantiles for stop/hedge selection.
- Forecasted-volatility allocation versus trailing-volatility and covariance-aware baselines.
- Options regime overlays tested with complete lifecycle, premium, margin, and tail accounting.

### Cross-sectional selection and relative value

- Fundamental LambdaRank versus linear factor composites.
- Dividend sustainability/yield ranking with vintage-safe data.
- PCA residual mean reversion versus sector-neutral reversal.
- Clustered pair discovery with multiple-testing correction and an actual net traded portfolio.
- Corporate-action event models, beginning with stock splits and exact-time event studies.

### Data and representation research

- Raw versus stationary versus fractionally differentiated versus PCA representations.
- Imputation and outlier-treatment sensitivity under real missingness/tails.
- Feature-selection stability across LASSO, ridge, trees, RFE, and PCA.
- Synthetic-to-real pattern learning with rule/template/frequency-matched controls.

### Text and foundation models

- FinBERT versus lexicon, bag-of-words, and general-LLM sentiment.
- Frozen general-LLM event extraction and news aggregation with publish-time replay.
- Cutoff-clean Chronos probabilistic forecasts versus naive/statistical/supervised models.
- Fine-tuning only where label quality, sample size, calibration, and incremental value justify it.

### Execution and portfolio construction

- Learned execution timing evaluated on total implementation shortfall.
- Distribution-aware portfolio optimization using forecast samples rather than median paths alone.
- Universal prediction-to-position tests: confidence calibration, turnover, costs, leverage, liquidity, margin, borrow, and tail risk.

### Research infrastructure

- Point-in-time multimodal datasets and transformation lineage.
- Walk-forward/purged evaluation with shuffled controls and multiple-testing discipline.
- Model/cutoff/version registry and reproducible persistence.
- Sensitivity-surface and cross-market generalization reporting as standard evidence.
