# from anyio.lowlevel import checkpoint
# from langgraph.checkpoint.sqlite import SqliteSaver
# from dotenv import load_dotenv
# from langchain.agents import create_agent
# from langchain_core.messages import HumanMessage,SystemMessage
# import sqlite3
#
# load_dotenv()
#
# #链接sqlite
# connection = sqlite3.connect("resources/database.db",check_same_thread=False)
# #初始化
# checkpointer = SqliteSaver(connection)
# #自动建表
# checkpointer.setup()
#
#
# agent = create_agent(
#     model="deepseek-v4-pro",
#     checkpointer=checkpointer
# )
#
# config = {"configurable":{"thread_id":"thread_2"}}
#
# response = agent.invoke(
#     {
#         "messages":[HumanMessage("你好我是墨")]},
#     config
# )
# for message in response["messages"]:
#     message.pretty_print()
#
# response = agent.invoke(
#     {
#         "messages":[HumanMessage("你知道我是谁吗")]},
#     config
# )
# for message in response["messages"]:
#     message.pretty_print()