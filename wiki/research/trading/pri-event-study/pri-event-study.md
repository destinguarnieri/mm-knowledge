# PRI Event Study Research

Status: in progress

Related process: [[research/trading/research_process_v2|Research Process V2]]  
Source glossary: [[trading/catalog_v1|Trading Catalog]]  
Catalog work inventory: [[research/trading/catalog_queue|Trading Catalog Implementation and Evaluation Queue]]  
Linear: [Price Reversal System Research](https://linear.app/money-machine/project/price-reversal-system-research-1b1579ea6126) · [MON-226](https://linear.app/money-machine/issue/MON-226/validate-pri-and-run-the-initial-prb-censored-event-study)

<!-- ================= LIVING HEAD — rewrite in place each session ================= -->

## TL;DR & What's Working

The first bounded study will test whether the Price Reversal Indicator (PRI) carries directional information after a closed-bar reclaim. The study is limited to signal validity: it excludes retest logic, PRZ behavior, position policy, execution, costs, and strategy economics.

**What's working:** the portable event and its active lifecycle are now specified. PRI requires a candle-color reversal plus a close through the prior candle's range. The PRI candle open is the primary Price Reversal Level (PRL). A later strict close through that open in the adverse direction is the Price Reversal Breaker (PRB) and terminates the original PRI event. The PRI candle directional extreme is retained as a secondary level for later work but does not define a retest in this study.

No empirical result exists yet. [MON-226](https://linear.app/money-machine/issue/MON-226/validate-pri-and-run-the-initial-prb-censored-event-study) is Ready. Historical evidence windows and forward horizons must be frozen before the first run.

## Current Read (provisional — not a verdict)

Proceed with a PRI-only event study on Binance USD-M perpetuals. Use a frozen current-liquidity universe and report every timeframe separately. First validate the emitted PRI events against the confirmed rule, then measure favorable and adverse paths only while the event remains valid.

This is a discretionary-codification signal-validity study. Destin's experience supplies the mechanism prior; the work does not assume the signal is alpha or that a particular trading mapping will monetize it.

## Open Threads / Next Experiments

1. Pull [MON-226](https://linear.app/money-machine/issue/MON-226/validate-pri-and-run-the-initial-prb-censored-event-study) and freeze chronological development, replication, and untouched holdout windows for each timeframe.
2. Freeze forward observation horizons in bars for `1d`, `4h`, `1h`, `30m`, `15m`, `5m`, and `1m`.
3. Validate the existing PRI implementation with a direct truth table and representative event-mark review before interpreting returns.
4. Run the first PRI-only forward-response study with matched color-flip and simpler momentum/candle-magnitude controls.
5. If PRI carries directional information, design capture work separately. If delayed testing appears important, specify a later PRL/PRZ study rather than adding retest logic post hoc to this one.

<!-- ================= STABLE ================= -->

## Research Card

### Decision

Determine whether a closed PRI print contains incremental directional information while the print remains valid, separately by side, asset, timeframe, and chronological evidence block.

Possible next states are:

- **amplify:** directional information survives controls and warrants capture research;
- **continue:** evidence is mixed but a bounded discriminating test remains;
- **narrow:** the effect is confined to identified sides, timeframes, assets, or regimes;
- **stop:** PRI does not beat the color-flip and simpler price-action controls on protected evidence;
- **inconclusive:** correctness, sample size, or evidence-window problems prevent a decision.

### Deployment Target

- Asset class: crypto.
- Venue: Binance USD-M perpetuals.
- Population: the 100 active perpetual contracts with the largest trailing 24-hour quote volume at plan creation.
- Universe handling: freeze symbols, rank, observed quote volume, and snapshot timestamp before inspecting results; use the same frozen universe across all timeframes and report missing-history exclusions rather than silently substituting smaller contracts.
- Timeframes: `1d`, `4h`, `1h`, `30m`, `15m`, `5m`, and `1m`.
- Reporting boundary: do not pool timeframes into one headline estimate.
- Account/subaccount: not applicable to this signal-validity study; no trading or capital mutation is in scope.

### Portable Signal Definition

**Bullish PRI:**

1. the previous candle is bearish;
2. the current candle is bullish;
3. the current candle closes strictly above the previous candle high.

**Bearish PRI:**

1. the previous candle is bullish;
2. the current candle is bearish;
3. the current candle closes strictly below the previous candle low.

A color flip without the prior-range reclaim is not PRI. Equality at the prior high or low is not a reclaim. A doji is neither bullish nor bearish for this definition. Events are recognized only from closed candles and must be prefix-causal.

### Active Event Lifecycle

- The event begins at the PRI candle close.
- The PRI candle open is the primary PRL.
- For bullish PRI, PRB occurs when a later candle closes strictly below the primary PRL.
- For bearish PRI, PRB occurs when a later candle closes strictly above the primary PRL.
- A wick through the primary PRL that closes back on the valid side does not invalidate PRI.
- Equality at the primary PRL is not a break.
- The event terminates at the earlier of the PRB close or its fixed forward horizon.
- Favorable excursion (MFE) and adverse excursion (MAE) include the terminal candle's intrabar extremes because invalidation is not known until that candle closes.
- Movement after PRB is excluded from the original PRI response. The reverse implication after PRB belongs to a later PRB study.
- The PRI candle low for bullish events and high for bearish events are retained as secondary levels for later PRL/PRZ work. They do not drive retest classification in the first study.

### Primary Outcomes

All directional outcomes are normalized so favorable movement is positive for both bullish and bearish events.

- directional forward response before PRB or the fixed horizon;
- MFE before termination;
- MAE before termination;
- PRB incidence and time-to-PRB;
- favorable-threshold reach before PRB, paired with its adverse complement;
- event count and censoring/termination reason.

Results remain separated by bullish/bearish side, asset, timeframe, and chronological evidence block. Standard metric tables remain in persisted runs and the backtest UI; this page will retain run IDs and interpretation only.

### Competing Hypotheses

| Hypothesis | Prediction | Strengthens it | Weakens or falsifies it | Next discriminating test |
|---|---|---|---|---|
| Control-transfer continuation | PRI identifies a genuine transfer of control and favorable movement precedes PRB | favorable response and MFE exceed matched controls across evidence blocks | no incremental response or frequent fast PRB | PRI versus matched non-reclaim color flips |
| Delayed confirmation | PRI is informative, but its useful response is not concentrated immediately after the print | weak early response with later favorable response before PRB | no horizon shows incremental response | horizon-separated path analysis; retest remains outside this study |
| Exhaustion | the reclaim is an overextended impulse that tends to fail | adverse movement and PRB dominate after the print | continuation survives controls and replication | compare response with candle magnitude and momentum controls |
| Null / simpler price action | color change, candle magnitude, or ordinary momentum explains the result | PRI has no incremental effect after matched controls | the reclaim condition adds stable directional information | matched-control event study |

### Baselines and Controls

- A matched candle-color flip that does not reclaim the prior range.
- A simpler directionally aligned momentum or candle-magnitude control, frozen before results.
- Unconditional forward response for the same asset, timeframe, side, and evidence block.

Control matching must not use future information. Exact matching variables and tolerances remain to be frozen with the evidence windows and horizons.

### Economic and Strategy Boundary

This first study tests signal behavior, not after-cost monetization. It does not specify entry timing, target, stop, sizing, leverage, funding, fees, slippage, or execution. PRB is an event-validity boundary here, not yet a claim that a realizable order exits exactly at the PRL or PRB close.

### Stopping Condition

Stop the first study when correctness is accepted and the frozen development/replication evidence can support one of three claims: PRI adds directional information beyond the controls, it does not, or the result is confined to an explicit boundary that warrants one narrower protected test. Do not add retest, PRZ, capture, or strategy rules to rescue a weak first result.

## Fixed Assumptions

- The catalog and Destin's direct clarifications are the semantic authority. The catalog queue is a work inventory, not the authority for PRI meaning or event-study design.
- PRI applies to every listed timeframe using the same closed-bar rule.
- The first study excludes retests.
- The PRI candle open is the primary PRL; the directional extreme is secondary.
- PRB requires a strict close-through of the primary PRL in the adverse direction.
- The current top-100 volume rank is a liquidity screen, not a predictor or historical-universe model.
- Search-budget counter: `0` evaluated configurations at kickoff.

<!-- ================= APPEND-ONLY TAIL — do not edit past entries ================= -->

## Run Registry (pointers, not tables)

No runs yet.

## Write Log

### 2026-08-14 — initial PRI study semantics and deployment target frozen

Created the durable PRI research thread from the Trading Catalog and Destin's clarifications. Froze the bullish/bearish three-condition reclaim, primary open PRL, strict close-through PRB, secondary directional extreme, PRB-censored MFE/MAE, exclusion of post-PRB movement, Binance USD-M current-liquidity top-100 population, and seven separate timeframes. Retest, PRZ, capture, economics, execution, and live paths remain outside the first study. Historical evidence windows, forward horizons, exact control matching, and a bounded Linear execution issue remain open. No backtest, code, live runtime, capital mutation, commit, or push occurred.

### 2026-08-14 — Price Reversal System project and PRI execution issue created

Created the active [Price Reversal System Research](https://linear.app/money-machine/project/price-reversal-system-research-1b1579ea6126) project for PRI, PRL, PRZ, PRB, the combined lifecycle, later capture, and cost-valid evaluation. Created High-priority Ready issue [MON-226](https://linear.app/money-machine/issue/MON-226/validate-pri-and-run-the-initial-prb-censored-event-study) as the first bounded packet. MON-226 mirrors the frozen PRI semantics, universe, timeframes, controls, evidence boundary, stopping rule, durable closeout, and offline-only safety boundary; it is related to completed provenance issues MON-89 and MON-169. No backtest, code, live runtime, capital mutation, commit, or push occurred.
