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



class Error(Exception):
    """基础 Exception"""
    pass


class TexturesError(Error):
    """材质相关error 包含info和textures"""

    def __init__(self, info, textures):
        self.info = info
        self.textures = textures

    def __str__(self):
        return '{}{}'.format(self.info, self.textures)


class LanguageError(Error):
    """lang文件相关error 包含info和language"""

    def __init__(self, info, language):
        self.info = info
        self.lang = language

    def __str__(self):
        return '{}{}'.format(self.info, self.lang)
