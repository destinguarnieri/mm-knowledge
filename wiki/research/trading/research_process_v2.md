# Research Process V2

Supersedes [[research/trading/research_process_v1|Research Process V1]] (2026-07-23). V1 is retained for history.

Purpose: turn a research question into a decision — and, when a real edge appears, into a *captured* edge — without either drifting into parameter chasing or killing a valid signal on the wrong assumption.

## Design principles

1. **Revenue proximity over strategy origin.** Discretionary codification, capture engineering, open discovery, and cross-market extension are research lanes, not a priority ranking. Fund the candidate with the strongest combination of evidence, expected net edge, operational fit, and shortest credible path to a money decision. The [[research/trading/research_index|Research Board]] holds the current ranking.
2. **Two separate questions, separately gated:** does the signal carry directional information (validity), and can we capture it after realistic costs (monetization)? Your own EMA work showed these diverge — direction right ~80% of the time while flip-only still lost money. A valid-but-uncaptured signal is a *promising, fundable state*, not a failure.
3. **Market-agnostic and foundational.** Asset class (crypto perp, equities, futures, FX, …) is an explicit research axis like timeframe or asset. Research produces reusable building blocks — signal definitions, features, capture mechanisms — meant to be re-pointed at other markets cheaply. An edge that fails in one market is *open*, not dead, in the others.
4. **Symmetric discipline.** Every stage carries both a kill thesis and an upside/capture thesis. Lead findings with the strongest positive read, then the caveats. Rigor is for calibration, not for deflating results.
5. **Two cost regimes, always.** Evaluate at the realistic achievable cost (e.g. maker vs taker, real fills) *and* under stress. Reporting only worst-case cost is what buries live edges; reporting only best-case is how you fool yourself.
6. **Protect against the researcher's own intelligence.** A capable model (or human) generates convincing narratives about noise. Untouched holdouts, predictions-before-results, search-budget awareness, and no retroactive narrative changes are non-negotiable. Eloquence is unrelated to evidence.
7. **Earn the right to risk.** Research earns the right to a small live canary; live evidence earns the right to scale. Capital mutation always requires explicit Destin authorization.

## 0. Route the work

Pick the lane before doing anything else so the correct method and evidence gates are used. **Lane selection does not set portfolio priority.** An agent must not promote or demote work merely because it is discretionary, systematic, discovered internally, or derived from an external source.

