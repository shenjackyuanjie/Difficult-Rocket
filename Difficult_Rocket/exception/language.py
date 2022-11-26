#  -------------------------------
#  Difficult Rocket
#  Copyright © 2021-2022 by shenjackyuanjie 3695888@qq.com
#  All rights reserved
#  -------------------------------

from Difficult_Rocket.exception import BaseError, BaseRuntimeError

__all__ = ['LanguageNotFound',
           'TranslateError',
           'TranslateKeyNotFound',
           'TranslateFileNotFound']


class LanguageNotFound(BaseError):
    """语言文件缺失"""


class TranslateError(BaseError):
    """翻译相关问题"""


class TranslateKeyNotFound(TranslateError):
    """语言文件某项缺失"""
    def __init__(self, item_names: list):
        self.item_names: list = item_names

    def __str__(self):
        return f"{self.__class__.__name__}: Can't get item {'. '.join(self.item_names)}"


class TranslateFileNotFound(TranslateError):
    """翻译文件缺失"""



