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
from Difficult_Rocket.api.mod import ModInfo
from Difficult_Rocket import DR_runtime, Options

"""
mod系统参数
"""
MOD_loader_version = "0.1.0.0"  # mod系统版本 版本号遵守 semver ++
semver_loader_version = Version(MOD_loader_version)

"""
一些重置用函数
"""
