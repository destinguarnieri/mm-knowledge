# Agentic Research Loop Product Brief

Status: in progress

Decision date: 2026-08-05

Related: [[research/trading/agentic_research_playbook|Agentic Research Playbook]] · [[research/trading/research_process_v2|Research Process V2]] · [[research/trading/research_index|Research Board]]

## Product frame

The research agent is the customer.

The product exists to let one agent take one bounded research question through reproducible execution, numerical inspection, visual diagnosis, an evidence-backed improvement insight, and durable closeout without requiring Destin to operate research tools.

The first product objective is not continuous autoresearch, a universal research UI, a generic scheduler, or a replacement backtest persistence model. It is to give agents reliable evidence access and perception so they can complete the existing research loop.

## Confirmed product policy

- **MCP is the autonomous research interface.** Agents discover, extract, and render evidence through typed tools.
- **The browser UI is human-only for this workflow.** Autonomous agents do not use Browser Use as a fallback. Browser access is allowed only when Destin explicitly requests UI inspection or when the UI itself is under test.
- **The UI need not represent every research type.** Event studies, forecasting, mapping tests, and other analyses may produce typed research-run artifacts without a dedicated frontend.
- **Signal-deciles is not the foundation.** It remains a specialized saved analysis; new generic research infrastructure must not extend its type-specific persistence or UI.
- **Generated evidence never lives in source packages.** Research code and generated run artifacts have separate homes.
- **Evidence permissions are enforced by tools.** Discovery, validation, and protected-holdout boundaries are not merely prompt instructions.
- **Structured evidence precedes pixels.** Agents can inspect bounded numerical series as well as rendered charts; chart images are not the only data interface.

## Observed customer evidence

The previous Agentic Research Loop project was parked until manual work demonstrated a real throughput bottleneck. That condition is now satisfied:

- one VWAP workstream consumed several hours of Destin-supervised agent work;
- Browser Use is slow and token-intensive;
- the backtest UI cannot represent event studies and other research types;
- the playbook requires chart review and core-time-series mining, but agents lack one uniform tool surface for those steps;
- event-study outputs were written beneath `backend/app/lib/analysis/`, producing roughly 312 MB across 355 Git-tracked generated files; and
- parallel research tempo is limited when Destin must mediate inspection or agents invent output paths and formats.

## Existing substrate

Do not rebuild capabilities that already exist:

- persisted backtests already have durable run IDs and full-retention artifacts;
- Research MCP now exposes `list_saved_run_series` and `get_saved_run_series`, providing discoverable and bounded signal/indicator access for saved backtests;
- the backend already includes Plotly, Matplotlib, and Pillow; and
- the human backtest UI remains useful to Destin.

The product should generalize these useful primitives to research runs without redesigning the backtest database first.

## First vertical slice

Use the EMA 10/200 event study as the first reference integration.

The acceptance journey is:

```text
run event study
→ receive research_run_id
→ describe available evidence
→ extract bounded aligned series
→ render diagnostic charts
→ preserve structured annotations
→ identify what is working and not working
→ derive one improvement insight
→ return a Research Process V2 decision
```

The slice passes only when an agent completes that journey without Browser Use, arbitrary output directories, or Destin operating the tools.

## Research-run artifact contract

Generated runs use an ignored workspace outside application source:

```text
.research/runs/
  <research_type>/
    <research_run_id>/
      manifest.json
      summary.json
      data/
      figures/
      annotations.json
      logs/
```

Minimum `manifest.json` fields:

- schema version;
- research run ID and research type;
- originating research thread and Linear issue when present;
- source backtest, model, dataset, or parent run IDs;
- code commit/version and configuration;
- data lineage, asset/universe, interval, and requested/actual windows;
- discovery/validation/holdout role and permitted evidence windows;
- cost assumptions and random seed when applicable;
- status, timestamps, warnings, and failure reason;
- artifact inventory with type, path, checksum, and retention class; and
- available numerical series and renderable panels.

The manifest is an outer contract. Each research type may retain typed domain-specific tables and metadata beneath it.

## Agent tool surface

### `describe_run`

Given a research run ID, return:

- research type, status, provenance, and evidence role;
- actual and permitted time windows;
- assets and intervals;
- available candles, numerical series, indicators, components, and panels;
- available summaries and artifacts;
- valid rendering options; and
- warnings or blocked evidence surfaces.

Agents call this before guessing names or requesting evidence.

### `extract_window`

Given a research run ID, bounded time window, selected series, and optional asset, return aligned machine-readable points with truncation and actual-window metadata.

Requirements:

- filtering happens before the MCP response;
- point and response-size limits are bounded;
- unknown series/components fail explicitly;
- evidence permissions apply before data is returned; and
- the response identifies missingness, alignment, and truncation behavior.

