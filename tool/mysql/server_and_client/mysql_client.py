import os
import json
import subprocess
import sys
from typing import Optional


class MysqlMcpClient:
    def __init__(self, server_script_path: str):
        self.server_script_path = server_script_path
        self.process: Optional[subprocess.Popen] = None

    def start(self):
        """启动 MCP Server 进程"""
        # 打开日志文件，确保编码为 utf-8
        log_file = open("server_runtime.log", "w", encoding="utf-8")

        if self.process is None or self.process.poll() is not None:
            print(f"启动 MCP Server: {self.server_script_path}")
            self.process = subprocess.Popen(
                [sys.executable, self.server_script_path],
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=log_file,  # 确保 stderr 被重定向到文件，防止缓冲区满
                text=True,
                encoding='utf-8',  # 关键：强制使用 utf-8 编码，解决 gbk 解码错误
                bufsize=1  # 行缓冲
            )
            print("MCP Server 启动成功，等待初始化...")
            # 可以在这里添加简单的逻辑读取初始化信息
        else:
            print(f"MCP Server 已启动: {self.server_script_path}")

    def stop(self):
        """停止 MCP Server 进程"""
        if self.process:
            print("正在停止 MCP Server...")
            # 先关闭 stdin，通知 server 结束
            self.process.stdin.close()
            self.process.terminate()
            self.process.wait()
            self.process = None
            print("MCP Server 已停止")

    def call_tool(self, customer_code: str) -> str:
        """
        通过 MCP 协议调用工具
        """
        if not self.process or self.process.poll() is not None:
            return "Error: MCP Server is not running."

        try:
            # --- 1. 构造请求 ---
            request = {
                "type": "call",
                "name": "query_sales_by_customer_code",
                "arguments": {
                    "customer_code": customer_code
                }
            }

            # --- 2. 发送请求 ---
            # 将字典转为 JSON 字符串
            content = json.dumps(request, ensure_ascii=False)
            # 写入 stdin
            self.process.stdin.write(content + "\n")  # 加上换行符，方便 server 读取
            # 必须 flush，否则数据可能卡在缓冲区里发不出去
            self.process.stdin.flush()
            print("已发送请求到 MCP Server...")

            # --- 3. 接收响应 ---
            # 读取 server 的一行输出
            response_line = self.process.stdout.readline()
            print(f"收到响应: {response_line.strip()}")

            if response_line:
                print(f"收到响应: {response_line.strip()}")
                try:
                    response_data = json.loads(response_line)
                    if "content" in response_data:
                        return str(response_data["content"])
                    elif "error" in response_data:
                        return f"Tool Error: {response_data['error']}"
                    else:
                        return f"Unknown Response: {response_line}"
                except json.JSONDecodeError as e:
                    return f"Parse Error: 无法解析 JSON ({e}) | Raw: {response_line}"
            else:
                return "No response from server"

        except Exception as e:
            return f"Call Error: {str(e)}"


# --- 全局客户端实例 ---
CURRENT_DIR = os.path.dirname(__file__)
SERVER_SCRIPT = os.path.join(CURRENT_DIR, "mysql_server.py")

mcp_client = MysqlMcpClient(SERVER_SCRIPT)

if __name__ == "__main__":
    mcp_client.start()
    # 模拟多次调用
    result = mcp_client.call_tool(customer_code='1900010454')
    print("最终结果:")
    print(result)
    # mcp_client.stop() # 根据需要决定是否关闭