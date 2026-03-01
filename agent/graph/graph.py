from typing import TypedDict, Annotated, List, Literal
from langgraph.graph import StateGraph, END
from agent.intention_agent.intention_agent import intention_analyst

# 定义状态
class AgentState(TypedDict):
    input: str
    messages: Annotated[List, lambda x, y: x + y]
    next: Literal["intention_analyst", "rag_worker", "mysql_worker", "reviewer"]
    answer: str

def build_agent_graph():

    # 初始化
    builder = StateGraph(AgentState)

    # 意图识别
    builder.add_node("intention_analyst", intention_analyst)
    builder.add_conditional_edges(
        "intention_analyst",
        router,
    )

    # 起始节点
    builder.set_entry_point("intention_analyst")

    graph = builder.compile()

    return graph

# 路由下个节点，实际是next指向的节点，每个节点执行完会更新next节点
def router(state):
    return state.get("next", "reviewer")

