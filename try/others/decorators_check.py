#  Copyright (c) 2021. Lorem ipsum dolor sit amet, consectetur adipiscing elit.
#  Morbi non lorem porttitor neque feugiat blandit. Ut vitae ipsum eget quam lacinia accumsan.
#  Etiam sed turpis ac ipsum condimentum fringilla. Maecenas magna.
#  Proin dapibus sapien vel ante. Aliquam erat volutpat. Pellentesque sagittis ligula eget metus.
#  Vestibulum commodo. Ut rhoncus gravida arcu.

"""
writen by shenjackyuanjie
mail:   3695888@qq.com
github: @shenjackyuanjie
gitee:  @shenjackyuanjie
"""


class MainGame:

    def __init__(self):
        self.ticks = {}
        self.speed = 0

    def tick(self):
        self.speed = 1
        # bla bla bla
        for mod in self.ticks:
            mod(self)

    def mix_tick(self, mod_name):
        def wrapper(fun, *args, **kwargs):
            self.ticks[mod_name] = fun
            return fun(*args, **kwargs)

        return wrapper


mod_game = MainGame()


@mod_game.mix_tick(mod_name='test')
def mod_tick(Game: MainGame):
    Game.speed += 1
