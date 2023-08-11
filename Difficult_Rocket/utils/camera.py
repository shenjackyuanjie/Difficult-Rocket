#  -------------------------------
#  Difficult Rocket
#  Copyright © 2020-2023 by shenjackyuanjie 3695888@qq.com
#  All rights reserved
#  -------------------------------
# Huge thanks to pyglet developers

from typing import Tuple, Optional

from pyglet.gl import gl
from pyglet.math import Mat4, Vec3
from pyglet.graphics import Group


class Camera:
    """
    
    >>> from pyglet.window import Window
    >>> window = Window()
    
    >>> camera = Camera(window)
    >>> @window.event
    
    >>> def on_draw():
    >>>     camera.begin()
    >>>     window.clear()
    >>>     camera.end()
    
    """

    def __init__(self,
                 window,
                 zoom: Optional[float] = 1.0,
                 dx: Optional[float] = 1.0,
                 dy: Optional[float] = 1.0,
                 min_zoom: Optional[float] = 1.0,
                 max_zoom: Optional[float] = 1.0) -> None:
        self.window = window
        self.dx = dx
        self.dy = dy
        self.zoom = zoom
        self.min_zoom = min_zoom
        self.max_zoom = max_zoom
        self._stored_view = window.view

    @property
    def position(self) -> Tuple[float, float]:
        return self.dx, self.dy

    @position.setter
    def position(self, value: Tuple[float, float]):
        self.dx, self.dy = value

    @property
    def zoom_level(self) -> float:
        return self.zoom

    @zoom_level.setter
    def zoom_level(self, value: float) -> None:
        self.zoom = min(max(value, self.min_zoom), self.max_zoom)

    def begin(self) -> None:
        view = self.window.view
        self._stored_view = view
        x = self.window.width / self.zoom + (self.dx / self.zoom)
        y = self.window.height / self.zoom + (self.dy / self.zoom)

        view_matrix = view.translate((x * self.zoom, y * self.zoom, 0))
        view_matrix = view_matrix.scale((self.zoom, self.zoom, 1))

        self.window.view = view_matrix

    def end(self) -> None:
        self.window.view = self._stored_view

    def reset(self):
        self.zoom = 1
        self.dx = 0
        self.dy = 0

    def __enter__(self):
        self.begin()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.end()


class CenterCamera(Camera):
    """
    A camera that centers the view in the center of the window
    
    >>> from pyglet.window import Window
    >>> window = Window()
    
    >>> camera = CenterCamera(window)
    >>> @window.event
    
    >>> def on_draw():
    >>>     camera.begin()
    >>>     window.clear()
    >>>     camera.end()
    """

    def begin(self) -> None:
        view = self.window.view
        self._stored_view = view
        x = self.window.width / 2.0 / self.zoom + (self.dx / self.zoom)
        y = self.window.height / 2.0 / self.zoom + (self.dy / self.zoom)

        view_matrix = view.translate((x * self.zoom, y * self.zoom, 0))
        view_matrix = view_matrix.scale((self.zoom, self.zoom, 1))

        self.window.view = view_matrix

    def end(self) -> None:
        self.window.view = self._stored_view


class GroupCamera(Group):
    """
    A camera by group
    can be used by just added to your widget
    """

    def __init__(self,
                 window,
                 order: int = 0,
                 parent: Optional[Group] = None,
                 view_x: Optional[int] = 0,
                 view_y: Optional[int] = 0,
                 zoom: Optional[float] = 1.0,
                 min_zoom: Optional[float] = 1.0,
                 max_zoom: Optional[float] = 1.0):
        super().__init__(order=order, parent=parent)
        self._window = window
        self._previous_view = None

        self._view_x = view_x
        self._view_y = view_y
        self._zoom = zoom
        self._zoom_x = self._zoom
        self._zoom_y = self._zoom
        self.min_zoom = min_zoom
        self.max_zoom = max_zoom

    @property
    def view_x(self) -> int:
        return self._view_x

    @view_x.setter
    def view_x(self, value: int):
        self._view_x = value

    @property
    def view_y(self) -> int:
        return self._view_y

    @view_y.setter
    def view_y(self, value: int):
        self._view_y = value

    @property
    def zoom(self) -> float:
        return self._zoom

    @zoom.setter
    def zoom(self, value: float):
        self._zoom = value
        self._zoom_x = self._zoom
        self._zoom_y = self._zoom

    def reset(self):
        self._view_x = 0
        self._view_y = 0
        self._zoom = 1

    def set_state(self):
        self._previous_view = self._window.view

        view = Mat4.from_translation(Vec3(self._view_x, self._view_y, 0))
        if self._zoom == 1.0:
            self._window.view = view
        else:
            view = view.scale(Vec3(self._zoom, self._zoom, 1))
            self._window.view = view

    def unset_state(self):
        self._window.view = self._previous_view


class CenterGroupCamera(GroupCamera):
    """
    A camera by group
    can be used by just added to your widget
    """

    def set_state(self):
        self._previous_view = self._window.view

        x = (self._window.width / 2) / self._zoom_x + (self._view_x / self._zoom_x)
        y = (self._window.height / 2) / self._zoom_y + (self._view_y / self._zoom_y)

        view = Mat4.from_translation(Vec3(x * self._zoom_x, y * self._zoom_y, 0))
        # 不懂就问 为啥这里 * zoom 下面还 * zoom
        if self._zoom == 1.0 and self._zoom_x == 1.0 and self._zoom_y == 1.0:
            self._window.view = view
        else:
            view = view.scale(Vec3(self._zoom_x, self._zoom_y, 1))
            self._window.view = view

    def unset_state(self):
        self._window.view = self._previous_view
