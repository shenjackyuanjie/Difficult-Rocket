"""
writen by shenjackyuanjie
mail:   3695888@qq.com
github: @shenjackyuanjie
gitee:  @shenjackyuanjie
"""


class Test:
    def __init__(self, a):
        self.name = 'shenjackyuanjie'
        self.a = a

    @property
    def value(self):
        return self.name

    def __str__(self):
        return str(self.a)

    def __int__(self):
        return int(self.a)


abc = Test(1.23)
print(int(abc))
print(abc)


