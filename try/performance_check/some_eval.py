#  -------------------------------
#  Difficult Rocket
#  Copyright © 2021-2022 by shenjackyuanjie
#  All rights reserved
#  -------------------------------

"""
writen by shenjackyuanjie
mail:   3695888@qq.com
github: @shenjackyuanjie
gitee:  @shenjackyuanjie
"""

import threading
import multiprocessing
import time

初始状态 = [6, 4, 5]
结果 = []


def 开撞(stack: int, 状态_: list, 记录: list, 动作: list = None):
    状态 = 状态_.copy()
    # 进行碰撞
    if 动作 is not None:
        if 状态[动作[0]] >= 1 and 状态[动作[1]] >= 1:
            if 动作[0] == 动作[1] and 状态[动作[0]] < 2:
                return "动作无效，退钱！"
            状态[动作[0]] -= 1
            状态[动作[1]] -= 1
            if 动作[0] == 动作[1]:
                状态[1] += 1
            else:
                状态[(6 - (动作[0] + 1) - (动作[1] + 1)) - 1] += 1
            记录.append(动作)
        else:
            return "动作无效，退钱！"
    # 判定是否只剩一个
    if 状态[0] + 状态[1] + 状态[2] == 1:
        global get
        get = [状态[x]+get[x] for x in range(0, 3)]
        # 结果 += [状态, 记录]
        # print(状态)
        # with open("soluition.md", mode='a') as file:
        #     file.write("{}\n".format(状态))
        return
    else:
        if stack < 3:
            进程池_ = []
            for x in range(0, 3):
                for y in range(x, 3):
                    撞他 = threading.Thread(target=开撞, args=(stack + 1, 状态, 记录, [x, y]), name="{}-{}".format(状态, 动作))
                    撞他.start()
                    进程池_.append(撞他)
            for 进程 in 进程池_:
                if 进程.is_alive():
                    进程.join()
        else:
            for x in range(0, 3):
                for y in range(x, 3):
                    开撞(stack + 1, 状态, 记录, [x, y])


def 找茬():
    while True:
        time.sleep(1)
        global get
        print(get)


if __name__ == '__main__':
    get = [0, 0, 0]
    finding = threading.Thread(target=找茬, daemon=True)
    finding.start()
    开撞(1, [6, 4, 5], [])
    print("----------------")
    print(get)
    # print(结果)
