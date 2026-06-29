# Money Machine Language

This is the shared trading language dictionary for Destin + agents working on Money Machine.

Purpose: reduce repeated explanation when translating screenshots, manual reads, and discretionary pattern language into strategy specs, UI stats, and backtestable code.

This doc is not a generic trading glossary. It should capture how we use terms in this repo. When a term is still fuzzy, mark it as provisional and refine it after screenshot/backtest mismatch reviews.

## How To Use This Doc

When designing strategy logic from a screenshot or manual read:

1. Add or update terms here before coding if language is ambiguous.
2. Translate each subjective phrase into observable predicates.
3. If backtest trades do not match the intended visual pattern, update the term definition or predicate mapping.
4. Prefer stable shorthand over verbose re-explanation once a term is defined.

## Entry Template

```md
### Term

Plain meaning:
-

Used when:
-

Observable candidates:
-

Not the same as:
-

Code/backtest notes:
-
```

## Core Translation Pattern

```text
screenshot / manual read
  -> Money Machine language term
  -> deterministic predicate(s)
  -> state machine transition
  -> backtest trade marker
  -> mismatch review
  -> refined term/predicate
```

The goal is not to make language sterile. The goal is to preserve the useful visual intuition while making it testable.

## Terms

### Regime

Plain meaning:
- The broad market behavior context a setup is happening inside.

Used when:
- Separating trend, chop, compression, reversal, reclaim, continuation, or breakdown contexts.

Observable candidates:
- Slow MA slope and price location relative to slow MA.
- Directional efficiency over a rolling window.
- ATR/range percentile.
- Sequence of pivot highs/lows.
- Band/trend-state color if using a strategy overlay.

Not the same as:
- A trade signal by itself.

Code/backtest notes:
- Regime should usually be a filter or state, not the entry trigger.

### Location

Plain meaning:
- Where price is relative to important structure right now.

Used when:
- Deciding whether a setup is clean, late, extended, midpoint chop, near invalidation, or into resistance/support.

Observable candidates:
- Distance to nearest support/resistance.
- Distance to moving averages/bands.
- ATR-normalized distance to levels.
- Position inside recent high/low range.

Not the same as:
- Directional bias.

Code/backtest notes:
- Bad location can invalidate otherwise good signals.

### Shelf

Plain meaning:
- A horizontal area price repeatedly respects, rejects from, or bases around.

Used when:
- Talking about support/resistance zones that matter more than a single tick level.

Observable candidates:
- Prior pivot high/low cluster.
- Repeated closes/wicks within tolerance.
- High-volume or high-touch zone if volume/profile is available.
- Manually supplied level in early versions.

Not the same as:
- Any single candle high/low.

Code/backtest notes:
- Implement as a zone with tolerance, not a single exact price.

### Reclaim

Plain meaning:
- Price loses a level or trades below it, then gets back above it in a way that matters.

Used when:
- Describing a potential bullish shift after breakdown/base behavior.

Observable candidates:
- Close above shelf/level after N bars below.
- Close above by X bps or X ATR fraction.
- Fast MA or short-term band flips up near the level.
- Optional volume/range expansion.

Not the same as:
- A wick above resistance.

Code/backtest notes:
- Usually needs a prior-below condition, a reclaim trigger, and an acceptance/failed-reclaim follow-up state.

### Failed Reclaim

Plain meaning:
- Price reclaims a level but cannot hold it and falls back below.

Used when:
- Avoiding late longs or defining short/reversal conditions.

Observable candidates:
- Close back below reclaimed shelf within K bars.
- Retest from below rejects after losing the shelf.
- Fast MA rolls over while price is below the shelf.

Not the same as:
- A normal shallow retest that holds.

Code/backtest notes:
- Needs a time window. A reclaim failing 3 bars later is different from failing 80 bars later.

### Acceptance

Plain meaning:
- Price does enough work above/below a level that the move is no longer just a wick or one-candle event.

Used when:
- Confirming a reclaim, breakdown, or range shift.

Observable candidates:
- N of last M closes above/below level.
- Retest holds with close back in direction.
- Minimum time spent beyond level.
- No close back through level within K bars.

Not the same as:
- Immediate breakout entry.

Code/backtest notes:
- Acceptance reduces false signals but enters later. Track this tradeoff explicitly.

### Retest Hold

Plain meaning:
- Price comes back to a reclaimed/broken level, tests it, and respects it.

Used when:
- Looking for cleaner entry after an impulse.

Observable candidates:
- Low/high touches level ± tolerance.
- Candle closes back on the correct side.
- Wick pierce allowed within tolerance.
- Follow-through candle confirms.

Not the same as:
- Blind limit order at the level.

