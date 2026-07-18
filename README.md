# Enterprise HR Knowledge Assistant (Work in Progress):
## Overview
An LLM-powered enterprise HR knowledge assistant that uses retrieval-augmented generation (RAG) to answer employee questions over internal HR documentation while enforcing role-based access controls to ensure privacy and policy adherence.

## Current Features:
- Document ingestion pipeline
- Semantic chunking
- Vector embeddings
- Retrieval-Augmented Generation (RAG)
- Role-based access filtering
- Mock enterprise HR document corpus


## Architecture

```text
HR Documents
      │
      ▼
 Chunking
      │
      ▼
 Embeddings
      │
      ▼
 Vector Store
      │
      ▼
Retrieve Relevant Documents
      │
      ▼
LLM Response
```

## In Progress:
- Retrieval evaluation
- Failure logging
- Response quality benchmarking
- Improved metadata filtering
- Tech Stack
- Python
- LangChain 
- Chroma
- OpenAI 
- OpenAI Embeddings 

## Motivation:
Built to explore how enterprise AI assistants can securely retrieve internal knowledge while respecting document-level permissions and minimizing hallucinations.
