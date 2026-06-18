from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
from langchain.agents import create_agent
from langchain_core.messages import HumanMessage,SystemMessage
import os


load_dotenv()

model = init_chat_model(
    model="qwen3.5-plus",
    model_provider="openai",
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    base_url=os.getenv("DASHSCOPE_BASE_URL")
)

agent = create_agent(model=model)


message =HumanMessage([
    {"type": "image", "url": "https://temp.aoki.dpdns.org/temp/14868b182414691b1ebaf3e8385a2926.png"},
    {"type": "text", "text": "这些图描绘了什么内容？"}
                ])



stream = agent.stream(
    #type:ignore
    {"messages":[message]},
    stream_mode="messages"
)

for chunk,metadata in stream:
        print(chunk.content,end=" ",flush=True)