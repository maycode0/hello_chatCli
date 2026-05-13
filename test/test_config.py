import pytest
from hello_chat_bot.config import AppConfig, ConfigError, load_config

# monkeypatch 是 pytest 自带的测试工具，作用是临时修改环境变量。测试结束后，它会自动恢复环境，不会污染你的真实系统环境
def test_load_config_requires_api_key(monkeypatch):
    '''1缺少 `OPENAI_API_KEY` 会报错'''
    monkeypatch.delenv("OPENAI_API_KEY", raising=False) # 如果要删除的环境变量不存在，也不要报错
    monkeypatch.setenv("OPENAI_BASE_URL", "https://api.deepseek.com")
    monkeypatch.setenv("MODEL_NAME", "deepseek-chat")
    monkeypatch.setenv("TEMPERATURE", "0.7")

    with pytest.raises(ConfigError, match="OPENAI_API_KEY"):
        load_config(load_env=False)

def test_load_config_requires_base_url(monkeypatch):
    '''2缺少 `OPENAI_BASE_URL` 会报错'''
    monkeypatch.setenv("OPENAI_API_KEY", "test-key")
    monkeypatch.delenv("OPENAI_BASE_URL", raising=False)# 如果要删除的环境变量不存在，也不要报错
    monkeypatch.setenv("MODEL_NAME", "deepseek-chat")
    monkeypatch.setenv("TEMPERATURE", "0.7")

    with pytest.raises(ConfigError, match="OPENAI_BASE_URL"):
        load_config(load_env=False) 

def test_load_config_uses_default_model_name(monkeypatch):
    '''3缺少 `MODEL_NAME` 时使用默认模型 '''
    monkeypatch.setenv("OPENAI_API_KEY", "test-key")
    monkeypatch.setenv("OPENAI_BASE_URL", "https://api.deepseek.com")
    monkeypatch.delenv("MODEL_NAME", raising=False)# 如果要删除的环境变量不存在，也不要报错
    monkeypatch.setenv("TEMPERATURE", "0.7")

    config = load_config(load_env=False)
    # assert config.model_name == "deepseek-chat"
    assert config.model_name == "gpt-5.4"
        
def test_load_config_uses_default_temperature(monkeypatch):
    '''4缺少 `TEMPERATURE` 时使用默认值 0.7 '''
    monkeypatch.setenv("OPENAI_API_KEY", "test-key")
    monkeypatch.setenv("OPENAI_BASE_URL", "https://api.deepseek.com")
    monkeypatch.setenv("MODEL_NAME", "deepseek-chat")
    monkeypatch.delenv("TEMPERATURE", raising=False)# 如果要删除的环境变量不存在，也不要报错

    config = load_config(load_env=False)
    assert config.temperature == 0.7


def test_load_config_rejects_invalid_temperature(monkeypatch):
    '''5缺少 `TEMPERATURE` 不是数字时报错 '''
    monkeypatch.setenv("OPENAI_API_KEY", "test-key")
    monkeypatch.setenv("OPENAI_BASE_URL", "https://api.deepseek.com")
    monkeypatch.setenv("MODEL_NAME", "deepseek-chat")
    monkeypatch.setenv("TEMPERATURE", "abc")

    with pytest.raises(ConfigError, match="TEMPERATURE"):
        load_config(load_env=False) 

def test_load_config_rejects_temperature_out_of_range(monkeypatch):
    '''6缺少 `TEMPERATURE` 超出范围时报错 '''
    monkeypatch.setenv("OPENAI_API_KEY", "test-key")
    monkeypatch.setenv("OPENAI_BASE_URL", "https://api.deepseek.com")
    monkeypatch.setenv("MODEL_NAME", "deepseek-chat")
    monkeypatch.setenv("TEMPERATURE", "3")

    with pytest.raises(ConfigError, match="TEMPERATURE"):
        load_config(load_env=False) 

def test_load_config_returns_config(monkeypatch):
    '''7加载配置时返回配置对象 '''
    monkeypatch.setenv("OPENAI_API_KEY", "test-key")
    monkeypatch.setenv("OPENAI_BASE_URL", "https://api.deepseek.com")
    monkeypatch.setenv("MODEL_NAME", "gpt-5.4")
    monkeypatch.setenv("TEMPERATURE", "0.7")

    config = load_config(load_env=False)
    assert config == AppConfig(
        api_key="test-key",
        base_url="https://api.deepseek.com",
        model_name="gpt-5.4",
        temperature=0.7,
    )
