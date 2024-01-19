#  -------------------------------
#  Difficult Rocket
#  Copyright © 2020-2023 by shenjackyuanjie 3695888@qq.com
#  All rights reserved
#  -------------------------------

from typing import Optional, Tuple

# from libs import pyglet
import pyglet
from pyglet.text import Label
from pyglet.gui import widgets
from pyglet.window import mouse

# from pyglet.sprite import Sprite
from pyglet.shapes import Rectangle

# from pyglet.image import AbstractImage
from pyglet.graphics import Batch, Group

from Difficult_Rocket.api.types import Options, FontData

# from Difficult_Rocket import DR_status


RGBA = Tuple[int, int, int, int]


class BaseButtonTheme:
    """
    按钮的风格
    """
    name = "BaseButtonTheme"

    def __init__(self, x: int, y: int,
                 width: int, height: int,
                 batch: Batch, group: Group):
        self.batch = batch
        self.group = group
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def on_touch(self, x, y) -> None:
        """
        当鼠标在按钮上的时候
        :param x: 鼠标绝对位置
        :param y: 鼠标绝对位置
        :return:
        """

    def on_move_away(self) -> None:
        """
        当鼠标移出按钮的时候
        :return:
        """

    def on_hit(self, x: int, y: int) -> None:
        """
        当鼠标点击按钮的时候
        :param x: 鼠标绝对位置
        :param y: 鼠标绝对位置
        :return:
        """

    def on_release(self) -> None:
        """
        当鼠标松开按钮的时候
        :return:
        """


class MinecraftWikiButtonTheme(BaseButtonTheme):
    """
    直接绘制按钮的风格
    """

    name = "MinecraftWikiButtonTheme"

    def __init__(self, x: int, y: int,
                 width: int, height: int,
                 batch: Batch, group: Group):
        super().__init__(x, y, width, height, batch, group)
        self.batch = batch
        self.group = group
        a = (72, 73, 74, 255)
        b = (109, 109, 110, 255)
        c = (88, 91, 92, 255)
        d = (124, 124, 125, 255)  # 左下和右上两个重叠点的颜色.... 画吗？
        e = (49, 50, 51, 255)
        touch_a = (49, 50, 51, 255)
        touch_b = (90, 91, 92, 255)
        touch_c = (71, 72, 72, 255)
        touch_d = (106, 107, 108, 255)  # 同上
        pad = 2  # 边框宽度 2 px
        list_pad = 4  # 下巴 4px
        # 主背景
        self.back_ground = Rectangle(x=x, y=y,
                                     width=width, height=height,
                                     color=a, batch=batch, group=Group(order=0, parent=group))
        # 左上方向的覆盖
        self.cover_back = Rectangle(x=x, y=y + pad + list_pad,
                                    width=width - pad, height=height - pad - list_pad,
                                    color=b, batch=batch, group=Group(order=1, parent=group))
        # 右下方向的覆盖
        self.cover_back2 = Rectangle(x=x + pad, y=y + pad + list_pad,
                                     width=width - (pad * 2), height=height - (pad * 2) - list_pad,
                                     color=c, batch=batch, group=Group(order=2, parent=group))
        # 下巴的框
        self.list_back = Rectangle(x=x, y=y,
                                   width=width, height=list_pad,
                                   color=e, batch=batch, group=Group(order=1, parent=group))
        self.a = a
        self.b = b
        self.c = c
        self.d = d
        self.e = e
        self.touch_a = touch_a
        self.touch_b = touch_b
        self.touch_c = touch_c
        self.touch_d = touch_d
        self.pad = pad
        self.list_pad = list_pad

    def on_touch(self, x, y) -> None:
        """
        当鼠标在按钮上的时候
        :param x: 鼠标绝对位置
        :param y: 鼠标绝对位置
        :return:
        """

    def on_move_away(self) -> None:
        """
        当鼠标移出按钮的时候
        :return:
        """

    def on_hit(self, x: int, y: int) -> None:
        """
        当鼠标点击按钮的时候
        :param x: 鼠标绝对位置
        :param y: 鼠标绝对位置
        :return:
        """
        self.back_ground.color = self.touch_a
        self.cover_back.color = self.touch_b
        self.cover_back2.color = self.touch_c

    def on_release(self) -> None:
        """
        当鼠标松开按钮的时候
        :return:
        """
        self.back_ground.color = self.a
        self.cover_back.color = self.b
        self.cover_back2.color = self.c


class ButtonThemeOptions(Options):
    """基于 Options 写的 ButtonTheme"""

    name = "ButtonTheme"
    untouched_color: RGBA = (39, 73, 114, 255)
    touched_color: RGBA = (66, 150, 250, 255)
    hit_color: RGBA = (15, 135, 250, 255)
    font_theme: FontData = FontData()

    def __str__(self):
        return self.as_markdown()


