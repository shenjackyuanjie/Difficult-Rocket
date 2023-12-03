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

from pyglet.text import DocumentLabel


class FontsLabel(DocumentLabel):
    """
    一个基于HTMLLabel的 可以同时在一行字里面显示多种字体的 Label
    """

    def __init__(self, x, y, width, height):
        super().__init__(x, y, width, height)
        self._text = "a"
        self.formatted_text = "a"
