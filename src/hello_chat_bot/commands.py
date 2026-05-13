from dataclasses import dataclass


'''
HELP_TEXT = """可用命令：
    /help    查看帮助
    /clear   清空当前上下文
    /model   查看当前模型
    /config  查看当前非敏感配置
    /exit    退出程序
'''


@dataclass(frozen=True)
class CommandResult:
    handled: bool # 这是不是一个已处理的命令
    message: str = "" # 需要打印给用户看的内容
    should_exit: bool = False # 主循环是否退出
    should_clear: bool = False # 主循环是否清空 messages

HELP_TEXT = """可用命令：
/help    查看帮助
/clear   清空当前上下文
/model   查看当前模型
/config  查看当前非敏感配置
/exit    退出程序
"""

def handle_command(user_input: str, config) -> CommandResult:
    command = user_input.strip()
    if not command.startswith("/"):
        return CommandResult(handled=False)
    if command == "/help":
        return CommandResult(
            handled=True,
            message=HELP_TEXT,
        )
    if command == "/clear":
        return CommandResult(
            handled=True,
            message="已清空当前上下文。",
            should_clear=True,
        )
    if command == "/model":
        return CommandResult(
            handled=True,
            message=f"当前模型：{config.model_name}",
        )
    if command == "/config":
        return CommandResult(
            handled=True,
            message=(
                "当前配置：\n"
                f"- base_url: {config.base_url}\n"
                f"- model_name: {config.model_name}\n"
                f"- temperature: {config.temperature}"
            ),
        )
    if command in ["/exit", "/quit", "/q"]:
        return CommandResult(
            handled=True,
            message="已退出。",
            should_exit=True,
        )
    return CommandResult(
        handled=True,
        message=f"未知命令：{command}\n输入 /help 查看可用命令。",
    )