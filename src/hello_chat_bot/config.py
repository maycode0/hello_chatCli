import os
from dataclasses import dataclass
from dotenv import load_dotenv


# ConfigError：配置错误专用异常
class ConfigError(Exception):
    pass
# AppConfig：保存配置结果，避免到处用 os.getenv()
@dataclass(frozen=True)
class AppConfig:
    api_key: str
    base_url: str
    model_name: str
    temperature: float

# 必填环境变量检查函数：
# - OPENAI_API_KEY
# - OPENAI_BASE_URL
# 缺少就直接报清楚的错误
def get_required_env(name: str) -> str:
    value = os.getenv(name)
    if value is None or not value.strip():
        raise ConfigError(f"缺少必要配置：{name}。请在 .env 文件中设置它。")
    return value.strip()

# temperature 校验函数
def get_temperature() -> float:
    raw_value = os.getenv("TEMPERATURE", "0.7").strip()
    try:
        temperature = float(raw_value)
    except ValueError:
        raise ConfigError("TEMPERATURE 必须是数字，例如 0.7。")
    if not 0 <= temperature <= 2:
        raise ConfigError("TEMPERATURE 必须在 0 到 2 之间。")
    return temperature

# 写统一加载配置函数
def load_config(load_env: bool = True) -> AppConfig:
    if load_env:
        load_dotenv()
    api_key = get_required_env("OPENAI_API_KEY")
    base_url = get_required_env("OPENAI_BASE_URL")
    # model_name = os.getenv("MODEL_NAME", "deepseek-chat").strip() or "deepseek-chat"
    model_name = os.getenv("MODEL_NAME", "gpt-5.4").strip() or "gpt-5.4"
    temperature = get_temperature()
    return AppConfig(
        api_key=api_key,
        base_url=base_url,
        model_name=model_name,
        temperature=temperature,
    )