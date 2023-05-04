
from typing import Optional

from .main import FivePointRender

from libs.MCDR.version import Version
from Difficult_Rocket.api.mod import ModInfo
from Difficult_Rocket.main import Game
from Difficult_Rocket.client import ClientWindow


class FivePoint_mod(ModInfo):

    mod_id = 'five_point'
    name = '五子棋 mod'
    version = Version('1.0.0.0')

    writer = 'shenjackyuanjie'
    info = "基于 DR SDK 的五子棋"
    description = "左键黑棋，右键白棋，无限制 感谢我的两位同学激励我写出了这个mod"

    DR_version = (Version("0.7.2.2"), Version("0.7.2.2"))
    DR_Api_version = (Version("0.2.0.0"), Version("0.2.0.0"))

    def on_load(self, game: Game, old_self: Optional["ModInfo"] = None):
        ...

    def on_client_start(self, game: Game, client: ClientWindow):
        print('五子棋 on clint start 加载开始')
        client.add_sub_screen('Five_point', FivePointRender)

    def on_unload(self, game: Game):
        del game.client.window.screen_list['Five_point']
        # 删除五子棋屏幕


mod_class = FivePoint_mod
