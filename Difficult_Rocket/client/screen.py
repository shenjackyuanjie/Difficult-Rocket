#  -------------------------------
#  Difficult Rocket
#  Copyright © 2021-2022 by shenjackyuanjie 3695888@qq.com
#  All rights reserved
#  -------------------------------

# import ctypes

from Difficult_Rocket.client import ClientWindow
from Difficult_Rocket.command.tree import CommandTree


class BaseScreen:
    def __init__(self, main_window: ClientWindow):
        self.window_pointer = main_window
        self.command_tree = None
        self.create_command_tree()

    def update(self, tick: float):
        pass

    def create_command_tree(self):
        self.command_tree = CommandTree({})


class DRScreen(BaseScreen):
    def __init__(self, main_window: ClientWindow):
        super().__init__(main_window)


class DRDEBUGScreen(BaseScreen):
    def __init__(self, main_window: ClientWindow):
        super().__init__(main_window)
