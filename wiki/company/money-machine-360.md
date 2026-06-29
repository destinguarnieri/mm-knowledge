# Money Machine 360

Purpose: capture the current business context, system reality, operating model, and strategic direction for Money Machine Labs so Hermes and future agents can operate with the right frame.

## Mission

Money Machine Labs is trying to become the largest AI-powered financial company in the world.

This specific system is for internal trading and research activities.

Important constraints on the business model:
- Money Machine Labs trades its own capital.
- There are no end users.
- There are no outside investors in a trading fund.
- The company lives and dies on its own capital and its own systems.

Long-term success means:
- compounding capital at scale
- becoming a dominant AI-native financial company
- eventually IPOing on the NASDAQ
- scaling to hundreds of billions in capital under management

## Current bottleneck

The immediate bottleneck is the speed of the backtest and research loop.

Current loop:
1. human reviews UI
2. human checks logs
3. human tweaks config / params
4. repeat

This is far too slow.

The first major agentic win should be compressing this loop from manual iteration into an automated research process that runs in seconds or minutes rather than long human cycles.

## System reality today

### High-level state

The trading infrastructure is currently functional.

It is best thought of as two major domains:
- trading infrastructure
- research infrastructure

Within those domains, there are many subcomponents, but the broad split is the most useful starting frame.

### What is true today

- The system is currently functional trading infrastructure for running continuous trading.
- Functionally, things are working.
- The overall system is in a good place.

### What is not yet true

- The system is not battle-tested in production.
- Strategy running in production is still missing.

This means the challenge is not “build from zero.”
The challenge is turning a working system into a reliable capital engine.

## Founder background

Destin comes from the manual discretionary trading world and has about 10 years of trading experience.

About 6 months ago, he started pursuing automation of his trading process.

Relevant background:
- about 6 years of coding experience
- catalog of indicators, signals, and strategies that have worked over time
- original goal: remove the human trader from the loop where possible
- currently studying AI / ML through Stanford coursework (CS230)
- not yet deeply specialized in ML research, but learning quickly and building practical understanding fast

## Operating model

### How work actually happens

Different days run in different modes.

Examples:
- Some days are ticket-pulling and execution-heavy.
- Some days are dominated by backtests, reviewing results, and iterative tweaking.

This means the operating system cannot assume one fixed mode of work.
It needs to support both execution mode and research mode.

### Where agents fit first

Agents fit in many places, but the first concrete high-leverage starting point is the backtest and research loop.

Target agentic flow:
1. strategy files with config and params are provided
2. an agent runs backtest research
3. the agent views results
4. the agent reasons about findings
5. the agent tweaks config / params
6. the agent repeats
7. the agent saves progress as discoveries are made
8. the agent pings the team with progress updates

This should be treated as a core company capability, not a side experiment.

### Hermes role

Hermes should primarily act as operator / manager / co-operator.

That means:
- helping Destin drive things forward
- structuring work
- keeping the operating system clean
- managing or supervising other agents where appropriate
- providing judgment support and prioritization support

For the backtest loop specifically, the preferred model is likely:
- another long-running agent (or subprocess) performs the repetitive research loop
- Hermes manages that process, tracks progress, and keeps it aligned with company priorities

### Coding agents

Agents can also contribute to coding, but the environment should not become a chaotic swarm of coding agents.

Important boundary:
- code that touches money paths is sensitive
- core trading infrastructure is human-judgment-heavy
- agentic coding in those paths should remain controlled and light

The desired posture is:
- use agents to gain parallelism and speed
- do not allow uncontrolled autonomous coding in capital-sensitive systems

## Work classes

The business should be thought of as having at least three work classes.

### 1. Capital lane
This includes anything that directly affects live trading, order flow, positions, reconciliation, risk, or production execution.

Characteristics:
- human judgment heavy
- low agent autonomy
- higher review standards
- mistakes are expensive

### 2. Research lane
This includes backtests, signal evaluation, parameter search, model experiments, strategy iteration, and result interpretation.

Characteristics:
- highest agent leverage
- should optimize for speed and throughput
- progress should be logged continuously
- the first big automation target

### 3. Enablement lane
This includes systems that improve the velocity of the other two lanes.

Examples:
- dashboards
- internal tools
- automation
- branch workflows
- experiment tracking
- memory and knowledge systems
- agent orchestration

Characteristics:
- leverage multiplier
- should help research and production move faster and more safely

## Strategic direction

### 30-day priorities

1. Get a minimum of two strategies into production.
2. Get one 24/7 agentic backtest loop running.
3. Train one quantile regression model to predict forward percent change.

### 90-day priorities

Groundwork for agentic experimentation should be in place.

Targets:
1. Agentic capabilities should expand beyond the narrow backtest loop.
   - Example: agents creating git branches
   - Example: agents writing strategy code
   - Example: agents making new signals
2. Train a basic neural network to predict volatility.
   - Reference direction: Ernest P. Chan / Chen-style volatility modeling work from 2023 context

### 180-day direction

By this point, capital should be scaling and the company should operate like a well-oiled machine.

Desired state:
- real human hires pushing progress alongside agents
- many experiments running in parallel
- strong public positioning as a serious AI-native financial company

Concrete 180-day targets:
1. End-to-end agentic flow
   - swarms of coordinated agents
   - pod-shop style orchestration
2. Significant progress on neural net development
3. Agents participating in model-weight setting and broader NN development workflows

## Biggest unknown

The AI landscape is moving extremely fast.

A rigid long-term plan will likely become outdated.

The more durable strategy is to build an operating system that can absorb new capabilities quickly and exploit them safely.

## Biggest opportunity

The biggest opportunity is to stand on top of the monsoon of open-source AI development and adapt it to financial trading.

Important framing:
- many labs around the world are producing rapid progress
- much of that progress uses language as the substrate
- Money Machine Labs can leverage that wave rather than reinventing it
- the edge is in adapting that progress to numbers, markets, trading systems, and research loops

In short:
- use the global open-source AI wave as leverage
- fit it for quantitative and trading use cases
- build internal systems that compound that advantage

## Current implications for operations

Based on this context, the operating system should optimize for:
- research speed
- safe production hardening
- capital protection
- experiment throughput
- agent leverage

It should not optimize for:
- customer feature theater
- SaaS-style roadmap rituals
- heavy ceremony disconnected from execution

## Current implications for Linear

The current Linear setup should be interpreted as follows:

- Trading System Reliability = capital lane hardening
- Backtesting and Evaluation = research lane
- Dashboard V2 = enablement lane

This framing matters because the lanes should be operated differently:
- capital lane = more caution, more human judgment
- research lane = more speed, more agent leverage
- enablement lane = internal velocity multiplier

## Open operating principle

Hermes should help run the system, not just track tickets.

That means Hermes should increasingly help with:
- prioritization
- project framing
- board hygiene
- identifying missing work
- sequencing decisions
- managing or supervising delegated agents
- turning rough founder context into executable operating structure

## Current conclusion

Money Machine Labs is no longer at the stage of “can this be built at all?”

It is at the stage of:
- tightening production reliability
- deploying live strategies
- compressing research loops
- building the first real agentic operating advantage

The most immediate leverage move is to make the backtest and research loop agentic.

The most important caution is to maintain strong human judgment in money-sensitive trading paths.

The medium-term opportunity is to turn the company into an AI-native research and trading machine that compounds both capital and learning speed.
