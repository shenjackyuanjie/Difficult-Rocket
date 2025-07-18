#  -------------------------------
#  Difficult Rocket
#  Copyright © 2020-2023 by shenjackyuanjie 3695888@qq.com
#  All rights reserved
#  -------------------------------

from __future__ import annotations

from .lib import *  # noqa: F403

from typing import TYPE_CHECKING, Dict, Tuple, Optional, List

if TYPE_CHECKING:
    IdType = int
    RawConnectionData = Tuple[int, int, IdType, IdType]

    def assert_ship(path: str) -> bool:
        """
        检查飞船存档是否可用
        :param path: 飞船存档路径
        :return: 是否可用
        """
        ...

    def get_version_str() -> str:
        """
        获取版本号
        :return: 版本号
        """
        ...

    def part_list_read_test(
        file_name: str | None = "./assets/builtin/PartList.xml"
    ) -> None:
        """
        PartList 读取测试
        :param file_name:
        """

    def read_ship_test(path: str | None = "./assets/builtin/dock1.xml") -> None:
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
        ...

    def opengl_render(width: int, height: int) -> DRglContent | None:
        """
        直接使用 opengl 进行的渲染覆盖
        """

    class DRglContent:
        """
        我投降, 手撸 OpenGL 了
        """
        def on_draw(self) -> None:
            ...

        def on_resize(self, width: int, height: int) -> None:
            ...

    def set_progress_value(all: int, complete: int) -> None:
        """
        Windows下设置当前窗口任务栏的进度条
        """

    def render_hack() -> WgpuRender | None:
        """
        进行一些 rust 方面的 渲染覆盖, 报错则返回 None
        """
        ...

    class WgpuRender:
        """
        一些很神奇的 wgpu 渲染
        用于在必要的时候跳过 pyglet 直接在 rust 中渲染
        目前 Windows only
        """
        def on_draw(self, clear: bool) -> None:
            ...

        def on_resize(self, width: int, height: int) -> None:
            ...

    class SR1PartType_rs:  # NOQA
        """
        用于从 rust 中读取 SR1PartType
        不能从 Python 端创建
        自带一些可从 Python 端读取的属性 (实际上就是一个接口)
        """

        @property
        def name(self) -> str:
            """零件的名字"""
            ...

        @property
        def description(self) -> str:
            """零件的描述"""
            ...

        @property
        def sprite(self) -> str:
            """零件的贴图"""
            ...

        @property
        def mass(self) -> float:
            """零件的质量"""
            ...

        @property
        def width(self) -> int:
            """零件的宽度"""
            ...

        @property
        def height(self) -> int:
            """零件的高度"""
            ...

        @property
        def friction(self) -> float:
            """零件的摩擦系数"""
            ...

        @property
        def hidden(self) -> bool:
            """零件是否隐藏"""
            ...

        @property
        def type(self):
            """零件的类型"""

    class SR1PartList_rs:  # NOQA
        """用于从 rust 中读取 SR1PartList"""

        def __init__(
            self,
            file_name: str | None = "./assets/builtin/PartList.xml",
            list_name: str | None = "NewPartList",
        ):
            ...

        def as_dict(self) -> dict[str, SR1PartType_rs]:
            ...

        def get_part_type(self, name: str) -> SR1PartType_rs:
            ...

    class SR1PartData_rs:  # NOQA
        """
        用于从 rust 中读取 SR1PartData (其实好像也没啥用哈)
        """

        @property
        def id(self) -> int:
            ...

        @property
        def part_type_id(self) -> str:
            ...

        @property
        def pos(self) -> tuple[float, float]:
            ...

        @property
        def x(self) -> float:
            ...

        @property
        def y(self) -> float:
            ...

        @property
        def activate(self) -> bool:
            ...

        @property
        def angle(self) -> float:
            ...

        @property
        def angle_r(self) -> float:
            ...

        @property
        def angle_v(self) -> float:
            ...

        @property
        def explode(self) -> bool:
            ...

        @property
        def flip_x(self) -> bool:
            ...

        @property
        def flip_y(self) -> bool:
            ...

        def get_part_box_by_type(
            self, part_type: SR1PartType_rs
        ) -> tuple[tuple[float, float], tuple[float, float]]:
            """
            当你同时已知一个部件的数据和类型的时候
            为啥不直接获取呢
            自: 0.3.6
            """
            ...

    class SaveStatus_rs:  # NOQA
        def __init__(self, save_default: Optional[bool] = False) -> None:
            ...

    class SR1Connection_rs:  # NOQA
        """用于存储一堆连接的信息
        同时提供了一些好用的 API
        至少总比你在那里吭哧吭哧在 Python 里搜快
        pub datas: Vec<Connection>"""

        def search_connection_by_parent(
            self, parent_id: IdType
        ) -> List[RawConnectionData]:
            """通过父节点搜索连接"""
            ...

        def search_connection_by_child(self, child_id: IdType) -> List[RawConnectionData]:
            """通过子节点搜索连接"""
            ...

        def search_connection_by_id(self, any_id: IdType) -> List[RawConnectionData]:
            """通过父子中任意一个 id 搜索连接"""
            ...

        def search_by_both_id(
            self, parent_id: IdType, child_id: IdType
        ) -> List[RawConnectionData]:
            """通过父子双方 id 获取连接

            保险起见, 我还是返回一个 Vec

            万一真有 双/多 连接呢"""
            ...

        def get_raw_data(self) -> List[RawConnectionData]:
            """获取原始数据

            万一你确实需要吭哧吭哧去处理原始数据呢"""
            ...

    class SR1Ship_rs:  # NOQA
        """用于高效且省内存的读取 SR1Ship"""

        def __init__(
            self,
            file_path: Optional[str] = "./assets/builtin/dock1.xml",
            part_list: Optional[SR1PartList_rs] = None,
            ship_name: Optional[str] = "NewShip",
        ):
            """
            读取 SR1Ship
            :raise ValueError: 读取失败
            :param file_path:
            :param part_list:
            :param ship_name:
            """

        @property
        def name(self) -> str:
            ...

        @property
        def description(self) -> str:
            ...

        @property
        def lift_off(self) -> bool:
            ...

        @property
        def touch_ground(self) -> bool:
            ...

        @property
        def mass(self) -> float:
            """获取整艘船的质量"""
            ...

        @property
        def img_pos(self) -> Tuple[int, int, int, int]:
            """-x -y +x +y  左下右上"""
            ...

        def get_part_box(
            self, part_id: IdType
        ) -> Optional[Tuple[Tuple[int, int], Tuple[int, int]]]:
            """获取所有零件的盒子"""

        def as_list(self) -> List[Tuple[SR1PartType_rs, SR1PartData_rs]]:
            """用于返回一个包含所有已连接零件的列表"""
            ...

        def as_dict(self) -> Dict[int, List[Tuple[SR1PartType_rs, SR1PartData_rs]]]:
            """用于返回一个包含所有已连接零件的字典"""
            ...

        def save(
            self, file_path: str, save_status: Optional[SaveStatus_rs] = None
        ) -> None:
            ...

        def connections(self) -> SR1Connection_rs:
            """获取所有连接"""
            ...

        def disconnected_parts(
            self
        ) -> List[Tuple[List[Tuple[SR1PartType_rs, SR1PartData_rs]], SR1Connection_rs]]:
            """获取所有未连接的零件"""
            ...

        def find_part_by_id(self, part_id: IdType) -> List[SR1PartData_rs]:
            """
            通过 id 获取零件
            当然, 支持重叠 ID
            自: 0.3.6
            """
            ...

    class Console_rs:  # NOQA
        def __init__(self) -> None:
            ...

        def start(self) -> None:
            ...

        def stop(self) -> bool:
            ...

        def get_command(self) -> Optional[str]:
            ...

        def new_command(self) -> bool:
            ...
