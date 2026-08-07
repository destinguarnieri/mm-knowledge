# Current Checkpoint

Date: 2026-08-06

Company frame: [[company/money-machine-360|Money Machine Operating Context]].

## Active Revenue Proof

- **Objective:** positive net realized live P&L after costs over a founder-set proof period.
- **Proof period:** not yet set; Destin sets it before live evaluation begins.
- **Company phase:** parallel revenue research and monetization. Strategy origin does not determine priority.
- **Research portfolio:** multiple agent-owned programs run in parallel. VWAP, the full EMA 10/200 program, EMA/PX agent vision, multi-speed EWMAC, position/control research, the Catalog queue, and the first multi-signal forecasting baseline are all represented on the Research Board and in Linear.
- **Current VWAP state:** no immediate-execution mapping is promoted. Both the whole-signal continuous control and corrected threshold-band identity failed the short forward window; the corrected mapper also weakened original-window economics and drawdown.
- **Observed VWAP blocker:** older Hyperliquid candles are unavailable for the planned preceding-window test, and fixed adverse slippage does not represent credible passive limit-order execution.
- **WIP:** one bounded issue per agent, many independent agents/programs in parallel; keep Destin's human decision/review queue small.

## Current Engineering State

- Agentic Research Loop product direction is now active and treats the research agent as the customer. Autonomous inspection will use typed MCP run discovery, bounded extraction, deterministic rendering, and structured annotations; the browser UI is human-only. The EMA 10/200 event study is the first vertical slice. Signal-deciles and the cancelled Study/Variant/Trial persistence redesign are explicitly not foundations for this work.
- `px_threshold` is implemented in `mm_v04` with Threshold Engine V3 transition-only full long/flat/full short sizing and no continuous rebalancing.
- The study's negative signal polarity is encoded as the strategy default. Four focused tests, focused Ruff, and focused mypy pass. The running backtest manager will not expose the strategy until Destin adds it manually in the UI.
- `px_threshold_continuous` uses the existing threshold-band mapper: exit edge → 0%, midpoint → 50%, entry edge → 100%, before volatility reduction. Thirty-two focused mapper/threshold tests plus Ruff/mypy pass. Its exact four-cell 15m evaluation completed 96/96 in every cell and is rejected as a monetization improvement.
- The shared PX threshold feature path now forwards the raw processed signal plus magnitude-only signal studies (`pos_mean`, `neg_mean`, and symmetric 1σ/2σ bands) using a default 200-bar stats lookback. Existing backtest UI rendering consumes these components directly; the price chart also receives VWAP mean and 1σ/2σ price overlays.
- Registered `px_threshold_slope` preserves threshold-only sizing and gates only fresh entries on `abs(normalized_vwap_slope) <= 0.1`, using a three-bar log-linear rolling-VWAP slope and the existing 252-bar min-max normalization. Existing exits are unchanged and blocked crossings are skipped. A first smoke exposed and corrected a missing hold-transition guard; ten focused tests plus Ruff/mypy pass. The corrected smoke and full paired Binance matrix completed.
- Registered `px_signal_bands` is the new bounded VWAP baseline: full threshold-only entry at the processed-signal outer 2σ band, inward exit at the same-side 1σ band, and synchronized 100-bar price/signal-stat lookback lengths. Its moving-band snapshot/state logic is local, following EMAC escalation; shared Threshold Engine V3 and DTOs are unchanged. It also emits display-only normalized VWAP slope, VFTI, PRI, RSI, ATR anomaly, volume anomaly, absorption, and ROC. Seventeen focused tests plus Ruff/format/mypy pass; manual UI registration and runtime smoke remain pending.


## Current Decision

VWAP remains one active program, but no tested immediate-execution mapping is promoted. The corrected threshold-band identity increased exposure and turnover, weakened original-window economics, worsened drawdown, failed stress, and remained negative forward. The frozen `0.4` rebalance floor is a manually discovered starting configuration, not an empirical optimum. PnL-aware resizing, wide stop loss, and slope filtering remain separate causal mechanisms. The frozen baseline may be revisited after credible mock limit-orderbook fills exist.

The confirmed VWAP thesis is selective, readiness-conditioned inward traversal: statistical extension identifies location, but the strategy does not indiscriminately fade price moving away from VWAP. Observable participant/price readiness and regime avoidance determine whether and when to trade; position and execution policy determine how risk is introduced and the inward move is captured. Destin has additional readiness tools to introduce.

