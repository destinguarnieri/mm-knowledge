# EMA Cross 10/200 Research

Related process: [[research/trading/research_process_v2|Research Process V2]]
Signal-stats event study: [[event_study_anchor_findings|Anchor + Holdout Findings]] · label definitions [[event_labels_v1|Event Labels V1]]

<!-- ================= LIVING HEAD — rewrite in place each session ================= -->

## TL;DR & What's Working

Testing whether the near-parameter-free EMA 10/200 cross carries tradable edge, and how to monetize it. **Direction is well-supported; the open game is capturing the signal, not proving it exists.**

**What's working — live threads worth capturing:**

- **Direction is right ~80% of the time.** Positions sit in profit for `77.84%`–`88.21%` of active bars across BTC intervals (and ~`84–88%` median across the multi-asset 4h batches), despite only `10–28%` realized win rates. That gap is a *capture/exit* problem, not a direction problem — the single most important finding in this study. Cites: BTC scan `ce0bc93e` (1d) → `987817d2` (1m); 20-asset 4h batch `3c0f2043`.
- **A real 4h leader cluster.** SUI, ETH, ARB, DOGE cleared Sharpe `1.0` in the 20-asset 4h batch (`3c0f2043`); roughly 30–40 assets show usable 4h/1h stats. ETH is the strongest risk-balanced name.
- **Escalation ladder — most monetizable structure found so far.** In the signal-stats event study, mean→±2σ band-to-band traversal is positive with payoff *and* hit rate rising up the ladder: mean→2σ hit `94%` (anchor) / `96%` (holdout), with conditional touch rates stable across two disjoint 50k-bar windows (P(1σ|mean) ≈ 0.69–0.71, P(2σ|1σ) ≈ 0.62–0.63). **Net positive at realistic maker costs (~1–2 bps/side)** — the ~20 bps figure that earlier read as a kill is a max-taker *ceiling*, not a floor. Cites: anchor `8077b0dd`, holdout `9c96c57f`; full numbers in [[event_study_anchor_findings]].
- **Capture vehicles now exist.** `emac_v4` (transition-only regime control) and `emac_v5` (continuous magnitude inside the Threshold Engine V3 regime) are implemented and pass focused tests — the mechanisms to hold the 80% instead of giving it back at the flip.

**Best next step:** spec and evaluate a bounded mean-cycle capture variant (S1 entry / retreat exit, optionally escalation-aware) against the flip-only control, and wire continuous exit/scale-out to harvest the time-in-money. See Open Threads.

## Current Read (provisional — not a verdict)

Living per-question status. A row only becomes a recorded **Decision** at a promotion gate (Research Process V1 §12) or an explicit kill; until then it stays provisional.

| Question | Current read | Confidence | Key evidence | What would change it |
|---|---|---|---|---|
| (B) Does 10/200 put you on the right side? | Leaning strongly yes | Med–High | `77.8–88.2%` time-in-money across intervals and multi-asset batches | fails on a fresh untouched holdout or a different venue |
| (A) Can dead-simple flip-only make money as-is? | Leaning no (flip-only) | Med | flip-only net-negative after costs at ≤1h; severe drawdown at 1d/4h | a real selection rule clears net after realistic costs |
| (C) Can a capture mechanism monetize the 80%? | Open — top priority | Low (early) | escalation ladder net-positive at maker cost; V4/V5 built | a mean-cycle / continuous variant beats the control out-of-sample |
| Universe filter from prior-window winners? | Rejected (on this evidence) | Med | prior-winner persistence weak; best causal AUC ~0.55–0.62, post-hoc only | a pre-registered rule holds on a genuinely untouched window |

Reframing note: this doc previously carried a hard "Verdict" table calling (B) *Supported* and (A) *Kinda/maybe*. The substance is unchanged — (B) strong, (A) weak as flip-only — but it is now tracked as a provisional read, because no promotion/kill gate has been run and the capture question (C) is still open.

## Open Threads / Next Experiments

Ranked by expected value, capture-first:

1. **Capture the 80% (top).** Spec a bounded mean-cycle variant (S1 entry / S4 mean-retreat exit, optionally escalation-aware) and evaluate against the flip-only control on both event-study fixtures. The hinge is cutting the non-escalating branch cheaply. See [[event_study_anchor_findings]] bottom line.
2. **Continuous positioning.** Evaluate `emac_v5` (continuous magnitude within the V3 regime) and `sig_to_position` mappings; measure profit retention versus the flip-only giveback. No V5 backtest has been run yet.
3. **Dynamic vs static thresholds.** Thresholds derived causally from the signal's own rolling mean/σ (no lookahead) versus static controls, on the same fixtures.
4. **Selection rule, done right.** If an asset/universe filter is reopened, pre-register the rule and consume a genuinely untouched window exactly once. Standing post-hoc leads (candidates only): lower prior cross count; high 4-bar variance ratio + high 1-bar return autocorrelation.
5. **Rolling-lens breakout episode** (Destin, 2026-07-22): enter on rolling ±2σ breach, exit on close back inside; needs a rolling-lens episode builder plus economics on both fixtures.
6. **Compression/expansion market-state label** — pending Destin's corrected phrasing before re-running the chop split.

Deferred: broad asset/timeframe expansion of flip-only `emac_cross` — answered sufficiently; reopen only in service of a capture mechanism.

<!-- ================= STABLE ================= -->

## Strategy & Data Facts

- Strategy: `emac_cross`, fast EMA `10`, slow EMA `200`. Direct-position variant `emac` (strategy `be3545d2`); control research in `emac_v4` (transition-only) and `emac_v5` (continuous magnitude).
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

**Continuous-control development (V4/V5):** see the Write Log for the sequence (`a1688414` discarded config mismatch; `6108178a`, `eea81901`, `b12d3a50`, `bad11f56`, `f2299e5b`, `e43db176`, `43036e20`, `e58f3c5d`).

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

Implemented registered backtest strategy `emac_v5` as the continuous-position counterpart to `emac_v4`. It preserves V4's EMA 10/200 processed signal, emitted-history, slope overlay, signal-stat modes, Threshold Engine V3 configuration, volatility adjustment, position caps, and execution safeguards. Threshold Engine V3 still controls the persistent `LONG` / `FLAT` / `SHORT` regime; `signal_to_position` controls exposure magnitude continuously inside that regime, with the configured target floor and adjustment deadband applied before execution. Threshold state is retained independently from actual position size so a zero-magnitude target does not erase the active regime. V4 remains transition-only and unchanged. Focused V4/V5 tests pass (17 total), including threshold gating, state retention through a zero target, continuous resize, and unchanged-target omission; focused Ruff, formatting, source mypy, IDE diagnostics, and diff checks pass. No backtest was run and no live/capital mutation was performed.
