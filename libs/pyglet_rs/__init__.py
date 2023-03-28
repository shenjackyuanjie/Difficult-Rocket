#  -------------------------------
#  Difficult Rocket
#  Copyright © 2020-2023 by shenjackyuanjie 3695888@qq.com
#  All rights reserved
#  -------------------------------

"""
from .lib import (get_version_str)

from .lib import (Sprite_rs,
                  Vector2_rs, Vector3_rs, Vector4_rs,
                  Matrix3_rs, Matrix4_rs)
"""
from .lib import *

from typing import TYPE_CHECKING

__version__ = get_version_str()
__all__ = ['patch_sprite', 'patch_vector', 'patch_matrix', 'patch_all',
           'Sprite_rs',
           'Vector2_rs', 'Vector3_rs', 'Vector4_rs',
           'Matrix3_rs', 'Matrix4_rs']

if TYPE_CHECKING:
    from pyglet.event import EventDispatcher

    def get_version_str() -> str: ...


    class Sprite_rs(EventDispatcher): ...

    class Vector2_rs: ...
    class Vector3_rs: ...
    class Vector4_rs: ...

    class Matrix3_rs: ...
    class Matrix4_rs: ...


def patch_sprite():
    from pyglet import sprite
    sprite.Sprite = Sprite_rs


def patch_vector():
    from pyglet import math
    math.Vector2 = Vector2_rs
    math.Vector3 = Vector3_rs
    math.Vector4 = Vector4_rs


def patch_matrix():
    from pyglet import math
    math.Matrix3 = Matrix3_rs
    math.Matrix4 = Matrix4_rs


def patch_all():
    patch_sprite()
    patch_vector()
    patch_matrix()
