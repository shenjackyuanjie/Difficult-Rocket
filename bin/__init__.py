"""
writen by shenjackyuanjie
mail: 3695888@qq.com
github: @shenjackyuanjie
"""
from .new_thread import new_thread
from .tools import config

__all__ = [
    'new_thread',
    'config'
]


@new_thread('think')
def think(some_thing_to_think):




    
    gotcha = 'think_result'
    return gotcha
