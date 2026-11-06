# Trading terminal UI

Status: in progress

Date: 2026-10-30

## Selected direction

Destin selected a separate `/terminal` route, Hyperliquid perpetuals first, no order book, and resizable/dockable panels from the outset. The reference screenshot has a dominant chart upper left, order entry upper right, positions/orders below the chart, and margin below order entry. This frontend-only work proceeds independently of the live startup/recovery refactor; execution remains unwired.

## Local implementation

Checkpoint commit: `db455737` (`feat: add dockable trading terminal UI`) on `feat/terminal`, created at Destin's request on 2026-10-30. Repository worktree was clean after that commit; not pushed. That checkpoint includes the complete first frontend pass and 18 isolated tests. Subsequent named-layout changes are local and uncommitted.

Worktree: `/Users/destinguarnieri/.codex/worktrees/a137/mm_v04`. New `frontend/src/components/Terminal/` components and a sidebar route use Dockview React for drag-to-dock tabs, splits, resizing, floating groups, maximize/restore, close/reopen, and Reset layout. Layout saves in browser localStorage under `mm-terminal-layout-v1`; malformed/unavailable storage falls back to defaults or reports saving unavailable. Layout, watchlist organization, and chart drawings persist independently; order drafts are ephemeral and stay in shared React context across docking.

The chart uses Lightweight Charts with deterministic sample candles, EMA overlays, market/timeframe selectors and click-to-set order prices. The local ticket includes market/limit/stop/scaled modes, asset/USD and percentage sizing, margin/leverage selectors, post/reduce-only, time in force, and TP/SL fields. Long/short actions preview only: no execution request or fabricated fills. Positions/orders/fills show empty states; margin uses explicitly labelled sample values. Exchange validation and live account/market integration are deferred. Mobile workspaces currently scroll horizontally below the 660px desktop minimum.

## State and integration boundaries

Bounded to seven unique panels, 320 fixture candles per chart, 2–50 scale levels, one draft and one preview; saved layouts are limited to 64,000 characters. No growing event history or backend subscriptions. Existing Monitor hooks are route-independent but strategy/account ownership and running-state gates make them unsuitable as a direct independent-account Terminal hook. Shared streamCoordinator/wsManager remain available for later wiring; do not bypass the ongoing account-recovery design.

## Verification and next step

Focused browser checks cover sizing, local preview actions, chart-price picking, market changes, docking, resizing, closed/floating layout reloads, reset, and corrupt layout recovery. Run `playwright test --config playwright.terminal.config.ts`; an optional `PLAYWRIGHT_CHROMIUM_EXECUTABLE_PATH` selects an installed browser. The isolated test fixture and `tests/terminal-server.mjs` never load local env files or start backend services. Production build, TypeScript and scoped Biome lint are the static checks. Review the UI with Destin and iterate from additional screenshots. No commit, push, deployment, account mutation, or live runtime operation.

Related: [[sessions/current-checkpoint]] · [[sessions/session-change-log]]

## UI refinements — 2026-10-30

Destin requested freely tracking crosshairs with no indicator dots; larger sizing inputs immediately after order type; price controls below size; compact margin/leverage selectors fixed at the ticket bottom; and sample Total/Available boxes under the preview buttons. These are implemented locally.

To avoid accidental tab closure, Destin selected a corner icon with per-panel tab visibility checkboxes instead of tab X buttons. Default tab close buttons and middle-click closing are disabled. Checking a hidden tab opens it in that panel; selecting a tab displayed elsewhere explicitly says Move here and relocates the existing instance. Unchecking the final tab removes the empty group; workspace Panels + and Reset layout remain recovery controls. Visibility and movement use the existing layout persistence. TypeScript, scoped lint, and three targeted browser tests pass, covering visibility, unique tab ownership, middle-click behavior, docking and persistence.


## Watchlist — 2026-10-30

Added a dockable Watchlist tab through the existing panel chooser. Fresh layouts include it beside Margin; existing saved layouts are retained. One named list currently supports search, collapsible sections, creating/removing empty sections, and adding/removing/moving the three sample markets (BTC, ETH, SOL). Clicking a market selects it in the chart and order ticket; clicking the already-selected market preserves the draft. Multiple named lists are a future request, not implemented; stable list/section IDs provide the starting structure.

