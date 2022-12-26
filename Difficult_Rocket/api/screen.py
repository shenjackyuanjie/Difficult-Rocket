#  -------------------------------
#  Difficult Rocket
#  Copyright © 2021-2022 by shenjackyuanjie 3695888@qq.com
#  All rights reserved
#  -------------------------------


import typing
from typing import List

# from pyglet.window import Window
from pyglet.event import EventDispatcher

# Difficult Rocket function
from Difficult_Rocket.command.api import CommandText

if typing.TYPE_CHECKING:
    from Difficult_Rocket.client import ClientWindow


class BaseScreen(EventDispatcher):
    """
    DR 的 页面API
    """

    def __init__(self, main_window: "ClientWindow"):
        super().__init__()
        self.window_pointer = main_window

    if typing.TYPE_CHECKING:
        def on_key_press(self, symbol: int, modifiers: int):
            """一个键盘按键被按下
            :param:
                `symbol` : int
                    按下按键的标识符
                `modifiers` : int
                    每一位(二进制)表示一个修饰键的启用情况
            """

        def on_key_release(self, symbol: int, modifiers: int):
            """一个键盘按键被松开
            :param:
                `symbol` : int
                    放下按键的标识符
                `modifiers` : int
                    每一位(二进制)表示一个修饰键的启用情况
            """

        def on_text(self, text: str):
            """用户输入了一个字符

            Typically this is called after :py:meth:`~pyglet.window.Window.on_key_press` and before
            :py:meth:`~pyglet.window.Window.on_key_release`, but may also be called multiple times if the key
            is held down (key repeating); or called without key presses if
            another input method was used (e.g., a pen input).

            You should always use this method for interpreting text, as the
            key symbols often have complex mappings to their unicode
            representation which this event takes care of.

            :param:
                `text` : unicode
                    用户输入的 unicode 编码的内容

            """

        def on_text_motion(self, motion: int):
            """The user moved the text input cursor.

            Typically this is called after :py:meth:`~pyglet.window.Window.on_key_press` and before
            :py:meth:`~pyglet.window.Window.on_key_release`, but may also be called multiple times if the key
            is help down (key repeating).

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

            :param:
                `motion` : int
                    The direction of motion; see remarks.

            """

        def on_text_motion_select(self, motion: int):
            """The user moved the text input cursor while extending the
            selection.

            Typically this is called after :py:meth:`~pyglet.window.Window.on_key_press` and before
            :py:meth:`~pyglet.window.Window.on_key_release`, but may also be called multiple times if the key
            is help down (key repeating).

            You should always use this method for responding to text selection
            events rather than the raw :py:meth:`~pyglet.window.Window.on_key_press`, as different platforms
            have different default keyboard mappings, and key repeats are
            handled correctly.

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

            :param:
                `motion` : int
                    The direction of selection motion; see remarks.

            """

        def on_mouse_motion(self, x: int, y: int, dx: int, dy: int):
            """The mouse was moved with no buttons held down.

            :param:
                `x` : int
                    Distance in pixels from the left edge of the window.
                `y` : int
                    Distance in pixels from the bottom edge of the window.
                `dx` : int
                    Relative X position from the previous mouse position.
                `dy` : int
                    Relative Y position from the previous mouse position.

            """

        def on_mouse_drag(self, x: int, y: int, dx: int, dy: int, buttons: int, modifiers: int):
            """The mouse was moved with one or more mouse buttons pressed.

            This event will continue to be fired even if the mouse leaves
            the window, so long as the drag buttons are continuously held down.

            :param:
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

            """

        def on_mouse_press(self, x: int, y: int, button: int, modifiers: int):
            """A mouse button was pressed (and held down).

            :param:
                `x` : int
                    Distance in pixels from the left edge of the window.
                `y` : int
                    Distance in pixels from the bottom edge of the window.
                `button` : int
                    The mouse button that was pressed.
                `modifiers` : int
                    Bitwise combination of any keyboard modifiers currently
                    active.

            """

        def on_mouse_release(self, x: int, y: int, button: int, modifiers: int):
            """A mouse button was released.

            :param:
                `x` : int
                    Distance in pixels from the left edge of the window.
                `y` : int
                    Distance in pixels from the bottom edge of the window.
                `button` : int
                    The mouse button that was released.
                `modifiers` : int
                    Bitwise combination of any keyboard modifiers currently
                    active.

            """

        def on_mouse_scroll(self, x: int, y: int, scroll_x: int, scroll_y: int):
            """The mouse wheel was scrolled.

            Note that most mice have only a vertical scroll wheel, so
            `scroll_x` is usually 0.  An exception to this is the Apple Mighty
            Mouse, which has a mouse ball in place of the wheel which allows
            both `scroll_x` and `scroll_y` movement.

            :param:
                `x` : int
                    Distance in pixels from the left edge of the window.
                `y` : int
                    Distance in pixels from the bottom edge of the window.
                `scroll_x` : float
                    Amount of movement on the horizontal axis.
                `scroll_y` : float
                    Amount of movement on the vertical axis.
            """

        def on_close(self):
            """The user attempted to close the window.

            This event can be triggered by clicking on the "X" control box in
            the window title bar, or by some other platform-dependent manner.

            The default handler sets `has_exit` to ``True``.  In pyglet 1.1, if
            `pyglet.app.event_loop` is being used, `close` is also called,
            closing the window immediately.
            """

        def on_mouse_enter(self, x: int, y: int):
            """The mouse was moved into the window.

            This event will not be triggered if the mouse is currently being
            dragged.

            :param:
                `x` : int
                    Distance in pixels from the left edge of the window.
                `y` : int
                    Distance in pixels from the bottom edge of the window.
            """

        def on_mouse_leave(self, x: int, y: int):
            """The mouse was moved outside of the window.

            This event will not be triggered if the mouse is currently being
            dragged.  Note that the coordinates of the mouse pointer will be
            outside of the window rectangle.

            :param:
                `x` : int
                    Distance in pixels from the left edge of the window.
                `y` : int
                    Distance in pixels from the bottom edge of the window.
            """

        def on_expose(self):
            """A portion of the window needs to be redrawn.

            This event is triggered when the window first appears, and any time
            the contents of the window is invalidated due to another window
            obscuring it.

            There is no way to determine which portion of the window needs
            redrawing.  Note that the use of this method is becoming
            increasingly uncommon, as newer window managers composite windows
            automatically and keep a backing store of the window contents.
            """

        def on_resize(self, width: int, height: int):
            """The window was resized.

            The window will have the GL context when this event is dispatched;
            there is no need to call `switch_to` in this handler.

            :param:
                `width` : int
                    The new width of the window, in pixels.
                `height` : int
                    The new height of the window, in pixels.
            """

        def on_move(self, x: int, y: int):
            """The window was moved.

            :param:
                `x` : int
                    Distance from the left edge of the screen to the left edge
                    of the window.
                `y` : int
                    Distance from the top edge of the screen to the top edge of
                    the window.  Note that this is one of few methods in pyglet
                    which use a Y-down coordinate system.
            """

        def on_activate(self):
            """The window was activated.

            This event can be triggered by clicking on the title bar, bringing
            it to the foreground; or by some platform-specific method.

            When a window is "active" it has the keyboard focus.
            """

        def on_deactivate(self):
            """The window was deactivated.

            This event can be triggered by clicking on another application
            window.  When a window is deactivated it no longer has the
            keyboard focus.
            """

        def on_show(self):
            """The window was shown.

            This event is triggered when a window is restored after being
            minimised, hidden, or after being displayed for the first time.
            """

        def on_hide(self):
            """The window was hidden.

            This event is triggered when a window is minimised
            or hidden by the user.
            """

        def on_context_lost(self):
            """The window's GL context was lost.

            When the context is lost no more GL methods can be called until it
            is recreated.  This is a rare event, triggered perhaps by the user
            switching to an incompatible video mode.  When it occurs, an
            application will need to reload all objects (display lists, texture
            objects, shaders) as well as restore the GL state.
            """

        def on_context_state_lost(self):
            """The state of the window's GL context was lost.

            pyglet may sometimes need to recreate the window's GL context if
            the window is moved to another video device, or between fullscreen
            or windowed mode.  In this case it will try to share the objects
            (display lists, texture objects, shaders) between the old and new
            contexts.  If this is possible, only the current state of the GL
            context is lost, and the application should simply restore state.
            """

        def on_file_drop(self, x: int, y: int, paths: List[str]):
            """File(s) were dropped into the window, will return the position of the cursor and
            a list of paths to the files that were dropped.
            """

        def on_draw(self):
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
            """

        def on_refresh(self):
            """The window contents must be redrawn.

            The `EventLoop` will dispatch this event when the window
            should be redrawn.

            The window will already have the GL context, so there is no
            need to call `switch_to`.  The window's `flip` method will
            be called after this event, so your event handler should not.

            You should make no assumptions about the window contents when
            this event is triggered; a resize or expose event may have
            invalidated the framebuffer since the last time it was drawn.

            """

        def on_command(self, command: CommandText):
            """

            :param command:
            :return:
            """

        def on_message(self, message: str):
            """

            :param message:
            :return:
            """


BaseScreen.register_event_type('on_key_press')
BaseScreen.register_event_type('on_key_release')
BaseScreen.register_event_type('on_text')
BaseScreen.register_event_type('on_text_motion')
BaseScreen.register_event_type('on_text_motion_select')
BaseScreen.register_event_type('on_mouse_motion')
BaseScreen.register_event_type('on_mouse_drag')
BaseScreen.register_event_type('on_mouse_press')
BaseScreen.register_event_type('on_mouse_release')
BaseScreen.register_event_type('on_mouse_scroll')
BaseScreen.register_event_type('on_mouse_enter')
BaseScreen.register_event_type('on_mouse_leave')
BaseScreen.register_event_type('on_close')
BaseScreen.register_event_type('on_expose')
BaseScreen.register_event_type('on_resize')
BaseScreen.register_event_type('on_move')
BaseScreen.register_event_type('on_activate')
BaseScreen.register_event_type('on_deactivate')
BaseScreen.register_event_type('on_show')
BaseScreen.register_event_type('on_hide')
BaseScreen.register_event_type('on_context_lost')
BaseScreen.register_event_type('on_context_state_lost')
BaseScreen.register_event_type('on_file_drop')
BaseScreen.register_event_type('on_draw')
BaseScreen.register_event_type('on_refresh')