# Backtest Strategies Index

Light inventory of the backtest strategy implementations in `mm_v04`. One entry per registered strategy: registered name, class, source file, one-line purpose, and key params. This documents the code surface; live research status lives in the [[research/trading/research_index|Research Board]] and metrics live in the backtest UI / saved runs (not here).

Full paths below are relative to the `mm_v04` repo; inventory filenames are relative to `backend/app/backtest/strategies/`.

## How the registry works

- All strategies live under `backend/app/backtest/strategies/` and subclass `BacktestStrategy` from `backend/app/backtest/strategies/strategy_base_backtest.py`.
- Each concrete strategy self-registers with the `@register("name")` decorator, which inserts it into the module-level `_BACKTEST_REGISTRY` keyed by its registered name.
- `backend/app/backtest/strategies/__init__.py` explicitly imports strategy modules, including nested modules, so importing the package triggers registration. `PX/` groups PX strategies, `ema/` groups EMA-specific strategies, and `labs/` groups lab strategies. The base/registry, `example.py`, and remaining standalone strategies stay at the root. Each group has an `__init__.py`; new strategies still need an explicit import in the parent package.
- Folder paths are independent of registered names. The UI consumes registered names through `/strategies/registry?backtest=true`; source folders do not create UI groups. The 2026-10-06 reorganization preserved all 19 registered names and their defaults.
- `list_strategies()` and `get_strategy_class(name)` (in `strategy_base_backtest.py`) expose the registry to the UI / Research MCP.
- A strategy declares its typed contract via class vars: `Params` (a `StrategyParams` subclass), `Config` (a `StrategySignalConfig` subclass), and `TradeConfig` (a `StrategyTradeConfig` subclass). `from_params(...)` builds instances from plain dicts.

`strategy_base_backtest.py` (base + registry) and `__init__.py` (registration wiring) are framework files, not registered strategies.

## Strategy inventory

### External model reproductions

- **`memlabs_ar3`** — `MemlabsAR3Strategy` (`memlabs_ar3.py`): frozen MemLabs three-lag linear forecast on 12h close log returns; closes and reopens each bar through MM's mock executor. Params: three `weights`, `bias`, optional predeclared `terminal_close_ms`; static or net-compounding sizing. Source pinned to `memlabs-research/build-a-quant-trading-strategy@c767f20d4eb5c031649e86c1a718b7eee0eaf4dc`. Local originals, isolated environment, executed Part 2 and reconciliation notebook: `mm_v04/.research/memlabs/` (git-ignored; launcher `launch-notebooks.sh`). The reconciliation matches predictions/directions and linear-ledger fills; upstream signed-log short payoff and gross-before-fees compounding explain accounting differences. This is reproduction, not independently validated out-of-sample evidence. No persisted run IDs or DB strategy records were created.
- Fresh frozen-model check (2026-10-06): evaluated unchanged static sizing and per-bar round trips from 2025-10-10 00:00 UTC through 2026-10-06 00:00 UTC using checksum-verified Binance USD-M archives. All 18 overlapping OHLC bars match the original trade-derived data. The original net result did not carry forward: gross capture was near flat while repeated execution fees dominated; information versus policy attribution remains unresolved. Local artifacts, executed notebook, monthly breakdown and independent reconciliation live in `mm_v04/.research/memlabs/fresh-2026-10-06/`. Local execution UUID `490d3135-ca1f-49cb-a19f-a68fd789f21f` is **not** a persisted database run ID. No retraining or reduced-turnover variant was implemented; funding/slippage remain excluded. Public REST was region-blocked; the archive endpoint is one half-day behind the latest completed candle.
- Shared `Interval` accepts `12h` with duration maps, generated client, form parsing and backtest selector updated. Live aggregation targets and live selector options remain explicit unchanged subsets. No schema migration required.

### EMA-crossover family

- **`example`** - `ExampleStrategy` (`example.py`): configurable EMA backtest registered 2026-09-29. Supports fixed/zero/no thresholds, full/continuous/banded sizing, transition/every-bar adjustment, and optional volatility adjustment. Shared SIG_TO_POS_SIZE and VOL_ADJ_POS_SIZE now belong in trade_config; old backtest payloads are rejected rather than translated. Catalog defaults refreshed and five disposable saved configuration groups deleted, retaining historical run/study snapshots. UI exposes structured thresholds and volatility controls. The four legacy EMA implementations and registry names are retired; see the replacement guide below.

