---
title: "Step 3: Model Choice, Training, and Application"
chapter: 5
source: "Hands-On AI Trading with Python, QuantConnect, and AWS"
source_file: "/Users/destinguarnieri/Desktop/Hands-On AI Trading with Python QuantConnect and AWS.epub/OPS/c005.xhtml"
status: "extracted"
---

# Chapter 5: Step 3—Model Choice, Training, and Application

## Overview

This chapter surveys model families used in financial analysis and demonstrates each with Python: regression, classification, ranking, clustering, and language/time-series foundation models. A **model** is a learned mathematical representation of relationships in training data, used either to explain that data or to predict unseen data. Supervised learning uses labeled feature/target pairs for regression or classification; unsupervised learning discovers structure in unlabeled data through methods such as clustering and dimensionality reduction. Large language models combine large-scale unlabeled next-token training with labeled fine-tuning and are therefore described here as semi-supervised. Reinforcement learning is treated separately: an agent learns actions through trial and error to maximize cumulative reward. Source: pp. 87–88.

The practical message is model-choice discipline: match the algorithm's assumptions and inductive bias to the target, data volume, nonlinearity, temporal structure, noise, interpretability needs, and scaling; tune using held-out data; measure the correct objective; and watch for overfitting. Source: pp. 87–140.

## Learning Objectives (Inferred)

- Distinguish supervised, unsupervised, semi-supervised, and reinforcement-learning paradigms. Source: pp. 87–88.
- Select among linear/polynomial/regularized/tree/kernel/regime-switching regressors. Source: pp. 88–110.
- Train and evaluate tree ensembles, logistic regression, HMMs, Gaussian Naive Bayes, and CNN/LSTM classifiers. Source: pp. 110–127.
- Apply learning-to-rank and density-based clustering with task-appropriate metrics. Source: pp. 127–132.
- Use general LLMs, Chronos, and FinBERT for text and time-series tasks while understanding fine-tuning and preprocessing needs. Source: pp. 132–140.

## Model-Selection Summary

| Model | Primary task | Financial uses | Scaling guidance | Main caution | Source |
|---|---|---|---|---|---|
| Linear regression | Continuous prediction | Trends, risk, prices/returns/rates/valuation | Recommended, not mandatory | Linear form; outliers | pp. 89–91 |
| Polynomial regression | Nonlinear continuous prediction | Cycles, rates, growth, asset performance | Recommended | High degree overfits | pp. 91–93 |
| LASSO | Sparse linear prediction/selection | Credit risk, factor selection, portfolios | Essential | Can discard relevant predictors | pp. 93–96 |
| Ridge | Shrunk linear prediction | Multicollinearity, returns, indicators, portfolios | Essential | Large penalty underfits | pp. 96–99 |
| Markov-switching regression | Regime-dependent time series | Cycles, bull/bear regimes, structural breaks | Recommended | Small data/infrequent regimes | pp. 99–103 |
| Decision-tree regression | Nonlinear rule prediction | Credit/distress/default and price drivers | Not required | Overfitting | pp. 103–105 |
| SVR + wavelets | Noisy/nonstationary forecasting | Price, volatility, cycles, high frequency | Essential | Compute and interpretability | pp. 105–110 |
| LightGBM random forest | Multiclass classification | Fraud, segmentation, credit | Not required | Tree complexity/overfit | pp. 110–114 |
| Logistic regression | Probabilistic classification | Default, fraud, approval, buy/sell | Recommended | Linear log-odds assumption | pp. 114–117 |
| HMM | Hidden-state classification | Regimes, cycles, patterns | Recommended | Parameter estimation/state count | pp. 117–119 |
| Gaussian Naive Bayes | Probabilistic classification | Risk, trend, anomaly, fraud | Recommended | Gaussian and independence assumptions | pp. 119–122 |
| CNN/LSTM network | Learned sequential patterns | Price, anomalies, high-frequency data | Essential | Data/compute/tuning; opaque | pp. 122–127 |
| LGBRanker | Within-group ranking | Borrowers, products, clients, assets | Optional/recommended | Groups and relevance labels must be meaningful | pp. 127–130 |
| OPTICS | Density clustering | Anomalies, clients, regimes | Recommended | Distance-scale sensitivity | pp. 130–132 |
| OpenAI LLM | Text generation/analysis | Research, compliance, reporting, sentiment | Text: no; numerical companions: useful | Cost/data and unsupported outputs | pp. 132–135 |
| Chronos | Pretrained time-series forecast | Prices, trends, risk/portfolio inputs | Required | Fine-tune for production | pp. 135–137 |
| FinBERT | Financial-text sentiment | News/reports/social/events/customer feedback | Required per source | Fine-tune for task/domain | pp. 137–140 |

