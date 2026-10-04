# Position Lab: stages 1–3 implementation plan

Status: in progress
Date: 2026-09-23
Approval: Destin explicitly approved the full plan on 2026-09-23. Autonomous implementation of stages 1–3 is authorized.
Scope: local Position Lab simulator only.
Delivery: stages 1–3 implemented and verified locally on 2026-09-23; awaiting Destin’s product review. Policy remains experimental.

## Goal

Turn Position Lab into a repeatable policy sandbox: record and replay a price path, explain inventory and economics at every step, and compare today's one-pass allocation with rearming accumulation after returning to flat. Deliver all three stages together for Destin's final hands-on review after approval. Preserve the compact layout, vertical price axis, curve editor, long/short symmetry, and fixed price endpoints.

Related context: [[research/trading/positioning/size-distribution|Size Distribution]], [[sessions/current-checkpoint|Current Checkpoint]]. This is a proposed UI experiment, not an accepted live trading policy or a research profitability finding.

## Blocking questions

None. Approval accepts the concrete defaults below. Stage 3 deliberately compares two policies rather than settling the eventual market-making strategy.

## Assumptions and boundaries

1. Stages 1–3 stay client-side. The existing read-only preview endpoint supplies normalized curve samples; local simulation integrates those samples. No backend contract, generated client, database, websocket, live runtime, exchange, or backtest strategy changes are required.
2. Automatic simulation and monetary accounting apply to **price** coordinates. Preserve manual signal-mode behavior and regression coverage; signal coordinates must not be labeled prices or converted into monetary P&L.
3. A run has one immutable starting configuration, curve sample set, fee setting, and ordered path. Configuration edits pause playback and start a fresh run, as current configuration edits already reset the sandbox. Side changes retain the existing mirrored-range behavior and start a new run. No mid-run configuration-event system is needed.
4. Capture each accepted changed slider coordinate, including movements that produce no fill. Equal consecutive coordinates are no-ops. Sequence order, not rendering frequency or wall-clock timing, determines execution. A move means continuous traversal between its two coordinates using the existing integrated curve model, not a realistic exchange fill.
5. Replay uses captured curve samples, not a fresh network response. In-flight or failed preview requests cannot authorize new fills from stale curves. Existing chart content remains mounted while a new configuration is loading.
6. One-pass remains the default for compatibility. Rearm-when-flat is an explicit comparison policy. No replenishment after partial sales, continuous inventory targeting, automatic side reversal, endpoint adjustment, or inventory-dependent skew is included.
7. Fees default to zero and are a configurable non-negative basis-point rate on absolute simulated fill notional. Accounting assumes linear base-unit inventory and quote-currency prices, without leverage, funding, margin, inverse contracts, spread, or slippage. Values describe this sandbox model only.
8. State is bounded: at most 5,000 accepted path events per run, one active run and two comparison results. At the limit, pause and show an export/reset message; never silently discard the beginning of a reproducible run. No automatic browser-storage persistence; versioned JSON export/import provides recovery and sharing.
9. Local-only unit tests, build, lint, and browser verification are authorized by subsequent plan approval. Do not start the backend/Compose, mutate live systems, access secrets, commit, push, or deploy. If the existing preview service is unavailable, use fixtures for verification and disclose the browser limitation.

## Current implementation and cause of the dead space

`frontend/src/components/PositionLab/positionLabSimulation.ts` tracks cumulative accumulation and distribution progress. Once consumed, accumulation capacity does not regenerate when inventory is sold. Retracing therefore cannot refill until it exceeds the earlier accumulation progress. This is the current one-pass policy, not a chart repaint issue.

`positionLabSimulationTypes.ts` stores a starting plan, current snapshot, and up to 101 fill-oriented history snapshots. `usePositionLabSimulation.ts` combines local transitions with server curve previews. The current history is useful for fill undo, but cannot reconstruct an entire price path: it does not retain every non-fill movement. Preserve these semantics as the baseline while separating replay state from display history.

## Implementation sequence

### Stage 1 — Record, inspect, and replay

**Deliverable:** a compact price timeline with fill markers, record/play/pause, previous/next event, seek, replay-from-start, playback speed, and JSON export/import. The existing coordinate slider remains the manual path input.

