#  -------------------------------
#  Difficult Rocket
#  Copyright © 2021-2022 by shenjackyuanjie 3695888@qq.com
#  All rights reserved
#  -------------------------------

from xml.etree import ElementTree
from typing import List, TYPE_CHECKING, Union

# third party package
from defusedxml.ElementTree import parse

# pyglet
from pyglet.graphics import Batch, Group
from pyglet.sprite import Sprite

# Difficult Rocket
from Difficult_Rocket import DR_option
from Difficult_Rocket.command.line import CommandText
from Difficult_Rocket.client.screen import BaseScreen
from Difficult_Rocket.api.types.SR1 import SR1Textures, SR1PartTexture, SR1PartData

if TYPE_CHECKING:
    from Difficult_Rocket.client import ClientWindow


class SR1ShipRender(BaseScreen):
    """用于渲染 sr1 船的类"""

    def __init__(self,
                 main_window: "ClientWindow",
                 scale: float):
        super().__init__(main_window)
        self.scale = scale
        self.textures: Union[SR1Textures, None] = None
        self.xml_doc = parse('configs/dock1.xml')
        self.xml_root: ElementTree.Element = self.xml_doc.getroot()
        self.part_batch = Batch()
        self.part_group = Group()
        self.part_data = {}
        self.parts_sprite = {}

    def load_textures(self):
        self.textures = SR1Textures()

    def render_ship(self):
        if self.textures is None:
            self.load_textures()
        parts = self.xml_root.find('Parts')
        for part in parts:
            if part.tag != 'Part':
                continue  # 如果不是部件，则跳过
            # print(f"tag: {part.tag} attrib: {part.attrib}")
            part_render = True
            part_id = int(part.attrib.get('id'))
            part_type = part.attrib.get('partType')
            part_x = float(part.attrib.get('x'))
            part_y = float(part.attrib.get('y'))
            part_activate = not not (part.attrib.get('activated') or 0)
            part_angle = float(part.attrib.get('angle'))
            part_angle_v = float(part.attrib.get('angleV'))
            part_editor_angle = int(part.attrib.get('editorAngle'))
            part_flip_x = not not (part.attrib.get('flippedX') or 0)
            part_flip_y = not not (part.attrib.get('flippedY') or 0)
            part_explode = not not (part.attrib.get('exploded') or 0)
            if part_type not in SR1PartTexture.part_type_sprite:
                part_render = False
                print('Textures None found!')
                part_textures = None
            else:
                part_textures = SR1PartTexture.get_sprite_from_type(part_type)
            print(f'id: {part_id:<4} type: {part_type:<10} x: {part_x} y: {part_y} activated: {part_activate} '
                  f'angle: {part_angle} angle_v: {part_angle_v} editor_angle: {part_editor_angle} '
                  f'flip_x: {part_flip_x} flip_y: {part_flip_y} explode: {part_explode} '
                  f'textures: {SR1PartTexture.get_sprite_from_type(part_type)}')
            if part_id in self.part_data:
                print(f'hey! warning! id{part_id}')
            part_data = SR1PartData(x=part_x, y=part_y, id=part_id, type=part_type,
                                    angle=part_angle, angle_v=part_angle_v,
                                    editor_angle=part_editor_angle, flip_x=part_flip_x,
                                    flip_y=part_flip_y, explode=part_explode, textures=part_textures)
            self.part_data[part_id] = part_data
            self.parts_sprite[part_id] = Sprite(img=self.textures.get_texture(part_data.textures),
                                                x=10, y=10, batch=self.part_batch, group=self.part_group)

    def on_draw(self):
        self.part_batch.draw()

    def on_file_drop(self, x: int, y: int, paths: List[str]):
        self.scale = DR_option.gui_scale
        self.render_ship()
        ...

    def on_command(self, command: CommandText):
        if command.match('render'):
            print('rua, render ship!')
            self.render_ship()
