# Research Process V1

> **Superseded by [[research/trading/research_process_v2|Research Process V2]] (2026-07-23).** V2 restructures this into a lane router + evidence ladder, splits signal validity from monetization, adds symmetric kill/upside framing, dual (realistic + stress) costs, and cross-market generalization. This page is retained for history and for existing links; use V2 for current work.

Purpose: make strategy research repeatable enough that a good idea can be tested, improved, rejected, or promoted without drifting into unconstrained parameter chasing.

## Route the work first

Money Machine currently has two distinct strategy paths:

- **Discretionary strategy codification:** use when Destin already trades the strategy. Extract the exact visual and control semantics, preserve independently deployable mappings, and prove behavioral parity before optimization. Destin's source strategy is the specification; unresolved material semantics return to him instead of being guessed.
- **Exploratory research:** use for explicit discovery, open empirical questions, or bounded uncertainty exposed during codification.

This document's idea-triage and optimization process applies directly to exploratory research. For a discretionary strategy, begin here only after a faithful executable baseline exists. Treat the original manual behavior and any later optimized variant as distinct strategy identities so performance cannot silently redefine the source strategy.

Before starting a new research project, create a research folder:

`/mm-knowledge/wiki/research/trading/[research-name]/`

The folder name should describe the research topic, not the temporary config being tested.

Then create the core research doc inside it:

`/mm-knowledge/wiki/research/trading/[research-name]/[research-name].md`

Use [[research/trading/example_research_directory/example_research_doc|Example Research Doc]] as the style reference for structured sections plus timestamped write logs.

Structure the rest of the folder as:

- `configs/` — exact strategy/trade config snapshots for every cited run, one file per config;
- `artifacts/[run-id]/` — exported grid/summary tables, and chart packs for that run or batch, keyed by its backend run ID;
- `review/` — artifact review notes and rejection writeups referenced from the write log or run registry.

Create the folder and its core doc together during idea triage, before baselines start, so every later section has somewhere reviewable to link into. Do not let artifacts accumulate loose under `research/` without a research-name folder to own them.

Every research doc must keep a run registry. A reader should be able to trace any claim back to run IDs, saved-run links, configs, artifacts, charts, and review notes. Run IDs are the backend's UUID `run_id` for saved single runs and saved batches (from the backtest run/save response, the saved-run list, or Research MCP `get_saved_run` / `get_saved_run_asset`) — copy the real UUID, do not invent a label. Each entry must record the backend commit or engine version (and seed where randomness is involved) so the run stays reproducible after the backtest engine changes.

The registry is an identity and interpretation index, not a second metrics database. Prefer: run ID, config pointer, window/cohort intent, and a short decision note. Do not paste standard metric tables or per-asset Sharpe/drawdown grids into the research doc, checkpoint, changelog, or canvas — those live in Destin's backtest UI and in persisted saved runs. Re-fetch metrics when needed. Canvas is optional only for a unique visual explanation the UI does not already provide.

The registry must also track the cumulative number of configs evaluated across the whole research project. Every interpretation step should weigh the leaderboard against that count: the best of two thousand runs looks good by construction.

## 1. Idea Triage

Every strategy gets a one-page research card before optimization starts.

Required fields:

- Strategy idea.
- Edge hypothesis: what market behavior should create edge?
- Asset universe and timeframes.
- Entry logic.
- Exit logic.
- Risk, sizing, leverage, fee, and slippage assumptions.
- Data split: a discovery range, a validation range, and an untouched holdout. Fix these before the first grid. The holdout is consumed exactly once, at the promotion gates.
- Market period / regime definition: how time will be segmented when checking period dependence and regime sanity (calendar segments or pre-defined vol/trend labels). Define the segmentation before the first grid so it cannot be chosen after seeing results.
- Core knobs: parameters that express the strategy idea.
- Incidental knobs: implementation details that should not define the edge.
- Expected risks and tripwires: fees, churn, regime dependence, low trade count, tail risk, overfit, or poor capacity.
- Initial kill criteria: the hard conditions that reject a config or the whole idea regardless of headline return, for example fee-stressed net return below zero, a drawdown floor, a minimum trade count, single-segment dependence, or an isolated top config with failing neighbors. These are the only numeric reject thresholds the process keeps; there is no separate guardrail list.

Example:

- Edge: trend-following strategy that enters during trend continuation and exits on trend reversal.
- Timeframes: 15m, 30m, 1h, 4h.
- Core knobs:
  - time-based signal window search;
  - entry/exit threshold search;
  - optional volatility filter or sizing adjustment.
- Expected risks and tripwires:
  - gets chopped up during non-trending regimes;
  - net performance disappears after fee/slippage stress;
  - best config depends on one lucky segment.

