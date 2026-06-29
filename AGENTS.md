# mm-knowledge

This is the version-controlled knowledge base for Money Machine Labs. Treat it as the durable agent-readable project memory: an Obsidian-compatible linked markdown wiki, indexed by QMD for search.

## Operating Model

- The **wiki graph** is the source of truth for synthesized durable knowledge.
- **QMD** is the retrieval/index layer over the markdown graph.
- **Linear** is the execution/backlog system, not the long-term context store.
- Built-in Hermes memory is only for compact global facts/preferences. Do not rely on it for project continuity.

## Required Agent Flow

Before answering project/context questions or doing Money Machine work:

1. Start with `wiki/index.md` when it exists; use it as the routing map.
2. Use QMD for search when available:
   - `/Users/destinguarnieri/.bun/bin/qmd query "<question>"`
   - `/Users/destinguarnieri/.bun/bin/qmd search "<keyword>" -c <collection>`
   - `/Users/destinguarnieri/.bun/bin/qmd get "<path-or-docid>"`
3. If QMD is broken, sparse, or missing embeddings, use filesystem search/read tools directly.
4. Follow relevant `[[wikilinks]]` and backlinks instead of stopping at the first matching page.
5. Retrieve source pages before summarizing; do not answer from search snippets alone when precision matters.

After meaningful work:

1. Update or create the relevant page(s) under `wiki/`.
2. Update `wiki/ops/current-checkpoint.md` with objective, current state, decisions, blockers, verification, and next action.
3. Append a concise entry to `wiki/ops/session-change-log.md` after ticketing, implementation, verification, or durable product/engineering decisions.
4. Update `wiki/index.md` when routing, page inventory, or key topics change.
5. Append a concise KB-structure entry to `wiki/log.md` when the KB itself changes.
6. Run `/Users/destinguarnieri/.bun/bin/qmd update` so search reflects the new markdown.
7. Run `/Users/destinguarnieri/.bun/bin/qmd embed` only when semantic retrieval needs to include new material immediately.
8. Commit and push KB changes when appropriate, unless Destin says not to.

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
  engineering/        # architecture, implementation context, invariants
  quant/              # quantitative research notes
  trading/            # strategy/research/trading concepts
  concepts/           # cross-cutting concepts and domain language
  decisions/          # decision records and supersession chains
  projects/           # active initiatives and project-level context
  sessions/           # compact session summaries/checkpoints promoted from chat
```

Canonical markdown belongs under `wiki/`. Do not keep duplicate top-level `company/`, `ops/`, `engineering/`, `quant/`, or `trading/` markdown trees. If old/source material should be retained but not treated as canonical, move it under `archive/` or `raw/` with a note.

## Wiki Rules

- Use Obsidian-style `[[wikilinks]]` for important relationships.
- Prefer stable, descriptive filenames.
- Keep pages concise but useful; split only when a page becomes hard to route or maintain.
- Raw sources belong in `raw/`; synthesized agent-readable knowledge belongs in `wiki/`.
- Decision pages should say what changed, why, date, and superseded decisions if any.
- Session pages should capture objective, decisions, verification, blockers, next actions, and links to Linear/issues/PRs when relevant.

## QMD Notes

QMD repo: https://github.com/tobi/qmd

Useful commands:

```bash
/Users/destinguarnieri/.bun/bin/qmd status
/Users/destinguarnieri/.bun/bin/qmd update
/Users/destinguarnieri/.bun/bin/qmd query "quarterly planning process"
/Users/destinguarnieri/.bun/bin/qmd search "API" -c mm-engineering
/Users/destinguarnieri/.bun/bin/qmd get "wiki/index.md"
/Users/destinguarnieri/.bun/bin/qmd search "authentication" --json -n 10
/Users/destinguarnieri/.bun/bin/qmd query "error handling" --all --files --min-score 0.4
```

Use QMD collection contexts to improve retrieval quality. If search results look weak, check `qmd status`, run `qmd update`, and inspect files directly before concluding knowledge is absent.
