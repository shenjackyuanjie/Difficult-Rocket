"""
writen by shenjackyuanjie
mail: 3695888@qq.com
"""

import decimal
import logging
# import re
import os
import sys
import time

import json5

sys.path.append('./')
try:
    from bin import tools
except (ModuleNotFoundError, ImportError, ImportWarning):
    import tools

# logger
configs_logger = logging.getLogger('configs')


def _BasicNumber(int_num=0, float_num=1, unit1=None, unit2=None) -> list:
    if unit1 is None:
        unit1 = []
    if unit2 is None:
        unit2 = []
    if tools.is_decimal(float_num):  # is decimal class?
        return [int_num, float_num, unit1, unit2]  # is just return
    else:
        return [int_num, decimal.Decimal(str(float_num)), unit1, unit2]  # no create a decimal class


def BasicNumber(int_num=0, float_num=1, unit1=None, unit2=None, num=1) -> list:
    numbers = []
    if num > 1:
        for x in range(0, num, 1):
            numbers.append(_BasicNumber(int_num, float_num, unit1, unit2))
    elif num == 1:
        return _BasicNumber(int_num, float_num, unit1, unit2)
    else:  # num < 1
        raise TypeError('you should give me a num with >= 1!')
    return numbers


class BasicNumberClass:
    def __init__(self, int_num=0, float_num=1, unit1=None, unit2=None):
        self.int = int_num
        self.float = decimal.Decimal(str(float_num))
        if unit1:
            self.units1 = unit1
        else:
            self.units1 = []
        if unit2:
            self.units2 = unit2
        else:
            self.units2 = []

    def sort(self):
        self.units1.sort()
        self.units2.sort()

    def float_int_check(self, int_=None, float_=None):
        if not int_:
            int_ = 1
        if not float_:
            float_ = decimal.Decimal(1.0)
        while float_ > 10:
            float_ / 10
            int_ + 1
        else:
            while float_ < 0.1:
                float_ * 10
                int_ - 1
        return [int_, float_]

    def units(self) -> list or bool:
        if (self.units1 == []) and (self.units2 == []):
            return None
        data = self.units1
        data.append(self.units2)
        return data

    def __str__(self):
        return [self.float, self.int, self.units1, self.units2]

    def __add__(self, other):
        o_type = type(other)
        if o_type == type(self):
            self.sort()
            other.sort()
            if self.units() == other.units():
                self_num = self.float * (10 ** self.int)
                other_num = other.float * (10 ** other.float)
                r_float = self_num + other_num
                check = self.float_int_check(1, r_float)
                self.float = check[0]
                self.int = check[1]
        elif o_type == type(decimal.Decimal('1.0')) and not self.units():
            pass

    def __radd__(self, other):
        self.__add__(self)

    def __mul__(self, other):
        pass

    def __rmul__(self, other):
        self.__mul__(self)

    def __truediv__(self, other):
        pass


def basic_poi(poi_type=None) -> list:
    if poi_type is None:
        return BasicNumber(unit1='m', num=2)
    if poi_type == 'chunk':
        return [BasicNumber(unit1='chunk', num=2), BasicNumber(unit1='m', num=2)]


def basic_force() -> list:
    return BasicNumber(unit1='N', num=2)


def configs(name, option=None) -> dict:
    with open(name, 'r') as file:
        data = json5.load(file)
        if option:
            try:
                data = data[option]
            except IndexError as exp:
                log = 'can\'t find stack named %s in file %s' % (option, name)
                configs_logger.exception(log)
                raise IndexError(log)
        return data


name_handlers = {'time.time': str(time.time()),
                 'dir': str(os.getcwd()),
                 'py_v': str(sys.version.split(' ')[0])
                 }


def name_handler(name: str, configs=dict) -> str:
    names = name_handlers
    if configs is dict:
        pass
    elif type(configs) is dict:
        names.update(configs)
    else:
        pass
    if 'date' in names:
        names['date'] = str(time.strftime(names['date'], time.gmtime(time.time())))
    handler_name = name.format(**names)
    return handler_name
