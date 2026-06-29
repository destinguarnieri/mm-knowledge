# Session Change Log

## 2026-06-28 22:26 EDT

- Created Linear tickets MON-97 through MON-101 for backtesting correctness/UX issues from Destin's backtester complaint list.
- Fixed QMD local install mismatch by reinstalling `@tobilu/qmd@2.5.3` with Bun; verified `qmd status`, `qmd update`, and keyword search work.
- Decided operating model: Money Machine KB is an Obsidian-compatible linked markdown wiki; QMD is indexed search/retrieval over it; prompts enforce discipline/hygiene.
- Patched `~/.hermes/SOUL.md` with global knowledge/continuity discipline.
- Patched `mm_v04/AGENTS.md` with Money Machine KB usage, checkpoint, and changelog requirements.
- Rewrote `/Users/destinguarnieri/Desktop/codebase/mm-knowledge/AGENTS.md` as the KB operating contract.
- Initialized `/Users/destinguarnieri/Desktop/codebase/mm-knowledge/wiki/` with index/log and core context pages.
- Updated canonical checkpoint path: `/Users/destinguarnieri/Desktop/codebase/mm-knowledge/wiki/ops/current-checkpoint.md`.
- Reorganized `/Users/destinguarnieri/Desktop/codebase/mm-knowledge` so canonical category markdown lives under `wiki/` instead of duplicate top-level category folders.
- Moved historical prompt dumps to `archive/prompts_DUMP/` and pointed QMD collections at `wiki/` paths.
- Added `scripts/check_wikilinks.py`; verified current wiki links with `missing=0` and `ambiguous=0`.
- Created Hermes skill `moneymachine-knowledge-base` for Money Machine wiki/QMD workflow.
- Redirected repo prompt/changelog discipline away from `mm_v04/docs/work/*` and into the KB paths under `mm-knowledge/wiki/ops/`.
