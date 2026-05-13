import os
from dotenv import load_dotenv
from openai import OpenAI


def clean_text(text: str) -> str:
        return text.encode("utf-8", errors="ignore").decode("utf-8")

# 读取根目录下的.env文件
load_dotenv()
# 创建一个能够访问大模型服务的客户端
client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    base_url=os.getenv("OPENAI_BASE_URL"),
)
# 从环境变量中读取模型名称
model_name = os.getenv("MODEL_NAME", "deepseek-chat")

messages = [
    {"role": "system", "content": "你是一个简洁、耐心的 AI 助手。"}
]

print("AI CLI Chatbot 已启动，输入 exit 退出。")

while True:
    # user_input = input("\n你：").strip()
    user_input = clean_text(input("\n你：").strip())

    if user_input.lower() in ["exit", "quit", "q"]:
        print("已退出。")
        break

    if not user_input:
        continue

    messages.append({"role": "user", "content": user_input})

    try:
        response = client.chat.completions.create(
            model=model_name,
            messages=messages,
            temperature=0.7,
        )
        assistant_reply = clean_text(response.choices[0].message.content or "")
        print(f"\nAI：{assistant_reply}")

        messages.append({"role": "assistant", "content": assistant_reply})

    except Exception as e:
        print(f"\n调用失败：{e}")