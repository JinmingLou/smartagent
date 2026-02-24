import os

from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from document.ragdocuments.txt.loadtxt import TxtLoader

class TxtEmbedder():
    def __init__(self):
        pass

    # 获取embedding模型，这里使用本地模型
    def get_embedding_model(self):
        current_dir = os.path.dirname(__file__)
        model_path = os.path.join(current_dir, "models", "text2vec-base-chinese")
        return HuggingFaceEmbeddings(model_name=model_path)
