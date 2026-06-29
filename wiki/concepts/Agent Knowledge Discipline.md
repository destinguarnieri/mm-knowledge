# Agent Knowledge Discipline

Agents working on Money Machine should not start from chat memory alone.

Related:
- [[index|Money Machine Knowledge Index]]
- [[Backtesting and Evaluation]]
- [[Money Machine Operating Context]]

## Source-of-Truth Stack

1. Current user direction.
2. Money Machine repo entrypoint: `mm_v04/AGENTS.md`.
3. Money Machine KB: `mm-knowledge/AGENTS.md`, `wiki/index.md`, and relevant linked wiki pages.
4. Linear for execution/backlog state.
5. QMD for search over the KB.
6. Built-in Hermes memory only for compact global facts/preferences.

## Required Session Flow

At session start or before meaningful work:

- Read the active repo `AGENTS.md`.
- Check `wiki/ops/current-checkpoint.md` and `wiki/ops/session-change-log.md`.
- Search or inspect this KB for relevant context.
- Retrieve source pages before summarizing or planning.

After meaningful work:

- Update repo checkpoint/changelog.
- Update relevant wiki pages when durable project knowledge changed.
- Run `qmd update` after KB edits.

## Anti-Patterns

- Treating memory as project truth.
- Answering from stale chat context when repo/KB docs exist.
- Creating Linear tickets without updating durable context when the ticket reflects a new product/engineering decision.
- Letting QMD search snippets replace reading actual pages.
