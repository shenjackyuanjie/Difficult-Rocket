#  -------------------------------
#  Difficult Rocket
#  Copyright © 2020-2023 by shenjackyuanjie 3695888@qq.com
#  All rights reserved
#  -------------------------------

# import math
import time
import random
import logging
import traceback

from pathlib import Path
from defusedxml.ElementTree import parse
from xml.etree.ElementTree import Element, ElementTree
from typing import List, TYPE_CHECKING, Union, Dict, Optional, Generator, Tuple

from pyglet.math import Vec4
from pyglet.text import Label
from pyglet.sprite import Sprite
# from pyglet.image import Texture
from pyglet.graphics import Batch, Group
from pyglet.shapes import Line, Rectangle
# pyglet OpenGL
from pyglet.gl import glViewport

from . import DR_mod_runtime

# Difficult Rocket
from Difficult_Rocket import DR_status
from Difficult_Rocket.utils.translate import Tr
from Difficult_Rocket.api.camera import CenterCamera
from Difficult_Rocket.api.types import Fonts, Options
from Difficult_Rocket.command.line import CommandText
from Difficult_Rocket.client.screen import BaseScreen
from .types import SR1Textures, SR1PartTexture, SR1PartData, SR1Rotation, xml_bool

if TYPE_CHECKING:
    from Difficult_Rocket.client import ClientWindow

if DR_mod_runtime.use_DR_rust:
    from .Difficult_Rocket_rs import (SR1PartList_rs,
                                      SR1Ship_rs)

logger = logging.getLogger('client.dr_game_sr1_ship')
logger.level = logging.DEBUG
sr_tr = Tr(lang_path=Path(__file__).parent / 'lang')


def get_sr1_part(part_xml: Element) -> Optional[SR1PartData]:
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
    return SR1PartData(x=part_x, y=part_y, id=part_id, p_type=part_type,
                       active=part_activate, angle=part_angle, angle_v=part_angle_v,
                       editor_angle=part_editor_angle, flip_x=part_flip_x,
                       flip_y=part_flip_y, explode=part_explode, textures=part_textures)


class SR1ShipRender_Option(Options):
    # debug option
    debug_d_pos: bool = False
    debug_mouse_pos: bool = False
    debug_mouse_d_pos: bool = False
    draw_size: Tuple[int, int] = (100, 100)


