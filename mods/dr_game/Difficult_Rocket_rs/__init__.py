#  -------------------------------
#  Difficult Rocket
#  Copyright © 2020-2023 by shenjackyuanjie 3695888@qq.com
#  All rights reserved
#  -------------------------------

from .lib import *

from typing import TYPE_CHECKING, Dict, Tuple, Optional, List

if TYPE_CHECKING:
    def test_call(py_obj) -> bool:
        """ 这里展示的代码实际上就是实际的等效实现 """
        py_obj.draw()
        return True


    def get_version_str() -> str:
        """
        获取版本号
        :return: 版本号
        """


    def part_list_read_test(file_name: Optional[str] = "./assets/builtin/PartList.xml") -> None:
        """
        PartList 读取测试
        :param file_name:
        """


    def read_ship_test(path: Optional[str] = "./assets/builtin/dock1.xml") -> None:
        """
        飞船存档读取测试
        :param path:
        :return:
        """


    def map_ptype_textures(part_type: str) -> str:
        """
        获取零件的贴图 (写死的)
        :param part_type:
        :return:
        """


    class SR1PartType_rs:  # NOQA
        """
        用于从 rust 中读取 SR1PartType
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


    class SR1PartList_rs:  # NOQA
        """ 用于从 rust 中读取 SR1PartList """

        def __init__(self, file_name: Optional[str] = "./assets/builtin/PartList.xml",
                     list_name: Optional[str] = 'NewPartList'): ...

        def as_dict(self) -> Dict[str, SR1PartType_rs]: ...

        def get_part_type(self, name: str) -> SR1PartType_rs: ...


    class SR1PartData_rs:  # NOQA
        """
        用于从 rust 中读取 SR1PartData (其实好像也没啥用哈)
        """

        @property
        def id(self) -> int: ...

        @property
        def part_type_id(self) -> str: ...

        @property
        def pos(self) -> Tuple[float, float]: ...

        @property
        def x(self) -> float: ...

        @property
        def y(self) -> float: ...

        @property
        def activate(self) -> bool: ...

        @property
        def angle(self) -> float: ...

        @property
        def angle_r(self) -> float: ...

        @property
        def angle_v(self) -> float: ...

        @property
        def explode(self) -> bool: ...

        @property
        def flip_x(self) -> bool: ...

        @property
        def flip_y(self) -> bool: ...


    class SaveStatus_rs:  # NOQA
        def __init__(self, save_default: Optional[bool] = False) -> None: ...


    class SR1Ship_rs:  # NOQA
        """ 用于高效且省内存的读取 SR1Ship """

        def __init__(self,
                     file_path: Optional[str] = './assets/builtin/dock1.xml',
                     part_list: Optional[SR1PartList_rs] = None,
                     ship_name: Optional[str] = 'NewShip'):
            """
            读取 SR1Ship
            :raise ValueError: 读取失败
            :param file_path:
            :param part_list:
            :param ship_name:
            """

        @property
        def name(self) -> str: ...

        @property
        def description(self) -> str: ...

        @property
        def lift_off(self) -> bool: ...

        @property
        def touch_ground(self) -> bool: ...

        @property
        def mass(self) -> float:
            """ 获取整搜船的质量 """

        @property
        def img_pos(self) -> Tuple[int, int, int, int]:
            """ -x -y +x +y  左下右上 """

        @property
        def connection(self) -> List[Tuple[int, int, int, int]]:
            """获取所有连接信息"""

        def get_part_box(self, part_id: int) -> Optional[Tuple[Tuple[int, int], Tuple[int, int]]]:
            """获取所有零件的盒子"""

        def as_list(self) -> List[Tuple[SR1PartType_rs, SR1PartData_rs]]:
            """用于返回一个包含所有已连接零件的列表"""

        def as_dict(self) -> Dict[int, List[Tuple[SR1PartType_rs, SR1PartData_rs]]]:
            """用于返回一个包含所有已连接零件的字典"""

        def save(self, file_path: str, save_status: Optional[SaveStatus_rs] = None) -> None: ...


    class Console_rs:  # NOQA
        def __init__(self) -> None: ...

        def start(self) -> None: ...

        def stop(self) -> bool: ...

        def get_command(self) -> Optional[str]: ...

        def new_command(self) -> bool: ...
