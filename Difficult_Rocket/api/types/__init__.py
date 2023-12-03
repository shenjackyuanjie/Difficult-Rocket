#  -------------------------------
#  Difficult Rocket
#  Copyright © 2020-2023 by shenjackyuanjie 3695888@qq.com
#  All rights reserved
#  -------------------------------

from typing import Dict, Union
from dataclasses import dataclass

from lib_not_dr.types.options import (
    Options,
    OptionsError,
    OptionNameNotDefined,
    OptionNotFound,
    get_type_hints_,
)
from libs.MCDR.version import Version, VersionRequirement, VersionParsingError


class Fonts(Options):
    # font's value

    HOS: str = "HarmonyOS Sans"
    HOS_S: str = "HarmonyOS Sans SC"
    HOS_T: str = "HarmonyOS Sans TC"
    HOS_C: str = "HarmonyOS Sans Condensed"

    鸿蒙字体: str = HOS
    鸿蒙简体: str = HOS_S
    鸿蒙繁体: str = HOS_T
    鸿蒙窄体: str = HOS_C

    CC: str = "Cascadia Code"
    CM: str = "Cascadia Mono"
    CCPL: str = "Cascadia Code PL"
    CMPL: str = "Cascadia Mono PL"

    微软等宽: str = CC
    微软等宽无线: str = CM
    微软等宽带电线: str = CCPL
    微软等宽带电线无线: str = CMPL

    得意黑: str = "得意黑"
    # SS = smiley-sans
    SS: str = 得意黑


@dataclass
class FontData:
    """用于保存字体的信息"""

    font_name: str = Fonts.鸿蒙简体
    font_size: int = 13
    bold: bool = False
    italic: bool = False
    stretch: bool = False

    def dict(self) -> Dict[str, Union[str, int, bool]]:
        return dict(
            font_name=self.font_name,
            font_size=self.font_size,
            bold=self.bold,
            italic=self.italic,
            stretch=self.stretch,
        )


__all__ = [
    # main class
    "Options",
    "Version",
    "VersionRequirement",
    # data class
    "FontData",
    "Fonts",
    # exception
    "OptionsError",
    "OptionNameNotDefined",
    "OptionNotFound",
    "VersionParsingError",
    # other
    "get_type_hints_",
]
