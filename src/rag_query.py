import os
import requests
import argparse

import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
from src.ingestion.pdfloader import load_pdf, chunk_text
from src.retrieval.vector_store import load_index


from src.llm.local_llm import LocalLLM
from src.llm.llama_api import LlamaAPI

USE_API_LLM = False  # change to True when needed to use API based model 


from transformers import pipeline

# Load local LLM once
llm = pipeline(
    "text2text-generation",
    model="google/flan-t5-base",
    device=-1
)




# ---------------- CONFIG ----------------

EMBEDDING_MODEL_NAME = "all-MiniLM-L6-v2"
TOP_K = 3
HF_API_URL = "https://api-inference.huggingface.co/models/google/flan-t5-small"

HF_API_TOKEN = os.getenv("HF_API_TOKEN")


# ------------- HELPERS ------------------

def embed_query(query, model):
    embedding = model.encode([query])
    return np.array(embedding).astype("float32")


def retrieve_chunks(query_embedding, index, chunks):
    distances, indices = index.search(query_embedding, TOP_K)
    return [(i, chunks[i]) for i in indices[0]]




def generate_answer(context, question):
    prompt = (
        "You are a research assistant.\n"
        "Using ONLY the information in the context, list the limitations mentioned.\n"
        "If the context does not mention a limitation, do not invent one.\n\n"
        f"Context:\n{context}\n\n"
        f"Question:\n{question}\n\n"
        "Answer as bullet points:"
    )

    output = llm(
        prompt,
        max_new_tokens=120,
        do_sample=False,
        temperature=0.0
    )

    return output[0]["generated_text"]



# ------------- MAIN ---------------------

if __name__ == "__main__":
    
    

    if USE_API_LLM and HF_API_TOKEN is None:
        raise ValueError("HF_API_TOKEN not set for API LLM")


    # Load FAISS index
    index = load_index()
    if index is None:
        raise ValueError("FAISS index not found. Run vector_store.py first.")

    # Load PDF and chunks
    pdf_path = "data/papers/gen ai research.pdf"
    text = load_pdf(pdf_path)
    chunks = chunk_text(text)

    # Load embedding model
    model = SentenceTransformer(EMBEDDING_MODEL_NAME)

    # User question
    question = input("Ask a research question: ")

    # Embed question
    query_embedding = embed_query(question, model)

    # Retrieve chunks
    retrieved_chunks = retrieve_chunks(query_embedding, index, chunks)

    context = "\n\n".join([chunk_text for _, chunk_text in retrieved_chunks[:2]])
    
    
    



    llm = LlamaAPI() if USE_API_LLM else LocalLLM()

    # Generate answer
    answer = llm.generate(context, question)


    print("\n--- ANSWER ---\n")
    print(answer)
    
    
    print("\n--- SOURCES ---")
for chunk_id, _ in retrieved_chunks[:2]:
    print(f"[Chunk {chunk_id}]")