- **`emac_slope_v1`** - `EMACSlopeV1Strategy` (`ema/emac_slope_v1.py`): standalone BacktestStrategy that continuously sizes positions from the processed slope of the EMAC signal; owns its params/config, EMA setup, warmup and signal-stat emission. The EMAC event-study pipeline also owns its configuration types in study_types.py, retaining historical V4 run identity without importing the V4 implementation.
- **`emac_escalation`** - `EMACEscalationStrategy` (`ema/emac_escalation.py`): band-escalation cycle; sets a piecewise-linear target fraction as the signal magnitude moves across the mean / 1-sigma / 2-sigma bands. Params: `fast_window=10`, `slow_window=200`, `signal_stats_lookback=200`; Config band targets `0.75` / `0.25`.
- **`emac_escalation_v2`** - `EMACEscalationV2Strategy` (`ema/emac_escalation_v2.py`): mean-cycle variant of the escalation strategy (enter when magnitude is below the mean band, exit on cross). Params: `fast_window=10`, `slow_window=200`, `signal_stats_lookback=200`.

Related research: [[research/trading/emac-cross-10-200/emac-cross-10-200|EMA Cross 10/200]].

### Price-extension / slope family

- **`px`** - `PxStrategy` (`PX/px.py`): price-extension (PX) strategy; long when PX > 0, else flat (short if symmetric). Params: `LEN=10`, `LOOKBACK=100`, `SOURCE=CLOSE`, `SYMETRIC=True`.
- **`px_slope_sniper`** - `PxSlopeSniperStrategy` (`PX/px_slope_sniper.py`): combines PX extension with slope for entry timing. Params: `PX_LEN=10`, `SLOPE_LEN=10`, `PX_LOOKBACK=100`, `SLOPE_LOOKBACK=3`, `SOURCE=CLOSE`, `SYMETRIC=True`.
- **`slope`** - `SlopeStrategy` (`slope.py`): slope-of-EMA signal strategy. Params: `LOOKBACK=3`, `LEN=10`, `SOURCE_1=CLOSE`, `SYMETRIC=True`.

### Oscillator / volume family

- **`rsi`** - `RSIStrategy` (`rsi.py`): simple RSI strategy. Params: `lookback=14`.
- **`vfti`** - `VFTIStrategy` (`vfti.py`): volume-flow trend indicator (VFTI) strategy. Params: `lookback=14`.

### Breakout / discretionary-codified

- **`n_bar_breakout`** - `NBarBreakoutStrategy` (`n_bar_breakout.py`): N-bar channel breakout; enters on a channel break and holds until the opposite channel breaks. Params: `LOOKBACK=20`; TradeConfig `MIN_ADJUSTMENT_VALUE_PCT=0.05`. See [[research/trading/n-bar-breakout/n-bar-breakout|N-Bar Breakout research]].
- **`ema_hilo_200_reentry`** - `EmaHilo200ReentryStrategy` (`ema/ema_hilo_200_reentry.py`): HYPE 4H discretionary mapping; the 200 close EMA permits direction while the 10 high/low EMAs control close-based stop and re-entry. Params: `fast_window=10`, `slow_window=200`. See [[projects/ema_hilo_200_reentry/hype-ema-hilo-200-reentry-codification|HYPE EMA High/Low 200 Re-entry Codification]].
- **`ema_px_trend`** - `EmaPxTrendStrategy` (`ema/ema_px_trend.py`): EMA/PX trend-regime strategy codified from discretionary chart-led blind pattern matching (rules R1 regime side, R2 continuation, R3 chop gate, R4 extension exits, R5 long/short asymmetry). Params include `fast_window=10`, `slow_window=200`, `atr_window=14`, plus stress/capitulation/acceleration/extension/chop tuning. See [[research/trading/ema_px_trend/strategy_ema_px_trend|ema_px_trend Strategy Doc]].

## Maintenance

- When adding a strategy, add its `@register(...)` import to `__init__.py` and add a one-line entry here.
- Keep this page light: purpose + key params only. Do not paste backtest metric tables (re-fetch via Research MCP / backtest UI).

