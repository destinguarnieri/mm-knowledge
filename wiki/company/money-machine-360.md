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

Money Machine's first lifecycle phase is discretionary alpha transfer. Destin has a large inventory of strategies developed through approximately ten years of manual trading. The current bottleneck is faithful codification, not a shortage of strategy ideas.

For this phase:

- select one strategy Destin actually trades
- extract its visual states, actions, exceptions, and risk semantics
- preserve distinct trade mappings, including opposing directions on isolated subaccounts
- prove the automated behavior matches Destin's intended behavior
- then test whether that faithful implementation remains viable after current costs and constraints

Destin's live experience is strong prior evidence for the strategy mechanism, but it does not replace behavioral-parity checks or current economic validation. Novel strategy discovery is secondary until the discretionary inventory is exhausted or Destin explicitly requests exploration. Exploratory work remains appropriate when a codification ambiguity requires empirical evidence.

## Current North Star

Produce positive net realized live P&L after costs over an active founder-set proof period.

The immediate loop is:

1. select one discretionary strategy Destin actually trades
2. elicit and codify its exact control semantics
3. prove behavioral parity against representative and edge-case examples
4. validate the faithful implementation with the current system and realistic costs
5. make an explicit decision for each independently deployable trade mapping
6. launch only with Destin's explicit capital and risk authorization
7. measure live net realized P&L after costs
8. learn from the result and repeat

Backtests, tickets, infrastructure, documents, and agent activity are inputs or costs. They are not the proof.

## System Reality

Money Machine already has functional live-trading and research infrastructure. Live runtime and backtest/research runtime are separate domains in one codebase.

The current challenge is not to build a complete platform or discover alpha from zero. It is to transfer Destin's existing discretionary alpha into faithful automated strategies, put one into controlled production, gather live evidence, and remove only the blockers that the attempt reveals.

The system is functional but not yet battle-tested in profitable production. Capital-sensitive paths therefore require strong human judgment and verification.

## Work Lanes

### Capital

Live runtime, accounts, orders, positions, reconciliation, risk, deployment, and strategy lifecycle.

- low agent autonomy
- explicit Destin authorization for mutations
- high correctness and review requirements

### Research

Discretionary-strategy elicitation, behavioral-parity review, backtests, signal evaluation, bounded parameter investigation, strategy iteration, and result interpretation.

- highest safe agent leverage
- optimize first for elapsed time to a faithful executable strategy, then for decision-quality evidence
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

Keep one primary revenue outcome in progress unless Destin explicitly expands WIP.

## Decision Standard

Progress is:

- live evidence
- positive net realized P&L after costs
- shorter time from strategy hypothesis to production evidence
- closed decisions and experiments
- unnecessary work deleted

Progress is not:

- ticket count
- lines of code
- document volume
- architecture completeness
- agent activity

New tickets, infrastructure, abstractions, or scope expansion must name the failed current-system attempt, causal blocker, no-build alternative, smallest fix, and work displaced.

## Safety And Authority

Destin must explicitly authorize live runtime, account, order, position, strategy lifecycle, deployment, secret, or other capital mutation.

Speed never authorizes skipping identity, failure/retry, type, negative-path, verification, or review requirements on money-sensitive or high-risk work.

## Current State

This page is durable company context. Current strategy selection, proof period, blockers, decisions, and next action live in [[sessions/current-checkpoint|Current Checkpoint]].
