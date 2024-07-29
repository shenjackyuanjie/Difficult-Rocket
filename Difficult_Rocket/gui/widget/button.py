#  -------------------------------
#  Difficult Rocket
#  Copyright © 2020-2023 by shenjackyuanjie 3695888@qq.com
#  All rights reserved
#  -------------------------------

from __future__ import annotations
import math
from typing import Optional, Tuple, Type, Sequence
from dataclasses import dataclass
from enum import Enum

# from libs import pyglet
import pyglet
from pyglet.gl import GL_ONE_MINUS_SRC_ALPHA, GL_SRC_ALPHA
from pyglet.graphics.shader import ShaderProgram
from pyglet.text import Label
from pyglet.gui import widgets
from pyglet.window import mouse

from pyglet.shapes import Rectangle, BorderedRectangle, ShapeBase, _rotate_point
from pyglet.gui.widgets import WidgetBase

from pyglet.graphics import Batch, Group

from Difficult_Rocket.api.types import Options, FontData

# from Difficult_Rocket import DR_status

RGBA = Tuple[int, int, int, int]


@dataclass
class WikiShapeColors:
    # 这里都是 未按下的颜色
    # 外面一圈高光
    highlight: RGBA = (255, 255, 255, 255)
    # 边框
    border: RGBA = (0, 0, 0, 255)
    # 下巴
    down_pad: RGBA = (49, 50, 51, 255)
    # 左下角和右上角的重叠点
    corner: RGBA = (124, 124, 125, 255)
    # 左上拐角
    left_up: RGBA = (109, 109, 110, 255)
    # 右下拐角
    right_down: RGBA = (90, 91, 92, 255)
    # 内部填充
    inner: RGBA = (72, 73, 74, 255)


class WikiButtonStyles(Enum):
    ...


