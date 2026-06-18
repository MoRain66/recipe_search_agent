# from http.client import responses
#
# from openai import OpenAI, base_url
# from dotenv import load_dotenv
# #os就是系统
# import os
#
# load_dotenv()
#
# api_key = os.getenv("DEEPSEEK_API_KEY")
# print(api_key)
#
# client = OpenAI(
#     api_key=api_key,
#     base_url="https://api.deepseek.com"
# )
#
# print("正在调用大模型......")
#
# response = client.chat.completions.create(
#     model="deepseek-v4-pro",
#     messages=[# type: ignore 压制黄色波浪线警告
#         {
#             "role": "system",
#             "content": "你是一名友好的AI助教。"
#         },
#         {
#             "role": "user",
#             "content": "你好，你是谁？"
#         }
#
#     ],
# )
#
# print("成功调用大模型。")
# print(response.model_dump_json())
# print(response.choices[0].message.content)
