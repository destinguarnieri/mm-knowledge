---
title: "Step 2: Dataset Preparation"
chapter: 4
source: "Hands-On AI Trading with Python, QuantConnect, and AWS"
source_file: "OPS/c004.xhtml"
status: "extracted"
---

# Chapter 4: Step 2: Dataset Preparation

## Overview

After defining an AI trading problem, the next stage is to build a trustworthy dataset for training and evaluation. Dataset quality and breadth directly affect model performance and generalization. The chapter's workflow covers collection, exploratory analysis, cleaning and transformation, feature engineering and selection, time-series stationarity and cointegration, and separation into training, validation, and test data. (Source: pp. 53–86)

## Learning Objectives (Inferred)

- Collect market, fundamental, macroeconomic, and alternative data from dependable providers. (Source: p. 53)
- Use exploratory data analysis (EDA) to understand distributions, patterns, anomalies, and assumptions. (Source: pp. 53–54)
- Detect, treat, and evaluate missing values and outliers. (Source: pp. 55–61)
- Engineer features and choose correctly between normalization and standardization. (Source: pp. 61–64)
- Test time series for stationarity, apply ordinary or fractional differencing, and identify cointegration. (Source: pp. 64–76)
- Select useful features with correlation, model importance, recursive elimination, and PCA. (Source: pp. 76–83)
- Construct training, validation, testing, and cross-validation schemes and understand their tradeoffs. (Source: pp. 83–86)

## Key Concepts

### Data Collection

Relevant inputs can include historical prices, trading volumes, other market observations, macroeconomic indicators, company financial statements, and alternative data such as news or social-media sentiment. Reliable sources are essential because inaccurate or compromised inputs undermine dataset integrity and downstream models. (Source: p. 53)

### Exploratory Data Analysis

EDA combines summary statistics and visualization to learn the dataset's structure, expose patterns and anomalies, check assumptions, and decide what preprocessing and modeling should follow. The chapter uses pandas for manipulation and Sweetviz for automated HTML reports. (Source: pp. 53–54)

The Sweetviz example creates 100 synthetic records with Age (integers 8–89), Income (integers 10,000–499,999), Gender, and five cities. `sv.analyze` produces a general report; `compare_intra` compares male and female subsets. A fixed random seed of 42 makes the sample reproducible. (Source: p. 54)

### Data Preprocessing

Preprocessing follows initial understanding of the data. It removes or corrects missing values, outliers, duplicates, errors, and inconsistencies originating from entry mistakes, technical failures, market anomalies, or unusual events. It may also scale mismatched features, transform non-stationary time series, and test pairs for cointegration. (Source: pp. 54–55)

### Handling Missing Data

Missing observations can bias results, reduce accuracy, and produce faulty financial forecasts. The first task is to locate and count them. The example creates 1,000 daily OHLCV observations, deliberately makes 50 Volume and 20 Close entries missing, and counts nulls with `df.isnull().sum()`. Volume is converted to floating point so it can hold `NaN`. (Source: pp. 55–57)

#### Missing-Data Strategies

- **Delete rows or columns:** `dropna()` is simple but can discard substantial information. (Source: p. 57)
- **Mean, median, or mode imputation:** `SimpleImputer` fills entries with a column statistic. (Source: p. 57)
- **KNN imputation:** `KNNImputer(n_neighbors=5)` uses values from five nearest observations. (Source: p. 57)
- **MICE:** `IterativeImputer` chains regression models to perform multivariate imputation. (Source: p. 57)

The Date field is excluded in the examples because the demonstrated imputers operate on numeric columns. After imputation, compare original and imputed data using plots or statistics; filling missing values is not complete until its effect is evaluated. (Source: pp. 57–58)

### Handling Outliers

Outliers can distort predictive models and conclusions, but they may be either errors or legitimate market events. Detection methods include box plots and scatterplots, z-scores, and interquartile-range rules. (Source: pp. 58–59)

#### Box-Plot Detection

The sample prices `[100, 95, 96, 101, 103, 98, 99, 500, 103, 110]` form a compact cluster near 100 with 500 visibly isolated. The box plot identifies 500 as an outlier. (Source: pp. 58–59)

#### Z-Score Detection

