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
import ctypes

# Difficult_Rocket function

# libs function
# from MCDR.serializer import Serializable

"""
DR 内部数据传输格式类型
"""


class datas(ctypes.Structure):
    _fields_: list = [("name", ctypes.c_char_p),
                      ("uuid", ctypes.c_char_p),
                      ]
