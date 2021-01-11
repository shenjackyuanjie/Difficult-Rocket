"""
writen by shenjackyuanjie
mail: 3695888@qq.com
"""

import libs


A = [2.573, 3, ["m", "kg"], ["N", "s"]]
B = [2.45, -7, ["N", "kg"], ["m", "s"]]
C = [1.14, 5, ["m"], ["s"]]
D = [1.419, -4, ["kg"], ["m"]]

print("A = " , A)
print("B = " , B)
print("C = " , C)
print("D = " , D)

a = libs.P_C.S_N_M(A, B)
b = libs.P_C.S_N_D(A, B)
c = libs.P_C.S_N_M(b, B)
d = libs.P_C.S_N_D(a, B)

print("A × B = " , a)
print("A ÷ B = " , b)
print("A × B ÷ B = ", c)
print("A ÷ B × B = ", d)

e = libs.P_C.S_N_M(A, B, C, D)
f = libs.P_C.S_N_M(A,libs.P_C.S_N_M(B,libs.P_C.S_N_M(C, D)))

print("A * B * C * D = " , e)
print("A * B * C * D = " , f)

G = libs.render
