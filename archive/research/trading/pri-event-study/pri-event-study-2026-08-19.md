# PRI Event Study Research

Status: superseded — historical audit only

> Quarantined 2026-08-19. The measurement designs and interpretations on this page are not active PRI evidence or priors for new strategy work. See the indexed active PRI page for the reset scope.

Related process: [[research/trading/research_process_v2|Research Process V2]]  
Source glossary: [[trading/catalog_v1|Trading Catalog]]  
Catalog work inventory: [[research/trading/catalog_queue|Trading Catalog Implementation and Evaluation Queue]]  
Linear: [Price Reversal System Research](https://linear.app/money-machine/project/price-reversal-system-research-1b1579ea6126) · [MON-226](https://linear.app/money-machine/issue/MON-226/validate-pri-and-run-the-initial-prb-censored-event-study)

<!-- ================= LIVING HEAD — rewrite in place each session ================= -->

## TL;DR & What's Working

The first bounded study will test whether the Price Reversal Indicator (PRI) carries directional information after a closed-bar reclaim. The study is limited to signal validity: it excludes retest logic, PRZ behavior, position policy, execution, costs, and strategy economics.

**What's working:** the portable event and its active lifecycle are specified and implemented in an isolated offline event-study package. Direct tests cover the bullish/bearish truth table, equality, doji/nonfinite handling, prefix stability, wick-through validity, strict close-through PRB, next-PRI episode replacement, terminal-bar excursions, right censoring, artifact lifecycle, and current-liquidity universe ranking. PRI requires a candle-color reversal plus a close through the prior candle's range. The PRI candle open is the primary Price Reversal Level (PRL). A later strict adverse close through that open is the Price Reversal Breaker (PRB). Any later PRI, of either direction, also ends the active episode and begins a new one at its close. The terminating candle's high and low remain part of the prior episode because its terminal condition is known only at close. The PRI candle directional extreme is retained as a secondary level for later work but does not define a retest in this study.

Canonical plan run `58ab2173-196c-410b-af3a-996cdba6cc38` freezes the 2026-08-14 Binance USD-M current-volume top 100, original horizons `1/3/6/12/24`, three chronological evidence roles, full verified daily histories, fixed intraday blocks, one causal pre-roll bar, and block-boundary censoring. Return-blind review run `acec7fd5-3c6c-459e-a45d-1c4bfdae4319` validated 42 event marks. The corrected full development pass is complete across 651 frozen asset/timeframe cells and 527,474 episodes. A probability-focused development extension now measures every horizon `H1–H6` without changing the frozen universe or windows. It preserves the approved episode MFE/MAE semantics and adds exact fixed-H close return alongside episode-constrained close return. Canonical per-timeframe run IDs are in the registry below; every registered checksum verifies.

The development review now distinguishes descriptive signal diagnostics from a trade-faithful path measurement. Exact fixed-H return starts at the PRI signal close and ends at the exact horizon close, even if PRB or another PRI ended the episode earlier. It is useful for measuring unconditional persistence of the original direction, but it ignores executable intrabar prices and is not expected trade return. MFE/MAE include executable highs and lows only until episode termination, but separate exceedance probabilities do not reveal which path event happened first. Small pooled signed means primarily reflect cancellation between substantial positive and negative outcomes rather than unusually small crypto movement; an independent BTC `5m` recomputation matched all 1,568 saved PRI events and H1–H6 outcomes exactly with zero formula discrepancy.

The first structural finding remains useful: the median episode lasts four bars across all seven timeframes, and most episodes terminate on a later PRI. This does not justify truncating the next study at H6. Full-series BTC review found events whose H6 return is adverse but whose later response becomes favorable. Preserve dense H1–H6 resolution, extend the path review through H8/H12/H24, and retain full-episode outcomes.

The next PRI development universe is now founder-reviewed rather than mechanically described as Binance's literal top 100. Destin reviewed every member of the frozen mapped 100, excluded 40 contracts, and retained all 60 approved contracts for PRI work. No contract outside the original frozen 100 may be substituted to restore a target count. The 40-name exclusion overlay is intended to be reused broadly so later research does not repeat the same asset-quality mistakes, although it is not yet declared an absolute ban for every possible context. Completed child plan `6ae6ecf0-9f9a-41dc-9a50-aecc56891454` preserves the original snapshot, cutoff, member fields, ranks, and windows. It contains 1,247 runnable cells and 13 explicit insufficient-history exclusions. `LITUSDT` remains eligible; its daily cells are runnable and its limited intraday coverage is handled per cell rather than by global blacklist.

The ordered first-passage development pass is complete across all seven timeframes: 410 runnable cells and 337,836 PRI episodes. It evaluates the frozen `5/10/25/50/100/200/300/500/750/1000` bps favorable-by-adverse threshold matrix at H1–H6, H8/H12/H24, and full episode. Every event stops at PRB, the next PRI, or the development boundary; terminating-bar extremes are included and no post-episode price is inspected. Same-bar dual touches are explicitly ambiguous because OHLC cannot recover their intrabar order. A preliminary structural read is that small thresholds become increasingly dominated by same-bar ambiguity on higher timeframes, while larger thresholds preserve more order information. This is a measurement limit to respect during review, not a reason to infer an order.

## Current Read (provisional — not a verdict)

Proceed with a PRI-only event study on Binance USD-M perpetuals. Use a frozen current-liquidity universe and report every timeframe separately. First validate the emitted PRI events against the confirmed rule, then measure favorable and adverse paths only while the event remains valid.

This is a discretionary-codification signal-validity study. Destin's experience supplies the mechanism prior; the work does not assume the signal is alpha or that a particular trading mapping will monetize it.

## Open Threads / Next Experiments

1. Review the ordered first-passage matrices by timeframe, direction, horizon, and threshold pair. Prioritize regions where favorable-first exceeds adverse-first without same-bar ambiguity dominating the denominator.
2. Decide which bounded development construction, if any, should become the candidate capture rule before opening replication.
3. Keep prior-PRI target selection and scale-out/full-target position management as the next full-system capture study. They are expected to reduce the magnitude and probability of negative realized returns but are not yet tested.
4. Keep chronological replication and holdout sealed until the revised development path estimand and candidate rule are accepted.

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
- Population: the 60 founder-approved contracts remaining after review of the frozen mapped 100 from plan `58ab2173-196c-410b-af3a-996cdba6cc38`.
- Universe handling: preserve the original frozen ranks and snapshot, remove the 40 founder-excluded contracts, never substitute contracts from outside the frozen 100, and report timeframe-specific missing-history exclusions without removing an asset globally.
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
- The event terminates at the earliest of a PRB close, the next PRI close of either direction, or its fixed forward horizon.
- The terminating candle's intrabar high and low are included in favorable excursion (MFE) and adverse excursion (MAE) because neither PRB nor a new PRI is known until that candle closes.
- A terminating PRI candle begins its own new episode at that same close; its high and low are not post-entry observations for the new episode.
- Movement after PRB is excluded from the original PRI response. The reverse implication after PRB belongs to a later PRB study.
- The PRI candle low for bullish events and high for bearish events are retained as secondary levels for later PRL/PRZ work. They do not drive retest classification in the first study.

### Primary Outcomes

All directional outcomes are normalized so favorable movement is positive for both bullish and bearish events.

- directional terminal-close response before PRB, the next PRI, or the fixed horizon;
- exact fixed-bar close return from the signal close to H1, H2, H3, H4, H5, and H6 regardless of earlier episode termination, retained as a measurement rather than a change to PRI validity;
- episode-constrained close return at the earlier of horizon, PRB, or next PRI;
- MFE before termination;
- MAE before termination;
- PRB and next-PRI incidence and time to termination;
- favorable-threshold reach from intrabar highs/lows before termination, paired with its adverse complement;
- event count and censoring/termination reason.

Results remain separated by bullish/bearish side, asset, timeframe, and chronological evidence block. Standard metric tables remain in persisted runs and the backtest UI; this page will retain run IDs and interpretation only.

### Competing Hypotheses

| Hypothesis | Prediction | Strengthens it | Weakens or falsifies it | Next discriminating test |
|---|---|---|---|---|
| Control-transfer continuation | PRI identifies a genuine transfer of control and favorable movement precedes PRB | favorable response and MFE exceed matched controls across evidence blocks | no incremental response or frequent fast PRB | PRI versus matched non-reclaim color flips |
| Delayed confirmation | PRI is informative, but its useful response is not concentrated immediately after the print | weak early response with later favorable response before PRB | no horizon shows incremental response | horizon-separated path analysis; retest remains outside this study |
| Exhaustion | the reclaim is an overextended impulse that tends to fail | adverse movement and PRB dominate after the print | continuation survives controls and replication | compare response with candle magnitude and momentum controls |
| Null / simpler price action | color change, candle magnitude, or ordinary momentum explains the result | PRI has no incremental effect after matched controls | the reclaim condition adds stable directional information | matched-control event study |

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
- Any subsequent PRI, same-side or opposite-side, ends the active episode at its close; terminal-candle highs and lows belong to the ending episode.
- The current mapped top-100 volume rank is a liquidity screen, not a predictor or historical-universe model. It is not a literal raw Binance top 100 because unsupported catalog symbols were filtered before the 100 members were selected. For the next PRI work, Destin reviewed that exact frozen set and accepted the 60 survivors rather than backfilling exclusions.
- Reusable founder exclusion overlay: `ACEUSDT`, `PAXGUSDT`, `WLFIUSDT`, `BCHUSDT`, `2ZUSDT`, `AVNTUSDT`, `TRUMPUSDT`, `MOVEUSDT`, `XAIUSDT`, `PIXELUSDT`, `ICPUSDT`, `XPLUSDT`, `BOMEUSDT`, `ETCUSDT`, `ASTERUSDT`, `TSTUSDT`, `SANDUSDT`, `NILUSDT`, `AXSUSDT`, `DOTUSDT`, `GALAUSDT`, `ILVUSDT`, `TRBUSDT`, `1000LUNCUSDT`, `PEOPLEUSDT`, `SAGAUSDT`, `NOTUSDT`, `CATIUSDT`, `MEGAUSDT`, `PNUTUSDT`, `DOODUSDT`, `CFXUSDT`, `0GUSDT`, `CCUSDT`, `SKYUSDT`, `GRASSUSDT`, `BABYUSDT`, `METUSDT`, `BIOUSDT`, and `POLUSDT`.
- `LITUSDT` remains approved. Its complete verified daily history is runnable. Its shorter verified lifespan excludes development/replication cells on `4h`, `1h`, and `30m`, plus the `15m` development cell; these coverage exclusions do not blacklist the contract.
- The frozen plan's original lifecycle horizons are `1`, `3`, `6`, `12`, and `24`; the accepted probability extension separately evaluates every close/path horizon `1`, `2`, `3`, `4`, `5`, and `6` without changing universe or evidence windows.
- H6 is not an accepted maximum useful horizon. The next ordered-path study retains H1–H6 and extends through H8/H12/H24 plus full episode duration.
- Intraday development/replication/holdout blocks contain `10,000` bars each for `1m`/`5m`/`15m`, `8,000` for `30m`, `4,000` for `1h`, and `1,000` for `4h`; every cell has one causal pre-roll bar and no outcome may cross its block boundary.
- Each `1d` asset uses its complete verified Binance history through the common frozen cutoff, split chronologically into thirds with any remainder assigned to holdout.
- Search-budget counter: `0` evaluated configurations at kickoff.

<!-- ================= APPEND-ONLY TAIL — do not edit past entries ================= -->

## Run Registry (pointers, not tables)

- `58ab2173-196c-410b-af3a-996cdba6cc38` — completed `pri_plan`; frozen universe and evidence plan only, with no candles or outcomes. Artifacts: `universe.json`, `plan.json`, and `summary.json` under the canonical ignored KB run store.
- `6ae6ecf0-9f9a-41dc-9a50-aecc56891454` — canonical reviewed `pri_plan`, parented to `58ab2173`; exact 60 approved survivors with preserved original ranks/snapshot/windows, no substitutions, 1,247 runnable cells, 13 explicit insufficient-history exclusions, ordered horizons H1–H6/H8/H12/H24, and full-episode observation enabled. Manifest and plan horizons agree, all three artifact checksums verify, and no candles or outcomes were loaded.
- `2f4f0b50-1ae6-464e-8e7e-6e1fa0671dce` — superseded reviewed-plan artifact. Its plan payload and checksums are valid, but its manifest retained the parent plan's old horizon label. It was not used for outcomes and is replaced by `6ae6ecf0`.
- `028f0780-3f70-46b0-a7f6-338406264df1` — canonical `1m` ordered first-passage development run.
- `c6a77cf2-d49a-4869-8dac-09461e50d6dc` — canonical `5m` ordered first-passage development run.
- `c9e1f56d-d784-426d-a171-2f47ddb34b24` — canonical `15m` ordered first-passage development run.
- `388c02e7-8435-4184-a9c2-443a4868c3dd` — canonical `30m` ordered first-passage development run.
- `120b3656-100f-463e-a3bb-ca41a5cb2669` — canonical `1h` ordered first-passage development run.
- `44e0f350-2d5a-48f4-a35c-450e546b341b` — canonical `4h` ordered first-passage development run.
- `085b74d2-6973-4623-8c36-bd6dacd19629` — canonical full-history `1d` ordered first-passage development run.
- `e873e9c7-e1fb-4d20-8f9e-3a8764c5c357` — noncanonical slow-aggregation `5m` predecessor. It completed with valid checksums; its decompressed probability report is byte-identical to canonical vectorized run `c6a77cf2` and serves as an implementation-equivalence check.
- `acec7fd5-3c6c-459e-a45d-1c4bfdae4319` — completed `pri_event_review`; 42 return-blind prior/signal candle pairs across BTC, STRK, XAI, all seven development timeframes, and both directions. No future candles or outcomes.
- `0a98a7c2-7f91-482f-9a2d-4d155102a221` — completed corrected `pri` development slice for BTC/ETH/SOL `5m`; non-overlapping episodes end at PRB, the next PRI of either direction, or horizon, and all eight artifact checksums verify.
- `11f9cce1-82a3-4531-b19f-a5c2780b2b27` — corrected full-universe `1m` development outcomes.
- `c01cdbab-cabf-4604-8610-e93d1bc9fb17` — corrected full-universe `5m` development outcomes.
- `d1fe1258-9870-4a18-b7c4-b0bfb50ebe84` — corrected `15m` development outcomes for all 96 runnable frozen cells.
- `eb5f3a42-0b1d-4dd2-930e-aa113726d91b` — corrected `30m` development outcomes for all 85 runnable frozen cells.
- `e29782e8-a61b-494b-b9e2-48d6525c2431` — corrected `1h` development outcomes for all 85 runnable frozen cells.
- `6f0ac16e-61b4-4818-8872-2abe101822da` — corrected `4h` development outcomes for all 85 runnable frozen cells.
- `db8a5650-d962-4688-a652-24fb6c02ebf2` — corrected full-lifespan `1d` development outcomes for all 100 frozen cells.
- `5fa93bdc-946a-4c0a-958f-626444913316` — canonical compressed `1m` H1–H6 probability development run.
- `870d34cc-9edd-4d04-a045-07e5a48fa2c0` — canonical compressed `5m` H1–H6 probability development run.
- `b84a9c5c-29b5-4f78-95ce-c4987a884ec2` — canonical compressed `15m` H1–H6 probability development run.
- `032ce2bd-63e9-4f27-84fa-cda71e665fdd` — canonical compressed `30m` H1–H6 probability development run.
- `215cc49d-91e2-475b-943c-f3236d7c7f4d` — canonical compressed `1h` H1–H6 probability development run.
- `b39d1332-2b8b-4ef7-a8e7-ceb15520ddde` — canonical compressed `4h` H1–H6 probability development run.
- `9b889b21-e3e0-4ff0-bbc5-3d1393a9eccc` — canonical compressed full-lifespan `1d` H1–H6 probability development run.
- `8d4f7643-e597-4fad-a29f-b37a8be8defd` — failed `pri_event_review`; candle retrieval completed but UUID JSON serialization failed before review artifacts were saved. Superseded by the completed typed-serialization rerun above.

Noncanonical semantic review aid: `/Users/destinguarnieri/.codex/visualizations/2026/08/14/01a00233-e6cc-7c01-856f-18d528e13115/pri-btc-full-series.html` contains the complete BTCUSDT `5m` development overview, PRI event navigator, H1–H6 exact returns, and episode-aware MFE/MAE ledger. It is a visual inspection aid, not registered run evidence.

## Write Log

### 2026-08-19 — ordered first-passage development pass completed

Completed seven canonical `pri_first_passage` development runs parented to reviewed plan `6ae6ecf0-9f9a-41dc-9a50-aecc56891454`. Across 410 runnable asset/timeframe cells, 337,836 PRI episodes were measured against the fixed ten-level favorable-by-adverse threshold matrix at H1–H6, H8/H12/H24, and full episode. The engine records favorable-first, adverse-first, same-bar ambiguity, no-hit terminal return, and explicit right censoring; it stops at PRB or the next PRI, includes terminating-bar highs/lows, and never inspects post-episode prices. All seven runs completed from cached Binance candles only. Every artifact checksum, parent link, group count, outcome-count identity, probability complement, and censoring denominator verifies. The initial slow `5m` aggregation and optimized vectorized rerun produce byte-identical decompressed probability reports. Small thresholds on higher timeframes are often unorderable within OHLC bars, so review must not redistribute the ambiguous category. Thirty-eight focused PRI tests pass; scoped Ruff, formatting, strict mypy, function-length, and diff checks are clean. Replication and holdout remain sealed; prior-PRI targets, scale-out, costs, execution, live runtime, capital mutation, commit, and push remain untouched.

### 2026-08-19 — reviewed 60-contract PRI plan materialized

Derived canonical plan `6ae6ecf0-9f9a-41dc-9a50-aecc56891454` entirely from verified parent `58ab2173-196c-410b-af3a-996cdba6cc38`, applying the founder-approved 40-contract exclusion overlay with no substitutions. The child preserves the frozen snapshot, cutoff, original non-contiguous ranks, member fields, and every retained evidence window. It records H1–H6/H8/H12/H24 plus full-episode observation, 1,247 runnable cells, and 13 explicit insufficient-history exclusions. `HYPEUSDT` and `PUMPUSDT` lack the `4h`/`1h`/`30m` development cells; `LITUSDT` has seven intraday exclusions but all three daily cells remain runnable. All registered checksums verify and manifest horizons match the plan payload. Initial child `2f4f0b50-1ae6-464e-8e7e-6e1fa0671dce` was superseded before use because its manifest inherited the old parent horizon label; no completed run was edited. Planner derivation tests pass without database fixtures; scoped Ruff, formatting, and strict mypy are clean. No candles, outcomes, replication/holdout evidence, live runtime, capital mutation, commit, or push occurred.

### 2026-08-19 — founder-reviewed 60-contract PRI universe accepted

Destin reviewed all 100 members of the frozen mapped universe and designated 40 contracts as a reusable, near-global exclusion overlay. `DOTUSDT` and `POLUSDT` were added during the second pass. `LITUSDT` remains approved despite limited daily history; coverage failure is handled at the asset/timeframe cell rather than by global exclusion. The next PRI development work uses all 60 remaining approved contracts, preserves their original frozen ranks and snapshot, and does not substitute any contract from outside the original frozen 100. The earlier 100-contract runs remain valid only for their exact frozen population and are descriptive predecessors, not evidence for the revised 60-contract population. No new plan, empirical run, code change, replication/holdout access, live runtime, capital mutation, commit, or push occurred.

### 2026-08-15 — development interpretation checkpointed; ordered path is next

Destin accepted the explanation for the small fixed-H signed means: they net substantial winners and losers and measure signal-close to exact horizon-close persistence, not the magnitude of the visible price leg or expected trade return. Fixed-H continuation after episode termination remains a descriptive counterfactual only. Episode-constrained closes and MFE/MAE probabilities also remain incomplete trading evidence because they do not encode path order, target fills, or scale-out behavior. BTC `5m` was independently reconstructed from 10,001 cached candles; all 1,568 saved events and every H1–H6 outcome matched recomputation exactly, with zero fixed-return formula discrepancy. A full-series interactive BTC trace was retained as a semantic review aid.

The next primary development estimand is ordered first passage from the signal close: whether and when executable highs/lows reach favorable thresholds before PRB or the next PRI, including the terminating candle's extremes, with no-hit terminal return recorded. H1–H6 stays as dense timing resolution but no longer caps observation; extend through H8/H12/H24 and full episode duration. Prior-PRI levels as actual targets and scaling out on the way to a full target remain a separate full-system capture study.

Universe audit found that the frozen selector filters the active Binance ranking to internal-catalog symbols before taking 100. Forty-seven members of the raw exchange top 100 were therefore replaced in the studied mapped universe. Existing run IDs remain valid for their exact frozen population, but no literal Binance top-100 claim should be made. Universe selection, including possible blacklist and durable eligibility rules, must be repaired or explicitly accepted before another pooled all-asset run. Replication and holdout remain sealed; no new empirical run, code change, live runtime, capital mutation, commit, or push occurred.

### 2026-08-14 — H1–H6 probability development pass completed

Added exact fixed-H close returns and retained the separate episode-constrained close return, while leaving MFE/MAE and episode termination semantics unchanged. Completed seven canonical development runs from cache-first Binance evidence; missing spans were fetched through the standard backtest loader and durably verified before artifact creation. All 84 side/timeframe/horizon groups are present, every artifact checksum verifies, and more than 11 million exact probability-curve points pass denominator, reached/not-reached complement, and count/probability identities. Fixed-H mean, median, and positive probability frequently disagree because of skew, while every episode-constrained H6 positive-close probability is below 50%; exact MFE/MAE threshold curves remain available for interactive review. Replication and holdout remain sealed. Twenty-six focused tests plus Ruff and strict mypy pass. No controls, target selection, retest, PRZ, costs, execution, live runtime, capital mutation, commit, or push occurred.

### 2026-08-14 — corrected full development pass completed

Completed one checksum-verified corrected development run per timeframe across 651 frozen cells and 527,474 PRI episodes. The median active episode is four bars on every timeframe, with only about `0.6–2.7%` reaching H24; most episodes instead end at a later same-side or opposite-side PRI. Terminal-close directional response generally becomes adverse after the first bar, but intrabar MFE and MAE are much more balanced, so this pass does not support treating terminal closes as the sole capture outcome. The next constructive question is whether a bounded first-touch or limit-capture mapping can harvest favorable excursion before adverse movement or episode termination. Replication and holdout remain sealed; no controls, retest, PRZ, costs, execution, live runtime, capital mutation, commit, or push occurred.

### 2026-08-14 — next-PRI episode lifecycle corrected and first slice rerun

Destin clarified that every subsequent PRI ends the active episode, whether it is same-side or opposite-side, and that high/low path outcomes matter because limit orders can capture intrabar prices. Updated the offline outcome engine so episodes end at the earliest PRB, next PRI, or horizon; the terminal candle's full range remains included and simultaneous PRB plus next-PRI triggers are retained. Twenty-one focused PRI tests plus scoped formatting, Ruff, and strict mypy pass. Corrected BTC/ETH/SOL `5m` development run `0a98a7c2-7f91-482f-9a2d-4d155102a221` completed with eight checksum-verified artifacts. On the reviewed BTC example, the next same-side PRI ends the episode at bar 7, leaving H1/H3/H6 unchanged and terminating H12/H24 at that shared boundary. Earlier `1m`/`5m` outcome runs are superseded; replication and holdout remain sealed. No controls, retest, PRZ, strategy economics, live runtime, capital mutation, commit, or push occurred.

### 2026-08-14 — return-blind PRI event marks verified

Completed review run `acec7fd5-3c6c-459e-a45d-1c4bfdae4319`, linked to the canonical plan. The selection rule was frozen before candle access: first, middle, and last frozen ranks among assets with all seven development cells, resolving to BTC, STRK, and XAI; within each cell, select the event nearest the midpoint for each direction. All 42 resulting prior/signal pairs satisfy the confirmed candle-color and strict prior-range reclaim rules. The artifact schema contains no future candle or outcome field and its manifest explicitly records `outcomes_computed=false`. Initial run `8d4f7643-e597-4fad-a29f-b37a8be8defd` failed at UUID serialization before artifact persistence and remains as an explicit failed manifest; the typed rerun completed with checksum-matching artifacts. No replication or holdout candle was loaded, and no PRB, return, MFE, MAE, economics, live runtime, or capital path was evaluated.

### 2026-08-14 — current Binance universe and chronological evidence plan frozen

Persisted canonical plan run `58ab2173-196c-410b-af3a-996cdba6cc38` from a live Binance USD-M exchange/ticker snapshot and the stored verified lifespan table. The plan freezes 100 mapped active perpetuals, horizons `1/3/6/12/24`, full verified `1d` histories split chronologically into thirds, fixed three-block intraday windows, one causal pre-roll bar, and no cross-boundary outcomes. It has 2,029 runnable cells and 71 explicit insufficient-history exclusions; all 300 daily cells are runnable. Artifact checksums match the completed manifest. No candle load, PRI outcome, holdout inspection, live runtime, capital mutation, commit, or push occurred.

### 2026-08-14 — PRI offline study foundation implemented and verified

Added the isolated `event_study/pri` package for exact closed-bar PRI events, primary-open PRLs, secondary directional extremes, strict close-through PRBs, PRB-censored directional return/MFE/MAE, explicit right censoring, independent overlapping events, per-side/per-asset/per-timeframe summaries, and typed checksum-registered artifacts without a pooled headline. Added a read-only Binance 24-hour ticker parser and deterministic current-liquidity universe ranking over active mapped USD-M perpetuals. Corrected the MON-177 shared artifact default from `mm_v04/.research/runs/` to the KB's ignored `mm-knowledge/.research/runs/` and reject explicit artifact roots anywhere inside the application repository. Verification passed across 63 focused and Binance regression tests; scoped Ruff and strict mypy are clean. No market-data fetch, empirical run, live runtime, capital mutation, commit, or push occurred. Windows, horizons, and control matching remain frozen-before-run decisions.

### 2026-08-14 — initial PRI study semantics and deployment target frozen

Created the durable PRI research thread from the Trading Catalog and Destin's clarifications. Froze the bullish/bearish three-condition reclaim, primary open PRL, strict close-through PRB, secondary directional extreme, PRB-censored MFE/MAE, exclusion of post-PRB movement, Binance USD-M current-liquidity top-100 population, and seven separate timeframes. Retest, PRZ, capture, economics, execution, and live paths remain outside the first study. Historical evidence windows, forward horizons, exact control matching, and a bounded Linear execution issue remain open. No backtest, code, live runtime, capital mutation, commit, or push occurred.

### 2026-08-14 — Price Reversal System project and PRI execution issue created

Created the active [Price Reversal System Research](https://linear.app/money-machine/project/price-reversal-system-research-1b1579ea6126) project for PRI, PRL, PRZ, PRB, the combined lifecycle, later capture, and cost-valid evaluation. Created High-priority Ready issue [MON-226](https://linear.app/money-machine/issue/MON-226/validate-pri-and-run-the-initial-prb-censored-event-study) as the first bounded packet. MON-226 mirrors the frozen PRI semantics, universe, timeframes, controls, evidence boundary, stopping rule, durable closeout, and offline-only safety boundary; it is related to completed provenance issues MON-89 and MON-169. No backtest, code, live runtime, capital mutation, commit, or push occurred.
