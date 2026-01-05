from pypdf import PdfReader

def load_pdf(file_path: str) -> str:
    """
    Reads a PDF file and returns all text as a single string.
    """
    reader = PdfReader(file_path)
    all_text = []

    for page in reader.pages:
        text = page.extract_text()
        if text:
            all_text.append(text)

    return "\n".join(all_text)


if __name__ == "__main__":
    pdf_path = "data/papers/gen ai research.pdf"  
    text = load_pdf(pdf_path)
    print("Total characters extracted:", len(text))
    print(text[:1000])  # preview first 1000 characters




def chunk_text(text, chunk_size=500, overlap=100):
    """
    Splits text into overlapping chunks.
    """
    chunks = []
    start = 0
    text_length = len(text)

    while start < text_length:
        end = start + chunk_size
        chunk = text[start:end]
        chunks.append(chunk)
        start = end - overlap

    return chunks


if __name__ == "__main__":
    pdf_path = "data/papers/gen ai research.pdf"  # update if needed
    text = load_pdf(pdf_path)

    chunks = chunk_text(text)

    print("\n\n\n\n\nTotal chunks created:", len(chunks))
    print("First chunk preview:\n", chunks[0][:500])

