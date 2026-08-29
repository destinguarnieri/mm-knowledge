# Study Menu

Status: current

Purpose: the named set of event-study shapes available to Money Machine research. Choose from this menu. Do not pattern-match the nearest existing study file — that is how a wrong instrument propagates from one program to the next.

Related: [[trading/pmax|P_Max]] · [[research/trading/research_index|Research Board]]

## Choosing a shape

Before selecting, state the **trade structure** being measured:

1. How many legs?
2. How many exits?
3. Does size change during the episode?
4. What ends the episode?

Then pick the shape that can represent that structure. If none can, design one. Measuring a reduced version of the strategy because a standard instrument exists for the reduced version is the most expensive mistake available here — no amount of metric refinement recovers from it.

Finally, answer explicitly: **what would this study be structurally unable to see?** If the answer includes anything the strategy depends on, the design is wrong.

## Invariants every shape obeys

Enforced by the shared measurement contract at
`backend/app/lib/analysis/event_study/contract.py`, which every study imports.
These raise `ContractViolation` at construction; they are not conventions:

- **Terminal states are a named, exhaustive partition summing to 1.0.** Reporting one probability and leaving the complement to inference is how a polarity error survives review.
- **Direction is signed at construction.** Returns live in hypothesis space, not price space, so "positive" always means the hypothesis was right.
- **No evaluative names.** `success`, `failure`, `win`, `hit` are banned. Name the physical event: `reverted_inward`, `continued_outward`, `horizon`, `right_censored`.
- **Censoring is first class** and excluded from probability denominators.

## The shapes

### 1. First-passage / barrier race

Which of several named barriers is reached first, plus path statistics up to that point.

- **Use when:** the trade has exactly one exit and the episode genuinely ends at the first barrier.
- **Cannot see:** anything after the first touch. For a strategy that scales out, holds a runner, or re-enters, this is where most of the P&L lives.
- **Reference:** the PRI study (source on branch `codex/pri-eventstudy`, not on `feat/work`) — `PriDirection = Literal[-1, 1]`, `OutcomeEnd = Literal["prb", "horizon", "right_censored"]`, returns signed at construction.
- **Counterexample:** `event_study/vwap_band`, where `success` means "continued outward" in one phase and "reverted inward" in another under one field name.

### 2. Path / schedule

Records the full episode path in trade coordinates and replays position policies over it as pure functions.

- **Use when:** the strategy is multi-leg — scaling in or out, runners, trailing stops, add-backs, or any position schedule.
- **Records:** level-touch sequence with timing, MFE *and the bar it occurred on*, revisits, time spent beyond each level, and how the episode structurally ended. Termination is the end of the setup, not the first barrier.
- **Why it matters operationally:** the expensive work — data, event detection, path extraction — runs once. Policy iteration then costs minutes instead of a study rebuild, and every policy is compared on identical paths with no re-run variance.
- **Headline metric:** capture ratio against `P_Max(Δt, costs)`.
- **Implementation:** `backend/app/lib/analysis/event_study/path/` — `record.build_episode_path` produces the path, `policy.replay` runs a schedule over it, `pmax.p_max` computes the ceiling by exact dynamic program. Reference policies: `HoldToEnd`, `ExitOnFirstTouch`, `ScaleOut`, and `OracleSingleExit` (non-causal; bounds what perfect exit timing alone is worth, separating an entry problem from an exit problem).

### 3. State-conditional forward returns

Distribution of forward returns conditioned on a state or signal value. No exit logic at all.

- **Use when:** the question is signal quality, not strategy performance — does this state carry information about forward price.
- **Cannot see:** anything about monetization. A strong result here is not a strategy, and a weak result does not condemn one.
- **Reference:** `lib/analysis/returns/forward_return_*`.

### 4. Survival / duration

How long a state persists before it resolves, and what the hazard looks like over time.

- **Use when:** the question is about persistence — how extended is a trend, how long does a regime hold, when does a setup go stale.
- **Pairs with:** cooldown, hysteresis, and time-stop design.

### 5. Matched control

Compares the event population against a matched baseline population that did not have the event.

- **Use when:** you need to establish that the event *matters* — that outcomes differ from what an arbitrary bar would have given you.
- **Cannot see:** anything about magnitude of opportunity. It answers "is this real," not "is this worth trading."
- **Note:** this is the shape most often skipped, and its absence is the most common reason a finding fails to reproduce.

## Combining shapes

A program usually needs more than one. A typical sequence: matched control to establish the event matters, state-conditional returns to size the raw signal, then path/schedule to design and compare capture policies. Running only the last one leaves you unable to tell a policy failure from a signal that was never there.