Watchlist state is shared above docked panels and independently persisted at `mm-terminal-watchlist-v1`. Bounds: 12 sections, 40-character names, three unique supported markets, 16,000-character storage-read limit. Invalid storage falls back to defaults and failed saves are indicated. Layout reset does not reset the list. No live price subscription or order wiring was added.

All eight isolated terminal tests pass, including market selection, section organization, search across collapsed sections, hide/reopen/reload, layout reset, and invalid watchlist recovery. TypeScript, scoped Biome lint and frontend production build pass; existing bundle-size and route-export warnings remain.


## Default chart price gestures — 2026-10-30

Limit orders now use any primary mouse click in the plot to set price without arming a picker. Limit Scale uses a primary mouse drag: press sets the start endpoint, release sets the end endpoint, preserving drag direction. A shaded price range previews the gesture; both draft fields commit together on release. Shift-drag retains normal chart panning in scaled mode; ordinary dragging pans in limit mode. Escape, window blur, wheel navigation, order-mode changes, or chart teardown cancel pending range selection. Single scaled clicks and releases outside the plot leave both prices unchanged. Axis clicks are excluded. Stop Market and Stop Limit also default to chart clicks for the trigger price. In Stop Limit, focusing either price input makes it the persistent chart-click target, highlighted with a border. Switching mode/market resets the target to trigger. All numeric fields remain editable; arming buttons and the cancel-picking banner have been removed.

Implementation uses bounded transient gesture state and one visual overlay; listeners are cleaned up with the chart. No new persisted state or execution requests. Focused browser checks cover repeated limit clicks, ascending/descending scale drags, cancellation, axes, panning, and stop-order picking. TypeScript, scoped lint and production build pass with existing build warnings.


## Persistent scale levels — 2026-10-30

The scaled-order draft now remains visible after range selection as dashed order-level lines plus a yellow quantity-weighted average line, with Start/End/Avg axis labels and a draft legend. Lines derive from current valid draft prices/count/distribution; manual edits update them and timeframe/EMA recreation restores them. Non-scaled modes, invalid price inputs, and market changes remove them. The average is normalized by distribution weights, available before total quantity is entered, and shared with the ticket's average display.

Native chart price lines stay aligned through pan/zoom/resize. At most 50 order lines plus one average are retained; replacements and chart teardown remove old lines. Drafts remain ephemeral, with no new browser persistence or live-order calls. Focused checks cover drag-release visibility, weighted-average arithmetic, manual edits, invalid-input cleanup and chart recreation; TypeScript, scoped lint, production build and visual inspection pass. Existing build warnings remain.


Stop-click refinement verification: three focused browser checks pass for repeated stop trigger clicks, stop-limit field targeting, mode reset, axis/pan exclusion and existing limit/scale gestures. TypeScript and scoped lint pass. Native mouse handling is shared across order types so rapid separate clicks are not suppressed by the chart library's double-click detector. No new persisted state or live calls.


## Order type selector — 2026-10-30

Replaced the native select with an inline expandable two-column selector matching Destin's reference. Limit: Order, Stop, Click, Chase TWAP, Chase, Scale. Market: Order, Stop, Swarm, TWAP. Scale Side intentionally excluded. Selected type is highlighted; choosing an entry collapses the panel and returns focus to its trigger; Escape also closes it.

The five existing types retain their price gestures and local preview behavior. New types (Limit Click, Chase TWAP, Chase, Market Swarm, TWAP) are selectable UI placeholders: controls/preview are explicitly pending, preview buttons disabled, no generated levels or chart-price mutation. Their detailed semantics remain to be specified. Ten fixed type definitions, one active draft, and one local expanded flag; no new storage or backend integration. All 14 terminal tests pass; final accessibility-markup refinement passes its focused selector test. TypeScript, scoped lint, build and visual inspection pass with existing build warnings.


## Horizontal drawing shortcuts — 2026-10-30