class PressTextButton(widgets.WidgetBase):
    """
    自带 字符 + 材质 的按钮，就不用单独做材质了
    """

    def __init__(
            self,
            x: int,
            y: int,
            width: int,
            height: int,
            text: str,
            batch: Optional[Batch] = None,
            group: Optional[Group] = None,
            theme: Optional[ButtonThemeOptions] = None,
            draw_theme: Optional[type(BaseButtonTheme)] = None,
    ):
        super().__init__(x, y, width, height)
        self.main_batch = batch or Batch()
        self.user_batch = batch is not None
        self.front_group = Group(order=10, parent=group)
        self.back_ground_group = Group(order=5, parent=group)
        self.pressed = False

        self.theme = theme or ButtonThemeOptions()

        self.untouched_color = self.theme.untouched_color
        self.touched_color = self.theme.touched_color
        self.hit_color = self.theme.hit_color
        # from ImGui

        self.text = text
        self.text_label = Label(
            font_name=self.theme.font_theme.font_name,
            font_size=self.theme.font_theme.font_size,
            batch=self.main_batch,
            group=self.front_group,
            x=self._x,
            y=self._y + 4,
            width=self._width,
            height=self._height,
        )
        self.font = pyglet.font.load(
            self.theme.font_theme.font_name,
            self.theme.font_theme.font_size,
            bold=self.theme.font_theme.bold,
            italic=self.theme.font_theme.italic,
            stretch=self.theme.font_theme.stretch,
        )
        self.font_height = self.font.ascent - self.font.descent
        if draw_theme is None:
            self.back_rec = Rectangle(
                x=self._x,
                y=self._y,
                width=self._width,
                height=self._height,
                color=self.untouched_color,  # ImGui color
                batch=self.main_batch,
                group=self.back_ground_group,
            )
            self.draw_theme = False
        else:
            self.draw_theme = draw_theme(
                x=self._x,
                y=self._y,
                width=self._width,
                height=self._height,
                batch=self.main_batch,
                group=self.back_ground_group,
            )

        self.value = text  # 重新分配一下高度和宽度的位置

    @property
    def value(self):
        return self.text

    @value.setter
    def value(self, value):
        self.text = value
        self.text_label.text = value
        text_width = self.text_label.content_width
        self.text_label.x = self._x + (self.width - text_width) // 2
        self.text_label.y = (
                self._y + (self.height - self.font_height) // 2 + (self.font_height * 0.2) + 4
        )  # 修正一下位置

    @property
    def batch(self) -> Batch:
        return self.main_batch

    @batch.setter
    def batch(self, value: Batch):
        assert isinstance(value, Batch), "batch must be a pyglet.graphics.Batch"
        self.main_batch = value
        self.text_label.batch = value
        self.back_rec.batch = value
        self.user_batch = True

    def __contains__(self, point):
        if self.draw_theme:
            x, y = self.x, self.y
            return x < point[0] < x + self._width and y < point[1] < y + self._height
        return point in self.back_rec

    def on_draw(self):
        if not self.user_batch:
            self.main_batch.draw()

    def on_mouse_motion(self, x, y, dx, dy):
        if (x, y) in self:
            if self.draw_theme:
                ...
            else:
                self.back_rec.color = self.touched_color
        else:
            self.pressed = False
            if self.draw_theme:
                self.draw_theme.on_move_away()
                self.draw_theme.on_release()
            else:
                self.back_rec.color = self.untouched_color

    def on_mouse_press(self, x, y, buttons, modifiers) -> bool:
        if (x, y) in self:
            if buttons == mouse.LEFT:
                if self.draw_theme:
                    self.draw_theme.on_hit(x, y)
                else:
                    self.back_rec.color = self.hit_color
                self.dispatch_event("on_press", x, y)
                self.pressed = True
                return True
        else:
            self.pressed = False
            if self.draw_theme:
                self.draw_theme.on_release()
            else:
                self.back_rec.color = self.untouched_color
            self.dispatch_event("on_release", x, y)
        return False

    def on_mouse_release(self, x, y, buttons, modifiers):
        if self.pressed and (x, y) in self:
            if self.draw_theme:
                self.draw_theme.on_release()
            else:
                self.back_rec.color = self.touched_color
            self.pressed = False

    def _update_position(self):
        self.text_label.position = self._x, self._y, 0
        self.back_rec.position = self._x, self._y
        self.back_rec.width = self._width
        self.back_rec.height = self._height


PressTextButton.register_event_type("on_press")
PressTextButton.register_event_type("on_release")
