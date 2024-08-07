#  -------------------------------
#  Difficult Rocket Mod
#  Copyright © 2020-2023 by shenjackyuanjie 3695888@qq.com
#  All rights reserved
#  -------------------------------

from __future__ import annotations

import traceback

from Difficult_Rocket import DR_status
from Difficult_Rocket.main import Game
from Difficult_Rocket.api.mod import ModInfo
from Difficult_Rocket.client import ClientWindow
from Difficult_Rocket.api.types import Options, Version

from lib_not_dr import loggers

DR_rust_version = Version("0.4.2")  # DR_mod 的 Rust 编写部分的兼容版本

logger = loggers.config.get_logger_from_old("client.dr_game", "client")


class ModLoadFaildError(BaseException):
    """
    就是用来告诉你, mod 加载错误
    """


class DRrsNotMatch(ModLoadFaildError):
    """
    就是用来告诉你, mod 的 rust 版本不匹配
    """


class _DR_mod_runtime(Options):
    name = "DR mod runtime"

    use_DR_rust: bool = True
    DR_rust_available: bool = False
    DR_rust_version: Version = DR_rust_version
    DR_rust_get_version: Version | None = None

    def init(self, **kwargs) -> bool:
        try:
            from .Difficult_Rocket_rs import get_version_str

            self.DR_rust_get_version = Version(get_version_str())
            self.DR_rust_available = True
            if self.DR_rust_get_version != self.DR_rust_version:
                relationship = (
                    "larger" if self.DR_rust_version > self.DR_rust_version else "smaller"
                )
                logger.fatal(
                    f"DR_rust builtin version is {self.DR_rust_version} "
                    f"but true version is {get_version_str()}.\n"
                    f"Builtin version {relationship} than true version",
                    tag="load_dll",
                )
                raise DRrsNotMatch(
                    f"DR rs found with version {get_version_str()}, "
                    f"but compat version is {DR_rust_version}"
                )
            self.use_DR_rust = self.use_DR_rust and self.DR_rust_available
        except Exception:
            traceback.print_exc()
            self.DR_rust_available = False
            self.use_DR_rust = False
            logger.warn(f"DR_rust load faild\n{traceback.format_exc()}", tag="load_dll")
        self.flush_option()
        return True


DR_mod_runtime = _DR_mod_runtime()


class DR_mod(ModInfo):
    mod_id = "difficult_rocket_mod"
    name = "Difficult Rocket mod"
    version = Version("0.4.0")

    writer = "shenjackyuanjie"
    link = "shenjack.top"
    description = "Difficult Rocket mod (where the game implement)"
    info = "Difficult Rocket mod (where the game implement)"

    config = DR_mod_runtime

    DR_version = (DR_status.DR_version, DR_status.DR_version)  # DR SDK 兼容版本

    # 反正是内置 mod 跟着最新版本的 DR 走就行了
    # DR_Api_version =   # DR Api版本
    # 同理 不管 API 版本   这东西要是不兼容了才是大问题

    def on_load(self, game: Game, old_self: DR_mod | None = None) -> bool:
        if not DR_mod_runtime.DR_rust_available:
            return False
        from .console import RustConsole

        game.console_class = RustConsole  # 替换掉原来的 console 类

        if old_self:
            from .sr1_ship import SR1ShipEditor

            game.client.window.add_sub_screen("SR1_ship", SR1ShipEditor)
        else:
            self.config.flush_option()
        logger.info("on_load")
        logger.info(f"\n{self.as_markdown()}")
        return True

    def on_client_start(self, game: Game, client: ClientWindow):
        # from .sr1_ship import SR1ShipRender
        from .menu import Menu

        client.add_sub_screen("DR_game_menu", Menu)
        logger.info("added dr_game_menu screen", tag="dr_game")

    def on_unload(self, game: Game):
        game.client.window.screen_list.pop("SR1_ship")


mod_class = DR_mod
