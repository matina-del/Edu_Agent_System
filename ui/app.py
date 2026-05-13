import streamlit as st
import os
import sys


sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.qa_agent import AdaptiveLearningAgent
from knowledge_base.vector_store import KnowledgeBase
from user_profile.profile_manager import UserProfileManager


os.environ["OPENAI_API_KEY"] = "sk-xxxxxxxxxxxxxxx"

os.environ["OPENAI_API_BASE"] = "https://api.gptsapi.net/v1" 

st.set_page_config(page_title="智能教育 Agent", page_icon="🎓")

# 初始化后端引擎 (利用 st.cache_resource 保证刷新页面时不重复加载)
@st.cache_resource
def init_agent():
    kb = KnowledgeBase()
    pm = UserProfileManager()
    dummy_question_bank = [] # 模拟题库，后期可以填入真实数据
    return AdaptiveLearningAgent(kb, pm, dummy_question_bank)

agent = init_agent()

st.title("🎓 智能教育自适应辅导 ")


# 聊天记录存储
if "messages" not in st.session_state:
    st.session_state.messages = []

# 显示历史聊天
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 用户输入框
if prompt := st.chat_input("请输入你想学习的知识点（例如：什么是勾股定理？）"):
    # 显示用户输入
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # 思考并调用 Agent 讲解
    with st.chat_message("assistant"):
        with st.spinner("AI 老师正在为您量身定制讲解内容..."):
            # 假定当前用户 ID 为 "user_001"
            response = agent.explain_concept(concept=prompt, user_id="user_001")
            st.markdown(response)
    
    st.session_state.messages.append({"role": "assistant", "content": response})