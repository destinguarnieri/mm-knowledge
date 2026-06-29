# mm-knowledge

Version-controlled knowledge base for Money Machine Labs.

This repo is an agent-readable, Obsidian-compatible markdown wiki with QMD indexing/search over it.

## Canonical Structure

```text
AGENTS.md             # operating contract for agents
README.md             # this overview
raw/                  # immutable or lightly-normalized source dumps
archive/              # historical/deprecated material, not canonical routing
scripts/              # maintenance scripts
wiki/                 # canonical linked markdown graph
  index.md            # start here: routing map and page inventory
  log.md              # chronological KB operation log
  company/            # company context and narrative
  ops/                # operating procedures and process docs
  engineering/        # architecture and implementation context
  quant/              # quantitative research notes
  trading/            # strategy/research/trading concepts
  concepts/           # cross-cutting concepts and domain language
  decisions/          # decision records and supersession chains
  projects/           # active initiatives and project context
  sessions/           # promoted session summaries/checkpoints
```

Canonical markdown belongs under `wiki/`. Avoid duplicate top-level category folders.

## How to Use

1. Read `AGENTS.md` for the operating contract.
2. Start navigation from `wiki/index.md`.
3. Follow Obsidian-style `[[wikilinks]]` for graph traversal.
4. Use QMD for search/retrieval when exact routing is unclear.

## QMD

QMD binary:

```bash
/Users/destinguarnieri/.bun/bin/qmd
```

Common commands:

```bash
/Users/destinguarnieri/.bun/bin/qmd status
/Users/destinguarnieri/.bun/bin/qmd update
/Users/destinguarnieri/.bun/bin/qmd query "backtesting correctness"
/Users/destinguarnieri/.bun/bin/qmd search "Linear" -c mm-ops
/Users/destinguarnieri/.bun/bin/qmd get "wiki/index.md"
```

QMD indexes the wiki and archived/supporting markdown. It does not validate wikilinks; use the link checker for that.
