"""
writen by shenjackyuanjie
mail: 3695888@qq.com
"""

import libs


A = [2.573, 3, ["m", "kg"], ["N", "s"]]
B = [0.245, -7, ["N", "kg"], ["m", "s"]]

print("A = " , A)
print("B = " , B)

C = libs.P_C.P_C_M(A, B)
D = libs.P_C.P_C_D(A, B)

print("A × B = " , C)
print("A ÷ B = " , D)