A z-score measures distance from the mean in standard-deviation units. The chapter describes thresholds of greater than 2 or less than -2, with ±3 also sometimes used. In the sample, 500 has a reported z-score of 2.844444 and is selected by `abs(Z_score) > 2`. (Source: p. 59)

#### IQR Detection

The interquartile range spans the first quartile, $Q_1$ (25th percentile), to the third, $Q_3$ (75th percentile). The conventional fences are $Q_1-1.5\,IQR$ and $Q_3+1.5\,IQR$, where $IQR=Q_3-Q_1$. The same sample again identifies 500. (Source: pp. 59–60)

#### Outlier Treatments

- **Remove:** appropriate when an extreme point is an error; the example retains only observations with absolute z-score at most 2. (Source: p. 60)
- **Transform:** appropriate when an extreme event is genuine and should remain; applying the natural logarithm compresses 500 from 500 to approximately 6.214608 on the log scale. (Source: pp. 60–61)
- **Cap/floor:** replace values beyond chosen lower or upper limits with those limits. IQR capping changes 500 to 110.125 while leaving the other sample prices unchanged. (Source: p. 61)

### Feature Engineering

Feature engineering modifies raw inputs or creates new ones so they represent the prediction problem more effectively. Techniques named include scaling, categorical encoding, missing-value treatment, and interaction terms. The example derives 5-day and 10-day rolling means of Close (`MA5`, `MA10`) from synthetic OHLCV data. (Source: pp. 61–62)

### Normalization and Standardization

Both methods put features on comparable scales and can improve convergence and performance when units differ. Normalization maps observed values into a fixed range, commonly 0–1, and is presented as useful for methods without a distribution assumption, including neural networks and KNN. Standardization centers features at zero with unit standard deviation and prevents large-unit variables from dominating scale-sensitive methods such as support vector machines. (Source: pp. 62–64)

### Transforming Time-Series Features to Stationary

A stationary series has stable mean, variance, and autocorrelation through time. Non-stationarity makes learned patterns and forecasts less dependable. Remedies include differencing, detrending, and logarithmic transformation. (Source: p. 64)

The Augmented Dickey-Fuller (ADF) test examines the unit-root null hypothesis. A statistic below the relevant critical value supports rejecting a unit root and treating the series as stationary. The example random walk has statistic -1.3583 and p-value 0.6021; after first differencing, its statistic is -10.0089 and p-value about $1.80\times10^{-17}$. (Source: pp. 64–66)

#### Fractional Differentiation

Ordinary differencing can remove predictive memory along with non-stationarity. The chapter recommends López de Prado's fractional differentiation for finance as a compromise between stationarity and retained signal. The fixed-width implementation recursively generates weights until the newest absolute weight falls below a cutoff, then searches $d\in\{0,0.1,\ldots,1.0\}$ for the first version with ADF p-value at most 0.05. In the example, fractional differencing produces statistic -3.6140 and p-value 0.00550, passing the displayed 1%, 5%, and 10% critical thresholds. (Source: pp. 67–70)

### Cointegration and the Engle-Granger Test

Non-stationary series are cointegrated when a linear combination is stationary, implying a stable long-run equilibrium. Engle-Granger testing helps find asset pairs whose relative price may mean-revert, permitting a trade on convergence rather than absolute direction. (Source: p. 70)

In the first synthetic example, two random-walk-like assets individually fail stationarity tests, while their simple spread `asset1 - asset2` is stationary. The cointegration statistic is -10.5469 with p-value about $1.07\times10^{-17}$; the spread ADF statistic is -10.8755 with p-value about $1.34\times10^{-19}$. The chapter uses 0.05 as the rejection level: below it, reject the null of no cointegration; above it, fail to reject. (Source: pp. 70–73)

### Hurst Coefficient and Pairs Trading

The Hurst coefficient $H\in[0,1]$ characterizes long-memory behavior: (Source: p. 73)

- $H<0.5$: mean-reverting.
- $H=0.5$: random walk/no long memory.
- $H>0.5$: persistent trend.