class WikiButtonShape(ShapeBase):
    def __init__(
        self,
        x: float,
        y: float,
        width: float,
        height: float,
        pad: float = 2,
        down_pad: float = 5.0,
        pop_out: bool = True,
        highlight: bool = False,
        colors: WikiShapeColors | None = None,
        blend_src: int = GL_SRC_ALPHA,
        blend_dest: int = GL_ONE_MINUS_SRC_ALPHA,
        batch: Batch | None = None,
        group: Group | None = None,
        program: ShaderProgram | None = None,
    ):
        self._x = x
        self._y = y
        self._width = width
        self._height = height
        self._pad = pad
        self._down_pad = down_pad
        self._pop_out = pop_out
        self._highlight = highlight
        self._colors = colors or WikiShapeColors()

        vertex = 28
        if pop_out:
            vertex += 4
        if highlight:
            vertex += 4
        super().__init__(vertex, blend_src, blend_dest, batch, group, program)

    @property
    def pop_out(self) -> bool:
        return self._pop_out

    @property
    def pad(self) -> float:
        return self._pad

    @property
    def down_pad(self) -> float:
        return self._down_pad

    @property
    def colors(self) -> WikiShapeColors:
        return self._colors

    @property
    def highlight(self) -> bool:
        return self._highlight

    @pop_out.setter
    def pop_out(self, value: bool) -> None:
        self._pop_out = value
        self._create_vertex_list()

    @pad.setter
    def pad(self, value: float) -> None:
        self._pad = value
        self._update_vertices()

    @down_pad.setter
    def down_pad(self, value: float) -> None:
        self._down_pad = value
        self._update_vertices()

    @colors.setter
    def colors(self, value: WikiShapeColors) -> None:
        self._colors = value
        self._update_color()

    @highlight.setter
    def highlight(self, value: bool) -> None:
        self._highlight = value
        self._create_vertex_list()

    def _update_color(self) -> None:
        colors = (
            self._colors.down_pad * 4
            + self._colors.corner * 8
            + self._colors.right_down * 6
            + self._colors.left_up * 6
            + self._colors.inner * 4
        )
        if self._pop_out:
            colors = self._colors.border * 4 + colors
        if self._highlight:
            colors += self._colors.highlight * 4
        self._vertex_list.colors[:] = colors

    def __contains__(self, point: tuple[float, float]) -> bool:
        assert len(point) == 2
        point = _rotate_point((self._x, self._y), point, math.radians(self._rotation))
        x, y = self._x - self._anchor_x, self._y - self._anchor_y
        return x < point[0] < x + self._width and y < point[1] < y + self._height

    def _get_vertices(self) -> Sequence[float]:
        if not self._visible:
            return (0, 0) * self._num_verts

        left = -self._anchor_x
        right = left + self._width
        bottom = -self.anchor_y
        top = bottom + self._height

        pad = self._pad
        down_pad = self._down_pad

        in_left = left + pad
        i_right = right - pad
        in_bottom = bottom + pad
        inner_top = top - pad
        """
        pop out ( 默认的弹出状态 )
        20 顶点 (还有外面一圈高光)
        3                        2
            18          15   14
                 19     16   17

            11   10     13
            7    9           6
            4                5
        0                        1
        unpop
        16 顶点
        3                       2
            7          15   6
                13     12   14

            10   9     11
            4    8          5
        0                       1
        """
        # fmt: off
        out_border = [
            left,  bottom, # 0
            right, bottom, # 1
            right, top,    # 2
            left,  top,    # 3
        ]
        highlight = [
            left - pad,  bottom - pad, # max+1
            right + pad, bottom - pad, # max+2
            right + pad, top + pad,    # max+3
            left - pad,  top + pad,    # max+4
        ]
        if self._pop_out:
            down_top = in_bottom + down_pad
            # 底下那个下巴
            down_part = [
                in_left, in_bottom, # 4
                i_right, in_bottom, # 5
                i_right, down_top,  # 6
                in_left, down_top,  # 7
            ]
            # 左下角的小方块
            left_down = [
                in_left,       down_top,       # 8
                in_left + pad, down_top,       # 9
                in_left + pad, down_top + pad, # 10
                in_left,       down_top + pad, # 11
            ]
            # 右上角的小方块
            right_up = [
                i_right - pad, inner_top - pad, # 12
                i_right,       inner_top - pad, # 13
                i_right,       inner_top,       # 14
                i_right - pad, inner_top,       # 15
            ]
            # 左上的拐弯条
            # 1   2
            #   4 3
            # 0 5
            left_up = [
                in_left,       down_top + pad,  # 16
                in_left,       inner_top,       # 17
                i_right - pad, inner_top,       # 18
                i_right - pad, inner_top - pad, # 19
                in_left + pad, inner_top - pad, # 20
                in_left + pad, down_top + pad,  # 21
            ]
            # 右下的拐弯条
            #   3 2
            # 5 4
            # 0   1
            right_down = [
                in_left + pad, down_top,        # 22
                i_right,       down_top,        # 23
                i_right,       inner_top - pad, # 24
                i_right - pad, inner_top - pad, # 25
                i_right - pad, down_top + pad,  # 26
                in_left + pad, down_top + pad,  # 27
            ]
            # 中间的方块
            inner_box = [
                in_left + pad, down_top + pad,  # 28
                i_right - pad, down_top + pad,  # 29
                i_right - pad, inner_top - pad, # 30
                in_left + pad, inner_top - pad, # 31
            ]
            if self._highlight:
                return (out_border +
                        down_part +
                        left_down + right_up +
                        left_up + right_down +
                        inner_box +
                        highlight)
            else:
                return (out_border +
                        down_part +
                        left_down + right_up +
                        left_up + right_down +
                        inner_box)
        else:
            # 左下角的小方块
            left_down = [
                in_left,       in_bottom,       # 4
                in_left + pad, in_bottom,       # 5
                in_left + pad, in_bottom + pad, # 6
                in_left,       in_bottom + pad, # 7
            ]
            # 右上角的小方块
            right_up = [
                i_right - pad, inner_top - pad, # 8
                i_right,       inner_top - pad, # 9
                i_right,       inner_top,       # 10
                i_right - pad, inner_top,       # 11
            ]
            # 左上的拐弯条
            # 1   2
            #   4 3
            # 0 5
            left_up = [
                in_left,       in_bottom + pad,  # 12
                in_left,       inner_top,        # 13
                i_right - pad, inner_top,        # 14
                i_right - pad, inner_top - pad,  # 15
                in_left + pad, inner_top - pad,  # 16
                in_left + pad, in_bottom + pad,  # 17
            ]
            # 右下的拐弯条
            #   3 2
            # 5 4
            # 0   1
            right_down = [
                in_left + pad, in_bottom,        # 18
                i_right,       in_bottom,        # 19
                i_right,       inner_top - pad,  # 20
                i_right - pad, inner_top - pad,  # 21
                i_right - pad, in_bottom + pad,  # 22
                in_left + pad, in_bottom + pad,  # 23
            ]
            # 中间的方块
            inner_box = [
                in_left + pad, in_bottom + pad,  # 24
                i_right - pad, in_bottom + pad,  # 25
                i_right - pad, inner_top - pad,  # 26
                in_left + pad, inner_top - pad,  # 27
            ]
            if self._highlight:
                return (out_border +
                        left_down + right_up +
                        left_up + right_down +
                        inner_box +
                        highlight)
            else:
                return (out_border +
                        left_down + right_up +
                        left_up + right_down +
                        inner_box)
        # fmt: on

    def _create_vertex_list(self) -> None:
        colors = self._colors.border * 4
        # fmt: off
        indices = [
            0, 1, 2, # 最基本的两个三角形
            0, 2, 3, # 用来画黑色边框
        ]
        if self._pop_out:
            indices += [4, 5, 6, 4, 6, 7]  # 下巴
            indices += [8, 9, 10, 8, 10, 11]  # 左下角
            indices += [12, 13, 14, 12, 14, 15]  # 右上角
            indices += [16, 17, 20, 16, 20, 21,
                        18, 19, 20, 18, 17, 20]  # 左上拐弯
            indices += [22, 23, 26, 22, 26, 27,
                        23, 24, 26, 24, 25, 26]  # 右下拐弯
            indices += [28, 29, 30, 28, 30, 31]  # 中间的方块
            if self._highlight:
                indices = [32, 33, 34, 32, 34, 35] + indices  # 高光
            colors += (
                self._colors.down_pad * 4
                + self._colors.corner * 8
                + self._colors.right_down * 6
                + self._colors.left_up * 6
                + self._colors.inner * 4
            )
            self._num_verts = 32
        else:
            indices += [4, 5, 6, 4, 6, 7]  # 左下角
            indices += [8, 9, 10, 8, 10, 11]  # 右上角
            indices += [12, 16, 17, 12, 13, 16,
                        14, 15, 16, 14, 13, 16]  # 左上拐弯
            indices += [18, 22, 23, 18, 19, 22,
                        20, 21, 22, 20, 19, 22]  # 右下拐弯
            indices += [24, 25, 26, 24, 26, 27]
            if self._highlight:
                indices = [28, 29, 30, 28, 30, 31] + indices  # 高光
            colors += (
                self._colors.corner * 8
                + self._colors.right_down * 6
                + self._colors.left_up * 6
                + self._colors.inner * 4
            )
            self._num_verts = 28
        if self._highlight:
            self._num_verts += 4
            colors += self._colors.highlight * 4
        # fmt: on
        self._vertex_list = self._program.vertex_list_indexed(
            self._num_verts,
            self._draw_mode,
            indices,
            self._batch,
            self._group,
            position=("f", self._get_vertices()),
            colors=("Bn", colors),
            translation=("f", (self._x, self._y) * self._num_verts),
        )

    def _update_vertices(self) -> None:
        self._vertex_list.position[:] = self._get_vertices()


