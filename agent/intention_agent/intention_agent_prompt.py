from langchain_core.example_selectors import LengthBasedExampleSelector
from langchain_core.prompts import ChatPromptTemplate, PromptTemplate, SystemMessagePromptTemplate, \
    FewShotPromptTemplate, HumanMessagePromptTemplate

examples = [
    {
        "input": "你好啊，有什么可以帮您？",
        "intent": "咨询"
    },
    {
        "input": "我想了解一下最新的牛奶促销活动",
        "intent": "咨询"
    },
    {
        "input": "客户代码C1001的名称是什么？",
        "intent": "按客户编码查询客户信息"
    },
    {
        "input": "客户编码M888有什么产品",
        "intent": "按客户编码查询客户信息"
    },
    {
        "input": "随便聊聊",
        "intent": "未知"
    },
    {
        "input": "asdf@#jkl",
        "intent": "未知"
    }
]

# 2. 定义示例的格式化模板
# 这决定了每个“样板”在最终提示词中长什么样。
example_prompt = PromptTemplate.from_template(
    "用户输入: {input}\n分类结果: {intent}"
)

# 3. 定义示例选择器
example_selector = LengthBasedExampleSelector(
    examples=examples,
    example_prompt=example_prompt,
    max_length=100  # 当输入字符超过100时开始筛选，这里仅作演示
)


# 4. 定义 FewShotPromptTemplate
def get_intention_agent_prompt():
    # 1. 定义系统消息的前缀（不包含示例）
    prefix = """你是一个专业的牛奶销售助手意图分类器。

        请严格分析用户输入的语义，将其归类为以下三种意图之一：
        - **咨询**: 用户询问牛奶产品信息、价格、促销活动，或者闲聊、提出非查询类的需求。
        - **按客户编码查询客户信息**: 用户明确要求查询某个客户（如经销商、门店）的具体信息，通常包含具体的客户编码或名称。
        - **未知**: 用户输入内容混乱、无法理解，或者与牛奶销售完全无关。

        #### 参考示例
        """

    # 2. 定义后缀（用户输入部分）
    suffix = """
        #### 用户输入
        {input}

        #### 分类结果
        """

    # 3. 构建 Few-shot 模板 (这才是核心)
    few_shot_prompt = FewShotPromptTemplate(
        example_selector=example_selector,
        example_prompt=example_prompt,
        prefix=prefix,          # 连接头
        suffix=suffix,          # 连尾巴
        input_variables=["input"],
    )

    # 4. 最终的 ChatPromptTemplate
    # 注意：这里把整个 few_shot_prompt 当作系统消息的内容
    chat_prompt = ChatPromptTemplate.from_messages([
        SystemMessagePromptTemplate(prompt=few_shot_prompt),
        HumanMessagePromptTemplate.from_template("{input}")
    ])

    return chat_prompt