Added Alt-H horizontal line and Alt-J horizontal ray, immediately at the hovered chart cursor. Ray anchors store timestamp and price; native series primitives render them against the chart's logical/time and price transforms across pan, zoom, resizing and timeframe/EMA recreation. Current fixture candles use a regular interval for timestamp/logical conversion; revisit that adapter when wiring irregular/live bars. Lines span the plot, rays extend right from their anchor. Selected drawings show a price label and ray anchor handle.

Click a drawing to select it without changing order prices; Delete/Backspace removes it; Escape deselects. The shortcut hint, drawing counter and trash toolbar were removed at Destin’s request. Right-click a chart and choose Clear drawings to remove all drawings for that chart’s market, including shared copies on matching charts; other markets are preserved. The action is disabled when that market has no drawings. Right-click prevents native focus from changing the active chart or ticket draft. Drawing-save failures are shown in this context menu. Shift-drag remains available for panning. Keyboard creation is ignored over axes, outside the plot, during mouse presses, for key-repeat, and in input/select/textarea/contenteditable editors. Drawing repositioning/style editing is not yet implemented.

Shared provider state preserves drawings across panel hide/reopen. Local storage `mm-terminal-drawings-v1` validates IDs, markets, kind, finite positive price, timestamps and bounds: 50 drawings per market, 150 total for the three supported samples, 40,000-character storage-read cap. Invalid storage falls back to empty, save failures are indicated, selection is transient and clears on market change. No backend subscriptions or trading actions. Primitive and input listeners detach on chart teardown. All 16 terminal tests, TypeScript, scoped lint, build and screenshot inspection pass; existing build warnings remain.


## Candle and indicator colors — 2026-10-30

The chart toolbar Colors popover offers Normal/Grayscale/Custom candles, custom up/down color pickers, and Grayscale/Colored indicators. Terminal reuses `config/backtestChartColors.ts` helpers used by the backtesting chart: indicator values above candle close are red, below close green, equal/missing gray. Both EMA overlays get per-point colors; normal/neutral candle palettes and neutral indicator colors come from the same shared helper. Backtesting code and preferences were not modified.

One validated Terminal-only preference record at `mm-terminal-chart-appearance-v1` stores two modes and two six-digit hex colors (1,000-character read cap). Invalid/missing data falls back to defaults, failed saves are indicated. Provider state survives panel remounts. Appearance changes apply to existing candle/EMA series, preserving the viewport, draft and drawings; EMA visibility now also updates in place. State remains bounded to the same two 320-point indicators and candle series. All 18 terminal tests, scoped TypeScript/lint, production build and screenshots pass; existing build warnings remain.


## Named layouts — 2026-10-30

Destin called the first pass complete and requested multiple saved layouts, retaining the four-panel arrangement as Default. The workspace toolbar now offers a layout selector, Save to update the selected custom snapshot, and a management popover for Save as, Rename, and two-step Delete. Default is immutable; Reset layout restores it. Snapshots preserve panel visibility, grouping, sizes, active tabs and floating groups. Dockview is isolated in its own stacking context so floating groups cannot cover toolbar popovers.

The current workspace continues autosaving separately at `mm-terminal-layout-v1`, retaining existing browser layouts and unsaved arrangement changes across reload. Named snapshots change only through Save/Save as. `mm-terminal-saved-layouts-v1` contains an active ID plus up to 12 custom snapshots with stable UUIDs, unique case-insensitive trimmed names of 1–40 characters, 64,000 characters per snapshot, and an 800,000-character library read cap. Default is a reserved ID/name. Switching replaces the current workspace; deleting the selected custom snapshot returns to Default. Malformed library storage falls back to an empty library; invalid selected snapshots restore Default with an error. Failed writes keep in-memory state and visibly report unavailable persistence. Layouts remain browser-local; watchlists, drawings, appearance and shared draft state are independent.

All 21 isolated terminal tests pass, including saved-layout lifecycle, snapshot isolation from autosave, validation, corrupt snapshot recovery, failed storage, and existing docking/chart/order interactions. TypeScript, scoped Biome lint, production build and visual inspection pass; existing build warnings remain. No backend integration, live operation, new commit or push.


## Multiple charts — 2026-10-30

