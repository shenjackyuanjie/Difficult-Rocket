#  -------------------------------
#  Difficult Rocket
#  Copyright © 2021 by shenjackyuanjie
#  All rights reserved
#  -------------------------------

"""
writen by shenjackyuanjie
mail:   3695888@qq.com
github: @shenjackyuanjie
gitee:  @shenjackyuanjie
"""

import re
import parse
import pprint
from typing import List, Dict, Union, Iterable

from Difficult_Rocket import translate


class SingleTextStyle:
    """
    单个字符的字体样式
    """

    def __init__(self,
                 font_name: str = '',
                 font_size: int = 15,
                 bold: bool = False,
                 italic: bool = False,
                 color: str = 'black',
                 text_tag: list = None,
                 show: bool = True,
                 text: str = ''):
        self.font_name = font_name
        self.font_size = font_size
        self.bold = bold
        self.italic = italic
        self.color = color
        self._tag = text_tag
        self.show = show
        self.text = text

    @property
    def tag(self) -> list:
        return self._tag

    @tag.setter
    def tag(self, value: list):
        assert type(value) == list, 'SingleTextStyle.tag must be list'
        for tag in value:
            if tag not in self._tag:
                self._tag.append(tag)
        self._tag.sort()

    """
    对运算操作的支持
    """

    def __add__(self, other: 'SingleTextStyle') -> 'SingleTextStyle':
        """
        叠加两个字体样式 优先使用 other 的样式
        :param other: 叠加的字体样式
        :return: 叠加后的字体样式
        """
        assert type(other) == SingleTextStyle, f'SingleTextStyle + other\n other must be the same type, not a {type(other)}'
        return SingleTextStyle(
                font_name=other.font_name or self.font_name,
                font_size=other.font_size or self.font_size,
                bold=other.bold or self.bold,
                italic=other.italic or self.italic,
                color=other.color or self.color,
                text_tag=other.tag + self.tag,
                show=other.show or self.show,
                text=self.text
        )

    def __iadd__(self, other: 'SingleTextStyle') -> 'SingleTextStyle':
        """
        叠加两个字体样式 优先使用 other 的样式
        :param other: 叠加的字体样式
        :return: 叠加后的字体样式
        """
        assert type(other) == SingleTextStyle, f'SingleTextStyle += other\n other must be the same type, not a {type(other)}'
        self.font_name = other.font_name or self.font_name
        self.font_size = other.font_size or self.font_size
        self.bold = other.bold or self.bold
        self.italic = other.italic or self.italic
        self.color = other.color or self.color
        self.tag += other.tag
        self.show = other.show or self.show
        self.text = self.text
        return self

    def same_tag(self, other: 'SingleTextStyle') -> bool:
        """
        比较两个字体样式是否相同
        :param other: 叠加的字体样式
        :return: 是否相同
        """
        assert type(other) == SingleTextStyle
        return self.tag == other.tag


# [\u4e00-\u9fa5] 中文字符
default_fonts_config = [
    {
        'match': re.compile(r'.'),  # 匹配的字符  匹配选项是re.compile()
        'shown': re.compile(r'.'),  # 匹配到的字符中显示的部分  匹配选项是re.compile()
        'style': SingleTextStyle(font_name=translate.鸿蒙简体, font_size=15, bold=False, italic=False, show=True, color='black'),
    },
    {
        'match': re.compile(r'[a-zA-Z]'),
        'shown': re.compile(r'[a-zA-Z]'),
        'style': SingleTextStyle(font_name=translate.微软等宽)
    },
    # Markdown 语法规则匹配
    {
        # Markdown 粗体语法规则匹配
        'match': re.compile(r'\*\*(.*?(?<!\s))\*\*'),
        'shown': re.compile(r'(?<=\*\*)(.*?(?<!\s))(?=\*\*)'),
        'tag':   {
            # 为 match 匹配到的字符添加标签
            'match': re.compile(r'\*\*'),
            'style': SingleTextStyle(text_tag=['bold'])
        },
        'style': SingleTextStyle(bold=True)
    },
    {
        # Markdown 斜体语法规则匹配
        'match':  re.compile(r'\*(.*?(?<!\s))\*'),
        'shown':  re.compile(r'(?<=\*)(.*?(?<!\s))(?=\*)'),
        'ignore': {
            # 如果匹配到的字符含有 tag 就忽略本次解析
            'match': re.compile(r'\*'),
            'style': SingleTextStyle(text_tag=['italic'])
        },
        'style': SingleTextStyle(italic=True)
    },
    {
        # Markdown 链接规则匹配
        # 注意：这里的匹配模式是非贪婪的，即匹配到的结果必须是完整的
        # 即：链接名称不能是空格等空白字符开头，链接名称不能是空格等空白字符结尾
        # 匹配的内容：[abc](def)
        # 显示的内容：abc
        'match': re.compile(r'\[(.*?(?<!\s))\]\((.*?(?<!\s))\)'),
        'shown': re.compile(r'(?<=\[)(.*?(?<!\s))(?=\]\((.*?(?<!\s))\))')
    }
]


def decode_text_to_HTML(text: str,
                        config=None) -> str:
    if config is None:
        config = default_fonts_config
    style_list = [SingleTextStyle() for x in range(len(text))]
    style_HTML_str = ''  # 字体样式HTML字符串


