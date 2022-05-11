#  -------------------------------
#  Difficult Rocket
#  Copyright © 2021-2022 by shenjackyuanjie
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

from typing import Union

# DR
from Difficult_Rocket.api.Exp import CommandQuotationMarkError

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
        self.value_list = []
        self.command_tree = {}
        tree_list = text.split(' ')

        pass_node = False
        for node in tree_list:
            if node[0] == "\"" and len(node) > 1:  # |"xxxxx|
                if pass_node:  # |"xxxx "xxxx|
                    self.error = CommandQuotationMarkError
                pass_node = True
                first_node = tree_list.index(node)
            if node[-1] == "\"" and len(node) > 1:  # |xxxxxx"|
                pass_node = False

    def find(self, text: str) -> Union[str, bool]:
        finding = re.match(text, self.text)
        if finding:
            return finding.group()
        else:
            return False

    def match(self, text: str) -> bool:
        finding = re.match(text, self.text)
        if finding:  # 如果找到了
            try:
                next_find = self.text[finding.span()[1]]
                # 这里try因为可能匹配到的是字符串末尾
            except IndexError:
                next_find = ' '
                # 直接过滤掉
            if next_find == ' ':
                self.text = self.text[finding.span()[1] + 1:]
                return True
            # 将匹配到的字符串，和最后一个匹配字符后面的字符删除(相当暴力的操作)
            return False
        else:
            return False

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
