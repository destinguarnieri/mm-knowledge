# MON-98 Backtest Sizing Smoking Gun

Date: 2026-07-02

## Summary

Controlled Research MCP repro confirms the user-visible backtest sizing issue: at higher configured max position percent, risk and costs continue increasing, but 100% total return underperforms 50%.

2026-07-02 update: after Docker compose down, a local full-detail diagnostic correctly emitted `leverage_value=10` and `margin_used=value/10`. The canonical 10/50/100 set below was rerun against the local-only backend and remains a valid smoking-gun repro.

Earlier 1h/500-candle runs were exploratory and are not the canonical repro.

Related pages:

- [[Backtesting and Evaluation]]
- [[mcp-v1-contract]]
- [[research-mcp-checkpoint]]

## Canonical Repro Settings

- Asset: BTC
- Strategy: `emac`
- Interval: `30m`
- Minimum candles: `1000`
- Initial capital: `100000`
- Fees: `0.00015`
- Slippage: `0.05`
- Leverage: `10`
- Margin: cross
- Position settings: `max_position_percent` at `10`, `50`, and `100`
- Strategy params:
  - `fast_window=20`
  - `slow_window=60`
  - `SOURCE=close`
  - `SYMETRIC=true`
- Strategy config defaults:
  - `SIG_POLARITY=positive`
  - `SIG_TO_POS_SIZE=direct`
  - `SIG_SCALE=min_max`
  - `SIG_SCALE_LOOKBACK=252`
  - `SIG_SMOOTH=0`
  - `SIG_CLIP_MAX=true`
  - `SIG_BUFFER_TYPE=none`
  - `SIG_BUFFER=0`
  - `VOL_ADJ_POS_SIZE=inverse`
- Trade config defaults:
  - `ENTRY_THRESHOLD=0`
  - `EXIT_THRESHOLD=0`
  - `STOP_EXIT_THRESHOLD=0`
  - `MIN_POSITION_VALUE=100`
  - `MIN_ADJUSTMENT_VALUE=20`
  - `PROFIT_AGG=1`
  - `ENTRY_AGG=1`
  - `REDUCE_AGG=1`
  - `MIN_POSITION_VALUE_PCT=0`
  - `MIN_ADJUSTMENT_VALUE_PCT=0`
  - `MIN_ADJUSTMENT_CLIP=false`

## Saved Runs

| Position % | Run ID | Bars | Trades |
| --- | --- | ---: | ---: |
| 10% | `9596d52b-6d38-4357-858a-97f876eda686` | 1940 | 1015 |
| 50% | `98369b3f-072e-4476-912d-98492d8eaaf9` | 1940 | 1017 |
| 100% | `4f636dd5-308f-4891-bc54-9c00d55fb4e1` | 1940 | 996 |

## UI Headline Metrics

| Metric | 10% | 50% | 100% |
| --- | ---: | ---: | ---: |
| Total Return | 5.33% | 20.05% | 18.69% |
| Sharpe Ratio | 1.94 | 1.92 | 1.88 |
| Vol Annual | 25.90% | 129.54% | 259.09% |
| Max Drawdown | -7.26% | -34.52% | -62.23% |
| Max Pos DD | -93.50% | -78.12% | -66.34% |
| Total Fees | -632.35 | -4,079.47 | -10,471.26 |
| Trade Win Rate | 55.86% | 54.47% | 48.90% |
| In Money | 68.99% | 68.06% | 65.27% |
| Avg Win | 23.15 | 127.40 | 307.80 |
| Avg Loss | -19.82 | -119.51 | -269.25 |
| Max Win | 301.52 | 2,324.07 | 8,027.81 |
| Max Loss | -469.42 | -2,264.29 | -4,325.28 |

## Interpretation

This is the user-facing smoking gun:

- 50% total return is 20.05%.
- 100% total return is only 18.69%.
- 100% still carries much higher volatility, drawdown, max position drawdown, and fees.
- Trade win rate and in-money rate degrade as configured exposure increases.

The issue should be investigated before treating headline backtest comparisons as trustworthy.

## Artifact Drill-Down

Hydrated local-only artifact comparison found:

