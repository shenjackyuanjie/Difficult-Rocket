
from typing import Dict

from pyglet.graphics import Batch
from pyglet.shapes import Circle, Line

from Difficult_Rocket.api.screen import BaseScreen
from Difficult_Rocket.client import ClientWindow


class FivePointRender(BaseScreen):

    def __init__(self, main_window: "ClientWindow"):
        super().__init__(main_window)

        self.scale = 50
        self.sheet_size = (-10, 10)
        self.chest_sheet = []
        self.batch = Batch()
        center_x, center_y = main_window.width // 2, main_window.height // 2
        for dx in range(self.sheet_size[0], self.sheet_size[1] + 1):
            x_side = Line(x=0, y=center_y + (dx * self.scale),
                          x2=main_window.width, y2=center_y + (dx * self.scale),
                          width=3, color=(0, 200, 0, 200), batch=self.batch)
            y_side = Line(x=center_x + (dx * self.scale), y=0,
                          x2=center_x + (dx * self.scale), y2=main_window.height,
                          width=3, color=(0, 200, 0, 200), batch=self.batch)
            self.chest_sheet.append([x_side, y_side])
        self.nodes: Dict[str, Circle] = {}

    def draw_batch(self, window: "ClientWindow"):
        self.batch.draw()

    def on_resize(self, width: int, height: int, window: "ClientWindow"):
        center_x, center_y = width // 2, height // 2
        for index, line in zip(range(self.sheet_size[0], self.sheet_size[1] + 1), self.chest_sheet):
            line[0].y = center_y + (index * self.scale)
            line[0].x2 = width
            line[0].y2 = center_y + (index * self.scale)
            line[1].x = center_x + (index * self.scale)
            line[1].x2 = center_x + (index * self.scale)
            line[1].y2 = height

    def on_mouse_press(self, x: int, y: int, button: int, modifiers: int, window: "ClientWindow"):
        if x > (window.width // 2 + self.scale * self.sheet_size[1]) or x < (window.width // 2 + self.scale * self.sheet_size[0]):
            return
        if y > (window.height // 2 + self.scale * self.sheet_size[1]) or y < (window.height // 2 + self.scale * self.sheet_size[0]):
            return
        dx_mouse = x - window.width // 2
        dy_mouse = y - window.height // 2
        pos_x = round(dx_mouse/self.scale)
        pos_y = round(dy_mouse/self.scale)
        pos_str = f'{pos_x}/{pos_y}'
        if button == 2:
            if self.nodes.get(pos_str):
                del self.nodes[pos_str]
            return
        color = (200, 24, 20, 200) if button == 1 else (24, 200, 20, 200)
        node = Circle(x=pos_x * self.scale + window.width // 2, y=pos_y * self.scale + window.height // 2,
                      radius=15, color=color, batch=self.batch)
        self.nodes[pos_str] = node

    def on_mouse_drag(self, x: int, y: int, dx: int, dy: int, buttons: int, modifiers: int, window: "ClientWindow"):
        self.on_mouse_press(x, y, buttons, modifiers, window)

