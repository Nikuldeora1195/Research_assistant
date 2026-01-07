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



 ##     🐳 Dockerized Deployment

This project is containerized using Docker to ensure reproducible execution and environment consistency, especially when working with ML libraries such as FAISS and Transformers.

Docker is used only for packaging and deployment and does not affect the RAG pipeline logic, retrieval quality, or generation behavior.

# Why Docker?

Eliminates “works on my machine” issues

Packages Python version, dependencies, and models together

Enables one-command execution of the RAG pipeline

Keeps retrieval and generation logic unchanged

Build the Docker Image

#            From the project root:

             docker build -t rag-assistant .

     # Run the Container
docker run -it rag-assistant

# Using Groq API (Optional)

To enable the optional Groq API (LLaMA) backend, pass the API key as an environment variable:

      docker run -it -e GROQ_API_KEY=your_key rag-assistant


Local inference using FLAN-T5 remains the default and requires no API key.

   #   Notes

The FAISS index must be built before running the container:

python src/retrieval/vector_store.py


Docker is used for reproducibility, not orchestration

No Docker Compose or Kubernetes is required for this project












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





## Folder structure


  research_assistant/<br>
  ├── data/<br>
  │   └── papers/<br>
  ├── src/<br>
  │   ├── ingestion/<br>
  │   │   └── pdfloader.py<br>
  │   ├── retrieval/<br>
  │   │   └── vector_store.py<br>
  │   ├── llm/<br>
  │   │   ├── base.py<br>
  │   │   ├── local_llm.py<br>
  │   │   └── llama_api.py<br>
  │   └── rag_query.py<br>
  ├── evaluation.md<br>
  ├── requirements.txt<br>
  ├── README.md<br>
  ├── .gitignore<br>
  └── venv/<br>






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


### Using Custom Documents

To query a different document, replace the file located at:


with your own PDF file and keep the same filename (`gen ai research.pdf`).

The system will automatically ingest this document and build embeddings
when the vector index is created.






# Notes

API usage is optional and disabled by default.

Retrieval pipeline remains unchanged across LLM backends.


Future improvements include benchmarking answer quality across different LLM backends.
