import time
import streamlit as st
from agent.react_agent import ReactAgent

# ========== 页面配置 ==========
st.set_page_config(
    page_title="智扫通智能客服",
    page_icon="🤖",
    layout="centered"
)

# ========== 自定义CSS ==========
st.markdown("""
<style>
/* 整体背景 */
.stApp {
    background-color: #f7f9fc;
}

/* 标题 */
.main-title {
    text-align: center;
    font-size: 32px;
    font-weight: 700;
    margin-bottom: 10px;
}

/* 副标题 */
.sub-title {
    text-align: center;
    color: gray;
    margin-bottom: 20px;
}

/* 聊天气泡 */
.chat-bubble {
    padding: 12px 16px;
    border-radius: 12px;
    margin-bottom: 10px;
    max-width: 80%;
    line-height: 1.6;
}

/* 用户气泡 */
.user-bubble {
    background-color: #4CAF50;
    color: white;
    margin-left: auto;
}

/* assistant气泡 */
.bot-bubble {
    background-color: white;
    border: 1px solid #e0e0e0;
}

/* 输入框优化 */
[data-testid="stChatInput"] {
    border-top: 1px solid #ddd;
}
</style>
""", unsafe_allow_html=True)

# ========== 标题 ==========
st.markdown('<div class="main-title">🤖 智扫通机器人智能客服</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">为您提供扫地机器人选购与使用建议</div>', unsafe_allow_html=True)

st.divider()

# ========== 初始化 ==========
if "agent" not in st.session_state:
    st.session_state.agent = ReactAgent()

if "messages" not in st.session_state:
    st.session_state.messages = []

# ========== 显示历史消息 ==========
for message in st.session_state["messages"]:
    role = message["role"]
    content = message["content"]

    if role == "user":
        st.markdown(
            f'<div class="chat-bubble user-bubble">{content}</div>',
            unsafe_allow_html=True
        )
    else:
        st.markdown(
            f'<div class="chat-bubble bot-bubble">{content}</div>',
            unsafe_allow_html=True
        )

# ========== 用户输入 ==========
prompt = st.chat_input("请输入你的问题，例如：小户型适合哪种扫地机器人？")

if prompt:
    # 显示用户消息
    st.markdown(
        f'<div class="chat-bubble user-bubble">{prompt}</div>',
        unsafe_allow_html=True
    )

    st.session_state["messages"].append({
        "role": "user",
        "content": prompt
    })

    responses_messages = []

    with st.spinner("🤖 智能客服思考中，请稍候..."):

        res_stream = st.session_state["agent"].execute_stream(prompt)

        # 打字机效果
        def capture(generator, cache_list):
            for chunk in generator:
                cache_list.append(chunk)
                for char in chunk:
                    time.sleep(0.01)
                    yield char

        # assistant输出
        response_container = st.empty()
        response_container.markdown(
            '<div class="chat-bubble bot-bubble">',
            unsafe_allow_html=True
        )

        full_response = st.write_stream(capture(res_stream, responses_messages))

        response_container.markdown("</div>", unsafe_allow_html=True)

        # 保存最后一条完整回复
        st.session_state["messages"].append({
            "role": "assistant",
            "content": responses_messages[-1] if responses_messages else ""
        })

        st.rerun()