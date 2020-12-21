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
    Unit1 = [].append(A[2].extend(B[2]))
    Unit2 = []
    for unit in B[3]:
        if unit in [Unit1]:
            Unit1.remove(unit)
        else:
            Unit2.append(unit)
    if Unit1 == None:
        Unit1 = []
    print(Unit1, Unit2)
    for unit in Unit2:
        print(unit)
        if unit in Unit1:
            Unit1.remove(unit)
            Unit2.remove(unit)
            print(unit)
        else:
            pass
    print(Unit1, Unit2)
    C = [Float, Int, Unit1, Unit2]
    print(C)
    return C


def P_C_D(A, B):  # stand for Physics Calculation divide
    """
    formats:
    A & B list format:docs.basic_config.json:basic_number
    """
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
    Unit1 = A[2].extend(B[3])
    Unit2 = []
    for unit in B[2]:
        if unit in [Unit1]:
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
