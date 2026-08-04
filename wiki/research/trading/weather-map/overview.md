# Multiframe Forecasting Weather Map

Status: in progress

Portfolio state: **horizon — parked**

Purpose: preserve Destin's concept for a continuously updated, probabilistic map of future price paths across multiple timeframes and forecast horizons. This is a long-horizon research program, not a current implementation contract or funded Linear project.

Related: [[research/trading/research_index|Research Board]], [[research/trading/quantile_regression/qr-trading-reference|Quantile Regression Trading Reference]], [From Position Targets to Transition Kernels](../../../../raw/research/concepts/from-position-targets-to-transition-kernels.md)

Visual inspiration: [Jane Street polyhedral puzzle](../../../../raw/research/concepts/polyhedral-desktop-DJBYbhaC.jpg)

## Core idea

Run probabilistic forecasting models across a grid of timeframes and forward horizons.

Initial example:

- timeframes: `1m`, `5m`, `15m`, `30m`, `1h`, `4h`, `1d`
- horizons per timeframe: `1`, `2`, `3`, `4`, `5`
- each timeframe's forecasts update when its next respective candle completes
- each predicted price carries a confidence or probability assessment

At a snapshot time `t₀`, the system therefore holds a multiscale view of possible future price paths. A simplified surface might contain:

```text
                    horizon
timeframe       1       2       3       4       5
1m           98.7    98.8    99.0    99.1    99.2
5m           99.1    99.9   100.25  101.0   101.5
1h          102.0   101.0   100.0   100.5   101.5
```

The `1m` row reaches five minutes forward, the `5m` row reaches twenty-five minutes forward, and the `1h` row reaches five hours forward. The actual output is probabilistic rather than a bare point-price matrix.

## Forecast node

A forecast can be represented conceptually as a node containing at least:

```text
(
  snapshot_time,
  source_timeframe,
  horizon_steps,
  target_time,
  predicted_price_or_distribution,
  confidence,
  last_update_time
)
```

The exact predictive model is not fixed. Quantile regression is the initial example because it naturally produces a distribution or interval rather than only a point estimate.

## Weather Map

Plotting the nodes together produces a changing surface or graph of future price possibilities:

- each timeframe contributes a forecast path at its own update rate;
- each horizon places a node at a future wall-clock time;
- confidence can control visual weight, opacity, width, color, or uncertainty bands;
- the combined view shows the current shape, agreement, divergence, and branching of expected paths.

The name comes from televised storm-path maps: multiple future locations form a probabilistic path or cone that updates as new observations arrive. It also resembles an options gamma map that shows how exposure is expected to transform across different price paths.

## Graph and traversal hypothesis

Once forecasts are represented as nodes, the system may model possible traversal through the forecast graph rather than treating every prediction independently.

Potential edge families include:

- agreement across timeframes at the same or nearby wall-clock target;
- short-horizon paths converging toward or diverging from longer-horizon paths;
- changes in the probability of moving from one forecast region to another;
- branch formation, collapse, or reversal as new candles update only part of the map;
- trading policies conditioned on both the expected path and the confidence/topology of alternatives.

This relates to the Jane Street-inspired transition-topology concept: behavior may be understood through flows between connected states, not only isolated state values. The precise graph topology and traversal law are not yet defined.

## Why it might matter

The working thesis is that a full multiscale picture of probable price paths can expose more profitable and distinctive trading opportunities than a single signal, timeframe, or forecast horizon.

Possible uses include:

- directional conviction from cross-timeframe agreement;
- conflict-aware position sizing when near- and long-horizon paths disagree;
- entries and exits based on expected path shape rather than a one-step forecast;
- dynamic holding-period selection;
- regime recognition from changes in the forecast surface;
- path-aware risk and scenario management.

These are hypotheses, not validated findings.

## Unresolved definitions

Do not implement by guessing these:

- **Forecast target:** price level, return, distribution, quantiles, or another state variable.
- **Confidence:** probability within a tolerance, calibrated interval coverage, model uncertainty, directional accuracy, or another definition.
- **Cross-timeframe coherence:** how forecasts with the same wall-clock target but different source timeframes should agree, compete, or combine.
- **Graph edges:** temporal adjacency, shared target time, path compatibility, learned transition probability, or another relationship.
- **Traversal:** observed realized-price movement, probabilistic scenario propagation, a trading policy's chosen route, or all three as separate objects.
- **Update semantics:** what remains fixed and what is recomputed when only one timeframe closes a new candle.
- **Trading mapping:** how the forecast graph changes entries, exits, sizing, risk, and holding periods.
- **Evaluation:** proper scoring rules, calibration, path accuracy, economic value, and baselines.

## Natural first decomposition when resumed

1. Forecast one target variable on one asset across the timeframe × horizon grid.
2. Validate each node's out-of-sample accuracy and confidence calibration independently.
3. Test coherence where different timeframe/horizon pairs forecast the same future wall-clock time.
4. Define and visualize a minimal graph without trading it.
5. Compare graph-derived features with the best individual forecast baselines.
6. Only then define a traversal-aware trading policy and test its incremental economic value.

## Resume condition

Resume when Money Machine chooses multiframe probabilistic forecasting as a funded research direction and can define:

- the first deployment target and asset;
- the forecast target and confidence/calibration contract;
- a minimal baseline model;
- the first graph relationship to test;
- the data, compute, and evaluation budget;
- what current work it displaces.

Until then, preserve this as horizon research. Do not create Linear execution or infer a complete model from this concept page.
