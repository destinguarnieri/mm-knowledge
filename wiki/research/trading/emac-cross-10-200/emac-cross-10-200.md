# EMA Cross 10/200 Research

Status: in progress

Related process: [[research/trading/research_process_v2|Research Process V2]]
Signal-stats event study: [[event_study_anchor_findings|Anchor + Holdout Findings]] · label definitions [[event_labels_v1|Event Labels V1]]

<!-- ================= LIVING HEAD — rewrite in place each session ================= -->

## TL;DR & What's Working

Testing whether the near-parameter-free EMA 10/200 family carries tradable edge, and how to monetize it. **Directional and traversal evidence is promising, but the version ladder is not yet comparison-ready: basic cross coverage is incomplete at 1D, continuous V1 lacks a clean baseline program, V4 economics are sparse, and V5 has no backtest evidence.**

**What's working — live threads worth capturing:**

- **Direction is promising where tested.** Positions sit in profit for `77.84%`–`88.21%` of active bars across BTC intervals (and ~`84–88%` median across the multi-asset 4h batches), despite only `10–28%` realized win rates. That gap is a *capture/exit* problem, not a direction problem. The boundary matters: basic `emac_cross` has multi-asset coverage at 4h and selected lower intervals, but its 1D result is BTC-only. Cites: BTC scan `ce0bc93e` (1d) → `987817d2` (1m); 20-asset 4h batch `3c0f2043`.
- **A real 4h leader cluster.** SUI, ETH, ARB, DOGE cleared Sharpe `1.0` in the 20-asset 4h batch (`3c0f2043`); roughly 30–40 assets show usable 4h/1h stats. ETH is the strongest risk-balanced name.
- **Escalation ladder — most monetizable structure found so far, and it generalizes.** In the signal-stats event study, mean→±2σ band-to-band traversal is positive with payoff *and* hit rate rising up the ladder: mean→2σ hit `94%` (anchor) / `96%` (holdout), with conditional touch rates stable across two disjoint 50k-bar windows (P(1σ|mean) ≈ 0.69–0.71, P(2σ|1σ) ≈ 0.62–0.63). **Net positive at realistic maker costs (~1–2 bps/side)** — the ~20 bps figure that earlier read as a kill is a max-taker *ceiling*, not a floor. Cites: anchor `8077b0dd`, holdout `9c96c57f`; full numbers in [[event_study_anchor_findings]].
- **Cross-asset generalization on 5m confirmed (leg 1, 2026-07-23).** The ladder is not BTC-specific: across a 20-asset cross-section of the ≥$250k Hyperliquid universe (majors + high-vol alts), P(1σ|mean) sits at `0.63–0.71` on every asset vs an unconditional mean-touch base rate of only ~`0.45–0.54`, P(2σ|1σ) is always `0.53–0.70`, and mean→2σ traversal is positive on all 20 at a mid-90s% hit rate (`91–98%`). Higher-vol alts show *larger* per-rung bps (better edge-to-fixed-cost ratio). The naive mean-cycle (S1-in/S4-out) stays negative-median everywhere — the band-to-band *traversal*, not the naive cycle, is the capture target. Artifacts + run pointers in the Write Log entry below; leg 2 sweeps the timeframe axis.
- **Cross-timeframe invariance confirmed on BTC (leg 2, 2026-07-23).** Same config swept over `1m/5m/15m/30m/1h/4h/1d`: the *conditional structure is timeframe-invariant* — P(1σ|mean) stays `0.65–0.71` and P(2σ|1σ) `0.58–0.66` across `1m`→`4h`, mean→2σ hit `93–100%` — while the *payoff scales monotonically with timeframe*: median mean→2σ traversal `+17 → +56 → +75 → +115 → +224 → +404 bps` from `1m` to `4h`. So the edge-to-cost ratio improves up the timeframe ladder: `1m` (+17 bps) is thin vs maker round-trip (~2–4 bps) but net positive; `≥15m` is comfortable. The naive mean-cycle stays negative through `4h`. `1d` is unreliable (14 legs, 2 mean→2σ obs). Side note: the flip-only *control* Sharpe also climbs with TF and turns positive at `4h` (+0.96) — same "bigger moves vs fixed cost" mechanism.
- **Timeframe-invariance confirmed off-BTC (leg 2 tail, 2026-07-24).** Ran the `1m` and `1h` extremes on ETH/SOL/DOGE/AVAX. Both BTC signatures replicate on every asset: at `1m`, P(1σ|mean) `0.63–0.69`, P(2σ|1σ) `0.59–0.62`, mean→2σ hit `91–96%`, median payoff `+17–30 bps`; at `1h`, P(1σ|mean) `0.67–0.69`, mean→2σ hit `91–96%`, median payoff `+224–556 bps` (higher-vol AVAX/SOL largest), mean-cycle negative on all. So the ladder is a joint asset×timeframe invariant, not a BTC or 5m artifact. Pointers in the Write Log entry below (`panel_tf_extremes_escalation.csv`).
- **Capture vehicles exist in code, not yet in comparable evidence.** Unthresholded continuous `emac` V1, transition-only thresholded `emac_v4`, and thresholded continuous `emac_v5` provide the right attribution ladder. Existing direct-`emac` runs were incidental to universe-filter work rather than a frozen baseline; V4 economics cover only a few BTC fixtures; V5 passes focused implementation tests but has no backtest.

