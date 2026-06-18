from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
from langchain.agents import create_agent
from langchain.tools import tool
from langchain_core.messages import SystemMessage,HumanMessage, AIMessage

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

agent = create_agent(
    model=model,
    tools=[getWeather]
)

response = agent.invoke({#type:ignore
    "messages":[
        # {"role":"system","content":"你是一个AI助手"},
        # {"role":"user","content":"你好我是墨"},
        # {"role":"assistant","content":"你好墨"},
        # {"role":"user","content":"上海今天天气如何？"}
        SystemMessage(content="你是一个AI助手"),
        HumanMessage(content="你好我是墨"),
        AIMessage(content="你好墨"),
        HumanMessage(content="上海今天天气如何？")
    ]
})

# print(response)
for message in response["messages"]:
    message.pretty_print()