from math import sin, cos, sqrt
import pyglet
from pyglet.gl import *


def vec(*args):
    return (GLfloat * len(args))(*args)


class GameEventHandler(object): # 这里用GameEventHandler把事件包装了一下
    rx, ry = 0, 0
    track = []

    def on_draw(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        # glLoadIdentity()
        position = (sin(integral_drift[0] / 2) / sqrt(integral_drift[0]),
                    cos(integral_drift[1] / 2) / sqrt(integral_drift[1]))
        self.track.append(position)


        glColor3f(1, 1, 1)
        glBegin(GL_LINE_STRIP)
        for v in self.track:
            glVertex3f(v[0], v[1], 0)
        glEnd()

    @staticmethod
    def on_resize(width, height):
        return pyglet.event.EVENT_HANDLED


def scene_init():
    # One-time GL setup
    glClearColor(0, 0, 0, 1)
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_CULL_FACE)
    glEnable(GL_BLEND)  # 启用混合功能，将图形颜色同周围颜色相混合
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

    glEnable(GL_POLYGON_SMOOTH)  # 多边形抗锯齿
    # glHint(GL_POLYGON_SMOOTH, GL_NICEST)

    glEnable(GL_LINE_SMOOTH)  # 线抗锯齿
    # glHint(GL_LINE_SMOOTH_HINT, GL_NICEST)

    glEnable(GL_POINT_SMOOTH)  # 点抗锯齿
    # glHint(GL_POINT_SMOOTH, GL_NICEST)

    pass


def update(dt):
    delta_x = 5 * dt
    delta_y = 5 * dt
    delta_z = 5 * dt
    integral_drift[0] += delta_x
    integral_drift[1] += delta_y
    integral_drift[2] += delta_z
    pass


window = pyglet.window.Window(resizable=True) 
scene_init()  
integral_drift = [0.1, 0.1, 0.1]  # 位移的总和
game_event = GameEventHandler()
window.push_handlers(game_event.on_draw)
pyglet.app.event_loop.clock.schedule(update) # 单位时间触发update
pyglet.app.run()