You are extracting structured knowledge from one chapter of a textbook.

## Assignment

Process only the chapter provided to you. Read it completely and produce a self-contained Markdown study/reference file.

Do not rely on outside knowledge unless explicitly instructed. Do not invent missing information. If content is unclear, incomplete, or illegible, flag it rather than guessing.

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
- Mathematical formulas and equations
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

For every important formula, include:

1. The formula
2. A definition of every symbol
3. Its purpose
4. Its assumptions or validity conditions
5. A short interpretation
6. A worked example if one appears in the chapter

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
status: "extracted"
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

## Quality-control checklist

Before finishing, verify that:

- The entire assigned chapter was examined
- Every major heading and subsection is represented
- All important formulas were captured
- Every formula’s symbols are defined
- Assumptions and exceptions were retained
- Important examples, figures, and tables are covered
- Source locators are present wherever available
- No unsupported information was introduced
- The output contains only this chapter
- The Markdown is valid and internally consistent

Finish by reporting the output file path and any unresolved extraction issues.