- Extract deterministic transition functions from hook orchestration. Define typed run configuration, curve template, ordered input events, snapshots, fills, replay cursor, and engine/export version.
- Store coordinate events independently of the bounded visible fill-history list. Replay from the immutable initial state through an event index; backward seek reconstructs state rather than attempting to reverse floating-point fills.
- Capture curve samples and initial settings when a run becomes ready. Reject invalid/non-finite ranges, values, sample shapes, unsupported import versions, oversized files, or excessive events before replacing the active run. Validate the entire import atomically; leave the current run intact on failure. Proposed import file-size cap: 5 MB.
- Pause playback before configuration edits, import, reset, undo, or manual input. A manual move after seeking backward truncates the future path and starts a new continuation; show that behavior in a concise control hint. Seeking alone never deletes history.
- Retain fill undo semantics by rewinding/truncating to immediately before the last fill-producing event; the timeline's previous/next controls step through every event, including non-fill movements.
- Playback speed controls presentation only; never alter the event sequence or fill arithmetic. Process events in order and cancel playback on unmount or reset. Repeated React renders cannot add events or fills.
- Add a small deterministic scenario selector: accumulation/distribution round trip, repeated oscillation, and partial exit/retrace. Mirror scenarios for short mode. These are synthetic test paths, not downloaded market data.
- Keep the existing chart at no more than half the desktop main section. Place the timeline and controls compactly below or within that section; preserve a usable stacked layout on narrow screens.

**Completion checks:** recording retains non-fill movements; replay produces the original inventory, average, progress and fills; backward/forward seek is exact within the documented numerical tolerance; export/import reproduces the run without a new preview request; invalid imports preserve current state; playback cancellation and the event cap work; existing long/short and signal tests still pass.

### Stage 2 — Inventory, economics, and inactivity explanations

**Deliverable:** synchronized inventory/average and P&L history, a fill ledger, and a plain-language explanation of what each side can do at the selected event.

- Extend fills with sequence ID, schedule/cycle ID, execution side, quantity, price, fee, and realized P&L. Preserve pre/post inventory and average in derived snapshots; do not keep duplicate unbounded histories.
- Use average-cost accounting. Accumulation updates weighted entry average. Distribution realizes `sideSign × quantity × (fillPrice − priorAverage)`, where long is +1 and short is −1. Partial exits preserve the remaining average; flat clears it to null.
- At each event, unrealized P&L is `sideSign × inventory × (currentPrice − average)`, or zero when flat. Fees accumulate separately and do not change entry average. Net total P&L equals gross realized plus unrealized minus fees.
- For seeded inventory, supplied entry average defines cost basis. Pre-run fees and realized P&L are unknown and excluded. Clearly label this basis; separately show change in net P&L since the initial mark so a run does not appear to earn its pre-existing unrealized P&L.
- Return structured status reasons from the engine, rather than guessing from chart geometry: empty inventory, capacity reached, outside the range, wrong traversal direction, consumed schedule, waiting for valid curves/configuration, and ready for eligible traversal. Show the primary reason per side and the last event's fill/no-fill reason.
- Extend the compact ledger with execution price, quantity, average after fill, realized P&L and fees. Let selecting a fill seek to its event. Provide compact history views without expanding the curve panel beyond the existing 50% width.

**Completion checks:** hand-calculated long and short examples cover weighted additions, partial exits, complete exits, fees, initial inventory, and multiple cycles; total P&L identity holds at every event; no average at flat; no monetary P&L in signal mode; reasons distinguish consumed allocation from simply being outside the range; ledger and charts agree after seek/import.

### Stage 3 — Explicit rearming and policy comparison

**Deliverable:** selectable One pass / Rearm when flat behavior and an aligned comparison using exactly the same starting inputs, curve samples, fees, and recorded price path.

