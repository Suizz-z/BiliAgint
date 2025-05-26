import streamlit as st
from langserve import RemoteRunnable
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))


st.markdown("""
<h1 style='text-align: center; color: blue; background: linear-gradient(to right, red, purple); -webkit-background-clip: text; -webkit-text-fill-color: transparent;'>
      📊 BiliBili 视频推荐查询
</h1>
""", unsafe_allow_html=True)


# 输入框单独占一行显示
# st.write("#### 请输入问题:")
input_text = st.text_input("请输入问题:", key="2")

if input_text:
    with st.spinner("正在处理..."):
        try:
            app = RemoteRunnable("http://localhost:8088/biliagent_chat")
            responses = []
            for output in app.stream({"input": input_text}):
                responses.append(output)
            if responses:
                print(responses)
                with st.expander("分析结果"):
                    last_response = responses[-1]
                    st.markdown(last_response["generate"]["generation"])

                with st.expander("查看详细推荐视频信息"):
                    for idx, doc in enumerate(last_response.get("documents", [])):
                        st.write(f"### 视频 {idx + 1}")
                        st.json(doc)

            else:
                st.info("没有返回结果。")
        except Exception as e:
            st.error(f"处理时出现错误: {str(e)}")


