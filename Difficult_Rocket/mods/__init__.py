#  -------------------------------
#  Difficult Rocket
#  Copyright © 2021-2022 by shenjackyuanjie 3695888@qq.com
#  All rights reserved
#  -------------------------------

"""
writen by shenjackyuanjie
mail:   3695888@qq.com
github: @shenjackyuanjie
gitee:  @shenjackyuanjie
"""

# system function
from typing import Tuple

# from libs
from MCDR.version import Version
from MCDR.serializer import Serializable

# from DR
from Difficult_Rocket import semver_game_version

"""
mod系统参数
"""
MOD_loader_version = "0.0.1"  # mod系统版本 版本号遵守semver2.0.0
semver_loader_version = Version(MOD_loader_version)

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
    version: Version  # mod版本
    dependencies: list = []  # mod依赖

    """作者、描述"""
    writer: str  # 作者
    link: str = ""  # 作者链接
    description: str = ""  # 描述 (务必简洁明了)
    info: str = ""  # 其他信息 (可以很多很多)

    """版本兼容信息"""
    write_version: Version  # mod编写版本
    write_loader_version: Version  # mod编写的加载器版本
    compatible_version: Tuple[Version, Version] = (semver_game_version, semver_game_version)  # mod兼容版本
    # 第一个是最低兼容版本,第二个是最高兼容版本
    # 例如: ("1.0.0", "1.1.0") 表示从1.0.0版本开始兼容,到1.1.0版本结束兼容


MOD_info = MODInfo(
    name="Difficult_Rocket",
    version="0.0.1",
    writer="shenjackyuanjie",
    write_version=semver_game_version,
    write_loader_version=semver_loader_version
)

# print(MOD_info.serialize())

"""
一些重置用函数
"""
