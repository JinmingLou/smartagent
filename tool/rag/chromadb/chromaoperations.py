import os

from langchain_community.vectorstores import Chroma
from langchain_experimental.text_splitter import SemanticChunker
from langchain_text_splitters import RecursiveCharacterTextSplitter

from document.ragdocuments.txt.loadtxt import TxtLoader
from tool.rag.embedding.embedding import TxtEmbedder


class ChromaOperator():

    def save_txt(self, file_name, embedding_model):

        # 切块规则，txt是自定义写入文本，按\n切换语义，分块基于\n进行切割
        text_splitter = SemanticChunker(
            embedding_model,  # 传入嵌入模型实例
            breakpoint_threshold_type="percentile",
            # 可选: "standard_deviation", "percentile", "interquartile", "gradient"
            breakpoint_threshold_amount=90  # 阈值，根据具体情况调整
        )
        # 执行切块
        documents = TxtLoader().doLoad(file_name);
        splitted_documents = text_splitter.split_documents(documents)

        print(f"文档切分完成，共得到 {len(splitted_documents)} 个文本块。")

        vectorstore = Chroma.from_documents(
            documents=splitted_documents,
            embedding=embedding_model,
            persist_directory=self.get_chroma_db_dir(),
            collection_name="my_documents",
            # --- 确保在这里传入 metadata ---
            collection_metadata={"hnsw:space": "cosine"}
        )

        # 持久化
        vectorstore.persist()
        print(f"文档向量保存完成。")

    # 执行检索
    def retrieve(self, message, embedding_model):
        vectorstore = Chroma(
            persist_directory=self.get_chroma_db_dir(),
            embedding_function=embedding_model,
            collection_name="my_documents"
        )
        # 执行相似性检索
        docs_and_scores = vectorstore.similarity_search_with_relevance_scores(message, k=3, score_threshold=0.5)

        # 提取内容并用分号连接
        # 使用集合去重（如果多个块内容一样），或者直接保留列表
        contents = [doc.page_content.strip() for doc, score in docs_and_scores]

        # 去重但保持顺序
        unique_contents = list(dict.fromkeys(contents))

        information = "; ".join(unique_contents) + "."

        print(f"检索到相关信息: {information}")
        return information

    def get_chroma_db_dir(self):
        current_dir = os.path.dirname(__file__)
        return os.path.join(current_dir, "db")

if __name__ == '__main__':
    file_name = "【经销进货+分子出库】说明.txt"
    embedding_model = TxtEmbedder().get_embedding_model()
    operator = ChromaOperator()
    # operator.save_txt(file_name=file_name, embedding_model=embedding_model)
    operator.retrieve(message="经销进货+分子出库", embedding_model=embedding_model)
