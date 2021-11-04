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

from ..api import translate

from libs import pyglet
from libs.pyglet.gui import widgets
from libs.pyglet.sprite import Sprite
from libs.pyglet.graphics import Batch, Group
from libs.pyglet.image import AbstractImage

__all__ = ['Parts']


class Parts(widgets.WidgetBase):
    """
    parts
    """

    def __init__(self,
                 x: int,
                 y: int,
                 width: int,
                 height: int,
                 textures: AbstractImage,
                 batch: Batch,
                 parts_data: dict):
        super().__init__(x, y, width, height)
        self.sprite = Sprite(img=textures, x=x, y=y, batch=batch)
        self._value = 0


class InputBox(widgets.WidgetBase):
    """
    input box
    """

    def __init__(self,
                 x: int,
                 y: int,
                 width: int,
                 height: int,
                 batch: Batch,
                 group: Group,
                 message: str = ''):
        super().__init__(x, y, width, height)

    @property
    def value(self):
        return self.enabled

    def _update_position(self):
        pass

a = InputBox(1, 2, 3, 4, 5, 6, 7)

