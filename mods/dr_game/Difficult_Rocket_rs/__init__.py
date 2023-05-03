#  -------------------------------
#  Difficult Rocket
#  Copyright © 2020-2023 by shenjackyuanjie 3695888@qq.com
#  All rights reserved
#  -------------------------------

from .lib import *

from typing import TYPE_CHECKING, Dict, Tuple, Optional

if TYPE_CHECKING:

    from pyglet.window import Window


    def test_call(py_obj) -> bool: ...


    def get_version_str() -> str: ...


    def simluation() -> None: ...


    """ 用来测试 rust 的物理模拟能不能用 """


    def part_list_read_test(file_name: Optional[str] = "./configs/PartList.xml") -> None: ...

    def read_ship_test(path: Optional[str] = "./configs/dock1.xml") -> None: ...

    class Camera_rs:
        """ 用于闲的没事 用 rust 写一个 camera """

        def __new__(cls, window: Window,
                    zoom: float = 1.0,
                    dx: float = 1.0, dy: float = 1.0,
                    min_zoom: float = 1.0,
                    max_zoom: float = 1.0): ...

        @property
        def dx(self) -> float: ...
        @property
        def dy(self) -> float: ...
        @property
        def zoom(self) -> float: ...
        @property
        def position(self) -> Tuple[float, float]: ...
        @dx.setter
        def dx(self, value: float) -> None: ...
        @dy.setter
        def dy(self, value: float) -> None: ...
        @zoom.setter
        def zoom(self, value: float) -> None: ...

        def begin(self) -> None: ...

        def end(self) -> None: ...

        def __enter__(self, window) -> None: ...

        def __exit__(self, exc_type, exc_val, exc_tb) -> None: ...


    class CenterCamera_rs(Camera_rs):
        """ 用于依旧闲的没事 用 rust 写一个中央对齐的 camera """


    class PartFrame_rs:
        ...


    class SR1PartType_rs:
        """ 用于从 rust 中读取 SR1PartType
        不能从 Python 端创建"""
        @property
        def name(self) -> str: ...
        @property
        def mass(self) -> float: ...


    class SR1PartList_rs:
        """ 用于从 rust 中读取 SR1PartList """
        def __init__(self, file_name: Optional[str] = "./configs/PartList.xml",
                     list_name: Optional[str] = 'NewPartList'): ...

        def as_dict(self) -> Dict[str, SR1PartType_rs]: ...

        def get_part_type(self, name: str) -> SR1PartType_rs: ...

    class SR1Ship_rs:
        """ 用于高效且省内存的读取 SR1Ship """
        @property
        def name(self) -> str: ...
        @property
        def description(self) -> str: ...
        @property
        def lift_off(self) -> bool: ...
        @property
        def touch_ground(self) -> bool: ...
        @property
        def img_pos(self) -> Tuple[int, int, int, int]: ...
        """ -x -y +x +y  左下右上 """
