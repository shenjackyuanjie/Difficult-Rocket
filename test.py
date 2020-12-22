"""
writen by shenjackyuanjie
mail: 3695888@qq.com
"""

import libs


A = [2.573, 3, ["m", "kg"], ["N", "s"]]
B = [0.245, -7, ["N", "kg"], ["m", "s"]]

print("A = " , A)
print("B = " , B)

C = libs.S_D.S_N_M(A, B)
D = libs.S_D.S_N_D(A, B)
E = libs.S_D.S_N_D(C, B)

print("A × B = " , C)
print("A ÷ B = " , D)
print("A × B ÷ B = " , E)