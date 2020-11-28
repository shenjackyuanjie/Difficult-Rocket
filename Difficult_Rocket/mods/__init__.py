#  -------------------------------
#  Difficult Rocket
#  Copyright © 2021-2022 by shenjackyuanjie
#  All rights reserved
#  -------------------------------

"""
writen by shenjackyuanjie
mail:   3695888@qq.com
github: @shenjackyuanjie
gitee:  @shenjackyuanjie
"""

from typing import Tuple

from Difficult_Rocket import game_version
from Difficult_Rocket.api.serializer import Serializable

"""
mod系统参数
"""
MOD_loader_version = "0.0.1"  # mod系统版本 版本号遵守semver2.0.0


"""
加载mod时会更改的参数
这里的只是范例,实际加载时会根据mod配置修改
"""


class MODInfo(Serializable):
    """
    加载mod时候的参数
    """
    """基本信息"""
    name: str  # mod名称
    version: str  # mod版本
    dependencies: list = []  # mod依赖

    """作者、描述"""
    writer: str  # 作者
    link: str = ""  # 作者链接
    description: str = ""  # 描述
    info: str = ""  # 其他信息 （可以很多很多）

    """版本兼容信息"""
    write_version: str  # mod编写版本
    compatible_version: Tuple[str, str] = (game_version, game_version)  # mod兼容版本
    # 第一个是最低兼容版本,第二个是最高兼容版本
    # 例如: ("1.0.0", "1.1.0")


MOD_info = MODInfo(
    name="Difficult_Rocket",
    version="0.0.1",
    writer="shenjackyuanjie"
)

"""
一些重置用函数
"""

