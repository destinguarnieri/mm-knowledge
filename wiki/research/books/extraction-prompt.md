You are extracting structured knowledge from one chapter of a textbook.

## Assignment

Process only the chapter provided to you. Read it completely and produce a self-contained Markdown study/reference file.

Do not rely on outside knowledge unless explicitly instructed. Do not invent missing information. If content is unclear, incomplete, or illegible, flag it rather than guessing.

## Completeness contract

Completeness is determined by reconciling the extraction against the supplied source, not by whether the final summary feels comprehensive.

Before drafting, make a source inventory of:

- every heading and subheading;
- every numbered equation and every unnumbered formula that defines a mechanism, calculation, decision rule, or parameter;
- every numbered example, exercise, algorithm, and code block;
- every figure and table;
- the first and last available page or other source boundary.

After drafting, reconcile every inventory item to either:

1. a specific place in the output; or
2. an explicit entry under `Open Questions or Extraction Issues` stating that the item was missing, truncated, illegible, or intentionally omitted and why.

Sequential gaps are mandatory review signals. For example, if the source or output contains Equations 2.5 and 2.7, Examples 2.3 and 2.6, or Figures 4.1 and 4.3, account explicitly for the missing identifiers before marking the chapter complete. Do not infer that an unobserved item is unimportant.

A prose description of a mathematical relationship does not substitute for its source formula. If the text names a formula, coefficient transformation, closed-form solution, threshold calculation, or parameter-selection rule, preserve the equation and the reasoning that connects it to its use.

Use `status: "extracted"` only when reconciliation passes. Use `status: "needs-review"` when source material or an inventory item cannot be recovered or confidently interpreted.

## Required output

Write the result to:

`chapters/<zero-padded-chapter-number>-<short-kebab-case-title>.md`

Example:

`chapters/03-probability-distributions.md`

## Extraction requirements

Capture all material needed to understand and apply the chapter, including:

- The chapter’s purpose and central argument
- Every major concept, principle, model, method, and definition
- Important distinctions and relationships between concepts
- Assumptions, constraints, boundary conditions, and exceptions
- Procedures, algorithms, and step-by-step methods
- Every numbered or displayed mathematical formula and equation
- Every unnumbered formula that defines a mechanism, calculation, decision rule, output, or parameter choice
- Definitions of every variable and symbol used in each formula
- Units, domains, and conditions under which formulas apply
- Derivations or proof outlines when they contribute to understanding
- Worked examples, preserving the important calculation steps
- Tables, figures, diagrams, and what they communicate
- Practical applications and implications
- Warnings, common errors, and edge cases
- Chapter conclusions and key takeaways
- Terms that should appear in a glossary
- Connections explicitly made to other chapters

Do not reduce the chapter to a shallow summary. Preserve the details required for someone to reconstruct the chapter’s reasoning without rereading the source.

## Formula handling

Transcribe formulas exactly using LaTeX:

- Inline mathematics: `$...$`
- Display mathematics: `$$...$$`

Formula importance is not discretionary. Capture:

- every numbered equation;
- every displayed equation;
- every formula referenced by a worked example, code block, later equation, or trading/research rule;
- every coefficient transformation or closed-form result used to interpret a model;
- every formula whose omission would prevent reconstruction of the chapter's reasoning or implementation.

For every captured formula, include:

1. The formula
2. A definition of every symbol
3. Its purpose
4. Its assumptions or validity conditions
5. A short interpretation
6. A worked example if one appears in the chapter

When equations form a derivation chain, preserve the chain and explain how one expression yields the next. Do not retain an upstream equation while replacing a downstream analytical result with prose.

Never silently “correct” a formula. If the source appears inconsistent, preserve the source version and add a clearly labeled note.

## Source traceability

Attach a page number, section number, or other available source locator to every major concept, formula, example, table, and figure.

Use this format where possible:

`Source: p. 42`

For a range:

`Source: pp. 42–44`

If reliable pagination is unavailable, cite the nearest section or subsection heading. Never fabricate a locator.

