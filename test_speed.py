import time

from decimal import Decimal as D


times = 1000000

a = 1
b = 2

c = 0.1
d = 2.1

a_start_time = time.time()
for x in range(0, times, 1):
    Da = D(str(a))
    Db = D(str(b))
    Dc = Da * Db
a_stop_time = time.time()

b_start_time = time.time()
Da = D(str(a))
Db = D(str(b))
for x in range(0, times, 1):
    Dc = Da * Db
b_stop_time = time.time()

c_start_time = time.time()
for x in range(0, times, 1):
    Tc = a * b
c_stop_time = time.time()

def test(times, a, b):
    t = times
    s = time.time()
    while t:
        
        t -= 1
    e = time.time()
    return e - s