class 拐角(ShapeBase):
    def __init__(
        self,
        x: float,
        y: float,
        width: float,
        height: float,
        thick1: float = 1.0,
        thick2: float = 1.0,
        color: tuple[int, int, int, int] = (255, 255, 255, 255),
        clockwise: bool = True,
        blend_src: int = GL_SRC_ALPHA,
        blend_dest: int = GL_ONE_MINUS_SRC_ALPHA,
        batch: Batch | None = None,
        group: Group | None = None,
        program: ShaderProgram | None = None,
    ) -> None:
        self._x = x
        self._y = y
        self._width = width
        self._height = height
        self._thick1 = thick1
        self._thick2 = thick2
        self._clockwise = clockwise

        self._rgba = color
        super().__init__(6, blend_src, blend_dest, batch, group, program)

    def __contains__(self, point: tuple[float, float]) -> bool:
        assert len(point) == 2
        # 先大框
        point = _rotate_point((self._x, self._y), point, math.radians(self._rotation))
        x, y = self._x - self._anchor_x, self._y - self._anchor_y
        return (x < point[0] < x + self._width and y < point[1] < y + self._height) and (
            (
                (point[1] > y + self._height - self._thick2)
                or (point[0] < x + self._thick1)
            )
            if self._clockwise
            else (
                (point[1] < y + self._thick1)
                or (point[0] > x + self._width - self._thick2)
            )
        )

    def _get_vertices(self) -> Sequence[float]:
        if not self.visible:
            return (0, 0) * self._num_verts

        t1, t2 = self._thick1, self._thick2
        left = -self._anchor_x
        bottom = -self._anchor_y
        right = left + self._width
        top = bottom + self._height

        x1 = left
        x2 = left + t1
        x3 = right - t1
        x4 = right
        y1 = bottom
        y2 = bottom + t1
        y3 = top - t2
        y4 = top

        # fmt: off
        return ([
                x1, y1,
                x1, y4,
                x4, y4,
                x4, y3,
                x2, y3,
                x2, y1
            ] if self._clockwise else[
                x1, y1,
                x4, y1,
                x4, y4,
                x3, y4,
                x3, y2,
                x1, y2
            ])
        # fmt: on

    def _update_color(self) -> None:
        self._vertex_list.colors[:] = self._rgba * self._num_verts

    def _update_vertices(self) -> None:
        self._vertex_list.position[:] = self._get_vertices()  # pyright: ignore reportAttributeAccessIssue

    def _create_vertex_list(self) -> None:
        # 1   2
        #   4 3
        # 0 5
        # or
        #   3 2
        # 5 4
        # 0   1
        # fmt: off
        groups = [
            1, 2, 3,
            1, 3, 4,
            1, 4, 5,
            1, 5, 0,
        ]
        # fmt: on
        self._vertex_list = self._program.vertex_list_indexed(
            self._num_verts,
            self._draw_mode,
            groups,
            self._batch,  # pyright: ignore reportArgumentType
            self._group,  # pyright: ignore reportArgumentType
            position=("f", self._get_vertices()),
            colors=("Bn", self._rgba * self._num_verts),
            translation=("f", (self._x, self._y) * self._num_verts),
        )

    @property
    def thick1(self) -> float:
        return self._thick1

    @property
    def thick2(self) -> float:
        return self.thick2

    @property
    def thickness(self) -> float:
        return self._thick1

    @thickness.setter
    def thickness(self, value: float):
        self._thick1 = value
        self._thick2 = value
        self._update_vertices()

    @property
    def width(self) -> float:
        return self._width

    @property
    def height(self) -> float:
        return self.height

    @property
    def clockwise(self) -> bool:
        return self._clockwise

    @thick1.setter
    def thick1(self, value: float):
        self._thick1 = value
        self._update_vertices()

    @thick2.setter
    def thick2(self, value: float):
        self._thick2 = value
        self._update_vertices()

    @width.setter
    def width(self, value: float):
        self._width = value
        self._update_vertices()

    @height.setter
    def height(self, value: float):
        self._height = value
        self._update_vertices()

    @clockwise.setter
    def clockwise(self, value: bool):
        self._clockwise = bool(value)
        self._update_vertices()


