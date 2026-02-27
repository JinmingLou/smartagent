import json
import sys

from tool.mysql.cursor.mysql_cursor import MysqlCursor


def send_json(message):
    json_str = json.dumps(message, ensure_ascii=False)
    # --- 必须加上这行头部 ---
    # header = f"Content-Length: {len(json_str)}\r\n\r\n"
    # sys.stdout.write(header)
    print(json_str, file=sys.stderr)
    sys.stdout.write(json_str + "\n")
    sys.stdout.flush()


def main():
    # # 1. 发送 Server Info (初始化握手)
    # send_json({
    #     "type": "init",
    #     "version": "1.0",
    #     "name": "sales-db-tool",
    #     "description": "查询销售数据的 MCP 工具"
    # })
    #
    # # 2. 定义工具列表 (告诉客户端/模型有哪些工具可用)
    # tools = [
    #     {
    #         "name": "query_sales_by_customer_code",
    #         "description": "根据客户编码查询销售明细数据",
    #         "input_schema": {
    #             "type": "object",
    #             "properties": {
    #                 "customer_code": {"type": "string", "description": "客户编码，例如 '1900010454'"}
    #             },
    #             "required": ["customer_code"]
    #         }
    #     }
    # ]
    #
    # send_json({"type": "tools", "tools": tools})

    cursor = MysqlCursor()

    # 3. 主循环：监听 stdin 输入
    print("\nMCP Server 启动，正在监听输入...", file=sys.stderr)

    for line in sys.stdin:

        print(f"{line}", file=sys.stderr)

        if not line.strip():
            print("\n检测到空行，跳过", file=sys.stderr)
            continue

        line = line.strip()
        if not line:
            continue

        try:
            request = json.loads(line)

            # 检查是否是调用工具的请求
            if request.get("type") == "call":
                tool_name = request.get("name")
                params = request.get("arguments", {})

                if tool_name == "query_sales_by_customer_code":
                    result_data = cursor.query(customer_code=params.get("customer_code"))
                    print(result_data, file=sys.stderr)

                    # 返回结果
                    send_json({
                        "type": "result",
                        "call_id": request.get("call_id"),  # 如果协议要求回传 ID
                        "content": result_data
                    })
                else:
                    send_json({"type": "error", "content": "未知的工具名称"})

        except json.JSONDecodeError:
            send_json({"type": "error", "content": "输入的 JSON 格式错误"})
        except Exception as e:
            send_json({"type": "error", "content": str(e)})

if __name__ == "__main__":
    main()