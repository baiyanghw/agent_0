import time

import streamlit as st
from agent.react_agent import ReactAgent

st.title("智扫通机器人智能客服")
st.divider()

if "agent" not in st.session_state:
    st.session_state.agent = ReactAgent()

if "messages" not in st.session_state:
    st.session_state.messages = []
for message in st.session_state["messages"]:
    st.chat_message(message["role"]).write(message["content"])


#用户输入
prompt=st.chat_input()

if prompt:
    st.chat_message("user").write(prompt)
    st.session_state["messages"].append({"role":"user","content":prompt})
    responses_messages=[]
    with st.spinner("智能客服思考中..."):
        res_stream=st.session_state["agent"].execute_stream(prompt)
        def capture(generator,chche_list):
            for chunk in generator:
                chche_list.append(chunk)
                for char in chunk:
                    time.sleep(0.01)
                    yield char
        st.chat_message("assistant").write_stream(capture(res_stream,responses_messages))
        st.session_state["messages"].append({"role":"assistant","content":responses_messages[-1]})
        st.rerun()