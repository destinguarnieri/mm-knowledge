# mm-knowledge

This is the version-controlled knowledge base for Money Machine Labs. Treat it as the durable agent-readable project memory: an Obsidian-compatible linked markdown wiki, indexed by QMD for search.

## Operating Model

- The **wiki graph** is the source of truth for synthesized durable knowledge.
- **QMD** is the retrieval/index layer over the markdown graph.
- **Linear** is the execution/backlog system, not the long-term context store.
- Built-in agent memory is only for compact global facts/preferences. Do not rely on it for project continuity.

Money Machine's operating objective is positive net realized live P&L after costs over the active founder-set proof period. Preserve durable context only when it helps close that revenue loop; documentation volume is not progress.

## Required Agent Flow

Before answering project/context questions or doing Money Machine work:

1. Start with `wiki/index.md` when it exists; use it as the routing map.
2. Use QMD for search when available:
   - `/Users/destinguarnieri/.bun/bin/qmd query "<question>"`
   - `/Users/destinguarnieri/.bun/bin/qmd search "<keyword>"`
   - `/Users/destinguarnieri/.bun/bin/qmd get "<path-or-docid>"`
3. If QMD is broken, sparse, or missing embeddings, use filesystem search/read tools directly.
4. Follow relevant `[[wikilinks]]` and backlinks instead of stopping at the first matching page.
5. Retrieve source pages before summarizing; do not answer from search snippets alone when precision matters.

After work that materially changes durable state:

1. Update an existing relevant page when possible; create a page only for reusable cross-session knowledge.
2. Update `wiki/sessions/current-checkpoint.md` only when the objective, state, decision, blocker, verification, or next action changed.
3. Append to `wiki/sessions/session-change-log.md` only for durable ticketing, implementation, verification, or product/engineering decisions.
4. Update `wiki/index.md` only when routing or page inventory changed.
5. Append to `wiki/log.md` only when KB structure changed.
6. Run `/Users/destinguarnieri/.bun/bin/qmd update` after KB edits, then `/Users/destinguarnieri/.bun/bin/qmd embed`. Treat these as one step: `update` re-indexes text, `embed` vectorizes it, and a document that is indexed but not embedded is invisible to `qmd query` even though `qmd search` can still find it. Skip `embed` only when it reports nothing pending.
7. Commit or push only when Destin explicitly authorized it for the current execution session.

If no durable state changed, close the loop without creating a page, changelog entry, index edit, commit, or push.

### Research continuity (metrics vs notes)

Persisted backtest `run_id` values are the metric source of truth. Destin's backtest UI is the default place for standard tables and metrics.

- Research wiki pages may record run IDs, experiment intent, fixed assumptions, interpretation, and decisions.
- Do not paste standard metric tables, per-asset result grids, or full MCP payloads into wiki, checkpoint, changelog, or canvas.
- Checkpoint and changelog are agent pickup aids. Keep them thin; do not use them as a metrics archive.
- Canvas is optional for a unique visual explanation Destin cannot get from the UI. It is not the default for ordinary batch/result tables.
- When numbers are needed again, re-fetch via Research MCP saved-run tools or open the UI.

## Structure

Canonical structure:

```text
AGENTS.md             # operating contract for agents
README.md             # human-readable repo overview
raw/                  # immutable or lightly-normalized source dumps
archive/              # deprecated or historical material kept out of canonical routing
scripts/              # maintenance scripts such as link checkers
wiki/                 # synthesized Obsidian-compatible markdown graph
  index.md            # routing map and page inventory
  log.md              # chronological KB operation log
  company/            # company context and narrative
  ops/                # operating procedures and process docs
  engineering/        # stable architecture, contracts, implementation context, invariants
  quant/              # quantitative research notes
  trading/            # strategy/research/trading concepts
  concepts/           # cross-cutting concepts and domain language
  decisions/          # decision records and supersession chains
  projects/           # active initiatives, project-level context, and bounded execution plans
  sessions/           # compact session summaries/checkpoints promoted from chat
  vendors/            # vendor specifications and documentation
                      # (named `vendors/` not `vendor/` — QMD hard-excludes dirs named `vendor`)
```

Canonical markdown belongs under `wiki/`. Do not keep duplicate top-level `company/`, `ops/`, `engineering/`, `research/`, or `trading/` markdown trees. If old/source material should be retained but not treated as canonical, move it under `archive/` or `raw/` with a note.

## Wiki Rules

- Any page covering in-progress work carries an explicit status line near the top: `Status: draft | in progress | confirmed | superseded`. A page with no status line is draft.
- `confirmed` means Destin confirmed the specific claim and considers it settled. Recording something Destin said once is `in progress` — a faithful transcript of a work-in-progress statement is still work in progress.
- Never imply maturity with a heading. Headings name the topic; the status line carries the confidence.
- Use Obsidian-style `[[wikilinks]]` for important relationships.
- Prefer stable, descriptive filenames.
- Keep pages concise but useful; split only when a page becomes hard to route or maintain.
- Raw sources belong in `raw/`; synthesized agent-readable knowledge belongs in `wiki/`.
- Keep `wiki/engineering/` for stable engineering knowledge: architecture, contracts, inventories, runbooks, and invariants. Do not create ticket or implementation-plan files there.
- Put bounded, active project or ticket execution plans in `wiki/projects/`; retain execution/backlog truth in Linear. After delivery, promote only durable conclusions to the relevant stable wiki page or decision record.
- Decision pages should say what changed, why, date, and superseded decisions if any.
- Session pages should capture objective, decisions, verification, blockers, next actions, and links to Linear/issues/PRs when relevant.

## QMD Notes

QMD repo: https://github.com/tobi/qmd

Useful commands:

```bash
/Users/destinguarnieri/.bun/bin/qmd status
/Users/destinguarnieri/.bun/bin/qmd update
/Users/destinguarnieri/.bun/bin/qmd embed
/Users/destinguarnieri/.bun/bin/qmd query "quarterly planning process"
/Users/destinguarnieri/.bun/bin/qmd search "API"
/Users/destinguarnieri/.bun/bin/qmd get "wiki/index.md"
/Users/destinguarnieri/.bun/bin/qmd search "authentication" --json -n 10
/Users/destinguarnieri/.bun/bin/qmd query "error handling" --all --files --min-score 0.4
```

There is one collection, `mm-knowledge`, covering the whole `wiki/` tree. It previously overlapped five per-topic collections rooted at subdirectories of the same tree, which double-indexed those files and let duplicate hits consume result slots; the topic collections were removed on 2026-07-25. Do not re-add a collection whose path sits inside another collection's path.

If search results look weak, check `qmd status` for pending embeddings first, then run `update` and `embed`, then inspect files directly before concluding knowledge is absent. `qmd query` is semantic and needs embeddings; `qmd search` is BM25 keyword and does not.
