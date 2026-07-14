---
title: "Application of Large Language Models and Generative AI in Trading"
chapter: 9
source: "Hands-On AI Trading with Python, QuantConnect, and AWS"
source_file: "/Users/destinguarnieri/Desktop/Hands-On AI Trading with Python QuantConnect and AWS.epub/OPS/c009.xhtml"
status: "extracted"
---

# Chapter 9: Application of Large Language Models and Generative AI in Trading

## Overview

This chapter treats generative AI primarily as an equity-research productivity tool. LLMs can search, summarize, classify, generate text, and answer questions over research reports, transcripts, presentations, and industry material, allowing analysts to spend less time locating information and more time evaluating it. The chapter develops a practical sequence: select a model for the use case and budget; improve it through prompt engineering; ground it with retrieval-augmented generation (RAG); monitor hallucinations; and deploy through services such as SageMaker Canvas, Bedrock, or enterprise assistants. Marriott and Hyatt research reports demonstrate grounded stock analysis, competitive comparison, and summarization. Source: pp. 341–360.

## Learning Objectives (inferred)

- Explain how generative AI can expand the breadth and depth of investment research.
- Select an LLM using task-specific benchmarks, proprietary tests, and cost/performance analysis.
- Apply zero-shot, few-shot, system, chain-of-thought, and tree-of-thought prompting.
- Construct prompts from instructions, context, and an explicit output format.
- Reduce hallucinations with deterministic settings, grounding, abstention instructions, and monitoring.
- Describe and implement the S3–Kendra–SageMaker Canvas RAG workflow.
- Evaluate RAG infrastructure costs and shut down idle resources.
- Use grounded LLM output for single-company analysis, competitive screening, and document summarization.
- Compare ChatGPT, Gemini, Bedrock, SageMaker, and Amazon Q Business. Source: pp. 341–360.

## Key Concepts

### Role of Generative AI in Creating Alpha

The scarce input in fundamental research is analyst time. Relevant evidence is distributed across analyst reports, investor presentations, earnings materials, industry research, and competitor disclosures. LLM applications lower the manual effort required for summarization, question answering, classification, and text generation. The proposed “alpha” is initially an information-processing edge: cover more companies and industries, find pertinent evidence faster, and allocate more time to analysis. The chapter does not demonstrate that LLM output alone produces excess trading returns; human validation and investment judgment remain necessary. Source: p. 341.

### Selecting an LLM for Building a Generative AI Application

No model dominates every task or data type because model families differ in training corpora, architecture, parameters, and learned relationships. Within an unfine-tuned family, larger models generally perform better and cost more; newer generations of equal size generally outperform older ones. Thus a base Llama 3 70B would normally understand more complex relationships than base Llama 3 8B. These are heuristics, not guarantees. Source: pp. 342–343.

A smaller model fine-tuned on proprietary domain data may match or exceed a larger general base model. However, fine-tuning itself can be very expensive, so smaller does not automatically mean cheaper end to end. The recommended escalation path is:

1. Improve the prompt.
2. Add RAG for grounded Q&A/chat.
3. Fine-tune only in exceptional, terminology-heavy expert domains where the first two methods are inadequate—for example, biology, medicine, or law. Source: p. 342.

For conversational or question-answering applications, choose an **Instruct** model where available. Providers tune these variants to follow directions, retain prior conversational context, and perform multi-turn interactions better than the corresponding base model. Source: pp. 342–343.

#### Three-step model-selection procedure

1. **Leaderboard screening:** choose high-performing candidates from leaderboards aligned to the intended task.
2. **Proprietary evaluation:** test candidates on representative private data using several prompt designs.
3. **Performance/cost selection:** choose the model that offers an acceptable result at sustainable inference cost. Source: pp. 343–344.

#### Table 9.1 — Leaderboards by use case

| Use case | Suggested leaderboard(s) |
|---|---|
| Chatbot, Q&A, multi-turn conversation | Chatbot Arena; HELM Instruct |
| General/multipurpose | MMLU; HELM Lite; Hugging Face Open LLM; AlpacaEval |
| Embeddings | Massive Text Embedding Benchmark (MTEB) |
| Emotional intelligence | EQ Bench |

