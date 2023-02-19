#  -------------------------------
#  Difficult Rocket
#  Copyright © 2020-2023 by shenjackyuanjie 3695888@qq.com
#  All rights reserved
#  -------------------------------

import time
import contextlib
from xml.etree import ElementTree
from xml.etree.ElementTree import Element
from typing import List, TYPE_CHECKING, Union, Dict, Optional, Callable, Generator

# third party package
from defusedxml.ElementTree import parse

# pyglet
from pyglet.math import Vec4
from pyglet.text import Label
from pyglet.shapes import Line
from pyglet.sprite import Sprite
from pyglet.graphics import Batch, Group

# Difficult Rocket
from Difficult_Rocket import DR_option
from Difficult_Rocket.api.types import Fonts, Options
from Difficult_Rocket.command.line import CommandText
from Difficult_Rocket.client.screen import BaseScreen
from Difficult_Rocket.api.types.SR1 import SR1Textures, SR1PartTexture, SR1PartData, SR1Rotation, xml_bool

if TYPE_CHECKING:
    from Difficult_Rocket.client import ClientWindow

if DR_option.use_DR_rust:
    from libs.Difficult_Rocket_rs import PartDatas, Camera_rs


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
    # print(f'id: {part_id:<4} type: {part_type:<10} x: {part_x} y: {part_y} activated: {part_activate} '
    #       f'angle: {part_angle} angle_v: {part_angle_v} editor_angle: {part_editor_angle} '
    #       f'flip_x: {part_flip_x} flip_y: {part_flip_y} explode: {part_explode} '
    #       f'textures: {SR1PartTexture.get_textures_from_type(part_type)}')
    return SR1PartData(x=part_x, y=part_y, id=part_id, p_type=part_type,
                       active=part_activate, angle=part_angle, angle_v=part_angle_v,
                       editor_angle=part_editor_angle, flip_x=part_flip_x,
                       flip_y=part_flip_y, explode=part_explode, textures=part_textures)


class _SR1ShipRender_Option(Options):
    # debug option
    debug_d_pos: bool = False
    debug_mouse_pos: bool = False
    debug_mouse_d_pos: bool = False


SR1ShipRender_Option = _SR1ShipRender_Option()


