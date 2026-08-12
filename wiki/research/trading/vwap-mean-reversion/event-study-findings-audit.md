# VWAP Event-Study Findings Audit

Status: in progress

Parent: [[research/trading/vwap-mean-reversion/vwap-mean-reversion|VWAP Mean Reversion Research]]

Date: 2026-08-09

## Technical Summary

The three VWAP event studies contain useful evidence, but they do not estimate the same object and should not be read as a single progressive validation chain.

- The **dual-domain band-traversal study** describes first-touch band transitions and ordered excursion ladders on BTC `15m`.
- The **fractional-depth extension** describes half-band continuation, retreat, partial traversal, and conditional payoff geometry on the same BTC `15m` windows.
- The **signed depth-response matrix** describes horizon-bounded fade responses after the first entry into fixed signed depth buckets across 30 assets, three timeframes, and three chronological blocks.

All three are retained as descriptive evidence. None currently specifies or validates Destin's intended trading policy, in which every eligible closed candle updates the position. The fractional-depth coordinate system is disputed, but its measurements remain recorded on their own terms; it is not automatically invalidated by the later signed-coordinate study. Likewise, the signed study corrects several coordinate and display problems without becoming the preferred strategy representation by default.

The strongest finding reviewed so far is a replicated **location-conditioned rejection effect** in the dual-domain study. After an outward transition began, continuation to the next band occurred only about 18–25% of the time; the competing inward barrier was reached about **75–82%** of the time. This appeared in both raw-price and processed-signal measurements and in both chronological windows. The fractional-depth study directionally reinforces the same result at finer spatial resolution: the competing inward barrier won about **62–76%** of half-step trials, with the outer half-steps concentrated near **70–76%** rejection. The continuation branch remains relevant because its price travel can be larger, but that is the risk attached to a favorable directional probability—not grounds to describe the result as poor. The studies also show partial inward movement that does not complete the next formal level, meaningful side/regime variation, and strong coupling between raw-price and normalized-signal domains.

The studies do **not** establish an optimal entry level, nonlinear position curve, readiness rule, full-position trigger, exit policy, or after-cost strategy. Event-study work is paused while these findings and their intended uses are reviewed.

## Audit Decision

| Study | Retained status | Legitimate use | Not established |
|---|---|---|---|
| Dual-domain band traversal | Retained, positive descriptive evidence | Replicated 75–82% local inward rejection after outward transitions; first-arrival risk, excursion ladders, price/signal timing | Bar-by-bar trading policy, full VWAP reversion, or independent price/signal confirmation |
| Fractional-depth traversal | Retained, positive descriptive evidence; coordinates disputed | Replicated 62–76% half-step inward rejection, partial traversal, conditional payoff asymmetry | Preferred coordinate system, optimal depth curve, or full-position rule |
| Signed depth response | Retained, descriptive; sampling and representation under review | Cross-asset/timeframe horizon response after first bucket entry | Every-candle policy, episode economics, stable universal depth rule |

This classification is intentionally non-destructive. A later methodology decision may narrow or reinterpret a study, but none is discarded merely because a newer representation exists.

## The Three Studies Measure Different Things

### Study 1: Dual-domain band traversal

**Question actually answered:** after the first closed-bar crossing of a named price or signal band transition, which competing barrier is reached first, and how often does an ordered excursion complete later rungs?

**Sampling unit:** crossing trials and first-touch episode rungs.

**Scope:** BTC, Binance USD-M, `15m`, matched 100-bar price/signal lookbacks. The anchor contains 10,000 bars, 402 market-side episodes, and 2,872 trials. The chronological replication contains 9,999 bars, 405 episodes, and 2,638 trials. This is a development-history replication, not a protected holdout.

**Canonical artifacts:**

- `e88e7013-9f93-48c8-aefc-e1ee197ed092` — anchor.
- `d474a327-d619-49ed-863d-fa6340bf1569` — chronological replication.

### Study 2: Fractional-depth traversal

**Question actually answered:** at fixed half-band checkpoints, how often does the next outward or inward half-step complete before crossing back through the starting checkpoint, how much partial traversal occurs inside an episode, and how large are the successful and failed branches?

**Sampling unit:** single-attempt competing-barrier trials plus retry-allowed market-side episode transitions.

**Scope:** the same BTC `15m` anchor and chronological replication. The anchor contains 5,060 depth events and 4,021 depth trials; the replication contains 4,901 depth events and 3,980 depth trials.