- Keep one-pass results unchanged. Implement rearming as a policy transition around the same fill engine, not a second copy of fill/accounting math.
- Rearm exactly once when distribution changes positive inventory to zero. Issue a new accumulation schedule/cycle ID, clear its consumed quantity, and restore its budget to available capacity. Retain the configured accumulation start/end and curve shape; retain the configured distribution far endpoint.
- Initialize the new schedule at the current coordinate's clipped progress. Do not execute historical portions retroactively, and do not generate a second fill in the same event that closes the old position. Subsequent eligible accumulation-direction movement can consume the new schedule. Normally the closing coordinate lies outside the accumulation zone, so its new progress is zero; overlapping ranges can still leave an intentional consumed segment. Explain this limitation rather than promising that every inactive price disappears.
- While flat, average is null and distribution is inactive. On the first new accumulation, average is established and distribution starts there. New accumulation continues to rebuild the distribution schedule with then-current inventory; partial distribution keeps that schedule frozen, matching the approved current behavior.
- Rearming does not reset the run's realized P&L, fees, timeline or ledger. There is no rearm on initial empty state, repeated empty ticks, partial exits, or rendering. Only a positive-to-flat exit triggers it.
- Compute both policy results from the immutable run inputs. Selecting a policy never seeds its result from the other policy's ending state. Keep both views synchronized to the same event index, with a summary of inventory, average, gross realized, unrealized, fees, net P&L, traded quantity, fills and completed cycles.
- Mark rearm events on the timeline and identify cycles in the ledger. The repeated-oscillation preset should visibly show the baseline remaining consumed while the rearmed policy can enter a second cycle.

**Completion checks:** long and mirrored short scenarios complete two full cycles under rearming; baseline retains its current dead-space behavior; partial exits do not rearm; unchanged coordinates cannot transact twice; large traversals do not exceed capacity or sell below zero; repeated seeks and comparisons are deterministic; endpoints stay fixed and distribution start follows the inventory average.

## File-level work map

Paths below are relative to `mm_v04`; use existing neighboring conventions and keep functions under 60 lines.

| File | Planned responsibility |
| --- | --- |
| `frontend/src/components/PositionLab/positionLabSimulationTypes.ts` | Typed run/event/fill/snapshot/status/policy contracts; keep public API DTOs unchanged. |
| `frontend/src/components/PositionLab/positionLabSimulation.ts` | Pure event transitions; preserve baseline; structured results and schedule identity. |
| `frontend/src/components/PositionLab/positionLabReplay.ts` (new) | Run creation, ordered replay/seek, branching, event limits, versioned import/export validation. |
| `frontend/src/components/PositionLab/positionLabAccounting.ts` (new) | Average-cost, realized/unrealized, fee and initial-mark calculations. |
| `frontend/src/components/PositionLab/positionLabPolicy.ts` (new) | One-pass/rearm policy transitions and comparison inputs. |
| `frontend/src/components/PositionLab/positionLabScenarios.ts` (new) | Small deterministic mirrored path presets. |
| `frontend/src/components/PositionLab/usePositionLabSimulation.ts` | React orchestration, preview readiness, run lifecycle and cancellable playback; no duplicated accounting. |
| `frontend/src/components/PositionLab/PositionLabTimeline.tsx` (new) | Price path, fill/rearm markers and playback/seek/import/export controls. |
| `frontend/src/components/PositionLab/PositionLabResults.tsx` (new) | Inventory/economics history, current status and aligned policy comparison. |
| `frontend/src/components/PositionLab/PositionLab.tsx` | Compose existing editor/chart with compact new panels. |
| `frontend/src/components/PositionLab/PositionLabControlPanel.tsx` | Fee and policy inputs with explicit fresh-run behavior. |
| `frontend/src/components/PositionLab/PositionLabHistoryPanel.tsx` | Ledger fields and selection-to-seek. |
| `frontend/src/components/PositionLab/PositionLabChart.tsx` | Selected replay snapshot and status overlays; preserve existing axes/layout. |
| `frontend/src/components/PositionLab/positionLabLifecycle.ts`, `positionLabCurve.ts`, `positionLabSide.ts` | Reuse current arithmetic/mirroring; change only for demonstrated integration needs. |
| `frontend/tests/position-lab.spec.ts` plus focused replay/accounting/policy specs | Regression and new behavioral tests; update `frontend/playwright.unit.config.ts` matching only if necessary. |

