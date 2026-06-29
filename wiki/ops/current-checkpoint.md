# Current Checkpoint

Date: 2026-06-28 22:26 EDT

## Current State

Session focus shifted from immediate backtesting execution to fixing agent operating continuity first. The practical decision:

- Use `mm-knowledge` as the durable Money Machine agent knowledge base.
- Treat it as an Obsidian-compatible linked markdown wiki.
- Use QMD as the indexed search/retrieval layer over that wiki.
- Use prompts/repo instructions to enforce KB, checkpoint, and changelog hygiene.
- Keep external memory providers as optional ambient recall later, not canonical project truth.

## Completed This Session

- Created Linear tickets for backtesting complaints/bugs:
  - MON-97 — fee-only/no-trade rows excluded from win-rate accounting.
  - MON-98 — position sizing behavior explicit/testable.
  - MON-99 — raw/transformed/flat/EPS signal semantics.
  - MON-100 — >2,000 bar fetch pagination and completeness checks.
  - MON-101 — signal/warmup UX clarity.
- Fixed local QMD native module mismatch by reinstalling `@tobilu/qmd@2.5.3` with Bun.
- Verified QMD runs and `qmd update` indexes the KB.
- Patched `~/.hermes/SOUL.md` with global knowledge/continuity discipline.
- Patched `mm_v04/AGENTS.md` with Money Machine KB and session hygiene requirements.
- Rewrote `mm-knowledge/AGENTS.md` into an operating contract for wiki + QMD.
- Initialized and reorganized `mm-knowledge/wiki/` as the canonical KB home. Top-level category docs were moved under `wiki/` to avoid duplicate markdown trees.
- Created `moneymachine-knowledge-base` Hermes skill for this exact wiki/QMD workflow.
- Added `mm-knowledge/scripts/check_wikilinks.py` and verified wiki links resolve.
- Current `mm-knowledge/wiki/` spine includes:
  - `wiki/index.md`
  - `wiki/log.md`
  - `wiki/company/overview.md`
  - `wiki/company/money-machine-360.md`
  - `wiki/ops/current-checkpoint.md`
  - `wiki/ops/session-change-log.md`
  - `wiki/ops/linear-operating-system.md`
  - `wiki/ops/research-mcp-runbook.md`
  - `wiki/concepts/Agent Knowledge Discipline.md`
  - `wiki/projects/Backtesting and Evaluation.md`
  - `wiki/projects/Money Machine Operating Context.md`

## Current Truth

Canonical continuity stack:

1. Explicit user direction.
2. `mm_v04/AGENTS.md` for repo-local safety and entrypoint instructions.
3. `/Users/destinguarnieri/Desktop/codebase/mm-knowledge/AGENTS.md` and `wiki/index.md` for KB operating discipline.
4. `mm-knowledge/wiki/ops/current-checkpoint.md` and `mm-knowledge/wiki/ops/session-change-log.md` for continuity.
5. Linear for execution/backlog truth.
6. QMD for indexed retrieval over the KB.
7. Built-in Hermes memory only for compact global facts/preferences.

## Known Open Items

- `mm-knowledge` has untracked/moved files and should be cleaned/committed intentionally.
- QMD reports pending embeddings; run `qmd embed` when semantic retrieval should be fully online.
- Add QMD collection contexts for better retrieval.
- Consider a Hermes cron job for ambient KB/checkpoint hygiene after the prompt/file discipline settles.
- External memory provider decision deferred; likely bakeoff Honcho vs Holographic only if Wiki+QMD+cron leaves a gap.

## Next Recommended Actions

1. Verify the prompt/KB hygiene changes are acceptable.
2. Optionally run `qmd embed` and add collection contexts.
3. Clean/commit `mm-knowledge` changes.
4. Resume backtesting work, likely starting with MON-98 or whichever ordering Destin decides.
