# Research MCP Reference

Status: confirmed

The maintained Research MCP instructions live beside the implementation in `mm_v04/research_mcp/`:

- [Operational runbook](../../../mm_v04/research_mcp/doc/runbook.md) — call sequence, request examples, retention, and troubleshooting.
- [Agent guide](../../../mm_v04/research_mcp/AGENT.md) — research-only boundary, tool usage, and continuity rules.
- [Tool registration](../../../mm_v04/research_mcp/research_mcp/tools/registry.py) and [policy allowlist](../../../mm_v04/research_mcp/research_mcp/policy/allowlist.py) — inspect the implementation if documentation and available tools disagree.

Keep operational examples and tool catalogs there; this page is only a routing reference. Research MCP does not expose live trading controls. Live runtime operations remain subject to the repo's explicit authorization rules.


## Chart snapshot storage

Destin requested that operational snapshot rules live in the MCP runbook. Use its
[browser-free snapshot workflow](../../../mm_v04/research_mcp/doc/runbook.md#browser-free-chart-snapshots)
for `render_backtest_snapshot`, configuration, verified strategy identity, PNG/receipt
storage, compression, and retention. The tool is implemented and verified through the refreshed MCP connection. Detailed operating rules are maintained there, not duplicated here.

The retained prototype for run `d7cfc05b-32d8-44d8-93b4-08a7ac9e0723` remains under
`research/trading/opposite_bid_trend/images/`; the new tool does not migrate or remove it.
