from langchain_core.prompts import ChatPromptTemplate, SystemMessagePromptTemplate, HumanMessagePromptTemplate

# 通用提示词模板
def getCommonPromptTemplate():

    system_message = "你是一个牛奶品牌销售管理专家，擅长牛奶经销商销售相关问题。你可以基于一些已知信息回答问题:{information}"
    user_message = "{question}"

    return ChatPromptTemplate.from_messages([
        ("system", system_message),
        ("human", user_message)
    ])