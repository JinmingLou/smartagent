from langchain.tools import tool
from pydantic import BaseModel, Field

# 假设这是你的客户端
from tool.mysql.server_and_client.mysql_client import mcp_client


# 1. 定义输入模型 (对应原来的 parameters)
class QuerySalesInput(BaseModel):
    customer_code: str = Field(
        ...,
        description="客户的唯一识别代码",
        examples=["CUS123456", "VIP987654"]
    )


# 3. 定义 Tool
@tool(args_schema=QuerySalesInput, return_direct=False)
def query_sales_by_customer_code(customer_code: str) -> str:
    """
    根据客户代码查询指定客户的销售详情。

    返回包含区域、客户类型、客户姓名、产品名称、管理类别的数据。
    """

    # 确保服务已启动
    if not mcp_client.process:
        mcp_client.start()

    # 假设 mcp_client.call_tool 返回的是一个字典
    # Tool 会自动根据 QuerySalesOutput 模型进行格式校验和转换
    raw_result = mcp_client.call_tool(customer_code=customer_code)


    return raw_result