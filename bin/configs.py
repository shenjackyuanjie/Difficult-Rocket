"""
writen by shenjackyuanjie
mail: 3695888@qq.com
"""

import re
import bin
import time
import json5
import decimal


def basic_number(int_num=0, float_num=1, unit1=None, unit2=None) -> list:
    if unit1 is None:
        unit1 = []
    if unit2 is None:
        unit2 = []
    if bin.tools.is_decimal(float_num):  # is decimal class?
        return [int_num, float_num, unit1, unit2]  # is just return
    else:
        return [int_num, decimal.Decimal(str(float_num)), unit1, unit2]  # no create a decimal class


def basic_force() -> list:
    return [basic_number(unit1=["N"]), basic_number(unit1=["N"])]


def configs(name, option=None) -> dict:
    with open(name, 'r') as file:
        data = json5.load(file)
        if option:
            try:
                data = data[option]
            except:
                print(Exception)
                raise Exception


def name_handler(name: str, configs: dict = None) -> str:
    if configs is None:
        return name
    for need_replace in configs:
        if need_replace == '{date}':  # special replace
            replace = time.strftime(configs[need_replace], time.gmtime(time.time()))
            name.replace(need_replace, replace)
        name.replace(need_replace, configs[need_replace])