MON-163 showed that the specific `abs(normalized_vwap_slope) <= 0.1` gate materially altered risk/economics on a disjoint Binance window, but it did not establish low slope as the correct semantic use of VWAP slope. Destin's visual observation and a return-blind BTC/ETH/SOL saved-series check show PX and slope magnitudes co-extend; low slope is rare at the largest PX extremes. Label low-slope filtering as a hypothesis. Keep slope level, slope extremity, PX/slope signed alignment, and slope change/deceleration as competing roles. The current threshold+slope mapping remains unpromoted; do not tune the three-bar/`0.1` identity on its evaluation window or create post-hoc asset exclusions.

EMA 10/200 is restored as a parent research program. Band-to-band traversal is one supported branch alongside the flip-only controls, thresholds, signal-stat market state, continuous/nonlinear positioning, and asset/timeframe selection.

One-signal → one-position backtests are retained as controls, not treated as the intended limit of strategy intelligence. The active queue now includes a bounded multi-signal market-state plus forward-price baseline and implementation of the confirmed bounded accumulation/distribution schedule architecture.

PnL-aware resizing is directionally confirmed but not specified: scaling in remains available, discretionary scaling out generally waits for profit, and threshold/stop exits override. Wide-stop semantics also remain open. Neither belongs in the corrected baseline rerun.

Destin observed that symmetric entry magnitude `±0.9` appears better than `±0.5`; preserve it as the first fixed setting for later threshold sensitivity, not a promoted result and not a change to the current mechanism test. PX threshold strategies now emit the calculated upper/lower 2-band prices beside RVWAP for full-retention chart inspection.

The isolated `±0.9` threshold-only test is complete on the same disjoint 20,000-bar Binance development window. It cut activity by more than half and broadly improved return/drawdown versus `±0.5` at 5/10 bps, but remained negative-median and had material counterexamples; preserve it as the stronger development reference, not a promoted or optimal threshold. Long-window saved runs: `17b63d0d` / `94dcfa45`. Full retention is currently capped operationally at 5,000 candles per individual job: BTC `e87153c9`, WLD `a0cc6330`, and NEAR `6b207683` are available for chart review. Multi-asset full-detail jobs that aggregate beyond this budget timed out without losing summary metrics.

Chart interpretation boundary: price-extension bands use raw percentage distance to VWAP over `LOOKBACK=100`; signal-stat bands use the processed/normalized signal over `signal_stats_lookback=200`. They are not expected to align panel-for-panel. Prior fixed-threshold trades did not consume the signal-stat bands, so existing economic evidence remains valid. Any future dynamic-band trade mechanism must choose its domain and lookback explicitly.

The fixed `±0.9` entry / `±0.5` exit follow-up (`616fe951`) is rejected: it reduced time active but increased turnover and worsened breadth, return, Sharpe, and tails versus `±0.9`/`±0.1`. NEAR chart review showed that profitable inward price travel can occur while processed extension remains beyond a fixed exit, leaving the position exposed to renewed continuation. The implemented dynamic baseline therefore chooses processed-signal 2σ entry / 1σ inward exit and synchronizes both lookback lengths at 100; this does not make raw price bands and processed-signal bands mathematically equivalent.

The dual-domain BTC 15m event study (`e88e7013` anchor, `d474a327` chronological replication) confirms that raw-price and normalized-signal bands carry the same reproducible traversal structure but are highly coupled. Under the stricter competing-barrier definition, inward 2σ→1σ completion before re-expansion is only about 49–54%, so the pending `px_signal_bands` smoke remains a baseline test rather than a promotion candidate. The normalized signal adds modest inward timing differences, not independent confirmation.

The fractional-depth extension (`52fa8f74` anchor, `c36a7b0f` chronological replication) rejects full touch as a necessary opportunity definition: outward continuation remained the minority at every fixed half-band checkpoint, and retry-allowed episodes frequently reversed without reaching the next checkpoint. It also rejects depth alone as a complete readiness or sizing rule; inward-turn completion was mixed and the losing branch remained larger. Use continuous depth as strategy-owned location and inventory-capacity context, not as an absolute target or an empirically selected nonlinear curve.

