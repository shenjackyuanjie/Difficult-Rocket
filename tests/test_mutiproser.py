
import multiprocessing as mp
from multiprocessing.context import Process
import os
import time
import random


class Main(mp.Process):
    def __init__(self, dev) -> None:
        Process.__init__(self)
        self.aaa = 1
        self.ttt = True
        self.dev = dev

    def run(self):
        while self.ttt:
            print(os.getpid())
            time.sleep(2)
            while not(self.dev.using):
                self.dev.using = True
                print('开始调用a')
                if self.dev.dev1 != 0:
                    self.aaa = self.dev.dev1
                if self.dev.bget == False:
                    print('B 没拿到')
                else:
                    print('B 拿到了')
                    self.dev.bget = False
                self.dev.aget = True
                self.ttt = self.dev.a
                self.dev.using = False
                print('结束调用a')
                break
            print(' aaa = ', self.aaa)
        print('完事，收工---a')


class render(mp.Process):
    def __init__(self, dev) -> None:
        Process.__init__(self)
        self.bbb = 3
        self.ggg = True
        self.dev = dev

    def run(self):
        while self.ggg:
            print(os.getpid())
            time.sleep(2)
            while not(self.dev.using):
                self.dev.using = True
                if random.choice(range(0, 5, 1)) == 4:
                    self.dev.dev1 = self.bbb
                print('开始调用b')
                if self.dev.aget == False:
                    print('A 没拿到')
                else:
                    print('A 拿到了')
                    self.dev.aget = False
                # self.dev.bget = True
                self.ggg = self.dev.b
                self.dev.using = False
                print('结束调用b')
                break
        print('完事，收工---b')


class Delivery():
    def __init__(self) -> None:
        self.using = False
        self.dev1 = 0
        self.a = True
        self.b = True
        self.aget = False
        self.bget = False


if __name__ == '__main__':
    dev = Delivery()
    A = Main(dev)
    B = render(dev)
    print(':aaa')
    A.start()
    time.sleep(1)
    B.start()
    time.sleep(5)
    print('gogogogogogoogogogogo')
    dev.a = False
    print('A is deadddddddddddddddddddd AAAAAAAA')
    time.sleep(3)
    dev.b = False
    print('BBBBBBBBBBBBBB')