- **Discretionary codification** — Destin already trades it. Use the `discretionary-strategy-codifier` skill. Extract exact visual/control semantics, preserve independently deployable mappings, prove behavioral parity *before* optimization. Destin's source strategy is the spec; unresolved semantics return to him. The mechanism is Destin's experience — the Mechanism rung (below) is satisfied, so start at Signal Validity or directly at Capture. This lane receives no automatic priority over other candidates.
- **Capture engineering** — a signal already believed valid but not yet monetized (e.g. EMA's 80% time-in-money). Skip discovery; start at the Monetization rung. The whole job is finding a control policy (entry, exit, sizing, holding, regime gating) that harvests the signal after realistic costs.
- **Open discovery** — an explicit new-edge search or an empirical uncertainty exposed during codification. Run the full ladder from Mechanism.
- **Cross-market extension** — take an already-validated edge to a new asset class/venue. Re-point the portable signal definition; re-derive only the market-specific capture and parameters; treat the new market as fresh holdout surface.

Each lane declares up front: the decision(s) it must support, the deployment target(s) including **asset class + venue + account isolation**, and the split between the **portable** part (signal/mechanism) and the **market-specific** part (capture/params).

## 1. Research card (symmetric, up front)

One page before optimization starts. Required fields:

- **Edge/mechanism hypothesis** (for discovery): who pays us, why they are willing or forced to, why competition has not removed it, under what conditions it should disappear, and whether we can capture it after costs. (For codification, record Destin's stated mechanism instead.)
- **Markets & venues in scope:** which asset classes and venues, and which are discovery vs holdout surface.
- **Signal definition (portable)** kept separate from **capture policy and parameters (market-specific)**, so findings are reusable building blocks.
- **Kill criteria:** the hard conditions that reject a config or the idea regardless of headline return (fee-stressed net below zero, drawdown floor, minimum trade count, single-segment dependence, isolated top config with failing neighbors).
- **Upside / capture thesis:** what would make this worth pursuing hard, what "good" looks like, and what the capture target is if the signal proves valid. This is the required counterweight to the kill criteria — do not write one without the other.
- **Data splits:** discovery, validation, and an untouched holdout, fixed before the first run. The holdout is consumed exactly once, at the promotion gates. Each additional market is additional independent holdout surface — use it as such.
- **Regime/period segmentation:** how time and market state will be segmented for period-dependence checks, defined before the first run.
- **Costs:** both the realistic achievable regime and the stress regime, defined explicitly.
- **Core vs incidental knobs.**
- **Search-budget counter:** cumulative configs evaluated across the whole project. Every interpretation weighs the leaderboard against this count — the best of two thousand runs looks good by construction.

## 2. The evidence ladder

The backbone. Each rung is fail-fast, and each carries both a kill read and an upside/capture read. A candidate can fail any rung without spawning follow-up work. **A rejection is scoped to what was tested** — "rejected in crypto 5m flip-only" is not "dead everywhere"; record where it remains open or untested.

1. **Mechanism** — a coherent reason the edge could exist. (Satisfied by Destin's experience for codification.)
2. **Cheap falsification** — the smallest test that could kill it, including a null/random-entry baseline (same exit, sizing, costs; shuffled entries) to confirm the signal beats noise at all.
3. **Signal validity** — *does it carry directional information?* Time-in-money, hit rate, forward-return / information coefficient, favorable-excursion capture. **This is a separate gate from making money.** Passing here with monetization unsolved = "promising, capture-open" → route to rung 4, do not reject.
4. **Monetization / capture** — *can a control policy harvest it after realistic costs?* Treat entry, exit, sizing, holding period, and regime gating as independent axes. Evaluate at realistic *and* stress costs. This is where capture-engineering work lives; a valid signal that no policy can monetize across realistic costs and markets is the real kill, not a losing first policy.
5. **Robustness / adversarial** — leakage and lookahead checks, overfit and parameter-cliff tests, regime/period dependence, search-budget haircut, and **cross-market generalization**: does the edge survive in another asset class, or is it market/microstructure-specific? Both outcomes are informative — a generalizing edge is stronger mechanism evidence *and* buys more independent regimes; a single-market edge is valid but labeled specialized. Do not force generalization; do not force rejection.
6. **Deployability** — capacity, liquidity, latency, operational complexity, and failure behavior, per venue and asset class.
7. **Shadow execution** — signals and simulated fills generated under real production conditions.
8. **Small live canary** — minimum useful capital with predetermined loss and time budgets. **Requires explicit Destin capital authorization.**
9. **Scale** — increase exposure only as live evidence supports the estimated edge, heavily haircut from historical estimates.

Reflect after early rungs and choose one next state explicitly: **amplify** (a real signal appeared but is not yet captured — fund the capture experiment), **continue**, **modify** (a missing mechanism belongs in the strategy), **extend** (take it to another market), or **stop**. The modify budget (≈2–3 mechanism changes on an idea showing no edge) governs undisciplined churn, not pursuit of a live edge — following a validated signal to capture it is expected work.

## 3. Cross-market as a first-class axis

- Asset class is a research dimension, not an afterthought. Design so a portable signal can be re-pointed at crypto, equities, futures, or FX with only the capture/params re-derived.
- Generalization across markets is strong evidence of a real mechanism and directly mitigates crypto's small number of independent regimes.
- A negative result in one market **opens** the question in others rather than closing it globally. Record the per-market state (validated / capture-open / rejected-in-market / untested).
- Keep a running inventory of foundational building blocks (signals, features, capture mechanisms) so later research composes them instead of rebuilding.

## 4. Guardrails against fooling ourselves

Non-negotiable, and they apply most to the agent:

- Complete experiment history and reproducible calculations (run IDs, config, data range, engine/commit, seed).
- Predictions recorded before results; label any post-result hypothesis revision.
- Untouched holdouts; explicit discovery/validation separation; a validation asset touched for tuning becomes a discovery asset and needs a fresh one.
- Multiple-testing / search-budget awareness; simple baselines.
- Independent adversarial review for promotion-track candidates.
- No retroactive narrative changes without disclosure. Eloquence ≠ evidence.

## 5. Ranking deployable edges

Rank candidates by something like:

> expected net edge × confidence × capacity × diversification value
> ÷ (tail risk × operational complexity × fragility)

Diversification value explicitly rewards cross-market and cross-mechanism decorrelation. A modest, understandable, reliably deployable edge can outrank a spectacular but fragile backtest.

Portfolio ranking should also account for **distance to the next decisive economic test**. When two candidates have comparable expected value, prefer the one that can reach a trustworthy promote/reject or shadow-execution decision sooner. Do not confuse amount of prior work with proximity to revenue.

## 6. Documentation

Use the two-layer research doc: a small **living head** rewritten in place each session (TL;DR & What's Working → Current Read (provisional, not a verdict) → Open Threads / Next Experiments), and an **append-only tail** (Fixed Assumptions, Run Registry as pointers-not-tables, Write Log). See [[research/trading/emac-cross-10-200/emac-cross-10-200|EMA Cross 10/200 Research]] as the reference structure and apply `.cursor/rules/research-continuity.mdc`.

- Persisted `run_id` values are the metric source of truth; Destin's UI is the default place for tables. Do not paste metric tables into wiki/checkpoint/changelog/canvas.
- Separate portable signal notes from market-specific capture notes so results stay reusable.
- The living head mirrors the handoff format below, so an end-of-session handoff *is* the doc-head update.

### Research Board and Linear synchronization

The three research-state layers have distinct authority:

- **Per-thread research page:** evidence, assumptions, run pointers, interpretation, and the thread's next experiment.
- **Research Board:** current portfolio ranking, primary/challenger/parked state, decisive uncertainty, and cross-thread relationships. This is the authority for what research is funded now.
- **Linear:** concrete funded execution and backlog. It is not the authority for scientific interpretation or portfolio ranking.

Agents must keep them synchronized as part of closing a material research session:

1. Before work, read the Research Board and the relevant thread page; confirm that an `active` or `primary` thread has a linked Linear execution item.
2. After evidence changes a thread's validity, monetization, priority, status, blocker, or next experiment, update the thread's living head and its Research Board row in the same session.
3. Update the linked Linear issue or project when the executable next action, state, blocker, or completion status changed. Do not copy metric tables into Linear.
4. Exactly one revenue candidate may be `primary`. A `parked` item must state the condition that would resume it. Replacing the primary requires explicitly demoting or closing the previous one.
5. Every `In Progress` research issue must map to a `primary` or `active` board entry, or be identified as bounded enablement for the primary. Every `primary` or `active` board entry must have funded execution represented in Linear.
6. If the layers disagree, stop treating the stale layer as context. Reconcile the board from the per-thread evidence, then reconcile Linear from the corrected board before starting unrelated work.

Routine synchronization is part of the research closeout, not a separate documentation project. Historical changelog entries remain historical and must not override the current board.

## 7. Handoff and decision

Return a decision vector, not a single binary, and state what's working first:

- **What is working:** the strongest positive signals and a concrete way to capture each — before the weaknesses.
- **Decision per independently deployable mapping and per market:** promote / amplify (pursue an uncaptured edge) / continue / extend to another market / narrow / reject-in-market / inconclusive.
- **Deployment target:** environment, asset class, venue, and account/subaccount identity for which each conclusion applies.
- **Evidence:** reviewable run IDs and artifact links; best and rejected configs with reasons.
- **Boundary conditions and per-market state:** where valid, where capture-open, where rejected, where untested.
- **Remaining uncertainty** capable of changing the decision, and the highest-value next experiment (capture-first). Use `none` only when a line is genuinely closed.
- **Promotion destination** if promoting: Linear ticket, live strategy config path, or paper/canary deployment.
