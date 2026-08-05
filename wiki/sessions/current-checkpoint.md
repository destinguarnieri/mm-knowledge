# Current Checkpoint

Date: 2026-08-04

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

- `px_threshold` is implemented in `mm_v04` with Threshold Engine V3 transition-only full long/flat/full short sizing and no continuous rebalancing.
- The study's negative signal polarity is encoded as the strategy default. Four focused tests, focused Ruff, and focused mypy pass. The running backtest manager will not expose the strategy until Destin adds it manually in the UI.
- `px_threshold_continuous` uses the existing threshold-band mapper: exit edge → 0%, midpoint → 50%, entry edge → 100%, before volatility reduction. Thirty-two focused mapper/threshold tests plus Ruff/mypy pass. Its exact four-cell 15m evaluation completed 96/96 in every cell and is rejected as a monetization improvement.


## Current Decision

VWAP remains one active program, but no tested immediate-execution mapping is promoted. The corrected threshold-band identity increased exposure and turnover, weakened original-window economics, worsened drawdown, failed stress, and remained negative forward. The frozen `0.4` rebalance floor is a manually discovered starting configuration, not an empirical optimum. PnL-aware resizing, wide stop loss, and slope filtering remain separate causal mechanisms. The frozen baseline may be revisited after credible mock limit-orderbook fills exist.

EMA 10/200 is restored as a parent research program. Band-to-band traversal is one supported branch alongside the flip-only controls, thresholds, signal-stat market state, continuous/nonlinear positioning, and asset/timeframe selection.

One-signal → one-position backtests are retained as controls, not treated as the intended limit of strategy intelligence. The active queue now includes a bounded multi-signal market-state plus forward-price baseline and a correctness audit of nonlinear/Citadel-inspired position mappings.

PnL-aware resizing is directionally confirmed but not specified: scaling in remains available, discretionary scaling out generally waits for profit, and threshold/stop exits override. Wide-stop semantics also remain open. Neither belongs in the corrected baseline rerun.

Destin observed that symmetric entry magnitude `±0.9` appears better than `±0.5`; preserve it as the first fixed setting for later threshold sensitivity, not a promoted result and not a change to the current mechanism test. PX threshold strategies now emit the calculated upper/lower 2-band prices beside RVWAP for full-retention chart inspection.

Destin's stronger forward hunch is that the best VWAP capture will use the calculated 2σ extension price bands as the trade mechanism together with signal escalation. Treat this as an unvalidated later branch with semantics still open; `±0.9` processed signal is directional evidence for more selective entries, not mathematically the same object as the dynamic 2σ band.

## Verification

- Linear MON-155 (fee/slippage cost semantics) is Done.
- Linear MON-156 (cold batch acceleration) is Done.
- Linear MON-145 (agent access to UI-owned saved runs) is Done.
- The Research Board is rebuilt around revenue candidates, reusable mechanisms, and horizon programs.
- Linear is rebuilt for parallel execution: MON-159 is Done; VWAP branches MON-162/163/164 are Ready; EMA 10/200 has a parent project with MON-157/165/167 Ready; EWMAC MON-166, position-control MON-168, Catalog queue MON-169, multi-signal forecasting MON-170, and EMA/PX agent-vision MON-171 are Ready. Human-labeled EMA/PX MON-172 remains blocked on Destin semantics.
- Registered `px_threshold` implementation: 4 focused tests pass; changed files pass focused Ruff and source mypy checks.
- Four 96-asset threshold-only runs persisted: original-window 5/10 bps and short-forward 5/10 bps. Original-window economics improved materially; both forward medians were negative.
- Four canonical 5m threshold-only runs persisted. The original runs had 95 successes plus ACE negative-equity failure; both complete forward runs had 96/96. 5m is rejected under stress/forward evidence.
- Four 96-asset whole-signal continuous controls persisted and remain the comparison for the now-completed corrected threshold-band evaluation.
- Four corrected threshold-band continuous 15m runs persisted, each 96/96. Original breadth was 48/96 at 5 bps and 37/96 at 10 bps; forward breadth was 32/96 and 22/96. The mapper is rejected as a monetization improvement.

## Next Action

Agents pull separate Ready issues in parallel, one bounded issue per agent. Preserve each mechanism's identity, fixtures, holdouts, and cost assumptions; synchronize the thread page, Research Board, and Linear at closeout. Destin reviews only named semantic forks, cross-workstream conflicts, and promotion decisions.
