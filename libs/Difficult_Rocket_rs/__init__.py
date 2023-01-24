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

    def test_call(py_obj) -> bool: ...

    def get_version_str() -> str: ...

    class PartDatas:
        """ 用于在 PyObj 里塞一个浓眉大眼的 HashMap<uszie, SR1PartData>"""
        def __new__(cls, py_part_data: Dict[int, SR1PartData]) -> "PartDatas": ...

        def get_rust_pointer(self) -> int: ...

    def better_update_parts(render: SR1ShipRender,
                            option: SR1ShipRender_Option,
                            window: BaseScreen,
                            parts: PartDatas) -> bool: ...


