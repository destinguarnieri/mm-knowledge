# Example Research Doc

Purpose: show the expected shape of a Money Machine research file in the two-layer format. This is an illustrative example, not real evidence; run IDs and numbers are fabricated.

How to use:

- The **living head** (TL;DR & What's Working → Current Read → Open Threads) is rewritten in place every session so it always reflects "now."
- The **append-only tail** (Run Registry, Write Log) is never edited — you only append.
- Follow [[research/trading/research_process_v2|Research Process V2]] and `.cursor/rules/research-continuity.mdc`. Persisted `run_id` values are the metric source of truth; **do not paste metric tables here** — cite run IDs and re-fetch numbers from the backtest UI / saved runs.
- Matching artifact folder holds `configs/`, `artifacts/[run-id]/`, and `review/`. Paths below are relative to that folder unless prefixed with `research/`.

Lane (Research Process V2 §0): **open discovery**. (Others: discretionary codification, capture engineering, cross-market extension.)

<!-- ================= LIVING HEAD — rewrite in place each session ================= -->

## TL;DR & What's Working

Testing whether a trend-continuation signal has directional edge and can be monetized after realistic costs on 1h bars, starting in crypto and intended to extend to equities.

**What's working — live threads:**

- **The entry signal beats noise (validity supported).** Against a random-entry null with matched exit/sizing/costs, the real entry is clearly better — the directional information is real. Cites: null `c4e8b219`, default `9f3b2a10`.
- **A stable parameter plateau exists.** Medium/slow windows around `fast=24, slow=96, entry≈0.35–0.45` survive nearby values rather than being a lone spike — a good sign for robustness. Cite: grid `5d2a7f14`.

**Not yet working (capture-open, not rejected):** the raw signal churns in chop and only clears *stress* costs weakly — this is a monetization problem, not a direction problem. The next job is capturing the edge, not re-proving it.

**Best next step:** add a slow-slope/chop filter to cut flat-regime losses, rerun the constrained grid around the plateau, then check the same region on ETH before any expansion.

## Current Read (provisional — not a verdict)

Two separate questions, separately gated (Research Process V2 §2). A row becomes a recorded Decision only at a promotion gate or explicit kill.

| Question | Current read | Confidence | Key evidence | What would change it |
|---|---|---|---|---|
| Signal validity — does it carry directional info? | Leaning yes | Med | beats random-entry null; stable plateau | plateau collapses on a fresh asset/window |
| Monetization — can a policy capture it after realistic costs? | Open (capture-open) | Low | raw signal churns; weak under 2× fee stress | slope filter clears realistic + stress costs |
| Cross-market — does it generalize to equities? | Untested | — | crypto only so far | run the frozen region on an equities 1h holdout |

## Open Threads / Next Experiments

Ranked, capture-first:

1. **Capture: slope/chop filter.** Require positive slow slope for longs / negative for shorts; test min slope `0`, `0.05`, `0.10`. Rerun the constrained grid around `fast=24, slow=96`. Goal: cut chop losses without destroying trade count. (Modify change 1 of the card's budget — but this is capturing a validated signal, not churn.)
2. **Validation asset.** Run the frozen candidate region on ETH 1h (quarantined; results must not tune params).
3. **Cross-market extension.** Re-point the portable signal at an equities 1h series (e.g. SPY/QQQ) as fresh holdout surface — a crypto-specific result would still be worth labeling, not discarding.

Deferred: broad multi-asset expansion until the slope-filtered region passes cost + artifact sanity.

<!-- ================= STABLE ================= -->

## Research Card

- **Lane / decision:** open discovery; decision = continue / modify / promote a trend-continuation config, per market.
- **Edge/mechanism hypothesis:** persistent directional moves continue long enough to overcome costs when entries avoid low-slope chop. Who pays: momentum-chasing and slow-to-adjust participants; should weaken in mean-reverting/range regimes.
- **Markets & venues in scope:** crypto perp 1h (discovery: BTC; validation: ETH); equities 1h as a later cross-market holdout. Asset class is an explicit axis.
- **Signal definition (portable):** trend signal from fast/slow windows + slope, expressed independently of any single venue.
- **Capture policy / params (market-specific):** entry/exit thresholds, slope minimum, sizing — re-derived per market.
- **Kill criteria:** < 30 validation trades; realistic-cost net < 0; max DD worse than −18%; isolated top config (nearby median Sharpe < 70% of top); turnover rising faster than net return without cause; > 60% of net return from one contiguous period.
- **Upside / capture thesis:** if validity holds, a turnover-reducing filter that clears realistic *and* stress costs on a plateau, generalizing to ≥1 other market, is worth promoting to a canary. "Good" = stable Sharpe ≈ 1 after realistic costs with explainable trades.
- **Data splits:** discovery BTC 1h 2025-01-01→2026-06-30; validation ETH 1h same range (quarantined); untouched holdout from 2026-07-01, consumed once at gates; each additional market is fresh holdout surface.
- **Regime/period segmentation:** calendar quarters, fixed before the first grid.
- **Costs:** realistic (`fee 0.00015`, `slippage 0.05`) AND stress (2× fees). Both reported.
- **Core knobs:** fast/slow windows, entry/exit thresholds, slope lookback/min. **Incidental:** chart display, artifact verbosity, run naming.
- **Search-budget counter:** cumulative configs evaluated (see Run Registry).

## Fixed Assumptions

- Initial capital `$100,000`; max position `50%`; leverage `3x`; sizing static for research comparability.
- Fees `0.00015`; slippage `0.05`; stress = 2× fees.
- Discovery range BTC 1h 2025-01-01 → 2026-06-30 (`13,104` candles); backend commit recorded per run.

<!-- ================= APPEND-ONLY TAIL — do not edit past entries ================= -->

## Run Registry (pointers, not tables)

Identity + interpretation index. Metrics live in the UI / saved runs — cite the run and re-fetch; do not paste metric tables. Keep discarded runs and mark why.

- `9f3b2a10-6e5c-4b8a-9d21-9c4a7e0f2b31` — single, BTC 1h — default baseline — `configs/example-default.json` — gross edge present, weak after cost stress.
- `2b6f9e33-1c7a-4f6e-8b52-3a8d5c9e0f14` — single, BTC 1h — no-filter baseline — `configs/example-no-filter.json` — higher gross but churny; worse DD → raw signal alone over-trades.
- `7a1d4c88-5f2b-4e9a-8c07-6b3f2d9a1e55` — single, BTC 1h — 2× fee stress — `configs/example-default-2x-fees.json` — weak cost robustness.
- `c4e8b219-3a7f-4d6c-9e10-8f2b5a6d3c07` — single, BTC 1h — random-entry null (seed in config) — `configs/example-random-entry.json` — clearly negative → entry signal beats noise (validity evidence).
- `5d2a7f14-9b3e-4c8a-a1f6-3e7c9b2d5a80` — batch/grid, BTC 1h — small structured grid — `configs/example-small-grid.json` — stable plateau near `fast=24, slow=96, entry 0.35–0.45`; lowest-threshold config wins on turnover and fails stress (rejected).

Search budget: `4` baselines + `54` grid configs = `58` cumulative. Review notes: `review/chop-loss-review.md`, `review/turnover-winner-rejection.md`.

## Write Log

Append when the question, data, strategy logic, interpretation, or decision changes. Terse; no metric dumps.

### 2026-07-08 09:10 EDT

Created the research card (open-discovery lane). Objective, kill criteria, upside/capture thesis, data splits, regime segmentation, and dual cost regimes written before any run. Plan: BTC 1h discovery, ETH 1h as quarantined validation, equities 1h as later cross-market holdout.

### 2026-07-08 10:35 EDT

Ran baselines `9f3b2a10`, `2b6f9e33`, `7a1d4c88`, `c4e8b219`. Validity evidence is positive: the entry beats the random-entry null under matched exit/sizing/costs. Monetization is the weak point — the no-filter version confirms raw trend signal over-trades, and cost robustness is thin. Framing: direction likely real, capture unsolved.

### 2026-07-08 12:05 EDT

Ran small structured BTC grid `5d2a7f14`. Profitable configs cluster on medium/slow windows into a plateau around `fast=24, slow=96, entry 0.35–0.45`; the sharpest winner is a turnover artifact that fails stress and is rejected. Plateau survives nearby values.

### 2026-07-08 13:20 EDT

Artifact review found losses concentrated in flat/choppy slow-slope segments. Decision: **modify** (add slope filter) and rerun the constrained grid before expanding. Objective unchanged. This is capturing a validated signal, not knob-churn on a dead idea — Current Read updated to validity=leaning-yes, monetization=capture-open.
