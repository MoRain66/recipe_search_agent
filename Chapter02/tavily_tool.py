from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain_core import tools
from langchain_core.messages import HumanMessage,SystemMessage,AIMessage
from langchain_tavily import TavilySearch
import os


load_dotenv()

# 初始化工具
# 执行完成之后，就是一个工具了
search_tool = TavilySearch(
    max_results=10,
    topic="general"
)

agent = create_agent(
    model="deepseek-v4-pro",
    tools=[search_tool],
    system_prompt="你是一个智能助手，使用工具解决问题"
)

response = agent.invoke({#type:ignore
    "messages":[HumanMessage("柠檬有什么功效？")]
}
)

for message in response["messages"]:
    message.pretty_print()