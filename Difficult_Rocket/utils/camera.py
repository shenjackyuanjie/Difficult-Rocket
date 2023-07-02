#  -------------------------------
#  Difficult Rocket
#  Copyright © 2020-2023 by shenjackyuanjie 3695888@qq.com
#  All rights reserved
#  -------------------------------

# Huge thanks to pyglet developers

from typing import Tuple, Optional


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
    