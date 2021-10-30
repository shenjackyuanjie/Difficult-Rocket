"""
这个测试主要是为了测试关于旋转的按钮碰撞箱判定的
感谢孙老师/
（下周就要学一次函数了
"""

import turtle

t = turtle

size = t.screensize()

screen = t.Screen()


def print_poi(x, y):
    print(x, y)
    this_t = turtle.clone()
    this_t.hideturtle()
    this_t.speed = 0
    this_t.penup()
    this_t.goto(x, size[1])
    this_t.pendown()
    this_t.goto(x, -size[1])


t.speed = 0

t.hideturtle()

screen.onclick(print_poi)
t.onclick(print_poi)
t.goto(10, 10)
t.goto(20, 100)
t.done()