Leaderboards are starting filters because each benchmark has a niche; they do not replace testing on the actual investment workflow. Source: Table 9.1, p. 343.

#### Table 9.2 — Bedrock on-demand token pricing in the source

The figures below are explicitly dated June 2024 and should be treated as historical examples, not current quotes. Prices are per 1,000 input/output tokens. Source: Table 9.2, pp. 343–344.

| Family/model | Input | Output |
|---|---:|---:|
| Claude 3.5 Sonnet | $0.0030 | $0.0150 |
| Claude 3 Opus | $0.0150 | $0.0750 |
| Claude 3 Haiku | $0.0003 | $0.0013 |
| Claude 3 Sonnet | $0.0030 | $0.0150 |
| Claude 2.1 | $0.0080 | $0.0240 |
| Claude 2.0 | $0.0080 | $0.0240 |
| Claude Instant | $0.0008 | $0.0024 |
| Llama 3 Instruct 8B | $0.0003 | $0.0006 |
| Llama 3 Instruct 70B | $0.0027 | $0.0035 |
| Llama 2 Chat 13B | $0.0008 | $0.0010 |
| Llama 2 Chat 70B | $0.0020 | $0.0026 |
| Mistral 7B | $0.0002 | $0.0002 |
| Mixtral 8×7B | $0.0005 | $0.0007 |
| Mistral Small | $0.0010 | $0.0030 |
| Mistral Large | $0.0040 | $0.0120 |
| Cohere Command | $0.0015 | $0.0020 |
| Command-Light | $0.0003 | $0.0006 |
| Command R+ | $0.0030 | $0.0150 |
| Command R | $0.0005 | $0.0015 |
| Embed English | $0.0001 | N/A |
| Embed Multilingual | $0.0001 | N/A |

### Prompt Engineering

A prompt is the question, instruction, guidance, hint, example, or scenario supplied to elicit a desired output. Prompt engineering iteratively changes wording, context, examples, structure, and required format to teach the model how to perform the task. Clear, detailed directions and deliberate processing are the chapter's two central prompting tenets. Source: pp. 344–346.

#### Prompting methods

- **Zero-shot:** no examples. Appropriate for relatively simple tasks such as basic sentiment classification.
- **Few-shot:** typically two to eight examples that demonstrate the task and desired output format. Better for more complex or format-constrained tasks.
- **System prompting:** establishes role, persona, context, style, or tone—such as financial analyst, hedge-fund manager, judge, teacher, or assistant. The chapter highlights suitability for Llama-family models.
- **Chain-of-thought (CoT):** decomposes a task into sequential intermediate steps before forming the final response. For an earnings report, the suggested decomposition covers revenue, expense categories, margins/profit, cash flow/CapEx/working capital, and balance sheet, then combines them.
- **Tree of thought:** explores alternative paths and reevaluates them to seek a better solution. Source: pp. 344–345.

Figure 9.1 arranges these methods in increasing complexity: zero-shot → few-shot → system → chain of thought → tree of thought. Source: Figure 9.1, p. 345.

#### Prompt Engineering in Practice

A strong prompt combines three elements:

1. **Instruction:** task, such as summary or Q&A, plus any assumed role.
2. **Context:** evidence needed to perform the task, desired style/tone/specificity, and possibly a stepwise decomposition.
3. **Output format:** required structure—sentence, list, schema, or other form—and good examples when available. Source: pp. 345–346.

Evaluate the first response for instruction following and usefulness, then refine instructions, context, and examples until quality is acceptable. Figure 9.2 depicts a “good prompt” as the intersection of instruction, context, and output format. Source: Figure 9.2, p. 346.

#### Addressing Model Hallucination

Hallucinations are responses that are factually wrong, incoherent, or disconnected from supplied context. Creativity may be useful in fiction but can cause serious harm in financial analysis. The chapter recommends two control groups:

