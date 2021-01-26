import threading
import time
import os
import sys
import random


class Aclass(threading.Thread):
    def __init__(self, dev, ID):
        threading.Thread.__init__(self)
        self.running = True
        self.value = 0
        self.dev = dev
        self.id = ID
        print(self.id)

    def run(self):
        while self.running:
            while self.dev.using == True:
                continue
            self.dev.using = True
            self.running = self.dev.running[self.id]
            self.dev.using = False
            print(self.id, os.getpid(), os.getppid(), self.running)
            time.sleep(1)

    def stop(self):
        self.running = False


class dev():
    def __init__(self):
        self.using = False
        self.gets = {'a': False, 'b': False}
        self.running = {'a': True, 'b': True}


Dev = dev()
A = Aclass(Dev, 'a')
time.sleep(random.random())
B = Aclass(Dev, 'b')
A.start()
B.start()
print("hmmm")
try:
    while True:
        In = input()
        if In == "stop":
            Dev.running['a'] = False
            Dev.running['b'] = False
            break
        try:
            eval(In)
        except:
            print(EnvironmentError)
except KeyboardInterrupt:
    A.stop()
    B.stop()
