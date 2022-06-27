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

# Difficult_Rocket function

# libs function
from MCDR.serializer import Serializable

"""
DR 内部数据传输格式类型
"""


# 一艘船的数据格式
class Ship(Serializable):
    data: dict

    def __init__(self, **kwargs):
        super().__init__(**kwargs)


# 蓝图部件的数据格式
class Blueprint(Serializable):
    data: dict

    def __init__(self, **kwargs):
        super().__init__(**kwargs)


# 飞船上的单个部件的数据格式
class Part(Serializable):
    data: dict

    def __init__(self, part_type: str, **kwargs):
        super().__init__()
        self.type = part_type
        self.name = kwargs.get('name')


# 整个存档的数据格式
class Save(Serializable):
    data: dict

    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class PartType(Serializable):
    data: dict  # 输出的数据格式


# 所有部件的格式的存储
class PartTypes(Serializable):
    data: dict = {}  # 所有部件的格式

    def add_part(self, part_type: str, **kwargs):
        self.data[part_type] = Part(part_type, **kwargs)
