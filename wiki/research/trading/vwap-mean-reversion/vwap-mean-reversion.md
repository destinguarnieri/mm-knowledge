# VWAP Mean Reversion Research

Related process: [[research/trading/research_process_v2|Research Process V2]]
Board: [[research/trading/research_index|Research Board]]
Linear: [VWAP Mean Reversion Research](https://linear.app/money-machine/project/vwap-mean-reversion-research-ec37e0025905)

Lane (Research Process V2 §0): **capture engineering** — a promising signal to reproduce and monetize, not an open discovery from zero.

<!-- ================= LIVING HEAD — rewrite in place each session ================= -->

## TL;DR & What's Working

VWAP mean reversion on the 96-asset Hyperliquid universe shows a **broad, high-win-rate edge at 5m and 15m**, and an **asset-selective edge at 1m** — now readable from the saved batches (404 fixed 2026-07-23). The decisive open question is whether it survives realistic costs, because it trades extremely heavily.

**What's working:**

- **Broad edge at 5m and 15m.** 5m: `66/96` assets positive, `59/96` Sharpe > 1 (median Sharpe ≈ `2.4`, median return `+2.8%` over ~15 days). 15m: `69/96` positive, `60/96` Sharpe > 1 (median return `+8.3%` over ~49 days, highest expectancy). Win rates cluster at `83–85%`; median drawdowns ≈ `−5.5%` (5m) / `−14%` (15m). Leaders: TIA/W/WIF/MEGA (5m, `+13–20%`), WLFI/LIT/BIO/PYTH (15m, `+42–71%`). Cites: 5m `5dc5f639`, 15m `6e013ad3`.
- **1m works, but selectively.** ~half the universe is strongly positive (`42/96` Sharpe > 2) while the other half is negative, so the median is ≈ flat. This is an asset-selection story, not a universe-wide 1m edge. Cite: 1m `cb0ee0c1`. (Raw 1m Sharpe magnitudes are inflated by the short ~3-day window — do not compare Sharpe across timeframes.)
- **Clean mean-reversion signature.** High hit rate with small average wins vs larger average losses — the edge is in win rate, the risk is in the tail.

**Costs are modeled — and this is where it gets interesting.** `total_return` is net (matches `net_return` on 96/96 assets) and the payload carries the full fee/slippage decomposition. Net-of-fee survival scales cleanly with timeframe as the per-trade cost is amortized over larger moves: median cost drag ≈ **72% of gross PnL at 1m → 32% at 5m → 13% at 15m**, and net-positive breadth goes **47 → 66 → 69** of 96. The signal is real gross everywhere; **1m is a true edge that fees destroy**, while 5m/15m clear fees comfortably.

**The remaining decisive caveat:** the slippage input in these runs was `0.05` bps — effectively **zero**. So results are net of ~1.5 bps/side fees but **not yet net of realistic slippage**. At ~600–700 trades/asset with avg hold ≈ 0, slippage is the dominant *unmodeled* cost — a realistic-slippage rerun is the gating monetization test, not fees. (Cost convention: `fees` is a fraction, `slippage` is bps — see Fixed Assumptions.)

**Best next step:** re-run 5m/15m with realistic Hyperliquid slippage (+ a stress multiple) using the now-confirmed config (Fixed Assumptions) and see whether the net edge holds.

## Current Read (provisional — not a verdict)

Two separate questions, separately gated (Research Process V2 §2).

| Question | Current read | Confidence | Key evidence | What would change it |
|---|---|---|---|---|
| Signal validity — does price-vs-VWAP carry reversion edge? | Supported at 5m/15m (broad); 1m asset-selective | Med–High | 66/96 & 69/96 assets positive at 5m/15m, 83–85% win | collapses on a disjoint window |
| Monetization — capture after realistic costs? | Net of ~1.5bps fees: survives at 5m/15m (drag ~13–32%), 1m killed by fees. Realistic slippage: **untested** (input ≈0) | Low–Med | net/gross decomposition in saved runs | net survives realistic slippage + stress |
| Cross-market — generalizes beyond Hyperliquid crypto? | Untested | — | crypto perp only so far | run on another venue / asset class (incl. equities) |

## Open Threads / Next Experiments

1. **Realistic-slippage cost stress (gating).** Config is now recovered (see Fixed Assumptions); the saved runs used ~0 slippage. Re-run 5m/15m with realistic Hyperliquid slippage plus a stress multiple; that decides monetization. NB: the Research-MCP batch tool caps at **32 assets** and requires a per-asset `assets` list covering every id, so the 96-universe needs 3 chunks/timeframe (the original 96-runs came via the UI).
2. **Characterize the 1m bimodality.** ~half the universe works at 1m and half doesn't — find what separates the working subset (liquidity, volatility, spread, tick size). Could become a deployment selection rule rather than a rejection.
3. **Tail-risk + artifact review.** Per-trade losses dwarf wins (classic mean-reversion payoff); confirm no single-asset blowup drives the aggregates and that trades are explainable. Worst single-asset losers exist (e.g. VINE/0G at 5m) — check they aren't masking universe fragility.
4. **Disjoint validation + one-time holdout.** All three windows are short and recent (~3d / 15d / 49d), so shared-regime risk is high; a disjoint preceding window is the cheapest test that could kill it, before any per-timeframe promote / narrow / continue / reject.
5. **Bounded improvement hypotheses — distinct identities.** The baseline uses no threshold controls or signal-statistic overlays. Test thresholds alone, signal-stats alone, then a justified combined variant; keep each a separate identity.

Boundary: `5m`/`15m` are the strong cluster; `1m` is asset-selective; performance trails off at `30m` — retain `30m` as negative boundary evidence, not a primary target.

<!-- ================= STABLE ================= -->

## Strategy & Data Facts

- Strategy family: VWAP mean reversion — the registered `px` strategy with `SOURCE=rvwap` (rolling VWAP) and `SIG_POLARITY=negative` (the negative polarity is what turns price-vs-VWAP into mean reversion). Full config confirmed 2026-07-23, see Fixed Assumptions.
- Frozen baseline: `LEN 200`, `LOOKBACK 100`, `MIN_ADJUSTMENT_VALUE_PCT 0.4` (40% min-adjustment floor on position changes).
- Controls: none yet — no threshold controls, no signal-statistic overlays. These are the bounded improvement axes above.
- Venue/universe: Hyperliquid, 96-asset universe; `96/96` assets completed on all three timeframes.
- Windows are short and recent: ~`4,100`/`4,400`/`4,700` scored bars ≈ ~`3` days (1m) / ~`15` days (5m) / ~`49` days (15m).
- Turnover is very high: ~`578`/`668`/`702` trades per asset (1m/5m/15m), average hold ≈ `0` bars — near-continuous flipping. Cost sensitivity is therefore the dominant risk.
- Payoff shape: high win rate (`77–85%` median) with average wins (~$15–30) smaller than average losses (~$−50 to −190) — the edge is frequency, the danger is the tail.
- Prime timeframes: `5m`/`15m` (broad edge); `1m` asset-selective; `30m` weaker (boundary evidence).

## Fixed Assumptions (confirmed 2026-07-23)

- Venue: Hyperliquid. Universe: 96 assets. Candle source: `hyperliquid`.
- Strategy: `px` (id `27260dfb-0a6f-412b-879c-87eee4198e15`).
- params: `SOURCE=rvwap`, `LEN=200`, `LOOKBACK=100`, `SYMETRIC=true`.
- config: `SIG_POLARITY=negative`, `SIG_TO_POS_SIZE=direct`, `SIG_SCALE=min_max`, `SIG_SCALE_LOOKBACK=252`, `SIG_SMOOTH=0`, `SIG_CLIP_MAX=true`, `SIG_BUFFER_TYPE=none`, `SIG_BUFFER=0`, `VOL_ADJ_POS_SIZE=inverse` (px defaults except polarity).
- trade_config: `MIN_ADJUSTMENT_VALUE_PCT=0.4`, all others default (`SIZING_MODE=compounding`, thresholds 0, aggs 1.0).
- Initial capital: `100,000`.
- **Cost convention (important, mixed units):** `fees` is a **fraction** — `0.00015` ≈ 1.5 bps/side, applied per fill. `slippage` is in **bps** — the saved runs used `0.05` bps ≈ **effectively zero**. Both are applied to fills, but the reported `total_slippage` metric is reconstructed from volume in a separate path, and `gross_pnl_before_fees` adds back fees only (not slippage). Net metrics here are therefore **net of fees, not of realistic slippage** — the key monetization caveat.

<!-- ================= APPEND-ONLY TAIL — do not edit past entries ================= -->

## Run Registry (pointers, not tables)

Metrics live in the UI / saved runs — cite and re-fetch; do not paste tables.

- `cb0ee0c1-9dd0-4da7-baaa-4c66c071d8df` — batch, Hyperliquid `1m`, 96/96 — asset-selective: 47/96 positive, 42/96 Sharpe > 2, but median ≈ flat (bimodal). ~3-day window.
- `5dc5f639-e82d-4ef0-b4e6-ccfc5a244d6e` — batch, Hyperliquid `5m`, 96/96 — broad edge: 66/96 positive, 59/96 Sharpe > 1, median return +2.8%, win ≈ 83%. ~15-day window.
- `6e013ad3-5545-450a-80f1-aa96f6e08c27` — batch, Hyperliquid `15m`, 96/96 — broad edge: 69/96 positive, 60/96 Sharpe > 1, median return +8.3% (highest expectancy), win ≈ 85%. ~49-day window.

Metrics retrieved via `get_saved_batch_run` on 2026-07-23 after the saved-run 404 was fixed. Re-fetch for full per-asset numbers; do not transcribe the 96-row grids here.

## Write Log

### 2026-07-23 05:21 EDT

Created the Linear project and recorded the overnight `1m`/`5m`/`15m` Hyperliquid batches. Destin froze the baseline at length `200` / minimum adjustment `0.4`, named `1m`/`5m`/`15m` as the prime cluster, and noted `30m` trails off. Strategy currently has no threshold controls or signal-stat overlays. Saved lookups `404`; 5m/15m live summaries confirm 96/96 assets. No live/capital mutation.

### 2026-07-23 16:13 EDT

Created this research doc in the two-layer format and added the thread to the [[research/trading/research_index|Research Board]]. Next: recover the exact strategy identity/config and reproduce the frozen baseline before pressure-testing.

### 2026-07-23 17:12 EDT

Confirmed strategy identity + full config with Destin (recorded in Fixed Assumptions): `px` / `SOURCE=rvwap` / `SIG_POLARITY=negative` / `SIG_TO_POS_SIZE=direct` / `LEN 200` / `LOOKBACK 100` / `MIN_ADJUSTMENT_VALUE_PCT 0.4` / init cap 100k / fees 0.00015 (fraction, ≈1.5bps) / slippage 0.05 (bps, ≈0). Traced cost semantics in code: fees are a fraction applied per fill (`mock_services._compute_fee`), slippage is bps applied to fill price (`_compute_fill_px`) but the runs used ≈0, and `total_slippage`/`gross_pnl_before_fees` reporting has a minor unit/decomposition muddle (Destin has deferred fixing). Net take: the "survives costs" read is net of fees only; realistic-slippage stress is the true monetization gate. Also found the Research-MCP batch cap (`MAX_BATCH_ASSETS=32`, `assets` must cover ids exactly) — a reproduction rerun attempt was blocked by it and not yet completed. No live/capital mutation.

### 2026-07-23 16:47 EDT

Saved-run 404 fixed by Destin; pulled all three batches via `get_saved_batch_run`. All 96/96 assets completed each timeframe. Findings: 5m and 15m show a broad universe-wide edge (66/96 and 69/96 assets positive, 59–60 with Sharpe > 1, 83–85% win rates, median returns +2.8%/+8.3% over ~15/49-day windows); 1m is bimodal (42/96 Sharpe > 2 but ~half negative → median flat), an asset-selection story rather than a universe edge. Turnover is extreme (~580–700 trades/asset, avg hold ≈ 0) and it is unconfirmed whether these metrics include fees/slippage — so realistic-cost survival is now the explicit gating question. Updated the living head, Current Read (validity supported at 5m/15m; monetization open/decisive), and Run Registry accordingly. No live/capital mutation.
