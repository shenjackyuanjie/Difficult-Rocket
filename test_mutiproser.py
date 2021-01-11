
import multiprocessing as mp
import os, time

class Main():
    def __init__(self, dev) -> None:
        self.aaa = 1
        self.ttt = False
        self.dev = dev

    def main(self):
        while self.ttt:
            print(time.time())
            print(os.getpid())
            time.sleep(0.5)
            while not(self.dev.using):
                self.dev.using = True
                if self.dev.bget == True:
                    print("B 没拿到")
                else:
                    print("B 拿到了")
                self.dev.aget = True
                self.dev.using = False


class render():
    def __init__(self, dev) -> None:
        self.bbb = 3
        self.ggg = True


class Delivery():
    def __init__(self) -> None:
        self.using = False
        self.dev1 = ""
        self.aget = False
        self.bget = False


if __name__ == "__main__":
    dev = Delivery()
