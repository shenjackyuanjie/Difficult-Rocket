import logging

tick_time, velocity, height, add_speed = 0, 0, 0, 0
m = 4610025
gravity = 9.798
R = 637100
n = 0.5943466
H = 70000
F = 208201000
TPS = 10
MSPT = 1 / TPS

logging.basicConfig(filename='logs/super.log',
                    filemode='w',
                    level=logging.DEBUG)

while True:  # 主tick循环
    logging.info([tick_time, velocity, height, add_speed])
    # 基础加速度运算
    add_speed = (F / m) - ((gravity * (R ** 2)) / ((R + height) ** 2))
    # 出大气层判定
    if height < 70000:  # 没出大气 加速度需要减去大气阻力
        add_speed -= ((n * (velocity ** 2) * (10 ** (-6 * height) / H)) / m)
    height += (MSPT * velocity)  # 高度 加 速度除以TPS（tick per second）（每tick加速）
    velocity += (MSPT * add_speed)  # 速度 加 加速度除以TPS
    if tick_time < 192:  # 一些我也不知道是什么意思的tick判定
        m -= ((MSPT * F) / 3399.2)  # 3399.2是个啥？
    elif tick_time < 240:
        m -= (129 * MSPT)  # ??? 129?
    else:
        m -= (4 * MSPT)  # 4?
    # tick 加时间
    tick_time += MSPT
    if tick_time < 48:  # 如果时间没到48秒
        continue
    elif tick_time == 48:  # 如果时间到了48秒
        m = 1243700
        F = 44189600
    elif tick_time == 96:
        m = 193125
        F = 8498000
    elif tick_time == 144:
        m = 40875
        F = 1699600
    elif tick_time == 192:
        m = 10225
        F = 446145
    elif tick_time == 240:
        m = 2308
        F = 21245
    elif tick_time >= 567:
        tick_time += ((12308300 - height) / velocity)
        break

print('t: %s' % tick_time)
