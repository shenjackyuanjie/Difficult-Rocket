# test of "for" speed
# R5 5600X 16*2GB DDR4 3200
import random
import time
from pprint import pprint

TPS = 60
SPT = 1 / TPS

list_num = 100
test_list = {}
for x in range(list_num):
    test_list[x] = [random.random()]
time_list = {}

times = 100
t = 0
start_t = time.time()
while t < times:
    s_t = time.time()
    t += 1
    for x in test_list:
        if test_list[x][0] > 0.5:
            print('y', end=' ')
        else:
            print('n', end=' ')
        pass
    print(t, end='\n')
    e_t = time.time()
    time_list[t] = [s_t, e_t, e_t - s_t]
end_time = time.time()
pprint(time_list)
pprint(test_list)
print(start_t, end_time, end_time - start_t)