**Coordinate used:** mean-extension `0`, first band `1`, second band `2`, with half-step checkpoints. Destin does not currently accept this as the preferred trading representation. Findings below therefore describe behavior inside this coordinate system rather than endorsing the coordinate.

**Canonical artifacts:**

- `52fa8f74-d7e7-4d5e-86a1-45612570ba20` — anchor.
- `c36a7b0f-b0a0-4f68-92d3-e05906aef22e` — chronological replication.

### Study 3: Signed depth response

**Question actually answered:** after the first closed bar enters a fixed signed depth bucket during a raw-price VWAP-side episode, what are the fade return, positive-return probability, MFE, and MAE over the next 1, 2, 4, 8, 16, and 32 closed bars?

**Sampling unit:** first entry per episode and signed `0.5` depth bucket.

**Scope:** 30 Binance USD-M assets across `5m`, `15m`, and `1h`, with development, replication, and confirmation blocks. All 270 asset/timeframe/block cells completed. The blocks span November 5, 2025 through June 1, 2026 UTC and are matched chronological samples, not a protected untouched holdout.

**Coordinates:** raw percentage from VWAP, price-band depth, trailing-volatility depth, and processed-signal band depth. Price and signal band coordinates anchor VWAP/zero at `0`, first bands at `±1`, second bands at `±2`, and extrapolate beyond `±2` without clipping.

**Canonical artifact:** `cf9dd71a-1002-4d3a-be9a-c67b27fec767`.

## Study 1 Findings: Outward Transitions Rejected Inward About 75–82% of the Time

The anchor and replication show a clear, favorable mean-reversion probability at the first competing barrier. The chart labels success from the outward trial's perspective, so its displayed continuation probability must also be read through the strategy-relevant complement.

| Outward transition | Continuation probability | Local inward-rejection probability |
|---|---:|---:|
| Mean→1σ | 23–25% | **75–77%** |
| 1σ→2σ | 18–21% | **79–82%** |

These ranges cover raw price and processed signal across the anchor and chronological replication. The result is unusually consistent across both domains and both windows: once an outward transition began, the next competing barrier was inward roughly three to four times as often as outward.

For an outward trial, a failure to continue is defined as an inward recross of the starting level. Therefore, the complement is a real **local rejection/reversion event**:

- Mean→1σ failure means price crossed inward through the mean-extension boundary before reaching 1σ.
- 1σ→2σ failure means price crossed inward through 1σ before reaching 2σ.

This does not mean 75–82% of trials completed a full reversion to VWAP. It means they produced the first inward movement the strategy is designed to capture. A later retry can still continue outward within the larger episode.

The inward rows answer different follow-on questions:

- The pooled raw-price inward 2σ→1σ completion probability was approximately `0.51–0.54`.
- The pooled raw-price inward 1σ→mean probability was approximately `0.36–0.39`.
- Mean→VWAP completion under the same strict race was only approximately `0.25–0.27`.

The apparent tension between strong outward rejection and lower completion of later inward rungs is definitional rather than contradictory. The first result asks whether the outward attempt is rejected through its starting boundary. The inward rows then ask whether that reversal continues through another complete band before re-expanding. Local rejection is common; uninterrupted full traversal is less common.

Price and processed signal generally touched the same transitions on the same bar. Signal occasionally led on inward transitions, but the normalized signal behaved primarily as a timing transform of the raw-price extension process. It should not be counted as independent confirmation of the same move.

![VWAP band traversal study](Screenshot%202026-08-07%20at%2011.26.24%E2%80%AFAM.png)

**Useful interpretation:** first touch has identified a replicated directional effect worth capturing. At the measured BTC `15m` locations, the immediate competing move strongly favored inward rejection. This can inform early fade participation, initial commitment, and reserved capacity for the 18–25% continuation branch. It does not describe the intended sequence of adds and reductions after arrival, but it is positive signal evidence rather than merely a risk diagnostic.

### Primary questions produced by Study 1

1. **How can the strategy monetize the approximately 75–82% local inward-rejection branch?**
2. **How economically damaging is the approximately 18–25% outward-continuation branch?**
3. **What is the return profile of enduring the mechanical compression after a 2σ turn?** Specifically, from the 2σ touch through 1σ, mean, and VWAP, what raw-price return, duration, MFE, and MAE does a position experience, and how much rung completion comes from price moving inward versus VWAP/bands mechanically catching up?

These are the main unanswered questions produced by the study so far. They are recorded here without proposing answers or selecting a follow-up design yet.

**Boundary:** this is one asset, one timeframe, and two adjacent historical blocks. It contains no execution costs or position simulation.

