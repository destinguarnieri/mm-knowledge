# Money Machine Operating Context

Purpose: give agents the smallest durable company frame needed to make good decisions.

## Company

Money Machine Labs is a proprietary quantitative trading and AI research company.

- It trades its own capital.
- It has no trading-product end users.
- It does not manage an outside investment fund.
- Its systems exist to codify, validate, deploy, and scale profitable trading strategies.

The long-term ambition is to build a dominant AI-native financial company. Current work is judged by whether it advances the next proof, not by how complete that future vision sounds.

## Current Company Phase

Money Machine is in **parallel revenue research and monetization**. The company has several strategy programs, reusable research components, and model directions at different evidence stages. The current bottleneck is research throughput and converting supported signals, market-state knowledge, forecasts, and control ideas into cost-valid strategy evidence without making Destin supervise every step.

Strategy origin does not determine priority. A discretionary strategy, a simple systematic baseline, a captured signal, a multi-signal model, or a newly discovered edge may become the next deployment candidate when its evidence, economics, operational fit, and distance to deployment justify promotion.

For this phase:

- maintain a visible portfolio of revenue candidates and reusable mechanisms
- keep the portfolio of research programs visible and let independent agents advance bounded workstreams in parallel
- use current evidence and distance to a money decision to order scarce human review, capital decisions, and shared-resource conflicts
- run the cheapest decisive validity, forecasting, control, monetization, or deployability test inside each funded workstream
- preserve valid signals when a particular capture policy fails
- promote a surviving candidate through shadow execution and an explicitly authorized live canary
- preserve explicit program/workstream state so independent work can continue, wait on a named dependency, or close without being lost

Destin's live experience is strong prior evidence when evaluating a discretionary strategy, but it does not automatically outrank other evidence. Likewise, a promising systematic backtest is a lead rather than a deployment verdict until costs, robustness, and execution are tested.

## Current North Star

Produce positive net realized live P&L after costs over an active founder-set proof period.

The immediate loop is:

1. decompose current programs into independent, reviewable workstreams
2. let separate agents execute non-colliding workstreams in parallel
3. use simple one-signal / one-position strategies as controls while also advancing market-state, forecasting, position-control, execution, and portfolio layers
4. require each workstream to produce a promote, narrow, continue, reject, or blocked-on-specific-decision result
5. route only true ambiguities, cross-workstream conflicts, and promotion decisions to Destin
6. test realistic costs, robustness, deployability, and shadow execution as the evidence warrants
7. launch only with Destin's explicit capital and risk authorization
8. measure live net realized P&L after costs, update the portfolio, and repeat

Tickets, infrastructure, documents, and raw agent activity are inputs or costs, not the proof. Backtests are the tool that surfaces edge: a backtest that reveals a real or promising edge is progress to pursue, even though it is not yet the live-P&L proof. Do not treat a promising result as a cost to minimize.

## System Reality

Money Machine already has functional live-trading and research infrastructure. Live runtime and backtest/research runtime are separate domains in one codebase.

The current challenge is not to build a complete platform or maximize thread count for its own sake. It is to run many well-bounded research packets concurrently, convert the strongest surviving evidence into controlled production candidates, gather live evidence, and remove only the blockers those attempts reveal.

The system is functional but not yet battle-tested in profitable production. Capital-sensitive paths therefore require strong human judgment and verification.

## Work Lanes

### Capital

Live runtime, accounts, orders, positions, reconciliation, risk, deployment, and strategy lifecycle.

- low agent autonomy
- explicit Destin authorization for mutations
- high correctness and review requirements

### Research

Candidate ranking, discretionary-strategy elicitation, behavioral-parity review, open discovery, backtests, signal evaluation, capture engineering, bounded parameter investigation, strategy iteration, and result interpretation.

- highest safe agent leverage
- optimize for elapsed time to a trustworthy money decision and then to deployable evidence
- stop research when the evidence is sufficient for a go/no-go decision

### Enablement

Tools, automation, dashboards, persistence, orchestration, and process improvements.

- justified only by an observed blocker in the active revenue loop
- prefer a manual or existing-system path first
- build the smallest fix, then return to the revenue experiment

## Operating Order

1. Question the requirement and identify who requires it.
2. Delete unnecessary work, process, and abstractions.
3. Simplify the smallest remaining path.
4. Accelerate the evidence loop.
5. Automate only after a real attempt proves the current path limiting.

Keep one bounded issue per agent, not one issue for the whole company. Run independent agent-owned research workstreams in parallel; reserve Destin's focus for decisions and review. The [[research/trading/research_index|Research Board]] is the current portfolio authority; strategy origin or lane must never silently override evidence or economics.

## Decision Standard

Progress is:

- live evidence
- a real or promising edge identified and pursued toward capture
- positive net realized P&L after costs
- shorter time from strategy hypothesis to production evidence
- a reduction in decision-relevant uncertainty
- closed decisions and experiments
- unnecessary work deleted

Progress is not:

- ticket count
- lines of code
- document volume
- architecture completeness
- agent activity

New tickets, infrastructure, abstractions, or scope expansion must name the failed current-system attempt, causal blocker, no-build alternative, smallest fix, and work displaced.

This deletion, deferral, and cost framing governs work-creation — tickets, infrastructure, abstractions, and busywork. It does not govern the interpretation of empirical results. A promising or surprising-positive finding (a live edge, a high hit rate, correct direction with poor capture) is progress: pursue and capture it rather than filing it under activity or defaulting it to no next move. Do not deflate real signal, and do not kill an edge using a worst-case cost assumption the intended venue would not actually pay.

## Safety And Authority

Destin must explicitly authorize live runtime, account, order, position, strategy lifecycle, deployment, secret, or other capital mutation.

Speed never authorizes skipping identity, failure/retry, type, negative-path, verification, or review requirements on money-sensitive or high-risk work.

## Current State

This page is durable company context. Current strategy selection, proof period, blockers, decisions, and next action live in [[sessions/current-checkpoint|Current Checkpoint]].
