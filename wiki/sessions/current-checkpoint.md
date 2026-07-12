# Current Checkpoint

Date: 2026-07-11 03:28 EDT

Company frame: [[company/money-machine-360|Money Machine Operating Context]].

## Active Revenue Proof

- **Objective:** positive net realized live P&L after costs over a founder-set proof period.
- **Proof period:** not yet set; Destin sets it before live evaluation begins.
- **Strategy / experiment:** passive EMA 10/200 cross timeframe scan on BTC followed by a `$250,000` rolling-24h-volume-filtered `4h` universe screen. Bullish cross targets maximum long, bearish cross targets maximum short, and the position is held between crosses. See [[research/trading/emac-cross-10-200/emac-cross-10-200|EMA Cross 10/200 Research]].
- **Observed blocker:** long-window compact autosave is not reliable. Two approximately 57,192-candle BTCUSDT 1h runs computed successfully, but each full-artifact background save exceeded the 10-second persistence timeout, rolled back, and returned 404 on saved-run retrieval. Tracked as Linear `MON-140`.
- **Next action:** confirm the long-history Top 10 and whether POL/PAXG should receive separate lower-timeframe validation; do not merge shorter-history Sharpe estimates into the 5,000-candle ranking.
- **WIP:** one primary revenue outcome unless Destin explicitly expands it.

## Current Engineering State

- `MON-122` and `MON-134` are done.
- `MON-132` is blocked behind the backtest-persistence redesign.
- `MON-140` records the reproduced legacy compact-autosave timeout and silent-404 failure mode; the current no-build workaround is smaller windows, higher timeframes, or `auto_save=false` when durable artifacts are unnecessary.
- `MON-141` is a high-priority Triage ticket for a saved-run report exporter and cached Binance candle-availability preflight. Historical liquidity filtering and multiple-comparison policy are explicitly deferred.
- `MON-135`–`MON-139`, grid expansion, artifact automation, and generalized orchestration are parked until separately justified by evidence from the revenue loop.
- The accepted persistence foundation uses Study → Variant → Trial → Attempt. Batch is an API/enqueue convenience, not a persistence entity.
- Binance spot research candles should use `data-api.binance.vision`; perps require non-restricted egress. See [[vendors/binance-market-data-access|Binance Market Data Access]].
- Destin selected Binance USD-M perpetual history for discovery and recent Hyperliquid candles for venue validation. Local Japan VPN access is verified: Binance futures ping, BTCUSDT 1h klines, and exchange metadata all returned HTTP 200. Idle Japan AWS infrastructure is fallback only.
- The bounded MON-113 implementation is complete: provider-qualified backtest candles and provenance, retry-safe DB-first Binance loading, structured provider failures, research-MCP fields, frontend source/date controls, and `emac_cross`.
- The path now derives direct Binance symbols from selected Hyperliquid assets, accepts exposed timeframes, has no preselected date range, and enforces a 100,000-candle hard cap in both API validation and UI gating. Local migrations are applied through `f8a9b0c1d2e3`.
- Research MCP shared-config batches now accept Binance USD-M, derive each child asset's source symbol independently, preserve partial failures, and accept up to 32 requested assets while backend concurrency remains capped at eight.

## Current Decision

Do not continue platform expansion merely because the dependency chain exists. The first attempted strategy selection exposed a concrete historical-data blocker. Build only the bounded backtest-candle/provider-loader and passive-cross strategy path in the accepted MON-113 plan; keep the broader Agentic Research Loop parked.

## Verification

- `MON-134` accepted and committed as `5a659548`.
- Foundation verification and detailed ticket history are recorded in `wiki/sessions/session-change-log.md` and the issue-linked briefs.
- Historical-data and strategy semantics were narrowed from grid/platform work to the accepted [[engineering/MON-113-binance-backtest-candles-plan|MON-113 plan]].
- The BTCUSDT 1h network-backed UI path successfully exercised the real gap-fetch/cache/backtest flow over approximately six years.
- Two full-range BTCUSDT 1h Research MCP runs reproduced the autosave failure with approximately 285,000 artifact rows each; both run IDs were absent from saved-run retrieval after rollback.
- Across the six reviewable BTC intervals, active positions were in profit for `77.84%`–`88.21%` of active bars despite only `10.22%`–`28.07%` realized win rates. This shifts the diagnosis from simply weak direction to poor profit retention under the hold-until-opposite-cross rule. Worst position ROE is now evaluated alongside portfolio drawdown.
- Generalization verification passed: all 229 backend backtest tests, five research-MCP tests, focused Ruff/compile checks, frontend lint/build, generated client, browser verification of ETH → ETHUSDT and 4h selection, and Alembic head at `f8a9b0c1d2e3`.
- Binance batch verification passed after correcting saved identity hydration to prefer persisted child candle provenance over mutable current asset metadata: 53 focused backend tests, 13 focused MCP tests, 232 non-destructive backend backtest tests, 70 deterministic MCP tests, focused Ruff/mypy/compile checks, frontend lint/build, generated client, and Alembic head. The legacy migration round-trip was excluded because populated `1d` candles cannot be represented by its `SMALLINT` downgrade; the unrelated password-login test still attempts a fake-host network call.
- The first Binance `4h` asset batch (`3c0f2043-aeac-44da-945f-523965b33c97`) completed 19/20 assets over a common 5,000-candle window. ETH, SUI, ARB, and DOGE cleared Sharpe `1.0`; median Sharpe was `0.438`, median drawdown `-64.38%`, median profit factor `0.951`, median time in money `87.84%`, and median trade win rate `23.73%`. MATIC failed cleanly on missing post-delisting candles.
- A point-in-time Hyperliquid `dayNtlVlm >= $250,000` filter expanded the known universe through Research MCP runs `8c3d5e49`, `c98d9c89`, and `28a4f773`. Across the liquidity-eligible set, 52 assets had complete comparable history and 29 lacked the full 5,000-candle Binance window. ZEC and HBAR posted Sharpe above `1.3` but failed risk review on drawdown, Worst Position ROE, and/or cost drag; no cleaner leader than ETH emerged.
- Tiered-history recovery completed: `20/29` assets ran over a common trailing 2,500-candle window and `7/9` remaining assets ran over 1,000 candles. POL (`1.231` Sharpe, `-40.08%` drawdown, 18 trades) and PAXG (`0.888`, `-26.04%`, 24 trades) led the 2,500 cohort. HYPE, MET, and MON were positive over 1,000 candles but had only 4–8 trades. APEX is unsupported on Binance USD-M; MEGA is 31 candles short of 1,000.

## Next Action

The tiered liquid-universe `4h` screen is complete for assets reachable in the first 200 Research MCP records. The 5,000-candle preliminary Top 10 remains SUI, ETH, ARB, DOGE, kBONK, kPEPE, XLM, WLD, BTC, and SEI. POL and PAXG are separate shorter-history candidates; HYPE, MET, and MON need more observations before promotion. Confirm K and cohort treatment before running lower intervals; any live launch or capital mutation requires separate explicit authorization.
