# Alpha Inbox

Purpose: capture potentially valuable trading ideas without interrupting funded research. An inbox entry is not a research project, commitment, or Linear task.

## Capture rules

- Capture in under 90 seconds.
- Title and observation are the only required fields.
- Screenshots, TradingView links, and rough thoughts are welcome.
- Do not begin researching while capturing.
- Return to the current primary after capture.
- Ideas enter the Research Board only after an explicit audition decision.
- Raw ideas never go directly into Linear.

## Inbox

### AI-YYYYMMDD-01 — Short descriptive name

- **Captured:** YYYY-MM-DD
- **Status:** inbox
- **Observation:** What did I see?
- **Market/timeframe:** Optional
- **Why it might work:** Optional rough mechanism
- **Trade expression:** Optional entry/exit/direction thought
- **Evidence:** Screenshot, TradingView link, or note
- **Related work:** Existing strategy, signal, or component if obvious
- **Time-sensitive:** no / yes — explain why

## Audition queue

Ideas selected for one bounded investigation.

### AI-20260813-01 — EMA-200 trend side and opposite-candle forward response

- **Captured:** 2026-08-13
- **Status:** audition pending
- **Source framing:** Destin proposed one event study with two parts and two claims. Both claims remain hypotheses until measured; no run IDs or results are attached yet.
- **Related work:** [[trading/catalog_v1|Trading Catalog]] `200 EMA` and `Opposite Only`; [[research/trading/emac-cross-10-200/emac-cross-10-200|EMA 10/200 Research]]; [[research/trading/ema_px_trend/codification|EMA/PX Trend Codification]]. This study isolates price relative to the 200-period EMA and does not require a 10/200 cross.
- **Portable trend-state definition:** on closed candle `t`, `close_t > EMA200_t` is the long trend state and `close_t < EMA200_t` is the short trend state. Equality handling, EMA price source, warmup, and whether the causal EMA value includes candle `t` must be frozen before measurement.
- **Part 1 — next-candle direction:** test whether the 200-EMA trend state changes the probability of candle `t+1` direction.
  - Long-side claim: when price is over the 200 EMA, candle `t+1` is more likely to close up than down.
  - Short-side inverse: when price is under the 200 EMA, candle `t+1` is more likely to close down than up.
  - Primary comparison: conditional direction probability versus the asset/timeframe's unconditional candle-direction base rate, not only versus `50%`.
- **Part 2 — opposite-candle forward return:** condition on a candle whose direction opposes the EMA trend state, then measure signed forward return over prespecified horizons `n`.
  - Long event: price is over the 200 EMA and candle `t` is down; enter long after the event is observable and test whether signed forward return is positive over horizon `n`.
  - Short event: price is under the 200 EMA and candle `t` is up; enter short after the event is observable and test whether signed forward return is positive over horizon `n`.
  - Keep gross signal validity separate from executable, after-cost monetization. Freeze entry timing (`close_t` with a feasible fill model versus `open_{t+1}`), exit mark, overlapping-event treatment, and realistic/stress costs before any trading claim.
- **Leading hypothesis:** a persistent long-term trend creates directional drift, while an opposite candle offers a temporary price concession before continuation.
- **Credible alternatives / nulls:** the effect is only the unconditional drift or candle imbalance of the asset/timeframe; opposite candles mean-revert regardless of EMA side; apparent edge comes from volatility/regime selection, overlapping horizons, or same-close leakage; the gross response exists but is too small or unstable to transact after costs.
- **Decision needed:** determine separately whether EMA side contains next-candle directional information and whether the opposite-candle condition adds positive signed forward response beyond trend state alone.
- **Cheapest useful test:** preregister one liquid asset/venue/timeframe development fixture; report both conditional probabilities and complements for Part 1; for Part 2 compare opposite candles with all candles in the same EMA state, same-direction candles, and a matched/null baseline across a small fixed horizon set. Preserve a disjoint untouched validation window before any expansion or parameter choice.
- **What would strengthen it:** both sides reproduce with economically meaningful lift over their conditional baselines, forward-return distributions remain favorable across adjacent horizons, and the result survives causal timing, non-overlapping/cluster-aware inference, validation, and realistic costs.
- **What would weaken or falsify it:** one-sided or regime-local results, no lift over base rates, disappearance under causal entry timing or independence controls, unstable horizon sign, or after-cost economics that reject the proposed transaction mapping while leaving only descriptive trend evidence.
- **Audition outcome:** pending. Required design inputs before execution: deployment market/venue, timeframe(s), EMA source convention, fixed horizon set, entry timing, data splits, and cost regimes.

### AI-YYYYMMDD-01 — Name

- **Decision needed:** What would the audition determine?
- **Cheapest useful test:** Smallest evidence capable of changing our view
- **What it could displace or improve:** Current candidate/component
- **Audition outcome:** pending

## Processed

Move reviewed ideas here with one outcome:

- **Promoted:** Added to the Research Board
- **Merged:** Belongs inside an existing candidate or mechanism
- **Incubating:** Worth retaining, but not worth research capacity now
- **Closed:** No longer worth retaining, with a one-line reason