Backend average-entry overlays now make the threshold-only path defect visually explicit on single-asset runs: `±0.5` often commits the full position before the eventual price extreme, leaving a fixed average entry to absorb substantial adverse continuation because the mapping has no escalation or basis improvement. Treat this as chart-supported motivation for the isolated `±0.9` test and later separation of setup awareness from full commitment, not as proof that `±0.9` is optimal. Require full-retention price/average-entry/position/signal review alongside batch metrics for subsequent VWAP experiments.

Destin's stronger forward hunch is that the best VWAP capture will use the calculated 2σ extension price bands as the trade mechanism together with signal escalation. Treat this as an unvalidated later branch with semantics still open; `±0.9` processed signal is directional evidence for more selective entries, not mathematically the same object as the dynamic 2σ band.

## Verification

- The Agentic Research Loop Linear project is reactivated around the event-study acceptance journey. [MON-177](https://linear.app/money-machine/issue/MON-177/establish-research-run-artifact-workspace-and-contain-event-study) is Ready; MON-178–181 are dependency-blocked through describe/extract, render/annotations, evidence permissions, and end-to-end acceptance. [MON-182](https://linear.app/money-machine/issue/MON-182/decide-preservation-and-cleanup-of-legacy-tracked-event-study-outputs) is human-blocked on the roughly 312 MB / 355 tracked historical outputs. Existing saved-backtest `list_saved_run_series` / `get_saved_run_series` tools are retained as substrate.
- Linear MON-155 (fee/slippage cost semantics) is Done.
- Linear MON-156 (cold batch acceleration) is Done.
- Linear MON-145 (agent access to UI-owned saved runs) is Done.
- The Research Board is rebuilt around revenue candidates, reusable mechanisms, and horizon programs.
- Linear is rebuilt for parallel execution: MON-159 is Done; VWAP branches MON-162/163/164 are Ready; EMA 10/200 has a parent project with MON-157/165/167 Ready; EWMAC MON-166, bounded accumulation/distribution schedules MON-168, Catalog queue MON-169, multi-signal forecasting MON-170, and EMA/PX agent-vision MON-171 are Ready. Human-labeled EMA/PX MON-172 remains blocked on Destin semantics.
- Registered `px_threshold` implementation: 4 focused tests pass; changed files pass focused Ruff and source mypy checks.
- Four 96-asset threshold-only runs persisted: original-window 5/10 bps and short-forward 5/10 bps. Original-window economics improved materially; both forward medians were negative.
- Four canonical 5m threshold-only runs persisted. The original runs had 95 successes plus ACE negative-equity failure; both complete forward runs had 96/96. 5m is rejected under stress/forward evidence.
- Four 96-asset whole-signal continuous controls persisted and remain the comparison for the now-completed corrected threshold-band evaluation.
- Four corrected threshold-band continuous 15m runs persisted, each 96/96. Original breadth was 48/96 at 5 bps and 37/96 at 10 bps; forward breadth was 32/96 and 22/96. The mapper is rejected as a monetization improvement.
- PX magnitude signal-stat emission: 10 focused threshold tests pass; focused Ruff and mypy are clean.
- Isolated VWAP dual-domain event study: 17 focused tests pass; Ruff, formatting, mypy, function-length review, and diff checks are clean. Canonical KB artifact runs are `e88e7013` and `d474a327`; the split is chronological replication within development history, not a protected holdout.
- Fractional-depth event-study extension: 25 focused tests pass with clean Ruff/format/mypy/function-length/diff checks. Canonical schema-v2 KB artifacts are `52fa8f74` and `c36a7b0f`; no strategy, Threshold Engine, nonlinear allocator, persistence, live, or capital path changed.
- MON-163 is Done. Paired Binance runs: intended control `5ce4aa11`, intended slope `f1b57f85`, stress control `8fb88390`, stress slope `8fbde7bc`; 30/32 paired assets completed, with LIT/SKR failing symmetrically for incomplete history.

## Next Action

For VWAP, retain `px_signal_bands` as the binary control rather than the intended final mapping. After MON-168's bounded accumulation/distribution allocator passes deterministic semantics, run one offline strategy-shaped comparison of binary full-touch/full-position, linear distributed allocation, and one preregistered favorable backloaded schedule over the supported `0→2` depth coordinate. Keep readiness features, allocator curve tuning, and live wiring out of that comparison. Manual UI registration/smoke of the binary control remains useful for execution correctness, not as the destination design.
