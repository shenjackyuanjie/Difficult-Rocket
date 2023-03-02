#  -------------------------------
#  Difficult Rocket
#  Copyright © 2020-2023 by shenjackyuanjie 3695888@qq.com
#  All rights reserved
#  -------------------------------

from Difficult_Rocket.exception import BaseError

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
    def __init__(self, value: dict = None, item_names: list = None):
        self.item_names: list = item_names
        self.value: dict = value

    def __str__(self):
        return f"{self.__class__.__name__}: Can't get item {'. '.join(self.item_names)} from: {self.value}"


class TranslateFileNotFound(TranslateError):
    """翻译文件缺失"""



