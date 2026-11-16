import os
import streamlit as st
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(
    api_key=os.getenv("DEEPSEEK_API_KEY"),
    base_url="https://api.deepseek.com"
)

# 整个产品的灵魂：指令文件直接当 system prompt
with open("INSTRUCTIONS.md", encoding="utf-8") as f:
    SYSTEM_PROMPT = f.read()

st.set_page_config(page_title="Prompt Optimizer", page_icon="✨")
st.title("✨ Prompt Optimizer")
st.caption("把一句自然语言需求，优化成三个可直接使用的 Prompt")

requirement = st.text_area(
    "你的需求",
    height=120,
    placeholder="例如：帮我写一条朋友圈，宣布我转行做 AI 工程师"
)

if st.button("开始优化", type="primary") and requirement.strip():
    with st.spinner("优化中..."):
        resp = client.chat.completions.create(
            model="deepseek-chat",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": requirement}
            ]
        )
    st.markdown(resp.choices[0].message.content)