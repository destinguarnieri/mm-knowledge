# Session Change Log

Historical record, not an active agenda. The 2026-10-06 research reset remains in force. This compact digest routes to durable evidence; [the full pre-compaction log](../../archive/history-compaction-2026-11-23/session-change-log.md) preserves every original entry, run ID, and verification caveat.

## 2026-11-24 — Sizing verified through MCP and committed

Six BTC daily saved backtests completed; all 4,386 candle decisions reconciled within execution tolerances, and Carver's 1%/100% allocation pair matched exactly. Committed code as `06a380bf`; no push. Run IDs and scope: [[engineering/bounded-ema-history#MCP sizing verification and commit — 2026-11-24]].

## 2026-11-24 — One sizing function, including Carver

At Destin's request, moved multi_speed_ewmac to calculate_sizing and removed the old helper and compatibility DTOs. The separate allocation cap was his crypto-leverage adaptation and is now removed. 360 offline tests and two synthetic engine replays pass; scoped typing/lint passes. Local/uncommitted. Details: [[engineering/bounded-ema-history#Single sizing function, including Carver — 2026-11-24]].

## 2026-11-24 — Maximum-based position sizing

Implemented the approved eight-caller sizing change: volatility maximum is twice the risk base, signals map onto the maximum, and clipping no longer removes the cap. Shared/engine checks: 369 passed; scoped typing/lint and frontend build passed. Local/uncommitted. Saved-config behavior and scope: [[engineering/bounded-ema-history#Maximum-based position sizing — 2026-11-24]].

## 2026-11-24 — Direction-only EMA execution

Opposite Bid Trend can use the processed sign of Example’s close EMA 10/200. Committed the selector as `7258a969`. All 2,308 saved scores on the BTC daily volatility-targeted reference matched in local replay. Recorded Destin’s internal urgency sketch and the open target and fraction choices. See [[research/trading/opposite_bid_trend/opposite-bid-trend]].

## 2026-11-24 — Opposite Bid Trend blend and saved ADX references

Destin prioritized the combined signal and dropped the solo-feature trial sequence. Recorded three hourly ADX runs using weekly sizing snapshots, the sizing cadence guidance, and both routes under consideration. See [[research/trading/opposite_bid_trend/opposite-bid-trend]].

## 2026-11-24 — Individual Opposite Bid Trend features

Added a single-feature selector for ADX, VFTI, RVWAP slope, centered RSI, and price extension. Combo v1 and Opposite Bid Trend share the component calculations. Verified the selector through synthetic engine replay and recorded two saved hourly short references. See [[research/trading/opposite_bid_trend/opposite-bid-trend]].

## 2026-11-24 — Opposite Bid Trend research focus

Destin selected trend signal, inventory fractions, and position sizing as the active research focus. Saved HYPE ADX run `d7cfc05b-32d8-44d8-93b4-08a7ac9e0723` anchors the comparison. The static example remains an execution control. See [[research/trading/opposite_bid_trend/opposite-bid-trend]].

## 2026-11-23 — Optional forecast volatility normalization

Added shared opt-in signal config with SIG_VOL_NORMALIZE and retained SIGNAL_VOL settings. EWMAC defaults on; off uses raw spreads and skips signal-volatility state/warmup. 127 focused backend checks and unchanged enabled-mode outputs across 24 synthetic engine runs pass. See [[engineering/bounded-ema-history]].

## 2026-11-23 — Multi EWMAC component ownership

Extracted bounded forecast calculation and typed snapshots, grouped per-stream state, and separated feature formatting/mock execution. Sizing/target-position functions remain unchanged. 122 focused checks and exact parity across 24 synthetic engine runs pass; schemas and signal version unchanged. Follow-up: moved MultiEwmacStream into the strategy file at Destin's request; removed the separate state module with no class-body changes. See [[engineering/bounded-ema-history]].

## 2026-11-23 — Per-speed Example forecasts

Destin selected Example processing per EWMAC speed. multi_ewmac signal version 4 now normalizes each spread by contemporaneous price-unit volatility, processes each bounded history independently, and averages processed forecasts. Fixed stale warmup configuration and trade-config registration. 114 focused tests, 12 independent synthetic replay scenarios, scoped typing/lint pass; no historical run. Supersedes the combined-spread processing below. See [[engineering/bounded-ema-history]].

## 2026-11-23 — Multi EWMAC signal normalization

Multi EWMAC signal version 3 seeds normalized spreads from warmup and retains the configured scaling lookback. Synthetic replay matched a per-bar reference at lookbacks of 32, 252 and 500. See [[engineering/bounded-ema-history]] for state and retention.

## 2026-11-23 — Multi-EWMAC strategy split

Carver’s backtest retains the registry key `multi_speed_ewmac` in `ema/multi_ewmac_example.py`. The Example-style `multi_ewmac` strategy accepts custom fast/slow pairs and uses a shared feature that returns the equally weighted raw EMA spread. The strategy optionally normalizes that spread by centered EWMA price volatility before signal processing. Its signal processing and sizing follow Example. The shared indicator and registry checks passed offline.

## 2026-11-23 — Example streaming volatility

Example now streams RMS and Centered independently for sizing and adjustment. See [[engineering/bounded-ema-history]] for retention and verification.

## 2026-11-23 — Knowledge maintenance

Simplified both agent entrypoints and [[index|the index]], made navigation optional, and added [[goals|Goals]] for selected outcomes. Compacted [[sessions/current-checkpoint|checkpoint state]] and this log; retained full history and recovered deleted reference pages in the [archive](../../archive/history-compaction-2026-11-23/README.md). Repaired links and distinguished missing historical sources from current references. No project priorities were inferred or cancelled. Documentation and local link-checking changes only.

## 2026-11-23 — Snapshot tool and strategy packaging

Fractional-distribution work committed as `da3b5e28`; snapshot MCP as `6943c2ce`. Strategy verification: 156 focused tests; MCP: 167 offline tests plus a native-image response through the refreshed connection. Saved run `d7cfc05b-32d8-44d8-93b4-08a7ac9e0723` supplied the snapshot evidence; no new research run. See [[research/trading/opposite_bid_trend/opposite-bid-trend]] and [[ops/research-mcp-runbook]].

## 2026-11-18–20 — Scoring windows and Opposite Bid Trend

Explicit dates and Latest N now select scoring candles with preceding warmup; completed-candle cutoff and saved artifacts verified through cache-backed runs. Fresh-fetch half-open filtering subsequently repaired an inclusive provider boundary; existing cached unfinished candles remain separate. Commits and run IDs: [[engineering/backtest-date-windows]].

Candle Inventory became Opposite Bid Trend. Both variants received decision-target routing repairs and zero-signal flattening; ADX added fractional distribution. Fixed BPS cost floor, cap enforcement, and neutral/doji policy evolved through explicit decisions. Final recorded behavior and verification limits: [[research/trading/opposite_bid_trend/opposite-bid-trend]]. Earlier formulas and superseded routing remain only in historical evidence.

## 2026-11-12–17 — Sizing, indicator imports, and input handling

Elapsed unit snapshots implemented and accepted after independent reconstruction of saved-run decisions; subsequent caller cleanup recorded separately. [Sizing note and run IDs](../../raw/research/concepts/sizing.md).

Indicator modules grouped by family; padded helpers, ADX, DPO, range/body/log-return features, and bounded-state contracts documented in [[engineering/bounded-ema-history]]. RSI/slope padding and uniform scaler input cleanup committed; transform-units/policy work deferred. [[projects/nan-handling-positioning-audit]].

## 2026-10-30–11-11 — Terminal, lifecycle planning, and testing

Terminal progressed to existing-path order submission/cancellation, stops, scale arrays, Close, and USD conversion. Percentage/MAX removed; metadata discovery unresolved. [[projects/trading-terminal-ui]].

Live startup/recovery separation remained a plan, with dedicated strategy accounts, explicit stop-and-flatten, and per-chunk review requirements; no lifecycle implementation was authorized by those notes. See the dated summary in [[sessions/current-checkpoint]] and the [archived lifecycle checkpoint](../../archive/history-compaction-2026-11-23/current-checkpoint.md#current-focus).

Backend test isolation accepted and merged locally; full-suite baseline failures retained in [[ops/backend-testing]]. Account-equity series and local migration verification: [[engineering/backtest-risk-measurement]].

## 2026-10-06–29 — Reset, engine exploration, and bounded state

Destin reset the research agenda on October 6. Engine V2 designs and implementation attempts followed; the core rewrite was removed on October 18. Historical plans do not activate replacement work. [[projects/backtest-engine-v2-plan]]. Bounded EMA retention, initialization, and sizing/volatility work: [[engineering/bounded-ema-history]].

## Before 2026-10-06 — Historical research and implementation

Older research, strategy retirement, Position Lab, risk-contract, and data-loader decisions remain in the [full log](../../archive/history-compaction-2026-11-23/session-change-log.md) and linked domain pages. The [October reset archive](../../archive/research-reset-2026-10-06/README.md) preserves the former agenda. Neither archive is an active backlog.

## Maintenance

Add one concise entry per material outcome, linking to evidence instead of copying progress reports. Keep this file under roughly 100 lines; archive older detail with a routing summary when needed. Preserve historical run IDs and limitations in the archive or domain page.
