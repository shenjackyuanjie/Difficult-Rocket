#  -------------------------------
#  Difficult Rocket
#  Copyright © 2020-2023 by shenjackyuanjie 3695888@qq.com
#  All rights reserved
#  -------------------------------

from typing import Tuple

from pyglet.graphics import Batch, Group

from Difficult_Rocket.gui.widget.theme import BaseTheme, FontTheme

_RGBA = Tuple[int, int, int, int]


class ButtonBaseTheme(BaseTheme):
    """
    Base theme of button
    inherit from BaseTheme and dict
    按钮的基础主题
    继承了 BaseTheme 和 dict
    """
    theme_name = 'Button Base Theme'

    def init(self, batch: Batch, group: Group, **kwargs) -> None:
        """
        Init theme
        :param batch: batch
        :param group: group
        :param kwargs: options
        :return: None
        """
        self.batch = batch
        self.group = group
        self.font_theme = FontTheme(**kwargs)


class BlockTheme(ButtonBaseTheme):
    """
    button theme: Block like button
    """
    theme_name = 'Block Theme(button)'
    main_color: _RGBA = (39, 73, 114, 255)
    touch_color: _RGBA = (66, 150, 250, 255)
    hit_color: _RGBA = (15, 135, 250, 255)

    font_theme: FontTheme = FontTheme()

