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

from typing import Optional, Union, Tuple

# from libs import pyglet
# from pyglet import font
from pyglet.text import Label, HTMLLabel
from pyglet.window import key
from pyglet.gui import widgets
# from pyglet.sprite import Sprite
from pyglet.shapes import Rectangle
# from pyglet.image import AbstractImage
from pyglet.graphics import Batch, Group
from pyglet.text.caret import Caret
from pyglet.text.document import UnformattedDocument
from pyglet.text.layout import IncrementalTextLayout

from Difficult_Rocket.api.types import Fonts
from Difficult_Rocket import DR_status


class PressTextButton(widgets.WidgetBase):
    """
    自带 字符 + 材质 的按钮，就不用单独做材质了
    """

    def __init__(self,
                 x: int,
                 y: int,
                 width: int,
                 height: int,
                 text: str,
                 font: str = Fonts.鸿蒙简体,
                 font_size: int = 13,
                 batch: Optional[Batch] = None,
                 group: Optional[Group] = None,
                 ):
        super().__init__(x, y, width, height)
        self.back_ground_batch = Batch()
        self.front_batch = batch or Batch()
        if group:
            self.front_group = Group(order=5, parent=group)
            self.back_ground_group = Group(order=10, parent=group)
        else:
            self.front_group = Group(order=5)
            self.back_ground_group = Group(order=10)

        self.untouched_color = (39, 73, 114, 255)
        self.touched_color = (66, 150, 250, 255)
        self.hit_color = (15, 135, 250, 255)
        # from ImGui

        self.text = text
        self.text_label = Label(font_name=font, font_size=font_size,
                                batch=self.front_batch, group=self.front_group)
        self.back_rec = Rectangle(x=self._x, y=self._y, width=self._width, height=self._height,
                                  color=self.untouched_color,  # ImGui color
                                  batch=self.back_ground_batch, group=self.back_ground_group)

    @property
    def value(self):
        return self.text

    def __contains__(self, item):
        return item in self.back_rec

    def on_mouse_motion(self, x, y, dx, dy):
        if (x, y) in self:
            self.back_rec.color = self.touched_color
        else:
            self.back_rec.color = self.untouched_color

    def on_mouse_press(self, x, y, buttons, modifiers):
        if (x, y) in self:
            self.back_rec.color = self.hit_color
            self.dispatch_event('on_press', x, y)
            return True
        return False

    def _update_position(self):
        self.text_label.position = self._x, self._y
        self.back_rec.position = self._x, self._y
        self.back_rec.width = self._width
        self.back_rec.height = self._height
        ...


PressTextButton.register_event_type('on_press')
