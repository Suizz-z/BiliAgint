from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.messages import SystemMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables import RunnableWithMessageHistory
from langchain_openai.chat_models import ChatOpenAI
from langchain_community.chat_message_histories import  ChatMessageHistory
import streamlit as st

llm = ChatOpenAI(
    api_key="sk-6d33490b5a004811b2768193ffe9a72e",
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
    model="qwq-32b",
    temperature=0,
    streaming=True
)

store = {}


def get_session_history(session_id: str) -> BaseChatMessageHistory:
    if session_id not in store:
        store[session_id] = ChatMessageHistory()

        # 动态获取当前session_state中的内容
        subtitle = st.session_state.get("full_subtitle", "暂无字幕内容")
        analysis = st.session_state.get("analysis_result", "暂无分析结果")

        chat_subtitle = f"""
        你是一位负责的助手，你将会根据提供的字幕以及字幕总结对用户的问题进行回答
        这是提供的字幕: {subtitle}
        这是提供的字幕总结: {analysis}
        """

        store[session_id].add_message(SystemMessage(chat_subtitle))

    return store[session_id]

def chat_stream(prompt):
    """
    使用流式方式获取并返回AI模型的响应。

    Args:
        prompt (str): 用户输入的提示文本

    Yields:
        str: AI模型响应的文本片段
    """

    subtitle_chat_prompt = ChatPromptTemplate.from_messages(
        [
            MessagesPlaceholder(variable_name="chat_history"),
            ("user", "{input}")
        ]
    )
    subtitle_chat_chain = subtitle_chat_prompt | llm

    chain_with_message_history = RunnableWithMessageHistory(
        subtitle_chat_chain,
        get_session_history= get_session_history,
        input_messages_key="input",
        history_messages_key="chat_history"
    )

    for chunk in chain_with_message_history.stream({"input":prompt},config={"configurable":{"session_id":"001"}}):
        if chunk.content:
            yield chunk.content
    # return chain_with_message_history


# 定义保存反馈的函数
def save_feedback(index):
    """
    保存用户对AI回复的反馈。

    Args:
        index (int): 消息在历史记录中的索引位置
    """
    st.session_state.history[index]["feedback"] = st.session_state[f"feedback_{index}"]

# if __name__ == "__main__":
#     res_chain = chat_stream()
#
#     for chunk in res_chain.stream({"input":"这个视频主要讲的什么"},config={"configurable":{"session_id":"001"}}):
#         if chunk.content:
#             print(chunk.content,end="", flush=True)








