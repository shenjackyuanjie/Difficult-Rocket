#  -------------------------------
#  Difficult Rocket
#  Copyright © 2020-2023 by shenjackyuanjie 3695888@qq.com
#  All rights reserved
#  -------------------------------

"""
writen by shenjackyuanjie
mail:   3695888@qq.com
github: @shenjackyuanjie
gitee:  @shenjackyuanjie
"""

# system function
import re

from typing import Union, Optional, Type, Tuple, List

# DR
from Difficult_Rocket.exception.command import *

search_re = re.compile(r'(?<!\\)"')


class CommandText:
    """
    CommandLine返回的字符，可以用来搜索
    """

    def __init__(self, text: str):
        self.plain_command = text
        self.text = text
        self.error = False
        self.value_dict = {}

    def counter(self, start: Optional[int] = 0) -> int:
        assert isinstance(start, int)
        i = start
        while True:
            yield i
            if self.error:
                break
            i += 1

    def find(self, text: str) -> Union[str, bool]:
        return finding.group() if (finding := re.match(text, self.text)) else False

    def re_match(self, text: str) -> bool:
        if finding := re.match(text, self.text):
            try:
                next_find = self.text[finding.span()[1]]
                # 这里try因为可能匹配到的是字符串末尾
                # 20230122 我现在也不知道为啥这么写了
                # 果然使用正则表达式就是让一个问题变成两个问题
            except IndexError:
                self.text = self.text[finding.span()[1] + 1:]
                return True
            if next_find == ' ':
                return True
        # 将匹配到的字符串，和最后一个匹配字符后面的字符删除(相当暴力的操作)
        return False

    def int_value(self, name: Optional[str]):
        ...

    def value(self,
              name: str = None,
              split: str = ' ',
              middle: list = ('\'', '\"')):
        pass

    def get_all(self, value_name: str):
        self.value_list.append(self.text)
        if value_name:
            self.value_dict[value_name] = self.text
        self.text = ''
        return self.value_list[-1]

    def get_value(self):
        pass

    def __str__(self):
        return str(self.text)

    def __int__(self):
        return int(self.text)
