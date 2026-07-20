# Current Checkpoint

Date: 2026-07-18 00:52 EDT

Company frame: [[company/money-machine-360|Money Machine Operating Context]].

## Active Revenue Proof

- **Objective:** positive net realized live P&L after costs over a founder-set proof period.
- **Proof period:** not yet set; Destin sets it before live evaluation begins.
- **Company phase:** discretionary alpha transfer. Select strategies Destin actually trades, codify their visual and control semantics, prove behavioral parity, and only then validate current economics. Novel discovery is secondary until that inventory is exhausted or Destin explicitly requests it.
- **Strategy / experiment:** EMA 10/200 discretionary-control transfer remains relevant, but Destin clarified that static/dynamic thresholds are mostly generic research knobs. The active discretionary-alpha transfer has pivoted to the chart-led EMA/PX trend-continuation mapping in [[projects/ema_px_trend/codification|EMA/PX Trend Continuation Codification]]. Short-side semantics and a first long-side fixture are partially elicited, but the long fixture exposed a rule-consistency issue that must not be promoted to accepted semantics yet.
- **Observed blocker:** no current Threshold Engine V3 implementation blocker. The remaining blocker is behavioral specification: entry permission, continuous scale-out curves, PX anchor choice (`10 EMA low` versus `200 EMA`), ATR cooldown, PRI/CSI event definitions, rolling-low representation, side-asymmetry/consistency audit, and failure-case fixtures need more chart evidence before implementation. Discretionary "knowing when to break the rules" must become a separate named mapping, an explicit exception predicate, or be excluded from deterministic code.
- **Next action:** continue chart-led codification for the EMA/PX trend-continuation strategy on the DOGE/BTC fixture before changing assets, so failure cases and volatile wrong-way regimes are not avoided. Focus next examples on entries and failures: audit whether early long `123` before the `10/200` cross is a separate entry strategy, valid explicit exception, missing shared permission rule, or labeling inconsistency; clarify PX anchor choice; decide whether long-duration trend capture belongs in this mapping or a separate strategy; then continuous PX scale-out, ATR cooldown, and failed `200 EMA` retest / slam short. After DOGE/BTC failure labels, ask Destin for a fresh unlabeled asset with the same colored EMA indicators for blind rule derivation, ideally by an unprimed/fresh agent not bounded by the current rule set. Do not reopen broad universe/timeframe expansion. Live/capital mutation still needs explicit authorization.
- **WIP:** one primary revenue outcome unless Destin explicitly expands it.

## Current Engineering State

