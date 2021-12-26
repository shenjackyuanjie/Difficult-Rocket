import time
import random


# 生成一个以纳秒为单位自动计时输入函数的耗时并以纳秒和秒为单位输出时长的装饰器
def time_measure(func):
    def wrapper(*args, **kwargs):
        t1 = time.perf_counter_ns()
        func(*args, **kwargs)
        t2 = time.perf_counter_ns()
        # print('{} took {} seconds'.format(func.__name__, t2 - t1))
        print('{} took {} nanoseconds'.format(func.__name__, (t2 - t1) / 1000000000))
        return func(*args, **kwargs)
    return wrapper


# 一个长度为十万的整数列表
nums = [random.randint(0, 1000000) for _ in range(1000000)]
test_list = [random.random() for _ in range(1000000)]


# 排序test_list并计时
@time_measure
def sort_test():
    test_list.sort()


@time_measure
def sortit():
    nums.sort()

sortit()
sort_test()

# 运行10次sort_test和sortit，并计算平均时间
for _ in range(10):
    sort_test()

for _ in range(10):
    sortit()


# 使用pyglet创建一个窗口，并在窗口中绘制一个线条
from libs import pyglet
window = pyglet.window.Window(width=500, height=500)
vertices = (0, 0, 0, 500, 500, 500, 500, 0)
colors = (255, 0, 0, 255, 0, 255, 255, 255)
batch = pyglet.graphics.Batch()
batch.add(4, pyglet.gl.GL_QUADS, None, ('v2i', vertices), ('c3B', colors))




# sortit took 144131100 seconds
# sortit took 0.1441311 nanoseconds
# sort_test took 146132900 seconds
# sort_test took 0.1461329 nanoseconds