**Best next step:** pause [MON-210](https://linear.app/money-machine/issue/MON-210/complete-the-multi-asset-1d-emac-cross-control) until Destin repairs and verifies the broken `emac_cross` strategy implementation. The 2026-08-07 fixed-floor batches are invalid because many assets returned zero/no metrics; they support no economic or generalization conclusion. After repair, rerun MON-210 from its frozen 100-asset population and assumptions. Do not use the invalid batches as the control for [MON-211](https://linear.app/money-machine/issue/MON-211/establish-the-unthresholded-continuous-emac-v1-baseline) or [MON-165](https://linear.app/money-machine/issue/MON-165/compare-thresholded-continuous-emac-v5-with-continuous-v1-and-v4). Band-to-band monetization remains an independent capture branch.

## Current Read (provisional — not a verdict)

Living per-question status. A row only becomes a recorded **Decision** at a promotion gate (Research Process V1 §12) or an explicit kill; until then it stays provisional.

| Question | Current read | Confidence | Key evidence | What would change it |
|---|---|---|---|---|
| (B) Does 10/200 put you on the right side? | Leaning strongly yes | Med–High | `77.8–88.2%` time-in-money across intervals and multi-asset batches | fails on a fresh untouched holdout or a different venue |
| (A) Can dead-simple flip-only make money as-is? | Leaning no (flip-only) | Med | flip-only net-negative after costs at ≤1h; severe drawdown at 1d/4h | a real selection rule clears net after realistic costs |
| (C) Can a capture mechanism monetize the 80%? | Open — top priority | Low (early) | escalation ladder net-positive at maker cost; V4/V5 built | a mean-cycle / continuous variant beats the control out-of-sample |
| (D) Is the EMAC version ladder comparison-ready? | No | High | 1D basic cross is BTC-only; no clean continuous-V1 baseline; V4 sparse; V5 untested economically | matched V1/V4/V5 fixtures plus multi-asset 1D control |

Reframing note: this doc previously carried a hard "Verdict" table calling (B) *Supported* and (A) *Kinda/maybe*. The substance is unchanged — (B) strong, (A) weak as flip-only — but it is now tracked as a provisional read, because no promotion/kill gate has been run and the capture question (C) is still open.

## Coverage Audit

| Variant | Evidence actually available | Material gap | Linear |
|---|---|---|---|
| Basic flip-only `emac_cross` | BTC across `1m`–`1d`; broad multi-asset 4h; selected cohorts at `1h`/`30m`/`5m` | Strategy implementation is broken; the attempted full-universe 1D batches are invalid and must be rerun after repair | [MON-210](https://linear.app/money-machine/issue/MON-210/complete-the-multi-asset-1d-emac-cross-control) — Blocked |
| Unthresholded continuous `emac` V1 | Direct-position runs exist inside universe-filter qualification/evaluation work | No frozen standalone baseline; run the full `>$250k` universe at `5m`/`1h`/`4h`/`1d` before attributing V5 improvements | [MON-211](https://linear.app/money-machine/issue/MON-211/establish-the-unthresholded-continuous-emac-v1-baseline) — Ready |
| Transition-only thresholded `emac_v4` | Transition correctness and a few BTC 1D/5m fixtures; extensive event-study configuration use | Sparse matched economic coverage across assets/timeframes | [MON-165](https://linear.app/money-machine/issue/MON-165/compare-thresholded-continuous-emac-v5-with-continuous-v1-and-v4) — blocked on MON-211 |
| Thresholded continuous `emac_v5` | Focused semantics/tests only | No backtest; no matched V1/V4 panel | [MON-165](https://linear.app/money-machine/issue/MON-165/compare-thresholded-continuous-emac-v5-with-continuous-v1-and-v4) — blocked on MON-211 |

## Open Threads / Next Experiments

Ranked by expected information value:

1. **Repair before rerunning the control surface.** MON-210's 100-asset snapshot remains frozen, but its attempted 1D `emac_cross` batches are invalid. Wait for Destin to repair and verify the strategy, then rerun all eligible assets and report source/history exclusions rather than silently narrowing the universe. Do not infer from zero/no-metric rows.
2. **Compare the version ladder.** After MON-211, fill matched V4/V5 cells across the same frozen liquid universe in MON-165. V1 vs cross isolates continuous sizing; V4 vs cross isolates threshold gating; V5 vs V4 isolates continuous magnitude inside the threshold regime; V5 vs V1 tests whether gating helps continuous sizing.
3. **Capture the 80%.** Independently spec a bounded mean-cycle variant (S1 entry / S4 mean-retreat exit, optionally escalation-aware) and evaluate against the flip-only control on both event-study fixtures. The hinge is cutting the non-escalating branch cheaply. See [[event_study_anchor_findings]] bottom line.
4. **Dynamic vs static thresholds.** Thresholds derived causally from the signal's own rolling mean/σ (no lookahead) versus static controls, on the same fixtures.
5. **Selection rule, done right.** If an asset/universe filter is reopened, pre-register the rule and consume a genuinely untouched window exactly once. Standing post-hoc leads (candidates only): lower prior cross count; high 4-bar variance ratio + high 1-bar return autocorrelation.
6. **Rolling-lens breakout episode** (Destin, 2026-07-22): enter on rolling ±2σ breach, exit on close back inside; needs a rolling-lens episode builder plus economics on both fixtures.
7. **Compression/expansion market-state label** — pending Destin's corrected phrasing before re-running the chop split.

Deferred: timeframes outside the frozen `5m`/`1h`/`4h`/`1d` comparison and any parameter sweep. Within those cells, full eligible-universe coverage is required; a handpicked representative panel is not sufficient.

<!-- ================= STABLE ================= -->

## Strategy & Data Facts

- Strategy ladder: `emac_cross` is the basic flip-only EMA 10/200 control; `emac` V1 (strategy `be3545d2`) is the unthresholded continuous signal-to-position control; `emac_v4` is transition-only threshold gating; `emac_v5` adds continuous magnitude inside the V4 threshold regime.
- Data depth: Hyperliquid serves only ~5,000 candles per timeframe; Binance USD-M provides full history via `candle_source: binance_usdm` (explicit `start_ms`/`end_ms`, 50,000-candle single-run cap, non-US egress). See [[vendors/binance-market-data-access|Binance Market Data Access]].
- Positioning family so far: flip-only, `sig_to_position` (amplitude → target) and its inverse, continuous V5, and a proposed quantile-regression mapping (Q90/Q50/Q10 with proximity-to-quantile sizing weighted by r²). Build philosophy: start simplest, add complexity progressively. All-in/all-out is the intentional control condition, not the destination.
- Methodology: asset selection is an explicit optimization axis for trend strategies (assets differ in serial correlation / trending behavior).
- Timeframe priority (Destin, 2026-07-20): prefer `1m`/`5m`; the higher the timeframe the less weight. Fast-interval flip-only rejections are verdicts on that monetization rule, not on the intervals.
- Started: 2026-07-11 00:18 EDT. Initial asset: BTC; liquid-universe screen used a point-in-time `$250,000` rolling 24-hour Hyperliquid notional-volume floor.

## Diagnosis — why flip-only leaks the edge

`pct_time_in_money` is the fraction of active bar snapshots whose position ROE is positive; it is not a direct signal-classification accuracy measure. Even so, `77.84%`–`88.21%` time-in-money alongside only `10.22%`–`28.07%` realized win rates is the core signal: positions are profitable during most active bars, but the hold-until-opposite-cross exit gives the favorable excursion back before realization.

Two failure textures, separated by worst position ROE vs portfolio drawdown:

- `1d`/`4h` allow large adverse in-position excursions (worst ROE `-17.93` / `-32.85` pts) alongside severe portfolio drawdowns.
- `1h`→`1m` keep worst individual adverse ROE small (`-4.18` to `-0.94` pts) yet still accumulate `-25.85%` to `-36.94%` portfolio drawdowns through repeated losses and costs.

Implication: the fix is profit retention + churn reduction (better exit / scale-out) and asset selection — not widening the EMA parameter search. Destin's selected-cohort Hyperliquid `1h`/`30m` runs also show interval rejection must be asset- and venue-specific, not inferred from BTC alone.

## Fixed Baseline Assumptions

- Candle source: Binance USD-M perpetual `BTCUSDT`.
- Initial capital: `$10,000`.
- Position sizing: compounding.
- Maximum position: `100%` of equity at `1x` leverage.
- Fee rate: `0.0005` (`5 bps`).
- Slippage input: `5.0` (`5 bps`; this field is expressed directly in basis points).
- Initial state: flat until the first observed cross; subsequent crosses flip between maximum long and maximum short.
- Funding is absent from OHLCV results and remains an explicit limitation.
- Timeframes may require different calendar windows because the explicit-request cap is 100,000 candles. Cross-timeframe results are therefore intuition-building, not a controlled ranking unless their windows overlap.

<!-- ================= APPEND-ONLY TAIL — do not edit past entries ================= -->

## Run Registry (pointers, not tables)

Identity + interpretation index. Metrics live in Destin's backtest UI and in persisted saved runs — re-fetch via Research MCP `get_saved_run` / `get_saved_batch_run` rather than pasting tables here. Cumulative reviewable asset-window evaluations: `86` successful.

**BTC timeframe scan (Binance USD-M):**

- `ce0bc93e-01c6-41cb-8a2b-3b08a5ef26a1` — BTC `1d` — positive absolute return, weak Sharpe, severe drawdown; continue-scan quality, not a candidate.
- `78ee3fe1-ee12-40d7-b68c-e962344d8652` — BTC `4h` — strongest BTC interval by Sharpe/profit factor, but extreme drawdown; the reasonable interval for a first cross-asset screen.
- `2c8223d5-4c4a-445e-82ac-cbd957379c14` — BTC `1h` — ~flat gross edge → negative after costs. Flip-only monetization rejected on this interval, not the directional signal.
- `756fade0-fc72-4397-96be-8790607f9080` — BTC `30m` — negative before and after fees despite high time-in-money.
- `e40c891e-8302-4317-b588-5a00a9a5a169` — BTC `5m` — structurally poor over the short recent sample.
- `987817d2-0c0f-406d-aa92-09b0da5fae38` — BTC `1m` — rapid churn overwhelms the rule over a one-week sample.
- A 57,192-bar BTC `1h` attempt completed computation but failed autosave.

**Cross-asset 4h batches:**

- `3c0f2043-aeac-44da-945f-523965b33c97` — 20-asset 4h — 19/20; SUI/ETH/ARB/DOGE cleared Sharpe `1.0`; coherent leader cluster with ETH best-balanced; monetization gap generalized. MATIC failed cleanly on missing post-delisting history.
- `8c3d5e49-5026-4146-a7be-d7fe1a6a1f7f` — 30-asset liquid 4h — broader breadth weakened the median; ZEC high headline Sharpe but fails risk/cost.
- `c98d9c89-971c-440a-9647-44929937e3bf` — 32-asset liquid 4h — 11/32 full history; no clean new leader (HBAR/IOTA fail risk).
- `28a4f773-c94c-48c1-892f-de1ff8ce6ab0` — MEGA 4h history check — insufficient candles; joins the new-listing cohort.
- `a32d01a7-096b-4ba8-b17f-b3c35baad2c3` — 29-asset 2,500-candle 4h cohort — weak aggregate; POL and PAXG materially better than cohort median.
- `687ef1b4-2043-4fc3-8742-5330d2ec415a` — 9-asset 1,000-candle 4h cohort — HYPE/MET/MON positive but only 4–8 trades → watchlist observations, not ranking-quality.

**Selected-cohort Hyperliquid (Destin's 4h leaders on lower timeframes):**

- `351ecce1-bb07-4b15-82e6-a1a9dccf1fac` — `1h` — materially stronger than the BTC-alone 1h rejection implied; falsifies "lower intervals are dead." Selected-set / different-venue caveat.
- `a8e58e9a-7ed8-4062-9008-0588d6b60475` — `30m` — remains live for this set; do not close from BTC alone.
- `1059fdc6-ad67-411e-94b3-9bedd21de364` — `5m` — cohort mostly collapses; weak/failed for the current flip-only rule.

**Direct-position `emac` + universe-filter holdouts (2026-07-23):**

- eval `aa84b35a-1ca6-4776-be07-dfeec643297a` (`emac_cross` 30m) vs qualification `61a85dcb`/`acdeb9f8`/`07d5b326` (+corrected `9ee37d7d`, `fafee3b7`): prior-winner persistence weak (3/9 repeated); reject a deployment universe filter from this evidence. Winner label = positive net return and Sharpe > `1.0`.
- eval `eac34bc8-49f6-4a19-b64b-960c08be6862` (direct `emac`, strategy `be3545d2-e597-41c7-a508-9f7be7b8d46d`) vs qualification `ba6c9314`/`c6251adf`/`44126629`: prior-strategy performance anti-predictive; freeze high 4-bar variance ratio + high 1-bar autocorrelation as a post-hoc candidate only, requiring a genuinely untouched window before any use. One cross-venue temporal split, not multi-fold walk-forward.

**Signal-stats event study:**

- anchor `8077b0dd-e440-48d7-8e64-a4ef81d1074e` (BTC Binance USD-M 5m, 49,800 scored bars, ~Jan 28 → Jul 19 2026) + Hyperliquid screenshot companion `d82eda65-aaf0-4a76-b536-12921c6682bb`; holdout `9c96c57f-733d-4b0b-a063-9a8824349d80` (disjoint ~Aug 7 2025 → Jan 27 2026). Findings and label definitions: [[event_study_anchor_findings]], [[event_labels_v1]].

**Continuous/version-control development:** direct `emac` V1 runs in the universe-filter section are not a clean baseline program. V4's saved sequence (`a1688414` discarded config mismatch; `6108178a`, `eea81901`, `b12d3a50`, `bad11f56`, `f2299e5b`, `e43db176`, `43036e20`, `e58f3c5d`) primarily establishes transition correctness on sparse BTC fixtures. V5 has no saved backtest run.

## Preliminary Risk-Filtered Top 10 (screen, not a promotion gate)

Selection requires positive net return, profit factor above one, maximum drawdown better than `-70%`, and worst position ROE better than `-25` percentage points, then ranks by Sharpe:

1. SUI
2. ETH
3. ARB
4. DOGE
5. kBONK
6. kPEPE
7. XLM
8. WLD
9. BTC
10. SEI

ZEC, HBAR, and IOTA rank highly on headline Sharpe but fail the stated risk filter.

## Write Log

### 2026-07-11 00:18 EDT

Opened the BTC 10/200 baseline timeframe scan. The first run is BTC `1d`; each result will be interpreted before advancing to the next interval.

### 2026-07-11 00:20 EDT

Completed BTC `1d` run `ce0bc93e-01c6-41cb-8a2b-3b08a5ef26a1`. The run loaded all 2,383 requested Binance candles and scored 2,183 after warmup. Net return was positive, but `0.471` Sharpe and `-45.77%` maximum drawdown indicate poor risk-adjusted quality. Continue to `4h` to learn whether the faster interval improves responsiveness without allowing turnover and costs to dominate.

### 2026-07-11 00:40 EDT

Completed the remaining BTC timeframe scan. The six-year `4h` run materially outperformed `1d` on Sharpe (`0.935` versus `0.471`) but suffered `-68.25%` maximum drawdown. A 57,192-bar `1h` attempt exposed an autosave timeout after generating roughly 250,000 artifacts, so the reviewable `1h`, `30m`, `5m`, and `1m` runs were limited to 10,000 requested bars each. All four were net-negative; deterioration accelerated as interval length shortened. Next question: does the fixed 10/200 configuration show a coherent `4h` edge across other assets, or was BTC performance asset-specific?

### 2026-07-11 01:08 EDT

Revised the interpretation to include time in money and worst position ROE. Every interval spent at least `77.84%` of active bars with positive position ROE, despite low realized win rates. The combination points to profit giveback and poor exit monetization rather than a clean rejection of directional information. Worst position ROE is now tracked alongside portfolio maximum drawdown for every run.

### 2026-07-11 01:48 EDT

The existing shared-config Research MCP batch path now supports Binance USD-M with per-asset symbol derivation and partial failure isolation. The request bound is 32 assets while execution concurrency remains eight. This removes the tooling blocker for the planned `4h` cross-asset screen; no new strategy result was produced in this implementation step.

### 2026-07-11 02:04 EDT

Completed 20-asset Binance USD-M `4h` batch `3c0f2043-aeac-44da-945f-523965b33c97`. Nineteen assets completed across a common 5,000-candle window; MATIC failed cleanly on missing post-delisting history. ETH, SUI, ARB, and DOGE cleared Sharpe `1.0`, but median profit factor remained below one and median maximum drawdown was `-64.38%`. The high-time-in-money/low-realized-win pattern persisted across the batch, strengthening the profit-retention diagnosis. Pause before wider screening to choose whether the next test should validate the leader cluster or modify exit monetization.

### 2026-07-11 02:28 EDT

Applied a point-in-time `$250,000` rolling 24-hour Hyperliquid notional-volume floor and expanded the common-window screen through three additional batch calls. The two substantive runs requested 30 and 32 assets; a final one-asset MEGA check completed the known liquid set available within the first 200 Research MCP assets. Thirty-four additional assets produced reviewable results and 29 liquid assets lacked the full 5,000-candle Binance window. Broader breadth weakened the median outcome and produced no cleaner leader than ETH. Formed a preliminary risk-filtered Top 10 for lower-timeframe testing while keeping the 29 newer assets in a separate cohort.

### 2026-07-11 02:38 EDT

Worked backward through the 29 incomplete-history assets. A common trailing 2,500-candle run recovered 20 assets; a trailing 1,000-candle run recovered seven of the remaining nine. POL and PAXG were the strongest shorter-history results. HYPE, MET, and MON were positive in the 1,000-candle cohort but produced only 4–8 trades, so they remain provisional. APEX has no Binance USD-M symbol and MEGA is 31 candles short of the 1,000-candle requirement. Kept all three calendar-window cohorts separate to avoid biased ranking.

### 2026-07-12 15:40 EDT

Destin rejected premature closure of lower timeframes from BTC-alone Binance results and ran selected 4h leaders on Hyperliquid `1h` (`351ecce1-…`), `30m` (`a8e58e9a-…`), and `5m` (`1059fdc6-…`). The `1h`/`30m` cohorts remain live; `5m` mostly fails under the current rule. Accepted methodological correction: asset selection is part of optimization for a trend strategy because assets differ in serial correlation / trending behavior. Remaining work is not “prove it on every asset,” but define a reusable selection rule and test whether selected-asset + interval claims survive holdout time and realistic costs/risk. Research MCP saved-batch 404s for Destin-owned runs retrieved by a non-superuser agent are under Destin's investigation as an auth/scoping issue.

### 2026-07-12 15:58 EDT

Closed the primary EMA-cross research loop against Destin's actual questions. (B) Directional usefulness of 10/200 is supported by `% time in money`. (A) Dead-simple prod monetization is only a weak/maybe under selection; Destin would prefer better entry/exit controls and does not want exhaustive further research on this flip-only rule. Optional one–two cleanup runs only; next move for expansion of this exact strategy: none.

### 2026-07-15 03:03 EDT

Started behavioral-parity work for `emac_v4` using Threshold Engine V3. The comparison target remains BTC Binance USD-M `1d`, 2020-01-01 through 2026-07-10 UTC, EMA 10/200, `$10,000`, 100% equity at 1x, compounding sizing, `0.0005` fees, and `5.0` bps slippage. Saved artifacts from baseline run `ce0bc93e-01c6-41cb-8a2b-3b08a5ef26a1` confirm compounding sizing: post-loss flips target reduced current equity rather than restoring a static `$10,000` notional.

Two diagnostic V4 runs completed. Static run `a1688414-48d3-430b-88b1-1cfe6a0bc802` was intentionally discarded as a configuration mismatch. Exact compounding run `6108178a-4411-41c8-bd13-fe0f9777aab3` proved that the zero-level paired V3 rules are accepted, but failed parity through repeated hold-period resizing. Its first short also occurred one bar before the baseline because rolling min-max normalization emitted zero while the raw EMA spread remained positive, and V3 treats landing on the threshold as a crossing. Decision: resolve these two behavioral mismatches before varying thresholds or evaluating economics.

### 2026-07-15 03:11 EDT

Updated `emac_v4` so order execution occurs only when Threshold Engine V3 reports a state-changing transition; unchanged state now holds the existing position without resizing. Added a focused negative-path test for a materially off-target existing position with no transition. Ruff, compilation, strategy mypy, and IDE diagnostics pass. The identical baseline rerun returned 503 after backend reload because the backtest manager was stopped, so behavioral parity remains unverified. Min-max normalization remains the accepted control signal.

### 2026-07-15 03:13 EDT

Completed the transition-only V4 baseline run `eea81901-fc13-44f0-b2a0-b727e6a83d52` on the identical BTC Binance USD-M `1d` fixture. The resizing defect is resolved: V4 produced 19 orders instead of the pre-fix run's 928, versus 23 for `emac_cross`. The remaining event difference is expected from the accepted V4 identity: rolling min-max emits exact zero samples, while V3 triggers when landing on a threshold and does not retrigger when starting exactly on it. This shifts the first short one bar earlier and merges several rapid raw-spread flips. Treat this saved run as the V4 zero-threshold baseline for incremental threshold work, not as exact event parity with raw `emac_cross`.

### 2026-07-15 03:33 EDT

Ran symmetric hysteresis candidate `b12d3a50-b3e9-4c4a-b8ed-4fb10a604f5b` on the identical fixture: long entry/short exit at `+0.01 CROSS_OVER`, long exit/short entry at `-0.01 CROSS_UNDER`. The run completed with 16 trades, reducing turnover and improving drawdown versus the zero-threshold V4 baseline, but weakening return and Sharpe. Treat this as a positional-control comparison for visual review, not a promotion decision.

### 2026-07-15 23:27 EDT

Completed `MON-146` verification with full-artifact run `bad11f56-d676-4577-92a0-4527b3577f92` on the identical BTC Binance USD-M `1d` fixture. The strategy now compares consecutive decision-time emitted min-max values. The visible 2023-03-13 to 2023-03-14 move from `0.0094370696` to `0.0368437059` immediately flipped the stale short to long on March 14; it no longer remained short through August. The corrected path produced 18 trades. Treat this run as the canonical symmetric `±0.01` V4 baseline for subsequent threshold work.

### 2026-07-15 23:44 EDT

Corrected the shared signed-magnitude min-max series contract without changing its normalization formula. Every array index now uses only the trailing window ending at that index and matches the scalar value that would have been emitted from the corresponding prefix. The full-series path uses SciPy's compiled O(n) one-dimensional min/max filters with explicit non-finite sentinels; unbuffered current-value consumers use a dedicated scalar path, while history-dependent buffers consume the causal series. Summary rerun `f2299e5b-bc39-44d1-ac1d-0644df0b6cef` reproduced the canonical V4 baseline metrics exactly, confirming the V4 emitted-history behavior is unchanged.

### 2026-07-16 00:16 EDT

Standardized the processing API as `process_signal()` for causal full-series consumers and `process_signal_last()` for current-value-only consumers; removed the misleading `normalize_signal` name and updated all callers. Because V4 needs the previous processed value, it now consumes `process_signal(...)[-2:]` directly and no longer maintains strategy-local emitted history. Ring buffers remain reserved for true streaming boundaries where complete source history is unavailable. Summary run `e43db176-6384-460d-a663-61e2e9f87807` exactly reproduced the canonical V4 baseline metrics.

### 2026-07-20 00:45 EDT

Corrected the preceding no-ring decision after BTC 5m run `43036e20-bce1-47d6-88f1-b7cc339f75a9` exposed four missed threshold transitions. The scaler's causal series is prefix-correct for one input array, but the backtester's sliding 512-bar input window changes the EMA seed and can rewrite the recomputed penultimate EMAC value. EMAC V4 again retains the last two actual decision-time emissions per asset/timeframe while continuing to use the causal full series for current signal statistics and slope overlays. Corrected full run `e58f3c5d-e501-4105-9278-f1bcc3ee2b7f` executed all four previously missed transitions with no new transition mismatches. Treat consecutive emitted values—not adjacent values recomputed from a later sliding window—as the threshold-crossing identity contract.

### 2026-07-20 03:15 EDT

Ran fresh BTC Hyperliquid 5m anchor `d82eda65-aaf0-4a76-b536-12921c6682bb` for the signal-stats event study (full retention, `emac_v4` defaults, ±0.01 hysteresis, $10k/1x/5bps+5bps). A 20,000-bar request failed: Hyperliquid 5m history only reaches back to ~2026-06-28 (~6,100 bars), so the anchor uses the maximum clean 5,600-scored-bar window (~June 30 → July 20 UTC). Flip-only behavior on this window matches the standing diagnosis: heavy churn, low realized win rate, high time-in-money. Separately, prior 5m run `e58f3c5d-…` is retrievable via Research MCP (`saved`, full artifacts) but was not visible in Destin's UI table — possible recurrence of the saved-run UI scoping/auth issue from 2026-07-12.

### 2026-07-20 03:30 EDT

Destin confirmed Hyperliquid serves only ~5,000 bars per timeframe and directed depth runs to Binance. After a geo-block fix on his side, ran the primary event-study anchor `8077b0dd-e440-48d7-8e64-a4ef81d1074e`: BTC Binance USD-M (`BTCUSDT`) 5m, 49,800 scored bars (~2026-01-28 → 2026-07-19 UTC), complete candle load, summary retention, same canonical config. Flip-only control economics over the ~6-month window are decisively negative net of costs (net −75.1%, gross −31.7% before fees, 689 trades, 16.1% win rate, 80.3% time-in-money, cost drag 86.8% of initial capital) — the strongest confirmation yet that direction survives but flip-only monetization fails at 5m, and the reference the event-study mechanisms must beat. Learned constraints: `binance_usdm` requires explicit `start_ms`/`end_ms`; single-run `min_candles` cap is 50,000; the Hyperliquid run `d82eda65-…` is retained as the screenshot-parity companion.

### 2026-07-16 02:05 EDT

Destin marked Threshold Engine V3 complete and reframed the next session around three bounded control questions. Static thresholds remain useful experimental controls but are unlikely to be the final solution; dynamic thresholds derived causally from signal statistics such as rolling mean and standard deviation are the stronger hypothesis. Position sizing should also move from discrete full-position states toward a continuous signal-to-target-position mapping using `sig_to_position` or an equivalent function. Next session: compare static controls, dynamic thresholds, and explicit continuous position semantics without reopening broad universe/timeframe expansion.

### 2026-07-23 04:10 EDT

Implemented registered backtest strategy `emac_v5` as the continuous-position counterpart to `emac_v4`. Detail retained in the session change log; superseded as the head focus by the leg-1 generalization work below.

### 2026-07-23 23:40 EDT

Leg 1 of the signal-study expansion (escalation ladder beyond the BTC anchor, on 5m). Extended the read-only event-study tooling so one canonical `emac_v4` config run can be reused per asset off cached candles: `run_event_study` gained `--asset-id`, `fixtures.load_run_fixture` resolves the per-asset `source_symbol` from `backtest_candle` (fails loudly on zero/ambiguous series) and reads the target symbol from the asset catalog so the asset need not belong to the config run, and a new `aggregate_escalation.py` CLI collates one cross-fixture comparison table (writes `output/universe_5m_escalation.csv`). Backend files were edited only during the tooling step (each edit bounces the fastapi-dev backtest manager). Candles cached via Research MCP summary batches over the anchor window (`start_ms 1769505600000` → `end_ms 1784505600000`, 5m, `binance_usdm`); chunk-1 batch run `c9bdf9fe-fcb5-4618-8a8e-1042bb1a1ae1` (MCP poll times out but the backend finishes caching), plus single ETH run `656f267e-3375-4da2-ab3e-3c8fc21d5df0`. Event study run per asset with `--run-id 8077b0dd-… --asset-id <asset>`; artifacts in `mm_v04/backend/app/lib/analysis/event_study/output/<SYMBOL>_8077b0dd-…/` (local, uncommitted).

Result: the escalation ladder generalizes strongly across the tested 20-asset cross-section — see the living head "What's Working". Destin reviewed and called leg 1 good; the mid-90s% mean→2σ hit rate replicating across the universe was the headline. Decision: leg-1 (cross-asset, 5m) is **closed as supported**; do not exhaustively grind the remaining ~90 universe names (confirmatory + thin-history coverage only). Next: leg 2 — sweep the same ladder across the timeframes MM uses (`1m`/`15m`/`30m`/`1h`/`4h`/`1d`) on a representative panel to get the full-picture timeframe dependence. Metrics live in the per-asset artifacts + `universe_5m_escalation.csv`; re-run `aggregate_escalation` to re-read rather than transcribing here.

### 2026-07-23 23:50 EDT

Leg 2 (timeframe axis) — BTC sweep. Reused the anchor recipe (`emac_v4`, params `10/200`, `signal_stats_lookback=200`, `binance_usdm`, costs immaterial to the event study) at each timeframe MM uses; each per-timeframe single run is both the event-study config source and the candle cache. BTC config runs: `1m 916530d8-6863-47a5-8141-314c99378577`, `5m 8077b0dd-…` (anchor, leg 1), `15m f4cb602b-6bd9-4773-8959-081b17827a7f`, `30m 4b8f6e7d-a4c6-4b9f-a1e7-352c6fe188e2`, `1h 3be86756-00f5-4fb3-b9bb-beea20afb1a4`, `4h 6ffedbdc-4349-4b9e-8b8b-e1f003746632`, `1d 9c30124d-744d-4743-b9ca-811e97da101c`. `1m`–`1h` ran full 50k-bar windows (49,800 scored); `4h`/`1d` are listing-capped (13,800 / 2,100 scored). Event studies + interpretations written per run; cross-timeframe collation in `output/btc_timeframe_escalation.csv` (added a `tf_sec` column to `aggregate_escalation.py` and sort by it). Backend edit was tooling-only (bounces the fastapi-dev manager on save).

Result (living head "What's Working" has the full read): conditional structure is timeframe-invariant across `1m`→`4h` (P(1σ|mean) `0.65–0.71`, P(2σ|1σ) `0.58–0.66`, mean→2σ hit `93–100%`), while median mean→2σ payoff scales monotonically `+17 → +404 bps` from `1m` to `4h`. Destin reviewed and accepted ("remarkably consistent, bingo on bps increasing with timeframe"). `1d` unreliable (14 legs). Naive mean-cycle negative through `4h`. Decision: BTC timeframe sweep **supported**; leg-2 tail = confirm invariance on a few non-BTC assets at the timeframe extremes (`1m`+`1h`) before any full panel×TF grid. Metrics live in the per-run artifacts + `btc_timeframe_escalation.csv`; re-run `aggregate_escalation` to re-read.

### 2026-07-24 00:05 EDT

Leg 2 tail — non-BTC timeframe-invariance confirmation. Ran the `1m` and `1h` extremes on a deep-history alt panel (ETH/SOL/DOGE/AVAX), each its own single run + config source (same anchor recipe). Run IDs — `1m`: ETH `9ea7a2cd-448d-4465-8d3e-c49bf3757581`, SOL `cb67d560-f29d-4bdd-81d2-16ddf3f3c653`, DOGE `6a7ebd16-a75a-43aa-a30e-992a0be80db8`, AVAX `6ccdd9a4-eb04-41eb-ad70-e83b2debed89`; `1h`: ETH `c3ea4023-98ed-4695-a19f-de9fd26b1575`, SOL `1d78a2fd-642c-49b3-a9d9-94b2d7f42be3`, DOGE `0f3cf6dc-d184-4430-8ff2-ff0b83ff61ab`, AVAX `a4afedce-6c0a-42a6-bc32-c8f80010d48e` (all 49,800 scored bars). Collation `output/panel_tf_extremes_escalation.csv`. Result: both BTC signatures replicate on all four alts at both extremes (living head has the numbers) — the ladder is a joint asset×timeframe invariant. Decision: **leg 2 complete/supported.** No further universe×TF grid needed to establish generalization; next research move is a decision (spec the bounded band-to-band capture variant vs the flip-only control, and which timeframe(s) to target given the payoff/cost scaling) rather than more coverage. Metrics live in the artifacts; re-run `aggregate_escalation` to re-read. It preserves V4's EMA 10/200 processed signal, emitted-history, slope overlay, signal-stat modes, Threshold Engine V3 configuration, volatility adjustment, position caps, and execution safeguards. Threshold Engine V3 still controls the persistent `LONG` / `FLAT` / `SHORT` regime; `signal_to_position` controls exposure magnitude continuously inside that regime, with the configured target floor and adjustment deadband applied before execution. Threshold state is retained independently from actual position size so a zero-magnitude target does not erase the active regime. V4 remains transition-only and unchanged. Focused V4/V5 tests pass (17 total), including threshold gating, state retention through a zero target, continuous resize, and unchanged-target omission; focused Ruff, formatting, source mypy, IDE diagnostics, and diff checks pass. No backtest was run and no live/capital mutation was performed.

### 2026-08-07 14:34 EDT

Prepared MON-210 without launching a backtest. Froze the point-in-time `>$250,000` rolling 24-hour Hyperliquid-notional population at 100 assets, ordered by observed volume: BTC, ETH, HYPE, SOL, ZEC, XRP, LIT, PUMP, ACE, ONDO, ENA, WLD, ADA, UNI, XMR, DOGE, BNB, XPL, PAXG, AAVE, NEAR, kBONK, SUI, KAITO, TAO, FARTCOIN, CC, LTC, AVAX, LINK, ETHFI, CRV, WLFI, kPEPE, LDO, VINE, ZRO, ARB, PENGU, MON, XAI, VVV, JUP, BCH, DOT, TRUMP, FET, INJ, NIL, AERO, XLM, JTO, FIL, RESOLV, PENDLE, OP, kSHIB, ASTER, MORPHO, ALGO, SKR, SPX, TRX, PEOPLE, SAGA, SUSHI, APT, ETC, EIGEN, VIRTUAL, HEMI, POL, SEI, SKY, MNT, 2Z, STBL, RENDER, GRASS, MET, RUNE, STABLE, MOVE, USUAL, TIA, MEGA, HBAR, ZORA, STRK, ATOM, GMX, ICP, WIF, CAKE, kNEIRO, BABY, AVNT, AXS, PNUT, DASH. Snapshot observed at approximately `2026-08-07T18:33Z`; DASH was the boundary asset at approximately `$251.9k`, and a 200-result request returned only these 100, so the tool result was not limit-truncated.

The deterministic `binance_cohort_pack_v1` plan uses completed common end `2026-08-07T00:00:00Z`, `1d`, `max_history`, relative tolerance `0.8`, maximum 16 assets per batch, and a strategy-aware minimum of 201 candles (EMA-200 warmup plus at least one scored bar). `max_history` was chosen over the standard cohort floors because MON-210 asks for available history; it retains each lifespan pack's maximum common window while bounding within-pack lifespan loss to 20%. It produced 13 plans covering 96 assets at 2,525 (BTC), 1,969 (two runtime chunks, 28 assets), 1,687 (2), 1,233 (8), 1,009 (7), 848 (12), 634 (6), 498 (14), 393 (4), 309 (9), 274 (4), and 227 (1) daily bars. Four eligible-universe assets remain explicit pre-result exclusions: SKR (197 bars) and MEGA (189) fall below the minimum; MNT and kNEIRO have unsupported Binance USD-M symbols. Frozen execution assumptions remain EMA 10/200, `$10,000`, 100% equity at 1x, compounding, 5 bps fee/side, 5 bps slippage/side, summary retention, and no funding. The first refresh-backed planning call timed out during provider preflight; the cache-backed retry completed and did not enqueue a backtest. Next: call `run_binance_cohort_batches` with this exact universe, common end, packing policy, and strategy configuration; preserve each plan's separate `run_id` and do not compare aggregate metrics across unlike lifespan cohorts.

### 2026-08-07 15:10 EDT

Shipped `binance_cohort_pack_v2` fixed-floor planning in `mm_v04` without launching a backtest. Both `plan_binance_batch_windows` and `run_binance_cohort_batches` now accept optional descending `cohort_floors`; each eligible asset is assigned to the largest supplied floor its exact trailing continuous history satisfies, each floor remains runtime-chunked at 16 by default, and the accepted floor list is echoed for audit. Invalid empty, unordered, duplicate, below-minimum, or wrong-mode floor policies fail validation; assets that clear the general viability threshold but miss the smallest supplied floor are explicit `below_smallest_cohort_floor` skips. Existing `cohort_floor` and `max_history` modes remain available and retain their API/MCP defaults. The backtest UI now defaults to fixed floors `[2500, 2000, 1500, 1200, 1000, 800, 600, 500, 300, 200]`; MON-210 must substitute `201` for the final floor because its strategy-aware minimum is 201. The earlier 13-plan max-history output remains planning evidence but is superseded as MON-210's execution policy. Verification passed: 16 focused backend tests, backend Ruff and source mypy, 10 MCP focused/smoke tests and Ruff, regenerated OpenAPI client, frontend lint, and production build. No backtest, manager, live/capital action, database migration, commit, or push occurred.

### 2026-08-07 16:33 EDT

Attempted MON-210 with fixed-floor batches, then invalidated the entire result set at Destin's direction. Many assets returned zero/no metrics, and Destin identified the strategy file itself as broken. No batch metric, cohort comparison, or prior continue/narrow/reject interpretation is admissible evidence. Preserve the saved IDs only as invalid diagnostic artifacts: `3f87759f-c6ab-44c8-94d9-77105d983f21`, `2c304705-fb14-4679-96db-5cdcd98b114c`, `69457916-1183-4852-90ea-3e96cee27c0b`, `c6a21f75-639c-45dd-b6e5-37ed93a62069`, `74aca9ab-b27f-4d4c-8ce8-dbf12e6d8c3f`, `230187a8-c7ab-45dc-b801-5362fa7deb29`, `625c4427-128b-4cb0-b9c5-e19c14a37c32`, `70aa6e22-075d-434b-9412-4efcfc30ce3c`, `4e3483b2-8c59-4cfa-be78-82740600d92c`, and `0c297049-5852-4bf4-bc48-84b50e350e92`. MON-210 is blocked until Destin repairs and verifies `emac_cross`; then rerun from the frozen universe and assumptions.
