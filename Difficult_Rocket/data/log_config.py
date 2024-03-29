#  -------------------------------
#  Difficult Rocket
#  Copyright © 2020-2023 by shenjackyuanjie 3695888@qq.com
#  All rights reserved
#  -------------------------------


default_config = """config_version = 1

[Logger]

    [Logger.client]
    # 日志名称
    logger_name = "client"
    level_name = "debug"
    # or 'DEBUG'
    # or level = 10
    outputs = ["std_out", "file_out"]

    [Logger.server]
    # 日志名称
    logger_name = "server"
    level_name = "debug"
    # or 'DEBUG'
    # or level = 10
    outputs = ["std_out", "file_out"]

    [Logger.main]
    # 日志名称
    logger_name = "main"
    level_name = "debug"
    # or 'DEBUG'
    # or level = 10
    outputs = ["std_out", "file_out"]

[Formatter]

    [Formatter.main_formatter]
    # 格式化器名称
    class = "MainFormatter"
    # 格式化器参数
    time_format = "%Y-%m-%d %H:%M:%S"
    msec_time_format = "{}-{:03d}"
    use_absolute_path = false

    [Formatter.std_formatter]
    class = "StdFormatter"
    sub_formatter = ["main_formatter"]
    default_template = "[${log_time}][${level}]|${logger_name}:${logger_tag}|${messages}"

[Outstream]

    [Outstream.std_out]
    # 输出流名称
    class = "StdioOutputStream"
    # 输出流参数
    formatter = "std_formatter"
    use_stderr = false
    # or true
    level_name = "debug"
    # or 'DEBUG'
    # or level = 10

    [Outstream.file_out]
    class = "FileCacheOutputStream"

    level = 10
    # or level_name = 'DEBUG'
    # or level_name = 'debug'
    formatter = "std_formatter"
    flush_count_limit = 10
    # 5 条日志刷新一次
    flush_time_limit = 5
    # 5 秒刷新一次
    # or flush_time_limit = 0.5
    file_path = "./logs"
    file_name = "dr-{time}.log"

"""

# 整的跟 export 一样
# fmt: off
__all__ = [
    "default_config"
]
# fmt: on
