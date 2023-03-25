#  -------------------------------
#  Difficult Rocket
#  Copyright © 2020-2023 by shenjackyuanjie 3695888@qq.com
#  All rights reserved
#  -------------------------------

from .lib import *

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pyglet.event import EventDispatcher

    def get_version_str() -> str: ...


    class Sprite_rs(EventDispatcher):
        ...


def patch_sprite():
    from pyglet import sprite
    sprite.Sprite = Sprite_rs
