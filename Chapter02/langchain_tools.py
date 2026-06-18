from dotenv import load_dotenv
from pydantic import BaseModel,Field
from typing import Literal
from langchain_core.tools import tool
from langchain.agents import create_agent
from langchain_core.messages import HumanMessage,SystemMessage

load_dotenv()

# 例如一个查询天气的tool
class WeatherInput(BaseModel):
    """查询天气的输入参数.""" # 工具描述
    # 各个参数
    # field后面写的就是对应参数的描述
    location: str = Field(description="City name or coordinates")
    units: Literal["celsius", "fahrenheit"] = Field(
        default="celsius",
        description="Temperature unit preference"
    )
    include_forecast: bool = Field(
        default=False,
        description="Include 5-day forecast"
    )

 # 定义一个查询天气的tool
@tool(args_schema=WeatherInput)# 参数的约束
def get_weather(location: str, units: str = "celsius", include_forecast: bool = False) -> str:
    """Get current weather and optional forecast."""
    temp = 22 if units == "celsius" else 72
    result = f"Current weather in {location}: {temp} degrees {units[0].upper()}"
    if include_forecast:
        result += "\nNext 5 days: Sunny"
    return result

agent = create_agent(
    model="deepseek-v4-pro",
    tools=[get_weather]
)

stream = agent.stream({#type:ignore
    "messages":[HumanMessage("今天上海的天气怎么样？")
    ]
},
    stream_mode="messages"
)

for chunk,metadata in stream:
    print(chunk.content,end=" ",flush=True)