"""
writen by shenjackyuanjie
mail: 3695888@qq.com
"""

import re
import bin
import time
import decimal


def basic_number(int_num=0, float_num=1, unit1=None, unit2=None) -> list:
    """

    :param unit2: list
    :param unit1: list
    :param int_num: int
    :type float_num: decimal.Decimal or float
    """
    if unit1 is None:
        unit1 = []
    if unit2 is None:
        unit2 = []
    if bin.tools.is_decimal(float_num):
        return [int_num, float_num, unit1, unit2]
    else:
        return [int_num, decimal.Decimal(str(float_num)), unit1, unit2]


def basic_force() -> list:
    return [basic_number(unit1=["N"]), basic_number(unit1=["N"])]


def configs(name) -> dict:
    pass


def name_handler(name: str, configs: dict = None) -> str:
    if configs is None:
        return name
    for need_replace in configs:
        if need_replace == '{date}':
            replace = time.strftime(configs[need_replace], time.gmtime(time.time()))
            name.replace(need_replace, replace)
        name.replace(need_replace, configs[need_replace])
