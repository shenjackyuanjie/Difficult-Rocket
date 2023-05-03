#  -------------------------------
#  Difficult Rocket
#  Copyright © 2020-2023 by shenjackyuanjie 3695888@qq.com
#  All rights reserved
#  -------------------------------

"""
writen by shenjackyuanjie
mail:   3695888@qq.com
github: @shenjackyuanjie
gitee:  @shenjackyuanjie
"""

import os
import sys
import time
import logging
import importlib
import importlib.util
import logging.config
import multiprocessing

from io import StringIO
from pathlib import Path
from typing import TYPE_CHECKING

if __name__ == '__main__':  # been start will not run this
    sys.path.append('/bin/libs')
    sys.path.append('/bin')

from Difficult_Rocket import client, server, DR_option, DR_runtime
if TYPE_CHECKING:
    from Difficult_Rocket.api.mod import ModInfo
from Difficult_Rocket.crash import write_info_to_cache
from Difficult_Rocket.utils import tools
from Difficult_Rocket.utils.translate import tr


class Game:
    def __init__(self):
        # basic config
        self.on_python_v_info = sys.version_info
        self.on_python_v = sys.version.split(' ')[0]
        self.start_time = time.strftime('%Y-%m-%d %H-%M-%S', time.gmtime(time.time()))
        # lang_config
        self.language = tools.load_file('configs/main.toml', 'runtime')['language']
        DR_option.language = self.language
        # logging config
        log_config = tools.load_file('configs/logger.toml')
        file_name = log_config['handlers']['file']['filename']
        del log_config['handlers']['file']['datefmt']
        log_config['handlers']['file']['filename'] = f'logs/{file_name.format(self.start_time)}'
        try:
            logging.config.dictConfig(log_config)
            self.logger = logging.getLogger('main')
        except ValueError:  # it should be no 'logs/' folder
            os.mkdir('logs')
            logging.config.dictConfig(log_config)
            self.logger = logging.getLogger('main')
            self.logger.info(tr().main.logger.mkdir())
        self.logger.info(tr().language_set_to())
        self.logger.info(tr().main.logger.created())
        # version check
        self.log_env()
        self.python_version_check()
        self.loaded_mods = []
        # self.client = client.Client
        # self.server = server.Server
        self.setup()
        
    def log_env(self) -> None:
        cache_steam = StringIO()
        write_info_to_cache(cache_steam)
        text = cache_steam.getvalue()
        self.logger.info(text)

    def load_mods(self) -> None:
        mods = []
        mod_path = Path(DR_runtime.mod_path)
        if not mod_path.exists():
            self.logger.info(tr().main.mod.find.faild.no_mod_folder())
            return
        # 寻找有效 mod
        paths = mod_path.iterdir()
        sys.path.append(DR_runtime.mod_path)
        for mod_path in paths:
            try:
                if mod_path.name == '__pycache__':
                    continue
                self.logger.info(tr().main.mod.find.start().format(mod_path))
                if mod_path.is_dir():
                    if importlib.util.find_spec(mod_path.name) is not None:
                        mods.append(mod_path.name)
                    else:
                        self.logger.warning(tr().main.mod.load.faild.info().format(mod_path.name, tr().main.mod.find.faild.no_spec()))
                elif mod_path.suffix in ('.pyz', '.zip', '.pyd', '.py'):
                    if importlib.util.find_spec(mod_path.name) is not None:
                        mods.append(mod_path.name)
            except ImportError as e:
                self.logger.warning(tr().main.mod.find.faild().format(mod_path, e))
        self.logger.info(tr().main.mod.find.done())
        # 加载有效 mod
        module = []
        for mod in mods:
            try:
                self.logger.info(tr().main.mod.load.start().format(mod))
                mod_module = importlib.import_module(mod)
                if not hasattr(mod_module, "mod_class"):
                    self.logger.warning(tr().main.mod.load.faild.info().format(mod, tr().main.mod.load.faild.no_mod_class()))
                    del mod_module  # 释放内存
                    continue
                mod_class: type(ModInfo) = mod_module.mod_class
                mod_class = mod_class()
                module.append(mod_class)
                self.logger.info(tr().main.mod.load.info().format(mod_class.mod_id, mod_class.version))
            except ImportError as e:
                self.logger.warning(tr().main.mod.load.faild().format(mod, e))
        self.logger.info(tr().main.mod.load.done())
        self.loaded_mods = module
        mod_list = []
        for mod in module:
            mod_list.append((mod.mod_id, mod.version))
        # 调用 on_load
        self.dispatch_event('on_load', game=self)
        DR_runtime.DR_Mod_List = mod_list

    def dispatch_event(self, event_name: str, *args, **kwargs) -> None:
        for mod in self.loaded_mods:
            if hasattr(mod, event_name):
                try:
                    getattr(mod, event_name)(*args, **kwargs)
                except Exception as e:
                    self.logger.error(tr().main.mod.event.error().format(event_name, e, mod.mod_id))

    def setup(self) -> None:
        self.load_mods()
        self.client = client.Client(game=self, net_mode='local')
        self.server = server.Server(net_mode='local')

    def python_version_check(self) -> None:  # best 3.8+ and write at 3.8.10
        self.logger.info(f"{tr().main.version.now_on()} {self.on_python_v}")
        if self.on_python_v_info[0] == 2:
            self.logger.critical(tr().main.version.need3p())
            raise SystemError(tr().main.version.need3p())
        elif self.on_python_v_info[1] < 8:
            warning = tools.name_handler(tr.main.version.best38p())
            self.logger.warning(warning)

    # @new_thread('main')
    def _start(self):
        self.server.run()
        if DR_option.use_multiprocess:
            try:
                game_process = multiprocessing.Process(target=self.client.start, name='pyglet app')
                game_process.start()
                game_process.join()
            except Exception:
                return -1
            else:
                return 1
        else:
            self.client.start()

    def start(self) -> None:
        self._start()
