import os
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
from src.ingestion.pdfloader import load_pdf, chunk_text


EMBEDDING_MODEL_NAME = "all-MiniLM-L6-v2"
VECTOR_DIMENSION = 384
INDEX_PATH = "data/faiss.index"


def create_embeddings(chunks, model):
    """
    Converts text chunks into embeddings.
    """
    embeddings = model.encode(chunks)
    return np.array(embeddings).astype("float32")


def build_faiss_index(embeddings):
    """
    Builds a FAISS index from embeddings.
    """
    index = faiss.IndexFlatL2(VECTOR_DIMENSION)
    index.add(embeddings)
    return index


def save_index(index):
    faiss.write_index(index, INDEX_PATH)


def load_index():
    if os.path.exists(INDEX_PATH):
        return faiss.read_index(INDEX_PATH)
    return None


if __name__ == "__main__":
    pdf_path = "data/papers/gen ai research.pdf"

    # 1. Load & chunk PDF
    text = load_pdf(pdf_path)
    chunks = chunk_text(text)

    print(f"Total chunks: {len(chunks)}")

    # 2. Load embedding model
    model = SentenceTransformer(EMBEDDING_MODEL_NAME)

    # 3. Create embeddings
    embeddings = create_embeddings(chunks, model)
    print("Embeddings shape:", embeddings.shape)

    # 4. Build FAISS index
    index = build_faiss_index(embeddings)

    # 5. Save index
    save_index(index)
    print("FAISS index saved successfully.")
