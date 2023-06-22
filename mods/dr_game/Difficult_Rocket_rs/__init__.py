#  -------------------------------
#  Difficult Rocket
#  Copyright © 2020-2023 by shenjackyuanjie 3695888@qq.com
#  All rights reserved
#  -------------------------------

from .lib import *

from typing import TYPE_CHECKING, Dict, Tuple, Optional, List, Tuple

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
        不能从 Python 端创建
        自带一些可从 Python 端读取的属性 (实际上就是一个接口)
        """
        @property
        def name(self) -> str:
            """ 零件的名字 """
        @property
        def description(self) -> str:
            """ 零件的描述 """
        @property
        def mass(self) -> float:
            """ 零件的质量 """
        @property
        def width(self) -> int:
            """ 零件的宽度 """
        @property
        def height(self) -> int:
            """ 零件的高度 """
        @property
        def friction(self) -> float:
            """ 零件的摩擦系数 """
        @property
        def hidden(self) -> bool:
            """ 零件是否隐藏 """


    class SR1PartList_rs:
        """ 用于从 rust 中读取 SR1PartList """
        def __init__(self, file_name: Optional[str] = "./configs/PartList.xml",
                     list_name: Optional[str] = 'NewPartList'): ...

        def as_dict(self) -> Dict[str, SR1PartType_rs]: ...

        def get_part_type(self, name: str) -> SR1PartType_rs: ...

    class SR1PartData_rs:
        """ 用于从 rust 中读取 SR1PartData (其实好像也没啥用哈)
        """
        @property
        def part_type_id(self) -> str: ...
        @property
        def pos(self) -> Tuple[float, float]: ...
        @property
        def angle(self) -> float: ...
        @property
        def flip_x(self) -> bool: ...
        @property
        def flip_y(self) -> bool: ...

    class SR1Ship_rs:
        """ 用于高效且省内存的读取 SR1Ship """
        def __init__(self, file_path = './configs/dock1.xml', part_list = './configs/PartList.xml', ship_name = 'NewShip'): ...
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
        def get_part_box(self, part_id: int) -> Optional[Tuple[Tuple[int, int], Tuple[int, int]]]: ...
        def as_dict(self) -> Dict[int, List[Tuple[SR1PartType_rs, SR1PartData]]]: 
            """用于返回一个包含所有已连接零件的字典"""
        
    class Console_rs:
        def __init__(self) -> None: ...
        def start(self) -> None: ...
        def stop(self) -> bool: ...
        def get_command(self) -> Optional[str]: ...
        def new_command(self) -> bool: ...
