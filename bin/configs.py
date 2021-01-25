"""
writen by shenjackyuanjie
mail: 3695888@qq.com
"""

import re


def basic_number(Int=0, Float=1, unit1=None, unit2=None) -> list:
    if unit2 is None:
        unit2 = []
    if unit1 is None:
        unit1 = []
    return [Int, Float, unit1, unit2]


def basic_force() -> list:
    return [basic_number(unit1=["N"]), basic_number(unit1=["N"])]


def configs(name) -> dict:
    pass


def name_handler(name: str, configs: dict) -> str:
    pass
