# mm-knowledge

Version-controlled knowledge base of Money Machine Labs, indexed with QMD.

## Agents

### QMD

Create collections for your notes, docs, and meeting transcripts
    qmd collection add ~/notes --name notes
    qmd collection add ~/Documents/meetings --name meetings
    qmd collection add ~/work/docs --name docs

    # Add context to help with search results, each piece of context will be returned when matching sub documents are returned. This works as a tree. This is the key feature of QMD as it allows LLMs to make much better contextual choices when selecting documents. Don't sleep on it!
    qmd context add qmd://notes "Personal notes and ideas"
    qmd context add qmd://meetings "Meeting transcripts and notes"
    qmd context add qmd://docs "Work documentation"

    # Generate embeddings for semantic search
    qmd embed

    # Search across everything
    qmd search "project timeline"           # Fast keyword search
    qmd vsearch "how to deploy"             # Semantic search
    qmd query "quarterly planning process"  # Hybrid + reranking (best quality)

    # Get a specific document
    qmd get "meetings/2024-01-15.md"

    # Get a document by docid (shown in search results)
    qmd get "#abc123"

    # Get multiple documents by glob pattern
    qmd multi-get "journals/2025-05*.md"

    # Search within a specific collection
    qmd search "API" -c notes

    # Export all matches for an agent
    qmd search "API" --all --files --min-score 0.3

    # Get structured results for an LLM
    qmd search "authentication" --json -n 10

    # List all relevant files above a threshold
    qmd query "error handling" --all --files --min-score 0.4

    # Retrieve full document content
    qmd get "docs/api-reference.md" --full