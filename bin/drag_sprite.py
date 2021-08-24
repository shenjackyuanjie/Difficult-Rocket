"""
writen by shenjackyuanjie
mail:   3695888@qq.com
github: @shenjackyuanjie
gitee:  @shenjackyuanjie
"""

import sys

if __name__ == '__main__':  # been start will not run this
    sys.path.append('/bin/libs')
    sys.path.append('/bin')

import pyglet
from pyglet.window import mouse
from pyglet.gui.widgets import WidgetBase


class DragSprite(WidgetBase):
    """Instance of a drag button.

    Triggers the event 'on_press' when it is clicked by the mouse.
    Triggers the event 'on_release' when the mouse is released.
    Triggers the event 'on_drag' when it is drag by mouse.
    """

    # TODO make it More standardized
    # TODO add group thing again(i don't know how to)
    # by shenjack

    def __init__(self,
                 x: int,
                 y: int,
                 image: pyglet.image.AbstractImage,
                 drag_by_all: bool = False,
                 drag_out_window: bool = False,
                 batch: pyglet.graphics.Batch = None,
                 group: pyglet.graphics.Group = None):
        """Create a draggable sprite.

        :Parameters:
            `x` : int
                X coordinate of the push button.
            `y` : int
                Y coordinate of the push button.
            `image` : `~pyglet.image.AbstractImage`
                Image to display when the sprite is pressed.
            `drag_by_all` : bool
                If True then sprite will move whatever witch mouse button drag the sprite,
                or the sprite will only move when Left mouse button drag.
            `drag_out_window` : bool
                If True then sprite will move out of the window with the mouse dragging,
                or the sprite will only stop on the edge of the window.
            `batch` : `~pyglet.graphics.Batch`
                Optional batch to add the sprite to.
            `group` : `~pyglet.graphics.Group`
                Optional parent group of the sprite.
        """
        super().__init__(x, y, image.width, image.height)
        self._image = image
        self._batch = batch or pyglet.graphics.Batch()
        self._sprite = pyglet.sprite.Sprite(self._image, x, y, batch=batch, group=group)
        self.drag_by_all = drag_by_all
        self.drag_out_window = drag_out_window
        self.dragging = False

    def _check_hit(self, x, y):
        print(self._x, self._y, x, y, self._width, self._height)
        return self._x < x < self._x + self._width and self._y < y < self._y + self._height

    def on_mouse_press(self, x, y, buttons, modifiers):
        if (buttons == mouse.LEFT) or self.drag_by_all:
            if self._check_hit(x, y):
                self.dragging = True
                self.dispatch_event('on_press', buttons, self.dragging)

    def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
        if self.dragging:
            # TODO find a way to get window height and width
            if (self._x + dx) < 0 and not self.drag_out_window:
                self._sprite.x = 0
                self._x = 0
            else:
                self._sprite.x += dx
                self._x += dx
            if (self._y + dy) < 0 and not self.drag_out_window:
                self._sprite.y = 0
                self._y = 0
            else:
                self._sprite.y += dy
                self._y += dy
            self.dispatch_event('on_drag', x, y, dx, dy, buttons, modifiers)

    def draw(self):
        self._sprite.draw()
        # just use self.draw can draw

    def on_mouse_release(self, x, y, buttons, modifiers):
        if self.dragging:
            self.dragging = not self.dragging
            self.dispatch_event('on_release', x, y, buttons, modifiers)


DragSprite.register_event_type('on_drag')
DragSprite.register_event_type('on_press')
DragSprite.register_event_type('on_release')