- **Reduce randomness:** lower temperature and top-p in SageMaker/Bedrock configuration. Lower values make output more deterministic and fact-oriented.
- **Strengthen grounding:** provide reliable facts; tell the model to use only supplied context; show examples of valid and invalid inferences; retrieve source documents from S3 through RAG; instruct the model to say when evidence is insufficient; and continuously monitor/evaluate responses. Source: pp. 346–347.

These techniques reduce hallucination but do not guarantee truth. Deterministic repetition of an unsupported statement is still wrong, so source verification remains necessary.

### Question Answering Using a Retrieval-Augmented Application in SageMaker Canvas

LLMs can locate an answer when both question and relevant passage fit in one input. Large research repositories exceed finite context windows, and models with larger windows usually cost more. RAG solves this by retrieving only passages relevant to the query and sending those passages plus the original prompt to the LLM. For an earnings-call question about organic revenue growth and currency effects, the retriever should find only the paragraphs addressing those topics. This improves context relevance and can improve factual accuracy. Source: pp. 347–348.

#### RAG components and query flow

1. A document database contains research materials.
2. An embedding model converts document text into numerical vectors.
3. A vector store indexes vectors so semantically similar content is nearby.
4. A question is embedded and matched against document vectors.
5. The most relevant passages are retrieved.
6. The original question and retrieved context are sent to the LLM.
7. The LLM composes a grounded answer. Source: p. 348.

Figure 9.3 shows the AWS realization: documents in S3; Kendra search/indexing; SageMaker/Canvas as the model/query layer; user question flowing through retrieval to response. Source: Figure 9.3, p. 348.

#### SageMaker Canvas setup workflow

The example repository contains March 2024 Marriott (MAR) and Hyatt (H) analyst reports with summaries, theses, developments, earnings/growth analysis, financial strength, risks, tables, and infographics. Source: pp. 348–349.

1. Upload PDF reports to an Amazon S3 bucket (Figure 9.4).
2. Use Amazon Kendra to extract/index document text and create vector-style search index `rag-index` (Figure 9.5).
3. In SageMaker domain/Canvas settings, enable document querying with Kendra so Canvas can retrieve indexed context (Figure 9.6). Source: pp. 349–350.

#### RAG Application Costs and Optimization Techniques

Table 9.3 assumes resources remain active for an entire month:

| Service | Tier/resource | Monthly price in source |
|---|---|---:|
| S3 | Standard storage, per GB | $0.02 |
| Kendra | Developer Edition index | $810 |
| SageMaker Canvas | Standard workspace instance | $1,368 |
| SageMaker Inference | `ml.G5.12xl` | $5,105 |

The fixed listed services total $7,283/month before multiplying S3 by stored GB and before other charges. Cost controls: log out of Canvas to release workspace resources; delete an unused Kendra index or disable auto-sync and run manual sync only when needed; stop model-hosting SageMaker instances; and delete unused development resources. Source: Table 9.3 and text, pp. 350–351.

### Testing the Infrastructure

Candidate families were Claude, Mistral, and Llama because the examples use AWS. Claude was removed because the workload was not complex enough to justify its higher cost. Mistral 7B and Llama 2 performed comparably; Llama-2-7b-instruct was chosen for a larger context window and stronger instruction/multi-turn behavior. This is an example-specific decision, not a universal ranking. Source: p. 351.

#### Example 1 — Analysis of Marriott International

The sequence deliberately increases prompt complexity. Source: pp. 351–354.

**Prompt 1: factual outlook.** A one-line request for Marriott's 2024 outlook returns a broadly positive view: RevPAR growth 3%–5%, adjusted EPS $9.15–$9.52, a raised EPS estimate of $9.72 from $9.61, and a 2025 estimate of $10.90, plus fee-based/corporate-travel strengths and risks from travel outlook and trimmed room-growth guidance. The output retrieves facts but offers limited investment judgment. Figure 9.7 shows this interaction in Canvas. Source: pp. 351–352.

