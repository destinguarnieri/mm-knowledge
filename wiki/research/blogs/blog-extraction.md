You are extracting durable, structured knowledge from a blog source for the Money Machine knowledge base.

## Assignment

Process only the blog article, series, or bounded collection provided to you.

Read every assigned page completely, including relevant captions, footnotes, tables, code blocks, diagrams, and author-supplied updates or corrections.

Do not expand the assignment to unrelated posts. Do not use outside knowledge unless explicitly instructed. Do not invent missing information. Flag inaccessible, ambiguous, incomplete, or unsupported material rather than guessing.

## Inputs

- **Source URL or supplied content:** `<URL, file, or content>`
- **Scope:** `<single article | named series | explicit URL list | bounded section of a blog>`
- **Knowledge-base root:** `<path to knowledge base>`
- **Preferred destination:** `<optional output directory>`
- **External-link policy:** `<do not follow | follow only essential supporting links | follow all author-cited primary sources>`
- **As-of date:** `<YYYY-MM-DD>`

If the scope is not explicit, process only the supplied page. Do not crawl the entire website.

## Objective

Create structured Markdown content that allows a future agent to:

- understand the author’s central thesis and reasoning
- identify the important concepts, claims, models, and methods
- distinguish evidence from opinion, speculation, and inference
- locate every important idea in the original source
- evaluate assumptions, limitations, and time-sensitive claims
- apply relevant knowledge without rereading the entire source
- connect the extracted knowledge to the existing wiki graph without duplicating established pages

This is not a shallow summary or a transcript. Preserve the reasoning and operational detail that make the source useful.

## Knowledge-base rules

Before writing:

1. Read the knowledge base’s `AGENTS.md`.
2. Start with `wiki/index.md`.
3. Search the existing knowledge base for the source, author, major concepts, and likely destination pages.
4. Retrieve the relevant existing pages before deciding whether to create or update content.
5. Follow important `[[wikilinks]]` and backlinks where needed to understand existing knowledge.
6. Prefer updating a relevant existing page over creating a duplicate.
7. Keep source-derived knowledge distinct from established Money Machine decisions, verified research results, and current operating state.

Follow all repository-specific rules for file placement, indexes, changelogs, link checking, and search-index updates.

## Source boundaries

Treat the assigned blog content as a source, not as automatically verified truth.

Clearly distinguish:

- **Author claim:** explicitly asserted by the author
- **Reported evidence:** data, citations, examples, experiments, or observations offered in support
- **Author interpretation:** the author’s explanation of what the evidence means
- **Author opinion or recommendation:** a judgment, preference, or proposed action
- **Agent inference:** a connection required to synthesize the material but not explicitly stated
- **Money Machine implication:** a possible application to the company, clearly labeled and never presented as an adopted decision
- **Externally verified fact:** include this category only if external verification was explicitly authorized and performed

Do not silently convert an author’s claim into an objective fact.

## Blog-specific provenance

Capture, where available:

- article title
- author or organization
- canonical URL
- publication date
- last-updated date
- date accessed
- blog or publication name
- article type, such as essay, tutorial, research note, announcement, opinion, case study, or postmortem
- series name and position in the series
- version, correction, or update notices
- disclosed affiliations, incentives, sponsorships, or conflicts
- referenced datasets, repositories, papers, products, or prior posts
- whether the page appears dynamic or likely to change

If the same article is syndicated or reposted, prefer the canonical source and record the relationship.

Do not infer publication or update dates from unreliable page elements. Use `unknown` when necessary.

## Extraction requirements

Capture all source-supported material needed to understand and use the assigned content, including:

- the source’s purpose, audience, and central thesis
- the problem or question being addressed
- every major claim and conclusion
- concepts, definitions, terminology, frameworks, and mental models
- the structure of the author’s argument
- evidence offered for each important claim
- examples, anecdotes, case studies, experiments, and counterexamples
- methods, procedures, algorithms, checklists, and decision rules
- formulas, variables, units, and validity conditions
- code, pseudocode, configurations, or commands when conceptually important
- quantitative results and how they were produced
- assumptions, prerequisites, constraints, and boundary conditions
- caveats, exceptions, limitations, and failure modes
- uncertainties or unresolved questions acknowledged by the author
- alternative views or objections discussed by the author
- recommendations and the conditions under which they apply
- diagrams, figures, tables, and embedded media
- corrections, updates, and material changes made after publication
- explicit relationships to other posts or sources
- durable implications relevant to Money Machine
- claims that are time-sensitive or require independent validation

Do not preserve incidental detail merely because it appears in the source. Preserve detail that supports understanding, evaluation, reproduction, or application.

## Claim and evidence analysis

For every major claim, record:

1. **Claim:** a precise paraphrase of what the author asserts
2. **Claim type:** factual, causal, predictive, normative, methodological, experiential, or speculative
3. **Support:** the evidence or reasoning supplied
4. **Evidence type:** data, citation, experiment, worked example, anecdote, authority, logical argument, or unsupported assertion
5. **Scope:** the population, market, system, timeframe, or conditions to which the claim applies
6. **Assumptions:** stated and materially implied assumptions
7. **Confidence:** how strongly the source itself supports the claim
8. **Limitations:** weaknesses, missing controls, conflicts, or unanswered questions visible from the supplied material
9. **Source locator:** heading, anchored URL, paragraph description, figure, timestamp, or other reliable locator

Use cautious language. For example, “The author argues…” or “The post reports…” is preferable to presenting a contested claim as settled fact.

Do not perform a full peer review unless requested, but identify obvious gaps between a claim and its stated support.

## Source traceability

Attach a reliable locator to every major claim, concept, method, example, formula, figure, and table.

Use the most precise available locator:

- anchored section URL
- section or subsection heading
- figure or table identifier
- numbered item
- video or audio timestamp
- supplied page or paragraph number

Examples:

`Source: “Transaction Costs” section`

`Source: https://example.com/post#transaction-costs`

`Source: Figure 3`

`Source: 18:42–20:10`

Never fabricate a locator.

When extracting multiple posts, identify the specific article for every locator.

## Hyperlinks and cited sources

Classify important outbound links as:

- foundational source
- supporting evidence
- dataset or code
- related explanation
- commercial or promotional material
- contextual but nonessential

Follow external links only according to the provided external-link policy.

If a linked source was not opened, write:

`Linked but not independently reviewed: <URL>`

Do not attribute the linked source’s contents based only on how the blog describes it.

## Formula and quantitative handling

Transcribe important formulas exactly using LaTeX:

- Inline mathematics: `$...$`
- Display mathematics: `$$...$$`

For each important formula include:

1. the formula
2. every symbol’s definition
3. units and domains where available
4. its purpose
5. assumptions and validity conditions
6. the author’s interpretation
7. calculation steps from any worked example
8. a source locator

Never silently correct a formula or numerical result. Preserve the source version and add a clearly labeled extraction note if it appears inconsistent.

For reported results, capture enough methodology to interpret them:

- dataset or sample
- period
- inclusion and exclusion criteria
- baseline or comparison
- metric definition
- costs or adjustments
- relevant parameters
- uncertainty measures, if supplied
- known sources of selection bias or leakage discussed or evident in the source

Do not imply reproducibility when required details are absent.

## Code and procedures

Do not copy large code listings unless the code itself is the assigned source material and retention is necessary.

Prefer to record:

- what the code or procedure does
- required inputs and dependencies
- outputs and side effects
- important steps
- parameters and defaults
- assumptions
- error and failure behavior
- security or operational warnings
- version-sensitive dependencies
- the smallest essential excerpt, if needed

Preserve exact syntax only when correctness depends on it.

## Figures, tables, and embedded media

For each important item record:

- identifier or descriptive title
- medium: figure, table, chart, diagram, image, video, audio, or interactive element
- what it contains
- axes, variables, units, legends, or categories
- the conclusion the author draws
- what the item actually establishes
- accessibility or interpretation limitations
- source locator

Do not claim to reproduce an item if you only describe it.

If important meaning exists only in an inaccessible embed, record it as an extraction issue.

## Time sensitivity

Flag information likely to become stale, including:

- prices and market conditions
- performance results
- software versions and APIs
- laws, regulations, or policies
- company personnel or product capabilities
- vendor terms
- links to live dashboards
- recommendations dependent on a particular environment

For each time-sensitive item, record the source publication or update date and the relevant as-of date when known.

Do not merge stale operational details into canonical runbooks without validation.

## Copyright and quotation

Paraphrase by default.

Use direct quotations only when the author’s exact wording is necessary to preserve a definition, qualification, or distinctive claim. Keep quotations short and attach an exact source locator.

Do not reproduce the article, a substantial portion of it, or long sequences of closely paraphrased text.

## Synthesis and knowledge-graph integration

After extraction:

1. Compare the extracted concepts with existing wiki pages.
2. Identify whether each durable item should:
   - update an existing canonical page
   - become a new source note
   - become a new reusable concept page
   - remain only in the source note
   - be omitted as non-durable or irrelevant
3. Add `[[wikilinks]]` to important existing pages.
4. Add a short “Related Knowledge” section linking the source note to relevant concepts, research, decisions, vendors, or projects.
5. Avoid creating multiple thin pages when one coherent page is more useful.
6. Do not modify current decisions, checkpoints, or operating policy merely because a blog recommends something.
7. Treat proposed Money Machine applications as hypotheses until independently evaluated and adopted.

## Required output

Unless the knowledge-base rules specify another location, create a source note at:

`wiki/research/blogs/<author-or-publication>/<yyyy-mm-dd>-<short-kebab-case-title>.md`

If no reliable publication date exists, use:

`wiki/research/blogs/<author-or-publication>/undated-<short-kebab-case-title>.md`

