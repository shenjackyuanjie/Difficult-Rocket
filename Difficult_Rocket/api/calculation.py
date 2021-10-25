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

import math
import decimal

from typing import List, Optional, Union
from decimal import Decimal


# linear_algebra


def C_R_P(position: List, degrees: List):  # stand for calculation
    """
    very thanks for lenny from pyglet developer
    https://github.com/LennyPhoenix
    this part of code is write by him
    """
    radians = degrees * (math.pi / 180)
    cos = math.cos(radians)
    sin = math.sin(radians)
    rotated_pos = (position[0] * cos - position[1] * sin, position[0] * sin + position[1] * cos)
    return rotated_pos


"""
Physics calculation
"""


def is_decimal(A: any) -> bool:
    if isinstance(A, decimal.Decimal):
        return False
    else:
        return True


def F_D(A: decimal, B: decimal) -> decimal:
    if is_decimal(A) and is_decimal(B):
        return A / B


def F_Mu(A: decimal, B: decimal) -> decimal:
    if is_decimal(A) and is_decimal(B):
        return A * B


def F_Mi(A: decimal, B: decimal) -> decimal:
    if is_decimal(A) and is_decimal(B):
        return A - B


def F_A(A: decimal, B: decimal) -> decimal:
    if is_decimal(A) and is_decimal(B):
        return A + B


def D_C(listA: list, listB: list):  # stand for Duplicate check
    """
    usage:\n
    input two list\n
    the fun will do duplicate check and sort then\n
    the fun won't return any thing just change the list now
    """
    for unit in listB:
        if unit in listA:
            listA.remove(unit)
            listB.remove(unit)
        else:
            continue
    listA.sort()
    listB.sort()


def S_C_float_check(SC):  # stand for Scientific notation's float check
    """
    formats:
    SC list format:docs.basic_config.json:basic_number"""
    while SC[0] >= 10:
        SC[0] = F_D(SC[0], 10)
        SC[1] += 1
    while SC[0] < 1:
        SC[0] = F_Mu(SC[0], 10)
        SC[1] -= 1


def S_N_M(*SN):  # stand for Scientific notation multiple
    """
    formats:
    A & B & C list format:docs.basic_config.json:basic_number"""
    if len(SN) < 2:
        raise TypeError('it need more than 1!')
    elif len(SN) == 2:
        return __S_N_M(SN[0], SN[1])
    else:
        R = __S_N_M(SN[0], SN[1])
        for A in SN[2:]:
            R = __S_N_M(R, A)
    return R


def __S_N_M(A, B):
    """
    formats:
    A & B list format:docs.basic_config.json:basic_number"""
    R = [F_Mu(A[0], B[0]), A[1] + B[1]]
    S_C_float_check(R)
    Unit1, Unit2 = A[2] + B[2], A[3] + B[3]
    if Unit1 is None:
        Unit1 = []
    D_C(Unit1, Unit2)
    R += [Unit1, Unit2]
    return R


def S_N_D(A, B):  # stand for Scientific notation divided
    """
    formats:
    A & B list format:docs.basic_config:basic_number"""
    R = [F_D(A[0], B[0]), A[1] - B[1]]
    S_C_float_check(R)
    Unit1, Unit2 = A[2] + B[3], A[3] + B[2]
    if Unit1 is None:
        Unit1 = []
    D_C(Unit1, Unit2)
    R += [Unit1, Unit2]
    return R


def G_C(M, m, R, G):  # stand for gravity calculation
    """
    formats:
    M : ship's mass
    m : planet's mass
    R : distance to the planet
    G : Gravitational constant
    M & m & R format: docs.basic_config:basic_number
    """
    g = basic_force()
    A = S_N_M(M, m, G)
    g = S_N_D(A, S_N_M(R, R))
    return g


def distance(A, B):
    """
    formats:
    A & B format: docs.basic_config:basic_poi
    """
    poi_dis = basic_poi()
    for x in A, B:
        x = decimal.Decimal(str(x))
    xd = A[0] - B[0]
    yd = A[1] - B[1]
    poi_dis[0] = xd
    poi_dis[1] = yd
    # 勾股定理
    poi_dis[0] **= 2
    poi_dis[1] **= 2
    poi_dis.append(poi_dis[0] + poi_dis[1])
    poi_dis[2] **= 0.5
    return poi_dis[2]


def _BasicNumber(int_num=0, float_num=1, unit1=None, unit2=None) -> list:
    if unit1 is None:
        unit1 = []
    if unit2 is None:
        unit2 = []
    if is_decimal(float_num):  # is decimal class?
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


class ScientificNumber:
    """
    A class of Scientific notation
    give float and integer and unit
    """

    def __init__(self,
                 小数: Union[float, Decimal] = 1.0,
                 指数: int = 0,
                 乘单位: list = list,
                 除单位: list = list):
        if not isinstance(小数, Decimal):
            self.小数 = Decimal(小数)
        else:
            self.小数 = 小数
        self.指数 = 指数
        self.乘单位 = 乘单位
        self.除单位 = 除单位
        self.check()

    def check(self):
        while self.小数 > 10:
            self.小数 /= 10
            self.指数 += 1
        while self.小数 < 1:
            self.小数 *= 10
            self.指数 -= 1
        self.除单位.sort()
        self.乘单位.sort()