- `MON-122` and `MON-134` are done.
- `MON-132` is blocked behind the backtest-persistence redesign.
- The backtest retention-contract rollout is implemented locally: one request field (`retention_mode=summary|full`), one persisted artifact outcome (`not_requested|writing|available|failed`), durable summaries for both modes, explicit outcome-aware artifact reads, and queryable queue/timeout/cancellation failure states. Legacy request branches, response aliases, writes, and database columns have been removed; unknown request fields are rejected.
- `MON-147` is implemented and verified in the running UI. Successful single `full` runs again return the complete chart payload already computed by the engine while asynchronous persistence remains unchanged; the frontend selects the returned `(run_id, asset_id)`, shows one selected result, and preserves the live chart while artifacts are `writing`. Summary and batch response contracts are unchanged.
- `MON-140` is canceled as superseded by the metrics-only summary retention contract. Long-window `full` retention remains unproven and is deferred until an audit workflow demonstrates that it is a revenue blocker.
- `MON-143` is the independent high-priority cached Binance candle-availability preflight for assigning assets to 5,000/2,500/1,000/<1,000 cohorts before execution.
- `MON-146` is implemented and verified locally. EMAC V4 consumes the causal `process_signal()` series directly, so its threshold engine receives the final two immutable processed values without strategy-local cache lifecycle. Threshold Engine V3 rejects zero levels, and transition-only execution prevents hold-period resizing. Smooth current-value strategies continue to use `process_signal_last()`.
- The shared signed-magnitude min-max scaler now has explicit causal series and current-scalar contracts: each series index equals the value emitted from that input prefix, while the latest-value formula remains unchanged. The series path uses SciPy's compiled O(n) one-dimensional min/max filters with sentinel-based non-finite handling. This repairs historical-array semantics without changing V4's emitted-history boundary.
- `MON-141` is canceled: the EMA-session “manual transcription” was agent documentation habit, not a missing report-export product. Research continuity prompting now treats persisted `run_id` + Destin's UI as the metric source; wiki/checkpoint/changelog keep interpretation, and canvas is optional only for unique visuals beyond the UI.
- `MON-85` follows `MON-143` to type and document the complete resulting registered Research MCP surface without changing runtime payloads.
- `MON-135`–`MON-139`, grid expansion, artifact automation, and generalized orchestration are parked until separately justified by evidence from the revenue loop.
- The accepted persistence foundation uses Study → Variant → Trial → Attempt. Batch is an API/enqueue convenience, not a persistence entity.
- The V2 `BtStudy.retention_mode` contract remains independently `metrics|full`; the new `summary|full` vocabulary applies to `BtBacktestRun` requests and was deliberately not propagated into V2.
- Binance spot research candles should use `data-api.binance.vision`; perps require non-restricted egress. See [[vendors/binance-market-data-access|Binance Market Data Access]].
- Destin selected Binance USD-M perpetual history for discovery and recent Hyperliquid candles for venue validation. Local Japan VPN access is verified: Binance futures ping, BTCUSDT 1h klines, and exchange metadata all returned HTTP 200. Idle Japan AWS infrastructure is fallback only.
- The bounded MON-113 implementation is complete: provider-qualified backtest candles and provenance, retry-safe DB-first Binance loading, structured provider failures, research-MCP fields, frontend source/date controls, and `emac_cross`.
- The path now derives direct Binance symbols from selected Hyperliquid assets, accepts exposed timeframes, has no preselected date range, and enforces a 100,000-candle hard cap in both API validation and UI gating. Local migrations are applied through `f8a9b0c1d2e3`.
- Research MCP shared-config batches now accept Binance USD-M, derive each child asset's source symbol independently, preserve partial failures, and accept up to 32 requested assets while backend concurrency remains capped at eight.
- The additive retention migration `b7c8d9e0f1a2` is applied to the local database at Alembic head. Its own downgrade/upgrade executed during the migration round-trip test; the broader historical downgrade remains blocked by populated daily candles that cannot fit the older `SMALLINT` schema.

## Current Decision

Do not continue platform expansion merely because the dependency chain exists. Use the current system to transfer one discretionary strategy at a time: semantic extraction, faithful codification, behavioral parity, then current economic validation. Keep open-ended discovery and the broader Agentic Research Loop parked unless Destin explicitly requests them or codification exposes a causal blocker.

## Verification

