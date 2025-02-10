#  -------------------------------
#  Difficult Rocket
#  Copyright © 2020-2023 by shenjackyuanjie 3695888@qq.com
#  All rights reserved
#  -------------------------------

from __future__ import annotations

from typing import TYPE_CHECKING, TypeVar
from os import PathLike

# from pyglet.window import Window
from pyglet.event import EventDispatcher

# Difficult Rocket function
from Difficult_Rocket.api.types import Options
from Difficult_Rocket.command.api import CommandText

if TYPE_CHECKING:
    from Difficult_Rocket.client import ClientWindow
else:
    ClientWindow = TypeVar("ClientWindow")


class BaseScreen(EventDispatcher, Options):
    """
    DR 的 页面API
    """

    name: str = "BaseScreen"

    def __init__(self, main_window: ClientWindow):
        super().__init__()
        self.focus = False
        self.window_pointer = main_window

    def on_cleanup(self, window: ClientWindow):
        """
        页面清理
        会在被移除的时候调用
        添加自: 0.9.2.0
        """

    if TYPE_CHECKING:

        def on_command(self, command: CommandText, window: ClientWindow) -> None | bool:
            """
            命令输入事件
            """

        def on_message(self, message: CommandText, window: ClientWindow) -> None | bool:
            """
            消息输入事件
            """

        def draw_update(self, tick: float, window: ClientWindow) -> None | bool:
            """
            画面更新
            如果返回 True, 则会取消后续的绘制
            """

        def draw_batch(self, window: ClientWindow) -> None | bool:
            """
            画面绘制
            如果返回 True, 则会取消后续的绘制
            """

        """
        Pyglet 定义的事件
        """

        def on_activate(self, window: ClientWindow) -> None | bool:
            """The window was activated.

            This event can be triggered by clicking on the title bar, bringing
            it to the foreground; or by some platform-specific method.

            When a window is "active" it has the keyboard focus.

            :event:
            """

        def on_close(self, source: str, window: ClientWindow) -> None:
            """The user attempted to close the window.

            This event can be triggered by clicking on the "X" control box in
            the window title bar, or by some other platform-dependent manner.

            The default handler sets `has_exit` to ``True``.  In pyglet 1.1, if
            `pyglet.app.event_loop` is being used, `close` is also called,
            closing the window immediately.

            :event:
            """

        def on_context_lost(self, window: ClientWindow) -> None:
            """The window's GL context was lost.

            When the context is lost no more GL methods can be called until it
            is recreated.  This is a rare event, triggered perhaps by the user
            switching to an incompatible video mode.  When it occurs, an
            application will need to reload all objects (display lists, texture
            objects, shaders) as well as restore the GL state.

            :event:
            """

        def on_context_state_lost(self, window: ClientWindow):
            """The state of the window's GL context was lost.

            pyglet may sometimes need to recreate the window's GL context if
            the window is moved to another video device, or between fullscreen
            or windowed mode.  In this case it will try to share the objects
            (display lists, texture objects, shaders) between the old and new
            contexts.  If this is possible, only the current state of the GL
            context is lost, and the application should simply restore state.

            :event:
            """

        def on_deactivate(self, window: ClientWindow):
            """The window was deactivated.

            This event can be triggered by clicking on another application
            window.  When a window is deactivated it no longer has the
            keyboard focus.

            :event:
            """

        # def on_draw(self, dt: float, window: ClientWindow):  # TODO: wait for pyglet 2.1
        def on_draw(self, window: ClientWindow) -> None:
            """The window contents must be redrawn.

            The `EventLoop` will dispatch this event when the window
            should be redrawn.  This will happen during idle time after
            any window events and after any scheduled functions were called.

            The window will already have the GL context, so there is no
            need to call `switch_to`.  The window's `flip` method will
            be called after this event, so your event handler should not.

            You should make no assumptions about the window contents when
            this event is triggered; a resize or expose event may have
            invalidated the framebuffer since the last time it was drawn.

            .. versionadded:: 1.1

            :event:
            """

        def on_expose(self, window: ClientWindow) -> None:
            """A portion of the window needs to be redrawn.

            This event is triggered when the window first appears, and any time
            the contents of the window is invalidated due to another window
            obscuring it.

            There is no way to determine which portion of the window needs
            redrawing.  Note that the use of this method is becoming
            increasingly uncommon, as newer window managers composite windows
            automatically and keep a backing store of the window contents.

            :event:
            """

        def on_file_drop(
            self, x: int, y: int, paths: list[PathLike], window: ClientWindow
        ):
            """File(s) were dropped into the window, will return the position of the
            cursor and a list of paths to the files that were dropped.

            .. versionadded:: 1.5.1

            :event:
            """

        def on_hide(self, window: ClientWindow):
            """The window was hidden.

            This event is triggered when a window is minimised
            or hidden by the user.

            :event:
            """

        def on_key_press(
            self, symbol: int, modifiers: int, window: ClientWindow
        ) -> None | bool:
            """A key on the keyboard was pressed (and held down).

            Since pyglet 1.1 the default handler dispatches the
            :py:meth:`~pyglet.window.Window.on_close`
            event if the ``ESC`` key is pressed.

            :Parameters:
                `symbol` : int
                    The key symbol pressed.
                `modifiers` : int
                    Bitwise combination of the key modifiers active.

            :event:
            """

        def on_key_release(
            self, symbol: int, modifiers: int, window: ClientWindow
        ) -> None | bool:
            """A key on the keyboard was released.

            :Parameters:
                `symbol` : int
                    The key symbol pressed.
                `modifiers` : int
                    Bitwise combination of the key modifiers active.

            :event:
            """

        def on_mouse_motion(
            self, x: int, y: int, dx: int, dy: int, window: ClientWindow
        ) -> None | bool:
            """The mouse was moved with no buttons held down.

            :Parameters:
                `x` : int
                    Distance in pixels from the left edge of the window.
                `y` : int
                    Distance in pixels from the bottom edge of the window.
                `dx` : int
                    Relative X position from the previous mouse position.
                `dy` : int
                    Relative Y position from the previous mouse position.

            :event:
            """

        def on_mouse_drag(
            self,
            x: int,
            y: int,
            dx: int,
            dy: int,
            buttons: int,
            modifiers: int,
            window: ClientWindow,
        ) -> None | bool:
            """The mouse was moved with one or more mouse buttons pressed.

            This event will continue to be fired even if the mouse leaves
            the window, so long as the drag buttons are continuously held down.

            :Parameters:
                `x` : int
                    Distance in pixels from the left edge of the window.
                `y` : int
                    Distance in pixels from the bottom edge of the window.
                `dx` : int
                    Relative X position from the previous mouse position.
                `dy` : int
                    Relative Y position from the previous mouse position.
                `buttons` : int
                    Bitwise combination of the mouse buttons currently pressed.
                `modifiers` : int
                    Bitwise combination of any keyboard modifiers currently
                    active.

            :event:
            """

        def on_mouse_press(
            self, x: int, y: int, button: int, modifiers: int, window: ClientWindow
        ) -> None | bool:
            """A mouse button was pressed (and held down).

            :Parameters:
                `x` : int
                    Distance in pixels from the left edge of the window.
                `y` : int
                    Distance in pixels from the bottom edge of the window.
                `button` : int
                    The mouse button that was pressed.
                `modifiers` : int
                    Bitwise combination of any keyboard modifiers currently
                    active.

            :event:
            """

        def on_mouse_release(
            self, x: int, y: int, button: int, modifiers: int, window: ClientWindow
        ) -> None | bool:
            """A mouse button was released.

            :Parameters:
                `x` : int
                    Distance in pixels from the left edge of the window.
                `y` : int
                    Distance in pixels from the bottom edge of the window.
                `button` : int
                    The mouse button that was released.
                `modifiers` : int
                    Bitwise combination of any keyboard modifiers currently
                    active.

            :event:
            """

        def on_mouse_scroll(
            self, x: int, y: int, scroll_x: float, scroll_y: float, window: ClientWindow
        ) -> None | bool:
            """The mouse wheel was scrolled.

            Note that most mice have only a vertical scroll wheel, so
            `scroll_x` is usually 0.  An exception to this is the Apple Mighty
            Mouse, which has a mouse ball in place of the wheel which allows
            both `scroll_x` and `scroll_y` movement.

            :Parameters:
                `x` : int
                    Distance in pixels from the left edge of the window.
                `y` : int
                    Distance in pixels from the bottom edge of the window.
                `scroll_x` : float
                    Amount of movement on the horizontal axis.
                `scroll_y` : float
                    Amount of movement on the vertical axis.

            :event:
            """

        def on_mouse_enter(self, x: int, y: int, window: ClientWindow) -> None | bool:
            """The mouse was moved into the window.

            This event will not be triggered if the mouse is currently being
            dragged.

            :Parameters:
                `x` : int
                    Distance in pixels from the left edge of the window.
                `y` : int
                    Distance in pixels from the bottom edge of the window.

            :event:
            """

        def on_mouse_leave(self, x: int, y: int, window: ClientWindow) -> None | bool:
            """The mouse was moved outside of the window.

            This event will not be triggered if the mouse is currently being
            dragged.  Note that the coordinates of the mouse pointer will be
            outside of the window rectangle.

            :Parameters:
                `x` : int
                    Distance in pixels from the left edge of the window.
                `y` : int
                    Distance in pixels from the bottom edge of the window.

            :event:
            """

        def on_move(self, x: int, y: int, window: ClientWindow) -> None:
            """The window was moved.

            :Parameters:
                `x` : int
                    Distance from the left edge of the screen to the left edge
                    of the window.
                `y` : int
                    Distance from the top edge of the screen to the top edge of
                    the window.  Note that this is one of few methods in pyglet
                    which use a Y-down coordinate system.

            :event:
            """

        def on_refresh(self, dt, window: ClientWindow) -> None:
            """The window contents must be redrawn.

            The `EventLoop` will dispatch this event when the window
            should be redrawn.

            The window will already have the GL context, so there is no
            need to call `switch_to`.  The window's `flip` method will
            be called after this event, so your event handler should not.

            You should make no assumptions about the window contents when
            this event is triggered; a resize or expose event may have
            invalidated the framebuffer since the last time it was drawn.

            .. versionadded:: 2.0

            :event:
            """

        def on_resize(self, width: int, height: int, window: ClientWindow):
            """The window was resized.

            The window will have the GL context when this event is dispatched;
            there is no need to call `switch_to` in this handler.

            :Parameters:
                `width` : int
                    The new width of the window, in pixels.
                `height` : int
                    The new height of the window, in pixels.

            :event:
            """

        def on_show(self, window: ClientWindow):
            """The window was shown.

            This event is triggered when a window is restored after being
            minimised, hidden, or after being displayed for the first time.

            :event:
            """

        def on_text(self, text: str, window: ClientWindow):
            """The user input some text.

            Typically this is called after :py:meth:`~pyglet.window.Window.on_key_press` and before
            :py:meth:`~pyglet.window.Window.on_key_release`, but may also be called multiple times if the key
            is held down (key repeating); or called without key presses if
            another input method was used (e.g., a pen input).

            You should always use this method for interpreting text, as the
            key symbols often have complex mappings to their unicode
            representation which this event takes care of.

            :Parameters:
                `text` : unicode
                    The text entered by the user.

            :event:
            """

        def on_text_motion(self, motion: int, window: ClientWindow):
            """The user moved the text input cursor.

            Typically this is called after :py:meth:`~pyglet.window.Window.on_key_press`
            and before :py:meth:`~pyglet.window.Window.on_key_release`, but may also be
            called multiple times if the key is help down (key repeating).

            You should always use this method for moving the text input cursor
            (caret), as different platforms have different default keyboard
            mappings, and key repeats are handled correctly.

            The values that `motion` can take are defined in
            :py:mod:`pyglet.window.key`:

            * MOTION_UP
            * MOTION_RIGHT
            * MOTION_DOWN
            * MOTION_LEFT
            * MOTION_NEXT_WORD
            * MOTION_PREVIOUS_WORD
            * MOTION_BEGINNING_OF_LINE
            * MOTION_END_OF_LINE
            * MOTION_NEXT_PAGE
            * MOTION_PREVIOUS_PAGE
            * MOTION_BEGINNING_OF_FILE
            * MOTION_END_OF_FILE
            * MOTION_BACKSPACE
            * MOTION_DELETE

            :Parameters:
                `motion` : int
                    The direction of motion; see remarks.

            :event:
            """

        def on_text_motion_select(self, motion: int, window: ClientWindow):
            """The user moved the text input cursor while extending the
            selection.

            Typically this is called after :py:meth:`~pyglet.window.Window.on_key_press`
            and before :py:meth:`~pyglet.window.Window.on_key_release`, but may also be
            called multiple times if the key is help down (key repeating).

            You should always use this method for responding to text selection
            events rather than the raw :py:meth:`~pyglet.window.Window.on_key_press`, as
            different platforms have different default keyboard mappings, and key repeats
            are handled correctly.

            The values that `motion` can take are defined in :py:mod:`pyglet.window.key`:

            * MOTION_UP
            * MOTION_RIGHT
            * MOTION_DOWN
            * MOTION_LEFT
            * MOTION_NEXT_WORD
            * MOTION_PREVIOUS_WORD
            * MOTION_BEGINNING_OF_LINE
            * MOTION_END_OF_LINE
            * MOTION_NEXT_PAGE
            * MOTION_PREVIOUS_PAGE
            * MOTION_BEGINNING_OF_FILE
            * MOTION_END_OF_FILE

            :Parameters:
                `motion` : int
                    The direction of selection motion; see remarks.

            :event:
            """


