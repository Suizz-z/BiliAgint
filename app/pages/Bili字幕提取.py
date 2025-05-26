import streamlit as st
import sys
import os
from streamlit_extras.colored_header import colored_header



sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from bilibili_tools.subtitle_fetcher import get_subtitles
from bilibili_tools.subtitle_analysis import get_subtitle_analysis
from bilibili_tools.chat_bot import save_feedback, chat_stream


# 页面配置
st.set_page_config(
    page_title="B站字幕提取分析器",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# 自定义CSS样式
st.markdown("""
<style>
    /* 主容器样式 */
    .main-container {
        background-color: #f8f9fa;
        border-radius: 10px;
        padding: 20px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }

    /* 按钮样式 */
    .stButton>button {
        border-radius: 8px;
        border: none;
        background-color: #4CAF50;
        color: white;
        padding: 8px 16px;
        transition: all 0.3s;
    }

    .stButton>button:hover {
        background-color: #45a049;
        transform: translateY(-2px);
    }

    /* 输入框样式 */
    .stTextInput>div>div>input {
        border-radius: 8px;
        border: 1px solid #ced4da;
    }

    /* 聊天消息样式 */
    .user-message {
        background-color: #e3f2fd;
        border-radius: 15px 15px 0 15px;
        padding: 10px 15px;
        margin: 5px 0;
    }

    .assistant-message {
        background-color: #f1f1f1;
        border-radius: 15px 15px 15px 0;
        padding: 10px 15px;
        margin: 5px 0;
    }

    /* 分割线样式 */
    .stDivider>div>div>div {
        background-color: #6c757d;
    }

    /* 卡片样式 */
    .card {
        background-color: white;
        border-radius: 10px;
        padding: 15px;
        margin-bottom: 15px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
</style>
""", unsafe_allow_html=True)

# 初始化session状态
if 'subtitle_data' not in st.session_state:
    st.session_state.subtitle_data = None
if 'analysis_done' not in st.session_state:
    st.session_state.analysis_done = False
if 'analysis_result' not in st.session_state:
    st.session_state.analysis_result = ""
if 'full_subtitle' not in st.session_state:
    st.session_state.full_subtitle = ""
if "history" not in st.session_state:
    st.session_state.history = []


col_left, col_mid,col_right = st.columns([1, 1, 1], gap="large")

# 左侧字幕提取功能
with col_left:
    # 顶部标题
    colored_header(
        label="🎬 B站字幕提取分析器",
        description="输入视频BV号和SESSDATA提取字幕",
        color_name="blue-70",
    )

    # 字幕提取卡片
    with st.container():
        st.markdown('<div class="card">', unsafe_allow_html=True)

        with st.form("subtitle_form", clear_on_submit=False):
            st.markdown("**视频信息**")

            col1, col2 = st.columns([1, 2])
            with col1:
                bvid = st.text_input(
                    "视频BV号",
                    placeholder="例如：BV1xx411x7xx",
                    help="需要完整BV号，以BV开头"
                )
            with col2:
                sessdata = st.text_input(
                    "SESSDATA",
                    type="password",
                    help="从浏览器Cookie获取，用于身份验证"
                )

            submitted = st.form_submit_button(
                "📥 提取字幕",
                use_container_width=True
            )

            if submitted:
                if not bvid.startswith("BV"):
                    st.error("❌ 请输入有效的BV号（以BV开头）")
                elif not sessdata:
                    st.error("❌ 需要提供SESSDATA以访问受保护内容")
                else:
                    with st.spinner("正在提取字幕，请稍候..."):
                        try:
                            result = get_subtitles(bvid, sessdata)
                            if result["status"] == "success":
                                st.session_state.subtitle_data = result
                                st.session_state.analysis_done = False
                                st.session_state.messages = []
                                st.success(f"✅ 成功提取 {len(result['subtitles'])} 个字幕文件")
                            else:
                                st.error(f"提取失败：{result['message']}")
                        except Exception as e:
                            st.error(f"发生意外错误：{str(e)}")

        st.markdown('</div>', unsafe_allow_html=True)

    # 显示字幕结果
    if st.session_state.subtitle_data and st.session_state.subtitle_data["status"] == "success":
        with st.container():
            st.markdown('<div class="card">', unsafe_allow_html=True)

            colored_header(
                label="📝 字幕提取结果",
                description="视频基本信息和提取到的字幕内容",
                color_name="green-70",
            )

            with st.expander("📊 视频基本信息", expanded=True):
                st.json(st.session_state.subtitle_data["metadata"])

            st.markdown("**提取到的字幕内容**")
            for idx, sub in enumerate(st.session_state.subtitle_data["subtitles"], 1):
                with st.expander(f"字幕 {idx}", expanded=False):
                    st.code(sub['content'], language="text")
                    st.session_state.full_subtitle = sub['content']

                if st.button(
                        "🧹 清除结果",
                        use_container_width=True,
                        type="secondary",
                        help="清除当前提取的字幕结果"
                ):
                    st.session_state.subtitle_data = None
                    st.session_state.analysis_done = False
                    st.session_state.messages = []
                    st.rerun()

            st.markdown('</div>', unsafe_allow_html=True)



with col_mid:
    colored_header(
        label="🤖 字幕分析",
        description="通过字幕对视频进行总结",
        color_name="violet-70",
    )

    if st.button("🤖 AI智能分析",use_container_width=True,help="对字幕内容进行智能分析"):
        print(st.session_state.full_subtitle)
        with st.expander("📊 AI字幕总结", expanded=True):
            subtitle_analysis= st.empty()
            with subtitle_analysis:
                full_response = ""
                for chunk in st.write_stream(get_subtitle_analysis(st.session_state.full_subtitle)):
                    full_response += chunk
                st.session_state.analysis_result = full_response

with col_right:
    colored_header(
        label="🤖 智能助手",
        description="随时为您解答问题",
        color_name="violet-70",
    )

    for index, message in enumerate(st.session_state.history):
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

            if message["role"] == "assistant":
                col1, col2 = st.columns([0.1, 0.9])
                with col1:
                    feedback_key = f"feedback_{index}"

                    if feedback_key not in st.session_state:
                        st.session_state[feedback_key] = ""

                    if st.button("👍", key=f"like_{index}"):
                        st.session_state[feedback_key] = "有帮助"
                        save_feedback(index)
                    if st.button("👎", key=f"dislike_{index}"):
                        st.session_state[feedback_key] = "无帮助"
                        save_feedback(index)

                with col2:
                    if st.session_state[feedback_key]:
                        st.caption(f"您的反馈：{st.session_state[feedback_key]}")

    if user_input := st.chat_input("请输入您关于视频内容的问题..."):
        # 添加用户消息到历史
        st.session_state.history.append({"role": "user", "content": user_input})

        # 显示用户消息
        with st.chat_message("user"):
            st.markdown(user_input)

        # 生成并显示AI回复
        with st.chat_message("assistant"):
            response_container = st.empty()
            full_response = ""

            # 流式获取响应
            for chunk in chat_stream(user_input):
                full_response += chunk
                response_container.markdown(full_response + "▌")

            response_container.markdown(full_response)

        # 添加AI回复到历史
        st.session_state.history.append({"role": "assistant", "content": full_response})
        st.rerun()

