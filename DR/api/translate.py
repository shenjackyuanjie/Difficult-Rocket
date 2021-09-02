"""
writen by shenjackyuanjie
mail:   3695888@qq.com
github: @shenjackyuanjie
gitee:  @shenjackyuanjie
"""


class Lang:
    """
    用于创建一个对应语言的翻译类
    感谢Fallen的MCDR提供idea
    https://github.com/Fallen-Breath/MCDReforged
    """
    def __init__(self, language: str):
        self.语言 = language
        self.翻译结果 = {}

    def __str__(self):
        return self.语言

    def __getitem__(self, item):
        return self.翻译结果[item]

    def __setitem__(self, key, value):
        pass
