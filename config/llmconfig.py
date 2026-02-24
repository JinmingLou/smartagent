from langchain_ollama import OllamaLLM

class QwenModel():
    def __init__(self):
        super().__init__()

    def getModel(self):
        return OllamaLLM(model='qwen3:4b')