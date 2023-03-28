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

from typing import TYPE_CHECKING, Union

# noinspection PyUnresolvedReferences
__version__ = get_version_str()
__all__ = ['patch_sprite', 'patch_vector', 'patch_matrix', 'patch_all',
           'Sprite_rs',
           'Vector2_rs', 'Vector3_rs', 'Vector4_rs',
           'Matrix3_rs', 'Matrix4_rs']

if TYPE_CHECKING:
    from pyglet.event import EventDispatcher

    Number = Union[int, float]


    def get_version_str() -> str: ...


    class Sprite_rs(EventDispatcher): ...


    class Vector2_rs:
        def __init__(self, x: Number, y: Number): ...
        def __add__(self, other: "Vector2_rs") -> "Vector2_rs": ...
        def __sub__(self, other: "Vector2_rs") -> "Vector2_rs": ...
        def __mul__(self, other: "Vector2_rs") -> "Vector2_rs": ...
        def __truediv__(self, other: "Vector2_rs") -> "Vector2_rs": ...
        def __floordiv__(self, other: "Vector2_rs") -> "Vector2_rs": ...
        def __repr__(self) -> str: ...


    class Vector3_rs:
        def __init__(self, x: Number, y: Number, z: Number): ...
        def __add__(self, other: "Vector3_rs") -> "Vector3_rs": ...
        def __sub__(self, other: "Vector3_rs") -> "Vector3_rs": ...
        def __mul__(self, other: "Vector3_rs") -> "Vector3_rs": ...
        def __truediv__(self, other: "Vector3_rs") -> "Vector3_rs": ...
        def __floordiv__(self, other: "Vector3_rs") -> "Vector3_rs": ...
        def __repr__(self) -> str: ...


    class Vector4_rs:
        def __init__(self, x: Number, y: Number, z: Number, w: Number): ...
        def __add__(self, other: "Vector4_rs") -> "Vector4_rs": ...
        def __sub__(self, other: "Vector4_rs") -> "Vector4_rs": ...
        def __mul__(self, other: "Vector4_rs") -> "Vector4_rs": ...
        def __truediv__(self, other: "Vector4_rs") -> "Vector4_rs": ...
        def __floordiv__(self, other: "Vector4_rs") -> "Vector4_rs": ...
        def __repr__(self) -> str: ...


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