- Signals match exactly across 10%, 50%, and 100% runs, so the divergence is not signal generation.
- Valid local-only position artifacts now carry `leverage_value=10` and `margin_used=value/10`.
- 100% trades a superlinear turnover path versus 50%: total volume is `69.81M` versus `27.20M`, or about `2.57x`, not `2x`.
- Fees follow that turnover: 100% fees are `-10,471.26` versus 50% fees of `-4,079.47`, or about `2.57x`.
- The 100% run builds a large mid-run advantage, peaking about `46.3k` realized PnL above 50%, then gives it back in later loss clusters. Final realized PnL is `7,618.48` for 100% versus `13,206.64` for 50%.
- Zero-cost isolation (`fees=0`, `slippage=0`) removes the inversion: 100% returns `26.23%` and 50% returns `23.32%`. Risk remains about 2x higher at 100%, and return still does not scale linearly.
- Fee-only isolation (`fees=0.00015`, `slippage=0`) reproduces the inversion: 100% returns `17.31%` and 50% returns `19.34%`.
- Slippage-only isolation (`fees=0`, `slippage=0.05`) does not reproduce the inversion: 100% returns `25.92%` and 50% returns `23.18%`.

Current conclusion: the 50% > 100% headline inversion is primarily fee drag applied to a path-dependent, superlinear turnover curve. This is not a display-only bug and not a stale leverage-artifact issue.

## Turnover Mechanism

The final drill-down explains how the superlinear turnover arises:

- EMAC sizes each bar from `current_equity * max_position_percent * leverage`, then applies signal, position limits, volatility adjustment, and a full market rebalance delta.
- Actual 100%/50% exposure ratio tracks the compounded equity-base ratio almost exactly. Average actual exposure ratio is about `2.22x`; the average target-base ratio implied by equity is also about `2.22x`.
- During the profitable middle of the run, 100% equity rises much faster than 50% equity, so the 100% target base grows above `2x`. Around bar `641`, 100% equity is about `1.323x` 50% equity, so the 100%/50% max target-base ratio is about `2.645x`.
- Final equity ratios compress back near parity (`100% / 50% ~= 0.989`), so the 100% run pays to scale up in the favorable regime and then scale down through later adverse/choppy regimes.
- A fixed `2x` version of the 50% signed exposure path would imply about `52.52M` of signed exposure movement. Actual 100% signed exposure movement is about `67.56M`, or `1.286x` higher than fixed-2x.
- Applying the changing compounded ratio to the 50% path reconstructs the 100% path movement. About `10.28M` of absolute movement comes from the ratio changing over time; because components can offset, treat this as a magnitude indicator rather than an additive PnL identity.
- Relative to simple `2x` volume (`54.39M`), compounded target-base weighting explains about `7.42M` of extra 100% volume, and the remaining measured uplift is consistent with the changing multiplier/path interaction plus rounding/execution precision.

Plain-language model: 100% is not just "the 50% run doubled." It is the same signal stream applied to a larger, self-changing equity base. Once its own PnL path diverges, the multiplier between 50% and 100% moves too, which creates extra rebalance volume and fee drag.

Open questions:

- Whether this is acceptable economics for the configured 10x / 100% notional exposure, or whether the UI/product expectation is fixed-notional proportional comparison.
- Whether current-equity compounding should remain default, become explicit in the UI, or get a fixed-initial-capital sizing mode for clean parameter comparisons.
- Whether the `slippage` unit contract is clear enough. Backend DTOs describe slippage as bps, so `0.05` means 0.05 bps, while other runtime comments refer to `0.05` as slippage tolerance.

## Resolved Environment Issue

Initial artifact drill found and resolved a backend routing/version issue:

- The strategy sizing path sees the supplied leverage and position percent.
- A diagnostic run with `max_position_percent=1` and `leverage=10` opened about `$9.5k` notional, proving strategy sizing used `100000 * 1% * 10x`.
- Before Docker compose down, emitted position artifacts reported `leverage_value=1` and `margin_used=value`, not `margin_used=value/10`.
- Direct local class sanity check against `MockTradingService` and `BacktestContext` emitted the expected `lev_value=10` and `margin_used=value/10`.
- After Docker compose down, Research MCP full-detail diagnostic also emitted `leverage_value=10` and `margin_used=value/10`.
- Conclusion: previous Research MCP runs were hitting the Docker backend, not the intended local backend code.
- Local-only canonical rerun still reproduces 50% total return outperforming 100%, so the core sizing/economic issue remains.
