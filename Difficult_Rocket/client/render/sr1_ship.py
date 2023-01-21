#  -------------------------------
#  Difficult Rocket
#  Copyright © 2020-2023 by shenjackyuanjie 3695888@qq.com
#  All rights reserved
#  -------------------------------

import math
from xml.etree import ElementTree
from xml.etree.ElementTree import Element
from typing import List, TYPE_CHECKING, Union, Dict, Optional

# third party package
from defusedxml.ElementTree import parse

# pyglet
from pyglet.text import Label
from pyglet.sprite import Sprite
from pyglet.graphics import Batch, Group

# Difficult Rocket
from Difficult_Rocket import DR_option
from Difficult_Rocket.api.types import Fonts
from Difficult_Rocket.command.line import CommandText
from Difficult_Rocket.client.screen import BaseScreen
from Difficult_Rocket.api.types.SR1 import SR1Textures, SR1PartTexture, SR1PartData, SR1Rotation, xml_bool

if TYPE_CHECKING:
    from Difficult_Rocket.client import ClientWindow


def get_part_data_from_xml(part_xml: Element) -> Optional[SR1PartData]:
    if part_xml.tag != 'Part':
        return None
    # print(f"tag: {part.tag} attrib: {part.attrib}")
    part_id = int(part_xml.attrib.get('id'))
    part_type = part_xml.attrib.get('partType')
    part_x = float(part_xml.attrib.get('x'))
    part_y = float(part_xml.attrib.get('y'))
    part_activate = xml_bool(part_xml.attrib.get('activated'))
    part_angle = float(part_xml.attrib.get('angle'))
    part_angle_v = float(part_xml.attrib.get('angleV'))
    part_editor_angle = int(part_xml.attrib.get('editorAngle'))
    part_flip_x = xml_bool(part_xml.attrib.get('flippedX'))
    part_flip_y = xml_bool(part_xml.attrib.get('flippedY'))
    part_explode = xml_bool(part_xml.attrib.get('exploded'))
    if part_type not in SR1PartTexture.part_type_sprite:
        part_textures = None
    else:
        part_textures = SR1PartTexture.get_textures_from_type(part_type)
    # print(f'id: {part_id:<4} type: {part_type:<10} x: {part_x} y: {part_y} activated: {part_activate} '
    #       f'angle: {part_angle} angle_v: {part_angle_v} editor_angle: {part_editor_angle} '
    #       f'flip_x: {part_flip_x} flip_y: {part_flip_y} explode: {part_explode} '
    #       f'textures: {SR1PartTexture.get_textures_from_type(part_type)}')
    part_data = SR1PartData(x=part_x, y=part_y, id=part_id, type=part_type,
                            active=part_activate, angle=part_angle, angle_v=part_angle_v,
                            editor_angle=part_editor_angle, flip_x=part_flip_x,
                            flip_y=part_flip_y, explode=part_explode, textures=part_textures)
    return part_data


