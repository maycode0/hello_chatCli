# Hello Chat Bot

Hello Chat Bot 是一个用于学习 AI Agent 与 AI 应用开发的命令行小项目。

这个项目从最小可运行的 AI 对话 CLI 开始，逐步补充配置校验、异常处理、上下文管理、命令系统、会话保存等能力。它的目标不是一开始就做复杂框架，而是通过一个小型项目理解 AI 应用的基本工程结构。

## 项目定位

这是一个学习型项目，主要用于练习：
- 如何用 Python 调用 OpenAI-compatible 大模型 API
- 如何用 uv 管理 Python 项目和依赖
- 如何组织一个 CLI AI 对话程序
- 如何逐步把 demo 改造成更可靠的工具
- 如何为后续 AI Agent 能力打基础

当前阶段重点是 AI 对话 CLI。后续会逐步加入工具调用、命令系统、会话管理等能力，让项目向简单 AI Agent 演进。

## 当前已具备的功能

- 支持命令行连续对话
- 支持通过 OpenAI-compatible API 调用大模型
- 支持从 `.env` 读取配置
- 支持配置校验
  - 检查 `OPENAI_API_KEY` 是否存在
  - 检查 `OPENAI_BASE_URL` 是否存在
  - 支持 `MODEL_NAME` 默认值
  - 支持 `TEMPERATURE` 默认值
  - 校验 `TEMPERATURE` 是否为合法数字
  - 配置错误时在启动阶段给出提示
- 支持基础文本清洗，避免部分非法 Unicode 字符导致请求失败
- 使用 uv 管理依赖和运行环境
- 使用 pytest 编写配置校验测试

## 当前项目结构

```
hello_chat_bot/
  pyproject.toml
  uv.lock
  README.md
  TODO.md
  .env
  src/
    hello_chat_bot/
      config.py
      main.py
      init.py
  test/
    test_config.py
```

说明：
- `src/hello_chat_bot/config.py`：负责读取和校验配置
- `src/hello_chat_bot/main.py`：负责 CLI 对话主流程
- `test/test_config.py`：负责测试配置校验逻辑
- `TODO.md`：记录后续鲁棒性增强计划

## 环境配置

项目使用 uv 管理依赖。

安装依赖：

```
uv sync
```

如果还没有安装开发测试依赖，可以执行：

```
uv add --dev pytest
```

## 配置 `.env`

在项目根目录创建 `.env` 文件：

```
OPENAI_API_KEY=你的_api_key
OPENAI_BASE_URL=https://api.deepseek.com
MODEL_NAME=deepseek-chat
TEMPERATURE=0.7
```

说明：
- `OPENAI_API_KEY`：模型服务 API Key，必填
- `OPENAI_BASE_URL`：OpenAI-compatible API 地址，必填
- `MODEL_NAME`：模型名称，可选
- `TEMPERATURE`：生成随机性，可选，默认 0.7

注意：`.env` 中可能包含密钥，不应该提交到 Git 仓库。

## 运行项目

推荐使用 uv 运行：

```
uv run python -m hello_chat_bot.main
```

如果已经配置了脚本入口，也可以使用：

```
uv run hello-chat-bot
```

启动后，在终端输入问题即可和模型对话。输入 `exit`、`quit` 或 `q` 可以退出。

## 运行测试

运行全部测试：

```
uv run pytest
```

只运行配置测试：

```
uv run pytest test/test_config.py
```

当前配置校验测试已经覆盖：
- 缺少 `OPENAI_API_KEY` 的情况
- 缺少 `OPENAI_BASE_URL` 的情况
- `MODEL_NAME` 默认值
- `TEMPERATURE` 默认值
- 非法 `TEMPERATURE`
- 超出范围的 `TEMPERATURE`
- 正常配置加载

## 后续计划

后续会逐步增加以下功能：

- 基础命令系统
  - `/help`：查看可用命令
  - `/clear`：清空当前上下文
  - `/model`：查看当前模型
  - `/config`：查看非敏感配置
  - `/exit`：退出程序

- 精细异常处理
  - 区分 API Key 错误
  - 区分模型名称错误
  - 区分网络连接失败
  - 区分代理配置错误
  - 区分请求超时、限流和服务端错误

- 超时与自动重试
  - 设置连接超时和读取超时
  - 对网络波动、429、5xx 错误进行有限重试
  - 避免一次请求长时间卡死

- 上下文长度管理
  - 限制最大历史轮数
  - 保留 system prompt
  - 裁剪过早的历史消息
  - 后续支持自动总结历史

- 流式输出
  - 支持模型边生成边显示
  - 提升 CLI 使用体验

- 会话持久化
  - 自动保存会话
  - 支持 JSONL 和 Markdown 导出
  - 支持恢复历史会话

- 日志、Token 与费用统计
  - 记录请求时间、模型名称、错误类型
  - 统计 token 使用量
  - 后续支持估算调用成本

- 项目结构拆分
  - `client.py`：封装模型 API 调用
  - `chat.py`：管理对话主循环
  - `commands.py`：处理 CLI 命令
  - `storage.py`：保存和加载会话
  - `utils.py`：通用工具函数

## 学习目标

通过这个项目，希望逐步掌握：
- AI 应用的最小闭环：输入、调用模型、输出结果、保存上下文
- OpenAI-compatible API 的基本使用方式
- Python CLI 应用的基本结构
- 配置管理和测试驱动开发的基础
- 从普通聊天机器人过渡到 AI Agent 的工程思路

这个项目会随着学习进度持续演进。当前它是一个简单 AI 对话 CLI，未来会逐步加入更多 AI Agent 相关能力。
