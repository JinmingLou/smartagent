 这是个agent萌新尝试自己搭建agent

开发框架：langchain+langgraph
Llm：qwen3:4b（ollama部署）
多轮对话记忆组件：ConversationSummaryMemory

Rag部分：
Embedding：text2vec-base-chinese
向量数据库：chroma
文档loader：TextLoader 
分块策略：基于\n分割，分块大小300，重叠度50
Index：HNSW 索引，距离计算使用余弦相似度 (cosine)
检索召回次数：3
检索优化：todo

Tool部分：
开发协议：MCP
模式：stdio 本地启动server和client，通过进程间通信实现sql查询
可操作tools：数据查询

提供的能力：
1 支持导入业务txt说明文档并写入知识库
2支持根据知识库进行知识问答
3 todo 支持通过excel由大模型导入excel并写入数据库，并根据用户诉求进行数据查询与报表生成

效果：目前为了省钱，Llm，Embedding等都是跑在本地。。等调得好些了再上付费模型
