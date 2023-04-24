#  -------------------------------
#  Difficult Rocket Mod
#  Copyright © 2020-2023 by shenjackyuanjie 3695888@qq.com
#  All rights reserved
#  -------------------------------

from .sr1_ship import SR1ShipRender

from MCDR.version import Version
from Difficult_Rocket.api.mod import ModInfo
from Difficult_Rocket.client import ClientWindow


class DR_mod(ModInfo):

    mod_id = "Difficult_Rocket_mod"
    name = "Difficult Rocket mod"
    version = Version("0.7.2.2")

    writer = "shenjackyuanjie"
    link = "shenjack.top"
    description = "Difficult Rocket mod (where the game implement)"
    info = "Difficult Rocket mod (where the game implement)"

    # DR_version =  # DR SDK 兼容版本
    # 反正是内置 mod 跟着最新版本的 DR 走就行了
    # DR_Api_version =   # DR Api版本
    # 同理 不管 API 版本   这东西要是不兼容了才是大问题

    def on_load(self):
        ...


mod_class = DR_mod
