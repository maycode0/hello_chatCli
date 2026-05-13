from openai import OpenAI
from hello_chat_bot.config import ConfigError, load_config
from hello_chat_bot.commands import handle_command

def clean_text(text: str) -> str:
    return text.encode("utf-8", errors="ignore").decode("utf-8")

try:
    config = load_config()
except ConfigError as e:
    print(f"配置错误：{e}")
    raise SystemExit(1)

# 创建一个能够访问大模型服务的客户端
client = OpenAI(
    api_key=config.api_key,
    base_url=config.base_url,
)
# 从环境变量中读取模型名称
model_name = config.model_name
temperature = config.temperature
messages = [
    {"role": "system", "content": "你是一个简洁、耐心的 AI 助手。"}
]

print("AI CLI Chatbot 已启动，输入 /exit、/quit 或 /q 退出。")

while True:
    # user_input = input("\n你：").strip()
    user_input = clean_text(input("\n你：").strip())
    command_result = handle_command(user_input, config)
    # 这样命令不会被发送给模型，只处理命令逻辑
    if command_result.handled:
        if command_result.message:
            print(command_result.message)
        if command_result.should_clear:
            messages = [
                    {"role": "system", "content": "你是一个简洁、耐心的 AI 助手。"}
                ]
        if command_result.should_exit:
            break
        continue

    messages.append({"role": "user", "content": user_input})

    try:
        response = client.chat.completions.create(
            model=model_name,
            messages=messages,
            temperature=temperature,
        )
        assistant_reply = clean_text(response.choices[0].message.content or "")
        print(f"\nAI：{assistant_reply}")

        messages.append({"role": "assistant", "content": assistant_reply})

    except Exception as e:
        print(f"\n调用失败：{e}")