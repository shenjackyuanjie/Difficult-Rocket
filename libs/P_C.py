"""
writen by shenjackyuanjie
mail: 3695888@qq.com
"""

import libs
import math


def P_C_M(A, B):  # stand for Physics Calculation multiple
    """
    formats:
    A & B list format:docs.basic_config.json:basic_number
    """
    C = [0.0, 1, [], []]
    Float = float(A[0] * B[0])
    Int = int(A[1] + B[1])
    if Float >= 10:
        Float /= 10
        Int += 1
    elif Float <= 0.01:
        Float *= 10
        Int -= 1
    else:
        pass
    Unit1, Unit2 = A[2] + B[2], []
    for unit in B[3]:
        if unit in Unit1:
            Unit1.remove(unit)
        else:
            Unit2.append(unit)
    if Unit1 == None:
        Unit1 = []
    for unit in Unit2:
        if unit in Unit1:
            Unit1.remove(unit)
            Unit2.remove(unit)
        else:
            pass
    C = [Float, Int, Unit1, Unit2]
    return C


def P_C_D(A, B):  # stand for Physics Calculation divide
    """
    formats:
    A & B list format:docs.basic_config.json:basic_number
    """
    B[2], B[3] = B[3], B[2]
    C = [0.0, 1, [], []]
    Float = float(A[0] / B[0])
    Int = int(A[1] - B[1])
    if Float >= 10:
        Float /= 10
        Int += 1
    elif Float <= 0.01:
        Float *= 10
        Int -= 1
    else:
        pass
    Unit1, Unit2 = A[2] + B[2], []
    for unit in B[3]:
        if unit in Unit1:
            Unit1.remove(unit)
        else:
            Unit2.append(unit)
    if Unit1 == None:
        Unit1 = []
    for unit in Unit2:
        if unit in Unit1:
            Unit1.remove(unit)
            Unit2.remove(unit)
        else:
            pass
    C = [Float, Int, Unit1, Unit2]
    return C