class WikiButton(WidgetBase):
    # 背景的颜色
    backgroud_color = (0, 0, 0, 255)
    # 内部填充的颜色
    inner_normal = (72, 73, 74, 255)
    inner_press = (49, 50, 51, 255)
    # 左上角的普通状态下颜色
    upper_normal = (109, 109, 110, 255)
    upper_press = (90, 91, 92, 255)
    # 右下角的
    down_normal = (90, 91, 92, 255)
    down_press = (70, 71, 71, 255)
    # 左下角方块
    corner_normal = (124, 124, 125, 255)
    corner_press = (106, 107, 108, 255)
    # 下巴的颜色
    down_pad_color = (49, 50, 51, 255)

    def __init__(
        self, x: int, y: int, width: int, height: int, batch: Batch, group: Group
    ) -> None:
        super().__init__(x, y, width, height)
        self.enabled = False
        pad = 2
        down_pad = 5
        self.pad = pad
        self.down_pad = down_pad
        # 覆盖式
        self.main_batch = batch or Batch()
        self.main_group = group or Group()

        # 背景的黑框
        self.background_group = Group(order=10, parent=self.main_group)
        # 左上右下两组
        self.border_group = Group(order=20, parent=self.main_group)
        # 左下右上两个小方块
        self.corner_group = Group(order=30, parent=self.main_group)
        # 内部填充
        self.inner_group = Group(order=40, parent=self.main_group)

        self.backgroud = Rectangle(
            x=self.x,
            y=self.y,
            width=width,
            height=height,
            color=self.backgroud_color,
            batch=self.main_batch,
            group=self.background_group,
        )
        self.upper_border = 拐角(
            x=self.x + pad,
            y=self.y + pad + down_pad,
            width=width - (pad * 2),
            height=height - (pad * 2) - down_pad,
            thick1=pad,
            thick2=pad,
            color=self.upper_normal,
            batch=self.main_batch,
            group=self.border_group,
        )
        self.down_border = 拐角(
            x=self.x + pad,
            y=self.y + pad + down_pad,
            width=width - (pad * 2),
            height=height - (pad * 2) - down_pad,
            thick1=pad,
            thick2=pad,
            clockwise=False,
            color=self.down_normal,
            batch=self.main_batch,
            group=self.border_group,
        )
        self.left_down = Rectangle(
            x=self.x + pad,
            y=self.y + pad + down_pad,
            width=pad,
            height=pad,
            color=self.corner_normal,
            batch=self.main_batch,
            group=self.corner_group,
        )
        self.right_up = Rectangle(
            x=self.x + self.width - (pad * 2),
            y=self.y + self.height - (pad * 2),
            width=pad,
            height=pad,
            color=self.corner_normal,
            batch=self.main_batch,
            group=self.corner_group,
        )
        self.inner_fill = Rectangle(
            x=self.x + pad + pad,
            y=self.y + pad + pad + down_pad,
            width=self.width - (pad * 4),
            height=self.height - (pad * 4) - down_pad,
            color=self.inner_normal,
            batch=self.main_batch,
            group=self.inner_group,
        )
        self.down_fill = Rectangle(
            x=self.x + pad,
            y=self.y + pad,
            width=width - (pad * 2),
            height=down_pad,
            color=self.down_pad_color,
            batch=self.main_batch,
            group=self.border_group,
        )

    def __contains__(self, pos: tuple[float, float]) -> bool:
        return self._check_hit()

    def on_mouse_press(self, x: int, y: int, buttons: int, modifiers: int) -> None:
        if (x, y) in self:
            ...


