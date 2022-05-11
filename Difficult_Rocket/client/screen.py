#  -------------------------------
#  Difficult Rocket
#  Copyright © 2021-2022 by shenjackyuanjie
#  All rights reserved
#  -------------------------------

import ctypes

from Difficult_Rocket.client import ClientWindow


class BaseScreen:
    def __init__(self, main_window: ClientWindow):
        self.main_window_pointer = ctypes.pointer(main_window)

    def update(self, tick: float):
        pass

    def create_command_tree(self):
        pass


class DRScreen(BaseScreen):
    def __init__(self, main_window: ClientWindow):
        super().__init__(main_window)