Proposed pure interfaces: `applyLabEvent(state, event, context) -> transition`, `replayLabRun(run, cursor, policy) -> replayResult`, `accountLabFill(account, fill) -> account`, and `parseLabRun(json) -> validatedRun | validationError`. Exact names can follow local conventions without changing the contract. Reuse Recharts and current UI controls; no new runtime dependency is planned.

Do not replace ordered events with fill-only history: that loses the no-fill traversal needed to explain the reported behavior. Do not simply clear accumulation progress on every retrace: that would repeatedly consume the same allocation without an explicit policy boundary.

## Verification and final delivery

1. Before edits, record repository status and run the existing Position Lab unit suite as a baseline. Preserve unrelated user changes.
2. Add focused tests with independently calculated expected outcomes, including event subdivision invariance for a monotonic traversal, long/short symmetry, import rejection, and accounting conservation. Specify absolute/relative numerical tolerances and avoid using the implementation itself as the test oracle.
3. At each stage, run its focused tests and applicable existing regressions. At integration, run scoped lint and the frontend production build. Do not broaden checks without a relevant failure or new risk.
4. Use the running in-app browser to verify record/replay/seek, full and partial cycles, comparison, export/import, loading/error behavior, and desktop/narrow layouts. Inspect UI state without operating live-system controls. If unavailable, record the exact unverified checks rather than claiming they passed.
5. Finish with a seeded example ready for review, concise usage steps, changed-file summary, test evidence and limitations. Update durable docs with actual behavior and remaining stages 4–6; do not promote a policy to confirmed merely because its tests pass.

## Autonomous execution and checkpoints

After explicit approval of this plan, execute stages 1, 2 and 3 sequentially without requesting approval between stages. Make routine implementation/layout choices within this contract. Keep this file as the authoritative pickup plan and update the checkpoint table after each completed stage and before any interruption/context handoff. Keep the shared current-checkpoint page thin and link here; append significant completion/decision evidence to the session changelog.

Checkpoint records must contain completed work, changed files, test results, unresolved failures, next concrete action, and any deviation. Record approval here before starting. Do not mark a stage complete until its acceptance checks pass, or silently substitute a different policy. If evidence requires a material semantic change, backend/live work, or expansion beyond this plan, stop the affected implementation and present the evidence and smallest proposed revision for approval. Ordinary test failures are work to resolve, not reasons to hand the task back.

| Checkpoint | Status | Evidence / next action |
| --- | --- | --- |
| Plan and approval | Approved | Explicit user approval 2026-09-23; no intermediate stage approval required. |
| Baseline | Complete | Clean worktree; all 32 existing Position Lab unit tests pass. |
| Stage 1 | Complete, with export-download limitation below | Event replay, branching, presets, bounded validation/import, timeline and playback delivered. Browser verifies valid/invalid imports, exact paused cursor, stepping, manual branching, config-change cancellation, and copyable JSON export. |
| Stage 2 | Complete | Accounting, statuses, history charts, fee input and bounded seekable ledger delivered. Independent tests cover long/short partial/full exits, seed basis, fee identity and signal exclusion. Browser short partial exit agrees with hand calculation. |
| Stage 3 | Complete | Shared engine supports flat rearming, cycle IDs, markers and same-path comparison. Long and short second cycles verified in tests and browser; baseline, partial-exit and endpoint rules preserved. |
| Integration and handoff | Complete | 51 unit tests pass, scoped Biome lint passes, production build passes, diff whitespace check passes. Desktop/narrow UI checked; final long oscillation example left paused at event 80 with rearming selected. Next: Destin’s hands-on review. |

## Explicitly deferred

Stages 4–6 remain separate: visible discrete quote ladders/reservations, inventory-aware reference/spread/skew/refresh policy, and realistic execution/market data/backend migration. Also deferred: historical data ingestion, queue position, partial exchange fills, latency, tick/lot rounding, funding, margin/liquidation, profitability claims, and saved-run APIs. This plan is a medium frontend simulator extension, with no database migration or production trading integration.

### Implementation observation — overlapping ranges

