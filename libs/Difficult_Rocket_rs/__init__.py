#  -------------------------------
#  Difficult Rocket
#  Copyright © 2020-2023 by shenjackyuanjie 3695888@qq.com
#  All rights reserved
#  -------------------------------

from .lib import *

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from Difficult_Rocket.client.screen import BaseScreen
    from Difficult_Rocket.client.render.sr1_ship import SR1ShipRender, SR1ShipRender_Option
    def sum_as_string(a: int, b: int) -> int: ...

    def for_x_in_range(a: int, b: int) -> None: ...

    def test_call(py_obj) -> bool: ...

    def better_update_parts(render: SR1ShipRender, option: SR1ShipRender_Option, window: BaseScreen) -> bool: ...

    class PartDatas:
        """ 用于在 PyObj 里塞一个浓眉大眼的 HashMap<uszie, SR1PartData>"""
        def __new__(cls, py_part_data) -> "PartDatas": ...

