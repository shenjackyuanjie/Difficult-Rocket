#  -------------------------------
#  Difficult Rocket
#  Copyright © 2021-2022 by shenjackyuanjie 3695888@qq.com
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
from pyglet import font
from pyglet.text import Label, HTMLLabel
# from pyglet.window import key
from pyglet.gui import widgets
# from pyglet.sprite import Sprite
from pyglet.shapes import Rectangle
# from pyglet.image import AbstractImage
from pyglet.graphics import Batch, Group
from pyglet.text.document import FormattedDocument
from pyglet.text.layout import IncrementalTextLayout

# from libs import pyperclip
# from libs.pyperclip import paste

from Difficult_Rocket.utils import translate
from Difficult_Rocket.client.guis.format import html
from Difficult_Rocket import DR_option

__all__ = ['InputBox']


# class Parts(widgets.WidgetBase):
#     """
#     parts
#     """
#
#     def __init__(self,
#                  x: int,
#                  y: int,
#                  width: int,
#                  height: int,
#                  textures: AbstractImage,
#                  # textures,
#                  batch: Batch,
#                  parts_data: dict):
#         super().__init__(x, y, width, height)
#         self.sprite = Sprite(img=textures, x=x, y=y, batch=batch)
#         self._value = 0


class TextButton(widgets.WidgetBase):
    """
    自带字符的按钮，就不用单独做材质了
    """

    def __init__(self,
                 x: int, y: int, width: int, height: int,
                 text: str,
                 font: str = translate.鸿蒙简体, font_size: int = 13):
        super().__init__(x, y, width, height)
        self.text = text
        self.text_label = Label(
                                font_name=font, font_size=font_size)

    @property
    def value(self):
        return self.text

    def _update_position(self):
        self.text_label.position = self._x, self._y
        ...


