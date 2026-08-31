# Supervised Trading Labels

Status: draft

Purpose: explain the mechanical contract that turns future market outcomes into supervised-learning targets without leaking those outcomes into model inputs. This is framework-independent; Jesse is one concrete reference implementation, not the concept itself.

Related: [[research/trading/research_process_v2|Research Process V2]], [[concepts/strategy-optimization-jesse-and-mm|Strategy Optimization: Jesse Mechanics and Money Machine Design]], [[concepts/reinforcement-learning-trading-mechanics-ziad-francis-GPT|RL Trading Mechanics — Ziad Francis (GPT)]]

## Core idea

A supervised trading example pairs:

- `x_t`: features observable at an observation or decision time `t`;
- `y_t`: the answer that becomes knowable only after the relevant future path or trade outcome resolves.

The model trains on many completed pairs `(x_t, y_t)`. The future is allowed to determine the historical answer `y_t`; it must not appear inside the feature vector `x_t`.

```text
At time t:
    observe features x_t
    open an unfinished example

During t+1 ... t+H:
    observe the future path or decision outcome

When the outcome resolves:
    attach label y_t to the original x_t
    store the completed pair (x_t, y_t)

After many completed examples:
    X = feature rows
    y = resolved labels
    model.fit(X_train, y_train)
```

## One example lifecycle

At the observation time:

```python
pending = {
    "observed_at": t,
    "features": {
        "atr_pct": 0.012,
        "ema_ratio": 0.018,
        "rsi_centered": -0.24,
    },
    "label": None,
}
```

Suppose the upper price barrier is reached seven bars later. The original observation is then finalized:

```python
completed = {
    "observed_at": t,
    "resolved_at": t + 7,
    "features": pending["features"],
    "label": 1,
}
```

The row means: *given the information observable at `t`, the upper-barrier outcome subsequently occurred.* It does not mean the model was shown the next seven bars.

Repeating the lifecycle produces a labeled dataset:

| Features observed at `t` | Future label |
| --- | ---: |
| ATR 0.012, EMA ratio +0.018, RSI -0.24 | `+1` |
| ATR 0.031, EMA ratio -0.011, RSI +0.47 | `-1` |
| ATR 0.009, EMA ratio +0.001, RSI +0.03 | `0` |

## From labeled rows to a trained model

The completed observations are ordered by their observation time and converted into a feature matrix `X` and target vector `y`:

```python
X = [row["features"] for row in completed_observations]
y = [row["label"] for row in completed_observations]
```

Training then follows this sequence:

1. Split observations chronologically into training and later evaluation periods.
2. Fit any required feature transformations on the training period only.
3. Transform training and evaluation features using the fitted transformation.
4. Fit the estimator on `X_train` and `y_train`.
5. Evaluate predictions against the untouched `y_test` outcomes.

For a random-forest classifier, training builds many decision trees whose feature splits increasingly separate the historical label classes. A current feature vector is passed through the fitted trees; their votes produce estimated class probabilities. With triple-barrier labels, the learned object is approximately:

```text
P(first barrier outcome | features observable now)
```

For regression, the same lifecycle uses a continuous label. The learned object is approximately a conditional value such as:

```text
E(forward return | features observable now)
```

## Common label resolvers

The observation lifecycle stays the same; the rule that resolves `y_t` changes.

### Fixed-horizon outcome

Wait `H` bars and label the original observation with a future quantity such as log return:

```text
y_t = log(price[t + H] / price[t])
```

The continuous value can train a regressor. Its sign or thresholded bins can instead train a classifier.

### First-barrier outcome

Anchor an upper price barrier, lower price barrier, and maximum time horizon at `t`. Resolve the label from the first barrier reached:

- `+1`: upper barrier first;
- `-1`: lower barrier first;
- `0`: time horizon first.

This trains a model on a path outcome: which event occurs first, not merely the price at one fixed future timestamp.

### Primary-signal outcome (meta-label)

A primary rule or model supplies the proposed side or decision. Record features when that signal fires, then label whether the proposed decision succeeds under its defined outcome rule:

- `1`: take or retain the proposed decision;
- `0`: pass, veto, or reduce it.

The resulting model does not need to rediscover direction. It learns the conditional success of a specific primary signal.

## Minimum record contract

A reusable labeled observation should retain at least:

- `observed_at`: when the features were knowable;
- `resolved_at`: when the answer became knowable;
- `features`: the values available at `observed_at`;
- `label`: the resolved historical answer;
- `feature_spec_id`: the versioned feature definition;
- `label_spec_id`: the versioned outcome, horizon, threshold, and barrier definition;
- optional `side`, `signal_id`, or `event_id` when the label is conditional on a primary decision.

The two timestamps are load-bearing. They distinguish information time from answer time and make chronological splitting and overlap handling possible.

## Invariants

1. Features contain only information available at `observed_at`.
2. A label may use later information because it is the historical answer, never an inference-time input.
3. The label definition fixes the outcome, horizon, thresholds, and conditioning signal before fitting.
4. Training and evaluation are separated through time.
5. Changing the feature definition, label resolver, horizon, barriers, or primary signal creates a different dataset specification.

## Provenance and current maturity

This page synthesizes mechanics that were previously scattered across raw external extracts. It explains a reusable concept; it does not confirm that any particular label contains tradable information.

Raw sources:

- [Problem definition: features and target variables](../../raw/research/book-extracts/hands-on-ai-trading/03-step-1-problem-definition.md)
- [Model choice, fitting, and evaluation](../../raw/research/book-extracts/hands-on-ai-trading/05-step-3-model-choice-training-and-application.md)
- [Time-safe forward-label alignment](../../raw/research/book-extracts/hands-on-ai-trading/06-applied-machine-learning.md)
- [Corrective AI and conditional forward-outcome rows](../../raw/research/book-extracts/hands-on-ai-trading/08-ai-for-risk-management-and-optimization.md)
- [Meta-labeling research framing](../../raw/research/book-extracts/hands-on-ai-trading/classification-07-09.md)
- [Forecasts paired with subsequent risk-adjusted returns](../../raw/research/book-extracts/advanced-futures-trading/chapters/12-adjusted-trend.md)

External implementation references:

- [Jesse feature/label recording lifecycle](https://github.com/jesse-ai/jesse/blob/master/jesse/strategies/Strategy.py)
- [Jesse `X`/`y` construction and estimator fitting](https://github.com/jesse-ai/jesse/blob/master/jesse/research/ml.py)
- [Triple-barrier example](https://github.com/saleh-mir/triple-barrier)