Distinguish clearly between:

- Content stated by the textbook
- Your concise paraphrase
- Any inference required to connect ideas

## Markdown structure

Use this structure:

---
title: "<Chapter title>"
chapter: <chapter number>
source: "<Textbook title>"
status: "<extracted | needs-review>"
---

# Chapter <number>: <title>

## Chapter Overview

A concise explanation of the chapter’s purpose, scope, and central ideas.

## Learning Objectives

List stated objectives. If none are explicitly provided, label inferred objectives as inferred.

## Key Concepts

### <Concept name>

Include its definition, explanation, significance, assumptions, relationships, and source locator.

## Mathematical Formulas

### <Formula or method name>

**Formula**

$$
...
$$

**Variables**

- `$x$` — definition and units
- `$y$` — definition and units

**Purpose:** ...

**Conditions and assumptions:** ...

**Interpretation:** ...

**Source:** ...

## Methods and Procedures

### <Method name>

1. ...
2. ...
3. ...

Include required inputs, expected outputs, decision points, and failure conditions.

## Derivations and Proofs

Preserve important logical or mathematical steps without adding unsupported steps.

## Worked Examples

### <Example name>

Include the problem, method, calculation steps, result, interpretation, and source locator.

Represent every numbered example in the supplied source. If an example is abbreviated because it repeats a method, still record its identifier, inputs, reported result, and what it adds. Reconcile gaps in example numbering under `Open Questions or Extraction Issues`.

## Figures and Tables

For each important item, record:

- Identifier and title
- What it contains
- What conclusion the reader should draw
- Relevant variables, axes, units, or categories
- Source locator

Do not claim to reproduce a figure if you only describe it.

## Applications

Describe practical uses explicitly discussed in the chapter.

## Assumptions, Limitations, and Edge Cases

Capture qualifications that could change how a concept or formula should be used.

## Common Mistakes and Warnings

Include mistakes identified by the author and errors a reader could make when applying the chapter’s methods.

## Key Takeaways

Provide a precise, information-dense recap.

## Glossary

| Term | Definition | Source |
|---|---|---|
| ... | ... | ... |

## Connections to Other Chapters

Include only connections stated or clearly supported by the supplied text. Label inferred connections.

## Open Questions or Extraction Issues

Record:

- Illegible or missing material
- Ambiguous notation
- Suspected source inconsistencies
- Figures or tables that could not be interpreted
- Items requiring human review

## Source Coverage Inventory

Provide a compact reconciliation table:

| Source item | Identifier or heading | Output location | Status |
|---|---|---|---|
| Source boundary | first–last supplied page/section | Chapter Overview | complete / truncated / needs review |
| Section | ... | ... | captured / needs review |
| Equation | ... | ... | captured / needs review |
| Example | ... | ... | captured / needs review |
| Figure or table | ... | ... | captured / needs review |

The table may group contiguous items only when every identifier in the range is present. Do not write `Equations 2.1–2.8` if one of those equations was not observed and reconciled.

## Quality-control checklist

Before finishing, verify that:

- The entire assigned chapter was examined
- Every major heading and subsection is represented
- Every numbered and displayed equation was inventoried and reconciled
- Every mechanism-, calculation-, rule-, output-, and parameter-defining formula was captured
- No mathematical relationship is represented only in prose when the source supplies its equation
- Every formula’s symbols are defined
- Equation-number sequences were checked for unexplained gaps
- Assumptions and exceptions were retained
- Every numbered example was inventoried and reconciled
- Example-number sequences were checked for unexplained gaps
- Figures, tables, algorithms, and code blocks were inventoried and reconciled
- Source locators are present wherever available
- No unsupported information was introduced
- The output contains only this chapter
- The Markdown is valid and internally consistent
- `status` is `needs-review` rather than `extracted` if any inventory item remains unresolved

Finish by reporting the output file path, the counts of inventoried equations/examples/figures/tables, and any unresolved extraction issues or numbering gaps.
