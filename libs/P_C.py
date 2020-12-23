"""
writen by shenjackyuanjie
mail: 3695888@qq.com

file name stand for : Physics calculation
"""

import libs
import math


def S_C_float_check(SC):  # stand for Scientific notation's float check
    """
    formats:
    SC list format:docs.basic_config.json:basic_number"""
    while SC[0] >= 10:
        SC[0] /= 10
        SC[1] += 1
    while SC[0] < 1:
        SC[0] *= 10
        SC[1] -= 1


def S_N_M(A, B):  # stand for Scientific notation multiple
    """
    formats:
    A & B list format:docs.basic_config.json:basic_number"""
    C = [A[0] * B[0], int(A[1] + B[1])]
    S_C_float_check(C)
    Unit1, Unit2 = A[2] + B[2], A[3] + B[3]
    if Unit1 == None:
        Unit1 = []
    libs.tools.D_C(Unit1, Unit2)
    C += [Unit1, Unit2]
    return C


def S_N_D(A, B):  # stand for Scientific notation divided
    """
    formats:
    A & B list format:docs.basic_config.json:basic_number"""
    C = [float(A[0] / B[0]), int(A[1] - B[1])]
    S_C_float_check(C)
    Unit1, Unit2 = A[2] + B[3], A[3] + B[2]
    if Unit1 == None:
        Unit1 = []
    libs.tools.D_C(Unit1, Unit2)
    C += [Unit1, Unit2]
    return C
