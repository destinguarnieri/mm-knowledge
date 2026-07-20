---
name: EMA Stats Pattern Trail
overview: Capture the current image-led hypotheses before further questioning, then convert only the surviving patterns into a bounded causal experiment. No strategy or runtime changes are implied by this plan.
todos:
  - id: lock-chart-context
    content: Confirm the screenshot asset, timeframe, rendered lookback, and exact plotted component identities.
    status: pending
  - id: formalize-events
    content: Translate the visual patterns into causal, non-overlapping event labels and falsifiable predictions.
    status: pending
  - id: test-incremental-information
    content: Measure whether rolling surprise or magnitude state adds information beyond zero crossing and signal slope.
    status: pending
  - id: bound-combined-control
    content: Specify and hold out-test the smallest combined timing-and-exposure control only if incremental information survives.
    status: pending
isProject: false
Model: GPT 5.6 Sol Medium
Skill: None
---

# EMA Signal-Stats Pattern Trail

## Decision this research should eventually support
Determine whether magnitude statistics, signed rolling statistics, or a deliberately combined control can monetize the EMA 10/200 signal's directional information better than static flip-only behavior—especially by improving transition timing and profit retention without introducing unstable path dependence.

## Evidence currently in hand
- Three screenshots of the same asset, time series, and raw signal: [magnitude_stats.png](/Users/destinguarnieri/Desktop/codebase/mm-knowledge/wiki/research/trading/emac-cross-10-200/magnitude_stats.png), [mag_asym_stats.png](/Users/destinguarnieri/Desktop/codebase/mm-knowledge/wiki/research/trading/emac-cross-10-200/mag_asym_stats.png), and [rolling_stats.png](/Users/destinguarnieri/Desktop/codebase/mm-knowledge/wiki/research/trading/emac-cross-10-200/rolling_stats.png).
- Magnitude mode in [sig_extension.py](/Users/destinguarnieri/Desktop/codebase/mm_v04/backend/app/lib/indicators/sig_extension.py) supports both symmetric zero-centered bands from `abs(signal)` and separate positive/negative envelopes.
- Rolling mode in [sig_stats.py](/Users/destinguarnieri/Desktop/codebase/mm_v04/backend/app/lib/indicators/sig_stats.py) computes signed rolling mean and standard-deviation bands.
- Both are emitted for visual inspection by [emac_v4.py](/Users/destinguarnieri/Desktop/codebase/mm_v04/backend/app/backtest/strategies/emac_v4.py); neither currently changes trading decisions.
- The durable strategy context remains [emac-cross-10-200.md](/Users/destinguarnieri/Desktop/codebase/mm-knowledge/wiki/research/trading/emac-cross-10-200/emac-cross-10-200.md): direction appears informative, while flip-only monetization gives back favorable excursions.

## Current observations
1. Rolling statistics appear to measure **surprise relative to the recent signed regime**. Reversals around the visually strongest expansions become exceptional while the distribution still reflects the prior sign.
2. Magnitude statistics appear to measure **absolute directional force**. Their symmetric bands retain cross-direction comparability but do not encode whether a move is novel relative to the preceding regime.
3. Signal peaks align more closely with price acceleration than final price extrema. Price often continues after signal magnitude begins declining, so a high-magnitude event is not automatically an exhaustion or fade event.
4. A recurring visual phase sequence is: envelope contraction → sign reversal/rolling surprise → price expansion → rolling-band adaptation → signal decay during trend continuation or consolidation.
5. At the right edge, rolling context makes the positive turn look relatively novel while magnitude context makes it look moderate in absolute force: a possible early re-acceleration state, not yet a strong-force state.
6. Asymmetric magnitude exposes **directional memory** that the other views hide. During sustained negative activity the lower envelope expands while the upper envelope contracts, and vice versa during positive activity.
7. The first impulse in a dormant direction naturally appears exceptional against its compressed same-side envelope. Continued same-sign activity then expands that envelope, separating directional shock from regime acceptance.
8. On the right-side rally, the upper envelope remains materially wider than the lower envelope while the later red pullback produces only limited downside expansion. This visually resembles a positive-force regime with a pullback rather than a balanced reversal.
9. A candidate phase model now has six states: dormant side → directional shock → envelope expansion/regime acceptance → mature trend with signal decay → same-side envelope contraction → opposite-side shock.