class SR1ShipRender(BaseScreen):
    """用于渲染 sr1 船的类"""

    def __init__(self,
                 main_window: "ClientWindow",
                 scale: float):
        super().__init__(main_window)
        self.rendered = False
        self.scale = scale
        self.focus = True
        self.dx = 0
        self.dy = 0
        self.textures: Union[SR1Textures, None] = None
        self.xml_doc: ElementTree = parse('configs/dock1.xml')
        self.xml_root: ElementTree.Element = self.xml_doc.getroot()
        self.part_batch = Batch()
        self.part_group = Group()
        self.debug_label = Label(x=20, y=main_window.height - 20, font_size=DR_option.std_font_size,
                                 text='SR1 render!', font_name=Fonts.微软等宽无线,
                                 width=main_window.width - 20, height=20,
                                 anchor_x='left', anchor_y='top',
                                 batch=self.part_batch)
        self.part_data: Dict[int, SR1PartData] = {}
        self.parts_sprite: Dict[int, Sprite] = {}

    def load_xml(self, file_path: str) -> bool:
        try:
            cache_doc = parse(file_path)
            self.xml_doc = cache_doc
            self.xml_root = self.xml_doc.getroot()
            return True
        except:
            return False

    def load_textures(self):
        self.textures = SR1Textures()

    def render_ship(self):
        if self.textures is None:
            self.load_textures()
        self.part_data: Dict[int, SR1PartData] = {}
        self.parts_sprite: Dict[int, Sprite] = {}
        parts = self.xml_root.find('Parts')
        for part_xml in parts:
            if part_xml.tag != 'Part':
                continue  # 如果不是部件，则跳过
            # print(f"tag: {part.tag} attrib: {part.attrib}")
            part_render = True
            part = get_part_data_from_xml(part_xml)
            if part.id in self.part_data:
                print(f'hey! warning! id{part.id}')
            self.part_data[part.id] = part
            # 下面就是调用 pyglet 去渲染的部分
            render_scale = DR_option.gui_scale  # 这个是 DR 的缩放比例 可以调节的(
            # 主要是 Windows 下有一个缩放系数嘛，我待会试试这玩意能不能获取（估计得 ctypes
            # 在不缩放的情况下，XML的1个单位长度对应60个像素
            render_x = part.x * render_scale * self.scale * 60 + self.window_pointer.width / 2 + self.dx
            render_y = part.y * render_scale * self.scale * 60 + self.window_pointer.height / 2 + self.dy
            # 你就这里改吧
            cache_sprite = Sprite(img=self.textures.get_texture(part.textures),
                                  x=render_x, y=render_y,
                                  batch=self.part_batch, group=self.part_group)
            # 你得帮我换算一下 XML 里的 x y 和这里的屏幕像素的关系（OK
            # 旋转啥的不是大问题, 我找你要那个渲染代码就是要 x y 的换算逻辑
            cache_sprite.rotation = SR1Rotation.get_rotation(part.angle)
            if part.flip_x:
                cache_sprite.scale_x = -1  # 就是直接取反缩放，应该没问题····吧？（待会试试就知道了
            if part.flip_y:
                cache_sprite.scale_y = -1
            cache_sprite.scale = self.scale * DR_option.gui_scale
            cache_sprite.x = cache_sprite.x - cache_sprite.scale_x / 2
            cache_sprite.y = cache_sprite.y - cache_sprite.scale_y / 2
            if not part_render:  # 如果不渲染(渲染有毛病)
                self.parts_sprite[part.id].visible = False
            self.parts_sprite[part.id] = cache_sprite
        self.rendered = True

    def update_parts(self) -> bool:
        if not self.rendered:
            return False
        for part_id in self.part_data:
            # x y scale
            self.parts_sprite[part_id].x = self.part_data[part_id].x * DR_option.gui_scale * self.scale * 60 + self.window_pointer.width / 2 + self.dx
            self.parts_sprite[part_id].y = self.part_data[part_id].y * DR_option.gui_scale * self.scale * 60 + self.window_pointer.height / 2 + self.dy
            self.parts_sprite[part_id].scale = self.scale * DR_option.gui_scale

    def on_draw(self):
        self.part_batch.draw()

    def on_resize(self, width: int, height: int):
        if not self.rendered:
            return
        self.update_parts()

    def on_mouse_scroll(self, x: int, y: int, scroll_x: int, scroll_y: int):
        if not self.rendered:
            return
        if not (self.scale + scroll_y * 0.1 == 0.0):
            self.scale += scroll_y * 0.1
        self.update_parts()

    def on_command(self, command: CommandText):
        if command.match('render'):
            # self.render_ship()
            print('应该渲染飞船的')

    def on_mouse_drag(self, x: int, y: int, dx: int, dy: int, buttons: int, modifiers: int):
        if not self.focus:
            return
        self.dx += dx
        self.dy += dy
        self.update_parts()

    def on_file_drop(self, x: int, y: int, paths: List[str]):
        for path in paths:
            if self.load_xml(path):  # 加载成功一个就停下
                break
        self.render_ship()