A spread with $H$ substantially below 0.5 is presented as attractive for pairs trading: long the underperformer and short the outperformer in expectation of convergence. A second synthetic example produces $H=0.309986$, described as favorable. Because the chosen Hurst routine depends on logarithms, the code removes non-positive spread values first and warns when it does so. (Source: pp. 73–76)

### Feature Selection

Feature selection keeps inputs that contribute predictive value and removes irrelevant or redundant ones, reducing overfitting and improving interpretability. The chapter covers correlation, tree-based importance, automated elimination, and PCA. (Source: p. 76)

#### Correlation Analysis

Correlation analysis identifies features related to the target and redundancies among features. In the synthetic matrix, Feature1 and Feature2 correlate at 0.994477; their target correlations are 0.980875 and 0.974603, while Feature3's target correlation is only 0.193556. (Source: pp. 76–77)

#### Feature-Importance Analysis

Tree models such as random forests expose model-based feature importance. Before fitting, the example drops predictors with pairwise absolute correlation greater than 0.9, removing the redundant Feature2. Random forest importance is then 0.984778 for Feature1 and 0.015222 for Feature3; the latter is a candidate for removal. (Source: pp. 77–78)

#### Automatic Feature Identification

RFE repeatedly fits a model and removes the least-important input; `SelectFromModel` is another named method. Because correlated features can each appear important in isolation, the example again removes correlations above 0.9 first. RFE is asked to choose two remaining features and selects Feature1 and Feature3. (Source: pp. 78–80)

#### Dimensionality Reduction and PCA

Dimensionality is the number of features. More dimensions demand more computation and memory, obscure structure, and raise overfitting risk. PCA replaces correlated original features with fewer uncorrelated linear combinations ordered by explained variance. Standardization before PCA is essential so scale does not determine contribution. (Source: pp. 80–81)

PCA is applied by computing the covariance matrix, obtaining eigenvectors and eigenvalues, ordering components by explained-variance ratio, keeping the top $K$ whose cumulative variance meets a goal (the chapter gives 90% as an example), assembling those eigenvectors, and projecting standardized data onto them. In the sample, three predictors become two components with explained-variance ratios 0.68742233 and 0.31073740, together retaining about 99.816% of variance. Finance applications include risk management, portfolio optimization, and compact representation of large datasets. (Source: pp. 81–83)

### Training, Validation, and Testing Sets

- **Training set:** fits model parameters and relationships.
- **Testing set:** evaluates generalization on unseen data and helps diagnose overfitting or underfitting.
- **Validation set:** optionally tunes hyperparameters during development, providing an additional check against overfitting. Hyperparameters are predefined controls of the learning process, unlike learned model parameters. (Source: p. 83)

Overfitting occurs when an overly complex model memorizes training observations, including noise and outliers, then generalizes poorly. Underfitting occurs when a model is too simple to capture the underlying pattern and therefore performs poorly on both seen and unseen data. (Source: p. 83)

Common allocations are 70–80% training and 20–30% testing, or 60%/20%/20% for training/validation/testing. A 100-record example with `test_size=0.2` produces 80 rows for training and 20 for testing, each with three predictors. (Source: pp. 83–84)

#### `train_test_split` Controls

- `arrays`: feature matrix and label vector.
- `test_size`: fractional, integer, or inferred test-set size.
- `train_size`: fractional, integer, or inferred training-set size.
- `random_state`: integer seed controlling reproducible shuffle behavior.
- `shuffle`: whether to shuffle before splitting; defaults to true.
- `stratify`: class labels used to preserve class proportions in classification. (Source: pp. 84–85)

#### Cross-Validation

Cross-validation is recommended for small or imbalanced classification datasets or when a more robust performance estimate is needed. In $k$-fold cross-validation, divide the data into $k$ equal folds, train on $k-1$, test on the remaining fold, repeat so each fold is the test fold once, and average the $k$ performance measurements. This is more reliable than one split but more computationally expensive. (Source: pp. 85–86)

On the UCI Wine classification example, five random-forest fold accuracies are 0.9722, 0.9444, 0.9722, 0.9714, and 1.0, averaging 0.9721. A single 80/20 split reports 1.0; the chapter flags that perfect single-split result as possible overfitting despite generally strong performance. (Source: pp. 85–86)

## Mathematical Formulas and Quantitative Relationships

