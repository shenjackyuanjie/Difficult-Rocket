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
from pyglet.text import Label
from pyglet.window import mouse
from pyglet.gui import widgets
# from pyglet.sprite import Sprite
from pyglet.shapes import Rectangle
# from pyglet.image import AbstractImage
from pyglet.graphics import Batch, Group

from Difficult_Rocket.api.types import Fonts

# from Difficult_Rocket import DR_status


RGBA = Tuple[int, int, int, int]


class BaseTheme:
    """
    用于定义主题的类
    """

    def __init__(self,
                 main_color: RGBA = (39, 73, 114, 256),
                 secondary_color: RGBA = (66, 150, 250, 256),
                 main_font: str = Fonts.鸿蒙简体,
                 ):
        self.main_color = main_color
        self.secondary_color = secondary_color
        self.main_font = main_font



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
        self.back_ground_batch = batch or Batch()
        self.front_batch = batch or Batch()
        if group:
            self.front_group = Group(order=10, parent=group)
            self.back_ground_group = Group(order=5, parent=group)
        else:
            self.front_group = Group(order=5)
            self.back_ground_group = Group(order=10)

        self.pressed = False

        self.untouched_color = (39, 73, 114, 255)
        self.touched_color = (66, 150, 250, 255)
        self.hit_color = (15, 135, 250, 255)
        # from ImGui

        self.text = text
        self.text_label = Label(font_name=font, font_size=font_size,
                                batch=self.front_batch, group=self.front_group,
                                x=self._x, y=self._y, text=self.text)
        self.back_rec = Rectangle(x=self._x, y=self._y, width=self._width, height=self._height,
                                  color=self.untouched_color,  # ImGui color
                                  batch=self.back_ground_batch, group=self.back_ground_group)

    @property
    def value(self):
        return self.text

    def __contains__(self, item):
        return item in self.back_rec

    def on_mouse_motion(self, x, y, dx, dy):
        if (x, y) in self.back_rec:
            self.back_rec.color = self.touched_color
        else:
            self.pressed = False
            self.back_rec.color = self.untouched_color

    def on_mouse_press(self, x, y, buttons, modifiers) -> bool:
        if (x, y) in self and buttons == mouse.LEFT:
            self.back_rec.color = self.hit_color
            self.dispatch_event('on_press', x, y)
            self.pressed = True
            return True
        return False

    def on_mouse_release(self, x, y, buttons, modifiers):
        if self.pressed and (x, y) in self:
            self.back_rec.color = self.touched_color
            self.pressed = False

    def _update_position(self):
        self.text_label.position = self._x, self._y
        self.back_rec.position = self._x, self._y
        self.back_rec.width = self._width
        self.back_rec.height = self._height
        ...


PressTextButton.register_event_type('on_press')
