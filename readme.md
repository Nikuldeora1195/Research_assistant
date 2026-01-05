# Automated Research Assistant (RAG-based)

This project is an Automated Research Assistant built using a Retrieval-Augmented Generation (RAG) pipeline.
It retrieves relevant context from academic research papers using semantic search (FAISS + embeddings)
and generates grounded answers using a modular LLM backend (local by default, API-based optional).






<img width="800" height="454" alt="Screenshot 2026-01-05 164025" src="https://github.com/user-attachments/assets/315f5b3b-82da-41bc-b0aa-d64c1c00a192" />






## Architecture Diagram

The LLM interface allows swapping between local and API-based models without changing retrieval logic.



                ┌──────────────────────┐
                │   Context Builder    │
                │ (Retrieved Chunks)   │
                └──────────┬───────────┘
                           │
                           ▼
                ┌──────────────────────┐
                │    LLM Interface     │
                │  (Pluggable Layer)   │
                └──────────┬───────────┘
                           │
              ┌────────────┴─────────────┐
              │                          │
              ▼                          ▼
      
         ┌─────────────────────┐   ┌────────────────────────────┐
         │  Local LLM           │   │  LLaMA-3.1-8B-Instant API   │
         │  (Default, Offline)  │   │  (Optional, Higher Quality) │
         └──────────┬───────────┘   └──────────┬─────────────────┘
                    │                          │
              └────────────┬─────────────┘
                           ▼
                ┌──────────────────────┐
                │  Answer + Citations  │
                │   (Chunk IDs)        │
                └──────────────────────┘




## Architecture Overview

The system follows a standard RAG pipeline:

1. PDF documents are ingested and converted to text.
2. Text is split into overlapping chunks to preserve context.
3. Each chunk is converted into embeddings using a sentence-transformer model.
4. Embeddings are stored in a FAISS vector database.
5. User queries are embedded and matched against stored vectors.
6. Retrieved chunks are passed to a local LLM for answer generation.
7. The generated answer is produced by a selectable LLM backend (local or API-based) and returned with source citations.



## LLM Backends

This project supports two interchangeable LLM backends:

- **Local LLM (default):**
  A lightweight, locally running instruction-tuned model used for zero-cost,
  reproducible execution and architectural demonstration.

- **API-based LLM (optional):**
  An optional integration with the LLaMA-3.1-8B-Instant model via an external API.
  This backend significantly improves explanation quality and reasoning depth,
  while keeping the retrieval and grounding pipeline unchanged.

The API-based LLM is optional, disabled by default, and can be enabled via configuration.
 The core RAG architecture does not depend on any external service.



Answer quality scales with the LLM backend, while retrieval correctness remains constant.






## Design Decisions

A local instruction-tuned model (FLAN-T5) is used as the default backend to ensure:

- Zero cost
- Reproducibility
- Stability without API dependency
- Clear demonstration of system design under resource constraints




## Installation & Usage

# Setup
      git clone <repo-url>
      cd research_assistant
      python -m venv venv
      venv\Scripts\activate   # Windows
      pip install -r requirements.txt

# Build Vector Index
      python -m src.retrieval.vector_store

# Run the Project
      python -m src.rag_query


Enter a research question to receive a grounded answer with citations.

## LLM Backend Selection

# Local LLM (default):
Runs offline, zero cost, no configuration needed.

# API-based LLaMA-3.1-8B-Instant (optional):
Provides clearer explanations and better reasoning.

# To enable API-based LLM:

      setx GROQ_API_KEY "your_api_key_here"


Then set in src/rag_query.py:

      USE_API_LLM = True

# Notes

API usage is optional and disabled by default.

Retrieval pipeline remains unchanged across LLM backends.





Future improvements include benchmarking answer quality across different LLM backends.