The existing saved-backtest series tools are the backtest-specific precursor to this contract.

### `render_chart`

The agent supplies a declarative configuration such as:

```json
{
  "run_id": "...",
  "asset_id": "...",
  "start_timestamp": 0,
  "end_timestamp": 0,
  "width": 1800,
  "height": 1200,
  "candles": {"visible": true, "color_mode": "neutral"},
  "show_avg_price": true,
  "indicators": {
    "ema_10": {"visible": true},
    "ema_200": {"visible": true}
  },
  "panels": [
    {"id": "signal", "series": ["signal.raw"]},
    {"id": "position", "series": ["position", "avg_price"]},
    {"id": "performance", "series": ["roe", "net_pnl"]}
  ],
  "annotations": []
}
```

The response returns:

- render ID and research run ID;
- image artifact reference;
- normalized configuration and config hash;
- requested and actual windows;
- rendered and skipped series;
- warnings; and
- artifact path and checksum.

Rendering is deterministic for the same run data, normalized configuration, and renderer version. Configs cannot contain arbitrary filesystem paths or executable plotting code.

### Structured annotations

Annotations remain data, not only burned pixels. An annotation identifies its type, timestamp or region, optional value/panel/series, label, interpretation state, and creator. Renderers may produce annotated PNGs from this source.

## Evidence access

`describe_run`, `extract_window`, and `render_chart` share one authorization boundary:

- discovery and authorized validation surfaces may be inspected;
- protected holdout metadata may be acknowledged without exposing values;
- attempts to extract or render protected windows fail before reading or rendering data; and
- authorized one-time holdout use is recorded against the research thread/candidate.

The first slice may use a manifest-backed evidence policy. It must not claim universal holdout enforcement beyond integrated research types.

## Implementation sequence

1. Establish the artifact workspace, manifest types, path resolver, and safe future-output behavior.
2. Adapt the event study to create a research run and implement `describe_run` plus `extract_window` for it.
3. Implement deterministic `render_chart` and structured annotations.
4. Enforce evidence permissions across all three tools.
5. Run the event-study acceptance journey and record the observed next bottleneck.

Existing tracked event-study outputs require a separate preservation/removal decision before destructive cleanup. New runs must stop adding to the source tree immediately; no worker may silently delete the existing output set.

## Explicitly deferred

- Karpathy-style continuous autoresearch or self-modifying optimization;
- generic research-process state machines;
- durable parameter-grid scheduling;
- automated promotion scoring;
- Research MCP ownership of KB Markdown files;
- a universal human research UI;
- extension of signal-deciles persistence;
- Study/Variant/Trial/Attempt backtest persistence replacement; and
- live deployment or capital mutation.

## Product success measures

The first slice succeeds when:

- one agent completes the event-study loop without Browser Use;
- no generated output is written under application source;
- every conclusion links to a reproducible research run and review artifacts;
- protected evidence cannot be retrieved or rendered accidentally;
- Destin is asked only for unresolved semantics, evidence authorization, or the resulting decision; and
- the attempt identifies the next product bottleneck from observed use rather than speculation.

## Linear execution

Execution belongs in the re-scoped [Agentic Research Loop](https://linear.app/money-machine/project/agentic-research-loop-176aff6d7aac) project. Historical cancelled issues remain historical; new issues are derived from this vertical slice rather than reopened wholesale.

- [MON-177](https://linear.app/money-machine/issue/MON-177/establish-research-run-artifact-workspace-and-contain-event-study) — **Done:** typed artifact workspace and manifest contract, future EMA event-study containment, explicit evidence-role input, failed-run manifests, checksummed inventories, and registered compression figures.
- [MON-178](https://linear.app/money-machine/issue/MON-178/expose-event-study-describe-run-and-bounded-extract-window-through) — **Blocked by MON-177:** event-study `describe_run` and bounded `extract_window`.
- [MON-179](https://linear.app/money-machine/issue/MON-179/add-declarative-render-chart-and-structured-annotations-for-research) — **Blocked by MON-177/178:** deterministic `render_chart` and structured annotations.
- [MON-180](https://linear.app/money-machine/issue/MON-180/enforce-discovery-validation-and-holdout-permissions-across-research) — **Blocked by MON-178/179:** evidence-permission enforcement across the read surface.
- [MON-181](https://linear.app/money-machine/issue/MON-181/prove-the-ema-event-study-alpha-loop-end-to-end-without-browser-use) — **Blocked by MON-177–180:** end-to-end product acceptance.
- [MON-182](https://linear.app/money-machine/issue/MON-182/decide-preservation-and-cleanup-of-legacy-tracked-event-study-outputs) — **Human blocked:** preservation/removal decision for the existing tracked output set.
