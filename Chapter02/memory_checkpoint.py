from dotenv import load_dotenv
from langchain.agents import create_agent
from langgraph.checkpoint.memory import InMemorySaver
from langchain_core.messages import HumanMessage,SystemMessage,AIMessage

load_dotenv()

agent = create_agent(
    model="deepseek-v4-pro",
    checkpointer=InMemorySaver()
)

config = {"configurable":{"thread_id":"thread_1"}}

response = agent.invoke(
    {
        "messages":[HumanMessage("你好我是墨")]},
    config
)
for message in response["messages"]:
    message.pretty_print()

response = agent.invoke(
    {
        "messages":[HumanMessage("你知道我是谁吗")]},
    config
)
for message in response["messages"]:
    message.pretty_print()