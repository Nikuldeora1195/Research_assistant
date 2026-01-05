class BaseLLM:
    def generate(self, context: str, question: str) -> str:
        raise NotImplementedError
