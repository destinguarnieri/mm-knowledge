# mm-knowledge

Money Machine Labs' durable project knowledge: an Obsidian-compatible markdown wiki indexed by QMD. Use relevant pages for continuity; verify implementation claims against the current code.

## Retrieve only what the task needs

Start from Destin's current request. `wiki/index.md` is an optional directory, not required reading. Do not load the index, goals, checkpoint, and changelog as a startup bundle.

- Planning or prioritization: read `wiki/goals.md` for desired outcomes and completion criteria.
- Resuming work: read the relevant section of `wiki/sessions/current-checkpoint.md` and its linked project page.
- Architecture, behavior, or procedures: search QMD for the specific question, then read the matching source pages. Follow links only when needed to resolve the question.
- Past decisions or verification: search `wiki/sessions/session-change-log.md`; do not read the full log by default.
- Use filesystem search/read tools when the path is known or QMD results are stale, sparse, or unavailable. Search snippets alone are not enough when precision matters.

## Goals, state, and history

- `wiki/goals.md` records forward-looking outcomes selected by Destin, their priority, and what counts as done. Keep it short; link to project detail and Linear rather than copying a backlog.
- `wiki/sessions/current-checkpoint.md` records where relevant work stands, verification, blockers, and the next pickup action. Replace superseded state for the same topic instead of stacking progress reports.
- `wiki/sessions/session-change-log.md` records material changes and decisions over time.
- Domain pages hold reusable knowledge; `wiki/projects/` holds bounded project plans. Linear remains the execution/backlog system.
- A goal is direction, not authorization for live operations, implementation, or a new task. Do not infer priorities from old checkpoint, ticket, or project labels. Record proposed goals as proposals until Destin selects them.
- Do not rely on built-in agent memory or chat history for project continuity.

Money Machine's operating objective is positive net realized live P&L after costs over the active founder-set proof period. Preserve context when it helps that objective; documentation volume is not progress.

## Historical boundary and safety

Destin reset the research agenda on **2026-10-06**. No pre-reset program, hypothesis, experiment, review request, or ticket carries forward as an active commitment. This boundary supersedes historical agenda/process instructions elsewhere in this repo.

- Do not auto-resume or repopulate work from old active/ready/in-progress/next-action labels, including Linear and session logs.
- Retrieve older evidence only when relevant; preserve its limitations and verify current implementation claims. Historical reading and reconciliation are not prerequisites for new work.
- Only Destin's explicit selection activates a research focus. Record the selected outcome in goals and relevant research/project context, with pickup state in the checkpoint, without reviving unrelated obligations.
- Existing external tickets remain unchanged until explicitly addressed. Live/capital authorization, correctness, and evidence-integrity constraints remain in force; follow `mm_v04/AGENTS.md` for code and runtime work.

## Maintain only material changes

1. Update the relevant existing page; create a page only for reusable cross-session knowledge.
2. Update goals only when Destin selects, changes, completes, or drops an outcome. Update checkpoint state only for affected work. Do not duplicate detailed evidence across them. Keep checkpoint and changelog each under roughly 100 lines; archive older detail with a concise routing summary, preserving run IDs, decisions, and verification limits. Archive history stays outside QMD.
3. Add a brief changelog entry for durable implementation, verification, ticketing, or product/engineering decisions. Link to detail.
4. Change the index only when a stable navigation destination changes. Keep project status, current focus, and individual implementation references out of it.
5. Check changed links. Run `/Users/destinguarnieri/.bun/bin/qmd update`, then `/Users/destinguarnieri/.bun/bin/qmd embed` to refresh text and semantic retrieval. Report any incomplete refresh.
6. Commit or push only when Destin explicitly authorizes it for the current execution session.

If no durable state changed, do not create a page, changelog entry, or other continuity edit.

## Page conventions

- Canonical Markdown belongs in `wiki/`; sources in `raw/`; historical/deprecated material in `archive/`. Do not create duplicate top-level topic trees.
- Pages covering in-progress work carry `Status: draft | in progress | confirmed | superseded` near the top. Missing status means draft. `confirmed` means Destin explicitly confirmed the specific claim as settled; merely transcribing a statement does not confirm it.
- Use descriptive filenames and Obsidian-style wikilinks for important relationships. Keep pages concise; headings name topics, status lines carry confidence.
- `wiki/engineering/` holds stable architecture, contracts, inventories, runbooks, and invariants. Put active execution plans in `wiki/projects/`; after delivery, promote durable conclusions to domain pages or decision records.
- Decision records capture what changed, why, date, and supersession. Checkpoints capture current state and links, not a second chronology.
- Vendor specifications belong in `wiki/vendors/`, not `vendor/` (QMD excludes directories named `vendor`).

## Research continuity

Follow `mm_v04/.cursor/rules/research-continuity.mdc` when running Research MCP or writing research notes. Persisted backtest `run_id` values are the metric source of truth; the backtest UI is the default for standard tables and metrics.

- Record run IDs, intent, fixed assumptions, interpretation, and decisions in research notes.
- Do not paste standard metric tables, per-asset grids, or full MCP payloads into wiki, checkpoint, changelog, or canvas. Re-fetch numbers through saved-run tools or the UI.
- Use canvas only when a unique visual explanation helps; it is optional.

## QMD

Use the QMD tools when available, or `/Users/destinguarnieri/.bun/bin/qmd`:

- `search "<keywords>" -c mm-knowledge` for lexical lookup; `query "<question>" -c mm-knowledge` for semantic retrieval; `get "<path-or-docid>"` to read a source.
- `mm-knowledge` indexes `wiki/`; `mm-raw` indexes `raw/`. Raw hits are third-party or draft material, not confirmed Money Machine practice. Synthesize and explicitly qualify them in the wiki before treating them as durable project knowledge.
- `archive/` stays unindexed. Do not create collections nested within another collection's path; overlapping collections duplicate results.
- For weak results, inspect `status` and pending embeddings, refresh with `update` and `embed` as needed, then check files directly before concluding knowledge is absent.

QMD does not validate wikilinks. Use `python3 scripts/check_wikilinks.py` for local Markdown/wiki links, attachments, and heading checks. Pass repo-relative archive paths to check changed historical material too; code examples are ignored and remote URLs are not fetched.
