#  -------------------------------
#  Difficult Rocket
#  Copyright © 2021-2022 by shenjackyuanjie
#  All rights reserved
#  -------------------------------

from Difficult_Rocket.api.Exp import Error


class LanguageError(Error):
    """语言相关 error"""


class TranslateFileNotFoundError(LanguageError):
    """某个语言的翻译文件未找到"""
