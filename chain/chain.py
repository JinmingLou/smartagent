from langchain_classic.memory import ConversationSummaryMemory
from langchain_core.output_parsers import StrOutputParser

from prompt.prompt import getCommonPromptTemplate
from config.llmconfig import QwenModel
from rag.chromadb.chromaoperations import ChromaOperator
from rag.embedding.embedding import TxtEmbedder


class LlmChain():

    def __init__(self):
        self.llm = QwenModel().getModel()
        self.prompt = getCommonPromptTemplate()
        self.txt_embedder = TxtEmbedder()
        self.chroma_operator = ChromaOperator()
        self.output_parser = StrOutputParser()
        self.memory = ConversationSummaryMemory(
            llm=self.llm,
            memory_key="chat_history",
            return_messages=True
        )

    # 执行chain
    def invokeChain(self, question):
        # 从记忆中加载历史摘要
        memory_data = self.memory.load_memory_variables({})
        # 获取历史摘要文本
        chat_history = str(memory_data.get("chat_history", ""))
        print(f"聊天记录摘要: {chat_history}")
        # 检索
        embedding_model = self.txt_embedder.get_embedding_model()
        retrieve_result = self.chroma_operator.retrieve(message=question, embedding_model=embedding_model)
        # 提示词
        prompt = self.prompt
        # llm
        llm = self.llm
        # 输出
        output_parser = self.output_parser
        # chain
        chain = prompt | llm | output_parser
        # 执行并返回结果
        response = chain.invoke({
            "question": question,
            "information": retrieve_result,
            "chat_history": chat_history
        })
        # 保存记忆
        self.memory.save_context(
            {"input": question},
            {"output": response}
        )
        return response