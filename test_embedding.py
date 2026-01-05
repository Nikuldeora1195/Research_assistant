from sentence_transformers import SentenceTransformer

# 1. Load a lightweight embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")

# 2. Example text (pretend this came from a research paper)
text = "Transformers are powerful models for natural language processing."

# 3. Generate embedding
embedding = model.encode(text)

# 4. Print results
print("Embedding length:", len(embedding))
print("First 10 values:", embedding[:10])
