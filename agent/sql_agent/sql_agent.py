from langchain_classic.agents import AgentExecutor, create_openai_tools_agent

from agent.sql_agent.sql_agent_prompt import get_sql_agent_prompt
from config.llmconfig import QwenModel
from tool.agent_tools import query_sales_by_customer_code


def create_sql_agent_executor():

    # 初始化 LLM
    llm = QwenModel().getModel(temperature=0)

    tools = [query_sales_by_customer_code]

    agent = create_openai_tools_agent(
        llm=llm,
        tools=tools,
        prompt=get_sql_agent_prompt()
    )

    executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

    return executor


if __name__ == '__main__':
    executor = create_sql_agent_executor()
    result = executor.invoke({"input": "你能做什么"})
    print(result)