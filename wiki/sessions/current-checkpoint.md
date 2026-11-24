# Current Checkpoint

Status: in progress

Compacted: 2026-11-23. These are the latest **recorded** states, not a fresh code/runtime audit or an instruction to resume every topic. Follow the current request; [[goals|Goals]] owns selected outcomes. Recheck code, branches, migrations, and ticket status before relying on older observations.

## Opposite Bid Trend — recorded 2026-11-24

- Code checkpoint `7258a969` adds the direction-only Example EMA 10/200 selector. It reproduced all 2,308 processed scores from the volatility-targeted BTC daily Example. The closeout ran 37 focused offline checks successfully. Historical EMA Opposite Bid execution performance is still unmeasured.
- Pickup is to choose the target risk size within the cap and sketch how distance from it changes the add and distribution fractions on eligible candles. The strategy note holds the urgency drawing, saved Example comparisons, and capture measures.
- Context [[research/trading/opposite_bid_trend/opposite-bid-trend]].

## Chart snapshot MCP — recorded 2026-11-23

- `render_backtest_snapshot` is committed as `6943c2ce`; refreshed MCP connection returned a native PNG and warning-free receipt for saved run `d7cfc05b-32d8-44d8-93b4-08a7ac9e0723` with `save=false`. The connection reload blocker is resolved; 167 offline tests and scoped lint/types passed.
- Preview is ephemeral; explicit saves verify strategy identity and retain deduplicated PNG/JSON. Fresh checkouts need the reviewed resvg binary provisioned locally. UI-local studies/zones and batch snapshots remain unsupported.
- Operating/storage instructions: [[ops/research-mcp-runbook]].

## Backtest dates and candles — recorded 2026-11-20

- Explicit scoring dates (`4d8b9839`), Latest N completed scoring candles plus warmup (`7269ac88`), and per-span half-open fresh-fetch filtering (`316ac7ed`) are committed.
- Saved verification runs: explicit dates `8256221e-4a8b-411a-8518-be91f3305500`; Latest N `e28447ab-3b23-44f7-92f6-98efba0faf63`. Those checks used cache; the fresh-fetch repair has 61 focused offline tests.
- Remaining issue: existing cached unfinished boundary candles are not retroactively repaired. Inspection/repair requires a separately scoped request.
- Contract and evidence: [[engineering/backtest-date-windows]].

## Terminal and live lifecycle — recorded 2026-11-11 / 2026-10-30

- Terminal execution and USD sizing committed as `19e78138`. Market/limit/stops/scale arrays and Cancel/Close are wired through existing paths. Percentage/MAX controls were deliberately removed. OrderManager was preserved; account feeds own displayed state.
- Order-metadata discovery remains unresolved, including whether an exchange fetch is necessary. No separate frontend order registry, retained placement requests, or unfamiliar-ID tracking was approved. Context: [[projects/trading-terminal-ui]].
- Separate live startup/recovery plan: dedicated accounts per strategy and explicit stop-and-flatten retained for stage one; service startup, synchronization, and explicit flattening are to be separated. Detailed implementation was not approved or begun at the recorded checkpoint.
- [MON-8](https://linear.app/money-machine/issue/MON-8/separate-live-startup-account-recovery-and-explicit-flattening), children MON-237–244: last recorded as Backlog. MON-237 is contract only; Destin deleted the proposed lifecycle test program. If resumed, review lifecycle/account scope first and preserve risk-halt exposure reduction. Each implementation chunk requires Destin's code review/acceptance before Done or continuing.

## Other pickup context — dated records, no automatic queue

- **Sizing, 2026-11-24:** committed `06a380bf`: one calculate_sizing for all nine callers, volatility max = 2 × risk base, reference_size mapper argument, no Carver allocation cap. 360 focused tests, two synthetic replays and six saved MCP runs passed; 4,386 candle decisions reconciled within execution tolerances. No push. [[engineering/bounded-ema-history#MCP sizing verification and commit — 2026-11-24]].
- **Indicators, 2026-11-17:** grouped package paths and imported helper/indicator behavior are documented in [[engineering/bounded-ema-history]]. ATR v1 remains a feature scaffold without trading rules; old streaming tests were stale after simplification. Do not treat earlier passing suites as validation of revised code.
- **NaN handling, 2026-11-16:** RSI/slope padding (`3da05787`) and uniform scaler cleanup (`15cb8800`) committed. Transform-units work and broader policy remain deferred; [[projects/nan-handling-positioning-audit]].
- **Account equity, 2026-11-03:** backend-derived series/UI delivered; migration `e24b6c91a703` was applied locally. This does not establish any other database's migration state; [[engineering/backtest-risk-measurement]].
- **Test isolation, 2026-11-03:** accepted and merged locally (`7e891a59`, merge `38fc3c93`); MON-149/245/246/247 recorded Done. Existing full-suite failures remain documented; [[ops/backend-testing]].
- **Engine V2, 2026-10-18:** earlier core rewrite was removed by Destin; do not restore it or resume its roadmap without new direction. Historical design context: [[projects/backtest-engine-v2-plan]].

## History and maintenance

[Full checkpoint before compaction](../../archive/history-compaction-2026-11-23/current-checkpoint.md) preserves detailed verification, earlier decisions, run IDs, and superseded state. [Archive guide](../../archive/history-compaction-2026-11-23/README.md) also routes to the full changelog and recovered deleted sources.

Replace the affected topic's state when it changes. Move completed detail to its domain page/history; keep this checkpoint under roughly 100 lines. Documentation cleanup did not run tests against the trading system, start services, mutate accounts, commit, or push.