## Key Concepts and Methods

### Regression

Regression fits a mathematical relationship between a dependent continuous variable and one or more independent variables. Finance commonly treats an asset price as dependent and economic factors or market indicators as predictors. Source: pp. 88–89.

#### Linear Regression

Linear regression is fast, simple, and interpretable, making it a useful baseline. It can fail when relationships are nonlinear or outliers dominate. Scaling is optional mathematically but improves interpretability and behavior when features have very different units. Source: pp. 89–91.

The example generates one-feature linear data with noise, makes a 70/30 train/test split, fits scikit-learn `LinearRegression`, predicts both partitions, reports mean squared error (MSE), $R^2$, coefficients, and intercept, and plots train/test observations with the fitted line. The output illustrates a positive linear fit. Source: pp. 89–91.

#### Polynomial Regression

Polynomial regression expands predictors into polynomial terms and applies a linear estimator in that transformed feature space. It captures curved/cyclical relationships, but increasing degree raises variance and can fit noise. L1 or L2 penalties restrain large polynomial coefficients and improve unseen-data performance. Scaling becomes increasingly helpful because higher powers expand feature ranges. Source: pp. 91–93.

The example creates quadratic data, splits it 70/30, constructs degree-2 `PolynomialFeatures`, fits linear regression on transformed features, evaluates MSE/$R^2$, and plots the smooth curve. Source: pp. 91–93.

#### LASSO Regression

Least Absolute Shrinkage and Selection Operator adds an L1 coefficient penalty. It is valuable when many candidate predictors exist but only a subset is expected to matter: increasing $\alpha$ shrinks weak coefficients and can set them exactly to zero, combining regularization with feature selection. It may be inappropriate if every feature is essential or the complete coefficient set must be retained. Standardization is essential so penalty size does not depend on units. Source: pp. 93–96.

The synthetic example uses 100 observations and 10 features, with only the first two driving the target, then standardizes, splits, fits `Lasso(alpha=0.1)`, evaluates predictions, and plots actual-versus-predicted values plus coefficients. Most learned coefficients are near zero, demonstrating selection. Source: pp. 93–96.

#### Ridge Regression

Ridge adds an L2 penalty and is designed for correlated predictors (**multicollinearity**), where ordinary coefficient estimates become unstable and individual effects are hard to isolate. Ridge accepts bias to reduce variance and improve prediction. Unlike LASSO, it generally retains all predictors while shrinking them. At $\alpha=0$ it reduces to ordinary linear regression; excessively large $\alpha$ underfits. Standardization is essential for uniform penalization. Source: pp. 96–99.

The example parallels LASSO using standardized 10-feature synthetic data and `Ridge(alpha=1.0)`, then evaluates and plots predictions and coefficient magnitudes. The source comments that most are effectively zero, though ridge shrinkage ordinarily need not produce exact zeros. Source: pp. 96–99.

#### Markov Switching Dynamic Regression

Markov-switching regression assumes multiple latent regimes, each with distinct regression parameters (for example rising versus falling markets). A stochastic Markov process controls transitions, with the next-state distribution depending only on the current state rather than full history. It captures business cycles, structural breaks, volatility regimes, and bull/bear behavior. It is unsuitable for small samples or regimes that occur too rarely/randomly to estimate. Scaling can improve convergence and interpretation. Source: pp. 99–103.

The example generates 200 observations in two blocks with different means/volatilities, fits a two-regime statsmodels `MarkovRegression` with switching variance, prints fit statistics, predicts, and plots fitted regime lines and smoothed state probabilities. The displayed summary reports regime-specific constants/variances and transition estimates; the probability plot indicates which regime dominates through time. Source: pp. 99–103.

