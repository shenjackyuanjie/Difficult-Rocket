#  -------------------------------
#  Difficult Rocket
#  Copyright © 2020-2023 by shenjackyuanjie 3695888@qq.com
#  All rights reserved
#  -------------------------------

# system function
from typing import Tuple, List

# from libs
from MCDR.version import Version

# from DR
from Difficult_Rocket import DR_runtime, Options


"""
加载mod时会更改的参数
这里的只是范例,实际加载时会根据mod配置修改
"""

RequireVersion = Tuple[Version, Version]
# 第一个是最低兼容版本,第二个是最高兼容版本
# 例如: ("1.0.0", "1.1.0") 表示从1.0.0版本开始兼容,到1.1.0版本结束兼容
ForceRequire = bool


# TODO 完善中
class MODInfo(Options):
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


"""
一些重置用函数
"""
