# N-Bar Breakout

Related process: [[research/trading/research_process_v1|Research Process V1]]

## Status

- Research state: idea triage / smoke baseline.
- Current decision: test.
- Last updated: 2026-07-09 18:10 EDT.
- Strategy: `n_bar_breakout`.
- Initial asset/timeframe: BTC 1h.

## Write Log

### 2026-07-09 18:10 EDT

Created the strategy and research card before the first run. This is a deliberately
small dogfood project: test a classic channel breakout and observe friction in the
current Research MCP workflow. The strategy enters long above the prior N-bar high,
enters short below the prior N-bar low, and holds until the opposite breakout.

The connected Research MCP currently exposes the strategy and typed config, but its
tool schema does not expose explicit date ranges or the newer suite tools. Any
rolling-window smoke run is therefore operational verification only and is excluded
from discovery evidence.

### 2026-07-09 18:18 EDT

Completed seven rolling-window workflow runs. The unbuffered first run produced 894
fills and 436 counted trades because fixed-notional sizing rebalanced almost every
bar; it is discarded. Adding a 5% minimum adjustment buffer reduced the default
lookback to 18 completed trades.

The buffered lookback sweep found a local `20-25` region with materially better
headline results than `10`, `15`, or `40`, but `15` was slightly negative and the
window is only about 41 days. The `20` config also remained positive at 2x fees.
Decision: **continue**, but stop parameter searching until explicit discovery ranges
are available through the connected MCP. None of these runs is promotion evidence.

### 2026-07-09 18:51 EDT

Expanded the smoke into a 49-asset UI batch after confirming the connected MCP still
lacks its checked-out batch tool. The run used 1h / 1,000 candles / `LOOKBACK=20`,
static sizing, 5% minimum adjustment, 10% default asset weight, and 10x-or-max
leverage. All 49 assets completed with complete candle loads.

Breadth was promising: 27/49 assets had positive return, 26/49 had Sharpe at least
1, median return was `+7.57%`, and median Sharpe was `1.30`. Risk was also high:
median max drawdown was `-21.18%`, and 15 assets drew down at least 30%. Strong
examples included ADA, TRX, PAXG, ZRO, ETH, and SOL; failures included TIA, LDO,
FARTCOIN, GRASS, AVAX, PENDLE, SUI, and INJ.

This batch consumes the previously quarantined ETH/SOL observations and invalidates
the original validation/holdout assignment. Any formal continuation needs a fresh
preregistered holdout. Absolute returns are not directly comparable to the earlier
1x run: BTC return and fees scaled almost exactly 10x, so leverage/asset-weight
semantics must be reconciled before treating the batch as edge evidence. The UI did
not expose a saved batch UUID, so the batch remains workflow characterization rather
than a registry-backed evidence run.

## 1. Research Card

- Strategy idea: classic symmetric N-bar price-channel breakout.
- Edge hypothesis: sustained directional moves persist after price escapes its recent range.
- Asset universe and timeframes:
  - discovery: BTC 1h;
  - validation: ETH 1h, quarantined until the BTC lookback family is frozen;
  - holdout: SOL 1h, consumed once at promotion.
- Entry logic:
  - long when close exceeds the highest high of the prior `LOOKBACK` bars;
  - short when close falls below the lowest low of the prior `LOOKBACK` bars.
- Exit logic: hold the current direction until the opposite channel breakout, then reverse.
- Risk and cost assumptions:
  - initial capital: `$100,000`;
  - max position: `50%`;
  - leverage: `1x`;
  - sizing mode: static;
  - fees: `0.00015`;
  - slippage: `0.05`.
- Intended temporal split:
  - discovery: 2026-04-01 through 2026-05-31;
  - validation: 2026-06-01 through 2026-06-30;
  - holdout: 2026-07-01 onward, consumed once.
- Period segmentation: calendar weeks, fixed before the first evidence run.
- Core knob: `LOOKBACK`.
- Incidental knobs: artifact detail and chart display.
- Expected risks: false breaks, fee drag from reversals, low trade count at long lookbacks, and dependence on one trend.
- Initial kill criteria:
  - fee-stressed net return at or below zero;
  - fewer than 20 completed discovery trades;
  - max drawdown worse than `-20%`;
  - no stable neighborhood across lookbacks `10`, `20`, and `40`;
  - more than `60%` of net return from one calendar week.

## 2. Optimization Objective

- Primary objective: maximize net Sharpe after fees and slippage.
- Net return and Sharpe use the cost-adjusted equity curve.
- Trade count means completed round trips.
- Fee drag is total fees as a percentage of initial capital.

Objective-change log:

- 2026-07-09 18:10 EDT: objective fixed before the first run.

## Run Registry

- `895aa38a-d93b-41ee-aa24-47eaf2411699`: `LOOKBACK=20`, no adjustment buffer; discarded for 894-fill fixed-notional rebalance churn.
- `9916f36b-607a-4c8c-a911-392103f12f12`: `LOOKBACK=20`, 5% adjustment buffer; return `8.02%`, Sharpe `3.13`, max drawdown `-4.99%`, 18 trades; [[research/trading/n-bar-breakout/review/lookback-20-smoke-review|artifact review]].
- `c84cebdc-52a7-4c10-aed7-abc18b732fbd`: `LOOKBACK=10`; return `2.57%`, Sharpe `1.08`, max drawdown `-7.91%`, 37 trades.
- `40d90b92-3cb5-42e2-a4e7-c6bd3bd16dd7`: `LOOKBACK=15`; return `-0.18%`, Sharpe `0.05`, max drawdown `-9.96%`, 25 trades.
- `0272d073-514e-44b5-9543-61090f905711`: `LOOKBACK=25`; return `7.18%`, Sharpe `2.82`, max drawdown `-5.03%`, 18 trades.
- `ba75e220-0c9b-4473-a60b-750c9c9244da`: `LOOKBACK=40`; return `2.38%`, Sharpe `1.03`, max drawdown `-7.73%`, 13 trades.
- `737697bb-d9c5-4a24-8b53-a46c8e79aa9e`: `LOOKBACK=20`, 2x fees; return `7.75%`, Sharpe `3.03`, max drawdown `-5.05%`, 18 trades.

- Cumulative configs evaluated: `7` (one discarded operational config, five lookbacks, one fee stress).
- Backend commit: `0f44d698` plus the current uncommitted strategy spike.

## 3. Baseline Plan

1. Refresh the connected Research MCP so explicit ranges and suite tools match the checked-out implementation.
2. Rerun BTC discovery with lookbacks `15`, `20`, and `25`.
3. Compare the response shape by predefined calendar weeks.
4. Do not inspect ETH or SOL before the BTC candidate family is frozen.

## 4. Current Friction

- A newly registered code strategy has no runnable UUID until a separate backtest-only `Strategy` row is created in the UI/database.
- Research MCP has no tool for creating that row.
- The connected MCP server is behind the checked-out Research MCP implementation: explicit ranges and suite tools are absent from its advertised schema.
- `avg_hold_bars` reports `0.0` for a strategy that is active for roughly 96% of scored bars; that metric is not usable for this review without a semantics check.
- Saved-run Data exposes aggregate metrics but no trade/fill ledger; fill review required hydrating a multi-megabyte MCP artifact.
- The UI batch completed 49 assets successfully, but the connected MCP had no batch tool and the UI did not expose a saved batch UUID for registry writeback.
