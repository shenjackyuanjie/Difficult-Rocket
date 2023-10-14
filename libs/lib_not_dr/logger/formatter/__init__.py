#  -------------------------------
#  Difficult Rocket
#  Copyright © 2020-2023 by shenjackyuanjie 3695888@qq.com
#  All rights reserved
#  -------------------------------
import time

from pathlib import Path
from string import Template
from typing import List, Union, Optional, Dict, Tuple, TYPE_CHECKING

from lib_not_dr.logger import LogLevel
from lib_not_dr.types.options import Options
from lib_not_dr.logger.structure import LogMessage, FormattingMessage

if TYPE_CHECKING:
    from lib_not_dr.logger.formatter.colors import BaseColorFormatter


class BaseFormatter(Options):
    name = 'BaseFormatter'

    sub_formatter: List['BaseFormatter'] = []
    color_formatters: List['BaseColorFormatter'] = []
    default_template: str = '[${log_time}][${level}]|${logger_name}:${logger_tag}|${messages}'

    @classmethod
    def add_info(cls, match: str, to: str, description: str) -> str:
        return f'- {to} -> ${{{match}}} : {description}'

    @classmethod
    def info(cls) -> str:
        infos = {BaseFormatter.name: BaseFormatter._info()}
        cache = ''
        for formatter in cls.sub_formatter:
            infos[formatter.name] = formatter._info()
        infos[cls.name] = cls._info()
        for name, info in infos.items():
            cache += f"## {name}\n"
            cache += info
            cache += '\n'
        return cache

    @classmethod
    def _info(cls) -> str:
        info = cls.add_info('logger_name', 'logger name', 'The name of the logger')
        info += '\n'
        info += cls.add_info('logger_tag', 'logger tag', 'The tag of the logger')
        return info

    def format_message(self,
                       message: LogMessage,
                       template: Optional[Union[Template, str]] = None) -> str:
        """
        Format message
        :param message: 输入的消息
        :param template: 日志输出模板
        :return:
        """
        basic_info = message.format_for_message()
        message, info = self._format((message, basic_info))

        if template is None:
            template = Template(self.default_template)
        elif isinstance(template, str):
            template = Template(template)

        try:
            return template.substitute(**info)
        except (KeyError, ValueError):
            return template.safe_substitute(**info)

    def _format(self, message: FormattingMessage) -> FormattingMessage:
        """
        Format message
        :param message:
        :return:
        """
        for formatter in self.sub_formatter:
            message = formatter._format(message)
        return message

    @property
    def template(self) -> str:
        return self.default_template

    @template.setter
    def template(self, template: str) -> None:
        if not isinstance(template, str):
            raise TypeError(f'The template must be str, not {type(template)}')
        self.default_template = template


class LevelFormatter(BaseFormatter):
    name = 'LevelFormatter'

    default_level: int = 20

    # If True, the undefined level will be set to the higher nearest level.
    level_get_higher: bool = True

    level_name_map = {
        LogLevel.notset: 'NOTSET',
        LogLevel.trace:  ' TRACE',
        LogLevel.fine:   ' FINE ',
        LogLevel.debug:  ' DEBUG',
        LogLevel.info:   ' INFO ',
        LogLevel.warn:   ' WARN ',
        LogLevel.error:  'ERROR ',
        LogLevel.fatal:  'FATAL ',
    }
    name_level_map = {
        'NOTSET': LogLevel.notset,
        ' TRACE': LogLevel.trace,
        ' FINE ': LogLevel.fine,
        ' DEBUG': LogLevel.debug,
        ' INFO ': LogLevel.info,
        ' WARN ': LogLevel.warn,
        'ERROR ': LogLevel.error,
        'FATAL ': LogLevel.fatal,
    }

    @classmethod
    def _info(cls) -> str:
        return cls.add_info('level', 'log level', 'The log level')

    def _format(self, message: FormattingMessage) -> FormattingMessage:
        if message[0].level in self.name_level_map:
            level_tag = self.level_name_map[message[0].level]
        else:
            if self.level_get_higher:
                for level in self.name_level_map:
                    if message[0].level <= self.name_level_map[level]:
                        level_tag = level
                        break
                else:
                    level_tag = 'FATAL'
            else:
                for level in self.name_level_map:
                    if message[0].level >= self.name_level_map[level]:
                        level_tag = level
                        break
                else:
                    level_tag = 'NOTSET'
        message[1]['level'] = level_tag
        return message


