#  -------------------------------
#  Difficult Rocket
#  Copyright © 2020-2023 by shenjackyuanjie 3695888@qq.com
#  All rights reserved
#  -------------------------------

from typing import Optional, Tuple, TYPE_CHECKING

from pyglet.graphics import Batch, Group


class BaseTheme(dict):
    """
    Base class of themes
    """

    theme_name = "BaseTheme"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        for k, v in kwargs.items():
            if hasattr(self, k):
                setattr(self, k, v)

    if TYPE_CHECKING:
        def init(self, batch: Batch, group: Group, **kwargs) -> None:
            """
            Init theme
            :param batch: batch
            :param group: group
            :param kwargs: options
            :return: None
            """


class FontTheme(BaseTheme):
    """
    Base class of font themes
    """

    theme_name = "FontTheme"
    font_name: Optional[str] = "Times New Roman"
    font_size: Optional[int] = 12
    bold: Optional[bool] = False
    italic: Optional[bool] = False
    stretch: Optional[bool] = False
    color: Optional[Tuple[int, int, int, int]] = (255, 255, 255, 255)
    align: Optional[str] = "center"
