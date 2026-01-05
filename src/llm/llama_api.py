import os
from groq import Groq
from src.llm.base import BaseLLM

class LlamaAPI(BaseLLM):
    def __init__(self):
        api_key = os.getenv("GROQ_API_KEY")
        if not api_key:
            raise ValueError("GROQ_API_KEY not set")

        self.client = Groq(api_key=api_key)

    def generate(self, context: str, question: str) -> str:
        messages = [
            {
                "role": "system",
                "content": "You are a research assistant. Use ONLY the provided context."
            },
            {
                "role": "user",
                "content": f"Context:\n{context}\n\nQuestion:\n{question}"
            }
        ]

        response = self.client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=messages,
            temperature=0.2,
            max_tokens=400
        )

        return response.choices[0].message.content
