# Money Machine Knowledge Index

Purpose: routing map for Money Machine's agent-readable knowledge graph. Agents should start here, then follow Obsidian-style wikilinks and use QMD search when exact routing is unclear.

## Core Pages

- [[Money Machine Operating Context]] — durable company/system/project frame.
- [[Agent Knowledge Discipline]] — how agents should use the wiki, QMD, Linear, checkpoints, and changelogs.
- [[Backtesting and Evaluation]] — backtest/research loop, correctness issues, and evaluation tooling.
- [[MON-97-backtest-metrics-plan]] — implementation plan for excluding fee-only/no-trade rows from backtest win-rate accounting.

## Wiki Areas

Canonical markdown lives under `wiki/`:

- `wiki/company/` — company overview, 360 context, narrative.
- `wiki/agents/templates/` — reusable agent, worker, and coding-manager prompt templates for Money Machine execution.
- `wiki/ops/` — operating runbooks, process notes, Linear operating system.
- `wiki/engineering/` — engineering plans, architecture, implementation context.
- `wiki/quant/` — quantitative research notes.
- `wiki/trading/` — trading language and discretionary/strategy context.
- `wiki/concepts/` — cross-cutting domain concepts and agent procedures.
- `wiki/projects/` — active initiative context and project-level synthesis.
- `wiki/decisions/` — durable decision records.
- `wiki/sessions/` — promoted session summaries.

## Routing Rules

- For current execution state, check `wiki/ops/current-checkpoint.md` and `wiki/ops/session-change-log.md`.
- For execution/backlog truth, check Linear.
- For durable project synthesis, update this wiki.
- For broad retrieval, use QMD over the wiki, then retrieve the matching markdown pages before answering.

## Open Maintenance

- Add backlinks and related links as pages stabilize.
- Add QMD collection context descriptions after the core wiki skeleton settles.
- Use `scripts/check_wikilinks.py` to verify links after wiki edits.
