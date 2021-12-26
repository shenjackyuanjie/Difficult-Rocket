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
from typing import List, Dict, Union

from Difficult_Rocket import translate

# [\u4e00-\u9fa5] 中文字符
compiler = Union[re.compile, parse.compile]
compiler = Union[compiler]
fonts_config = List[Dict[str: str, str: compiler, str: Dict[str: str, str: str]]]
default_fonts_config = [
    {
        'match':  re.compile(r'.'),  # 匹配的字符  匹配选项可以是re.compile() 或者 parse.compile() 或者有 .parse的方法都可以（一定要有返回值）
        'shown':  parse.compile(r'{}'),  # 匹配到的字符中显示的部分
        'mode':   'default',
        'name':   translate.鸿蒙简体,
        'size':   12,
        'bold':   False,
        'italic': False,
        'color':  'black'
    },
    {
        'match': re.compile(r'[a-zA-Z]'),
        'shown': re.compile(r'[a-zA-Z]'),
        'mode':  'default',
        'name':  translate.微软等宽,
    },
    # Markdown 语法规则匹配
    {
        # Markdown 粗体语法规则匹配
        'match': re.compile(r'\*\*(.*?(?<!\s))\*\*'),
        'shown': re.compile(r'(?<=\*\*)(.*?(?<!\s))(?=\*\*)'),
        'mode':  'set',
        'bold':  True,
        'tag':   {
            # 为 match 匹配到的字符添加标签
            'match': re.compile(r'\*\*'),
            'name':  'bold'
        }
    },
    {
        # Markdown 斜体语法规则匹配
        'match':  re.compile(r'\*(.*?(?<!\s))\*'),
        'shown':  re.compile(r'(?<=\*)(.*?(?<!\s))(?=\*)'),
        'mode':   'set',
        'italic': True,
        'ignore': {
            # 如果匹配到的字符含有 tag 就忽略本次解析
            'match': re.compile(r'\*'),
            'tag': 'bold'
        }
    },
    {
        # Markdown 链接规则匹配
        # 注意：这里的匹配模式是非贪婪的，即匹配到的结果必须是完整的
        # 即：链接名称不能是空格等空白字符开头，链接名称不能是空格等空白字符结尾
        # 匹配的内容：[abc](def)
        # 显示的内容：abc
        'match': re.compile(r'\[(.*?(?<!\s))\]\((.*?(?<!\s))\)'),
        'shown': parse.compile(r'[{}]({})')
    }
]


def decode_text_to_HTML(text: str,
                        config: fonts_config=default_fonts_config) -> str:
    style_list = range(0, len(text))  # 字体样式列表
    tag_list = range(0, len(text))  # 字符标签列表
    style_HTML_str = ''  # 字体样式HTML字符串


