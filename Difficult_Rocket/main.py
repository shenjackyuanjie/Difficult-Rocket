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

import multiprocessing

from typing import List, Optional, Dict

from Difficult_Rocket.api.types import Options
from Difficult_Rocket.mod.loader import ModManager
from Difficult_Rocket.utils.thread import new_thread
from Difficult_Rocket import client, server, DR_status

from lib_not_dr.loggers import config
from lib_not_dr.loggers.logger import Logger


class Console(Options):
    name = "python stdin console"

    running: bool = False
    caches: List[str] = []

    @new_thread("python console", daemon=True, log_thread=True)
    def main(self):
        while self.running:
            try:
                get_str = input(">>>")
            except (EOFError, KeyboardInterrupt):
                get_str = "stop"
            self.caches.append(get_str)
            if get_str == "stop":
                self.running = False
                break

    def start(self):
        self.running = True
        self.main()

    def stop(self):
        self.running = False

    def get_command(self) -> Optional[str]:
        return self.caches.pop(0) if self.caches else None

    def new_command(self) -> None:
        return None


class Game(Options):
    name = "MainGame"

    client: client.Client
    server: server.Server
    console: Console
    console_class: Console = Console

    main_config: Dict
    logger: Logger

    mod_manager: ModManager

    def dispatch_mod_event(self, event_name: str, *args, **kwargs) -> None:
        self.mod_manager.dispatch_event(event_name, *args, **kwargs)

    def init_mods(self) -> None:
        """验证/加载 mod"""
        self.mod_manager = ModManager()
        mod_class = self.mod_manager.load_mods()
        self.mod_manager.init_mods(mod_class)
        self.dispatch_mod_event("on_load", game=self)

    def init_console(self) -> None:
        self.console = self.console_class()
        self.console.start()

    def start(self):
        self.server.run()
        if DR_status.use_multiprocess:
            try:
                game_process = multiprocessing.Process(
                    target=self.client.start, name="pyglet app"
                )
                game_process.start()
                game_process.join()
            except Exception:
                return -1
            else:
                return 1
        else:
            self.client.start()

    def log_env(self) -> None:
        self.logger.info(f"\n{self.as_markdown()}")

    def setup(self) -> None:
        self.client = client.Client(game=self, net_mode="local")
        self.server = server.Server(net_mode="local")

    def init(self, **kwargs) -> bool:
        self.logger = config.get_logger("main")
        self.load_file()
        self.setup()
        self.log_env()
        return True

    def load_file(self) -> bool:
        """加载文件"""
        self.init_mods()
        self.init_console()
        return True
