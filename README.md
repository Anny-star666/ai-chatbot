# AI 问答机器人

一句话：基于 DeepSeek 的多轮对话应用，支持流式输出与异常兜底。

## 功能
- 多轮对话，保留上下文
- 流式输出，首字延迟 < 1s
- 密钥错误、额度不足、网络超时均有中文提示

## 截图
<img width="800" height="1484" alt="image" src="https://github.com/user-attachments/assets/20ca0581-3061-4a63-b9cc-735473d43b5f" />

## 如何运行
1. 克隆仓库
2. 创建虚拟环境：python -m venv venv
3. 安装依赖：venv\Scripts\python.exe -m pip install -r requirements.txt
4. 复制 .env.example 为 .env，填入 DEEPSEEK_API_KEY
5. 启动：venv\Scripts\python.exe -m streamlit run app.py

## 踩坑记录
- Windows 智能应用控制会拦截 pandas/pyarrow，需关闭
- 流式结束后必须把完整文本存回 messages，否则下一轮丢上下文
