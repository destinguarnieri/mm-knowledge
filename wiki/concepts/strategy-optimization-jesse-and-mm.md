# Strategy Optimization: Jesse Mechanics and Money Machine Design

Status: draft

Purpose: record exactly how Jesse currently searches strategy parameters, identify the useful mechanics independent of Jesse's platform, and specify a Money Machine version that treats optimization as bounded search plus robustness testing rather than as a machine for finding the highest historical score.

Related: [[concepts/supervised-trading-labels|Supervised Trading Labels]], [[research/trading/research_process_v2|Research Process V2]], [[trading/pmax|P_Max]]

Source snapshot: Jesse `master` at commit [`d53f6d1`](https://github.com/jesse-ai/jesse/tree/d53f6d16446e61284f7d0ad297dfb5a70b1d1ae0), reviewed 2026-08-30. The implementation may change after this commit.

## Executive read

Jesse's current optimization mode is a bounded, parallel random search around repeated strategy backtests:

```text
declare parameter ranges
        ↓
sample one random parameter configuration
        ↓
backtest it on the training period
        ↓
calculate training fitness
        ↓
backtest viable configurations on the testing period
        ↓
store and rank the completed trial
```

Jesse imports Optuna and creates an Optuna study, but Optuna does not generate the candidate parameters. Jesse samples parameters directly with NumPy and adds the completed result to Optuna afterward. Ray supplies parallel execution. In this implementation, Optuna is principally a trial schema, persistence layer, and best-trial index—not the search algorithm.

This is separate from supervised model training. Optimization searches control settings by evaluating complete strategy runs. Supervised training fits a function from point-in-time features to later-resolved labels. An optimizer can wrap a supervised pipeline, but it does not replace the feature/label/model-fitting lifecycle described in [[concepts/supervised-trading-labels|Supervised Trading Labels]].

## Part I — What exactly Jesse is doing

### 1. The strategy declares the search space

A Jesse strategy implements `hyperparameters()` and returns parameter specifications. Supported forms are:

- integer: `name`, `min`, `max`, `default`, and optional `step`;
- float: `name`, `min`, `max`, `default`, and optional `step`;
- categorical: `name`, `options`, and `default`.

The selected values are injected into the running strategy through `self.hp`. A categorical parameter can therefore select not only a numeric value but also a rule or indicator family.

Source: [Jesse hyperparameter documentation](https://docs.jesse.trade/docs/optimize/hyperparameters).

### 2. The trial budget grows with the number of parameters

Jesse calculates:

```text
total trials = number of declared hyperparameters × configured trials
```

With three declared parameters and the default `trials = 200`, Jesse evaluates 600 complete configurations. This multiplication is a Jesse convention; it is not required by Optuna or by random search.

Source: [`Optimizer.__init__`](https://github.com/jesse-ai/jesse/blob/d53f6d16446e61284f7d0ad297dfb5a70b1d1ae0/jesse/modes/optimize_mode/Optimize.py#L80-L149).

### 3. Jesse independently samples every trial

For each configuration, Jesse uses NumPy to draw:

- an integer uniformly from its permitted values;
- a float uniformly from its interval or permitted step values;
- a categorical option uniformly from its list.

The generator does not call `trial.suggest_int`, `trial.suggest_float`, `study.ask`, or `study.optimize`. A successful earlier trial therefore does not affect where the next trial searches.

Source: [`Optimizer._generate_trial_params`](https://github.com/jesse-ai/jesse/blob/d53f6d16446e61284f7d0ad297dfb5a70b1d1ae0/jesse/modes/optimize_mode/Optimize.py#L226-L259).

### 4. Ray runs independent backtests in parallel

The training candles, testing candles, routes, configuration, and parameter specification are placed into Ray's shared object store. Jesse maintains up to approximately twice as many outstanding trial tasks as allocated CPU cores, while each task requests one CPU.

Each task receives one complete parameter dictionary and calls the same fitness function. This is embarrassingly parallel because candidate generation does not depend on previously completed trials.

Source: [`ray_evaluate_trial` and `Optimizer.run`](https://github.com/jesse-ai/jesse/blob/d53f6d16446e61284f7d0ad297dfb5a70b1d1ae0/jesse/modes/optimize_mode/Optimize.py#L24-L76).

### 5. Fitness comes entirely from the training backtest

The parameter configuration is first backtested on the training candles. It is eligible only when the training result contains more than five trades.

Jesse then selects one configured training metric and normalizes it against a fixed range:

| Objective | Normalization range |
| --- | ---: |
| Sharpe | `-0.5` to `5` |
| Calmar | `-0.5` to `30` |
| Sortino | `-0.5` to `15` |
| Omega | `-0.5` to `5` |
| Serenity | `-0.5` to `15` |
| Smart Sharpe | `-0.5` to `5` |
| Smart Sortino | `-0.5` to `15` |

A negative raw objective is assigned the minimum fitness `0.0001`. Otherwise, the final score is:

```text
trade_count_factor = min(
    log10(training_trade_count) / log10(optimal_total),
    1
)

fitness = trade_count_factor × normalized_training_objective
```

`optimal_total` is therefore not an optimum found by the search. It is a user-supplied target controlling how quickly the trade-count factor reaches full credit. The trade count is a rough evidence-volume adjustment, not an independence or uncertainty estimate.

Source: [`get_fitness`](https://github.com/jesse-ai/jesse/blob/d53f6d16446e61284f7d0ad297dfb5a70b1d1ae0/jesse/modes/optimize_mode/fitness.py#L23-L108).

### 6. The testing period is measured but does not affect ranking

If the training configuration has more than five trades and a nonnegative objective, Jesse runs the same configuration over the testing candles. It returns both sets of metrics to the dashboard.

The testing metrics are not included in `fitness`. Candidate ordering and the top-candidate list use only the training score. Test performance is presented for human comparison.

This makes the testing period algorithmically out of sample, but not necessarily procedurally untouched. If a person repeatedly sees those test results and uses them to choose parameters or change the search, the period has become a validation surface. Jesse's own documentation consequently recommends a third period that is not used during optimization.

Sources: [fitness implementation](https://github.com/jesse-ai/jesse/blob/d53f6d16446e61284f7d0ad297dfb5a70b1d1ae0/jesse/modes/optimize_mode/fitness.py#L79-L102), [Jesse overfitting guidance](https://docs.jesse.trade/docs/optimize/overfitting).

### 7. Optuna records the completed random trial

After the backtests finish, Jesse constructs the appropriate Optuna distribution objects, creates a completed `FrozenTrial` containing the already-selected parameters and score, and adds it to the study. Training and testing metrics are stored as trial user attributes.

The dashboard version persists the study in SQLite and uses Optuna to recover `best_trial`. The research/notebook version creates an in-memory study but explicitly states that random sampling occurs directly outside it.

There is no active Optuna sampler feedback loop and no Optuna pruning loop in the reviewed implementation.

Sources: [`Optimizer._create_optuna_trial`](https://github.com/jesse-ai/jesse/blob/d53f6d16446e61284f7d0ad297dfb5a70b1d1ae0/jesse/modes/optimize_mode/Optimize.py#L261-L314), [research optimizer](https://github.com/jesse-ai/jesse/blob/d53f6d16446e61284f7d0ad297dfb5a70b1d1ae0/jesse/research/optimize/__init__.py).

### 8. DNA is serialized configuration, not genetic search

For a viable trial, Jesse sorts the parameter dictionary as JSON and base64-encodes it. The resulting DNA string can restore the configuration in the dashboard. It does not imply mutation, crossover, or a genetic algorithm.

Source: [Jesse DNA documentation](https://docs.jesse.trade/docs/optimize/dna-usage).

## What Jesse's random search gets right

Random search has useful properties here:

- trials are independent and easy to distribute;
- it gives broad global coverage without following each early historical winner;
- it handles mixtures of continuous, integer, and categorical controls;
- its search behavior is simpler to audit than an adaptive sampler;
- it supplies a necessary baseline for determining whether a more complex optimizer adds value.

Those properties matter in trading because the objective is noisy and nonstationary. Adaptive search can efficiently concentrate around a historical accident. Random search does not solve data snooping—the best of many random trials is still selected from many hypotheses—but it does not add an additional feedback mechanism that steers later trials toward the same apparent accident.

Jesse leaves several useful controls unspecified:

- no seed is supplied to NumPy, so the sampled set is not reproducible by configuration alone;
- uniform random draws can leave uneven coverage and duplicate effectively similar configurations;
- no budget-matched search baseline is reported;
- the leaderboard favors one scalar training maximum rather than a stable parameter neighborhood;
- testing output is visible during the run, permitting human-driven reuse of the testing period;
- the trial count is tied to parameter count rather than the size, geometry, and cost of the search space.

## Part II — How Money Machine should do it

### Objective

Optimization should answer:

> Which bounded configuration or configuration region generalizes well enough to justify the next economic test?

It should not answer only:

> Which configuration produced the highest score anywhere in the history we searched?

The process inherits the discovery, validation, untouched-holdout, cost, and search-budget rules from [[research/trading/research_process_v2|Research Process V2]]. Optimization produces candidates; protected evidence decides whether they advance.

### 1. Freeze the object being optimized

Before search begins, record:

- the strategy or model family;
- the portable signal definition;
- market-specific capture and execution rules;
- feature and label specifications when supervised learning is involved;
- core parameters that may be searched;
- incidental implementation values that remain fixed;
- discovery, validation, and one-time holdout boundaries;
- realistic and stress cost assumptions;
- minimum evidence and risk constraints;
- total search budget across humans, agents, manual runs, random trials, and adaptive trials.

Changing the signal, label resolver, execution semantics, or evaluation metric after results are visible creates a new hypothesis. It must be versioned and must not inherit the earlier claim's untouched validation status.

### 2. Establish baselines before adaptive search

Every optimization begins with:

1. the declared default or economically meaningful configuration;
2. simple hand-selected anchors;
3. a preregistered random, quasi-random, or coarse-grid search budget;
4. an appropriate null or random-entry control where signal validity is at issue.

The broad search is not merely a warm-up. It reveals whether the parameter surface contains a plateau, cliffs, interactions, dead regions, or several distinct mechanisms. It also becomes the budget-matched baseline against which Optuna must demonstrate incremental value.

Quasi-random coverage is preferable to naive random draws when the space is continuous and fixed because it fills the space more evenly while preserving parallel evaluation. Ordinary random search remains appropriate for conditional, irregular, or rapidly changing spaces.

### 3. Score only out-of-fold development results

A configuration must not receive fitness from the observations used to fit its model or choose its internal state. Divide the development history into chronological folds. Within each fold:

```text
fit or initialize on the fold's earlier training segment
        ↓
make decisions on its later validation segment
        ↓
simulate those decisions with fixed costs and execution semantics
        ↓
record fold-level utility and guardrail metrics
```

For a non-ML strategy, “fit” may mean only applying the proposed static parameters. For an ML strategy, preprocessing and the estimator are fitted using the fold's training observations only. Overlapping forward labels require purging or an equivalent boundary that prevents a training label from resolving inside the validation interval.

The optimizer receives a preregistered robust aggregation of the validation-fold results—not in-sample training performance. The exact utility is project-specific, but the pattern is:

```text
if any hard validity, evidence, cost, or risk constraint fails:
    trial is ineligible
else:
    fitness = robust aggregation of validation-fold utility
```

A median, lower quantile, worst-fold-aware value, or median-minus-dispersion score is generally more aligned with robustness than the single pooled maximum. The chosen aggregation must be frozen before results are examined.

### 4. Use Optuna as an optional second-stage search

After broad coverage establishes that refinement is justified, Optuna may propose additional configurations inside the development surface:

```text
Optuna asks for a configuration
        ↓
Money Machine evaluates all required development folds
        ↓
Money Machine returns the frozen robust fitness
        ↓
Optuna updates its sampler
```

Requirements:

- select and record the sampler explicitly;
- record sampler and model seeds;
- keep the adaptive trial budget fixed;
- retain every completed, failed, and pruned trial;
- compare its results with the budget-matched broad-search baseline;
- do not expose validation or holdout data to the sampler;
- do not claim value from Optuna unless its selected region generalizes better than the broad-search baseline.

TPE is reasonable for a mixed or conditional search space when trials are expensive and sequential feedback is useful. Random or quasi-random search remains reasonable when trials are cheap, parallelism is abundant, or the objective is too noisy to support local adaptation.

Early pruning should be used only when the intermediate resource axis is meaningful. Training epochs may support pruning for some ML models. The first months of a trading backtest are not automatically a valid “early step”: pruning on them can prefer the regime that happens to occur first.

### 5. Select a region, not `best_trial`

The primary output is a shortlist of stable neighborhoods. A candidate should have:

- acceptable adjacent parameter values rather than one isolated spike;
- acceptable results across chronological development folds;
- no dependence on one asset, regime, or small set of trades unless that scope was explicit;
- acceptable realistic-cost results and understood stress-cost behavior;
- consistent results across required seeds for stochastic models;
- a defensible mechanism for why the setting matters.

The exact historical maximum is evidence of where the search found an extreme. It is not automatically the configuration to deploy. A representative point from a broad plateau may be preferable.

### 6. Consume validation and holdout deliberately

After development search:

1. Evaluate only the frozen shortlist on the separate validation period.
2. Select or reject candidates under preregistered rules.
3. If the validation result causes another parameter or rule change, reclassify that period as development and obtain fresh validation surface.
4. Run the chosen, locked configuration once on the untouched holdout at the applicable promotion gate.
5. Advance surviving candidates through shadow execution and an explicitly authorized small live canary.

No optimizer receives holdout feedback. No manual search receives holdout feedback. A one-time holdout is evidence, not another optimization fold.

### 7. Supervised model and label search is nested

When optimization wraps labeled training, each outer trial may propose bounded values such as:

- estimator hyperparameters;
- feature-set switches;
- decision-probability thresholds;
- fixed-horizon length or barrier widths, if label-definition search was explicitly authorized;
- capture and risk controls.

For every proposed configuration and chronological development fold:

```text
construct training labels from the trial's frozen label specification
fit transformations on training features only
fit the estimator on X_train and y_train
predict later validation observations
apply the frozen decision and execution mapping
calculate net validation utility
```

Searching label parameters changes the target dataset itself. Such a trial is not merely tuning a classifier; it is comparing different prediction problems. Its label specification, class balance, overlap, resolution horizon, and sample count must be stored and its outer validation boundary must remain protected.

### 8. Preserve a complete trial record

Every trial record should retain or point to:

- full parameter dictionary and search-space version;
- strategy, feature, label, and execution specification IDs;
- discovery folds, validation period, and holdout identity;
- realistic and stress cost configurations;
- engine and code version;
- data snapshot or dataset version;
- sampler, sampler seed, model seed, and trial number;
- status: completed, failed, pruned, or ineligible, with reason;
- persisted backtest `run_id` values for metric retrieval;
- aggregate fitness definition and value;
- membership in a stable neighborhood or isolated peak.

Persisted run IDs remain the metric source of truth. The wiki records intent, assumptions, interpretation, decisions, and run pointers—not duplicated result grids.

## Side-by-side contract

| Dimension | Jesse at reviewed commit | Money Machine version |
| --- | --- | --- |
| Candidate generation | Independent NumPy random draws | Broad grid/random/quasi-random coverage; optional adaptive refinement |
| Optuna role | Completed-trial storage and best-trial lookup | Actual candidate proposal plus trial ledger when adaptive refinement is justified |
| Trial execution | Ray-parallel full backtests | Parallel where valid; sequential feedback only when the selected sampler benefits |
| Trial budget | Parameters × configured trial count | Preregistered cumulative budget based on search geometry, cost, and evidence risk |
| Fitness data | Training-period backtest | Chronological out-of-fold development results |
| Fitness | Normalized ratio × trade-count factor | Frozen robust aggregation after hard evidence/cost/risk gates |
| Testing data | Evaluated for each viable trial but excluded from score | Separate validation used only for a frozen shortlist |
| Final holdout | Recommended third period | Explicit one-time promotion evidence, invisible to optimizer and manual selection |
| Selection target | Highest training fitness | Stable neighborhood with fold, cost, regime, and seed robustness |
| ML handling | Strategy-dependent; optimizer itself does not train from labels | Nested fit/predict/backtest evaluation with time-safe labels and preprocessing |
| Search accounting | Current session trial count | Whole-project count across automated and manual configurations |
| Output | Ranked trials, metrics, and base64 DNA | Auditable shortlist, stability interpretation, run pointers, and promote/reject decision |

## Current maturity

The Jesse section is a source-faithful description of the reviewed commit. The Money Machine section is a proposed optimization contract aligned with Research Process V2; it has not yet been confirmed through an implementation or a completed optimization campaign.
