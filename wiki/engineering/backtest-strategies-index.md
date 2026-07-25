# Backtest Strategies Index

Light inventory of the backtest strategy implementations in `mm_v04`. One entry per registered strategy: registered name, class, source file, one-line purpose, and key params. This documents the code surface; live research status lives in the [[research/trading/research_index|Research Board]] and metrics live in the backtest UI / saved runs (not here).

Paths below are relative to the `mm_v04` repo.

## How the registry works

- All strategies live under `backend/app/backtest/strategies/` and subclass `BacktestStrategy` from `backend/app/backtest/strategies/strategy_base_backtest.py`.
- Each concrete strategy self-registers with the `@register("name")` decorator, which inserts it into the module-level `_BACKTEST_REGISTRY` keyed by its registered name.
- `backend/app/backtest/strategies/__init__.py` imports every strategy module so importing the package triggers registration.
- `list_strategies()` and `get_strategy_class(name)` (in `strategy_base_backtest.py`) expose the registry to the UI / Research MCP.
- A strategy declares its typed contract via class vars: `Params` (a `StrategyParams` subclass), `Config` (a `StrategySignalConfig` subclass), and `TradeConfig` (a `StrategyTradeConfig` subclass). `from_params(...)` builds instances from plain dicts.

`strategy_base_backtest.py` (base + registry) and `__init__.py` (registration wiring) are framework files, not registered strategies.

## Strategy inventory

### EMA-crossover family

- **`emac`** - `EmaCrossStrategy` (`emac.py`): simple EMA crossover; long when the fast EMA is above the slow EMA (short if symmetric). Params: `fast_window=20`, `slow_window=60`, `SOURCE=CLOSE`, `SYMETRIC=True`.
- **`emac_cross`** - `EMACCrossStrategy` (`emac_cross.py`): passive two-state EMA cross; flips the target direction (+1/-1) on each cross of the EMA spread through zero. Params: `fast_window=20`, `slow_window=60`.
- **`emac_v4`** - `EMACV4Strategy` (`emac_v4.py`): trend strategy using signal-stats normalization of the EMAC signal plus the V3 threshold engine, with explicit long/short entry/exit cross thresholds. Params: `fast_window=10`, `slow_window=200`, `signal_stats_lookback=200`; Config carries the entry/exit thresholds and `signal_stats_mode`.
- **`emac_v5`** - `EMACV5Strategy` (`emac_v5.py`): subclass of V4 that continuously sizes positions from the processed EMAC signal rather than a two-state flip.
- **`emac_slope_v1`** - `EMACSlopeV1Strategy` (`emac_slope_v1.py`): subclass of V4 that continuously sizes positions from the processed slope of the EMAC signal.
- **`emac_escalation`** - `EMACEscalationStrategy` (`emac_escalation.py`): band-escalation cycle; sets a piecewise-linear target fraction as the signal magnitude moves across the mean / 1-sigma / 2-sigma bands. Params: `fast_window=10`, `slow_window=200`, `signal_stats_lookback=200`; Config band targets `0.75` / `0.25`.
- **`emac_escalation_v2`** - `EMACEscalationV2Strategy` (`emac_escalation_v2.py`): mean-cycle variant of the escalation strategy (enter when magnitude is below the mean band, exit on cross). Params: `fast_window=10`, `slow_window=200`, `signal_stats_lookback=200`.

Related research: [[research/trading/emac-cross-10-200/emac-cross-10-200|EMA Cross 10/200]].

### Price-extension / slope family

- **`px`** - `PxStrategy` (`px.py`): price-extension (PX) strategy; long when PX > 0, else flat (short if symmetric). Params: `LEN=10`, `LOOKBACK=100`, `SOURCE=CLOSE`, `SYMETRIC=True`.
- **`px_slope_sniper`** - `PxSlopeSniperStrategy` (`px_slope_sniper.py`): combines PX extension with slope for entry timing. Params: `PX_LEN=10`, `SLOPE_LEN=10`, `PX_LOOKBACK=100`, `SLOPE_LOOKBACK=3`, `SOURCE=CLOSE`, `SYMETRIC=True`.
- **`slope`** - `SlopeStrategy` (`slope.py`): slope-of-EMA signal strategy. Params: `LOOKBACK=3`, `LEN=10`, `SOURCE_1=CLOSE`, `SYMETRIC=True`.

### Oscillator / volume family

- **`rsi`** - `RSIStrategy` (`rsi.py`): simple RSI strategy. Params: `lookback=14`.
- **`vfti`** - `VFTIStrategy` (`vfti.py`): volume-flow trend indicator (VFTI) strategy. Params: `lookback=14`.

### Breakout / discretionary-codified

- **`n_bar_breakout`** - `NBarBreakoutStrategy` (`n_bar_breakout.py`): N-bar channel breakout; enters on a channel break and holds until the opposite channel breaks. Params: `LOOKBACK=20`; TradeConfig `MIN_ADJUSTMENT_VALUE_PCT=0.05`. See [[research/trading/n-bar-breakout/n-bar-breakout|N-Bar Breakout research]].
- **`ema_hilo_200_reentry`** - `EmaHilo200ReentryStrategy` (`ema_hilo_200_reentry.py`): HYPE 4H discretionary mapping; the 200 close EMA permits direction while the 10 high/low EMAs control close-based stop and re-entry. Params: `fast_window=10`, `slow_window=200`. See [[projects/ema_hilo_200_reentry/hype-ema-hilo-200-reentry-codification|HYPE EMA High/Low 200 Re-entry Codification]].
- **`ema_px_trend`** - `EmaPxTrendStrategy` (`ema_px_trend.py`): EMA/PX trend-regime strategy codified from discretionary chart-led blind pattern matching (rules R1 regime side, R2 continuation, R3 chop gate, R4 extension exits, R5 long/short asymmetry). Params include `fast_window=10`, `slow_window=200`, `atr_window=14`, plus stress/capitulation/acceleration/extension/chop tuning. See [[research/trading/ema_px_trend/strategy_ema_px_trend|ema_px_trend Strategy Doc]].

## Maintenance

- When adding a strategy, add its `@register(...)` import to `__init__.py` and add a one-line entry here.
- Keep this page light: purpose + key params only. Do not paste backtest metric tables (re-fetch via Research MCP / backtest UI).