The existing simulator guard rejects a distribution endpoint on the accumulation side of its start while flat. Rearming preserves this baseline validation: it clips new progress and creates no retroactive fill, but a configuration that becomes invalid at flat remains blocked with an explicit reason. No new endpoint policy is introduced.

## Delivery evidence and review guide — 2026-09-23

Implementation stays under `frontend/src/components/PositionLab/` plus `frontend/tests/position-lab-run.spec.ts` and its unit-test matcher. In addition to the planned modules, validation, status text, comparison and export UI were separated into small focused files. No backend/schema, trading runtime, database or generated-client changes; no commit, push or deployment.

Verification:

- `playwright test -c playwright.unit.config.ts tests/position-lab.spec.ts tests/position-lab-run.spec.ts`: 51 passed, including all 32 baseline tests. Numerical accounting comparisons use explicit 1e-8 or tighter tolerance; a full 5,000-event / 121-sample run passed in roughly 0.12 seconds in the unit runner.
- Scoped Biome lint (22 files), frontend production build and `git diff --check` passed. Build retains existing route code-splitting and large-bundle warnings.
- Running localhost browser: long oscillation comparison, short imported replay with fees, partial-exit ledger seeking, replay/play/pause/step, manual slider cycles, rewind branching, fresh-run fee edit, invalid-range disabling with chart retained, valid import, rejected import preserving event 16, and copyable JSON export all verified.
- Narrow 390×844 viewport override and desktop viewport have no page-wide horizontal overflow; wide tables scroll within their own panels. Temporary viewport override reset.
- Initially, the browser denied file selection when Destin was away. Destin then explicitly authorized retry; both invalid and valid local JSON imports passed. This was browser file-access permission, not a backend data upload.

Limitations and recovery:

- The embedded browser did not emit a download event for JSON export, even with a mounted link and delayed blob cleanup. Native file-download completion remains unverified in that browser. Export now includes a verified Copy JSON button and selectable JSON text as a recovery path; save that text as `.json` to import later. Export serialization/import roundtrip tests pass.
- No live backend outage was induced. Preview failure/stale-data guards remain in the hook; invalid configuration was exercised in the browser. Imported runs use captured samples with the preview query disabled.
- No automatic reload persistence: export before closing/reloading. One active run contains at most 5,000 input events and two derived arrays of at most 5,001 frames; engine fill history stays bounded to 101 snapshots and the ledger renders the latest 100 fills. There is no growing run archive. Replays are memoized across cursor changes.
- Signal mode retains manual execution and omits monetary economics and price-policy comparison. One pass remains the default; rearming never occurs on partial exits. The existing overlapping-range validation is retained as described above.

For review: open Position Lab, load **Repeated oscillation**, and compare **One pass** with **Rearm when flat** at the end (already prepared in the browser). Rewind or drag the event slider to inspect the second accumulation cycle; select a ledger event to inspect its inventory, average and P&L. Set fees before recording a new path. Stages 4–6 remain deferred.

## Approved UI consolidation — 2026-09-25

Destin reviewed stages 1–3 and confirmed they function as described, then approved a UI-only consolidation. The workspace now has equal desktop columns: curve chart, Move price and replay on the left; integrated Accumulate/Distribute editors and History/Compare/Fills tabs on the right. A top toolbar contains side/policy/scenario controls, Setup drawer, Overlays, Run actions and help. A shared status strip keeps inventory/capacity, average and P&L visible. The separate permanent configuration sidebar and repeated summaries were removed. Comparison uses metric rows so both policies fit the panel; schedule IDs are available on ledger event hover. Simulation/replay/accounting behavior is unchanged.

UI verification: at 1148px viewport, columns measure 549px each and the chart, both editors, playback and history charts fit the first screen. At 390px, panels stack without horizontal page overflow. Setup, result tabs, Run/Export dialog and ledger controls were checked in the running browser. Temporary viewport override reset. Existing 51 regression tests pass; scoped lint/build verification accompanies the change. No new behavior tests added for presentation-only changes.

Navigation update: setup inputs are under **Setup**; import/export/reset under **Run**; detailed results under **History / Compare / Fills**. Curve inputs now sit beside their own fill/status summaries. Existing export-download limitation and all simulation policy boundaries still apply.
