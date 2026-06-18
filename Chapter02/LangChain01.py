from dotenv import load_dotenv
from langchain.tools import tool
from langchain.agents import create_agent
from pyexpat.errors import messages


load_dotenv()# 加载环境变量

@tool
def getWeather(location:str) -> str:
    """
     Get the weather in a given location.
     Args:
         location: city name or coordinates
     """
    return f"Current weather in {location} is sunny"

# 创建Agent
agent = create_agent(
    "deepseek-v4-pro",# 调用大模型的名称
    tools=[getWeather]
)

print("正在调用大模型......")
response = agent.invoke({#type:ignore
    "messages":[
        {"role":"user","content":"今天上海天气怎么样？"}
    ]
})

print(response)