Do not start by asking, "Which params win?" Start by asking, "What behavior would prove or disprove the edge?"

## 2. Define Optimization Objective

Write the objective before running a broad grid.

- Use exactly one primary target, such as maximizing net Sharpe or net return after fees and slippage.
- Define the metrics precisely enough that runs stay comparable across research docs: what return series Sharpe is computed on, what counts as a trade, how fee drag is measured.
- Keep an objective-change log in the research doc. If the objective changes later, the change must be written down, not applied silently.

Do not keep a separate list of numeric guardrail thresholds here. Hard reject conditions live in the research card kill criteria (section 1), and final acceptance checks live in the promotion gates (section 12). A standalone threshold list creates false comfort: the more configs a search evaluates, the more likely something clears any fixed bar by luck. The honest overfit controls are the kill criteria, the cumulative search-budget count, and the gates.

## 3. Run Baselines

Before optimizing, run enough baselines to know what improvement means.

Recommended baselines:

- current/default config;
- simple naive config;
- random-entry (null) baseline: same exit, sizing, and cost logic with random or shuffled entries, to confirm the entry signal beats noise at all;
- no-filter version if filters exist;
- fee/slippage stress version;
- asset/timeframe baseline comparison.

Record the run IDs, saved-run review links, config, data range, candle count, and backend commit, plus a short interpretive note. Leave the metric tables in the UI / saved-run records. If baselines are unstable or unexplainable, fix that before expanding the search.

## 4. Run a Small Structured Grid

Use a deliberately small grid first:

- 2-4 values for signal windows;
- 2-4 threshold sets;
- 2-3 sizing or volatility-adjustment modes;
- fixed fees, slippage, and leverage;
- discovery data range only; validation and holdout data stay untouched.

The goal is to map response shape, not find the final winner. You want broad plateaus, not a single sharp peak.

Good early questions:

- Do profitable configs cluster together?
- Does performance survive nearby parameter values?
- Is the best config just the highest-turnover config?
- Does net performance vanish when fees increase slightly?
- Does the strategy depend on one short lucky segment?
- Are trades explainable from the intended strategy logic?

Required output:

- grid summary;
- run registry entries for each run or batch;
- top configs;
- median config performance;
- nearest-neighbor performance around the top configs;
- notes on plateaus, cliffs, or noisy regions;
- initial continue / modify / stop recommendation.

## 5. Reflect on Results

Pause after the first grid and review the results from first principles. Lead the review with the strongest positive signal in the results and what it implies, then examine the risks and failure modes — not the other way around. A partial win (for example correct direction most of the time but poor exit monetization) is a finding to build on, not just a reason to reject.

Choose exactly one next state:

- Amplify: a real edge or promising signal appeared but is not yet captured. Design the mechanism or experiment that would harvest it (exit, scale-out, sizing, holding period, regime gating) before widening or stopping. Distinguishing "the current mapping fails to monetize" from "the signal has no edge" is the whole job here.
- Continue: the idea shows stable edge and can move into broader validation.
- Modify: the results reveal a missing mechanism that belongs in the strategy.
- Stop: no stable edge appears, or the failure is structural.

Example:

Question: Is the strategy missing logical functionality that would improve performance?

Answer: "The trend strategy gets chopped up during non-trending environments. Add a slope or regime filter, then rerun the small grid."

If a strategy change is made, rerun the small structured grid before expanding. Do not keep widening the grid around a strategy whose first-principles logic changed.

Modify is not free. Each modification is a researcher degree of freedom that consumes statistical credibility. Log every modification as a hypothesis change in the write log and count them. Default budget: two or three mechanism changes per research card. If the idea still has no stable edge after that, choose stop or restart with a fresh research card; do not keep iterating.

This budget governs undisciplined mechanism-churn on an idea that has shown no edge. It does not cap pursuit of a live edge. When the results already show a real signal that is simply not yet captured (the Amplify state), pulling the thread to harvest that signal is expected work, not budgeted degrees of freedom — keep following it as long as the evidence stays live. Do not use the modify budget as a reason to abandon a promising result.

## 6. Expand the Grid or Stop

Only expand after the small grid shows a stable direction.

Expansion should be based on what the early grid discovered:

- refine around broad plateaus;
- widen only where the response shape is still unclear;
- remove knobs that do not change outcomes;
- add targeted values where cliffs or constraints appear;
- keep fees, slippage, leverage, and data ranges explicit.

Avoid expanding every dimension at once. Each expansion should answer a named question.

## 7. Choose Asset Generalization Path

Before scanning the full universe, decide how asset-specific this strategy is expected to be.

Option A: optimize each asset separately.