The toolbar Charts menu now offers Single chart, Two stacked, and Four-chart grid. These are real Dockview panels with stable IDs `chart`, `chart2`, `chart3`, `chart4`, all rendering the same chart component. Presets preserve current chart settings while rearranging existing instances, restore non-chart group sizes, and recover from tabbed/floating charts. Extra charts can also be shown/hidden through the existing panel chooser. Default remains the original four groups with one chart; at most four chart instances and ten panel IDs exist. The canvas now has `min-width: 0` so its price axis stays visible when a docked panel shrinks.

Each chart owns its market, timeframe and EMA visibility independently. Destin approved removing linking and hover activation: clicking a chart body or tab selects it and makes the ticket follow its market. The first primary plot gesture on an inactive chart only activates it; subsequent clicks/drags can edit prices. Hover and focus alone do not change chart selection. Clicking the ticket, watchlist or another non-chart panel keeps the selected chart. Ticket/watchlist market changes update only that chart. Same-market switches preserve the draft; market changes reset draft, price target, preview and drawing selection.

Chart settings (market, timeframe, EMA visibility) live in strictly validated Dockview parameters and persist in workspace autosave/named snapshots. Old snapshots containing a `linked` boolean remain readable; validation discards the retired flag and preserves the stored market/timeframe/EMA settings. Legacy charts without parameters use defaults. Color preferences remain shared. Order drafts remain transient and are not saved with layouts.

Only the active chart can edit order prices or use drawing shortcuts, with the pointer inside its plot for shortcuts. Shared drawings and draft-scale lines still render on every chart of the corresponding market. A pointer-down capture records whether a plot gesture began inactive and blocks its mouse-down from reaching drawing/order handlers even after React changes selection. Stop-field focus targeting and scale drag semantics are unchanged. Tab activation is handled explicitly because the default Dockview tab can report its selection through an API-origin event. The Dockview subscription stays stable, filters programmatic active-panel events, and reconciles chart settings after layout restoration/removal. Selection uses one bounded ID/market record and a Dockview API reference, without duplicating chart settings or adding a new persistence store.

Footprint is bounded to four charts, each with 320 sample candles, two EMA series, and at most 51 scale lines. Drawings remain the same shared 150-record bounded store; no per-chart duplicate drawing persistence. Chart settings add four small parameter records to existing layout snapshots; the 64,000-character snapshot and 12-snapshot library bounds remain. Chart teardown disposes drawing/order listeners, series and chart resources. No live subscriptions or order execution added.

Verification: all 27 isolated terminal tests pass after click-only selection changes. Coverage includes chart-body/tab activation, unchanged hover, ticket/watchlist routing, same-market draft preservation, cross-market reset, first-gesture protection for limit/stop/scale orders, drawing hotkey isolation, and legacy snapshot migration, alongside existing layouts and chart interactions. TypeScript, scoped lint, production build and visual inspection pass with existing build warnings. Changes remain local after `db455737`, with named-layout work; no commit or push.


## Compact chart header — 2026-10-30

Merged each chart toolbar into its Dockview header. Visible chart-number labels are replaced by a small drag grip while accessible tab names remain. Market selector, timeframe dropdown, indicator icon/menu, palette icon, and existing group actions occupy one 28px row. The indicator menu independently toggles EMA 20 and EMA 100; these two booleans persist in the existing chart parameters and named layouts. Older `showEma` parameters migrate to both flags without losing visibility preferences. No new storage, series or subscriptions; appearance changes still update existing series.

Verification: all 27 existing terminal tests passed after the header migration; the new independent-indicator/reload test and three affected docking/preset tests pass after final alignment cleanup. TypeScript, scoped lint, production build and four-chart/compact screenshot review pass. Existing route-export and bundle-size warnings remain. Changes are local and uncommitted; no backend or live operations.


Drawing context-menu verification: seven affected chart/drawing/order browser checks pass, including clear/cancel/empty-menu behavior, other-market preservation, reload persistence, shortcut deletion and unchanged ticket selection. TypeScript, scoped lint, production build and screenshot inspection pass. No new storage, backend work, commit or push.
