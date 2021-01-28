"""
writen by shenjackyuanjie
mail: 3695888@qq.com
"""

import bin
import json5
import decimal

"""
some tools
"""


def mbool(thing):  # stand for my bool
    if (thing == "True") or (thing == 1) or (thing == "1"):
        return True
    elif (thing == "False") or (thing == 0) or (thing == "0"):
        return False
    else:
        raise ValueError("Need a 'like bool' not anything else")


"""
Physics calculation
"""


def is_decimal(A: any) -> bool:
    if type(A) != type(decimal.Decimal):
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


def D_C(listA: list, listB: list) -> '1':  # stand for Duplicate check
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
    return 1


def S_C_float_check(SC) -> None:  # stand for Scientific notation's float check
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
        raise TypeError("it need more than 2!")
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
    if Unit1 == None:
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
    g = bin.config.basic_number()
    A = S_N_M(M, m, G)
    g = S_N_D(A, S_N_M(R, R))
    return g


def distance(A, B):
    """
    formats:
    A & B format: docs.basic_config:basic_poi
    """
    D = bin
    pass


"""
loads
"""


def config(file_name, stack=None):
    rd = {}  # rd -> return
    try:
        with open(file_name, "r") as jf:  # jf -> json file
            rd = json5.load(jf)
    except FileNotFoundError:
        raise FileNotFoundError("no config file")
    if stack != None:
        rd = rd[stack]
    return rd