#  -------------------------------
#  Difficult Rocket Mod
#  Copyright © 2020-2023 by shenjackyuanjie 3695888@qq.com
#  All rights reserved
#  -------------------------------

import logging
import warnings
import traceback

from typing import Optional

from Difficult_Rocket import DR_status
from Difficult_Rocket.main import Game
from Difficult_Rocket.main import Console
from Difficult_Rocket.api.mod import ModInfo
from Difficult_Rocket.client import ClientWindow
from Difficult_Rocket.api.types import Options, Version

DR_rust_version = Version("0.2.11.0")  # DR_mod 的 Rust 编写部分的兼容版本

logger = logging.getLogger('client.dr_game')


class _DR_mod_runtime(Options):
    name = 'DR mod runtime'

    use_DR_rust: bool = True
    DR_rust_available: bool = False
    DR_rust_version: Version = DR_rust_version
    DR_rust_get_version: Optional[Version] = None

    def init(self) -> None:
        try:
            from .Difficult_Rocket_rs import get_version_str
            self.DR_rust_get_version = Version(get_version_str())
            self.DR_rust_available = True
            if self.DR_rust_get_version != self.DR_rust_version:
                relationship = 'larger' if self.DR_rust_version > self.DR_rust_version else 'smaller'
                warnings.warn(
                    f'DR_rust builtin version is {self.DR_rust_version} but true version is {get_version_str()}.\n'
                    f'Builtin version {relationship} than true version')
            self.use_DR_rust = self.use_DR_rust and self.DR_rust_available
        except Exception:
            traceback.print_exc()
            self.DR_rust_available = False
            self.use_DR_rust = False
        self.flush_option()


DR_mod_runtime = _DR_mod_runtime()


class DR_mod(ModInfo):
    mod_id = "difficult_rocket_mod"
    name = "Difficult Rocket mod"
    version = Version("0.2.0.0")

    writer = "shenjackyuanjie"
    link = "shenjack.top"
    description = "Difficult Rocket mod (where the game implement)"
    info = "Difficult Rocket mod (where the game implement)"

    config = DR_mod_runtime

    DR_version = (DR_status.DR_version, DR_status.DR_version)  # DR SDK 兼容版本

    # 反正是内置 mod 跟着最新版本的 DR 走就行了
    # DR_Api_version =   # DR Api版本
    # 同理 不管 API 版本   这东西要是不兼容了才是大问题

    def on_load(self, game: Game, old_self: Optional["DR_mod"] = None) -> bool:
        if not DR_mod_runtime.DR_rust_available:
            return False
        from .console import RustConsole

        game.console_class = RustConsole  # 替换掉原来的 console 类

        if old_self:
            game.client.window.add_sub_screen("SR1_ship", old_self.screen)
        else:
            self.config.flush_option()
        logger.info("on_load")
        logger.info(self.as_markdown())
        return True

    def on_client_start(self, game: Game, client: ClientWindow):
        from .sr1_ship import SR1ShipRender
        self.screen = SR1ShipRender
        client.add_sub_screen("SR1_ship", SR1ShipRender)
        logger.info('on_client_start added sub screen')

    def on_unload(self, game: Game):
        if DR_mod_runtime.DR_rust_available:
            game.console.stop()
            game.console_class = Console
            logger.info('replace Console class')
            game.init_console()
            logger.info('reinit console')


mod_class = DR_mod
