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

# from libs import pyglet
from libs.pyglet import font
from libs.pyglet.text import Label
from libs.pyglet.window import key
from libs.pyglet.gui import widgets
from libs.pyglet.sprite import Sprite
from libs.pyglet.shapes import Rectangle
from libs.pyglet.image import AbstractImage
from libs.pyglet.graphics import Batch, Group
# from libs import pyperclip
from libs.pyperclip import paste, copy

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
                 font_bold: bool = False,
                 font_italic: bool = False,
                 font_stretch: bool = False,
                 font_dpi: int = 100,
                 text_color: [int, int, int] = (187, 187, 187, 255),
                 out_line_color: [int, int, int] = (37, 116, 176),
                 cursor_color: [int, int, int] = (187, 187, 187),
                 select_color: [int, int, int] = (63, 115, 255),
                 out_line: int = 2,
                 batch: Batch = Batch(),
                 group: Group = Group()):
        super().__init__(x, y, width, height)
        self._text = message
        self._text_position = 0
        self.font = font.load(name=font_name, size=font_size,
                              blod=font_bold, italic=font_italic, stretch=font_stretch,
                              dpi=font_dpi)
        self.font_height = self.font.ascent - self.font.descent
        self.out_bound = out_line
        self._input_box = Label(x=x + out_line, y=y + out_line,
                                width=width, height=height,
                                color=text_color,
                                font_name=font_name, font_size=font_size,
                                batch=batch, group=group,
                                text=message)
        self._out_box = Rectangle(x=x - out_line, y=y - out_line,
                                  color=out_line_color,
                                  width=width + (out_line * 2), height=height + (out_line * 2),
                                  batch=batch, group=group)
        self._光标 = Rectangle(x=x + out_line, y=y + out_line,
                             color=cursor_color,
                             width=1, height=self.font_height,
                             batch=batch, group=group)
        self._选择框 = Rectangle(x=x, y=y, width=0, height=self.font_height,
                              color=select_color)
        self._选择的字 = Label(x=x, y=y, width=0, height=self.font_height,
                           color=text_color,
                           font_name=font_name, font_size=font_size,
                           batch=batch, group=group,
                           text='')

    """
    输入框的属性
    """

    @property
    def text(self) -> str:
        return self._text

    @text.setter
    def text(self, value) -> None:
        assert type(value) is str, 'Input Box\'s text must be string!'
        self._text = value
        self._input_box.text = value

    @property
    def opacity(self) -> int:
        return self._input_box.opacity

    @opacity.setter
    def opacity(self, value: int) -> None:
        assert type(value) is int, 'Input Box\'s opacity must be int!'
        self._input_box.opacity = value
        self._out_box.opacity = value
        self._选择的字.opacity = value
        self._选择框.opacity = value
        self._光标.opacity = value

    @property
    def visible(self) -> bool:
        return self._input_box.visible

    @visible.setter
    def visible(self, value: bool) -> None:
        assert type(value) is bool, 'Input Box\'s visible must be bool!'
        self._input_box.visible = value
        self._out_box.visible = value
        self._选择的字.visible = value
        self._选择框.visible = value
        self._光标.visible = value


    @property
    def value(self) -> str:
        return self._text

    """
    事件调用
    """

    def _update_position(self):
        self._input_box.position = self._x + self.out_bound, self._y + self.out_bound
        self._out_box.position = self._x - self.out_bound, self._y - self.out_bound
        self._光标.position = self._x + self.out_bound, self._y + self.out_bound

    def on_text(self, text: str):
        if self.enabled:
            if text in ('\r', '\n'):
                if self.text:
                    self.dispatch_event('on_commit', self.text)
            else:
                self.text = f'{self.text[:self._text_position]}{text}{self.text[self._text_position:]}'

    def on_text_motion(self, motion):
        if self.enabled

    def on_text_motion_select(self, motion):
        pass

    def on_mouse_press(self, x, y, buttons, modifiers):
        if self._check_hit(x, y) and self._input_box.visible:
            self.enabled = True
        else:
            self.enabled = False

    def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
        pass

    def on_mouse_release(self, x, y, buttons, modifiers):
        pass

    def on_commit(self, text: str):
        pass
