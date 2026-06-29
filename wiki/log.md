# Money Machine Knowledge Log

Chronological log of meaningful KB changes. Keep entries concise and link changed pages.

## 2026-06-28

- Redirected session continuity from `mm_v04/docs/work/*` to `wiki/ops/current-checkpoint.md` and `wiki/ops/session-change-log.md` so the repo `docs/` tree can be removed without losing agent continuity.
- Restored the trading language dictionary into `wiki/trading/money-machine-language.md` and updated `mm_v04/AGENTS.md` to point there.
- Moved category docs into canonical `wiki/` subfolders: `wiki/company/` and `wiki/ops/`.
- Removed duplicate top-level category trees and moved historical prompt dumps to `archive/prompts_DUMP/`.
- Added `scripts/check_wikilinks.py` and verified current wiki links resolve.
- Initialized `wiki/` graph spine and clarified operating model: wiki graph is durable context, QMD is retrieval/index over it, Linear is execution truth.
- Added/updated: [[index|Money Machine Knowledge Index]], [[Agent Knowledge Discipline]], [[Backtesting and Evaluation]], [[Money Machine Operating Context]].
- Follow-up: add QMD collection contexts and continue promoting active docs into linked wiki pages as they are used.
