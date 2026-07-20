---
name: EMA Stats Comparison
overview: Snapshot the current visual interpretation of symmetric magnitude, asymmetric magnitude, and rolling signed statistics and define the smallest experiment that could distinguish their roles.
todos:
  - id: define-events
    content: Specify causal symmetric-magnitude, asymmetric handoff, rolling-surprise, and sign-cross event definitions.
    status: pending
  - id: run-event-study
    content: Measure conditioned forward return, MFE, and MAE over bounded horizons.
    status: pending
  - id: decide-mapping
    content: Accept, reject, or narrow the proposed direction/sizing/transition role split.
    status: pending
isProject: false
Model: GPT 5.6 Sol Medium
Skill: Exploratory Researcher
---

# EMA Signal Statistics Comparison

## Current interpretation
- **Signal sign** appears to carry direction, while signal amplitude reflects trend expansion.
- **Magnitude statistics** provide a symmetric strength scale and may be best suited to exposure sizing or continuation confirmation.
- **Asymmetric magnitude statistics** separate positive and negative activity. Visually, the inactive side's envelope contracts and the first opposing impulse becomes conspicuous, making this a plausible regime-handoff detector.
- **Rolling signed statistics** retain directional regime memory and may be best suited to detecting transitions or opposite-regime surprises.
- Large deviations visually align more with acceleration than exhaustion; fading outer-band events is not supported by this sample.
- Signal amplitude often decays while the price trend persists, arguing against amplitude as a standalone direction or full-exit rule.
- Both methods self-normalize after strong impulses as their adaptive bands expand.
- The multi-panel view strengthens the existing profit-retention diagnosis: favorable position paths build during established trends, then surrender substantial open profit near eventual flips. Magnitude peaks generally occur before or during that profit accumulation, not at a dependable exit point.
- The late-window chop shows a possible role for magnitude gating: direction changes continue while magnitude is subdued relative to bands, but this remains a visual hypothesis rather than tested evidence.

## Asymmetric-statistic semantics
- The current asymmetric helper is frequency-weighted, not a pure conditional distribution of same-side magnitudes: absent-side samples contribute zero while the full lookback remains the divisor.
- Each side's envelope therefore combines amplitude, sign frequency, and recency of same-side activity.
- The first moments mostly decompose existing information:
  - `positive_mean + negative_mean` approximates the signed rolling mean;
  - `positive_mean - negative_mean` approximates mean absolute magnitude.
- Side-specific dispersion is the more distinct information.
- A plausible combined mapping is asymmetric magnitude for early handoff detection, confirmed by rolling signed surprise or EMA-regime evidence.

## Competing hypotheses
1. **Continuation intensity:** magnitude-band crossings predict continued movement in the signal direction.
2. **Transition detection:** rolling-stat opposite-regime deviations identify meaningful reversals earlier or more selectively.
3. **Asymmetric handoff:** the first impulse through a contracted same-side envelope identifies a regime transition earlier than pooled magnitude statistics.
4. **Chop suppression:** low magnitude relative to the prevailing envelope identifies sign changes that should not trigger full exposure flips.
5. **Null:** none of the statistics adds useful information beyond signal sign and EMA regime.

## Bounded experiment
- Use the existing `emac_v4` processed signal and causal statistics in [`backend/app/backtest/strategies/emac_v4.py`](backend/app/backtest/strategies/emac_v4.py).
- Define event classes without changing trading behavior:
  - magnitude crossings of mean, 1σ, and 2σ;
  - asymmetric same-side crossings, including the first crossing after side inactivity;
  - rolling signed deviations in the prevailing and opposing directions;
  - zero/sign crossings as the baseline.
- For each event, measure forward return, MFE, and MAE over 1, 3, 6, and 12 bars, conditioned on EMA regime, regime age, and recent same-side activity.
- Compare whether symmetric magnitude extremes behave as continuation events, asymmetric first impulses behave as early handoffs, and rolling opposing deviations confirm transitions.
- Compare sign crosses occurring at low versus high normalized magnitude to test the chop-suppression hypothesis.
- Stop after this event study unless the separation is clear enough to justify one narrowly specified strategy mapping.

## Decision mapping if supported
- **Signal sign:** directional state.
- **Symmetric magnitude statistics:** target exposure, entry urgency, or continuation confirmation.
- **Asymmetric magnitude statistics:** early opposing-impulse or regime-handoff candidate.
- **Rolling signed statistics:** handoff confirmation or exit override.

## Concerns and falsifiers
- **Inactive-side collapse:** a modest countertrend impulse can appear extreme after its side has been absent, creating false reversal signals.
- **Conflated semantics:** asymmetric bands mix magnitude with sign frequency and recency; they must not be interpreted as ordinary conditional z-scores.
- **Adaptive self-normalization:** all rolling bands expand after strong impulses, so event meaning changes with regime age.
- **Profit-giveback mismatch:** amplitude decay precedes many actual trend endings, so direct amplitude-based exits could truncate winners or still miss late giveback.
- **Visual-selection risk:** the apparent handoffs were identified after viewing one favorable window.
- **Redundancy:** asymmetric first moments may add presentation clarity without incremental predictive information.
- The asymmetric-handoff hypothesis is weakened if first opposing-band crossings do not outperform ordinary sign crosses on forward return, MFE/MAE, or false-transition rate.
- The chop-suppression hypothesis is weakened if low-magnitude sign crosses are not materially worse than high-magnitude crosses.

## Boundaries
- Current evidence is visual and limited to one asset/window.
- Multi-panel identities and exact event timing should be verified from stored series before treating the visual alignment as measured evidence.
- No predictive, economic, cross-asset, or after-cost conclusion has been established.
- This plan does not authorize strategy implementation, broad parameter sweeps, or live/capital actions.