if not DR_option.InputBox_use_TextEntry:
    class InputBox(widgets.WidgetBase):
        """ 自定义的输入框 """
        
        def __init__(self, x: int, y: int, width: int,
                     message: str,
                     batch: Optional[Batch], group: Optional[Group]):

            super().__init__(x=x, y=y, width=width)
            ...
    # class InputBox(widgets.WidgetBase):
    #     """
    #     input box
    #     """
    # 
    #     def __init__(self,
    #                  x: int, y: int, width: int, height: int,
    #                  message: str = '',
    #                  font_name: str = translate.微软等宽,
    #                  font_size: int = 15,
    #                  font_bold: bool = False,
    #                  font_italic: bool = False,
    #                  font_stretch: bool = False,
    #                  font_dpi: int = 100,
    #                  text_color: [int, int, int] = (187, 187, 187, 255),
    #                  out_line_color: [int, int, int] = (37, 116, 176),
    #                  cursor_color: [int, int, int] = (187, 187, 187),
    #                  select_color: [int, int, int] = (63, 115, 255),
    #                  out_line: int = 2,
    #                  batch: Batch = None,
    #                  group: Group = None):
    #         if batch is None:
    #             batch = Batch()
    #         if group is None:
    #             group = Group()
    #         super().__init__(x, y, width, height)
    #         self.enabled = False
    #         self._text = message
    #         self._cursor_poi = 0
    #         self.font = font.load(name=font_name, size=font_size,
    #                               bold=font_bold, italic=font_italic, stretch=font_stretch,
    #                               dpi=font_dpi)
    #         self.font_height = self.font.ascent - self.font.descent
    #         self.out_bound = out_line
    #         if DR_option.InputBox_use_TextEntry:
    #             # 基于IncrementalTextLayout的处理系统
    #             self._doc = FormattedDocument(message)
    #             # self._doc.set_style()
    #             self._layout = IncrementalTextLayout(self._doc, self.font, width, height,
    #                                                  batch=batch, group=group)
    #             self._input_box = widgets.TextEntry(x, y, width, height,
    #                                                 self._doc, self._layout,
    #                                                 batch=batch, group=group)
    #         else:
    #             # 基于Label的处理系统
    #             self._input_box = Label(x=x + out_line, y=y + out_line,
    #                                     width=width, height=self.font_height + self.out_bound * 2,
    #                                     color=text_color,
    #                                     font_name=font_name, font_size=font_size,
    #                                     batch=batch, group=group,
    #                                     text=message)
    #             self._HTML_box = HTMLLabel(x=x + out_line, y=y + out_line + 30,
    #                                        width=width, height=self.font_height + self.out_bound * 2,
    #                                        batch=batch, group=group,
    #                                        text=message)
    #             self._out_box = Rectangle(x=x - out_line, y=y - out_line,
    #                                       color=out_line_color,
    #                                       width=width + (out_line * 2), height=height + (out_line * 2),
    #                                       batch=batch, group=group)
    #             self._光标 = Rectangle(x=x + out_line, y=y + out_line,
    #                                    color=cursor_color,
    #                                    width=1, height=self.font_height,
    #                                    batch=batch, group=group)
    #             self._选择框 = Rectangle(x=x, y=y, width=0, height=self.font_height,
    #                                      color=select_color)
    #             self._选择的字 = Label(x=x, y=y, width=0, height=self.font_height,
    #                                    color=text_color,
    #                                    font_name=font_name, font_size=font_size,
    #                                    batch=batch, group=group,
    #                                    text='')
    # 
    #     """
    #     输入框的属性
    #     """
    # 
    #     # 本身属性
    #     @property
    #     def text(self) -> str:  # 输入框的文本
    #         return self._text
    # 
    #     @text.setter
    #     def text(self, value) -> None:
    #         assert type(value) is str, 'Input Box\'s text must be string!'
    #         self._text = value
    #         self._input_box.text = value
    #         self._HTML_box.text = html.decode_text2HTML(value, show_style=True)
    # 
    #     @property
    #     def cursor_poi(self) -> int:  # 光标位置
    #         return self._cursor_poi
    # 
    #     @cursor_poi.setter
    #     def cursor_poi(self, value) -> None:
    #         assert type(value) is int, 'Input Box\'s cursor poi must be int!'
    #         self._cursor_poi = value
    #         self._光标.x = self.x + self.out_bound + self._input_box.content_width
    # 
    #     # 渲染时属性
    #     @property
    #     def opacity(self) -> int:  # 透明度
    #         return self._input_box.opacity
    # 
    #     @opacity.setter
    #     def opacity(self, value: int) -> None:
    #         assert type(value) is int, 'Input Box\'s opacity must be int!'
    #         self._input_box.opacity = value
    #         self._out_box.opacity = value
    #         self._选择的字.opacity = value
    #         self._选择框.opacity = value
    #         self._光标.opacity = value
    # 
    #     @property
    #     def visible(self) -> bool:  # 是否可见
    #         return self._input_box.visible
    # 
    #     @visible.setter
    #     def visible(self, value: bool) -> None:
    #         assert type(value) is bool, 'Input Box\'s visible must be bool!'
    #         self._input_box.visible = value
    #         self._out_box.visible = value
    #         self._选择的字.visible = value
    #         self._选择框.visible = value
    #         self._光标.visible = value
    # 
    #     @property
    #     def value(self) -> str:
    #         return self._text
    # 
    #     """
    #     事件调用
    #     """
    # 
    #     def _update_position(self):
    #         self._input_box.position = self._x + self.out_bound, self._y + self.out_bound
    #         self._out_box.position = self._x - self.out_bound, self._y - self.out_bound
    #         self._光标.position = self._x + self.out_bound, self._y + self.out_bound
    # 
    #     # 输入东西
    #     def on_text(self, text: str):
    #         if self.enabled:
    #             if text in ('\r', '\n'):
    #                 if self.text:
    #                     self.dispatch_event('on_commit', self.text)
    #             else:
    #                 self.text = f'{self.text[:self.cursor_poi]}{text}{self.text[self.cursor_poi:]}'
    #                 self.cursor_poi += len(text)
    # 
    #     # 移动光标
    #     def on_text_motion(self, motion):
    #         if self.enabled:
    #             # 根据按键处理
    #             # 单格移动光标(上下左右)
    #             if motion in (key.MOTION_UP, key.MOTION_LEFT):  # 往上一个移动
    #                 self.cursor_poi = max(0, self._cursor_poi - 1)
    #             elif motion in (key.MOTION_DOWN, key.MOTION_RIGHT):  # 往下一个移动
    #                 self.cursor_poi = min(len(self.text), self._cursor_poi + 1)
    #             # 大前后移动(开头或结尾)
    #             elif motion in (
    #                     key.MOTION_BEGINNING_OF_LINE, key.MOTION_BEGINNING_OF_FILE, key.MOTION_PREVIOUS_PAGE):  # 开头
    #                 self.cursor_poi = 0
    #             elif motion in (key.MOTION_END_OF_LINE, key.MOTION_END_OF_FILE, key.MOTION_NEXT_PAGE):  # 结尾
    #                 self.cursor_poi = len(self.text)
    #             # 删除操作
    #             elif motion == key.MOTION_BACKSPACE:
    #                 if self.text:  # 如果有文字
    #                     self.text = f'{self.text[:self.cursor_poi - 1]}{self.text[self.cursor_poi:]}'
    #                 self.cursor_poi = max(0, self._cursor_poi - 1)
    #             elif motion == key.MOTION_DELETE:
    #                 if self.text and self.cursor_poi != len(self.text) - 1:  # 如果有文字，并且光标不在最后
    #                     self.text = f'{self.text[:self.cursor_poi]}{self.text[self.cursor_poi + 1:]}'
    #             # 剪贴板操作
    #             elif motion == key.MOTION_COPY:
    #                 pass
    #             elif motion == key.MOTION_PASTE:
    #                 paste_text = paste()
    #                 self.text = f'{self.text[:self.cursor_poi]}{paste_text}{self.text[self.cursor_poi:]}'
    #                 self.cursor_poi += len(paste_text)
    # 
    #     def on_text_motion_select(self, motion):
    #         pass
    # 
    #     def on_mouse_press(self, x, y, buttons, modifiers):
    #         if self._check_hit(x, y) and self._input_box.visible:
    #             self.enabled = True
    #         else:
    #             self.enabled = False
    # 
    #     def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
    #         pass
    # 
    #     def on_mouse_release(self, x, y, buttons, modifiers):
    #         pass
    # 
    #     def on_commit(self, text: str):
    #         pass


    InputBox.register_event_type('on_commit')
else:
    InputBox = widgets.TextEntry
    # class InputBox(widgets.TextEntry):
    #     pass