#### Decision Tree Regression

A decision tree recursively partitions observations by feature thresholds and predicts a constant within each leaf. It captures nonlinear structure without polynomial engineering and is invariant to monotonic rescaling. Its explicit rules and plotted structure aid interpretation, but unconstrained trees overfit; depth/pruning constraints or ensembles improve generalization. Source: pp. 103–105.

The example fits a depth-4 `DecisionTreeRegressor` to synthetic one-dimensional data, evaluates train/test MSE and $R^2$, plots its stepwise prediction function, and renders nodes with split conditions, sample counts, and leaf values. Source: pp. 103–105.

#### Support Vector Regression with Wavelet Forecasting

An SVM classifier finds a separating hyperplane; SVR instead seeks a smooth function containing as many observations as possible within an $\epsilon$-wide margin/tube. Kernel choices include linear, polynomial, and radial basis function (RBF, sklearn's default). $C$ trades model simplicity/margin width against training errors: larger $C$ penalizes errors more and tends toward a narrower margin; smaller $C$ tolerates more errors. Smaller $\epsilon$ demands a tighter fit and increases overfit risk. $\gamma$ controls how local a training point's influence is. Scaling is essential for convergence and distance/kernel behavior. Source: pp. 105–108.

Wavelets decompose a nonstationary signal into time/frequency components so short- and long-horizon trends or cycles can be modeled separately and reconstructed. `pywt.wavedec(y, 'db1', level=2)` returns multilevel Daubechies-1 coefficients; `pywt.waverec(coeffs, 'db1')` reconstructs the signal. The text labels reconstruction with `wavedec`, but the shown API and description indicate `waverec`. Source: pp. 106–107.

The first example denoises/reconstructs a sinusoidal signal, scales the feature, fits RBF SVR, evaluates MSE/$R^2$, and plots the curve. A second example uses `GridSearchCV` across kernels and $C$, $\gamma$, and $\epsilon$ values, selecting by negative MSE and reporting the best settings/test performance. Source: pp. 107–110.

### Classification

Classification predicts discrete labels rather than continuous values. The chapter covers ensembles, linear probability classification, latent-state models, generative Bayesian classification, and deep networks. Source: pp. 110–127.

#### Multiclass Random Forest Model

**Ensemble learning** combines several models to outperform individuals; common patterns are bagging, boosting, and stacking. A decision tree maps feature tests to branches and class-valued leaves but readily overfits. A random forest trains diverse trees using bootstrap samples and random feature subsets, then aggregates predictions. **Bagging** means training on random resampled subsets and averaging/voting. Source: pp. 110–111.

The example configures LightGBM with `boosting_type='rf'` for multiclass logarithmic-loss optimization. Important controls are `num_leaves` (complexity/overfit), `learning_rate` (step shrinkage and tree count), `feature_fraction`, `bagging_fraction`, and `bagging_freq`. Synthetic classes are approximately balanced; `GridSearchCV` selects hyperparameters. Outputs include class distribution, confusion matrix, and feature importance. Source: pp. 111–114.

#### Logistic Regression and Evaluation Metrics

Logistic regression produces class probabilities for binary tasks and extends to multiclass. Finance uses it for default, fraud, product uptake, and trading actions. Its central assumption is that predictors relate linearly to the **log odds**, not necessarily to probability itself. Scaling helps convergence and coefficient comparison. Source: pp. 114–116.

The example generates binary data, standardizes it, splits it, tunes $C$ and penalty with cross-validation, then reports accuracy, confusion matrix, classification report, ROC curve, and AUC (shown as about 0.74). A confusion matrix distinguishes true positive (TP), true negative (TN), false positive (FP/Type I), and false negative (FN/Type II). ROC plots true-positive rate against false-positive rate across thresholds; AUC nearer 1 indicates stronger discrimination. Source: pp. 115–117.

#### Hidden Markov Models

An HMM represents observations as emissions from unobserved states and estimates probabilistic transitions between those states. It supports regime detection, economic-cycle inference, and sequential pattern forecasting, but parameter estimation can be difficult. The number of states is an input; the chapter suggests beginning with two and increasing based on results. Scaling can improve convergence. Source: pp. 117–119.

The example generates a two-state time series, fits `GaussianHMM(n_components=2)`, predicts hidden states, and plots observations colored/segmented by inferred regime. Source: pp. 118–119.

#### Gaussian Naive Bayes

Gaussian Naive Bayes applies Bayes' theorem, estimates a mean and variance for each feature within each class, assumes Gaussian feature likelihoods and conditional feature independence, and chooses the class with highest posterior probability. It is fast and interpretable but degrades when distributions are strongly non-Gaussian or dependence is material. Source: pp. 119–120.

The example creates binary data, standardizes, fits `GaussianNB`, reports predictions/classification statistics, and plots an ROC curve with AUC about 0.84. Source: pp. 120–122.

#### Convolutional Neural Networks

Neural networks transform inputs through connected weighted layers and learn weights by minimizing a loss. CNNs learn local/complex patterns; recurrent networks handle sequence/context; transformers support language; feedforward networks cover simpler patterns. Architecture selection determines input size, hidden-layer connectivity, and output. Loss and optimizer are core hyperparameters. Regularization, dropout, early stopping, and augmentation combat overfitting. CNNs can be powerful on financial sequences but demand data, compute, tuning, and sacrifice interpretability. Scaling is essential. Source: pp. 122–124.

The example combines three Conv1D layers (64 outputs), dropout, two LSTM layers (50-unit sequence output then 50-unit vector), and a one-unit dense output. LSTMs retain long dependencies; dropout randomly zeros a fraction of units. Adam is selected for efficiency, low memory use, and performance on large data. Synthetic time-series samples are reshaped and trained for 300 epochs. Source: pp. 123–126.

The ROC output evaluates classification. The loss plot shows training loss steadily approaching zero while validation loss bottoms out then rises, a direct overfitting diagnosis: the model memorizes training noise and generalizes worse. Source: pp. 126–127.

### Ranking

#### LGBRanker Ranking

Learning-to-rank learns orderings from lists whose items have partial relevance order and predicts permutations for new lists. LightGBM's LGBRanker uses LambdaRank to optimize ranking objectives at scale. Finance applications include ordering borrowers by default risk, products by customer suitability, clients by value/risk, and assets by expected return/risk. As a tree model it does not require scaling, though scaling may help disparate features. Source: pp. 127–128.

The example creates 100 synthetic stocks with returns, volatility, and momentum, forms a weighted relevance target, and divides them into ten groups of ten. Each group is ranked independently—analogous to each trading day or portfolio segment. **NDCG@5** scores the top five ranked items from 0 to 1, with 1 perfect. The predicted-versus-true scatter lies near the diagonal, corroborating high NDCG. Source: pp. 128–130.

### Clustering

#### OPTICS Clustering

OPTICS (Ordering Points To Identify the Clustering Structure) orders points by density reachability and core distance. Unlike k-means, it does not require a prespecified cluster count and can recover clusters of differing density while labeling noise. Uses include transaction anomaly detection, behavioral segmentation, and market-regime discovery. Feature normalization is recommended because distances otherwise reflect units. Source: pp. 130–132.

The example creates synthetic blobs and fits sklearn `OPTICS`; black points represent noise. The **silhouette score** is better when higher because points resemble their own cluster more than others; the **Davies–Bouldin index** is better when lower because clusters are less similar to their closest rival. Source: pp. 131–132.

### Language Models

#### OpenAI Language Model

GPT-family LLMs are trained on large text corpora and can summarize, translate, answer questions, generate text, and classify sentiment. They extract patterns from unstructured financial language for research, reports, compliance, prediction, and risk workflows. Their drawbacks include substantial data/compute requirements. Text features do not require ordinary numeric normalization, though accompanying numerical inputs may benefit from it. Source: pp. 132–133.

The example sends a batch of synthetic positive, negative, and neutral sentences to an OpenAI chat model with instructions to return structured JSON sentiment labels, then parses and prints the response. Production use should treat the requested schema as an interface contract and validate returned content. Source: pp. 133–135.

#### Amazon Chronos Model

Chronos is a family of pretrained time-series forecasters built on language-model architecture. It scales and quantizes a time series into tokens, trains with cross-entropy, and was pretrained on public and Gaussian-process-generated synthetic series. Financial uses include prices, trends, portfolio inputs, and risk forecasts. The chapter requires normalization/scaling and recommends task-specific fine-tuning for production. Source: pp. 135–136.

The example forecasts 30 points from a synthetic series with a pretrained Chronos model. Its forecast tensor contains multiple sampled futures by horizon; taking the median across samples yields one central path. Alternatively, 10%, 50%, and 90% quantiles express a likely range. The plotted prediction tracks the actual continuation with uncertainty implicit in samples/quantiles. Source: pp. 136–137.

#### FinBERT Model

FinBERT further trains BERT on financial language and fine-tunes it for sentiment. It targets news, reports, social media, customer feedback, earnings, and merger language; sentiment can inform market prediction, risk, portfolio decisions, and product improvement. The source describes normalization/standardization as required and recommends task-specific fine-tuning for production. Source: pp. 137–140.

The example tokenizes synthetic financial statements, creates attention masks so the model attends to relevant non-padding tokens, performs inference, maps output scores to negative/positive labels, and prints confidence/probabilities. Source: pp. 138–140.

## Mathematical Formulas

### LASSO Objective (MathML nodes 1–4)

$$
\mathcal{L}_{\text{LASSO}}=RSS+\alpha\sum_{i=1}^{n}|w_i|
$$

**Symbols:** $RSS=\sum_j(y_j-\hat y_j)^2$ is residual sum of squares; $w_i$ is coefficient $i$; $n$ is the number of penalized coefficients; $\alpha\ge 0$ is regularization strength. **Purpose:** balance fit against coefficient sparsity. **Validity/conditions:** features should be standardized for comparable penalties; the useful $\alpha$ should be selected on validation data. **Interpretation:** larger $\alpha$ lowers coefficient magnitudes and can make them exactly zero. The source's MathML consists of one display objective plus inline $w_i$, $\alpha$, and a repeated $\alpha$ reference. Source: p. 93.

### Ridge Objective (MathML nodes 5–8)

$$
\mathcal{L}_{\text{ridge}}=RSS+\alpha\sum_{i=1}^{n}w_i^2
$$

**Symbols:** $RSS$, $w_i$, $n$, and $\alpha$ are as above. **Purpose:** stabilize correlated-predictor regression and reduce variance without selecting variables exactly. **Validity/conditions:** standardize features; $\alpha=0$ gives ordinary least squares; very large $\alpha$ can underfit. **Interpretation:** L2 penalization smoothly shrinks all coefficients. The source's MathML consists of the display objective plus inline $\alpha$, repeated $\alpha$, and $w_i$. Source: p. 96.

### Accuracy (MathML node 9)

$$
\mathrm{Accuracy}=\frac{TP+TN}{TP+TN+FP+FN}
$$

**Symbols:** TP/TN are correctly predicted positives/negatives; FP/FN are Type I/II errors. **Purpose:** overall correct fraction. **Conditions:** denominator must be nonzero; accuracy can mislead under class imbalance or unequal error costs. **Interpretation:** weights every observation and both classes equally. Source: p. 117.

### Precision (MathML node 10)

$$
\mathrm{Precision}=\frac{TP}{TP+FP}
$$

**Purpose:** fraction of predicted positives that are correct. **Conditions:** $TP+FP>0$; relevant when false positives are costly. **Interpretation:** high precision means few positive alarms are false. Source: p. 117.

### Recall (MathML node 11)

$$
\mathrm{Recall}=\frac{TP}{TP+FN}
$$

**Purpose:** fraction of actual positives detected; also sensitivity/true-positive rate. **Conditions:** $TP+FN>0$; relevant when missed positives are costly. **Interpretation:** high recall means few positives are missed. Source: p. 117.

### F1 Score (MathML node 12)

$$
F_1=\frac{2\,\mathrm{Precision}\,\mathrm{Recall}}{\mathrm{Precision}+\mathrm{Recall}}
$$

**Purpose:** harmonic balance of precision and recall. **Conditions:** their sum must be positive; it omits true negatives and does not encode business costs. **Interpretation:** becomes low when either precision or recall is low. Source: p. 117.

## General Training and Evaluation Procedure

1. Define the task: continuous prediction, class label/probability, within-group rank, unlabeled structure, text transformation, or probabilistic forecast.
2. Split data before fitting transformations; for financial time series, preserve chronology even though many synthetic chapter examples use random splits.
3. Normalize/standardize when required by penalties, kernels, distances, or neural optimization.
4. Fit only on training data; tune hyperparameters through cross-validation/grid search or an explicit validation set.
5. Evaluate on unseen data with task-specific metrics: MSE/$R^2$, confusion/ROC/AUC/F1, NDCG, silhouette/Davies–Bouldin, or forecast quantiles.
6. Inspect coefficients, feature importance, regime probabilities, tree structure, learning curves, and plots for failure modes that a scalar score hides.
7. Fine-tune pretrained models to production-domain data and validate outputs/interfaces.

Source: pp. 89–140.

## Figures and Tables

### Image Figures (24)

| Source element | Content and meaning | Source |
|---|---|---|
| Figure 5.1 | Train/test points align around a positive fitted linear line. | pp. 90–91 |
| Figure 5.2 | Degree-2 curve captures concave-up nonlinear data. | pp. 92–93 |
| Figure 5.3 | LASSO actual-versus-predicted values lie near ideal diagonal. | p. 93 |
| Figure 5.4 | Most LASSO feature coefficients are near zero, showing selection. | pp. 95–96 |
| Figure 5.5 | Ridge actual-versus-predicted fit. | pp. 98–99 |
| Figure 5.6 | Ridge coefficient shrinkage across features. | pp. 98–99 |
| Unnumbered Markov summary | 200 observations; two regimes with different constants/variances; transition estimates and likelihood/AIC/BIC/HQIC. | pp. 101–102 |
| Figure 5.7 | Observations/fitted values transition between regime-specific regressions. | p. 102 |
| Figure 5.8 | Smoothed probabilities show time-varying likelihood of each regime. | pp. 102–103 |
| Figure 5.9 | Decision-tree regressor produces a stepped piecewise-constant function. | p. 104 |
| Figure 5.10 | Depth-4 tree exposes threshold rules, samples, and leaf predictions. | p. 105 |
| Figure 5.11 | RBF SVR follows a sinusoidal/wavelet-processed pattern. | p. 108 |
| Figure 5.12 | Synthetic multiclass labels are approximately balanced. | p. 113 |
| Figure 5.13 | Heat-map confusion matrix displays correct and incorrect class assignments. | pp. 113–114 |
| Figure 5.14 | Horizontal feature-importance bars rank predictors. | p. 114 |
| Figure 5.15 | Logistic ROC has AUC about 0.74, better than chance but imperfect. | p. 116 |
| Figure 5.16 | Observations are segmented into two inferred hidden states. | p. 119 |
| Figure 5.17 | Gaussian Naive Bayes ROC has AUC about 0.84. | pp. 121–122 |
| Unnumbered architecture | Conv1D 1→64, two more Conv1D 64→64, dropout, LSTM 64→50 sequence, LSTM 50→50, dense 50→1. | pp. 123–124 |
| Figure 5.18 | Neural classifier ROC visualizes discrimination. | p. 126 |
| Figure 5.19 | Train loss falls toward zero while validation loss rises after its minimum: overfitting. | pp. 126–127 |
| Figure 5.20 | Ten group-colored rank points lie near the true=predicted diagonal. | p. 130 |
| Figure 5.21 | OPTICS recovers colored clusters; black denotes noise. | p. 132 |
| Figure 5.22 | Chronos forecast follows actual synthetic/AMZN-like closing-price trend. | p. 137 |

### Table Figures (18)

Seventeen model-summary tables state description, finance use cases, scaling requirement, and install dependencies for: linear, polynomial, LASSO, ridge, Markov switching, decision tree, SVR/wavelets, multiclass random forest, logistic regression, HMM, Gaussian Naive Bayes, CNN, LGBRanker, OPTICS, OpenAI LLM, Chronos, and FinBERT. Their details are consolidated in “Model-Selection Summary.” Source: pp. 89, 91, 93, 96, 99, 103, 105, 110, 114, 117, 119, 122, 127, 130, 132–133, 135, 137.

The eighteenth table is the $2\times2$ binary confusion-matrix layout: rows are actual positive/negative, columns predicted positive/negative, and cells TP/FN/FP/TN. Source: p. 117.

## Applications

- Forecast prices, returns, rates, volatility, and macro indicators with regressors or Chronos. Source: pp. 89–110, 135–137.
- Select factors and stabilize correlated portfolio/risk models with LASSO/ridge. Source: pp. 93–99.
- Identify bull/bear, volatility, or economic regimes with Markov models and OPTICS. Source: pp. 99–103, 117–119, 130–132.
- Classify default, fraud, distress, market direction, or trade actions. Source: pp. 103–127.
- Rank borrowers, customers, products, or securities within comparable groups. Source: pp. 127–130.
- Extract sentiment and structured insights from financial language with GPT-family models and FinBERT. Source: pp. 132–140.

## Assumptions, Limitations, and Edge Cases

- Linear regression assumes an adequate linear specification and is sensitive to substantial outliers. Source: p. 89.
- Polynomial degree increases feature magnitude and overfit risk; validation and regularization are necessary. Source: pp. 91–93.
- LASSO assumes sparsity is useful; correlated relevant features can be unstable under selection. The latter is a methodological implication, not explicitly discussed by the source. Source: pp. 93–96.
- Ridge stabilizes multicollinearity but introduces bias and does not supply sparse selection. Source: pp. 96–99.
- Markov models assume current-state-dependent transitions and enough observations per regime. Source: pp. 99–103.
- Trees are scale-invariant but unstable/overfit without constraints or ensembles. Source: pp. 103–105.
- SVR depends strongly on scaling and $C$, $\epsilon$, $\gamma$, and kernel choices. Source: pp. 105–110.
- Random train/test splitting in the synthetic examples does not address temporal leakage; real financial validation should be chronological. This is an extraction inference based on example design.
- Logistic regression's linear-log-odds structure may be wrong; accuracy is unsafe under imbalance. Source: pp. 114–117.
- HMM state count is imposed and states are statistical constructs, not guaranteed economic regimes. Source: pp. 117–119.
- Gaussian Naive Bayes assumes conditional independence and Gaussian likelihoods. Source: pp. 119–122.
- Neural networks require substantial data/compute and can overfit even as training loss improves. Source: pp. 122–127.
- Ranking requires correct group boundaries; scores are meaningful only within the list/group definition. Source: pp. 127–130.
- OPTICS is distance-based; unscaled dimensions can dominate. Noise labels are expected, not necessarily errors. Source: pp. 130–132.
- Pretrained LLM/Chronos/FinBERT models require output validation and often task-specific fine-tuning before production. Source: pp. 132–140.

## Common Mistakes and Warnings

- Selecting a complex model before establishing a linear baseline. Source: pp. 89–93.
- Scaling the full dataset before splitting, which would leak held-out distribution information (inferred best practice).
- Using unstandardized inputs with LASSO, ridge, SVM, CNN, or distance clustering. Source: pp. 93–99, 105–110, 122–132.
- Treating near-zero ridge coefficients as guaranteed exact feature elimination; that property belongs to LASSO. Source: pp. 93–99.
- Raising polynomial degree, tree depth/leaves, $C$, or neural epochs based only on training score. Source: pp. 91–127.
- Choosing Markov/HMM regimes without enough data or checking state probabilities and stability. Source: pp. 99–103, 117–119.
- Reporting accuracy alone without confusion matrix, precision, recall, F1, ROC, and the business costs of FP/FN. Source: pp. 116–117.
- Reading falling training loss as success while validation loss rises. Source: pp. 126–127.
- Comparing ranks across groups when the model objective ranks within each group. Source: pp. 128–130.
- Treating an LLM's requested JSON or label as trustworthy without parsing and schema/semantic validation (inferred deployment warning).
- Using a pretrained Chronos/FinBERT model as final production logic without domain fine-tuning. Source: pp. 135–140.

## Key Takeaways

1. Task definition determines the model and metric: prediction, classification, ranking, clustering, language, and probabilistic forecasting are not interchangeable.
2. Scaling is integral—not cosmetic—for penalties, kernels, distances, and neural optimization.
3. Regularization manages the bias–variance trade-off: LASSO selects; ridge shrinks; dropout and early stopping regularize networks.
4. Financial regimes and nonstationarity motivate Markov and wavelet methods, but added flexibility increases estimation difficulty.
5. Validation evidence outranks training fit; learning curves, state probabilities, coefficients, and error decompositions reveal failure modes.
6. Foundation models accelerate text/time-series work, but production use still needs task-specific adaptation and validation.

## Glossary

| Term | Definition | Source |
|---|---|---|
| AUC | Area under ROC; threshold-independent discrimination summary. | p. 117 |
| Bagging | Bootstrap aggregating across resampled training sets. | pp. 110–111 |
| CNN | Network using convolutional filters to learn local patterns. | pp. 122–126 |
| Core distance | OPTICS density measure needed to characterize a point's neighborhood. | pp. 130–131 |
| Dropout | Regularizer that randomly zeros units during training. | pp. 123–124 |
| Ensemble learning | Combining multiple models into one prediction. | pp. 110–111 |
| HMM | Probabilistic sequence model with hidden states and emissions. | pp. 117–119 |
| LASSO | L1-regularized regression capable of zeroing coefficients. | pp. 93–96 |
| LGBRanker | LightGBM learning-to-rank estimator using LambdaRank. | pp. 127–130 |
| Log odds | Logarithm of probability odds, modeled linearly by logistic regression. | p. 114 |
| LSTM | Recurrent neural layer designed to retain long dependencies. | pp. 123–126 |
| Multicollinearity | High predictor correlation that destabilizes coefficient estimates. | p. 96 |
| NDCG@5 | Top-five normalized discounted cumulative gain, from 0 to 1. | p. 130 |
| OPTICS | Density-ordering clustering method supporting variable densities and noise. | pp. 130–132 |
| Reachability | OPTICS density relation used to order/discover clusters. | pp. 130–131 |
| Ridge | L2-regularized regression that shrinks coefficients. | pp. 96–99 |
| ROC | Curve of true-positive versus false-positive rates over thresholds. | p. 117 |
| Semi-supervised learning | Combination of unlabeled pretraining and labeled fine-tuning. | pp. 87–88 |
| SVR | Support-vector method fitting a smooth function within an epsilon margin. | pp. 105–110 |
| Wavelet decomposition | Multiscale representation in time and frequency. | pp. 106–107 |

## Connections to Other Chapters

- Reinforcement learning is explicitly deferred to a separate chapter. Source: p. 88.
- Later examples fine-tune pretrained Chronos and FinBERT models on task-specific data. Source: pp. 135–140.
- This chapter is Step 3 of the book's broader AI-trading workflow: it assumes data/features/targets exist and focuses on choice, training, and application.

## Extraction Issues and Completeness Audit

- **Headings:** all 40 numbered section headings (`c005-sec-0001` through `c005-sec-0040`) are represented, including every “Python Example,” either as a dedicated model discussion or its example paragraph.
- **MathML:** all 12 nodes are represented: LASSO display + three inline references; ridge display + three inline references; four display classification metrics.
- **Figures:** all 42 source `<figure>` elements are represented: 24 image figures (22 numbered, 2 unnumbered) and 18 table figures.
- **Tables:** all 18 tables are represented: 17 model summary tables plus one confusion matrix.
- The text incorrectly labels wavelet reconstruction as `pywt.wavedec`; its subsequent code/description uses reconstruction semantics (`waverec`). Source: pp. 106–107.
- The Ridge narrative says most example coefficients are “essentially zeros.” Ridge shrinks but generally does not create exact zeros; the distinction is preserved. Source: pp. 98–99.
- The CNN summary table calls the task financial time-series classification, while Figure 5.18's caption calls the network “regression”; the example uses ROC, indicating classification evaluation. Source: pp. 122–126.
- The OpenAI example, package/model names, installation URLs, and API calling patterns are time-sensitive and are recorded as book content, not current documentation.
- Several examples use synthetic/random splits. They demonstrate APIs but do not establish out-of-sample trading validity, transaction-cost robustness, or time-series leakage control.
