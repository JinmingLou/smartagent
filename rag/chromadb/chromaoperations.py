import os

import chromadb
from langchain_community.vectorstores import Chroma
from langchain_text_splitters import RecursiveCharacterTextSplitter

from document.ragdocuments.txt.loadtxt import TxtLoader
from rag.embedding.embedding import TxtEmbedder


class ChromaOperator():

    def save_txt(self, file_name, embedding_model):

        # 切块规则，txt是自定义写入文本，按\n切换语义，分块基于\n进行切割
        splitter = RecursiveCharacterTextSplitter(
            separators=["\n", "\n\n", " ", ""],
            chunk_size=300,
            chunk_overlap=0,
        )
        # 执行切块
        documents = TxtLoader().doLoad(file_name);
        splitted_documents = splitter.split_documents(documents)

        print(f"文档切分完成，共得到 {len(splitted_documents)} 个文本块。")

        # 获取持久化客户端
        client = chromadb.PersistentClient(path=self.get_chroma_db_dir())

        # 使用 HNSW 索引，距离计算使用余弦相似度 (cosine)
        collection_metadata = {
            "hnsw:space": "cosine",  # 可选: "l2", "ip", "cosine"
        }

        client.get_or_create_collection(
            name="my_documents",
            metadata=collection_metadata
        )

        # 创建 Chroma 向量数据库并保存
        vectorstore = Chroma.from_documents(
            documents=splitted_documents,
            embedding=embedding_model,
            persist_directory=self.get_chroma_db_dir(),  # LangChain 自动使用此路径
            collection_name="my_documents"  # 必须显式指定集合名
        )

        # 持久化
        vectorstore.persist()
        print(f"文档向量保存完成。")

    # 执行检索
    def retrieve(self, message, embedding_model):
        vectorstore = Chroma(
            persist_directory=self.get_chroma_db_dir(),
            embedding_function=embedding_model
        )
        # 执行相似性检索
        docs_and_scores = vectorstore.similarity_search_with_relevance_scores(message, k=3)

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
    operator.save_txt(file_name=file_name, embedding_model=embedding_model)
    # operator.retrieve(message="明细excel是销售管理分析销售情况常用的表", embedding_model=embedding_model)
