#  -------------------------------
#  Difficult Rocket
#  Copyright © 2020-2023 by shenjackyuanjie 3695888@qq.com
#  All rights reserved
#  -------------------------------

import sys
import time
import logging
import traceback
import importlib
from pathlib import Path
from typing import List, Dict, Optional

from Difficult_Rocket.mod.api import ModInfo
from Difficult_Rocket.utils.translate import tr
from Difficult_Rocket.api.types import Options, Version

logger = logging.getLogger('mod_manager')
ONE_FILE_SUFFIX = ('.py', '.pyc', '.pyd')
PACKAGE_SUFFIX = ('.pyz', '.zip', '.dr_mod')


class ModManager(Options):
    name = 'Mod Manager'

    mods_path: List[Path] = [Path('./mods')]
    loaded_mod_modules: Dict[str, ModInfo] = {}

    def dispatch_event(self, event_name: str, *args, **kwargs):
        """
        分发事件
        :param event_name:
        :param args:
        :param kwargs:
        :return:
        """
        for mod in self.loaded_mod_modules.values():
            if hasattr(mod, event_name):
                try:
                    getattr(mod, event_name)(*args, **kwargs)
                except Exception as e:
                    logger.error(tr().mod.event.error().format(mod, event_name, e, traceback.format_exc()))

    def load_mods(self, extra_path: Optional[List[Path]] = None) -> List[type(ModInfo)]:
        """
        加载所有 mod  (可提供额外的 mod 路径)
        :param extra_path: 额外的 mod 路径
        :return:
        """
        find_path = self.mods_path + (extra_path if extra_path is not None else [])
        sys.path += [str(path_) for path_ in find_path]
        mods = []
        start_time = time.time()
        logger.info(tr().mod.load.start().format(find_path))
        for path in find_path:
            if not path.exists():
                path.mkdir(parents=True)
                continue
            for mod in path.iterdir():
                try:
                    if mod.name == '__pycache__':
                        # 忽略 __pycache__ 文件夹 (Python 编译文件)
                        continue
                    logger.info(tr().mod.load.loading().format(mod))
                    if mod.is_dir() or mod.suffix in PACKAGE_SUFFIX or mod.suffix in ONE_FILE_SUFFIX:
                        # 文件夹 mod
                        loading_mod = importlib.import_module(mod.name)
                        if not hasattr(loading_mod, 'mod_class'):
                            logger.warning(tr().mod.load.faild.no_mod_class().format(mod))
                            continue
                        mod_class: type(ModInfo) = loading_mod.mod_class  # 获取 mod 类
                        mods.append(mod_class)
                except ImportError:
                    logger.warning(tr().mod.load.faild.error().format(mod))
        logger.info(tr().mod.load.use_time().format(time.time() - start_time))
        return mods

    def init_mods(self, mods: List[type(ModInfo)]):
        """
        加载 mod
        :param mods:
        :return:
        """
        start_time = time.time()
        for mod_class in mods:
            try:
                init_mod = mod_class()
                self.loaded_mod_modules[init_mod.name] = init_mod
                logger.info(tr().mod.init.success().format(init_mod, init_mod.version))
            except Exception as e:
                logger.error(tr().mod.init.faild().format(mod_class, e, traceback.format_exc()))
                continue
        logger.info(tr().mod.init.use_time().format(time.time() - start_time))
