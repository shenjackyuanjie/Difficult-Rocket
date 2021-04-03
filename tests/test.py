"""
writen by shenjackyuanjie
mail: 3695888@qq.com
"""

import decimal

import bin

A = [2.573, 3, ['m', 'kg'], ['N', 's']]
B = [2.45, -7, ['N', 'kg'], ['m', 's']]
C = [1.14, 5, ['m'], ['s']]
D = [1.419, -4, ['kg'], ['m']]

print('A = ', A)
print('B = ', B)
print('C = ', C)
print('D = ', D)

a = bin.tools.S_N_M(A, B)
b = bin.tools.S_N_D(A, B)
c = bin.tools.S_N_M(b, B)
d = bin.tools.S_N_D(a, B)

print('A × B = ', a)
print('A ÷ B = ', b)
print('A × B ÷ B = ', c)
print('A ÷ B × B = ', d)

e = bin.tools.S_N_M(A, B, C, D)
f = bin.tools.S_N_M(A, bin.tools.S_N_M(B, bin.tools.S_N_M(C, D)))

print('A * B * C * D = ', e)
print('A * B * C * D = ', f)

e = decimal.Decimal('0.1')
f = 0.1

print(type(e), type(f))