### MathML 1 — Min–Max Normalization

$$
X_{\mathrm{norm}}=\frac{X-X_{\min}}{X_{\max}-X_{\min}}.
$$

- $X$: original feature value, in the feature's original units.
- $X_{\min}$: minimum observed feature value, same units as $X$.
- $X_{\max}$: maximum observed feature value, same units as $X$.
- $X_{\mathrm{norm}}$: dimensionless normalized value.

**Purpose:** Map observed values, normally into $[0,1]$. **Conditions:** Requires $X_{\max}\ne X_{\min}$ and fitted minimum/maximum values. **Interpretation:** The result is the value's fractional position across the observed range. (Source: p. 62)

### MathML 2 — Z-Score Standardization

$$
Z=\frac{X-\mu}{\sigma}.
$$

- $Z$: dimensionless standardized value.
- $X$: original feature value.
- $\mu$: feature mean, same units as $X$.
- $\sigma$: feature standard deviation, same units as $X$.

**Purpose:** Center at zero and scale to unit standard deviation. **Conditions:** $\sigma>0$ and all quantities must refer to the same fitted feature distribution. **Interpretation:** $Z$ is the signed distance from the mean in standard-deviation units. (Source: p. 63)

### MathML 3–5 — Inline Standardization Symbols

The source separately encodes `$Z$`, `$X$`, and `$\mu$` as MathML nodes and defines them respectively as the standardized value, original value, and feature mean. These are variables in the preceding equation, not additional formulas. (Source: p. 63)

### MathML 6 — Population Mean

$$
\mu=\frac{1}{N}\sum_{i=1}^{N}X_i.
$$

- $\mu$: arithmetic mean of the feature.
- $N$: number of observations.
- $i$: observation index, from 1 through $N$.
- $X_i$: feature value at observation $i$.

**Purpose:** Compute the centering value for standardization. **Conditions:** $N>0$ and included observations are defined. **Interpretation:** Sum all values and divide by their count. (Source: p. 63)

### MathML 7–9 — Inline Mean Symbols

The source separately encodes `$N$`, `$X_i$`, and `$i$` as MathML nodes to define the count, indexed observation, and index used in the mean and standard-deviation equations. They are not separate mathematical relationships. (Source: p. 63)

### MathML 10 — Inline Standard-Deviation Symbol

The source separately encodes `$\sigma$` as the feature's standard deviation and immediately defines it using MathML 11. (Source: p. 64)

### MathML 11 — Population Standard Deviation

$$
\sigma=\sqrt{\frac{1}{N}\sum_{i=1}^{N}(X_i-\mu)^2}.
$$

- $\sigma$: population standard deviation.
- $N$: number of observations.
- $i$: observation index.
- $X_i$: feature value for observation $i$.
- $\mu$: population mean.

**Purpose:** Compute the scale used in z-score standardization. **Conditions:** $N>0$; standardization additionally requires $\sigma>0$. **Interpretation:** Square root of the average squared deviation from the mean. The source deliberately uses divisor $N$, not the sample estimator's $N-1$. (Source: p. 64)

### Other Explicit Quantitative Rules

- Z-score outlier rule: $|Z|>2$ in the example; ±3 is also named as an alternative convention. (Source: p. 59)
- IQR: $IQR=Q_3-Q_1$; outliers lie below $Q_1-1.5IQR$ or above $Q_3+1.5IQR$. (Source: pp. 59–61)
- ADF decision: a statistic below the chosen critical value supports rejecting a unit root; p-values at or below 0.05 are used in the fractional-differencing search. (Source: pp. 64–69)
- Cointegration decision: the chapter uses p-value below 0.05 to reject no cointegration. (Source: pp. 72–73)
- Hurst regimes: $H<0.5$ mean-reverting, $H=0.5$ random-walk-like, $H>0.5$ persistent. (Source: p. 73)
- Correlation pruning: discard one of a pair when absolute correlation exceeds 0.9 in the examples. (Source: pp. 77–80)
- PCA selection: keep top $K$ eigenvectors until a desired cumulative explained variance, such as 90%, is reached. (Source: p. 81)
- Data splits: 70–80%/20–30% train/test or 60%/20%/20% train/validation/test. (Source: pp. 83–84)