**Prompt 2: role plus explicit factors.** Asking the model to act as a financial analyst and cover EBITDA, RevPAR, developments, growth, and risks produces a BUY recommendation with a $270 target. It cites 4%–5% RevPAR growth, 8%–10% EBITDA growth, global/loyalty/fee-based drivers, cautious guidance, and a stated 24.0× 2024 P/E versus a 31× peer average. System prompting makes the response more decision-oriented, but it still omits balance sheet, competitive position, industry trends, and sentiment and feels formulaic. Source: pp. 352–354.

**Prompt 3: model-generated analytical steps, then execution.** First ask the model to outline an investment process: financial statements, valuation multiples, historical/industry/competitive growth, cyclical/regulatory/geopolitical risk, and market sentiment. Then supply those steps and request advice with metrics. The response covers 4%–5% RevPAR, adjusted EPS $9.15–$9.52, EBITDA margin rising from 18.4% in 4Q22 to 19.6% in 4Q23, debt $11.9B, cash $300M, P/E 24.6× versus 26.1× industry, and P/B 4.3× versus 4.2×. The lesson is that staged CoT produces a more cohesive qualitative/quantitative framework. Source: p. 354.

#### Example 2 — Expanded Competitive Analysis Between Companies

Separate system prompts ask an experienced hedge-fund manager to form Hyatt and Marriott theses. Hyatt's thesis emphasizes balance sheet, brand portfolio, transition toward asset-light operations, debt/profitability benefits, digital/brand investment, removal of weak properties, retained pandemic savings, and growing distributions. Marriott's emphasizes fee-based income, loyalty/brand strength, liquidity, corporate travel, global expansion, rising costs/borrowing, and shareholder returns. Source: p. 355.

The next prompt compares decade room growth: Hyatt 4%–5% annually, Marriott about 4%, both above estimated U.S. industry supply growth of 1%–2%. A final multi-turn prompt asks which stock is better. The model favors Marriott in the near term, citing RevPAR, global reach, 7% global room share, and luxury leadership, while recognizing Hyatt's 38%-of-base pipeline and lower density of four rooms per U.S. market versus Marriott's 14. This demonstrates macro/micro competitive screening and retained context. Source: pp. 355–356.

**Important inconsistency.** The model first says Hyatt has higher decade room growth, then says Marriott has a slight edge “in terms of room growth estimates,” apparently switching from decade room growth to nearer-term RevPAR. This is exactly the kind of internal inconsistency that requires analyst review, even in grounded multi-turn output. Source: p. 356.

### Summarization

Summarization compresses large unstructured documents and can standardize them around decision-relevant attributes. The example uses Llama2-7b-chat in SageMaker Canvas on a Marriott analyst report and compares a generic prompt with a persona/context-rich prompt. Source: pp. 356–359.

#### Example — Summarize Analyst Report for Insights

**Prompt 1** asks for growth and risks. The response identifies 4Q23 adjusted EPS $3.57 versus $1.96, revenue +3% to $6.1B, low-teens base-management-fee growth, franchise fees +7%, RevPAR guidance 4%–5%, 1Q24 EBITDA $1.12–$1.15B, $4.5B returned to shareholders in 2023, and global expansion, alongside economic and operating-expense risks. The answer is truncated when context length is reached, demonstrating that summarization can still fail when input plus output exceeds model capacity. Source: pp. 357–358.

**Prompt 2** assigns the role of an experienced hedge-fund manager explaining the thesis to clients and explicitly asks for financial performance, market strength, and growth prospects. The response reorganizes evidence around 2023 adjusted EPS $9.99 (+36%), EBITDA margin 19.6% versus 18.4%, international RevPAR +17%, 1Q24 RevPAR guidance 4%–5%, long-term earnings growth forecast 12%, BBB debt rating, $11.9B debt, and $300M cash. The persona and audience create a contextual investment summary rather than a generic list. Source: pp. 358–359.

### Useful AI Platforms and Services

#### ChatGPT

OpenAI's ChatGPT offers a conversational UI and developer API. The source names GPT-3.5 Turbo, GPT-3.5, and GPT-4 and dates ChatGPT's release to November 2022. Its strength in this comparison is accessible high-performing text generation through both user and developer surfaces. Product/model references are historically situated to the book. Source: p. 359.

