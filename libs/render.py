"""
writen by shenjackyuanjie
mail: 3695888@qq.com
"""

import pyglet
import threading

from pyglet.app import run
from pyglet.window import Window
from pyglet.resource import image

class RenderThread(threading.Thread):
    def __init__(self):
        pass