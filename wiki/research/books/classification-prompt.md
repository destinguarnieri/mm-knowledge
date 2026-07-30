# Book Classification and Condensation Prompt

You are classifying a batch of detailed textbook chapter extractions into a smaller, research-ready knowledge body.

## Assignment

Read every supplied chapter extraction completely. Produce one self-contained Markdown classification file for the assigned chapter range.

The source chapter files are already exhaustive extractions. Do **not** rewrite them chapter by chapter and do not create another textbook summary. Compress across chapters by merging repeated ideas and retaining only material that is useful for future research, implementation design, or evidence evaluation.

Use only the supplied extracts. Do not add outside facts. Do not treat a textbook statement, backtest, parameter choice, or anecdote as independently established evidence.

## Objective

Reduce the source into a neutral map of:

1. durable foundational knowledge;
2. transferable research and validation methods;
3. concrete, falsifiable research directions;
4. strategic capabilities required by multiple research directions;
5. frontier or unusually complex directions;
6. source-, vendor-, broker-, instrument-, or platform-specific material;
7. claims and parameters requiring independent validation.

The classification is a research inventory, not a recommendation or current priority ranking. Difficulty, capital needs, weak evidence, and operational risk should be recorded without automatically deleting an idea.

## Compression rules

- Merge duplicate concepts across chapters.
- Preserve distinctions that change design or interpretation: signal versus sizing, directional versus relative value, gross versus net performance, forecast quality versus execution quality, synthetic versus executable instruments, and source evidence versus classifier inference.
- Retain formulas only when they define a portable mechanism. Prefer a compact verbal specification when the exhaustive source already preserves the full derivation.
- Retain parameter values when they define the proposed test; label them source defaults, not universal constants.
- Keep negative results when they close or narrow a direction.
- Preserve boundary conditions, data requirements, capital/granularity constraints, costs, leakage risks, operational hazards, and failure modes.
- Collapse worked examples, table-by-table results, repeated definitions, tutorial prose, and glossary material unless they change the research design or evidentiary conclusion.
- Do not copy large performance tables. Summarize the direction and evidentiary strength.
- Do not infer that the best historical variant is the best future choice.
- Do not silently correct a suspected source inconsistency; flag it.

## Evidence convention

Use these labels when provenance could be confused:

- **Textbook proposal:** a mechanism, rule, parameter, or claim made by the source.
- **Reported textbook result:** a historical result reported in the extracts; it still requires replication.
- **Classifier inference:** a research implication derived from combining or generalizing supplied material.
- **Not supported by this batch:** a plausible claim that the supplied chapters do not establish.

## Classification taxonomy

### Foundational knowledge

Durable concepts needed to reason correctly about the domain.

### Transferable research methods

Reusable ways to specify, test, compare, falsify, or implement research across multiple strategies or markets.

### Concrete research directions

Falsifiable strategies, models, or workflows. For each material direction include, compactly:

- textbook basis;
- core hypothesis/question;
- applicable markets or instruments;
- required data;
- candidate rule/model;
- meaningful baselines;
- evaluation design;
- major failure modes;
- a clear continue/narrow/reject criterion when supported.

Group closely related variants under one direction instead of inflating the inventory.

### Frontier / high-complexity directions

Serious longer-horizon programs with unusual data, capital, execution, modelling, or operational demands.

### Strategic capabilities

Shared infrastructure or competence required by several directions. These are capability categories, not automatic build recommendations.

### Source-specific material

Broker codes, exchange lists, named datasets, author portfolio composition, historical contract facts, website resources, fixed source-era costs, and other implementation details whose portable lesson should be separated from the literal example.

### Claims requiring independent validation

Reported performance, empirical regularities, fixed thresholds, cost assumptions, formula conventions, instrument rules, and causal stories that should not be accepted without current, point-in-time replication.

## Required Markdown structure

```markdown
# Neutral Classification of Chapters <range>

## Scope and evidence convention

## Classification map

## Foundational knowledge

## Transferable research methods

## Concrete research directions

### 1. <Direction name>

- **Textbook basis:** ...
- **Core hypothesis/question:** ...
- **Applicable markets:** ...
- **Required data:** ...
- **Candidate methods/rules:** ...
- **Meaningful baselines:** ...
- **Evaluation design:** ...
- **Major failure modes:** ...
- **Continue only if:** ...

## Frontier / high-complexity directions

## Strategic capabilities

## Source-specific material

## Claims requiring independent validation

## Broad one-sheet nominations by theme

## Source files
```

Omit an empty section. The exact organization may adapt to the batch, but the evidence convention and taxonomy must remain intact.

## Cross-batch synthesis

After all batch files are complete, create `classification-synthesis.md` that:

- deduplicates the batch classifications;
- organizes the book by foundation, method, research direction, capability, frontier program, and validation risk;
- preserves negative or mixed findings;
- separates directional signals, portfolio construction, execution, and risk controls;
- gives an evidence ladder from textbook proposal through realistic forward/live evidence;
- provides broad one-sheet nominations without pretending they are current priorities;
- links every batch classification and the chapter index.

## Quality control

Before finishing, verify that:

- every assigned chapter was represented;
- repeated chapter material was consolidated;
- no outside knowledge was introduced;
- textbook claims were not promoted to facts;
- weak and negative findings were retained;
- operational, cost, capital, and data boundary conditions remain visible;
- the result is materially smaller than the source extracts;
- Markdown and relative source links are valid.

Finish by reporting the output path and unresolved classification issues.
