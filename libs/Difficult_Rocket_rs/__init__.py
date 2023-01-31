#  -------------------------------
#  Difficult Rocket
#  Copyright © 2020-2023 by shenjackyuanjie 3695888@qq.com
#  All rights reserved
#  -------------------------------

from .lib import *

from typing import TYPE_CHECKING, Dict

if TYPE_CHECKING:
    from Difficult_Rocket.client.screen import BaseScreen
    from Difficult_Rocket.api.types.SR1 import SR1PartData
    from Difficult_Rocket.client.render.sr1_ship import SR1ShipRender, SR1ShipRender_Option

    from pyglet.window import Window

    def test_call(py_obj) -> bool: ...

    def get_version_str() -> str: ...

    class PartDatas:
        """ 用于在 PyObj 里塞一个浓眉大眼的 HashMap<uszie, SR1PartData>"""
        def __new__(cls, py_part_data: Dict[int, SR1PartData]) -> "PartDatas": ...

        def get_rust_pointer(self) -> int: ...

    def better_update_parts(render: SR1ShipRender,
                            option: SR1ShipRender_Option,
                            window: BaseScreen,
                            parts: PartDatas,
                            global_scale: float,
                            sr1_xml_scale: int) -> bool: ...

    class Camera_rs:
        """ 用于闲的没事 用 rust 写一个 camera """
        def __new__(cls, window: Window,
                    zoom: float = 1.0,
                    dx: float = 1.0, dy: float = 1.0,
                    min_zoom: float = 1.0,
                    max_zoom: float = 1.0): ...

        def start(self) -> None: ...

        def end(self) -> None: ...

        def __enter__(self, window) -> None: ...

        def __exit__(self, exc_type, exc_val, exc_tb) -> None: ...