#### Gemini

Google DeepMind's Gemini family is integrated into Gmail, Docs, Sheets, and Search and is available by API. The source describes Ultra, Pro, and Nano sizes and multimodal support for text, images, audio, video, and code, supporting writing, planning, and learning. Source: p. 359.

#### Bedrock

Amazon Bedrock is a serverless, fully managed gateway to models from AI21 Labs, Anthropic, Cohere, Meta, Mistral AI, Stability AI, and Amazon through one API. It emphasizes model choice, AWS integration, security, privacy, and responsible-AI capabilities without managing inference infrastructure directly. Source: p. 359.

#### SageMaker

SageMaker provides managed build/train/deploy infrastructure. JumpStart is a model hub for discovery, experimentation, fine-tuning, and deployment through Studio or Python SDK. Canvas supplies a no-code interface and ready-to-use models from Bedrock and JumpStart. It is the most customizable of the AWS options described but can incur persistent workspace/inference costs. Source: pp. 359–360.

#### Amazon Q Business

Q Business is a managed, permissions-aware enterprise assistant that answers questions, summarizes, generates content, and performs tasks over company data with citations. The source also describes code generation, testing, debugging, and multistep planning/reasoning. Its distinguishing value is enterprise-data access control and citations rather than custom model training. Source: p. 360.

## Quantitative Relationships

### Token-to-text approximation

The table footnote gives rough planning conversions:

$$1\ \text{token}\approx0.75\ \text{word},\qquad 1\ \text{page}\approx1{,}000\ \text{tokens}.$$

Therefore a rough page contains about 750 words by the source's convention. Tokenization differs by model and content, so this is budgeting guidance, not an exact formula. Source: Table 9.2 footnote, p. 344.

### Request-cost estimate

For input tokens $T_i$, output tokens $T_o$, and per-1,000-token rates $P_i,P_o$:

$$C\approx\frac{T_i}{1000}P_i+\frac{T_o}{1000}P_o.$$

This relationship is inferred directly from the pricing units. It excludes infrastructure, retrieval, storage, fine-tuning, and other charges. Source: Table 9.2, pp. 343–344.

### Few-shot range

The chapter characterizes few-shot prompting as typically **2–8 examples**. More examples consume context and cost, so the correct number depends on task complexity and context-window capacity. Source: pp. 344–345.

### RAG monthly cost example

The fixed listed monthly resources sum to:

$$810+1{,}368+5{,}105=\$7{,}283,$$

plus S3 at $0.02 per stored GB and any unlisted usage. This is the full-month, always-on scenario in the source. Source: Table 9.3, p. 350.

## Methods and Procedures

### Model-selection workflow

1. Define task, data modality, context length, latency, privacy, and output requirements.
2. Consult a task-aligned leaderboard.
3. Shortlist several models, favoring Instruct variants for conversation/Q&A.
4. Build representative proprietary test cases and a quality rubric.
5. Try prompt variants before training.
6. Add retrieval when the answer must come from a document corpus.
7. Compare quality, token cost, infrastructure cost, and operational complexity.
8. Fine-tune only when distinctive domain knowledge remains unmet. Source: pp. 342–344.

### Prompt-refinement workflow

1. State the task and role.
2. Supply reliable context.
3. Specify required tone, detail, decision factors, and constraints.
4. Specify output schema and, for difficult formats, provide 2–8 examples.
5. Ask for a staged analytical plan when the task is complex.
6. Evaluate completeness, factual support, consistency, and instruction following.
7. Refine and repeat; retain an explicit abstention rule. Source: pp. 344–347.

### RAG/SageMaker workflow

1. Upload point-in-time research PDFs to S3.
2. Create and populate a Kendra index.
3. Connect Kendra document query to SageMaker Canvas.
4. Choose an instruction-following LLM after proprietary testing.
5. Submit a question; embed it and retrieve relevant passages.
6. Generate an answer from the question plus retrieved evidence.
7. Validate citations, numbers, dates, and cross-turn consistency.
8. Log out/stop/delete unused resources to limit idle charges. Source: pp. 347–351.