## Methods and Procedures

### End-to-End Dataset Preparation

1. Collect relevant data from reliable providers.
2. Perform EDA with summaries and visualizations.
3. Locate missing values, outliers, duplicates, and inconsistencies.
4. Choose treatments based on the cause and meaning of each issue; evaluate their effects.
5. Engineer problem-relevant features.
6. Scale features where model sensitivity or unit disparities require it.
7. Test time-series features for stationarity and transform cautiously.
8. Test candidate asset relationships for cointegration and, where useful, mean reversion.
9. Remove irrelevant/redundant dimensions or transform them with PCA.
10. Divide observations into development and final-evaluation sets; use cross-validation where appropriate. (Source: pp. 53–86)

### Engle-Granger/Pairs-Screening Procedure

1. Test each candidate asset series for stationarity with ADF.
2. Apply the Engle-Granger test to non-stationary candidates.
3. Construct their spread or estimated linear combination.
4. confirm that the spread is stationary using its ADF statistic and p-value.
5. Optionally assess $H$ to characterize mean reversion.
6. Consider pairs-trading suitability only after the statistical relationship is supported. (Source: pp. 70–76)

### PCA Procedure

1. Standardize features.
2. Compute their covariance matrix.
3. Obtain covariance eigenvectors and eigenvalues.
4. Sort by explained-variance ratio and select top $K$.
5. Form the feature-vector matrix from selected eigenvectors.
6. Project standardized observations into component space. (Source: pp. 81–83)

## Examples

- Sweetviz general and gender-comparison reports for a synthetic demographic dataset. (Source: p. 54)
- Missing-value identification and three imputation families on 1,000 OHLCV rows. (Source: pp. 56–58)
- Three ways to detect 500 as an extreme price and three ways to treat it. (Source: pp. 58–61)
- Creation of 5- and 10-day moving-average features. (Source: pp. 61–62)
- MinMaxScaler and StandardScaler applied to three differently scaled features. (Source: pp. 62–64)
- Ordinary and fractional differencing of a synthetic random walk, evaluated by ADF. (Source: pp. 64–70)
- Engle-Granger, spread ADF, and Hurst analysis of synthetic pairs. (Source: pp. 70–76)
- Correlation pruning, random-forest importance, RFE, and two-component PCA. (Source: pp. 76–83)
- An 80/20 regression split and five-fold versus single-split Wine classification. (Source: pp. 83–86)

## Figures and Tables

The chapter has no formal tables and includes 13 figures:

1. **Figure 4.1:** Sweetviz dashboard summarizes Age, Income, Gender, and City without a comparison target. (Source: p. 54)
2. **Figure 4.2:** Sweetviz dashboard compares male and female subsets. (Source: p. 54)
3. **Figure 4.3:** Price box plot isolates 500 above the cluster near 100. (Source: pp. 58–59)
4. **Figure 4.4:** Original random-walk series visibly trends and fluctuates, illustrating non-stationarity. (Source: p. 66)
5. **Figure 4.5:** First-differenced series fluctuates without a sustained trend, illustrating stationarity. (Source: p. 66)
6. **Figure 4.6:** Original non-stationary series before fractional differentiation. (Source: p. 69)
7. **Figure 4.7:** Fractionally differenced series fluctuates around a stable level without a visible trend. (Source: p. 70)
8. **Figure 4.8:** Two individually non-stationary assets track a common path while their spread oscillates around a stable level. (Source: p. 72)
9. **Figure 4.9:** A second cointegrated pair with rising common trend and a stationary spread used for the Hurst example. (Source: pp. 75–76)
10. **Figure 4.10:** Heatmap shows strong Feature1–Feature2 redundancy and strong Feature1/Feature2 target relationships. (Source: p. 77)
11. **Figure 4.11:** Random-forest bar chart shows Feature1 near 0.985 importance and Feature3 near 0.015, supporting possible removal of Feature3. (Source: p. 78)
12. **Figure 4.12:** RFE selection indicator gives both Feature1 and Feature3 a value of 1 (selected); this is selection status, not graded importance. (Source: p. 80)
13. **Figure 4.13:** Scatterplot shows 100 observations projected onto the first two PCA axes; dispersion along each axis represents captured variation. (Source: pp. 82–83)

