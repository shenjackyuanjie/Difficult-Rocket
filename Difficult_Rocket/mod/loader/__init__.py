#  -------------------------------
#  Difficult Rocket
#  Copyright © 2020-2023 by shenjackyuanjie 3695888@qq.com
#  All rights reserved
#  -------------------------------

import sys
import time
import traceback
import importlib
from pathlib import Path
from typing import List, Dict, Optional, TypeVar

from Difficult_Rocket.mod.api import ModInfo
from Difficult_Rocket.utils.translate import tr
from Difficult_Rocket.api.types import Options

from lib_not_dr.loggers import config

Game = TypeVar("Game")

logger = config.get_logger_from_old("mod_manager", "client")
ONE_FILE_SUFFIX = (".py", ".pyc", ".pyd")
PACKAGE_SUFFIX = (".pyz", ".zip", ".dr_mod")


def _add_path_to_sys(paths: List[Path]):
    for path in paths:
        if str(path) not in sys.path:
            sys.path.append(str(path))


class ModManager(Options):
    name = "Mod Manager"

    mods_path: List[Path] = [Path("./mods")]
    find_mod_paths: Dict[str, Path] = {}
    loaded_mod_modules: Dict[str, ModInfo] = {}

    def init(self, **kwargs) -> bool:
        self.logger = config.get_logger_from_old("mod_manager", "client")

    def get_mod_module(self, mod_name: str) -> Optional[ModInfo]:
        """
        获取指定 mod 的模块
        :param mod_name: mod 名
        :return:
        """
        for mod in self.loaded_mod_modules.values():
            if mod.name == mod_name:
                return mod
        return None

    def dispatch_event(self, event_name: str, *args, **kwargs):
        """
        分发事件
        :param event_name: 事件名
        :param args: 事件参数
        :param kwargs: 事件参数
        :return:
        """
        for mod in self.loaded_mod_modules.values():
            if hasattr(mod, event_name):
                try:
                    getattr(mod, event_name)(*args, **kwargs)
                except Exception as e:
                    self.logger.error(
                        tr()
                        .mod.event.error()
                        .format(mod, event_name, e, traceback.format_exc())
                    )

    def load_mod(self, mod_path: Path) -> Optional[type(ModInfo)]:
        """
        加载指定路径下的 mod
        :param mod_path: mod 的路径
        :return:
        """
        logger = self.logger.set_tag("load")
        if not mod_path.exists():
            logger.error(tr().mod.load.faild.not_exist().format(mod_path), tag="load")
            return None
        _add_path_to_sys([mod_path.parent])
        try:
            if mod_path.name == "__pycache__":
                # 忽略 __pycache__ 文件夹 (Python 编译文件)
                return None
            logger.info(tr().mod.load.loading().format(mod_path), tag="load")
            if (
                    mod_path.is_dir()
                    or mod_path.suffix in PACKAGE_SUFFIX
                    or mod_path.suffix in ONE_FILE_SUFFIX
            ):
                # 文件夹 mod
                loading_mod = importlib.import_module(mod_path.name)
                if not hasattr(loading_mod, "mod_class") or not issubclass(
                        loading_mod.mod_class, ModInfo
                ):
                    logger.warn(
                        tr().mod.load.faild.no_mod_class().format(mod_path), tag="load"
                    )
                    return None
                mod_class: type(ModInfo) = loading_mod.mod_class  # 获取 mod 类
                if mod_class.mod_id not in self.find_mod_paths:
                    self.find_mod_paths[mod_class.mod_id] = mod_path
                return mod_class
        except ImportError:
            logger.warn(
                tr().mod.load.faild.error().format(mod_path, traceback.format_exc()),
                tag="load",
            )
        return None

    def find_mods_in_path(
            self, extra_mods_path: Optional[List[Path]] = None
    ) -> List[Path]:
        """
        查找所有 mod 路径
        :return: 找到的 mod 的路径 (未校验)
        """
        find_path = self.mods_path + (
            extra_mods_path if extra_mods_path is not None else []
        )
        mods_path = []
        start_time = time.time()
        for path in find_path:
            if not path.exists():
                path.mkdir(parents=True)
                continue
            for mod in path.iterdir():
                if mod.name == "__pycache__":
                    # 忽略 __pycache__ 文件夹 (Python 编译文件)
                    continue
                if (
                        mod.is_dir()
                        or mod.suffix in PACKAGE_SUFFIX
                        or mod.suffix in ONE_FILE_SUFFIX
                ):
                    # 文件夹 mod
                    mods_path.append(mod)
        self.logger.info(
            tr().mod.finded().format(len(mods_path), time.time() - start_time), tag="find"
        )
        return mods_path

    def load_mods(
            self,
            extra_path: Optional[List[Path]] = None,
            extra_mod_path: Optional[List[Path]] = None,
    ) -> List[type(ModInfo)]:
        """
        加载所有 mod  (可提供额外的 mod 路径)
        :param extra_path: 额外的 mod 路径
        :param extra_mod_path: 额外的找到的 mod 路径
        :return:
        """
        find_path = self.mods_path + (extra_path if extra_path is not None else [])
        _add_path_to_sys(find_path)
        mods = []
        start_time = time.time()
        self.logger.info(tr().mod.load.start().format(find_path), tag="load")
        for path in find_path:
            if not path.exists():
                path.mkdir(parents=True)
                continue
            for mod in path.iterdir():
                if (cache := self.load_mod(mod)) is not None:
                    mods.append(cache)
        if extra_mod_path is not None:
            for path in extra_mod_path:
                if (cache := self.load_mod(path)) is not None:
                    mods.append(cache)
        self.logger.info(tr().mod.load.use_time().format(time.time() - start_time), tag="load")
        return mods

    def init_mods(self, mods: List[type(ModInfo)]):
        """
        加载 mod
        :param mods: 要加载的 mod 的 ModInfo 类
        :return:
        """
        start_time = time.time()
        for mod_class in mods:
            try:
                init_mod = mod_class()
                self.loaded_mod_modules[init_mod.mod_id] = init_mod
                self.logger.info(
                    tr().mod.init.success().format(init_mod, init_mod.version), tag="init"
                )
            except Exception as e:
                self.logger.error(
                    tr().mod.init.faild().format(mod_class, e, traceback.format_exc()),
                    tag="init",
                )
                continue
        self.logger.info(tr().mod.init.use_time().format(time.time() - start_time), tag="init")

    def unload_mod(self, mod_id: str, game: Game) -> Optional[ModInfo]:
        """
        卸载 mod
        :param mod_id: 要卸载的 mod id
        :param game: 游戏实例
        :return: 卸载的 mod 的 ModInfo 类
        """
        if (
                not (mod_class := self.loaded_mod_modules.get(mod_id))
                and (mod_class := self.get_mod_module(mod_id)) is None
        ):
            self.logger.warn(tr().mod.unload.faild.not_find().format(mod_id), tag="unload")
            return None
        try:
            mod_class.on_unload(game=game)
            self.loaded_mod_modules.pop(mod_class.mod_id)
            self.logger.info(tr().mod.unload.success().format(mod_id), tag="unload")
            return mod_class
        except Exception as e:
            self.logger.error(
                tr().mod.unload.faild.error().format(mod_id, e, traceback.format_exc()),
                tag="unload",
            )
        return None

    def reload_mod(self, mod_id: str, game: Game):
        """
        重载 mod
        :param mod_id:
        :param game:
        :return:
        """
        unload = self.unload_mod(mod_id, game)
        if unload is None:
            return
        mod_class: Optional[ModInfo] = None
        if unload.mod_id not in self.find_mod_paths:
            self.logger.warn(
                tr().mod.reload.faild.not_find().format(unload.mod_id), tag="reload"
            )
            paths = self.find_mods_in_path()
            for path in paths:
                mod_class = self.load_mod(path)
                if mod_class is not None and mod_class.mod_id == unload.mod_id:
                    self.init_mods([mod_class])
                    break
        else:
            mod_class = self.load_mod(self.find_mod_paths[unload.mod_id])
            if mod_class is not None:
                self.init_mods([mod_class])
        if mod_id in self.loaded_mod_modules and mod_class is not None:
            self.loaded_mod_modules[mod_id].on_load(game=game, old_self=mod_class)
            self.logger.info(tr().mod.reload.success().format(mod_id), tag="reload")
