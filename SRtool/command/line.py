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

import re
import time
import logging

from typing import Union
from decimal import Decimal

# from DR
from SRtool import translate
from SRtool.api import new_thread

# from libs.pyglet
from libs import pyglet
from libs.pyglet import font
from libs.pyglet.text import Label
from libs.pyglet.window import key
from libs.pyglet.gui import widgets
from libs.pyglet.graphics import Batch, Group

logger = logging.getLogger('command_line')


class CommandText:
    """
    CommandLine返回的字符，可以用来搜索
    """
    def __init__(self, text: str):
        self.text = text

    def find(self, text: str) -> bool:
        finding = re.match(text, self.text)
        if finding:
            return True
        else:
            return False

    def match(self, text: str) -> bool:
        finding = re.match(text, self.text)
        print(self.text + '|' + text)
        if finding:  # 如果找到了
            try:
                next_find = self.text[finding.span()[1]]
                # 这里try因为可能匹配到的是字符串末尾
            except IndexError:
                next_find = ' '
                # 直接过滤掉
            print(self.text + '|' + text + '|' + next_find)
            if next_find == ' ':
                self.text = self.text[finding.span()[1] + 1:]
                print(self.text + text + next_find)
                return True
            # 将匹配到的字符串，和最后一个匹配字符后面的字符删除(相当暴力的操作)
            return False
        else:
            return False

    def greedy(self, ):
        pass

    def __str__(self):
        return str(self.text)

    def __int__(self):
        return int(self.text)



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
        self._command_list = ['' for line in range(length)]
        self._command_text = command_text
        self._text_position = 0
        self._command_view = 0
        self._value = 0
        self._text = ''
        self.command_split = 25
        self.command_distance = 20

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
        self._label = [Label(x=x + 10, y=y + self.command_distance + (line * self.command_split), batch=batch, text='a',
                             anchor_x='left', anchor_y='bottom',
                             font_size=font_size - 3, font_name=translate.鸿蒙简体,
                             group=bg_group)
                       for line in range(length)]
        # Rectangular outline with 5-pixel pad:
        color = (100, 100, 100, 100)
        self._pad = p = 5
        self._outline = pyglet.shapes.Rectangle(x=x - p, y=y - p,
                                                width=width + p, height=height + p,
                                                color=color[:3],
                                                batch=batch, group=fg_group)
        self._outline.opacity = color[3]

        self.editing = False

    def _update_position(self):
        pass

    def update_groups(self, order):
        self._line.group = Group(order=order + 1, parent=self._user_group)
        for label in self._label:
            label.group = Group(order=order + 1, parent=self._user_group)
        self._outline.group = Group(order=order + 2, parent=self._user_group)

    """
    values
    """

    @property
    def value(self):
        return self.text

    @property
    def text(self):
        return self._text

    @text.setter
    def text(self, value):
        assert type(value) is str, 'CommandLine\'s text must be string!'
        self._text = value
        self._line.text = value

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
        assert -self.length < value < self.length, f'Command View must be bigger than {-self.length} and smaller than {self.length}'
        if value == -1:  # flush command list
            self._label.insert(0, self._label[-1])
            self._label.pop(-1)
            for line in range(self.length):
                self._label[line].y = self.y + self.command_distance + (line * self.command_split)
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
        # self._command_view = value

    @property
    def editing(self):
        return self._editing

    @editing.setter
    def editing(self, value):
        assert type(value) is bool, 'Command editing must be bool!'
        self._editing = value
        self._line.visible = value
        self._outline.visible = value
        for label in self._label:
            label.visible = value

    @new_thread('command wait', daemon=True, log_thread=False)
    def wait(self, wait: Union[float, int] = 0):
        this = self._label[0]
        self._label[0].visible = True
        time.sleep(wait)
        if self._label[0].visible and not self.editing:
            while (self._label[0].opacity >= 30) and self._label[0].visible and (self._label[0] is this) and not self.editing:
                # (label 的透明度不是 0) and (label 还在显示) and (label 还是载入线程时候的那个label) and (现在不在输入新行)
                self._label[0].opacity -= 2
                time.sleep(0.01)
            if self._label[0] is this:  # 如果结束的时候label还是这个label
                self._label[0].opacity = 255
            else:  # 如果不是就赶快找回来！
                now = self._label.index(this)
                self._label[now].opacity = 255
            if not self.editing:  # 如果不在编辑再隐藏
                self._label[0].visible = False

    @property
    def command_list(self):
        return self._command_list

    """
    events
    """

    def on_text(self, text):
        if self.editing:
            if text in ('\r', '\n'):  # goto a new line
                if not self.text:
                    pass
                elif self.text[0] == self._command_text:
                    self.dispatch_event('on_command', CommandText(self.text[1:]))
                else:
                    self.dispatch_event('on_message', self.text)
                # on_message 和 on_command 可能会覆盖 self.text 需要再次判定
                if self.text:
                    self.command_view = -1
                self.editing = False
                self.wait()
            else:
                self.text = f'{self.text[:self._text_position]}{text}{self.text[self._text_position:]}'  # 插入字符（简单粗暴）
                self._text_position += 1
        elif text == 't':  # open message line
            self.editing = True
        elif text == '/':  # open command line
            self.editing = True
            self.text = '/'
            self._text_position = 1

    def on_text_motion(self, motion):
        if self.editing:
            # edit motion
            if motion == key.MOTION_DELETE:  # 确保不越界
                self.text = f'{self.text[:self._text_position]}{self.text[self._text_position + 1:]}'  # 简单粗暴的删除
            elif motion == key.MOTION_BACKSPACE and self._text_position >= 1:  # 确保不越界
                self.text = f'{self.text[:self._text_position - 1]}{self.text[self._text_position:]}'  # 简单粗暴的删除
                self._text_position -= 1  # 记得切换光标位置

            # move motion
            elif motion == key.MOTION_LEFT and self._text_position >= 0:  # 确保不越界
                self._text_position -= 1
            elif motion == key.MOTION_RIGHT and self._text_position <= len(self.text):  # 确保不越界
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
            pass

    def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
        if self.editing:
            pass

    def on_mouse_press(self, x, y, buttons, modifiers):
        if self.editing:
            pass

    """
    custom event
    """

    def on_command(self, command: text):
        if self.editing:
            return
        """give command to it"""

    def on_message(self, message: text):
        if self.editing:
            return
        """give message to it"""

    def push_line(self, line: Union[str, int, float, Decimal], block_line: bool = False):
        _text = self.text
        self.text = str(line)
        self.command_view = -1
        if not block_line:
            self.text = _text


CommandLine.register_event_type('on_command')
CommandLine.register_event_type('on_message')