class TraceFormatter(BaseFormatter):
    name = 'TraceFormatter'

    time_format: str = '%Y-%m-%d %H:%M:%S'
    msec_time_format: str = '{}-{:03d}'
    use_absolute_path: bool = False

    @classmethod
    def _info(cls) -> str:
        info = cls.add_info('log_time', 'formatted time when logging', 'The time format string'
                                                                       '. See https://docs.python.org/3/library/time'
                                                                       '.html#time.strftime for more information.')
        info += '\n'
        info += cls.add_info('log_source', 'logging file', 'the logging file name')
        info += '\n'
        info += cls.add_info('log_line', 'logging line', 'the logging line number')
        info += '\n'
        info += cls.add_info('log_function', 'logging function', 'the logging function name')
        return info

    def _format(self, message: FormattingMessage) -> FormattingMessage:
        message = self._time_format(message)
        message = self._trace_format(message)
        return message

    def _time_format(self, message: FormattingMessage) -> FormattingMessage:
        time_mark = time.localtime(message[0].log_time / 1000000000)
        if self.msec_time_format:
            time_mark = self.msec_time_format.format(time.strftime(self.time_format, time_mark),
                                                     message[0].create_msec_3)
        message[1]['log_time'] = time_mark
        return message

    def _trace_format(self, message: FormattingMessage) -> FormattingMessage:
        if message[0].stack_trace is None:
            return message
        path = Path(message[0].stack_trace.f_code.co_filename)
        if self.use_absolute_path:
            message[1]['log_source'] = path.absolute()
        message[1]['log_source'] = path
        message[1]['log_line'] = message[0].stack_trace.f_lineno
        message[1]['log_function'] = message[0].stack_trace.f_code.co_name
        return message


class StdFormatter(BaseFormatter):
    name = 'StdFormatter'

    enable_color: bool = True

    sub_formatter: List[BaseFormatter] = [LevelFormatter(),
                                          TraceFormatter()]
    from lib_not_dr.logger.formatter.colors import (LevelColorFormatter,
                                                    LoggerColorFormatter,
                                                    TimeColorFormatter,
                                                    TraceColorFormatter,
                                                    MessageColorFormatter)
    color_formatters: List[BaseFormatter] = [LevelColorFormatter(),
                                             LoggerColorFormatter(),
                                             TimeColorFormatter(),
                                             TraceColorFormatter(),
                                             MessageColorFormatter()]

    def __init__(self,
                 enable_color: bool = True,
                 sub_formatter: Optional[List[BaseFormatter]] = None,
                 color_formatters: Optional[List[BaseFormatter]] = None,
                 **kwargs) -> None:
        """
        Initialize the StdFormatter
        :param enable_color: enable color
        :param sub_formatter: list of sub formatter
        :param color_formatters: list of color formatter
        :param kwargs: other options
        """
        # 同 structures.LogMessage.__init__ 的注释 (逃)
        self.enable_color = enable_color
        if sub_formatter is not None:
            self.sub_formatter = sub_formatter
        if color_formatters is not None:
            self.color_formatters = color_formatters
        super().__init__(**kwargs)

    def _format(self, message: FormattingMessage) -> FormattingMessage:
        super()._format(message)

        if not self.enable_color:
            return message

        for formatter in self.color_formatters:
            message = formatter._format(message)

        return message

    @classmethod
    def _info(cls) -> str:
        return 'None'


if __name__ == '__main__':
    import inspect

    log_message = LogMessage(messages=['Hello World!'],
                             level=7,
                             stack_trace=inspect.currentframe(),
                             logger_tag='tester',
                             logger_name='test')

    print(LevelFormatter.info())
    print(LevelFormatter().format_message(log_message))

    print(TraceFormatter.info())
    print(TraceFormatter().format_message(log_message))

    print(StdFormatter.info())
    print(StdFormatter().format_message(log_message))

    std_format = StdFormatter()
    std_format.default_template = "${log_time}|${logger_name}|${logger_tag}|${log_source}:${log_line}|${log_function}|${level}|${messages}"

    test_levels = (0, 5, 7, 10, 20, 30, 40, 50)

    print("with color")

    for test_level in test_levels:
        log_message.level = test_level
        print(std_format.format_message(log_message), end='')

    print("without color")

    std_format.enable_color = False

    for test_level in test_levels:
        log_message.level = test_level
        print(std_format.format_message(log_message), end='')

    print(std_format.as_markdown())