## Study 2 Findings: Half-Step Rejection Reproduced at Approximately 62–76%

The fractional-depth study directionally reproduces Study 1's local inward-rejection effect at finer half-band resolution. The favorable direction is therefore not confined to the coarser mean, 1σ, and 2σ checkpoints.

### Every outward half-step favored inward rejection

For pooled market sides, raw-price single-attempt probabilities were:

| Half-step | Anchor continuation | Anchor rejection | Replication continuation | Replication rejection |
|---|---:|---:|---:|---:|
| `0→0.5` | 29.7% | **70.3%** | 37.5% | **62.5%** |
| `0.5→1` | 34.9% | **65.1%** | 29.8% | **70.2%** |
| `1→1.5` | 27.8% | **72.2%** | 30.3% | **69.7%** |
| `1.5→2` | 25.3% | **74.7%** | 27.0% | **73.0%** |

The processed-signal domain showed the same result. Across price and signal, anchor and replication, local inward rejection ranged from approximately **62.5% to 75.5%** at every measured half-step. The two outer rungs, `1→1.5` and `1.5→2`, concentrated near **69.7–75.5%** rejection. The tendency generally strengthened with depth, especially beyond `1`, although it was not strictly monotonic in every series.

Study 1 found approximately 75–82% rejection across full-band outward transitions; Study 2 finds approximately 62–76% across half-band transitions. The direction and broad magnitude are consistent. This is positive finer-resolution confirmation that extension more often met the local inward barrier than the next outward checkpoint, not merely a reframing of a disappointing continuation rate.

### Inward-turn completion improved at deeper checkpoints, but was not deterministic

For pooled raw-price turns, next-inner half-step completion ranged from approximately 40% to 64% across the two windows. The deepest measured turn, `2→1.5`, was strongest: 54.6% in the anchor and 63.6% in replication. Shallower turns were generally closer to a coin flip or below it.

This supports distinguishing **location** from **turn evidence**. It does not show that depth alone is a sufficient readiness signal.

### Partial traversal was economically relevant

This is the most durable contribution of the study: a formal target can label a path incomplete even when the path contains tradeable movement.

### Low continuation probability coexisted with larger continuation payoffs

In the anchor, successful outward raw-price half-steps had conditional median travel of roughly `+33` to `+58 bps`, while retreat failures were approximately `−16` to `−19 bps`. Replication showed the same directional asymmetry with smaller successful travel at several rungs.

![VWAP fractional-depth traversal](Screenshot%202026-08-07%20at%2011.32.08%E2%80%AFAM.png)

**Useful interpretation:** the chart independently echoes the first study's favorable rejection result at finer resolution. It also shows why both full-touch-only opportunity definitions and full-position-on-touch rules are too coarse. Rejection pressure, partial inward movement, and continuation-tail magnitude all matter for capacity and capture design.

**Boundary:** the coordinate representation remains disputed. Preserve the observed probabilities and conditional paths as properties of this measurement; do not treat `0/0.5/1/1.5/2` as the accepted strategy state space without a separate decision.

## Study 3 Findings: Broader Coverage Reveals Strong Period and Side Dependence

The signed study fixed important representation failures: it preserved sign, removed clipping, extrapolated beyond the second band, removed eventual-recross outcomes, and bounded every outcome to explicit forward horizons. Formula-level BTC `15m` recomputation matched saved depth values to floating-point precision.

The wider matrix does not reveal a stable universal response curve.

- Price-band observations reached approximately `−8.75` to `+9.25` in the asset-equal output; the underlying fixed bucket indices reached `−18` through `+18`. The data was not truncated at `±2`.
- At the commonly populated central and outer depths, positive-return probabilities were often only modestly above or below `0.50`; MFE and MAE were frequently of similar order.
- Development, replication, and confirmation sometimes changed the sign and size of the median fade response at the same timeframe, side, depth, and horizon.
- The instability increased with horizon and was especially visible at `15m` and `1h`.
- Using only price-band rows with at least five contributing assets, the sign of median fade return agreed across all three chronological blocks in approximately 46% of `5m`, 41% of `15m`, and 27% of `1h` matched depth/horizon cells. These are audit diagnostics, not hypothesis-test results.
- `5m` displayed the greatest directional consistency of the three timeframes, but even there fewer than half of matched cells preserved the same sign across all blocks.

The study also exposed side asymmetry. For example, several `15m` positive-side depths showed strong fade returns in development or replication while corresponding negative-side depths were weak or negative; confirmation sometimes reversed that emphasis. Blending the chronological blocks would conceal this instability rather than resolve it.

