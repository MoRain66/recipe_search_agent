from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain_core.messages import HumanMessage,SystemMessage
from langchain.agents.middleware import SummarizationMiddleware
from langgraph.checkpoint.memory import InMemorySaver

load_dotenv()

checkpointer = InMemorySaver()

#初始化中间件
middleware = SummarizationMiddleware(
    model="deepseek-chat",
    trigger=("messages",3),
    keep=("messages",1)
)

config = {"configurable":{"thread_id":"thread_3"}}

agent = create_agent("deepseek-v4-pro",middleware=[middleware],checkpointer=checkpointer)

# 制造长会话历史
agent.invoke({"messages": "你好，我是墨."}, config)
agent.invoke({"messages": "我最喜欢的运动是乒乓"}, config)
agent.invoke({"messages": "我最喜欢的动物是猫猫"}, config)
# 测试效果
final_response = agent.invoke({"messages": "你还记得我吗？"}, config)


for message in final_response["messages"]:
    message.pretty_print()


