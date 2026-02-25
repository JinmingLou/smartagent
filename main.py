from chain.chain import LlmChain

if __name__ == '__main__':
    print("欢迎使用牛奶销售管理智能助手，输入 'exit' 退出程序")
    #初始化chain
    chain = LlmChain()
    while True:
        user_input = input("请输入指令或消息: ")
        if user_input.lower() == "exit":
            print("bye！")
            break
        else:
            response = chain.invokeChain(question=user_input)
            print(response)


