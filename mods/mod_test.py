#  -------------------------------
#  Difficult Rocket
#  Copyright © 2021 by shenjackyuanjie
#  All rights reserved
#  -------------------------------

"""
writen by shenjackyuanjie
mail:   3695888@qq.com
github: @shenjackyuanjie
gitee:  @shenjackyuanjie
"""

"""
this is a test of modding in Difficult Rocket
just a test
只是一个DR的mod测试
"""

# from libs
import semver

# from DR
from Difficult_Rocket import semver_game_version
from Difficult_Rocket.mods import MODInfo, semver_loader_version

mod_info = MODInfo(name="test mod",
                   version=semver.VersionInfo.parse("0.0.1"),
                   write_version=semver_game_version,
                   write_loader_version=semver_loader_version)

print(mod_info.serialize())
