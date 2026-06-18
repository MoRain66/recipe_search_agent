import checkpointer
from app.common.logger import logger
from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage, AIMessageChunk
from langchain_core.tools import tool
from langgraph.checkpoint.sqlite import SqliteSaver
from langchain.chat_models import init_chat_model
import os
import sqlite3
from langchain_tavily import TavilySearch


load_dotenv()

# 初始化模型
model = init_chat_model(
    model="qwen3.5-plus",
    model_provider="openai",
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    base_url=os.getenv("DASHSCOPE_BASE_URL")
)

search = TavilySearch(
    max_result = 5,
    topic="general"
)
# 自定义工具
@tool
def websearch(query:str):
    """Search web search"""
    return search.invoke(query)


#初始化中间件
connection_recipe = sqlite3.connect(r"D:\Develop\projects\PythonProject1\db\Recipes.db", check_same_thread=False)
checkpointer_recipe = SqliteSaver(connection_recipe)
checkpointer_recipe.setup()

#构建系统提示词
system_prompt = """
你是一名私人厨师。收到用户提供的食材照片或清单后，请按以下流程操作：
1.识别和评估食材：若用户提供照片，首先辨识所有可见食材。基于食材的外观状态，评估其新鲜度与可用量，整理出一份“当前可用食材清单”。
2.智能食谱检索：优先调用 web_search 工具，以“可用食材清单”为核心关键词，查找可行菜谱。
3.多维度评估与排序：从营养价值和制作难度两个维度对检索到的候选食谱进行量化打分，并根据得分排序，制作简单且营养丰富的排名靠前。
4.结构化方案输出：把排序后的食谱整理为一份结构清晰的建议报告，要包含食谱信息、得分、推荐理由、食谱的参考图片，帮助用户快速做出决策。

请严格按照流程，优先调用 web_search 工具搜索食谱，搜索不到的情况下才能自己发挥。
"""

# 创建agent
agent = create_agent(
    model=model,
    checkpointer=checkpointer_recipe,
    tools=[websearch],
    system_prompt=system_prompt
)

# 流式对话
async def search_recipes(prompt: str, image: str, thread_id: str):
    """调用agent搜索食谱"""
    logger.info(f"[用户]: {prompt}, image: {image}, thread_id: {thread_id}")
    try:
        # 判断是否有图片，封装不同格式的消息
        if not image or image.strip() == "":
            message = HumanMessage(content=prompt)
        else:
            message = HumanMessage(content=[
                {"type": "image", "url": image},
                {"type": "text", "text": prompt}
            ])

        # 流式调用Agent
        for chunk, metadata in agent.stream(
            {"messages": [message]},
            {"configurable": {"thread_id": thread_id}},
            stream_mode="messages"
        ):
            if isinstance(chunk, AIMessageChunk) and chunk.content:
                yield chunk.content

    except Exception as e:
        logger.error(f"\n[错误]: {str(e)}")
        yield "信息检索失败，试试看手动输入食物列表？"

# 清空会话
def clear_messages(thread_id: str):
    """清空会话"""
    logger.info(f"清空历史消息，thread_id: {thread_id}")
    checkpointer.delete_thread(thread_id)

# 查询会话历史
def get_messages(thread_id: str) -> list[dict[str, str]]:
    """获取会话历史"""
    logger.info(f"获取历史消息，thread_id: {thread_id}")

    # 根据 thread_id 查询 checkpoint
    checkpoint = checkpointer.get({"configurable": {"thread_id": thread_id}})

    # 如果不存在，返回空列表
    if not checkpoint:
        return []

    # 安全获取 messages
    channel_values = checkpoint.get("channel_values")
    if not channel_values:
        return []

    messages = channel_values.get("messages", [])
    if not messages:
        return []

    # 转换消息格式
    result = []
    for msg in messages:
        if not msg.content:
            continue

        if isinstance(msg, HumanMessage):
            result.append({"role": "user", "content": msg.content})
        elif isinstance(msg, AIMessage):
            result.append({"role": "assistant", "content": msg.content})

    return result
















#调用也不需要在这里写

# multi_messages = HumanMessage(content=[
#     {"type":"text","text":"帮我看看能做什么"},
#     {"type":"image","url":"https://temp.aoki.dpdns.org/temp/14868b182414691b1ebaf3e8385a2926.png"}
# ])
#
# config = {"configurable":{"thread_id":"thread6"}}
#
# response = agent.invoke(
#     {"messages":[multi_messages]},
#     config=config
# )
#
# print(response["messages"][-1].content)
