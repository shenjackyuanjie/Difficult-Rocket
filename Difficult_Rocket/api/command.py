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

import time

# from DR
from Difficult_Rocket.api import translate
from Difficult_Rocket.api.new_thread import new_thread

# from libs.pyglet
from libs import pyglet
from libs.pyglet.text import Label
from libs.pyglet.window import key
from libs.pyglet.gui import widgets
from libs.pyglet.text.caret import Caret
from libs.pyglet.graphics import Batch, Group
from libs.pyglet.text.layout import IncrementalTextLayout
from libs.pyglet.text.document import UnformattedDocument


class CommandLine(widgets.WidgetBase):
    """
    command line show
    """

    def __init__(self,
                 x: int,
                 y: int,
                 width: int,
                 height: int,
                 length: int,
                 batch: Batch,
                 group: Group = None,
                 command_text: str = '/',
                 font_size: int = 20):
        super().__init__(x, y, width, height)

        # normal values
        self.length = length
        self.command_list = ['' for line in range(length)]
        self.command_text = command_text
        self._text_position = 0
        self._command_view = 0
        self._value = 0

        # group
        self._user_group = group
        bg_group = Group(order=0, parent=group)
        fg_group = Group(order=1, parent=group)

        # hidden value
        self._text = ''
        self._line = Label(x=x, y=y, batch=batch, text=self.text,
                           color=(100, 255, 255, 255),
                           anchor_x='left', anchor_y='bottom',
                           font_size=font_size, font_name=translate.鸿蒙简体,
                           group=fg_group)
        self._label = [Label(x=x + 10, y=y + 20 + (line * 20), batch=batch, text='a',
                             anchor_x='left', anchor_y='bottom',
                             font_size=font_size - 3, font_name=translate.鸿蒙简体,
                             group=bg_group)
                       for line in range(length)]
        # Rectangular outline with 5-pixel pad:
        color = (100, 100, 100, 100)
        self._pad = p = 5
        self._outline = pyglet.shapes.Rectangle(x=x - p, y=y - p,
                                                width=width + p + p, height=height + p + p,
                                                color=color[:3],
                                                batch=batch, group=fg_group)
        self._outline.opacity = color[3]

        self.document = UnformattedDocument(text=self.text)
        self.document.set_style(0, len(self.document.text), dict(color=(200, 132, 123, 255),
                                                                 font_size=font_size, font_name=translate.鸿蒙简体))
        font = self.document.get_font()
        height = font.ascent - font.descent

        self.layout = IncrementalTextLayout(document=self.document,
                                            width=width, height=height,
                                            batch=batch)
        self.layout.position = x, y
        self.caret = Caret(self.layout, color=(200, 132, 123), batch=batch)
        self.editing = False

    def _update_position(self):
        self._line.position = self._x, self._y

    def update_groups(self, order):
        self._line.group = Group(order=order + 1, parent=self._user_group)
        for label in self._label:
            label.group = Group(order=order + 1, parent=self._user_group)
        self._outline.group = Group(order=order + 2, parent=self._user_group)

    @property
    def text(self):
        return self._text

    @text.setter
    def text(self, value):
        assert type(value) is str, 'CommandLine\'s text must be string!'
        self._text = value
        self._line.text = value
        self.document.text = value

    @property
    def command_view(self):
        return self._command_view

    @command_view.setter
    def command_view(self, value):
        """
        value:
        -1 -> 将整个列表添加一个数据
              如果长度超过length就删掉多余的
              将视角移动到最下面，刷新显示列表
        0 ~ (self.length-1) -> 切换视角到对应的行数
                               实际上还有一个限制
        """
        assert type(value) is int, 'Command View must be integer'
        assert -2 < value < self.length, f'Command View must be bigger than -1 and smaller than {self.length}'
        if value == -1:  # flush command list
            self._label.insert(0, self._label[-1])
            self._label.pop(-1)
            for line in range(self.length):
                self._label[line].y = self.y + 20 + (line * 20)
            self._label[0].text = self.text
            self.text = ''
            self._command_view = 0
            self._text_position = 0
        elif value == self._command_view:  # not doing anything
            pass
        elif value > self._command_view:  # move upwards
            pass
        else:  # move downwards
            pass
        self._command_view = value

    @property
    def editing(self):
        return self._editing

    @editing.setter
    def editing(self, value):
        assert type(value) is bool, 'Command editing must be bool!'
        self._editing = value
        self._line.visible = value
        self._outline.visible = value
        self.caret.visible = value
        for label in self._label:
            label.visible = value

    @new_thread('command wait')
    def wait(self, wait):
        self._label[0].visible = True
        time.sleep(wait)
        if self._label[0].visible and not self.editing:
            self._label[0].visible = False

    def on_text(self, text):
        if self.editing:
            self.caret.on_text(text)
            if text in ('\r', '\n'):  # goto a new line
                if self.text[0] == self.command_text:
                    self.dispatch_event('on_command', self.text[1:])
                else:
                    self.dispatch_event('on_message', self.text)
                self.command_view = -1
                self.editing = False
                self.wait(1)
            else:
                self.text = f'{self.text[:self._text_position]}{text}{self.text[self._text_position:]}'  # 插入字符（简单粗暴）
                self._text_position += 1
        elif text == 't':  # open message line
            self.editing = True
        elif text == '/':  # open command line
            self.editing = True
            self.text = '/'
            self._text_position = 1
            self.caret.on_text_motion(key.MOTION_RIGHT)

    def on_text_motion(self, motion):
        if self.editing:
            self.caret.on_text_motion(motion)
            # edit motion
            if motion == key.MOTION_DELETE:
                self.text = f'{self.text[:self._text_position]}{self.text[self._text_position + 1:]}'
            elif motion == key.MOTION_BACKSPACE:
                self.text = f'{self.text[:self._text_position - 1]}{self.text[self._text_position:]}'
                self._text_position -= 1

            # move motion
            elif motion == key.MOTION_LEFT:
                self._text_position -= 1
            elif motion == key.MOTION_RIGHT:
                self._text_position += 1
            elif motion in (key.MOTION_BEGINNING_OF_LINE, key.MOTION_BEGINNING_OF_FILE, key.MOTION_PREVIOUS_PAGE):
                self._text_position = 0
            elif motion in (key.MOTION_END_OF_LINE, key.MOTION_END_OF_FILE, key.MOTION_NEXT_PAGE):
                self._text_position = len(self.text)

            # view move motion
            elif motion == key.MOTION_DOWN:
                if not self.command_view == -1:
                    self.command_view -= 1
                else:
                    pass

    def on_text_motion_select(self, motion):
        if self.editing:
            self.caret.on_text_motion_select(motion)

    def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
        if self.editing:
            self.caret.on_mouse_drag(x, y, dx, dy, buttons, modifiers)

    def on_mouse_press(self, x, y, buttons, modifiers):
        if self.editing:
            self.caret.on_mouse_press(x, y, buttons, modifiers)

    def on_command(self, command):
        if self.editing:
            return
        """give command to it"""

    def on_message(self, message):
        if self.editing:
            return
        """give message to it"""


CommandLine.register_event_type('on_command')
CommandLine.register_event_type('on_message')
