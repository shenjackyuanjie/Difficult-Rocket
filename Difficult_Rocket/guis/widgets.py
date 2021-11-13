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

from Difficult_Rocket import translate

from libs import pyglet
from libs.pyglet import font
from libs.pyglet.text import Label
from libs.pyglet.gui import widgets
from libs.pyglet.sprite import Sprite
from libs.pyglet.shapes import Rectangle
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
                 x: int, y: int, width: int, height: int,
                 message: str = '',
                 font_name: str = translate.鸿蒙简体,
                 font_size: int = 15,
                 blod: bool = False,
                 text_color: [int, int, int] = (0, 0, 0, 255),
                 out_line_color: [int, int, int] = (255, 255, 255),
                 cursor_color: [int, int, int] = (255, 255, 255),
                 out_line: int = 2,
                 batch: Batch = Batch(),
                 group: Group = Group()):
        super().__init__(x, y, width, height)
        self._text = message
        self.text = self._text
        self.字体 = font.load(name=font_name, size=font_size, blod=blod)
        self.字高 = self.字体.ascent - self.字体.descent
        self.外框距离 = out_line
        self._输入框 = Label(x=x + out_line, y=y + out_line,
                          width=width, height=height,
                          color=text_color,
                          font_name=font_name, font_size=font_size,
                          batch=batch, group=group,
                          text=message)
        self._外框 = Rectangle(x=x-out_line, y=y-out_line,
                             color=out_line_color,
                             width=width + (out_line * 2), height=height + (out_line * 2),
                             batch=batch, group=group)
        self._光标 = Rectangle(x=x+out_line, y=y+out_line,
                             color=cursor_color,
                             width=1, height=self.字高,
                             batch=batch, group=group)

    """
    输入框的属性
    """

    @property
    def text(self):
        return self._text

    @text.setter
    def text(self, value):
        assert type(value) is str, 'Input Box\'s text must be string!'
        self._text = value
        self._输入框.text = value

    @property
    def opacity(self):
        return self._输入框.opacity

    @opacity.setter
    def opacity(self, value: int):
        assert type(value) is int, 'Input Box\'s opacity must be int!'
        self._输入框.opacity = value
        self._外框.opacity = value
        self._光标.opacity = value

    """
    事件调用
    """

    def _update_position(self):
        self._输入框.position = self._x + self.外框距离, self._y + self.外框距离
        self._外框.position = self._x - self.外框距离, self._y - self.外框距离
        self._光标.position = self._x + self.外框距离, self._y + self.外框距离

    def on_text(self, text):
        pass

    def on_text_motion(self, motion):
        pass

    def on_text_motion_select(self, motion):
        pass

    def on_mouse_press(self, x, y, buttons, modifiers):
        pass

    def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
        pass

    def on_mouse_release(self, x, y, buttons, modifiers):
        pass

    def on_commit(self, text: str):
        pass