- `MON-134` accepted and committed as `5a659548`.
- Foundation verification and detailed ticket history are recorded in `wiki/sessions/session-change-log.md` and the issue-linked briefs.
- Historical-data and strategy semantics were narrowed from grid/platform work to the accepted [[engineering/MON-113-binance-backtest-candles-plan|MON-113 plan]].
- The BTCUSDT 1h network-backed UI path successfully exercised the real gap-fetch/cache/backtest flow over approximately six years.
- Two full-range BTCUSDT 1h Research MCP runs reproduced the autosave failure with approximately 285,000 artifact rows each; both run IDs were absent from saved-run retrieval after rollback.
- Across the six reviewable BTC intervals, active positions were in profit for `77.84%`–`88.21%` of active bars despite only `10.22%`–`28.07%` realized win rates. This shifts the diagnosis from simply weak direction to poor profit retention under the hold-until-opposite-cross rule. Worst position ROE is now evaluated alongside portfolio drawdown.
- Generalization verification passed: all 229 backend backtest tests, five research-MCP tests, focused Ruff/compile checks, frontend lint/build, generated client, browser verification of ETH → ETHUSDT and 4h selection, and Alembic head at `f8a9b0c1d2e3`.
- Binance batch verification passed after correcting saved identity hydration to prefer persisted child candle provenance over mutable current asset metadata: 53 focused backend tests, 13 focused MCP tests, 232 non-destructive backend backtest tests, 70 deterministic MCP tests, focused Ruff/mypy/compile checks, frontend lint/build, generated client, and Alembic head. The legacy migration round-trip was excluded because populated `1d` candles cannot be represented by its `SMALLINT` downgrade; the unrelated password-login test still attempts a fake-host network call.
- Legacy-free retention verification passed across 243 backend backtest tests and 82/83 Research MCP tests, focused Ruff and core mypy checks, frontend lint/build, Python compilation, regenerated OpenAPI client, whitespace checks, offline migration SQL rendering, direct schema inspection, and Alembic head `c8d9e0f1a2b3`. The skipped/failing tests are documented pre-existing blockers: the broad migration test reaches the old daily-candle `SMALLINT` downgrade, and the password-login negative test calls a fake host before rejecting missing credentials. No network-backed backtest, live runtime mutation, trading, deployment, commit, or push occurred.
- The first Binance `4h` asset batch (`3c0f2043-aeac-44da-945f-523965b33c97`) completed 19/20 assets over a common 5,000-candle window. ETH, SUI, ARB, and DOGE cleared Sharpe `1.0`; median Sharpe was `0.438`, median drawdown `-64.38%`, median profit factor `0.951`, median time in money `87.84%`, and median trade win rate `23.73%`. MATIC failed cleanly on missing post-delisting candles.
- A point-in-time Hyperliquid `dayNtlVlm >= $250,000` filter expanded the known universe through Research MCP runs `8c3d5e49`, `c98d9c89`, and `28a4f773`. Across the liquidity-eligible set, 52 assets had complete comparable history and 29 lacked the full 5,000-candle Binance window. ZEC and HBAR posted Sharpe above `1.3` but failed risk review on drawdown, Worst Position ROE, and/or cost drag; no cleaner leader than ETH emerged.
- Tiered-history recovery completed: `20/29` assets ran over a common trailing 2,500-candle window and `7/9` remaining assets ran over 1,000 candles. POL (`1.231` Sharpe, `-40.08%` drawdown, 18 trades) and PAXG (`0.888`, `-26.04%`, 24 trades) led the 2,500 cohort. HYPE, MET, and MON were positive over 1,000 candles but had only 4–8 trades. APEX is unsupported on Binance USD-M; MEGA is 31 candles short of 1,000.
- `MON-146` verification passed: 31 focused strategy/threshold tests, focused mypy, Ruff, formatting, and IDE diagnostics. Full-artifact Research MCP run `bad11f56-d676-4577-92a0-4527b3577f92` confirmed the March 14 crossing flips short to long immediately and completed with 18 trades.
- Causal min-max and unified processing verification passed across 37 focused scaler/processing/V2/V4 tests plus focused mypy, Ruff, formatting, compilation, and IDE diagnostics. Stateless V4 summary run `e43db176-6384-460d-a663-61e2e9f87807` exactly matched the canonical V4 run's metrics, including 18 trades.

## Next Action

Continue the bounded EMA V4 control experiment across three axes: static-threshold controls, causal dynamic thresholds derived from signal statistics, and explicit continuous position semantics using `sig_to_position` or an equivalent mapping. Live/capital mutation still needs explicit authorization.

Researcher reminder: Destin reports [[trading/dump|Trading Knowledge Dump]] is about `70%` complete as of 2026-07-18. Treat it as useful provisional source material, not a finished spec, and keep asking at the start of research sessions until he confirms it is complete.