## Competing hypotheses
- **Leading:** asymmetric magnitude is the strongest candidate for directional regime state; rolling context may add transition timing, while symmetric magnitude may add sign-neutral conviction or exposure sizing. A minimal combined control would keep those responsibilities separate.
- **Alternative:** asymmetric envelope imbalance alone captures both regime permission and transition information, making rolling statistics unnecessary.
- **Alternative:** rolling-band breaches are mostly artifacts of lag after sign changes and add no predictive information beyond the raw zero crossing and signal slope.
- **Alternative:** magnitude contraction/expansion alone contains the useful state information; signed rolling statistics merely re-label it with path-dependent thresholds.
- **Null:** all three overlays are descriptive transformations of the same signal and will not improve out-of-sample net outcomes after costs.

## Candidate derived states
- **Directional dominance:** compare the positive and absolute negative envelopes, preferably with a bounded imbalance such as `(upper - abs(lower)) / (upper + abs(lower))`.
- **Same-side extension:** locate the current signal relative to the active direction's mean and bands.
- **Dormancy/compression:** identify when one side's envelope has contracted near zero before a new impulse.
- **Acceptance/persistence:** identify same-side envelope expansion after the initiating impulse.
- These are candidate research labels, not accepted trading rules.

## Boundary conditions and unresolved facts
- The screenshots alone do not establish the asset, timeframe, exact calendar period, band lookback used for this rendering, or forward returns after each event.
- Visual correspondence is hypothesis generation, not evidence of predictive value.
- Rolling thresholds are inherently path-dependent: the same absolute signal can be extreme after an opposite regime and ordinary after a same-sign regime.
- The asymmetric implementation is not a conventional conditional distribution over only positive or negative observations. Opposite-sign samples contribute zero while the result remains divided by the full lookback, so each side's envelope mixes magnitude, sign occupancy, and recency. Interpret it provisionally as **side-specific force occupancy**, not pure positive/negative magnitude.
- A newly activated direction faces a compressed baseline, so an initial same-side band breach can be mechanically easy. Any predictive claim must distinguish this denominator/compression effect from genuine information.
- No claim should be promoted until all event rules are causal and tested on fixtures not selected from these screenshots.

## Planned discriminating work
1. Lock the chart metadata and exact formulas before interpreting thresholds numerically.
2. Define causal event labels separately: zero/sign transition, slope direction, rolling-band surprise, symmetric magnitude state, asymmetric dominance, same-side extension, dormancy, and envelope expansion/contraction.
3. First test whether asymmetric dominance separates continuation/pullback states from true reversals better than raw sign and slope alone.
4. Compare forward price paths and trade outcomes for sign transitions with versus without rolling surprise, stratified by asymmetric dominance and contemporaneous magnitude state.
5. Test whether rolling surprise adds information beyond zero crossing, slope, and asymmetric compression; reject it if the simpler state explains the same outcomes.
6. Test whether the asymmetric signal remains useful after controlling separately for sign frequency and same-side average magnitude, so the source of any effect is understood.
7. If complementary information survives, specify the smallest combined control: asymmetric state for directional permission, rolling surprise for timing only if incremental, and symmetric or same-side magnitude for target exposure.
8. Validate on the same fixed fixture first, then one untouched holdout fixture; judge net economics, drawdown/adverse excursion, profit retention, turnover, and costs rather than visual fit.

## Stop condition
Stop or reject the overlay when it does not add stable, causal information beyond the simpler raw-signal baseline. Continue only if it changes a bounded entry, exit, or sizing decision and improves decision-relevant outcomes on holdout evidence.