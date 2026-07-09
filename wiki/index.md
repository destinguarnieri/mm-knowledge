# Money Machine Knowledge Index

Purpose: routing map for Money Machine's agent-readable knowledge graph. Agents should start here, then follow Obsidian-style wikilinks and use QMD search when exact routing is unclear.

## Core Pages

- [[Money Machine Operating Context]] — durable company/system/project frame.
- [[Agent Knowledge Discipline]] — how agents should use the wiki, QMD, Linear, checkpoints, and changelogs.
- [[Backtesting and Evaluation]] — backtest/research loop, correctness issues, and evaluation tooling.
- [[research/trading/research_process_v1|Research Process V1]] — repeatable quant strategy research protocol from idea card through candidate handoff.
- [[research/trading/example_research_directory/example_research_doc|Example Research Doc]] — style reference for structured research files with timestamped write logs.


## Wiki Areas

Canonical markdown lives under `wiki/`:

- `wiki/company/` — company overview, 360 context, narrative.
- `wiki/agents/templates/` — reusable agent, worker, and coding-manager prompt templates for Money Machine execution.
- `wiki/ops/` — operating runbooks, process notes, Linear operating system.
- `wiki/engineering/` — engineering plans, architecture, implementation context.
- `wiki/quant/` — quantitative research notes.
- `wiki/research/trading/` — strategy research protocol and per-project research docs (`research_process_v1`, example research directory).
- `wiki/trading/` — trading language and discretionary/strategy context.
- `wiki/concepts/` — cross-cutting domain concepts and agent procedures.
- `wiki/projects/` — active initiative context and project-level synthesis.
- `wiki/decisions/` — durable decision records.
- `wiki/sessions/` — promoted session summaries and current checkpoint / change log.

## Routing Rules

- For current execution state, check `wiki/sessions/current-checkpoint.md` and `wiki/sessions/session-change-log.md`.
- For execution/backlog truth, check Linear.
- For durable project synthesis, update this wiki.
- For broad retrieval, use QMD over the wiki, then retrieve the matching markdown pages before answering.

## Open Maintenance

- Add backlinks and related links as pages stabilize.
- Add QMD collection context descriptions after the core wiki skeleton settles.
- Use `scripts/check_wikilinks.py` to verify links after wiki edits.