## Retired EMA strategies → Example (2026-09-29)

Status: confirmed — Destin authorized this consolidation. The four files `backend/app/backtest/strategies/{emac,emac_cross,emac_v4,emac_v5}.py` and their registry exports were removed. Their catalog rows were soft-deleted through the existing API, retaining IDs/FKs for historical results. New executions use `example` (catalog UUID `429d3307-791e-4c3a-b386-7aa3a9cc0be4`); no old-name aliases or automatic payload translation exist. Saved results keep their original names and snapshots; reading them does not require the old implementation. Historical references in research write logs remain provenance, not instructions to select retired names.

### Explicit replacement settings

These are the tested mappings, not a guarantee that every historical custom variation is equivalent. Copy the original run's EMA windows, source, signal processing, position limits, costs, data source and date window explicitly. Example's defaults are not historical research defaults (notably fixed thresholds default to long entry 0.1 / exit 0.9, not ±0.01).

| Historical name | Example THRESHOLDS | SIZING | ADJUSTMENT | VOLATILITY |
|---|---|---|---|---|
| emac | null | continuous | every_bar | fast_span 35, slow_span 200 |
| emac_cross | "zero_cross" | full | transitions | null |
| emac_v4 | fixed levels/cross directions from original run | full | transitions | null |
| emac_v5 | fixed levels/cross directions from original run | continuous | every_bar | fast_span 35, slow_span 200 |

The tested V4/V5 fixed config is long_entry=long_exit=0.01, short_entry=short_exit=-0.01; long-entry/short-exit cross_over, long-exit/short-entry cross_under. All those settings live in `trade_config.THRESHOLDS`. `SIG_TO_POS_SIZE` and `VOL_ADJ_POS_SIZE` also live in trade_config (tested direct/inverse respectively), not signal config. StrategyParams remains intentionally empty at the shared level; Example owns fast_window, slow_window and SOURCE. Do not copy legacy SYMETRIC or signal_stats_lookback into Example. Example supports signed two-sided sizing; legacy one-sided/custom signal-stat display variants are not covered by this comparison. Research statistics remain available in their study pipeline rather than being added back to Example.

Exact paired payloads are preserved as historical evidence in `backend/tests/backtest/fixtures/example_ema_comparisons.json`; only each `example` payload is executable now. Existing sizing, zero-cross, threshold, state-memory, inverse-saturation and rolling-window regression coverage lives in `test_example.py`, `test_example_registry.py`, `test_mon99_emac_signal_semantics.py` and the shared sizing tests. Old implementation-only tests were removed.

### Verification and interpretation limits

Aligned longest-input warmup was applied before comparison. Cross/V4/V5 matched fills and metrics exactly on the paired LINKUSDT daily window. Continuous emac's small V1/V2 position-rounding difference was explicitly accepted by Destin; do not describe it as bitwise parity. Cleanup run `56008fed-9630-491f-be00-4a765582b7c1` exactly matched pre-cleanup Example `3c12b85f-a1cb-442f-b0bf-80fea58cdbe1`. Four legacy comparison runs remain readable after catalog retirement: emac `6ace7d7f-e361-4292-b419-cf44b6f1188a`, cross `53fd2597-6716-4b5c-bd64-43c797abdbbd`, V4 `bd1a5d44-b7a1-41db-9814-f0633a819a53`, V5 `60295611-2b6d-4a41-9c3c-18f7005a13d5`.

This is implementation consolidation, not new trading evidence or a promotion of previously quarantined research. Older runs with different warmup windows may not reproduce exactly. Rebuild explicit Example configurations for new research rather than replaying obsolete saved JSON unchanged. Smoothing implementation remains deferred.

### Research dependency handling

`emac_slope_v1` owns its setup and inherits only BacktestStrategy. `event_study/study_types.py` owns EMACStudyParams/EMACStudyConfig; fixture loading, series calculation and the runner no longer import V4. The existing event-study CLI intentionally still requires a historical saved `emac_v4` run as its input identity; do not pass a new Example run to it without separately adapting that contract. Its full-series calculation, historical warmup and documented log-slope behavior were preserved, not made equivalent to Example's rolling execution. Existing saved V4 anchors remain usable.

Other EMA, PX, slope, escalation and specialized strategies are not retired by this change.
