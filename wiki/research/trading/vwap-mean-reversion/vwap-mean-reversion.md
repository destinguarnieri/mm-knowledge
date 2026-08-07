# VWAP Mean Reversion Research

Status: in progress

Related process: [[research/trading/research_process_v2|Research Process V2]]
Board: [[research/trading/research_index|Research Board]]
Linear: [VWAP Mean Reversion Research](https://linear.app/money-machine/project/vwap-mean-reversion-research-ec37e0025905) · [MON-159 realistic-slippage gate](https://linear.app/money-machine/issue/MON-159/run-vwap-5m15m-realistic-slippage-monetization-gate)

Lane (Research Process V2 §0): **capture engineering** — a promising signal to reproduce and monetize, not an open discovery from zero.

<!-- ================= LIVING HEAD — rewrite in place each session ================= -->

## Strategy Thesis

We target statistically unusual extensions of current price from its rolling volume-weighted average price.

We are not broadly providing liquidity against price merely because it is moving away from VWAP. Price can trend away from its average for long enough to create unacceptable adverse path, cost, and tail risk. Statistical overextension identifies where an opportunity may exist; it does not by itself make the reversion ready to trade.

We seek high-probability conditions where an extreme extension is becoming exhausted and price and market participants display observable readiness to travel inward toward VWAP. The objective is to capture that inward traversal, not to assume immediate or complete convergence. Price and a moving VWAP may converge because price returns, VWAP catches up, or both move, and the timing may be too slow to support a profitable trade.

The strategy therefore has distinct layers:

1. **Location:** quantify how statistically overextended price is from VWAP.
2. **Readiness:** require observable evidence that the outward move is exhausting and inward travel is becoming probable. Destin has additional readiness tools to introduce; do not predefine this layer from the current PX and slope evidence alone.
3. **Regime avoidance:** recognize periods when price can continue trending away and avoid indiscriminate fading or liquidity provision.
4. **Risk introduction and capture:** use thresholding, escalation, position control, exits, and execution policy to enter and monetize the inward traversal without allowing failed reversions or costs to dominate.

Working distinction: **extension magnitude says where; readiness and regime say whether/when; position and execution policy say how much and how to capture it.**

### Catalog tools plausibly useful to VWAP readiness

Source inventory: [[trading/catalog_v1|Trading Catalog]]. These are mechanism candidates, not a combined strategy specification or evidence that each adds alpha. Introduce and evaluate one incremental feature at a time after the current slope/regime reference.

| Tool | Thesis layer | Why it may work here | Important boundary |
|---|---|---|---|
| **VWAP slope** | Regime avoidance | Directly distinguishes a relatively stationary mean from a VWAP migrating strongly enough that fading price can be dangerous. The catalog explicitly identifies strong VWAP trend as the mean-reversion blowout regime. | Test first and alone. Define normalization, lookback, allowed slope state, and whether it gates entry only or also forces exit. |
| **VFTI** | Participant readiness | Volume flow can turn against the current price direction before price visibly reverses. At a PX extreme, divergence or an inward VFTI turn may show participants withdrawing support from the outward move. | A continuous flow signal; specify divergence/turn semantics and avoid treating every disagreement as reversal proof. |
| **PRI / PRL / PRZ / PRB** | Control transfer and invalidation | PRI requires the opposing side to reclaim the prior candle's range, making it a concrete price-action event for “ready to travel inward.” Its levels/zones can anchor entry, retest, and invalidation rather than relying on candle-color reversal. | Test the PRI event first; do not bundle the full level/zone/breaker system until the trigger itself earns inclusion. |
| **Volume anomaly** | Exhaustion | A roughly 4× volume event near a local or PX extreme may indicate exuberance and exhaustion: participants committed unusual capital but failed or are beginning to fail to extend price. | Location matters; the same anomaly in the middle of a range can be acceleration rather than reversal. |
| **ATR anomaly** | Exhaustion and risk state | An unusually large range often precedes partial retracement and may mark capitulation at an extension. It can also warn that risk has changed abruptly. | “Something big happened” is not directional readiness by itself; likely a risk/reduction input unless paired with a separately validated inward trigger. |
| **Volume-delta anomaly** | Flow divergence | Candle direction opposed by cumulative volume delta may reveal outward price movement that underlying aggressive flow does not confirm. | Requires trustworthy delta data and an explicit sign/alignment contract. Test independently from VFTI. |
| **Absorption** | Exhaustion / failed continuation | Large wick relative to candle body at an outer extension can show attempted continuation being absorbed and rejected. | Catalog entry is WIP; definition and implementation correctness must precede economic testing. |
| **Order-book imbalance** | Quoted participant intention | At an extension, a change in quoted inventory pressure may show accumulation/distribution before price turns and may improve entry timing. | Book state is fragile and execution-sensitive; defer until credible L2 replay/mock-book infrastructure exists. |
| **Funding-rate state/change** | Broader participant positioning | Funding exposes how perp participants are positioned and what they pay to maintain that positioning. A sign change or failure of price to follow crowded funding may support reversal readiness. | Slow, venue-specific context rather than a standalone bar-level trigger. Avoid lookahead around funding publication/settlement. |
| **Trade speed** | Urgency and adverse selection | Rising event intensity can distinguish a quiet extension from an active attempt to continue or exhaust; it may guide whether to wait, cross, or avoid being adversely selected. | Not inherently directional and can diverge from volume; treat first as execution/risk context. |
| **RSI leaving an extreme** | Price-action readiness control | The catalog independently notes that fading is usually better when RSI is leaving an extreme, matching the outward-extension versus inward-reentry distinction observed in PX. | Likely correlated with PX; require incremental benefit beyond the existing signal rather than counting the same price move twice. |

Most direct future readiness candidates: **VFTI** for participant flow and **PRI** for an observable transfer of price control. Exhaustion features (volume/ATR anomaly and absorption) are plausible qualifiers. Order-book imbalance, funding, and trade speed belong later as participant or execution context. Do not combine these into the slope experiment.

## TL;DR & What's Working

VWAP mean reversion retains a valid gross signal, but the frozen high-turnover mapping does **not** preserve a broad net edge under the preregistered immediate-execution costs. At `5 bps` slippage/side plus `1.5 bps` fees/side, `5m` fails broadly and the frozen `15m` baseline is marginal. Raising the `15m` rebalance floor from `0.4` to `0.8` improved the original window, but failed a short non-overlapping forward diagnostic. Do not promote or tune that floor further on the original window. The fixed-slippage OHLC model is a blunt proxy; Destin wants the frozen baseline revisited after credible mock limit-orderbook/passive-fill modeling exists.

**What's working:**

- **Broad edge at 5m and 15m.** 5m: `66/96` assets positive, `59/96` Sharpe > 1 (median Sharpe ≈ `2.4`, median return `+2.8%` over ~15 days). 15m: `69/96` positive, `60/96` Sharpe > 1 (median return `+8.3%` over ~49 days, highest expectancy). Win rates cluster at `83–85%`; median drawdowns ≈ `−5.5%` (5m) / `−14%` (15m). Leaders: TIA/W/WIF/MEGA (5m, `+13–20%`), WLFI/LIT/BIO/PYTH (15m, `+42–71%`). Cites: 5m `5dc5f639`, 15m `6e013ad3`.
- **1m works, but selectively.** ~half the universe is strongly positive (`42/96` Sharpe > 2) while the other half is negative, so the median is ≈ flat. This is an asset-selection story, not a universe-wide 1m edge. Cite: 1m `cb0ee0c1`. (Raw 1m Sharpe magnitudes are inflated by the short ~3-day window — do not compare Sharpe across timeframes.)
- **Clean mean-reversion signature.** High hit rate with small average wins vs larger average losses — the edge is in win rate, the risk is in the tail.

**Costs are modeled — and this is where it gets interesting.** `total_return` is net (matches `net_return` on 96/96 assets) and the payload carries the full fee/slippage decomposition. Net-of-fee survival scales cleanly with timeframe as the per-trade cost is amortized over larger moves: median cost drag ≈ **72% of gross PnL at 1m → 32% at 5m → 13% at 15m**, and net-positive breadth goes **47 → 66 → 69** of 96. The signal is real gross everywhere; **1m is a true edge that fees destroy**, while 5m/15m clear fees comfortably.

**Realistic-slippage gate (2026-08-03):** under `5 bps` slippage/side, frozen `5m` fell to `18/96` positive assets and frozen `15m` to `45/96`; their medians were negative. At `10 bps`, breadth fell to `2/96` and `28/96`. The `15m` `0.8` rebalance-floor variant improved intended-cost breadth to `56/96` positive with positive median return and reduced turnover, while its stress result remained negative-median (`38/96` positive). See the Run Registry for saved IDs.

**Forward check:** the intended preceding 49-day window was unavailable from Hyperliquid history. On the available non-overlapping July 23–August 4 window, the `15m`/`0.8` variant fell to `28/96` positive at 5 bps and `21/96` at 10 bps, with negative median economics in both regimes. The window is short (~952 scored bars/asset), but it is sufficient to reject promotion from the same-window improvement.

**Threshold-only check (2026-08-04):** `px_threshold` reduced original-window trades from `65,464` to `3,419` (~95%) and improved intended-cost breadth to `56/96` positive, with median return `+4.44%` and median Sharpe `0.90`. It remained positive-median at 10 bps (`+0.83%`, Sharpe `0.47`, `49/96` positive). The price was materially worse tail exposure: median drawdown moved to about `−24%`, and ACE reached roughly `−89%`. On the unchanged short forward window, intended-cost breadth fell to `44/96` with median return `−0.91%`; at 10 bps it fell to `39/96` and `−1.56%`. Threshold-only therefore proves hysteresis solves much of the churn problem, but the preregistered full-state mapping is not promoted and its levels should not be tuned on the original window.

**5m threshold-only check:** the same unchanged thresholds cut frozen-window trades from `62,405` to `3,339`. At 5 bps, 55/95 successful assets were positive and median return/Sharpe improved to `+1.67%` / `1.17`; ACE was a terminal negative-equity failure and is not excluded from the risk read. The original 10 bps run failed (`32/95` positive, median return `−2.37%`). On the complete non-overlapping forward window, breadth fell to `30/96` at 5 bps and `16/96` at 10 bps, with median returns `−2.77%` and `−5.27%`. Reject threshold-only 5m: hysteresis materially reduces churn but does not create robust cost or forward survival.

**Whole-signal continuous control:** the first `px_threshold_continuous` implementation incorrectly used generic `signal / 1.0` sizing inside the threshold gate, so signals at the `0.1` exit / `0.3` midpoint / `0.5` entry mapped to 10% / 30% / 50% rather than mapping the admitted threshold band to position space. Its four runs remain useful controls: scaling reduced threshold-only path risk, but both forward windows stayed negative. They are not evidence for the intended threshold-band continuous identity.

**Corrected threshold-band continuous result:** the intended `0.1 → 0%`, `0.3 → 50%`, `0.5 → 100%` mapper was run unchanged across the exact 15m matrix. It was more aggressive than the whole-signal control: original-window trades rose from `17,264` to `19,628`, median drawdown worsened from `−12.8%` to `−18.0%`, and intended-cost breadth/median return fell from `58/96` / `+2.71%` to `48/96` / approximately flat. Stress fell to `37/96` positive and `−5.00%` median return. The short forward remained negative (`32/96`, `−1.64%` at 5 bps; `22/96`, `−2.53%` at 10 bps). Reject the corrected mapper as a monetization improvement; do not tune it on these windows.

**VWAP slope/regime result:** the preregistered `abs(normalized_vwap_slope) <= 0.1` entry-only gate materially changed the risk path on a disjoint 20,000-bar Binance USDM 15m window: fewer trades, broad paired return/drawdown improvement, and roughly half as many severe-drawdown assets at both costs. Median economics nevertheless remained negative. This supports **the tested low-slope gate as a useful experimental filter on that window**, not the stronger claim that low slope is the correct VWAP-extreme regime or that slope should always be used as an absolute filter. A return-blind BTC/ETH/SOL check found `|PX extension|` and `|VWAP slope|` rise together consistently; at `|PX| >= 0.9`, the `.1` low-slope state occurred in only about 6–8% of bars. Keep low-slope gating explicitly labeled as a hypothesis and leave slope direction, alignment, extremity, and change/deceleration roles open. Do not promote the current threshold+slope mapping or tune `0.1`/lookback on this window. MON-163 is Done.

**Entry-threshold result:** changing only symmetric entry from `±0.5` to `±0.9`, with `±0.1` exits and no slope gate, broadly improved the same 20,000-bar Binance window. Trades fell by more than half; return and drawdown improved on roughly two-thirds of the 30 paired assets at both cost levels, and severe-drawdown counts fell materially. The 5 bps median Sharpe became slightly positive, but median return remained negative; 10 bps remained negative-median. LDO/WLD were strong improvements, while CRV/ETHFI surrendered profitable behavior and NEAR/FARTCOIN worsened. Treat `±0.9` as a better full-commitment candidate than `±0.5` on this development window, not a promoted or optimal threshold. Long-window summary runs: `17b63d0d` and `94dcfa45`.

**Fixed-exit follow-up:** moving only the symmetric exit from `±0.1` to `±0.5` on the same `±0.9` entry setup reduced time active but worsened turnover, breadth, return, Sharpe, and tails on the 20,000-bar 5 bps development run `616fe951`. Reject `±0.9`/`±0.5` as a capture improvement and do not spend the 10 bps stress run on it. The NEAR chart explains the semantic failure: price traveled profitably inward past the short average entry while the processed signal remained statistically extended, so the fixed `.5` exit did not capture the move; the position then remained exposed into renewed continuation.

**Best next step:** register and smoke the new `px_signal_bands` identity, then inspect a bounded full-retention chart before economic batching. It enters full threshold-only risk on a processed-signal 2σ crossing and exits on the corresponding inward 1σ crossing, with both price-extension and signal-stat lookbacks fixed at 100 for this identity. Its display-only market view emits normalized VWAP slope, VFTI, PRI, RSI, ATR anomaly, volume anomaly, absorption, and ROC so continuation/failed-reversion episodes can be inspected without adding a gate. Escalation, stops, PnL-aware resizing, and readiness rules remain separate later mechanisms.

**Required visual review:** use full-retention single-asset charts alongside batch metrics. Inspect price/VWAP bands, backend average entry, position state, and signal together. The first average-entry review of the `±0.5` threshold control shows full risk frequently committed while price is still inside the eventual outward move; the fixed average then absorbs substantial adverse travel toward the later extreme because threshold-only cannot add at a better basis. This is direct path evidence that `±0.5` is a poor full-size commitment candidate on the inspected fixture. It supports testing `±0.9` and later separating early setup awareness from escalation/full commitment, but one chart does not itself establish the correct threshold.

**Price-band versus signal-band boundary:** existing fixed-threshold identities retain raw price-extension bands at `LOOKBACK=100` and processed-signal statistics at `signal_stats_lookback=200`; those domains are related but not equivalent, and prior results remain valid because the signal bands were display-only. The new `px_signal_bands` experiment explicitly chooses the processed-signal domain for trading and synchronizes both lookbacks to 100. This aligns window length, not mathematical domain: price-panel bands remain raw price-distance statistics while trade thresholds are processed-signal statistics.

**Dual-domain traversal study (2026-08-06):** a closed-bar BTC Binance USDM `15m` event study froze both lookbacks at 100 and measured raw-price and processed-signal band crossings separately across chronological 10,000/9,999-bar halves. Both domains reproduced the same broad structure: outward continuation becomes less likely at the next rung, while the stricter inward 2σ→1σ race completes before re-expansion only about half the time. Price and signal touches overlap heavily, so the normalized signal is a timing transform of the price-extension process—not independent confirmation; its modest distinction is slightly earlier inward timing. This supports continuing with the bounded dynamic-band smoke, but not promoting threshold-only full risk. Canonical artifact runs: `e88e7013-9f93-48c8-aefc-e1ee197ed092` and `d474a327-d619-49ed-863d-fa6340bf1569`.

**Fractional-depth extension (2026-08-06):** the same two BTC windows now map contemporaneous band space continuously (`mean=0`, `1σ=1`, `2σ=2`) and measure fixed half-band checkpoints. At every outward half-step, immediate continuation remained the minority in both price and signal domains; retreats through the starting depth occurred roughly two-thirds to three-quarters of the time. Retry-allowed episodes also contained meaningful partial traversals that ended before the next half-step, confirming that exact/full touches discard tradeable path information. Simple inward-turn confirmation was not uniformly decisive: next-inner completion varied by depth and side, with the deepest turn strongest but still negatively skewed. Decision: replace full-touch/full-position semantics with continuous location plus bounded inventory capacity, but do not claim the study identifies an optimal nonlinear curve. Canonical schema-v2 artifacts: `52fa8f74-d7e7-4d5e-86a1-45612570ba20` and `c36a7b0f-b0a0-4f68-92d3-e05906aef22e`.

## Current Read (provisional — not a verdict)

Two separate questions, separately gated (Research Process V2 §2).

| Question | Current read | Confidence | Key evidence | What would change it |
|---|---|---|---|---|
| Signal validity — does price-vs-VWAP carry reversion edge? | Supported at 5m/15m (broad); 1m asset-selective | Med–High | 66/96 & 69/96 assets positive at 5m/15m, 83–85% win | collapses on a disjoint window |
| Monetization — capture after realistic costs? | No mapping promoted: `±0.9` entry improves the `±0.5` development-window path broadly, but remains negative-median after costs | Med | intended/stress gate, paired Binance threshold test, and prior non-overlapping forward runs | the selective-entry effect survives a new disjoint holdout, or passive-fill modeling materially changes executable costs |
| Cross-market — generalizes beyond Hyperliquid crypto? | Untested | — | crypto perp only so far | run on another venue / asset class (incl. equities) |

## Open Threads / Next Experiments

### Strategy path map (agreed 2026-08-04)

1. **Threshold-only — evaluated (`px_threshold`).** The preregistered `±0.5` entry / `±0.1` exit identity removed ~95% of trades at both 5m and 15m. The 5m version failed stress and forward; the 15m version survived same-window stress but materially worsened full-size tails and failed the short forward diagnostic. Preserve as the threshold reference; do not tune its levels on the original windows.
2. **Thresholds plus continuous sizing — corrected and rejected (`px_threshold_continuous`).** The intended mapping uses `signal_to_position_banded` over each state's exit-to-entry magnitude, so exit edge maps to flat, band midpoint to half size, and entry edge to full size. Against the whole-signal control it increased turnover/exposure, weakened original-window intended-cost economics, worsened drawdown, failed stress, and remained negative forward. The baseline retained `MIN_ADJUSTMENT_VALUE_PCT=0.4`, which Destin originally found through a one-night manual grid as a configuration that stood out; it remains a useful frozen reference, not an empirical optimum. Do not tune this mapper on the seen windows.
3. **PnL-aware continuous resizing — direction confirmed, semantics open.** Negative churn often comes from mechanically resizing to the signal without considering whether the live position is in the money. Destin directionally confirmed the current interpretation: scaling in remains available; discretionary scaling out generally waits until the position is profitable; threshold and stop exits override. Exact definitions of “in profit,” partial reductions, and any additional risk-reduction exception remain unresolved. Test only after the corrected banded baseline.
4. **Wide stop loss — hypothesis recorded, semantics open.** A wide but sensible stop may cap catastrophic failed reversions. Keep it separate from PnL-aware resizing and slope filtering. Define trigger unit, close-versus-intrabar execution, and rearm/cooldown semantics before implementation so a stopped regime cannot immediately re-enter accidentally.
5. **VWAP slope role — low-slope gate evaluated; broader use remains hypothesis (`px_threshold_slope`).** The tested identity used log-linear rolling-VWAP slope, `SLOPE_LOOKBACK=3`, 252-bar min-max scaling, and fresh entries only when `abs(normalized_vwap_slope) <= 0.1`. It improved risk/economics broadly but remained negative-median and missed profitable behavior, most clearly ETHFI. Do not generalize this into “low slope is the correct entry regime.” Return-blind saved-series inspection shows moderate, consistent positive association between `|PX|` and `|slope|`; `.1` is rare at the largest PX extremes. The causal possibilities remain live: absolute low slope may identify a special subset; high slope may be part of the extension phenomenon; signed PX/slope alignment may distinguish continuation from convergence; slope change/deceleration may express readiness better than slope level. Freeze the completed gate result and investigate these roles with an event study before another slope strategy.
6. **Dynamic signal-band mechanism — first threshold-only identity implemented; escalation remains later.** `px_signal_bands` enters full risk when the processed PX signal crosses its moving outer 2σ band and exits when it crosses inward through the same-side 1σ band. Both band lookbacks are 100; moving crossings compare previous signal/previous band with current signal/current band. This is intentionally threshold-only. Destin's stronger outcome hypothesis still predicts that escalation layered onto an extreme-band mechanism will perform best, but escalation sizing, successive levels, stops, and rearm remain out of scope until the dynamic baseline and display-only market state are visually and economically understood.
7. **Execution-model revisit.** Re-run the frozen baseline when a credible mock limit-orderbook/passive-fill model exists. Treat that as execution-model validation, not evidence that the current market-order mapping survived.
8. **Longer-history validation.** Hyperliquid supplies only roughly 5,000 bars. Use Binance candle data for longer and genuinely disjoint windows where venue comparability is acceptable; keep provider provenance explicit.
9. **Entry-threshold sensitivity — evaluated, not promoted.** The fixed symmetric `±0.9` entry comparison retained `±0.1` exits and all other threshold-only settings. It reduced activity and broadly improved return/drawdown versus `±0.5`, but remained negative-median after costs and produced meaningful missed-profit/worse-tail counterexamples. Preserve `±0.9` as the stronger development reference for full commitment; do not tune another level on this window.

Additional open analyses: characterize the `1m` bimodality by liquidity/volatility/spread/tick size, and inspect the worst loss tails/artifacts before any promotion. The threshold-only severe-drawdown set (`max_drawdown <= −40%`) contains 12 assets and accounts for about half of all losing-asset return magnitude. It is enriched in the current low-volume quartile (5 severe names versus 1 in the high-volume quartile), but current 24-hour volume has almost no monotonic relationship with drawdown across all 96 assets (Spearman ≈ `0.08`) and ZEC is a high-volume counterexample. Treat “low-quality coin” as a hypothesis requiring explicit measurable features, not an asset-exclusion rule.

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
- `224a57a6-4b35-4e22-9633-8ee6b576bf57` — frozen `5m`, 5 bps slippage/side + 1.5 bps fees/side, 96/96 — broad economics fail.
- `54f4fff6-3ef1-4654-ab7b-1d13dde8731f` — frozen `5m`, 10 bps stress, 96/96 — current mapping decisively fails.
- `533e4ba2-5860-4ad8-88e3-0055886c8920` — frozen `15m`, 5 bps slippage/side + 1.5 bps fees/side, 96/96 — marginal/negative-median.
- `0bba584d-8bc9-4b3f-a007-6a9c3c3f252d` — frozen `15m`, 10 bps stress, 96/96 — broad economics fail.
- `f4d5c52f-58f7-4e92-8260-2b8b2c5740be` — `15m`, rebalance floor `0.8`, 5 bps intended slippage, 96/96 — ~41% fewer trades; broad positive intended-cost lead restored.
- `157e7f7f-d37c-4d7f-84d9-d7e9ff8f4d61` — `15m`, rebalance floor `0.8`, 10 bps stress, 96/96 — improved versus frozen stress but negative-median; not broad stress survival.
- `bdfb2b57-ae87-44da-b2c3-703297d3577d` — short forward `15m`, rebalance floor `0.8`, 5 bps intended slippage, 96/96 — 28/96 positive and negative-median; same-window improvement did not generalize.
- `a7d1b5ac-fcb9-47b5-a682-ef8b246e53cd` — short forward `15m`, rebalance floor `0.8`, 10 bps stress, 96/96 — 21/96 positive and negative-median.
- `c3f04ae6-8aed-42df-8d50-25590fb3cbce` — threshold-only `15m`, original window, 5 bps intended slippage, 96/96 — 56/96 positive; ~95% fewer trades; positive median economics but worse full-size tails.
- `3cee5164-d103-44e2-bc84-66c74ace7a63` — threshold-only `15m`, original window, 10 bps stress, 96/96 — 49/96 positive and positive-median; stress survival on the comparison window.
- `397a8461-16a2-4115-bef0-72205d1c9fcc` — threshold-only short forward `15m`, 5 bps intended slippage, 96/96 — 44/96 positive and negative-median; not promoted.
- `a4f00228-f10e-4e2d-a1e5-d86e60f7f561` — threshold-only short forward `15m`, 10 bps stress, 96/96 — 39/96 positive and negative-median.
- `ceb1b5a7-535f-40a3-a820-f9a4b3d4b537` — threshold-only `5m`, original window, 5 bps intended slippage — 95 successes plus ACE terminal negative-equity failure; 55 successful assets positive and positive-median economics.
- `428a3d20-9b0a-42d9-82fd-6fad13d629bb` — threshold-only `5m`, original window, 10 bps stress — 95 successes plus ACE terminal negative-equity failure; 32 successful assets positive and negative-median.
- `c9b39f48-79d7-4c94-aa0d-c7b054d6fdac` — threshold-only `5m`, complete forward window, 5 bps intended slippage, 96/96 — 30/96 positive and negative-median.
- `7a501d2c-458d-40db-8eed-1813144d5a08` — threshold-only `5m`, complete forward window, 10 bps stress, 96/96 — 16/96 positive and decisively negative-median.
- `b0d1adb6-5e4a-461e-87ed-ca1031b9e5c7` — whole-signal continuous control `15m`, original window, 5 bps, 96/96 — not the intended threshold-band mapper.
- `ee416d79-0fb9-4aa3-b100-34c80ac5f6d6` — whole-signal continuous control `15m`, original window, 10 bps, 96/96.
- `06f1fac0-8399-4dee-a9ba-0f3026a045e5` — whole-signal continuous control short forward `15m`, 5 bps, 96/96.
- `3a2a627a-8cf1-4fb0-b4c8-eb2bdd4cce3a` — whole-signal continuous control short forward `15m`, 10 bps, 96/96.
- `95c3ded1-5220-44c8-977e-958da19f8a6f` — corrected threshold-band continuous `15m`, original window, 5 bps, 96/96 — 48/96 positive, approximately flat median return, median drawdown about −18.0%.
- `c9226973-0b64-4c70-bc2d-4c408af838c2` — corrected threshold-band continuous `15m`, original window, 10 bps, 96/96 — 37/96 positive, median return about −5.00%.
- `8dfae36f-4c62-41b9-9a2d-9848d32d5b81` — corrected threshold-band continuous short forward `15m`, 5 bps, 96/96 — 32/96 positive, median return about −1.64%.
- `c9cced6e-19c8-40f0-acae-21c53297ac88` — corrected threshold-band continuous short forward `15m`, 10 bps, 96/96 — 22/96 positive, median return about −2.53%.
- `35206de0-72f1-4ec2-8f88-c65a3b194227` — BTC Binance USDM `15m`, 5,000-bar full-retention `px_slope_sniper` diagnostic used only for the return-blind normalized VWAP-slope distribution; not strategy-economic evidence.
- `308801b5-4374-4401-ba25-7045368db69f` — ETH Binance USDM `15m`, same return-blind slope-distribution diagnostic.
- `8906c8a0-372d-4c08-92c5-8a65fc373a67` — SOL Binance USDM `15m`, same return-blind slope-distribution diagnostic.
- `e7c1c0ba-4ad6-48c0-8a1b-dc1be384ba6d` — invalid BTC Binance USDM `15m` `px_threshold_slope` runtime smoke; a missing subclass transition guard caused hold-bar resizing and 535 fills. Do not use as economic evidence.
- `409b607a-7907-4eae-8c4d-02a42b712a5a` — paired unchanged `px_threshold` smoke on the identical BTC candles; its 32 fills exposed the slope subclass execution mismatch. Diagnostic control only.
- `4089eaee-4f74-4e28-b294-f79e3d03f135` — corrected BTC Binance USDM `15m` slope-gate smoke; 19 fills versus 32 for the paired base control, confirming transition-only runtime behavior before the longer matrix.
- `5ce4aa11-60b9-4b91-8a0c-6b6494ccc3d0` — disjoint 20,000-bar Binance USDM `15m` threshold control, 5 bps intended slippage; 30 paired successes.
- `f1b57f85-c92c-4833-9e92-782255b761dd` — identical intended-cost slope gate; broad paired return/drawdown improvement and materially fewer severe drawdowns, but negative median return.
- `8fb88390-5f92-456b-b716-77d9c2eef65f` — identical threshold control at 10 bps stress.
- `8fbde7bc-937a-4f1c-8ad2-1b96b97518d0` — identical slope gate at 10 bps stress; improvement survived stress but median return remained negative.
- `17b63d0d-511a-4d06-bcb5-db9d054fa50d` — Binance USDM `15m`, 20,000-bar `±0.9` threshold-only entry test, 5 bps; 30 paired successes, broad improvement versus `5ce4aa11`, still negative-median return.
- `94dcfa45-9003-4fe6-b558-2cc4aa798d6c` — identical `±0.9` threshold-only test at 10 bps; broader positive breadth and fewer severe drawdowns than `8fb88390`, still negative-median.
- `616fe951-6714-45c8-963b-d4ae500a33b5` — Binance USDM `15m`, 20,000-bar `±0.9` entry / `±0.5` exit test at 5 bps; 30/32 successes, decisively worse than the paired `±0.9`/`±0.1` reference. No 10 bps follow-up.
- `6138d5ed-5ca0-4500-b0c1-02eed1309702` — failed BTC/WLD/NEAR 20,000-bar full-retention batch; calculations completed but artifact flush timed out. No chart evidence.
- `3dad09f0-9f52-45ad-91d7-c3ea39716066` — failed three-asset 5,000-candle full-retention batch; roughly 15,000 detailed bars still exceeded the current flush budget. No chart evidence.
- `e87153c9-f7e5-415c-8711-8a5df2e32e7a` — BTC final-5,000-candle `±0.9` full-retention visual fixture; artifacts available.
- `a0cc6330-01f2-4754-ab6a-a6fffea27901` — WLD matching full-retention visual fixture; artifacts available.
- `6b207683-c927-45eb-b444-6c102101835e` — NEAR matching full-retention visual fixture; artifacts available.
- `e88e7013-9f93-48c8-aefc-e1ee197ed092` — BTC Binance USDM `15m` dual-domain traversal study, first chronological 10,000-bar half; raw-price episodes plus price/signal competing-barrier trials.
- `d474a327-d619-49ed-863d-fa6340bf1569` — matching second chronological 9,999-bar half; replication artifact, not a protected holdout.
- `52fa8f74-d7e7-4d5e-86a1-45612570ba20` — BTC Binance USDM `15m` fractional-depth schema-v2 anchor; fixed half-band price/signal attempts, episode traversal, and path excursions.
- `c36a7b0f-b0a0-4f68-92d3-e05906aef22e` — matching fractional-depth chronological replication; development-history replication, not a protected holdout.

Metrics retrieved via `get_saved_batch_run` on 2026-07-23 after the saved-run 404 was fixed. Re-fetch for full per-asset numbers; do not transcribe the 96-row grids here.

## Write Log

### 2026-08-06 — fractional-depth VWAP traversal shipped

Extended the isolated VWAP event study without changing strategy, Threshold Engine, nonlinear positioning, or persistence paths. Each closed bar now receives a piecewise band coordinate with mean-extension `0`, 1σ `1`, and 2σ `2`; fixed half-step crossings preserve both single-attempt competing barriers and retry-allowed VWAP-side episodes. Outputs retain price/signal and long/short identity and include durations, price traversal, MFE/MAE, episode reach rates, partial-without-next rates, and maximum depth. The anchor/replication result supports continuous location and bounded accumulation/distribution rather than exact full-touch/full-position commands, while failing to identify a monotonic or optimal nonlinear curve from depth alone. Twenty-five focused tests plus Ruff, formatting, mypy, function-length review, and diff checks pass. Generated artifacts remain under the KB's ignored `.research/runs/` workspace. No live runtime, capital mutation, database-write change, commit, or push occurred.

### 2026-08-06 — dual-domain VWAP band traversal study shipped

Added an isolated `event_study/vwap_band` package without changing Threshold Engine V3. The study reconstructs the saved RVWAP/PX signal, freezes price and signal-stat lookbacks at 100, detects closed-bar outward/inward crossings in raw-price and processed-signal domains, and records competing-barrier outcomes, path bps, MFE/MAE, cross-domain completion, and EMA-compatible first-touch episodes. Generated artifacts are rejected if the output path is inside `mm_v04` and are stored in the KB's ignored `.research/runs/vwap_band_traversal/` workspace. Two chronological BTC 15m halves reproduced the stricter transition structure; signal and price were strongly coupled, with only modest inward timing differences. Seventeen focused tests plus Ruff, formatting, mypy, function-length review, and diff checks pass. No live runtime, capital mutation, commit, or push occurred.

### 2026-08-06 — dynamic processed-signal band baseline implemented

Implemented the distinct registered `px_signal_bands` identity after the fixed `±0.9`/`±0.5` capture attempt failed. The baseline enters full threshold-only risk on a moving processed-signal outer-2σ crossing and exits inward at the same-side 1σ band; moving crossings compare each signal observation to its contemporaneous band. Following the existing EMAC escalation pattern, the moving-band snapshot and transition logic is local to this strategy; shared Threshold Engine V3 and its DTOs remain unchanged. This identity synchronizes raw price-extension and processed-signal-stat lookback lengths at 100 while preserving their different domains. It emits display-only normalized VWAP slope, VFTI, PRI, RSI, ATR anomaly, volume anomaly, absorption, and ROC using Indicator Lab conventions; none gates trading. Dynamic escalation, stops, PnL-aware sizing, and feature rules remain excluded. Seventeen focused PX strategy tests pass; focused Ruff, formatting, and mypy are clean. Awaiting Destin's manual UI strategy registration before the first bounded full-retention smoke. No live runtime, capital mutation, commit, or push occurred.

### 2026-08-06 — fixed `.5` exit rejected and chart failure localized

Run `616fe951` changed only the `±0.9` threshold-only exit from `±0.1` to `±0.5` on the same 20,000-bar Binance USDM 15m development window at 5 bps plus 1.5 bps fees/side. It reduced exposure duration but increased trades and broadly worsened economics and tails, so the planned 10 bps stress was skipped. NEAR full-retention inspection showed the core defect: price crossed profitably through the short average-entry area while the processed extension signal remained far from the fixed `.5` exit, then renewed continuation steamrolled the still-open position. This supports testing a dynamic inward 1σ capture boundary and separately visualizing market-state features; it does not establish any readiness rule. No live/capital mutation, commit, or push occurred.

### 2026-08-06 — `±0.9` entry threshold evaluated and visual fixtures bounded

Changed only threshold-only entry magnitude from `±0.5` to the forward-recorded `±0.9`, retaining `±0.1` exits, the 20,000-bar Binance USDM 15m development window, and 5/10 bps slippage plus 1.5 bps fees/side. The change broadly reduced activity and improved return/drawdown, but did not produce positive-median net return and had material counterexamples. Decision: preserve `±0.9` as a better development reference for full commitment, do not optimize another threshold on this window, and require visual/path review before choosing the next mechanism. Long full artifacts timed out under current persistence limits; a three-asset 5,000-candle batch also exceeded the aggregate flush budget. Separate 5,000-candle BTC/WLD/NEAR single runs persisted successfully and are the canonical visual fixtures. Current operating limit: summary retention for long economics; full retention only in individual jobs capped at 5,000 candles. No code, Linear, live/capital mutation, commit, or push occurred.

### 2026-08-06 — price and processed-signal band semantics separated

Destin noticed that a candle between the price 1σ/2σ bands did not occupy the analogous region in the signal panel. Code inspection confirmed the price overlay uses raw price-to-VWAP percentage extension with `LOOKBACK=100`, while signal statistics use the processed/normalized signal with `signal_stats_lookback=200`. The visual series are related but neither window- nor domain-equivalent. Prior fixed-threshold experiments remain valid because these signal-stat components were display-only; the discrepancy changes chart interpretation and must be resolved explicitly before using either band family for dynamic entries/exits. No code, backtest, Linear, live/capital mutation, commit, or push occurred.

### 2026-08-06 — backend average-entry chart exposes early full-risk commitment

Destin moved average-entry calculation from the frontend to the backend, so saved/full single-asset views now place the orange average-entry series against the same canonical position path. Visual inspection of the `±0.5` threshold control shows repeated positions opened before the eventual extension extreme: average entry remains fixed while price continues materially against the full-size position, and the position panel confirms there is no basis-improving escalation. Recorded this as path evidence—not a performance verdict—that `±0.5` is likely too early for full commitment. The next isolated `±0.9` test should predict fewer entries and better entry location/adverse excursion, then pair batch economics with full-retention chart review. The same observation strengthens the later hypothesis that an earlier threshold may identify setup state while more extreme bands govern escalation or full risk. No code, backtest, Linear, live/capital mutation, commit, or push occurred.

### 2026-08-06 — low-slope interpretation downgraded to hypothesis

Destin's chart inspection challenged the stronger interpretation that VWAP slope should be “flat enough” at price extremes. A return-blind re-read of the saved BTC/ETH/SOL 15m slope diagnostic runs (`35206de0`, `308801b5`, `8906c8a0`) supports that concern: absolute PX extension and absolute normalized VWAP slope increase together consistently, and the `.1` low-slope state becomes rare at the largest PX extremes. Revised the durable conclusion: MON-163 proved that the specific low-slope gate materially changed risk and economics on its evaluation window; it did not prove low slope is the correct semantic use of slope. Preserve competing hypotheses around absolute slope, slope extremity, PX/slope sign alignment, and slope change/deceleration. Do not reopen or tune the completed gate; use a return-path event study before another slope implementation. No new backtest, code, live/capital mutation, commit, or push occurred.

### 2026-08-05 — VWAP slope/regime filter evaluated on disjoint Binance history

Completed MON-163 without changing the preregistered identity. The window requested 20,000 Binance USDM 15m bars immediately before the original Hyperliquid study; 30/32 current liquid-panel assets completed both strategies, while LIT and SKR lacked the required full span and failed symmetrically. At 5 bps, the slope gate cut trades from 4,078 to 2,332, improved return on 22/30 assets and drawdown on 21/30, moved median return from −17.4% to −2.6%, median drawdown from −46.7% to −38.1%, and severe-drawdown count from 23 to 11. At 10 bps, it improved return on 24/30 and drawdown on 23/30, moved median return from −27.3% to −10.0%, median drawdown from −48.9% to −39.5%, and severe-drawdown count from 24 to 13. Positive breadth improved but remained insufficient for promotion. ETHFI was the clearest missed-profit counterexample; do not respond with asset exclusion or slope tuning. Decision: support slope as a real failed-reversion/risk-reduction mechanism, reject promotion of the present threshold+slope mapping, freeze `SLOPE_LOOKBACK=3` and `max_abs_slope=0.1` on this evidence, and close MON-163. No live/capital mutation, commit, or push occurred.

### 2026-08-05 — VWAP slope-gate identity frozen and implemented

Destin selected threshold-only behavior, normal VWAP-slope normalization, entry-only gating with ordinary exits, and a provisional three-bar slope lookback. A return-blind Binance USDM 15m distribution check across BTC, ETH, and SOL showed that normalized absolute slope `0.1` is near the ordinary-bar median while admitting only about one-third of fresh `±0.5` extension crossings, so `0.1` was frozen as a materially selective first regime boundary. Implemented registered strategy `px_threshold_slope`: rolling-VWAP log-linear slope, three-bar slope lookback, existing 252-bar min-max scaling with true slope direction, `abs(slope) <= 0.1` for fresh entries only, skipped blocked crossings, unchanged threshold exits, and normalized slope UI emission. The first runtime smoke exposed a missing subclass transition guard: invalid run `e7c1c0ba` resized on hold bars (535 fills) while paired base control `409b607a` had 32. Restored the guard and added the negative-path regression; ten focused PX threshold tests pass, and focused Ruff/source mypy are clean. Linear MON-163 is In Progress. The database strategy entry exists; the code reload stopped the research manager, so corrected smoke and economic runs await an explicit research-manager restart. No valid economic slope-gate backtest, live/capital mutation, commit, or push occurred.

### 2026-08-05 — catalog readiness-tool map recorded

Mapped plausible Trading Catalog tools into the confirmed VWAP thesis so later work does not need to rediscover them. VWAP slope is the isolated regime filter. VFTI and PRI are the strongest direct readiness candidates; volume/ATR anomalies, volume-delta disagreement, and absorption may qualify exhaustion or failed continuation; order-book imbalance, funding, and trade speed provide later participant/execution context; RSI leaving an extreme is a correlated control requiring incremental-value evidence. Recorded mechanism, rationale, and boundary for each. This is a reusable candidate map, not permission to bundle features; no code, backtest, Linear, live/capital mutation, commit, or push occurred.

### 2026-08-05 — strategy thesis explicitly confirmed

Destin confirmed the first explicit thesis card for the VWAP program. The strategy targets statistically unusual price extension from rolling VWAP, but is not unconditional liquidity provision or a generic fade of price moving away from its average. Because price can trend away and convergence with a moving VWAP may occur through price, VWAP, or both—and too late to monetize—the trade requires observable readiness for inward travel plus regime avoidance. Separate location, readiness, regime, and risk/capture layers. Destin has additional participant-readiness tools to introduce; preserve that layer as open rather than inferring its contents. Mirrored the concise thesis into the Linear project; no code, backtest, live/capital mutation, commit, or push occurred.

### 2026-08-05 — PX magnitude signal statistics forwarded to UI

Before beginning the slope/regime branch, added the established EMAC V4/V5 magnitude-stat pattern to the shared `px_threshold` feature path inherited by `px_threshold_continuous`. The strategy now calculates `sig_extension` over a configurable `signal_stats_lookback` defaulting to `200` and emits only `pos_mean`, `neg_mean`, `upper_band_1`, `lower_band_1`, `upper_band_2`, and `lower_band_2` as components of the existing PX signal message. The raw processed signal remains the `value` component. The backtest chart already renders non-value signal components as signal studies, so no frontend recomputation or schema change was required. Preserved concurrent price-overlay emission for VWAP mean and 1σ/2σ price bands. Ten focused PX threshold tests, Ruff, and focused mypy pass. No backtest, Linear, live/capital mutation, commit, or push occurred.

### 2026-08-05 — 2σ-band plus escalation outcome hypothesis

Destin recorded a forward prediction: the apparent improvement from raising processed-signal entry magnitude from `0.5` to `0.9` points toward more selective extreme-extension trading, and he expects the strongest VWAP result to use the calculated two-standard-deviation price bands as the trade mechanism together with signal escalation. This is a directional, unvalidated outcome hypothesis. `0.9` processed signal and the dynamic 2σ band are not treated as equivalent. Exact band transitions, escalation levels, sizing, exits, reversals, and tail-risk behavior remain open. Continue the existing independent Ready branches as-is; do not bundle this hypothesis into them.

### 2026-08-04 — PX chart bands and later threshold note

Destin observed that an entry magnitude of `0.9` appears materially better than `0.5`; record symmetric `±0.9` as the first entry-threshold setting when sensitivity testing is reached, without changing the current experiment or treating it as validated. Added the already-calculated PX `upper_band_2_price` and `lower_band_2_price` values to the same `IndicatorMsg` stream as RVWAP for `px_threshold` and inherited `px_threshold_continuous`, so full-retention backtest charts can overlay the price bands without frontend recomputation. Ten focused threshold tests, Ruff, and focused mypy pass. Backend lifecycle, live runtime, and capital were not mutated.

### 2026-08-04 — corrected threshold-band continuous evaluation

Ran the corrected `px_threshold_continuous` identity unchanged across the exact original and short-forward 15m windows at 5/10 bps slippage plus 1.5 bps fees/side. All four 96-asset batches completed and persisted. Compared with the prior whole-signal control, mapping the admitted band to the full position range increased trades and exposure, reduced original intended-cost breadth from 58/96 to 48/96, moved median return from +2.71% to approximately flat, and worsened median drawdown from about −12.8% to −18.0%. Original stress was negative-median; both forward runs remained negative, with only 32/96 and 22/96 positive. Worst losses were distributed rather than explained by one coin: the worst five represented about 29% of losing-asset PnL at original 5 bps and about 21% forward, with ZEC the worst original return/drawdown and STRK the worst forward return. Decision: reject the corrected mapper as a monetization improvement and do not tune it on these windows. PnL-aware resizing, a wide stop, and a slope/regime filter remain separate candidate mechanisms; no live or capital mutation occurred.

### 2026-08-04 — threshold-band mapping correction and new risk hypotheses

Destin reviewed `px_threshold_continuous` and identified that it used the generic whole-signal mapper despite being threshold gated. Corrected it to the existing threshold-aware `signal_to_position_banded`: each active state's exit magnitude is the zero-size inner edge and entry magnitude is the full-size outer edge. The prior four runs remain useful whole-signal controls but are not the intended identity. Thirty-two focused mapper/threshold tests plus Ruff and mypy pass. Destin also identified two separate mechanisms: PnL-aware resizing to avoid mechanically realizing losing adjustments, and a wide stop loss to cap catastrophic failed reversions. Stop trigger/execution/rearm semantics and exact PnL-aware increase/reduction rules remain open; do not combine them with the corrected baseline. Backend reload stopped the research manager; no restart, new run, live, or capital mutation occurred.

Destin subsequently confirmed the PnL-aware direction while deliberately leaving exact semantics open: allow scaling in, generally defer discretionary scaling out until the position is profitable, and always permit threshold/stop exits. Preserve both this and the wide-stop idea for later one-mechanism-at-a-time tests.

### 2026-08-04 — threshold-gated continuous evaluation

Destin clarified that the frozen `0.4` rebalance floor came from a manual one-night grid where it stood out; it is a useful frozen baseline, not an empirically correct value. Ran `px_threshold_continuous` at 15m across the exact original and short-forward windows under 5/10 bps slippage plus 1.5 bps fees/side. Continuous scaling reintroduced meaningful but bounded turnover and substantially reduced full-state path risk: original median drawdown fell to about −13% with positive intended-cost economics and no insolvency failures; forward median drawdown fell to about −4%. Original stress was near breakeven, while both forward runs remained negative. Decision: the continuous mechanism did what it was meant to do on path dependency, but regime dependence remains the monetization blocker. Await Destin's continuous-position commentary before choosing Binance threshold sensitivity versus a VWAP-slope regime filter. Four saved run IDs are in the registry; no live or capital mutation.

### 2026-08-04 — threshold-gated continuous implementation

Destin clarified the economic acceptance criterion: continuous scaling necessarily reintroduces turnover, and that can be beneficial through lower path dependency and faster compounding; only unprofitable churn is the problem. Implemented registered strategy `px_threshold_continuous` as a distinct identity. It retains the processed VWAP mean-reversion signal, negative polarity, `±0.5`/`±0.1` threshold state gate, volatility reduction, and the frozen baseline's `MIN_ADJUSTMENT_VALUE_PCT=0.4`; processed signal magnitude continuously sizes exposure within the allowed state. Independent threshold state survives position resizing, small adjustments below the original floor are omitted, and exits close regardless of the floor. Eight focused threshold tests, focused Ruff, and source mypy pass. Awaiting Destin's manual UI registration before research runs; no runtime restart, live, or capital mutation.

### 2026-08-04 — 5m threshold-only evaluation

Applied the unchanged `px_threshold` identity to the exact frozen 5m comparison window and the immediately following July 23–August 4 window at 5/10 bps slippage plus 1.5 bps fees/side. Hysteresis again cut trades about 95%. The original 5 bps result was promising, but ACE crossed into negative equity and failed the compounding notional guard; the original 10 bps result was negative-median. Both complete forward runs failed broadly, with only 30/96 and 16/96 positive. A first forward 5 bps attempt `0063d9fa` completed 89/96 because seven Hyperliquid fetches hit HTTP 429; it was replaced by complete cached rerun `c9b39f48` and is not economic evidence. Decision: reject threshold-only 5m, retain 15m as the stronger horizon, and keep threshold-gated continuous sizing as the next distinct identity. No live or capital mutation.

### 2026-08-04 — threshold-only tail follow-up

Clarified the quick diagnostics used after the intended-cost run. Breadth was a direct count of per-asset saved results above zero return (plus Sharpe/profit-factor threshold counts); the initial “tail concentration” wording referred only to sorting per-asset maximum drawdown and return, not a separately computed concentration statistic. A follow-up quantified concentration: 12 assets with drawdown at or below −40% represented about 49% of total losing-asset return magnitude; the worst five losers represented about 29%. Severe tails were more common in the current bottom volume quartile, but the full-universe volume/drawdown rank relationship was negligible and ZEC was a high-volume exception. Preserve VWAP slope as a candidate failed-reversion filter; do not introduce a post-hoc coin-quality exclusion rule.

### 2026-08-04 — threshold-only evaluation

Ran the preregistered `px_threshold` identity across the exact frozen 15m comparison window and the existing short forward window at 1.5 bps fees/side plus 5/10 bps slippage/side. The original window showed a real capture improvement: ~95% fewer trades, positive median economics at both costs, and improved breadth. The mechanism also exposed its expected weakness: full-size state persistence materially worsened drawdowns, including an approximately −89% ACE drawdown. Both forward runs were negative-median. Decision: preserve threshold-only as evidence that hysteresis solves churn, do not tune its levels on the original window, and move the next distinct test to threshold-gated continuous sizing. Four saved run IDs are in the Run Registry. No live or capital mutation.

### 2026-08-04 — strategy path map and threshold-only start

Destin confirmed the forward map: threshold-only, threshold-gated continuous sizing, a distinct VWAP slope/regime filter, and later escalation-ladder transfer; Binance is available for longer history because Hyperliquid supplies only roughly 5,000 bars. Implemented the first identity in `mm_v04` as registered strategy `px_threshold`, reusing the processed PX/VWAP mean-reversion signal and Threshold Engine V3 for transition-only full long/flat/full short states. The strategy locks the frozen study's negative signal polarity; initial entry/exit levels are symmetric `±0.5`/`±0.1` starting hypotheses. Four focused tests, focused Ruff, and focused mypy pass. The strategy still needs Destin to add it manually in the UI before it appears in the running backtest manager; no research run or runtime restart occurred.

### 2026-08-03 — forward follow-up

The planned preceding April 12–June 2 Hyperliquid disjoint window was unavailable (0/96 candles; failed attempts `310571f4` and `358a59e1`, no performance evidence). Ran the only clean fallback: a non-overlapping July 23–August 4 forward diagnostic. The 15m/0.8 variant was negative-median at both 5 bps and 10 bps and retained only 28/96 and 21/96 positive assets. This short window does not settle signal validity or passive execution, but it rejects promotion and further same-window tuning of the rebalance floor. Destin wants the frozen baseline revisited after mock limit-orderbook/passive-fill modeling exists and now wants to consider explicit next strategy changes. No live or capital mutation.

### 2026-08-03

Completed MON-159's same-window realistic-slippage gate with immediate-execution assumptions preregistered at 1.5 bps fees/side, 5 bps intended slippage/side, and 10 bps stress slippage/side. Frozen 5m failed broadly; frozen 15m became marginal at intended cost and failed broadly under stress. Used the allowed one bounded capture fix on 15m only: raising `MIN_ADJUSTMENT_VALUE_PCT` from 0.4 to 0.8 cut trades about 41% and restored broad positive intended-cost evidence, but the 10 bps stress remained negative-median. Current decision: reject the 5m current mapping, narrow to the 15m/0.8 candidate, and require a disjoint-window dual-cost validation before promotion. All six 96-asset batches completed and persisted; IDs are in the Run Registry and MON-159. No live or capital mutation.

### 2026-07-23 05:21 EDT

Created the Linear project and recorded the overnight `1m`/`5m`/`15m` Hyperliquid batches. Destin froze the baseline at length `200` / minimum adjustment `0.4`, named `1m`/`5m`/`15m` as the prime cluster, and noted `30m` trails off. Strategy currently has no threshold controls or signal-stat overlays. Saved lookups `404`; 5m/15m live summaries confirm 96/96 assets. No live/capital mutation.

### 2026-07-23 16:13 EDT

Created this research doc in the two-layer format and added the thread to the [[research/trading/research_index|Research Board]]. Next: recover the exact strategy identity/config and reproduce the frozen baseline before pressure-testing.

### 2026-07-23 17:12 EDT

Confirmed strategy identity + full config with Destin (recorded in Fixed Assumptions): `px` / `SOURCE=rvwap` / `SIG_POLARITY=negative` / `SIG_TO_POS_SIZE=direct` / `LEN 200` / `LOOKBACK 100` / `MIN_ADJUSTMENT_VALUE_PCT 0.4` / init cap 100k / fees 0.00015 (fraction, ≈1.5bps) / slippage 0.05 (bps, ≈0). Traced cost semantics in code: fees are a fraction applied per fill (`mock_services._compute_fee`), slippage is bps applied to fill price (`_compute_fill_px`) but the runs used ≈0, and `total_slippage`/`gross_pnl_before_fees` reporting has a minor unit/decomposition muddle (Destin has deferred fixing). Net take: the "survives costs" read is net of fees only; realistic-slippage stress is the true monetization gate. Also found the Research-MCP batch cap (`MAX_BATCH_ASSETS=32`, `assets` must cover ids exactly) — a reproduction rerun attempt was blocked by it and not yet completed. No live/capital mutation.

### 2026-07-23 16:47 EDT

Saved-run 404 fixed by Destin; pulled all three batches via `get_saved_batch_run`. All 96/96 assets completed each timeframe. Findings: 5m and 15m show a broad universe-wide edge (66/96 and 69/96 assets positive, 59–60 with Sharpe > 1, 83–85% win rates, median returns +2.8%/+8.3% over ~15/49-day windows); 1m is bimodal (42/96 Sharpe > 2 but ~half negative → median flat), an asset-selection story rather than a universe edge. Turnover is extreme (~580–700 trades/asset, avg hold ≈ 0) and it is unconfirmed whether these metrics include fees/slippage — so realistic-cost survival is now the explicit gating question. Updated the living head, Current Read (validity supported at 5m/15m; monetization open/decisive), and Run Registry accordingly. No live/capital mutation.