### Investment-research summarization workflow

1. Define audience and decision objective.
2. Request specific categories: growth, margins, balance sheet, valuation, catalysts, and risks.
3. Require key numbers and comparison periods.
4. Ask the model to separate source facts from interpretations.
5. Constrain format and length so output fits the context budget.
6. Check every number against the report and investigate omitted/truncated risks.
7. Treat summary as a screening aid, not a substitute for the full source. Source: pp. 356–359.

## Figures and Tables

1. **Figure 9.1:** increasing prompting complexity from zero-shot through tree of thought. Source: p. 345.
2. **Figure 9.2:** instruction, context, and output format overlap to form a good prompt. Source: p. 346.
3. **Figure 9.3:** AWS RAG architecture connecting S3, Kendra, SageMaker, Canvas, query, retrieval, and response. Source: p. 348.
4. **Figure 9.4:** S3 bucket/dashboard containing source reports. Source: p. 349.
5. **Figure 9.5:** Kendra wizard for creating/managing the document index. Source: p. 349.
6. **Figure 9.6:** SageMaker/Canvas setting enabling Kendra document query. Source: p. 350.
7. **Figure 9.7:** Canvas snapshot of grounded Marriott analysis. Source: p. 352.
8. **Table 9.1:** leaderboards mapped to model use cases. Source: p. 343.
9. **Table 9.2:** June 2024 Bedrock input/output token pricing across Anthropic, Meta, Mistral, and Cohere. Source: pp. 343–344.
10. **Table 9.3:** illustrative full-month RAG service costs and resource tiers. Source: p. 350.

The XHTML contains seven numbered image figures and three numbered table figures—ten figure elements total. Thus the user's “all 10 figures, and 3 tables” appears to count the three table figures within the ten; there are not ten image figures plus three additional tables in the source.

## Trading and Investment Applications

- Search large historical repositories of transcripts, reports, and industry research.
- Extract specific operating metrics and currency impacts from filings/calls.
- Build a structured single-stock thesis from financial, valuation, growth, risk, and sentiment evidence.
- Compare competitors on company-specific and industry-level drivers.
- Standardize report summaries for screening and monitoring.
- Classify text sentiment or themes before incorporating them into a separately tested signal.
- Expand analyst coverage while preserving human time for source validation and judgment. Source: pp. 341–359.

## Assumptions, Limitations, and Edge Cases

- Larger/newer base models are generally, not universally, better.
- Fine-tuned small-model economics must include training and maintenance, not only inference.
- Leaderboard rank may not transfer to proprietary financial documents.
- Context windows cap combined instructions, retrieved passages, and output; the summarization example is visibly truncated.
- Larger contexts tend to cost more and can still contain irrelevant material.
- RAG improves grounding only if retrieval finds the correct, current passage.
- PDFs with tables/infographics may extract poorly; retrieval over text may omit visual evidence.
- Multi-turn context can propagate earlier errors and produce contradictions, as in the Hyatt/Marriott room-growth comparison.
- Lower temperature/top-p reduces randomness, not factual error.
- Persona prompting can make unsupported opinions sound more authoritative.
- Historical prices and service descriptions in this chapter are dated and may change.
- Reports from March/May 2024 contain forecasts and opinions, not realized outcomes.
- Generated investment advice must be checked for source support, dates, units, and internal consistency. Source: pp. 342–360.

## Common Mistakes and Warnings

- Selecting a model solely from a generic leaderboard.
- Fine-tuning before exhausting prompts and retrieval.
- Omitting output format or examples for constrained tasks.
- Asking for an investment opinion without specifying required evidence categories.
- Treating eloquent model reasoning as proof of correctness.
- Failing to tell the model to abstain when evidence is insufficient.
- Leaving Canvas, Kendra, or inference instances running idle.
- Trusting a summary after it has hit the context/output limit.
- Confusing room growth with RevPAR growth or near-term with decade forecasts.
- Using generated recommendations directly for trading without independent validation, risk controls, and backtesting. Source: pp. 342–359.

