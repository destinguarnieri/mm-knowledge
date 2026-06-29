QMD knowledge base repo is located at /Users/destinguarnieri/Desktop/codebase/mm-knowledge.
§
qmd CLI is installed locally at /Users/destinguarnieri/.bun/bin/qmd and is usable from the mm-knowledge repo.
§
For mm-knowledge, Hermes has read/write permission. After changing files in that repo, commit and push to GitHub by default unless Destin says otherwise.
§
Linear workspace available to Destin includes team Money Machine with key MON.
§
Destin wants Linear optimized for company ops and dev for himself, Hermes, and future agents; not a user-facing product cycle.
§
Linear MON team now uses states Triage, Backlog, Ready, In Progress, Blocked, Done, Canceled with labels grouped under Area, Codebase, Type, and Exec.
§
Linear operating process doc is stored in mm-knowledge at ops/linear-operating-system.md.
§
Money Machine Labs is an internal prop trading and research company trading only its own capital; no external users or fund investors.
§
Immediate strategic bottleneck: backtest/research loop is too slow; Destin wants agentic flows to compress review-tweak-repeat cycles to seconds/minutes.
§
Money-path/core trading infra is sensitive and human-judgment-heavy; Destin wants only light agentic coding there, with Hermes more as operator/manager than autonomous code swarms.
§
Near-term goals: within 30 days get two strategies into production, run one 24/7 agentic backtest loop, and train one quantile regression model for forward percent change.
§
Money Machine 360 context doc is stored in mm-knowledge at company/money-machine-360.md.
§
Top priority: fast backtest loop. research_mcp is separate root service: never live trading, no batch or signal deciles in v1, minimal loop only. Long-term: avoid backend imports in MCP startup/build code; use backend over HTTP.
§
PUSH PENDING: feat/backtest (mm_v04) + mm-knowledge main timed out 2026-03-19. Push both at session start.
§
Primary trading system codebase appears to be at /Users/destinguarnieri/Desktop/codebase/mm_v04.
§
mm_v04 now has future-agent docs under /Users/destinguarnieri/Desktop/codebase/mm_v04/docs/agents, and CLAUDE.md points agents there first.