class SR1ShipRender(BaseScreen):
    """用于渲染 sr1 船的类"""

    def __init__(self,
                 main_window: "ClientWindow"):
        super().__init__(main_window)
        self.rendered = False
        self.focus = True
        self.need_draw = False
        self.drawing = False
        self.gen_draw: Optional[Generator] = None
        self.need_update_parts = False
        self.dx = 0
        self.dy = 0
        self.debug_line = Line(main_window.width / 2, main_window.height / 2,
                               main_window.width / 2, main_window.height / 2,
                               width=3, color=(200, 10, 200, 255))
        self.debug_line.visible = SR1ShipRender_Option.debug_d_pos
        self.debug_mouse_line = Line(main_window.width / 2, main_window.height / 2,
                                     main_window.width / 2, main_window.height / 2,
                                     width=3, color=(10, 200, 200, 255))
        self.debug_mouse_line.visible = SR1ShipRender_Option.debug_mouse_pos
        self.debug_mouse_delta_line = Line(main_window.width / 2, main_window.height / 2,
                                           main_window.width / 2, main_window.height / 2,
                                           width=2, color=(200, 200, 10, 255))
        self.debug_mouse_delta_line.visible = SR1ShipRender_Option.debug_mouse_d_pos
        self.debug_d_pos_label = Label('debug label NODATA', font_name=Fonts.微软等宽无线,
                                       x=main_window.width / 2, y=main_window.height / 2)
        self.debug_d_pos_label.visible = SR1ShipRender_Option.debug_d_pos
        self.debug_mouse_label = Label('debug mouse_label NODATA', font_name=Fonts.微软等宽无线,
                                       x=main_window.width / 2, y=main_window.height / 2)
        self.debug_mouse_label.visible = SR1ShipRender_Option.debug_mouse_pos
        self.textures: Union[SR1Textures, None] = None
        self.xml_doc: ElementTree = parse('configs/dock1.xml')
        self.xml_root: ElementTree.Element = self.xml_doc.getroot()
        self.part_batch = Batch()
        self.part_group = Group()
        self.debug_label = Label(x=20, y=main_window.height - 20, font_size=DR_option.std_font_size,
                                 text='SR1 render!', font_name=Fonts.微软等宽无线,
                                 width=main_window.width - 20, height=20,
                                 anchor_x='left', anchor_y='top')
        self.part_data: Dict[int, SR1PartData] = {}
        self.parts_sprite: Dict[int, Sprite] = {}
        if DR_option.use_DR_rust:
            self.camera_rs = Camera_rs(main_window,
                                       min_zoom=(1 / 2) ** 10, max_zoom=10)
            self.rust_parts = None

    def load_xml(self, file_path: str) -> bool:
        try:
            cache_doc = parse(file_path)
            self.xml_doc = cache_doc
            self.xml_root = self.xml_doc.getroot()
            return True
        except Exception:
            return False

    def load_textures(self):
        self.textures = SR1Textures()

    def gen_sprite(self, part_datas: Dict[int, SR1PartData], each_count: int = 100) -> Generator:
        count = 0
        self.drawing = True
        for part_id, part in part_datas.items():
            # 下面就是调用 pyglet 去渲染的部分
            # render_scale = DR_option.gui_scale  # 这个是 DR 的缩放比例 可以调节的(
            # 主要是 Windows 下有一个缩放系数嘛，我待会试试这玩意能不能获取（估计得 ctypes
            # 在不缩放的情况下，XML的1个单位长度对应60个像素
            render_x = part.x * 60
            render_y = part.y * 60
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
            cache_sprite.x = cache_sprite.x - cache_sprite.scale_x / 2
            cache_sprite.y = cache_sprite.y - cache_sprite.scale_y / 2
            self.parts_sprite[part.id] = cache_sprite
            # if not part_render:  # 如果不渲染(渲染有毛病)
            #     self.parts_sprite[part.id].visible = False
            count += 1
            if count >= each_count:
                count = 0
                yield each_count
        self.drawing = False
        raise GeneratorExit

    def render_ship(self):
        if self.textures is None:
            self.load_textures()
        start_time = time.perf_counter_ns()
        self.part_data: Dict[int, SR1PartData] = {}
        self.parts_sprite: Dict[int, Sprite] = {}
        self.camera_rs.zoom = 1.0
        if DR_option.use_DR_rust:
            self.camera_rs.dx = 0
            self.camera_rs.dy = 0
        parts = self.xml_root.find('Parts')
        for part_xml in parts:
            if part_xml.tag != 'Part':
                continue  # 如果不是部件，则跳过
            # print(f"tag: {part.tag} attrib: {part.attrib}")
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

        if DR_option.use_DR_rust:
            print(type(self.part_data))
            self.rust_parts = PartDatas(self.part_data)
            # print(self.rust_parts.get_rust_pointer())
        print(len(self.part_data))
        print(time.perf_counter_ns() - start_time)
        self.rendered = True

    def update_parts(self) -> bool:
        if not self.rendered:
            return False
        self.debug_line.x2, self.debug_line.y2 = self.camera_rs.dx + (
                    self.window_pointer.width / 2), self.camera_rs.dy + (
                                                         self.window_pointer.height / 2)
        self.debug_d_pos_label.text = f'x: {self.camera_rs.dx} y: {self.camera_rs.dy}'
        self.debug_d_pos_label.position = self.camera_rs.dx + (self.window_pointer.width / 2), self.camera_rs.dy + (
                self.window_pointer.height / 2) + 10, 0
        self.need_update_parts = False

    def on_draw(self):
        if self.need_draw:
            self.render_ship()

        if self.drawing:
            with contextlib.suppress(GeneratorExit):
                next(self.gen_draw)

        if self.need_update_parts:
            self.update_parts()
            self.need_update_parts = False

        with self.camera_rs:
            self.part_batch.draw()

        self.debug_label.draw()

        if SR1ShipRender_Option.debug_d_pos:
            self.debug_line.draw()
            self.debug_d_pos_label.draw()
        if SR1ShipRender_Option.debug_mouse_pos:
            self.debug_mouse_line.draw()
            self.debug_mouse_label.draw()
        if SR1ShipRender_Option.debug_mouse_d_pos:
            self.debug_mouse_delta_line.draw()

    def on_resize(self, width: int, height: int):
        if not self.rendered:
            return
        self.debug_line.x = width / 2
        self.debug_line.y = height / 2
        self.debug_mouse_line.x = width / 2
        self.debug_mouse_line.y = height / 2
        self.debug_mouse_delta_line.x = width / 2
        self.debug_mouse_delta_line.y = height / 2
        self.update_parts()

    def on_mouse_scroll(self, x: int, y: int, scroll_x: int, scroll_y: int):
        if not self.rendered:
            return
        mouse_dx = x - (self.window_pointer.width / 2)
        mouse_dy = y - (self.window_pointer.height / 2)
        # 鼠标缩放位置相对于屏幕中心的位置
        mouse_dx_d = mouse_dx - self.camera_rs.dx
        mouse_dy_d = mouse_dy - self.camera_rs.dy
        # 鼠标相对偏移量的偏移量
        if scroll_y > 0:
            zoom_d = ((2 ** scroll_y) - 1) * 0.5 + 1
        elif scroll_y == 0:
            zoom_d = 1
        else:
            zoom_d = ((2 ** scroll_y) - 1) * 0.5 + 1
        # 缩放的变换量
        if self.camera_rs.zoom == 10:
            if scroll_y >= 0:
                self.camera_rs.dx += mouse_dx_d * 0.5
                self.camera_rs.dy += mouse_dy_d * 0.5
            else:
                self.camera_rs.zoom *= zoom_d
                self.camera_rs.dx += mouse_dx_d
                self.camera_rs.dy += mouse_dy_d
        else:
            mouse_dx_d *= (1 - zoom_d)
            mouse_dy_d *= (1 - zoom_d)
            self.camera_rs.zoom *= zoom_d
            if self.camera_rs.zoom * zoom_d >= 10:
                zoom_d = 10 / self.camera_rs.zoom
                self.camera_rs.zoom = 10
            self.camera_rs.dx += mouse_dx_d
            self.camera_rs.dy += mouse_dy_d

        self.debug_mouse_line.x2, self.debug_mouse_line.y2 = x, y
        self.debug_mouse_delta_line.x2 = (mouse_dx - self.camera_rs.dx) * (1 - (0.5 ** scroll_y)) + (
                    self.window_pointer.width / 2)
        self.debug_mouse_delta_line.y2 = (mouse_dy - self.camera_rs.dy) * (1 - (0.5 ** scroll_y)) + (
                    self.window_pointer.height / 2)
        self.debug_mouse_label.text = f'x: {mouse_dx} y: {mouse_dy}'
        self.debug_mouse_label.position = x, y + 10, 0
        self.need_update_parts = True
        # self.update_parts()

    def on_command(self, command: CommandText):
        if command.re_match('render'):
            if command.re_match('reset'):
                self.camera_rs.zoom = 1
                self.camera_rs.dx = 0
                self.camera_rs.dy = 0
                self.window_pointer.view = Vec4()
            else:
                self.need_draw = True
            print('应该渲染飞船的')
        elif command.re_match('debug'):
            print('sr ?')
            if command.re_match('delta'):
                SR1ShipRender_Option.debug_d_pos = not SR1ShipRender_Option.debug_mouse_d_pos
                self.debug_line.visible = SR1ShipRender_Option.debug_d_pos
                self.debug_d_pos_label.visible = SR1ShipRender_Option.debug_d_pos
                # print('sr1 delta')
            elif command.re_match('mouse'):
                if command.re_match('delta'):
                    SR1ShipRender_Option.debug_mouse_pos = not SR1ShipRender_Option.debug_mouse_pos
                    self.debug_mouse_line.visible = SR1ShipRender_Option.debug_mouse_pos
                    self.debug_mouse_label.visible = SR1ShipRender_Option.debug_mouse_pos
                    # print('sr1 mouse delta')
                else:
                    SR1ShipRender_Option.debug_mouse_d_pos = not SR1ShipRender_Option.debug_mouse_d_pos
                    self.debug_mouse_delta_line.visible = SR1ShipRender_Option.debug_mouse_d_pos
                    # print('sr1 mouse')
        elif command.re_match('get_buf'):

            def screenshot(window):
                from libs.pyglet.gl import GLubyte, GLint, GL_RGBA, GL_UNSIGNED_BYTE, \
                    glReadPixels
                # from libs.pyglet.gl.gl_compat import GL_AUX_BUFFERS, GL_AUX0
                import pyglet
                width = window.width
                height = window.height
                format_str = "RGBA"
                buffer_count = GLint(0)
                # glGetIntegerv(GL_AUX_BUFFERS, buffer_count)
                print(buffer_count)
                buf = (GLubyte * (len(format_str) * width * height))()
                glReadPixels(0, 0, width, height, GL_RGBA, GL_UNSIGNED_BYTE, buf)
                # print(buf)
                return pyglet.image.ImageData(width, height, format_str, buf)

            image_data = screenshot(self.window_pointer)
            image_data.save('test.png')

    def on_mouse_drag(self, x: int, y: int, dx: int, dy: int, buttons: int, modifiers: int):
        if not self.focus:
            return
        self.camera_rs.dx += dx
        self.camera_rs.dy += dy
        self.need_update_parts = True
        # self.update_parts()

    def on_file_drop(self, x: int, y: int, paths: List[str]):
        for path in paths:
            if self.load_xml(path):  # 加载成功一个就停下
                break
        self.render_ship()
        print(paths)


if __name__ == '__main__':
    from objprint import op

    op(SR1ShipRender_Option)
