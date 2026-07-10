# Lookback 20 Smoke Artifact Review

Run: `9916f36b-607a-4c8c-a911-392103f12f12`

## Sanity Check

- 1,000 candles loaded completely; 980 bars scored after the 20-bar warm-up.
- 980 signal rows: 484 long, 461 short, and 35 initial flat rows before the first breakout.
- 23 orders / fills for 18 completed trades. The five additional fills are bounded notional adjustments after applying the 5% rebalance buffer.
- Position exposure is active for 96.4% of scored bars, consistent with holding direction until an opposite breakout.
- The 2x-fee run remained positive (`7.75%` net return).

## Caveats

- `avg_hold_bars` reports `0.0` despite persistent signal and position exposure. Do not use this field for interpretation until its metric semantics are checked.
- This is a rolling recent-data smoke run, not the preregistered discovery range.
- Headline Sharpe is based on a short approximately 41-day window and is not promotion evidence.

## Decision

Artifacts match the intended strategy lifecycle well enough to continue into an explicit-range discovery rerun. Do not broaden the parameter search from this smoke window.