Code/backtest notes:
- Define wick tolerance and required close behavior separately.

### Rejection

Plain meaning:
- Price tests a level or zone and is pushed away decisively.

Used when:
- Identifying failed upside/downside attempts or resistance/support response.

Observable candidates:
- Wick through level with close back below/above.
- Large opposite-color candle after test.
- Failed close beyond level.
- Momentum flips against the test.

Not the same as:
- Price pausing near a level.

Code/backtest notes:
- Rejection should include both test and response.

### Breakdown

Plain meaning:
- Price loses a meaningful support/shelf and accepts below.

Used when:
- Bearish continuation or failed support structure.

Observable candidates:
- Close below shelf by X bps/ATR.
- N of M closes below.
- Retest from below rejects.
- Increased range/ATR during loss.

Not the same as:
- A wick below support.

Code/backtest notes:
- Mirror of reclaim logic when useful.

### Compression

Plain meaning:
- Price movement tightens and directional progress slows.

Used when:
- Describing coiling before expansion or chop before impulse.

Observable candidates:
- ATR/range percentile below threshold.
- Bollinger/Keltner width contraction.
- Lower realized volatility.
- Overlapping candles in narrow range.

Not the same as:
- Low volume by itself.

Code/backtest notes:
- Compression often needs an expansion trigger; alone it is not direction.

### Impulse

Plain meaning:
- A strong directional move that changes local structure.

Used when:
- Describing breakout/reclaim momentum or liquidation-style moves.

Observable candidates:
- N-bar return > threshold.
- Candle body > ATR fraction.
- Consecutive directional closes.
- Break of local pivot with range expansion.

Not the same as:
- Slow grind.

Code/backtest notes:
- Impulse entries can chase; combine with location/extension filters.

### Extended

Plain meaning:
- Price has moved far enough from a fair/mean reference that fresh entries are lower quality.

Used when:
- Avoiding chase after vertical moves.

Observable candidates:
- Distance from fast/slow MA > X ATR.
- Distance from reclaim/shelf > X ATR.
- N-bar move percentile high.
- Price near next resistance/support with poor reward-to-risk.

Not the same as:
- Strong trend by itself.

Code/backtest notes:
- Extension can be a no-trade filter or require pullback/retest entry.

### Bad Location

Plain meaning:
- The setup may be directionally right, but current price is in a poor place to enter.

Used when:
- Avoiding midpoint chop, late entries into resistance, or shorts into support.

Observable candidates:
- Too close to next opposing level.
- Too far from invalidation.
- Middle of range between nearest support/resistance.
- Extended from trigger level.

Not the same as:
- Bad thesis.

Code/backtest notes:
- Bad-location filters are often what make coded trades match human discretion.

### Chop

Plain meaning:
- Back-and-forth structure with poor directional follow-through.

Used when:
- Avoiding overtrading or false signals.

Observable candidates:
- Low directional efficiency.
- Frequent MA/band crosses.
- Alternating candle direction.
- Price near middle of range.
- Breakouts/reclaims failing quickly both ways.

Not the same as:
- Compression, though they can overlap.

Code/backtest notes:
- Chop filters should be tested carefully; too strict can remove valid early reversals.

### Invalidation

Plain meaning:
- The condition that proves the trade idea is wrong enough to exit or avoid entry.

Used when:
- Defining risk and state-machine failure.

Observable candidates:
- Close back below/above key level.
- Loss of retest hold.
- Opposite state transition.
- Stop distance in ATR/structure terms.

Not the same as:
- Pain tolerance or arbitrary stop.

Code/backtest notes:
- Every strategy state should know its invalidation.

### At A Glance

Plain meaning:
- A UI/stat presentation that lets Destin understand the trading context without reconstructing it manually.

Used when:
- Designing manual trading clarity panels.

Observable candidates:
- Current regime label.
- Nearest level distances.
- Reclaim/breakdown state.
- Pullback depth.
- Volatility-adjusted room to next level.
- Active invalidation.

Not the same as:
- A black-box trade recommendation.

Code/backtest notes:
- Read-only first. Useful at-a-glance stats can later become strategy predicates.

## Screenshot Review Notes

When reviewing a screenshot, capture:

```md
## Screenshot Translation
- Ticker/timeframe:
- Intended side:
- What my eye sees:
- Key level/shelf:
- Entry I would want:
- Entry I would avoid:
- Invalidation:
- Term(s) from this dictionary:
- Predicate candidates:
- State-machine implication:
```

## Open Terms To Define Later

- liquidity sweep
- trap
- squeeze
- displacement
- absorption
- trend day
- mean reversion day
- auction failure
- value area / volume profile terms, if used
- risk-on / risk-off context
- relative strength / weakness
