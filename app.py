import os
import json
import requests
import streamlit as st
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("DEEPSEEK_API_KEY")
URL = "https://api.deepseek.com/chat/completions"

st.title("我的 AI 助手")

if "messages" not in st.session_state:
    st.session_state.messages = []

if st.button("清空对话"):
    st.session_state.messages = []
    st.rerun()

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])


def stream_chat(messages):
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json",
    }
    payload = {
        "model": "deepseek-chat",
        "messages": messages,
        "stream": True,
    }
    with requests.post(URL, headers=headers, json=payload, stream=True, timeout=60) as r:
        if r.status_code != 200:
            raise Exception(f"HTTP {r.status_code}: {r.text[:200]}")
        for line in r.iter_lines():
            if not line:
                continue
            line = line.decode("utf-8")
            if not line.startswith("data: "):
                continue
            data = line[6:]
            if data == "[DONE]":
                break
            try:
                delta = json.loads(data)["choices"][0]["delta"].get("content")
            except (KeyError, IndexError, json.JSONDecodeError):
                continue
            if delta:
                yield delta


question = st.chat_input("说点什么...")

if question:
    st.session_state.messages.append({"role": "user", "content": question})
    with st.chat_message("user"):
        st.write(question)

    answer = ""
    with st.chat_message("assistant"):
        try:
            answer = st.write_stream(stream_chat(st.session_state.messages))
        except Exception as e:
            msg = str(e)
            if "401" in msg:
                st.error("密钥不对，检查 .env 里的 DEEPSEEK_API_KEY")
            elif "402" in msg or "429" in msg:
                st.error("余额不足或请求太频繁")
            else:
                st.error("出错了：" + msg[:200])

    if answer:
        st.session_state.messages.append({"role": "assistant", "content": answer})