## Key Takeaways

1. Generative AI's immediate investment edge is research throughput, not autonomous alpha.
2. Model choice is empirical: benchmark shortlist, test on private data, then evaluate total cost.
3. Prompting should precede RAG, and RAG should usually precede fine-tuning.
4. A useful prompt combines instruction, context, and explicit output format.
5. Grounding, low randomness, abstention, and monitoring reduce but do not eliminate hallucination.
6. RAG makes large proprietary repositories queryable within finite model context.
7. Multi-stage prompts can produce richer theses but can also magnify contradictions.
8. AWS no-code tooling accelerates prototypes, while idle infrastructure can be expensive.
9. Every generated metric and recommendation requires source-level verification. Source: pp. 341–360.

## Glossary

| Term | Definition | Source |
|---|---|---|
| Alpha | Investment edge; here primarily improved research speed, breadth, and insight discovery. | p. 341 |
| Chain-of-thought prompting | Decomposing a complex task into sequential intermediate steps. | p. 345 |
| Context window | Maximum combined input/context capacity accepted by a model. | pp. 347–348 |
| Embedding | Numerical representation used for semantic matching. | p. 348 |
| Few-shot prompting | Supplying a small set, typically 2–8, of task/output examples. | pp. 344–345 |
| Hallucination | Incorrect, incoherent, or context-disconnected model output. | pp. 346–347 |
| Instruct model | Variant tuned to follow directions and support multi-turn interaction. | pp. 342–343 |
| Kendra | AWS enterprise search/index service used as the retrieval layer. | p. 349 |
| RAG | Retrieval of pertinent source context before generation. | pp. 347–350 |
| System prompting | Setting role, persona, style, tone, and governing context. | p. 345 |
| Temperature | Sampling control; lower settings reduce randomness. | pp. 346–347 |
| Top-p | Probability-mass sampling control; lower values narrow token choices. | pp. 346–347 |
| Tree of thought | Exploring and reevaluating multiple reasoning paths. | p. 345 |
| Vector store | Index that supports similarity search over document embeddings. | p. 348 |
| Zero-shot prompting | Requesting a task without examples. | pp. 344–345 |

## Connections to Other Chapters

- Chapter 6's GPT-4 and FinBERT trading examples operationalize text sentiment, while this chapter focuses on research workflows and grounding.
- AWS storage, inference, and SageMaker deployment concepts support the RAG architecture presented here.
- Earlier backtesting and bias principles remain necessary before converting generated analysis into a trading signal. Source: pp. 341–360.

## Completeness Audit

- Full XHTML read across embedded print pages 341–360.
- All 18 source headings represented: chapter title; seven major sections; prompt practice; hallucination; RAG cost; infrastructure testing; two RAG examples; summarization example; and five platform subsections.
- All seven numbered image figures (9.1–9.7) captured.
- All three numbered tables (9.1–9.3) captured with every row/value.
- All ten `<figure>` elements accounted for: seven images plus three tables.
- All model-selection criteria, prompting methods, RAG components/setup, cost controls, infrastructure tests, summarization steps, platform comparisons, examples, numerical claims, limitations, and warnings represented.

## Extraction Issues

- The source title spells the first RAG example “Marriot”; this extraction uses the correct company name, Marriott.
- The source writes `Top005Fp`, evidently a rendering/encoding error for top-p.
- The Marriott/Hyatt comparison contradicts itself: Hyatt is stated to have higher decade room growth, but the final response claims Marriott has a room-growth edge while citing nearer-term RevPAR.
- The first summary output is explicitly truncated at the context limit, so its remaining risk discussion is unavailable.
- Table 9.2 pricing is dated June 2024; Table 9.3 is an illustrative always-on monthly configuration. Neither should be treated as current pricing.
- The chapter supplies generated claims but does not show passage-level citations for every figure in the model answers, so their factual accuracy cannot be independently established from this XHTML alone.