BaseScreen.register_event_type("on_key_press")
BaseScreen.register_event_type("on_key_release")
BaseScreen.register_event_type("on_text")
BaseScreen.register_event_type("on_text_motion")
BaseScreen.register_event_type("on_text_motion_select")
BaseScreen.register_event_type("on_mouse_motion")
BaseScreen.register_event_type("on_mouse_drag")
BaseScreen.register_event_type("on_mouse_press")
BaseScreen.register_event_type("on_mouse_release")
BaseScreen.register_event_type("on_mouse_scroll")
BaseScreen.register_event_type("on_mouse_enter")
BaseScreen.register_event_type("on_mouse_leave")
BaseScreen.register_event_type("on_close")
BaseScreen.register_event_type("on_expose")
BaseScreen.register_event_type("on_resize")
BaseScreen.register_event_type("on_move")
BaseScreen.register_event_type("on_activate")
BaseScreen.register_event_type("on_deactivate")
BaseScreen.register_event_type("on_show")
BaseScreen.register_event_type("on_hide")
BaseScreen.register_event_type("on_context_lost")
BaseScreen.register_event_type("on_context_state_lost")
BaseScreen.register_event_type("on_file_drop")
BaseScreen.register_event_type("on_draw")
BaseScreen.register_event_type("on_refresh")