**Useful interpretation:** the matrix is a map of conditional forward response and regime sensitivity. It is useful for identifying where effects are stable enough to investigate and where MFE/MAE may constrain capacity. It is not evidence for one universal monotonic sizing curve.

**Boundary:** first entry per episode/bucket deliberately prevents persistent occupancy from dominating the arrival-conditioned estimate. That sampling rule does not represent Destin's intended every-candle position updates. Whether and how every-bar observations should be treated as statistically dependent remains open for later discussion; this audit does not freeze that decision.

## Cross-Study Findings

### 1. First-touch extension contains a strong local inward-rejection effect

The dual-domain study shows 75–82% local inward rejection after the measured outward transitions, replicated across price/signal domains and chronological windows. The fractional study independently echoes that direction at finer resolution, with 62–76% rejection across every half-step and approximately 70–76% at the outer rungs. Together they show that the effect is not confined to coarse full-band checkpoints. This is the clearest positive result in the event-study sequence so far. The continuation tail, MFE/MAE balance, and execution economics still determine how to monetize it, but they do not negate the favorable directional probability.

### 2. Full touches discard useful path information

The fractional study directly records episodes that move inward without completing the next half-step. The intended trading semantics also update inventory on each eligible candle, meaning the economic object is the path rather than a final band-touch label.

### 3. First touch still has a legitimate role

First touch isolates what happens after an excursion first arrives at a location. It may inform initial commitment, reserve capacity, and arrival-conditioned failure risk. It should be labeled as setup geometry, not as the complete trade model.



## What None of the Studies Tested

- Destin's intended rule in which every eligible closed candle changes position.
- A sequential inventory simulation with existing position, average entry, remaining capacity, and realized/unrealized P&L.
- Episode-level net P&L after fees, slippage, funding, and achievable fills.
- Readiness features such as participant flow, control transfer, absorption, or volatility/volume anomalies.
- A protected untouched holdout selected before methodology changes.
- A causal claim that VWAP extension creates later reversion.
- A final statistical treatment of overlapping horizons or within-episode observations. Destin has reserved the independence question for later discussion.

## Remaining Competing Interpretations

1. **Location-plus-readiness hypothesis:** depth identifies where opportunity exists, while a separate turn/readiness state determines whether to act.
2. **Sequential inventory hypothesis:** the edge is harvested through repeated accumulation and distribution across the entire excursion rather than through one entry and one exit.
3. **Regime-mixture hypothesis:** apparently conflicting blocks reflect distinct continuation/reversion regimes that should be identified rather than blended.
4. **Weak-edge/null hypothesis:** much of the observed response is small relative to path risk and costs, and unstable signs indicate insufficient standalone economic value.

The current evidence supports keeping all four live. The first two are economically promising interpretations; the latter two are necessary alternatives.

## Research Pause and Review Gate

No additional VWAP event study should be designed or implemented until this audit is reviewed with Destin.

The review should decide:

1. Which first-touch questions are worth retaining.
2. Which fractional-depth observations are useful despite disagreement with its coordinate representation.
3. Whether the signed coordinate system is useful, requires revision, or should remain only an audit view.
4. The exact estimand for an every-candle study, including whether it is a conditional-return study, a sequential position-policy simulation, or both.
5. The treatment of within-episode and overlapping-horizon dependence; this remains open rather than assumed.

Only after those decisions should the next experiment be preregistered with a single decision question, primary outcome, fixed sampling unit, and stopping condition.

## Source Inventory

- Dual-domain raw artifacts: `.research/runs/vwap_band_traversal/e88e7013-9f93-48c8-aefc-e1ee197ed092/` and `.research/runs/vwap_band_traversal/d474a327-d619-49ed-863d-fa6340bf1569/`.
- Fractional-depth raw artifacts: `.research/runs/vwap_band_traversal/52fa8f74-d7e7-4d5e-86a1-45612570ba20/` and `.research/runs/vwap_band_traversal/c36a7b0f-b0a0-4f68-92d3-e05906aef22e/`.
- Signed depth-response raw artifacts: `.research/runs/vwap_signed_depth_response/cf9dd71a-1002-4d3a-be9a-c67b27fec767/`.
- Parent synthesis and run registry: [[research/trading/vwap-mean-reversion/vwap-mean-reversion|VWAP Mean Reversion Research]].

The persisted artifacts remain the metric source of truth. This page records the audit interpretation and decision boundaries rather than duplicating full raw tables.