class BaseButtonTheme:
    """
    按钮的风格
    """

    name = "BaseButtonTheme"

    def __init__(
        self, x: int, y: int, width: int, height: int, batch: Batch, group: Group
    ):
        self.batch = batch
        self.group = group
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.enable = False

    def on_enable(self, x: int, y: int, button):
        """
        当按钮被启用的时候
        :param x:
        :param y:
        :param button:
        :return:
        """

    def on_disable(self, button):
        """
        当按钮被禁用的时候
        :param button:
        :return:
        """

    def on_update(self, button) -> None:
        """
        当按钮被更新的时候
        :param button:
        :return:
        """


class MinecraftWikiButtonTheme(BaseButtonTheme):
    """
    直接绘制按钮的风格
    """

    name = "MinecraftWikiButtonTheme"

    def __init__(
        self,
        x: int,
        y: int,
        width: int,
        height: int,
        batch: Batch,
        group: Group,
        theme: Optional[dict] = None,
    ):
        super().__init__(x, y, width, height, batch, group)
        self.enable = False
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
        if theme is None:
            theme = {}
        pop_out = theme.get("pop_out", False)
        if pop_out:
            # 主背景
            self.back_ground = Rectangle(
                x=x + (pad * 2),
                y=y + (pad * 2) + list_pad,
                width=width - (pad * 4),
                height=height - (pad * 4) - list_pad,
                color=a,
                batch=batch,
                group=Group(order=3, parent=group),
            )
            # 左上方向的覆盖
            self.cover_back = Rectangle(
                x=x + pad,
                y=y + pad + list_pad,
                width=width - (pad * 2),
                height=height - (pad * 2) - list_pad,
                color=b,
                batch=batch,
                group=Group(order=1, parent=group),
            )
            # 右下方向的覆盖
            self.cover_back2 = Rectangle(
                x=x + (pad * 2),
                y=y + pad + list_pad,
                width=width - (pad * 3),
                height=height - (pad * 3) - list_pad,
                color=c,
                batch=batch,
                group=Group(order=2, parent=group),
            )
        else:
            # 主背景
            self.back_ground = Rectangle(
                x=x + (pad * 2),
                y=y + (pad * 2) + list_pad,
                width=width - (pad * 4),
                height=height - (pad * 4) - list_pad,
                color=c,
                batch=batch,
                group=Group(order=3, parent=group),
            )
            # 左上方向的覆盖
            self.cover_back = Rectangle(
                x=x + pad,
                y=y + pad + list_pad,
                width=width - (pad * 2),
                height=height - (pad * 2) - list_pad,
                color=a,
                batch=batch,
                group=Group(order=2, parent=group),
            )
            # 右下方向的覆盖
            self.cover_back2 = Rectangle(
                x=x + pad,
                y=y + (pad * 2) + list_pad,
                width=width - (pad * 3),
                height=height - (pad * 3) - list_pad,
                color=b,
                batch=batch,
                group=Group(order=1, parent=group),
            )
        # 下巴的框
        self.list_back = BorderedRectangle(
            x=x,
            y=y,
            width=width,
            height=height,
            border=pad,
            border_color=(0, 0, 0, 255),
            color=e,
            batch=batch,
            group=Group(order=0, parent=group),
        )
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
        self.pop_out = pop_out
        self.drag_list = theme.get("drag_list", False)

    def on_enable(self, x: int, y: int, button):
        if self.pop_out:
            self.back_ground.color = self.touch_a
            self.cover_back.color = self.touch_b
            self.cover_back2.color = self.touch_c
        else:
            self.back_ground.color = self.touch_c
            self.cover_back.color = self.touch_a
            self.cover_back2.color = self.touch_b
        if self.drag_list:
            button.text_label.y = (
                self.y
                + (self.height - button.font_height) // 2
                + (button.font_height * 0.2)
                + (self.list_pad // 2)
            )
            self.back_ground.y = self.y + (self.pad * 2)
            self.back_ground.height = self.height - (self.pad * 4)
            self.cover_back.y = self.y + self.pad
            self.cover_back.height = self.height - (self.pad * 2)
            self.cover_back2.y = self.y + self.pad
            self.cover_back2.height = self.height - (self.pad * 3)
        else:
            button.text_label.y = (
                self.y
                + (self.height - button.font_height) // 2
                + (button.font_height * 0.2)
                + self.list_pad
            )
        self.enable = True

    def on_disable(self, button) -> None:
        if self.pop_out:
            self.back_ground.color = self.a
            self.cover_back.color = self.b
            self.cover_back2.color = self.c
        else:
            self.back_ground.color = self.c
            self.cover_back.color = self.a
            self.cover_back2.color = self.b
        if self.drag_list:
            self.back_ground.y = self.y + (self.pad * 2) + self.list_pad
            self.back_ground.height = self.height - (self.pad * 4) - self.list_pad
            self.cover_back.y = self.y + self.pad + self.list_pad
            self.cover_back.height = self.height - (self.pad * 2) - self.list_pad
            self.cover_back2.y = self.y + self.pad + self.list_pad
            self.cover_back2.height = self.height - (self.pad * 3) - self.list_pad
        button.text_label.y = (
            self.y
            + (self.height - button.font_height) // 2
            + (button.font_height * 0.2)
            + self.list_pad
        )
        self.enable = False

    def on_update(self, button) -> None:
        super().on_update(button)
        self.list_back.x = self.x
        self.list_back.y = self.y
        if self.enable and self.drag_list:
            button.text_label.y = (
                self.y
                + (self.height - button.font_height) // 2
                + (button.font_height * 0.2)
                + self.list_pad // 2
            )

            self.back_ground.x = self.x + (self.pad * 2)
            self.back_ground.y = self.y + (self.pad * 2)
            self.back_ground.position = self.x + (self.pad * 2), self.y + (self.pad * 2)
            self.back_ground.height = self.height - (self.pad * 4)
            self.cover_back.x = self.x + self.pad
            self.cover_back.y = self.y + self.pad
            self.cover_back.position = self.x + self.pad, self.y + self.pad
            self.cover_back.height = self.height - (self.pad * 2)
            self.cover_back2.x = self.x + self.pad
            self.cover_back2.y = self.y + self.pad
            self.cover_back2.position = self.x + self.pad, self.y + self.pad
            self.cover_back2.height = self.height - (self.pad * 3)
        else:
            button.text_label.y = (
                self.y
                + (self.height - button.font_height) // 2
                + (button.font_height * 0.2)
                + self.list_pad
            )
            self.back_ground.position = (
                self.x + (self.pad * 2),
                self.y + (self.pad * 2) + self.list_pad,
            )
            self.back_ground.height = self.height - (self.pad * 4) - self.list_pad
            self.cover_back.position = (
                self.x + self.pad,
                self.y + self.pad + self.list_pad,
            )
            self.cover_back.height = self.height - (self.pad * 2) - self.list_pad
            self.cover_back2.position = (
                self.x + self.pad,
                self.y + self.pad + self.list_pad,
            )
            self.cover_back2.height = self.height - (self.pad * 3) - self.list_pad
        self.back_ground.position = (
            self.x + (self.pad * 2),
            self.y + (self.pad * 2) + self.list_pad,
        )
        self.back_ground.height = self.height - (self.pad * 4) - self.list_pad


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
        draw_theme: Optional[Type[BaseButtonTheme]] = None,
        dict_theme: Optional[dict] = None,
    ):
        super().__init__(x, y, width, height)
        self.main_batch = batch or Batch()
        self.user_batch = batch is not None
        self.front_group = Group(order=10, parent=group)
        self.back_ground_group = Group(order=5, parent=group)
        self.pressed = False

        self.theme = theme or ButtonThemeOptions()
        if dict_theme is None:
            dict_theme = {}
        self.dict_theme = dict_theme

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
            self.draw_theme.on_update(self)

        self.value = text  # 重新分配一下高度和宽度的位置

    @property
    def x(self) -> int:
        return self._x

    @x.setter
    def x(self, value: int) -> None:
        self._x = value
        self.text_label.x = value
        if self.draw_theme:
            assert isinstance(self.draw_theme, BaseButtonTheme)
            self.draw_theme.x = value
            self.draw_theme.on_update(self)

    @property
    def y(self) -> int:
        return self._y

    @y.setter
    def y(self, value: int) -> None:
        self._y = value
        self.text_label.y = value + 4
        if self.draw_theme:
            assert isinstance(self.draw_theme, BaseButtonTheme)
            self.draw_theme.y = value
            self.draw_theme.on_update(self)

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
            self._y + (self.height - self.font_height) // 2 + (self.font_height * 0.2)
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
                assert isinstance(self.draw_theme, BaseButtonTheme)
                self.draw_theme.on_disable(self)
            else:
                self.back_rec.color = self.untouched_color

    def on_mouse_press(self, x, y, buttons, modifiers) -> bool:
        if (x, y) in self:
            if buttons == mouse.LEFT:
                if self.draw_theme:
                    assert isinstance(self.draw_theme, BaseButtonTheme)
                    self.draw_theme.on_enable(x, y, self)
                else:
                    self.back_rec.color = self.hit_color
                self.dispatch_event("on_press", x, y)
                self.pressed = True
                return True
        else:
            self.pressed = False
            if self.draw_theme:
                assert isinstance(self.draw_theme, BaseButtonTheme)
                self.draw_theme.on_disable(self)
            else:
                self.back_rec.color = self.untouched_color
        return False

    def on_mouse_release(self, x, y, buttons, modifiers):
        if self.pressed and (x, y) in self:
            if self.draw_theme:
                assert isinstance(self.draw_theme, BaseButtonTheme)
                self.draw_theme.on_disable(self)
            else:
                self.back_rec.color = self.touched_color
            self.pressed = False
            self.dispatch_event("on_release", self, x, y)

    def _update_position(self):
        self.text_label.position = self._x, self._y, 0
        self.back_rec.position = self._x, self._y
        self.back_rec.width = self._width
        self.back_rec.height = self._height


PressTextButton.register_event_type("on_press")
PressTextButton.register_event_type("on_release")
