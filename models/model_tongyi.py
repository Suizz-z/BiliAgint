import os
from dotenv import load_dotenv, find_dotenv


from langchain_core.prompts import ChatPromptTemplate

load_dotenv(find_dotenv())
from langchain_openai import ChatOpenAI
llm = ChatOpenAI(
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
    model="qwen-plus",
)

prompt = ChatPromptTemplate(
    [
        ("system","你是一位乐于助人的小助手"),
        ("user","{input}")
    ]
)

chain = prompt | llm

res = chain.invoke({"input":"你好"})
print(res.content)