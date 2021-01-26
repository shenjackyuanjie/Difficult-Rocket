import time

from decimal import Decimal as D

times = 500000
# 尽量不要超过 5000000 否则整体执行时间>10s
# 5000000

a = 1.1
b = 2.5

# 重新创建 decimal 对象
a_start_time = time.time()
for x in range(0, times, 1):
    Da = D(str(a))
    Db = D(str(b))
    Dc = Da * Db
a_stop_time = time.time()

# 单次创建 decimal 对象
b_start_time = time.time()
Da = D(str(a))
Db = D(str(b))
for x in range(0, times, 1):
    Dc = Da * Db
b_stop_time = time.time()

# 直接计算
c_start_time = time.time()
for x in range(0, times, 1):
    Tc = a * b
c_stop_time = time.time()

print('重新创建 decimal 对象所需时间：', a_stop_time - a_start_time)
print('单次创建 decimal 对象所需时间：', b_stop_time - b_start_time)
print('直接计算所需时间: ', c_stop_time - c_start_time)
