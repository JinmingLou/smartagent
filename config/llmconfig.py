from langchain_ollama import OllamaLLM
from langchain_community.chat_models import ChatTongyi

class OllamaModel():
    def __init__(self):
        super().__init__()

    def getModel(self):
        return OllamaLLM(model='qwen3:4b')

class QwenModel():

    def __init__(self):
        model='qwen-max'
        self.model=model

    def getModel(self, temperature):
        return ChatTongyi(
            model=self.model,
            api_key='sk-7858338b4f8045de94e22aabc24c02e9',
            temperature=temperature,
            base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",)