- Pros: more accurate, flexible, and controlled.
- Cons: slower research, more complexity, higher overfit risk.
- Use when: assets have clearly different behavior or market structure.

Option B: use one asset's grid as the basis for a universe scan.

- Pros: simple, scalable, efficient.
- Cons: can overgeneralize from one asset.
- Use when: the goal is fast screening or the asset is a strong representative proxy.

Option C: cluster assets by behavior and optimize per cluster.

- Pros: balances generalization and specificity.
- Cons: requires a clustering rule and more review.
- Use when: one global config is too blunt, but per-asset optimization is too noisy or expensive.

Write the chosen path and why it matches the strategy hypothesis.

Whichever path is chosen, validation assets are quarantined: their results must not influence parameter selection. If a validation asset's results are used to tune parameters, it becomes a discovery asset and a fresh validation asset is required.

## 8. Run Mid-Research Sweep

Run the chosen asset path and produce mid-research results.

Required outputs:

- run registry entries for every reviewed run or batch;
- selected and rejected config families, cited by run ID;
- interpretive notes on whether the edge appears local, universal, or clustered (re-fetch metrics from saved runs or UI rather than pasting tables);
- updated risks and tripwires.

By this stage, you should understand the direction the optimal parameters are leaning toward and whether the strategy is worth an endgame optimization pass.

## 9. Robustness Scoring

Rank each config by multiple metrics, not average return alone.

Recommended scoring:

- reward median net return, Sharpe, Sortino, or expectancy;
- penalize drawdown, tail loss, fee drag, turnover, and low trade count;
- penalize cross-asset instability;
- penalize train-validation rank decay;
- penalize parameter cliffs;
- reward configs that are good enough across many assets or a coherent asset group.

Robustness checks:

- Compute median rank across assets instead of average return only.
- Penalize configs with high variance of rank across assets.
- Compare in-sample winners against validation or out-of-sample ranks.
- Measure distance from parameter cliffs; nearby configs should perform similarly.
- Weigh the leaderboard against the cumulative search budget from the run registry; a top score drawn from thousands of configs is only meaningful if nearby configs and out-of-sample behavior agree.
- Do not force one global config if asset behavior clearly differs.

You are looking for durable parameter regions, not leaderboard winners.

## 10. Review Objective Before Endgame Optimization

Before the final optimization loop, reread the original objective and kill criteria.

Ask:

- Is the original objective still the right objective?
- Did the first grids expose a more important constraint?
- Are we optimizing net performance or hiding cost/churn?
- Are we optimizing one market period by accident?
- Are the remaining knobs core to the edge or incidental?

If the objective changes, write the change down and rerun enough prior checks to avoid moving the goalposts silently.

## 11. Final Optimization Loop

Use the smallest loop that can answer the remaining question.

Loop:

1. Select a narrow candidate region.
2. Run focused configs around that region.
3. Compare to baselines and nearby configs.
4. Stress fees, slippage, and data period.
5. Review trade artifacts for explainability.
6. Promote, modify, or reject.

Stop when additional runs no longer change the decision. Do not keep searching just because a slightly better score might exist.

## 12. Promote Candidates Through Gates

A candidate should advance only if it passes the gates below.

- Artifact sanity: every trade can be explained.
- Statistical sanity: enough trades and enough independent periods.
- Cost sanity: edge survives worse fees and slippage.
- Parameter sanity: nearby configs also work.
- Asset sanity: works across a coherent group or has a clear reason for being asset-specific.
- Regime sanity: not only one market mode, using the period/regime segmentation defined in the research card.
- Forward sanity: the untouched holdout range holds up. The holdout is consumed exactly once; if the candidate fails here it goes back to research and that holdout is burned — the next attempt needs a fresh holdout (new data or a new asset).
- Operational sanity: turnover, leverage, sizing, and capacity are plausible.

If a candidate fails a gate, either reject it or send it back to the smallest earlier step that can answer the failure.

## 13. Research Handoff

End every research project with a handoff summary.

Required fields:

- research question;
- final decision: promote, amplify (pursue an uncaptured edge), continue research, or reject;
- what is working: the strongest positive signals found and a concrete proposed way to capture each, stated before the weaknesses;
- reviewable run IDs and artifact links supporting the decision;
- best candidate configs;
- rejected configs and why;
- assets/timeframes where the strategy applies;
- known weaknesses;
- required follow-up tests;
- links to run IDs, charts, tables, and artifacts;
- promotion destination if promoting: where the config goes next (Linear ticket, live strategy config path, or paper-trade deployment);
- recommendation for next action.

The handoff should make it possible for another researcher or coding agent to understand what was learned without rerunning the whole exploration.
