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
    Float = A[0] * B[0]
    Int = A[1] + B[1]
    if Float >= 10:
        Float /= 10
        Int += 1
    elif Float <= 0.01:
        Float *= 10
        Int -= 1
    else:
        Float = float(Float)
        Int = int(Int)
    Unit1 = [].append(A[2].extend(B[2]))
    Unit2 = []
    for unit in B[3]:
        if unit in [Unit1]:
            n = Unit1.index(unit)
            Unit1.pop(n)
        else:
            Unit2.append(unit)
    if Unit1 == None:
        Unit1 = []
    C = [Float, Int, Unit1, Unit2]
    return C


def P_C_D(A, B):  # stand for Physics Calculation divide
    """
    formats:
    A & B list format:docs.basic_config.json:basic_number
    """
    C = [0.0, 1, [], []]
    Float = A[0] / B[0]
    Int = A[1] - B[1]
    if Float >= 10:
        Float /= 10
        Int += 1
    elif Float <= 0.01:
        Float *= 10
        Int -= 1
    else:
        Float = float(Float)
        Int = int(Int)
    Unit1 = A[2].extend(B[3])
    Unit2 = []
    for unit in B[2]:
        if unit in [Unit1]:
            n = Unit1.index(unit)
            Unit1.pop(n)
        else:
            Unit2.append(unit)
    if Unit1 == None:
        Unit1 = []
    C = [Float, Int, Unit1, Unit2]
    return C
