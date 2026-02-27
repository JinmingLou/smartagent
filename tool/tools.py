import os

from langchain.tools import tool
import subprocess
import json

from tool.mysql.server_and_client.mysql_client import mcp_client


@tool
def query_sales_by_customer_code(customer_code: str) -> str:
    """
    Query sales data by customer code using MCP protocol.
    Args:
        customer_code (str): The code of the customer.
    Returns:
        str: The sales data result.
    """
    # 确保服务已启动
    if not mcp_client.process:
        mcp_client.start()

    return mcp_client.call_tool(customer_code)