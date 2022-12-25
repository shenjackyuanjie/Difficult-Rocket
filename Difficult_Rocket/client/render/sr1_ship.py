#  -------------------------------
#  Difficult Rocket
#  Copyright © 2021-2022 by shenjackyuanjie 3695888@qq.com
#  All rights reserved
#  -------------------------------

# third party package
from defusedxml.ElementTree import DefusedXMLParser

# pyglet
from pyglet.graphics import Batch
from pyglet.resource import texture

# Difficult Rocket
from client.screen import BaseScreen
from Difficult_Rocket.client import ClientWindow


class SR1ShipRender(BaseScreen):
    """用于渲染 sr1 船的类"""

    def __init__(self, x: float, y: float,
                 scale: float,
                 xml_doc: DefusedXMLParser,
                 main_window: "ClientWindow"):
        super().__init__(main_window)
        self.x, self.y = x, y
        self.scale = scale
        self.xml_doc = xml_doc
        self.part_batch = Batch()

    def on_draw(self):
        ...

    def on_command(self, command):
        ...
