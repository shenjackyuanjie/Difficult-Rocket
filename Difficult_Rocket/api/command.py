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

from Difficult_Rocket.api import translate

# from libs.pyglet
from libs import pyglet
from libs.pyglet.text import Label
from libs.pyglet.window import key
from libs.pyglet.gui import widgets
from libs.pyglet.graphics import Batch, Group
from libs.pyglet.text.caret import Caret
from libs.pyglet.text.layout import IncrementalTextLayout


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
                 font_size: int = 20):
        super().__init__(x, y, width, height)
        # normal values
        self.length = length
        self._editing = False
        self.command_list = ['' for line in range(length)]
        bg_group = Group(order=0, parent=group)
        fg_group = Group(order=1, parent=group)
        # hidden value
        self._text = ''
        self._doc = pyglet.text.document.UnformattedDocument('')
        self._doc.set_style(0, len(self._doc.text), dict(color=(0, 0, 0, 255)))
        self._line = Label(x=x, y=y, batch=batch, text=self.text,
                           color=(100, 255, 255, 200),
                           anchor_x='left', anchor_y='center',
                           font_size=font_size, group=fg_group)
        self._label = [Label(x=x, y=y + 20 + (line * 20), batch=batch, text='a',
                             anchor_x='left', anchor_y='center',
                             font_size=12, group=bg_group)
                       for line in range(length)]
        # Rectangular outline with 2-pixel pad:
        color = (255, 255, 255, 255)
        self._pad = p = 2
        self._outline = pyglet.shapes.Rectangle(x-p, y-p, width+p+p, height+p+p, color[:3], batch, fg_group)
        self._outline.opacity = color[3]
        self._text_position = 0
        self._command_view = 0
        self._value = 0

    def _update_position(self):
        self._line.position = self._x, self._y

    @property
    def text(self):
        return self._text

    @text.setter
    def text(self, value):
        assert type(value) is str, 'CommandLine\'s text must be string!'
        self._text = value
        self._line.text = value
        self._doc.text = value

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

    def on_text(self, text):
        if self.editing:
            if text in ('\r', '\n'):  # goto a new line
                self.command_view = -1
                self._editing = False
            else:
                self.text = f'{self.text[:self._text_position]}{text}{self.text[self._text_position:]}'
                # 插入字符（简单粗暴）
                self._text_position += 1
                # 光标位置+1
        elif text == 't':  # open command line
            self._editing = not self.editing

    def on_text_motion(self, motion):
        if self.editing:
            motion_string = key.motion_string(motion)
            if motion == key.MOTION_DOWN:
                # 刷新整个命令列表，向上刷新一遍
                self.command_list[-1].text = self.command_list[0].text  # 把最上面一个显示替换成最新的
                last = self.command_list[-1]  # 获取一遍现有的最后一个
                self.command_list.pop(-1)  # 删除最后一个
                self.command_list.insert(1, last)  # 把之前的最后一个插进第2个的位置（整体往后挪一个）
                for line in range(1, len(self.command_list)):
                    self.command_list[line].y = 50 + (20 * line)  # 挨个重设 y
                self.command_list.text = ''  # 清除第一个的数据

    def on_text_motion_select(self, motion):
        pass
