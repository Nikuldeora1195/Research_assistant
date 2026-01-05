from transformers import pipeline
from src.llm.base import BaseLLM

class LocalLLM(BaseLLM):
    def __init__(self):
        self.pipe = pipeline(
            "text2text-generation",
            model="google/flan-t5-base",
            device=-1
        )

    def generate(self, context: str, question: str) -> str:
        prompt = (
            "Answer the question using ONLY the context below.\n\n"
            f"Context:\n{context}\n\n"
            f"Question:\n{question}\n\n"
            "Answer:"
        )

        output = self.pipe(
            prompt,
            max_new_tokens=200,
            do_sample=False
        )

        return output[0]["generated_text"]
