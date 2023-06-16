#  -------------------------------
#  Difficult Rocket
#  Copyright © 2020-2023 by shenjackyuanjie 3695888@qq.com
#  All rights reserved
#  -------------------------------

import logging
from pathlib import Path
from typing import List, Dict, Optional

from Difficult_Rocket.api.screen import BaseScreen
from Difficult_Rocket.api.types import Options, Version
from Difficult_Rocket.mod.api import ModInfo
# from Difficult_Rocket import DR_status, DR_runtime


class ModManager(Options):
    name = 'Mod Manager'
    logger: logging.Logger

    mods_path: List[Path] = [Path('./mods')]
    loaded_mod_modules: Dict[str, ModInfo] = {}

    def find_mods(self) -> List[Path]:
        """
        查找mods文件夹下的所有mod
        :return:
        """
        mods = []
        for path in self.mods_path:
            if not path.exists():
                path.mkdir(parents=True)
                continue
            for mod in path.iterdir():
                ...

    def init(self) -> None:
        self.logger = logging.getLogger('client')
        self.logger.name = 'mod_manager'
        self.logger.info('Mod Manager init')

