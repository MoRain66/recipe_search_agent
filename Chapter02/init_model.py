from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
from langchain.agents import create_agent
from langchain.tools import tool



load_dotenv()

@tool
def getWeather(location:str) -> str:
    """
     Get the weather in a given location.
     Args:
         location: city name or coordinates
     """
    return f"Current weather in {location} is sunny"

model = init_chat_model("deepseek-chat")

# 已经完成了模型初始化，那么怎么在agent中使用呢
agent = create_agent(
    model = model,
    tools=[getWeather]
)


response = agent.invoke({#type:ignore
    "messages":[
        {"role":"user","content":"你是谁？"}
]
})

print(response['messages'][1].content)