## Applications

- Build reliable historical training corpora for predictive trading models.
- Detect and responsibly treat corrupted, absent, or extreme market records.
- Create technical features such as rolling means.
- Prevent large-unit variables from dominating scale-sensitive models.
- Preserve time-series memory while achieving stationarity.
- Screen pairs for stable relative-value relationships and possible convergence trades.
- Reduce factor sets for interpretable, computationally manageable risk and portfolio models.
- Estimate model generalization using held-out data or cross-validation. (Source: pp. 53–86)

## Assumptions, Limitations, and Edge Cases

- Deletion can cause material data loss; imputation can alter distributions and must be evaluated. (Source: pp. 57–58)
- Numeric imputers in the examples cannot directly process the Date column. (Source: p. 57)
- Extreme financial observations may be genuine market events; automatic removal can erase important information. (Source: pp. 60–61)
- Min–max scaling fails for a constant feature because its range is zero and can be sensitive to extrema. The zero-range point is mathematically implied but not discussed explicitly. (Source: p. 62; limitation inferred)
- Standardization requires nonzero variance. Scale parameters should be learned without contaminating evaluation data; the chapter does not explicitly discuss leakage. (Source: pp. 63–64; limitation inferred)
- Ordinary differencing can destroy memory; fractional differencing introduces choices of order $d$, cutoff threshold, and window width. (Source: pp. 67–69)
- ADF and cointegration conclusions depend on specifications and significance thresholds; failure to reject is not proof that the null is true. (Source: pp. 64–73)
- Filtering non-positive spread values changes the Hurst sample and may affect the estimate; it is required only by the demonstrated logarithm-based routine. (Source: pp. 73–75)
- Correlation measures association, not causation, and linear correlation can miss nonlinear relevance. The latter is an inferred limitation. (Source: pp. 76–77)
- Random-forest importance and RFE are model- and sample-dependent. Correlated predictors can split or duplicate apparent importance. (Source: pp. 77–80)
- PCA components improve compactness but replace named features with linear combinations, reducing direct interpretability. (Source: pp. 80–83; tradeoff inferred)
- The generic shuffled split demonstrated is not time-aware. For chronological financial prediction, random shuffling may leak future information; the chapter does not supply a time-series split. (Source: pp. 83–85; critical edge case inferred)
- Cross-validation improves estimation stability but costs more computation and must also respect chronology for time-series applications. (Source: pp. 85–86; chronology caveat inferred)

## Common Mistakes and Warnings

- Trusting data without checking provider reliability, completeness, anomalies, and assumptions. (Source: pp. 53–55)
- Dropping every missing or extreme observation without examining its cause or informational value. (Source: pp. 57–61)
- Imputing dates with numeric-only example pipelines or failing to compare imputed and original distributions. (Source: pp. 57–58)
- Allowing scale-sensitive algorithms to overweight variables merely because their units are larger. (Source: pp. 62–64)
- Treating a non-stationary series as stable or over-differencing until its predictive memory disappears. (Source: pp. 64–70)
- Calling two assets cointegrated merely because their charts look similar; the spread/linear combination must be tested. (Source: pp. 70–73)
- Reading a p-value as the probability that the null is true; the chapter defines it conditionally on the null. (Source: p. 73)
- Running feature importance or RFE without first addressing strong predictor redundancy. (Source: pp. 77–80)
- Applying PCA before standardization. (Source: p. 81)
- Using test data for tuning, or confusing hyperparameters with learned parameters. (Source: p. 83)
- Overinterpreting a perfect single train/test result; the Wine example explicitly flags possible overfitting. (Source: p. 86)

## Key Takeaways

- Dataset preparation is a modeling stage, not clerical cleanup: it determines reliability and generalization. (Source: p. 53)
- EDA should precede transformations so remedies respond to observed data properties. (Source: pp. 53–55)
- Missing values and outliers require cause-aware treatment and post-treatment evaluation. (Source: pp. 55–61)
- Scaling, stationarity transformations, and feature selection must match the algorithm and financial meaning. (Source: pp. 61–83)
- Cointegration concerns a stationary combination of non-stationary series; low Hurst values further suggest mean reversion. (Source: pp. 70–76)
- Redundancy control, model importance, RFE, and PCA solve related but distinct dimensionality problems. (Source: pp. 76–83)
- Held-out testing and cross-validation estimate unseen performance; a strong isolated score can still be misleading. (Source: pp. 83–86)

