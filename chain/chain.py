from langchain_core.output_parsers import StrOutputParser

from prompt.prompt import getCommonPromptTemplate
from config.llmconfig import QwenModel
from rag.chromadb.chromaoperations import ChromaOperator
from rag.embedding.embedding import TxtEmbedder


class LlmChain():

    def __init__(self):
        super().__init__()

    def invokeChain(self, question):
        # 检索
        embedding_model = TxtEmbedder().get_embedding_model()
        retrieveResult = ChromaOperator().retrieve(message=question, embedding_model=embedding_model)
        # 提示词
        prompt = getCommonPromptTemplate()
        # llm
        llm = QwenModel().getModel()
        # 输出
        output_parser = StrOutputParser()
        # chain
        chain = prompt | llm | output_parser
        # 执行并返回结果
        response = chain.invoke({"question": question, "information": retrieveResult})
        return response