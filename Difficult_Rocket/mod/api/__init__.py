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

# system function
from typing import Tuple, List, Optional, TypeVar, TYPE_CHECKING


# from DR
if TYPE_CHECKING:
    from Difficult_Rocket.main import Game
    from Difficult_Rocket.client import ClientWindow
else:
    Game = TypeVar("Game")
    ClientWindow = TypeVar("ClientWindow")
from Difficult_Rocket import DR_runtime
from Difficult_Rocket.utils.options import Options

# from libs
from libs.MCDR.version import Version

RequireVersion = Tuple[Version, Version]
# 第一个是最低兼容版本,第二个是最高兼容版本
# 例如: ("1.0.0", "1.1.0") 表示从1.0.0版本开始兼容,到1.1.0版本结束兼容
ForceRequire = bool


class ModInfo(Options):
    """
    加载mod时候的参数
    """
    """基本信息"""
    mod_id: str  # mod id
    name: str  # mod 名称
    version: Version  # mod 版本

    """作者、描述"""
    writer: str  # 作者
    link: str = ""  # 作者链接
    description: str = ""  # 描述 (务必简洁明了)
    info: str = ""  # 其他信息 (可以很多很多)

    """版本相关信息"""
    DR_version: RequireVersion = (DR_runtime.DR_version, DR_runtime.DR_version)  # DR SDK 兼容版本
    DR_Api_version: RequireVersion = (DR_runtime.API_version, DR_runtime.API_version)  # DR Api版本
    Mod_Require_version: List[Tuple[str, ForceRequire, RequireVersion]] = []  # mod 依赖版本

    """mod 状态"""
    is_enable: bool = True  # 是否启用
    is_loaded: bool = False  # 是否加载

    """mod 配置"""
    config: Options = Options()  # mod 配置存储
    old_mod: Optional["ModInfo"] = None  # 旧的mod实例

    def on_load(self, game: Game, old_self: Optional["ModInfo"] = None) -> bool:
        """ 加载时调用 """
        print(f'Mod {self.mod_id} loaded')
        return True

    def on_client_start(self, game: Game, client: ClientWindow):
        """ 客户端启动时调用 """
        print(f'Mod {self.mod_id} client start')

    def on_client_stop(self, game: Game, client: ClientWindow, source: str = 'window'):
        """ 客户端停止时调用 """
        print(f'Mod {self.mod_id} client stop')

    def on_server_start(self, game: Game):
        """ 服务器启动时调用 """
        print(f'Mod {self.mod_id} server start')

    def on_server_stop(self, game: Game):
        """ 服务器停止时调用 """
        print(f'Mod {self.mod_id} server stop')

    def on_unload(self, game: Game):
        """ 卸载时调用 """
        print(f'Mod {self.mod_id} unloaded')