## Glossary

| Term | Definition | Source |
|---|---|---|
| EDA | Statistical and visual exploration used to understand data, anomalies, and assumptions. | pp. 53–54 |
| Imputation | Replacement of missing observations using statistics or models. | p. 57 |
| MICE | Multivariate imputation by chained regression equations. | p. 57 |
| Outlier | Observation unusually distant from the rest of a distribution. | pp. 58–59 |
| IQR | Difference between third and first quartiles. | p. 59 |
| Feature engineering | Transformation or creation of inputs to better represent a learning problem. | pp. 61–62 |
| Normalization | Min–max scaling, commonly to the interval 0–1. | p. 62 |
| Standardization | Centering and scaling to mean zero and standard deviation one. | pp. 63–64 |
| Stationarity | Stability of mean, variance, and autocorrelation over time. | p. 64 |
| ADF test | Unit-root test used to assess stationarity. | pp. 64–65 |
| Fractional differentiation | Differencing with fractional order to balance stationarity against memory preservation. | pp. 67–70 |
| Cointegration | Stationary linear combination among otherwise non-stationary series. | p. 70 |
| Engle-Granger test | Procedure used to test time-series cointegration. | p. 70 |
| p-value | Under a true null, probability of results at least as extreme as observed. | p. 73 |
| Hurst coefficient | Number from 0 to 1 describing mean reversion, randomness, or persistence. | p. 73 |
| Pairs trading | Market-neutral long/short strategy seeking profit from convergence of cointegrated securities. | p. 73 |
| Feature selection | Retention of useful predictors and removal of irrelevant/redundant ones. | p. 76 |
| RFE | Recursive feature elimination, which repeatedly removes least-important predictors and refits. | pp. 78–80 |
| Dimensionality | Number of features in a dataset. | p. 80 |
| PCA | Projection onto ordered, uncorrelated linear components that capture variance. | pp. 81–83 |
| Explained variance ratio | Fraction of total variance captured by a principal component. | p. 81 |
| Overfitting | Memorizing training details/noise at the expense of unseen performance. | p. 83 |
| Underfitting | Model simplicity that fails to represent the underlying pattern. | p. 83 |
| Hyperparameter | Preset setting controlling learning rather than learned from the training data. | p. 83 |
| Stratification | Splitting that preserves class proportions. | p. 85 |
| Cross-validation | Repeated training/evaluation across multiple data folds. | pp. 85–86 |

## Connections to Other Chapters

- This stage follows Chapter 3's problem definition: the target, market universe, horizon, and hypothesis determine which data and features should be prepared. (Source: p. 53; connection inferred from opening sequence)
- Its cleaned, transformed, selected, and partitioned outputs feed later model construction, tuning, and evaluation stages. (Source: pp. 53, 83–86; connection inferred)

## Extraction Issues

- The XHTML was complete and readable, with print anchors spanning pages 53–86.
- All 11 MathML nodes were accounted for. Seven are isolated inline symbols supporting definitions; four are substantive displayed/inline equations. No external equations were added to replace them.
- All 13 referenced figure assets were accounted for. Selected assets were visually checked where their charts conveyed details beyond captions.
- Figure 4.11's image alt text says Feature3 is approximately 0.001, while the printed numeric output and visible bar indicate 0.015222; this extraction uses the numeric output and visible figure. (Source: p. 78)
- Figure 4.12 plots binary RFE selection flags, although the caption calls it an “importance” plot; this extraction distinguishes selection status from graded importance. (Source: p. 80)
- The prose gives one set of ADF critical values near Figure 4.8 that differs slightly from the immediately preceding printed output. Both support the same conclusion, but exact values should be taken from the relevant test output. (Source: pp. 72–73)
- The source refers to “differentiating” in places where standard time-series terminology is “differencing.” The extraction uses the conventional term while preserving the method's meaning.