class SR1ShipRender(BaseScreen):
    """用于渲染 sr1 船的类"""

    def __init__(self,
                 main_window: "ClientWindow"):
        super().__init__(main_window)
        self.logger = logger
        logger.info(sr_tr().mod.info.setup.start())
        load_start_time = time.time_ns()
        self.rendered = False
        self.focus = True
        self.need_draw = False
        self.drawing = False
        self.need_update_parts = False
        self.render_option = SR1ShipRender_Option()
        self.dx = 0
        self.dy = 0
        self.main_batch = Batch()
        self.part_group = Group(10, parent=main_window.main_group)
        self.debug_label = Label(x=20, y=main_window.height - 100, font_size=DR_status.std_font_size,
                                 text='SR1 render!', font_name=Fonts.微软等宽无线,
                                 width=main_window.width - 20, height=20,
                                 anchor_x='left', anchor_y='top',
                                 batch=self.main_batch, group=Group(5, parent=self.part_group))
        self.render_d_line = Line(0, 0, 0, 0, width=5, color=(200, 200, 10, 255),
                                  batch=self.main_batch, group=Group(5, parent=self.part_group))
        self.render_d_line.visible = self.render_option.debug_mouse_d_pos
        self.render_d_label = Label('debug label NODATA', font_name=Fonts.微软等宽无线,
                                    x=main_window.width / 2, y=main_window.height / 2)
        self.render_d_label.visible = self.render_option.debug_d_pos

        # Optional data
        self.gen_draw: Optional[Generator] = None
        self.textures: Union[SR1Textures, None] = None
        self.xml_name: Optional[str] = None
        self.xml_doc: Optional[ElementTree] = None
        self.xml_root: Optional[Element] = None
        self.rust_ship: Optional[SR1Ship_rs] = None

        # List/Dict data
        self.part_data: Dict[int, SR1PartData] = {}
        self.parts_sprite: Dict[int, Sprite] = {}
        self.part_box_dict: Dict[int, Rectangle] = {}
        self.part_line_box: Dict[int, List[Line]] = {}
        self.part_line_list: List[Line] = []

        self.load_xml('assets/builtin/dock1.xml')

        load_end_time = time.time_ns()
        logger.info(sr_tr().mod.info.setup.use_time().format((load_end_time - load_start_time) / 1000000000))
        self.camera = CenterCamera(main_window, min_zoom=(1 / 2) ** 10, max_zoom=10)
        if DR_mod_runtime.use_DR_rust:
            self.rust_parts = None
            self.part_list_rs = SR1PartList_rs('assets/builtin/PartList.xml', 'default_part_list')

    def load_xml(self, file_path: str) -> bool:
        try:
            start_time = time.time_ns()
            logger.info(sr_tr().sr1.ship.xml.loading().format(file_path))
            cache_doc = parse(file_path)
            self.xml_doc = cache_doc
            self.xml_root = self.xml_doc.getroot()
            self.xml_name = file_path
            if DR_mod_runtime.use_DR_rust:
                self.rust_ship = SR1Ship_rs(file_path, 'assets/builtin/PartList.xml', 'a_new_ship')
            logger.info(sr_tr().sr1.ship.xml.load_done())
            logger.info(sr_tr().sr1.ship.xml.load_time().format(
                (time.time_ns() - start_time) / 1000000000))
            return True
        except Exception as e:
            print(e)
            return False

    def load_textures(self):
        self.textures = SR1Textures()

    def gen_sprite(self, part_datas: Dict[int, SR1PartData], each_count: int = 100) -> Generator:
        count = 0
        self.drawing = True
        for part_id, part in part_datas.items():
            # 下面就是调用 pyglet 去渲染的部分
            # render_scale = DR_status.gui_scale  # 这个是 DR 的缩放比例 可以调节的(
            # 主要是 Windows 下有一个缩放系数嘛，我待会试试这玩意能不能获取（估计得 ctypes
            # 在不缩放的情况下，XML的1个单位长度对应60个像素
            render_x = part.x * 60
            render_y = part.y * 60
            # 你就这里改吧
            cache_sprite = Sprite(img=self.textures.get_texture(part.textures),
                                  x=render_x, y=render_y, z=random.random(),
                                  batch=self.main_batch, group=self.part_group)
            # 你得帮我换算一下 XML 里的 x y 和这里的屏幕像素的关系（OK
            # 旋转啥的不是大问题, 我找你要那个渲染代码就是要 x y 的换算逻辑
            cache_sprite.rotation = SR1Rotation.get_rotation(part.angle)
            if part.flip_x:
                cache_sprite.scale_x = -1  # 就是直接取反缩放，应该没问题····吧？（待会试试就知道了
            if part.flip_y:
                cache_sprite.scale_y = -1
            cache_sprite.x = cache_sprite.x - cache_sprite.scale_x / 2
            cache_sprite.y = cache_sprite.y - cache_sprite.scale_y / 2
            self.parts_sprite[part.id] = cache_sprite

            if DR_mod_runtime.use_DR_rust:
                line_box_group = Group(6, parent=self.part_group)
                part_debug_box = self.rust_ship.get_part_box(part.id)
                if part_debug_box:
                    # 线框
                    part_line_box = []
                    width = 4
                    color = (random.randrange(0, 255), random.randrange(0, 255), random.randrange(0, 255),
                             random.randrange(100, 200))
                    part_line_box.append(Line(x=part_debug_box[0][0] * 30, y=part_debug_box[0][1] * 30,
                                              x2=part_debug_box[0][0] * 30, y2=part_debug_box[1][1] * 30,
                                              batch=self.main_batch, width=width, color=color, group=line_box_group))
                    part_line_box.append(Line(x=part_debug_box[0][0] * 30, y=part_debug_box[1][1] * 30,
                                              x2=part_debug_box[1][0] * 30, y2=part_debug_box[1][1] * 30,
                                              batch=self.main_batch, width=width, color=color, group=line_box_group))
                    part_line_box.append(Line(x=part_debug_box[1][0] * 30, y=part_debug_box[1][1] * 30,
                                              x2=part_debug_box[1][0] * 30, y2=part_debug_box[0][1] * 30,
                                              batch=self.main_batch, width=width, color=color, group=line_box_group))
                    part_line_box.append(Line(x=part_debug_box[1][0] * 30, y=part_debug_box[0][1] * 30,
                                              x2=part_debug_box[0][0] * 30, y2=part_debug_box[0][1] * 30,
                                              batch=self.main_batch, width=width, color=color, group=line_box_group))
                    self.part_line_box[part.id] = part_line_box
            # if not part_render:  # 如果不渲染(渲染有毛病)
            #     self.parts_sprite[part.id].visible = False
            count += 1
            if count >= each_count:
                count = 0
                yield count
        if DR_mod_runtime.use_DR_rust:
            connect_line_group = Group(7, parent=self.part_group)
            for connect in self.rust_ship.connection:
                # 连接线
                parent_part_data = self.part_data[connect[2]]
                child_part_data = self.part_data[connect[3]]
                color = (random.randrange(100, 255), random.randrange(0, 255), random.randrange(0, 255), 255)
                self.part_line_list.append(Line(x=parent_part_data.x * 60, y=parent_part_data.y * 60,
                                                x2=child_part_data.x * 60, y2=child_part_data.y * 60,
                                                batch=self.main_batch, group=connect_line_group,
                                                width=1, color=color))
                count += 1
                if count >= each_count * 3:
                    count = 0
                    yield count
        self.drawing = False
        raise GeneratorExit

    def render_ship(self):
        if self.textures is None:
            self.load_textures()
        logger.info(sr_tr().sr1.ship.ship.load().format(self.xml_name))
        start_time = time.perf_counter_ns()
        self.part_data: Dict[int, SR1PartData] = {}
        self.parts_sprite: Dict[int, Sprite] = {}
        self.part_line_box = {}
        self.part_line_list = []
        self.camera.zoom = 1.0
        self.camera.dx = 0
        self.camera.dy = 0
        parts = self.xml_root.find('Parts')
        for part_xml in parts:
            if part_xml.tag != 'Part':
                continue  # 如果不是部件，则跳过
            part = get_sr1_part(part_xml)
            if part.id in self.part_data:
                print(f'hey! warning! id{part.id}')
            self.part_data[part.id] = part
        # 调用生成器 减少卡顿
        try:
            self.gen_draw = self.gen_sprite(self.part_data)
            next(self.gen_draw)
        except GeneratorExit:
            self.drawing = False
        self.need_draw = False
        full_mass = 0
        if DR_mod_runtime.use_DR_rust:
            for part in self.part_data:
                full_mass += self.part_list_rs.get_part_type(self.part_data[part].p_type).mass * 500
        logger.info(sr_tr().sr1.ship.ship.load_time().format(
            (time.perf_counter_ns() - start_time) / 1000000000))
        logger.info(sr_tr().sr1.ship.ship.info().format(
            len(self.part_data), f'{full_mass}kg' if DR_mod_runtime.use_DR_rust else sr_tr().game.require_DR_rs()))
        self.rendered = True

    def draw_batch(self, window: "ClientWindow"):
        if self.rendered:
            self.render_d_label.text = f'x: {self.camera.dx} y: {self.camera.dy}'
            self.render_d_label.position = self.camera.dx + (self.window_pointer.width / 2), self.camera.dy + (
                    self.window_pointer.height / 2) + 10, 0  # 0 for z
            self.render_d_line.x2 = self.camera.dx
            self.render_d_line.y2 = self.camera.dy
        with self.camera:
            # glViewport(int(self.camera.dx), int(self.camera.dy), window.width // 2, window.height // 2)
            self.main_batch.draw()
            # glViewport(0, 0, window.width, window.height)

    def on_draw(self, window: "ClientWindow"):
        if self.need_draw:
            self.render_ship()

        if self.drawing:
            try:
                next(self.gen_draw)
            except GeneratorExit:
                self.drawing = False
                self.logger.info(sr_tr().sr1.ship.ship.render.done())

        self.debug_label.draw()

    def on_resize(self, width: int, height: int, window: "ClientWindow"):
        self.debug_label.y = height - 100
        if not self.rendered:
            return
        self.render_d_line.x2 = width // 2
        self.render_d_line.y2 = height // 2
        self.render_option.draw_size = (width, height)

    def on_mouse_scroll(self, x: int, y: int, scroll_x: int, scroll_y: int, window: "ClientWindow"):
        if not self.rendered:
            return
        mouse_dx = x - (window.width / 2)
        mouse_dy = y - (window.height / 2)
        # 鼠标缩放位置相对于屏幕中心的位置
        mouse_dx_d = mouse_dx - self.camera.dx
        mouse_dy_d = mouse_dy - self.camera.dy
        # 鼠标相对偏移量的偏移量
        if scroll_y == 0:
            zoom_d = 1
        else:
            zoom_d = ((2 ** scroll_y) - 1) * 0.5 + 1
        # 缩放的变换量
        if not (self.camera.zoom == 10 and scroll_y > 0):
            if self.camera.zoom * zoom_d >= 10:
                zoom_d = 10 / self.camera.zoom
                self.camera.zoom = 10
            else:
                self.camera.zoom *= zoom_d
            mouse_dx_d *= (1 - zoom_d)
            mouse_dy_d *= (1 - zoom_d)
            self.camera.dx += mouse_dx_d
            self.camera.dy += mouse_dy_d


    def on_command(self, command: CommandText, window: "ClientWindow"):
        self.logger.info(f'command: {command}')
        if command.find('render'):
            if command.find('reset'):
                self.camera.zoom = 1
                self.camera.dx = 0
                self.camera.dy = 0
                self.window_pointer.view = Vec4()
            else:
                self.need_draw = True
            print('应该渲染飞船的')
        elif command.find('debug'):
            if command.find('delta'):
                self.render_d_line.visible = not self.render_d_line.visible
                self.render_option.debug_mouse_d_pos = self.render_d_line.visible
                self.logger.info(f'sr1 mouse {self.render_option.debug_mouse_d_pos}')
            elif command.find('ship'):
                if self.rendered:
                    for index, sprite in self.parts_sprite.items():
                        sprite.visible = not sprite.visible

        elif command.find('get_buf'):

            def screenshot(window):
                from pyglet.gl import GLubyte, GL_RGBA, GL_UNSIGNED_BYTE, \
                    glReadPixels
                import pyglet
                format_str = "RGBA"
                buf = (GLubyte * (len(format_str) * window.width * window.height))()
                glReadPixels(0, 0, window.width, window.height, GL_RGBA, GL_UNSIGNED_BYTE, buf)
                return pyglet.image.ImageData(window.width, window.height, format_str, buf)

            image_data = screenshot(self.window_pointer)
            image_data.save('test.png')
        elif command.find('gen_img'):
            if not self.rendered:
                return
            if not DR_mod_runtime.use_DR_rust:
                # 这个功能依赖于 DR rs (简称,我懒得在Python端实现)
                return
            img_box = self.rust_ship.img_pos
            img_size = (img_box[2] - img_box[0] + 1000, img_box[3] - img_box[1] + 1000)
            # 中心点是左上角坐标
            img_center = (abs(img_box[0]), abs(img_box[3]))
            try:
                from PIL import Image
            except ImportError:
                traceback.print_exc()
                print('PIL not found')
                return
            img = Image.new('RGBA', img_size)
            for part, sprite in self.parts_sprite.items():
                sprite_img = sprite.image
                print(f"sprite_img: {sprite_img} {sprite_img.width} {sprite_img.height}")
                img_data = sprite_img.get_image_data()
                fmt = img_data.format
                if fmt != 'RGB':
                    fmt = 'RGBA'
                pitch = -(img_data.width * len(fmt))
                pil_image = Image.frombytes(fmt, (img_data.width, img_data.height), img_data.get_data(fmt, pitch))
                pil_image = pil_image.rotate(SR1Rotation.get_rotation(self.part_data[part].angle), expand=True)
                if self.part_data[part].flip_y:
                    pil_image.transpose(Image.FLIP_TOP_BOTTOM)
                if self.part_data[part].flip_x:
                    pil_image.transpose(Image.FLIP_LEFT_RIGHT)
                img.paste(pil_image, (
                int(self.part_data[part].x * 60 + img_center[0]), int(-self.part_data[part].y * 60 + img_center[1])),
                          pil_image)
            img.save(f'test{time.time()}.png', 'PNG')

        elif command.find('test'):
            if command.find('save'):
                if not self.rendered:
                    return
                if not DR_mod_runtime.use_DR_rust:
                    return
                logger.info(sr_tr().sr1.ship.save.start().format(self.rust_ship))
                self.rust_ship.save('./test-save.xml')
            elif command.find('render'):
                glViewport(0, 0, 1000, 1000)

    def on_mouse_drag(self, x: int, y: int, dx: int, dy: int, buttons: int, modifiers: int, window: "ClientWindow"):
        if not self.focus:
            return
        self.camera.dx += dx
        self.camera.dy += dy
        self.need_update_parts = True
        # self.update_parts()

    def on_file_drop(self, x: int, y: int, paths: List[str], window: "ClientWindow"):
        for path in paths:
            if self.load_xml(path):  # 加载成功一个就停下
                break
        self.render_ship()


if __name__ == '__main__':
    from objprint import op

    op(SR1ShipRender_Option())
