from langchain_core.prompts import ChatPromptTemplate, SystemMessagePromptTemplate, HumanMessagePromptTemplate

# 通用提示词模板
def getCommonPromptTemplate():

    system_message = """你是一个牛奶品牌销售管理专家。
    已知相关信息如下:
    {information}
    
    以下是之前的对话摘要，用于提供上下文:
    {chat_history}
    
    请基于以上信息回答问题。"""

    user_message = "{question}"

    return ChatPromptTemplate.from_messages([
        ("system", system_message),
        ("human", user_message)
    ])