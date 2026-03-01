from langchain_core.messages import AIMessage

from agent.intention_agent.intention_agent_prompt import get_intention_agent_prompt
from config.llmconfig import QwenModel

def intention_analyst(state):

    user_input = state["input"]

    prompt = get_intention_agent_prompt()

    llm = QwenModel().getModel(temperature=0)

    chain = prompt | llm

    result = chain.invoke({"input":user_input})

    raw_intent = result.content.strip()

    next = "reviewer"
    if (raw_intent == "咨询"):
        next = "rag_worker"
    elif (raw_intent == "按客户编码查询客户信息"):
        next = "mysql_worker"
    else:
        next = "reviewer"

    return {
        "messages": [AIMessage(content=f"意图分析器：识别到意图 '{raw_intent}'，交给manager处理")],
        "next": next
    }

if __name__ == '__main__':
    mock_state = {
        "input": "ssadsad？",
        "messages": [],
        "next": "Intention_analyst"
    }

    print("🚀 开始执行意图分析节点...\n")
    result = intention_analyst(mock_state)

    # 3. 打印输出结果
    print(f"  消息: {result['messages'][0].content}")
    print(f"  下一步: {result['next']}")