For a multi-post series, create:

```text
wiki/research/blogs/<author-or-publication>/<series-slug>/
  index.md
  <yyyy-mm-dd>-<article-slug>.md
  ...
```

Create or update separate concept pages only when the material is durable, reusable across sources, and substantial enough to justify canonical treatment.

## Source-note structure

Use this structure:

---
title: "<Article title>"
author: "<Author or organization>"
publication: "<Blog or publication>"
published: "<YYYY-MM-DD or unknown>"
updated: "<YYYY-MM-DD or unknown>"
accessed: "<YYYY-MM-DD>"
canonical_url: "<URL>"
source_type: "<essay | tutorial | research-note | announcement | opinion | case-study | postmortem | other>"
series: "<Series name or null>"
status: "extracted"
verification: "<source-only | partially-verified | externally-verified>"
tags:
  - "<relevant-tag>"
---

# <Article title>

## Source Overview

Briefly identify the source, intended audience, subject, purpose, and why it may be useful.

## Executive Synthesis

Provide an information-dense explanation of the central thesis, reasoning, conclusions, and most important qualifications.

## Author’s Argument

Describe the argument in logical order:

1. problem or premise
2. intermediate claims
3. evidence or reasoning
4. conclusion
5. recommendation, if any

Preserve uncertainty and distinguish explicit reasoning from inferred connections.

## Key Concepts

### <Concept name>

**Definition:** ...

**Explanation:** ...

**Significance:** ...

**Assumptions and boundaries:** ...

**Relationships:** ...

**Source:** ...

## Claims and Evidence

### <Claim name>

- **Claim:** ...
- **Type:** ...
- **Support provided:** ...
- **Evidence type:** ...
- **Scope:** ...
- **Assumptions:** ...
- **Limitations:** ...
- **Source-supported confidence:** `<strong | moderate | weak | unsupported>`
- **Source:** ...

## Methods and Procedures

### <Method name>

**Purpose:** ...

**Inputs and prerequisites:** ...

**Procedure:**

1. ...
2. ...
3. ...

**Outputs:** ...

**Decision points:** ...

**Failure conditions and warnings:** ...

**Source:** ...

## Formulas and Quantitative Results

### <Formula, experiment, or result name>

Include formulas, variables, units, methodology, result, interpretation, assumptions, and source locator.

## Examples and Case Studies

### <Example name>

Include the situation, method or intervention, observed outcome, author’s interpretation, limitations, and source locator.

Do not generalize an anecdote beyond what it supports.

## Figures, Tables, and Media

Describe each important item and its evidentiary role.

## Assumptions, Limitations, and Counterarguments

Record qualifications that could materially change the interpretation or application of the source.

## Recommendations

For each recommendation include:

- recommended action
- intended audience
- conditions under which it applies
- expected benefit
- tradeoffs or risks
- strength of supporting evidence
- source locator

## Time-Sensitive Information

List facts or recommendations requiring future revalidation and state their relevant dates.

## Money Machine Relevance

### Potentially Applicable Ideas

Describe source-supported ideas that might be useful to Money Machine.

### Required Validation

State what would need to be checked, reproduced, backtested, or decided before application.

### Conflicts or Tensions

Identify any conflict with existing Money Machine evidence, architecture, policy, safety constraints, or decisions. Link the relevant wiki pages.

Do not present this section as an adopted plan or decision.

## Related Knowledge

- [[existing/page|Descriptive relationship]]
- [[another/page|Descriptive relationship]]

## Glossary

| Term | Definition in this source | Source |
|---|---|---|
| ... | ... | ... |

## References and Links

For each material link include its title, URL, role, and whether it was independently reviewed.

## Open Questions and Extraction Issues

Record:

- inaccessible or missing content
- ambiguous language or notation
- unsupported claims
- broken or unreviewed links
- unclear publication history
- inaccessible embeds
- suspected inconsistencies
- questions requiring domain review
- claims requiring independent verification

## Extraction quality control

Before finishing, verify that:

- every assigned article was read completely
- no unassigned posts were silently included
- the author’s thesis and argument structure are represented
- every major claim is paired with its stated support
- author claims, evidence, opinion, and agent inference remain distinct
- important methods, formulas, examples, figures, and tables are covered
- reliable source locators are attached wherever available
- external links are labeled as reviewed or unreviewed
- time-sensitive information is dated and flagged
- recommendations retain their original conditions and caveats
- no unsupported information was introduced
- quotations are limited and necessary
- existing wiki pages were checked before creating new ones
- new pages add durable value rather than documentation volume
- Money Machine implications are labeled as hypotheses, not decisions
- Markdown, frontmatter, and `[[wikilinks]]` are valid
- required knowledge-base maintenance steps were completed

Finish by reporting:

1. files created
2. files updated
3. source pages processed
4. external sources reviewed
5. unresolved extraction or verification issues
6. any suggested follow-up validation, without performing it unless authorized