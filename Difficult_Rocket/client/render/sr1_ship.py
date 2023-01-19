#  -------------------------------
#  Difficult Rocket
#  Copyright © 2021-2022 by shenjackyuanjie 3695888@qq.com
#  All rights reserved
#  -------------------------------

import math
from xml.etree import ElementTree
from typing import List, TYPE_CHECKING, Union, Dict

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
        self.parts_sprite: Dict[int, Sprite] = {}

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
            # 下面就是调用 pyglet 去渲染的部分
            render_scale = DR_option.gui_scale  # 这个是 DR 的缩放比例 可以调节的(
            # 主要是 Windows 下有一个缩放系数嘛，我待会试试这玩意能不能获取（估计得 ctypes
            # 在不缩放的情况下，XML的1个单位长度对应60个像素
            render_x = part_x * render_scale * 60 + self.window_pointer.width / 2
            render_y = part_y * render_scale * 60 + self.window_pointer.height / 2
            # 你就这里改吧
            cache_sprite = Sprite(img=self.textures.get_texture(part_data.textures),
                                  x=render_x, y=render_y,
                                  batch=self.part_batch, group=self.part_group)
            # 你得帮我换算一下 XML 里的 x y 和这里的屏幕像素的关系（OK
            # 旋转啥的不是大问题, 我找你要那个渲染代码就是要 x y 的换算逻辑
            if part_flip_x:
                cache_sprite.scale_x = -cache_sprite.scale_x  # 就是直接取反缩放，应该没问题····吧？（待会试试就知道了
            if part_flip_y:
                cache_sprite.scale_y = -cache_sprite.scale_y
            cache_sprite.x = cache_sprite.x - cache_sprite.scale_x / 2
            cache_sprite.y = cache_sprite.y - cache_sprite.scale_y / 2
            cache_sprite.rotation = part_data.angle / math.pi * 180
            if not part_render:  # 如果不渲染(渲染有毛病)
                self.parts_sprite[part_id].visible = False

            self.parts_sprite[part_id] = cache_sprite

    def on_draw(self):
        self.part_batch.draw()

    def on_file_drop(self, x: int, y: int, paths: List[str]):
        self.render_ship()
