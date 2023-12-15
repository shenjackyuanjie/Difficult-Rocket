#  -------------------------------
#  Difficult Rocket
#  Copyright © 2020-2023 by shenjackyuanjie 3695888@qq.com
#  All rights reserved
#  -------------------------------

import time
import random
import logging
import traceback

from pathlib import Path
from typing import List, Dict, Optional, Generator, Tuple

from pyglet.gl import gl
from pyglet.math import Mat4
from pyglet.text import Label
from pyglet.sprite import Sprite
from pyglet.graphics import Batch, Group
from pyglet.shapes import Line, Rectangle

from . import DR_mod_runtime
from .types import SR1Textures, SR1Rotation

# Difficult Rocket
from Difficult_Rocket import DR_status
from Difficult_Rocket.utils.translate import Tr
from Difficult_Rocket.client import ClientWindow
from Difficult_Rocket.api.types import Fonts, Options
from Difficult_Rocket.command.line import CommandText
from Difficult_Rocket.client.screen import BaseScreen
from Difficult_Rocket.api.camera import CenterGroupCamera
from Difficult_Rocket.api.gui.widget import PressTextButton

if DR_mod_runtime.use_DR_rust:
    from .Difficult_Rocket_rs import (
        SR1PartList_rs,
        SR1Ship_rs,
        SR1PartData_rs,
        SR1PartType_rs,
    )

logger = logging.getLogger("client.dr_game_sr1_ship")
logger.level = logging.DEBUG
sr_tr = Tr(lang_path=Path(__file__).parent / "lang")


class SR1ShipRenderStatus(Options):  # NOQA
    name = "SR1ShipRenderStatus"
    # main status
    draw_done: bool = False
    draw_call: bool = False
    update_call: bool = False
    focus: bool = True
    moving: bool = False

    # button status
    show_moving: bool = False
    show_focus: bool = False
    show_scale: bool = False

    # debug status
    draw_d_pos: bool = False
    draw_mouse_pos: bool = False
    draw_mouse_d_pos: bool = False


class SR1ShipRender(BaseScreen):
    """用于渲染 sr1 船的类"""

    name = "DR_game_sr1_ship_render"

    def __init__(self, main_window: ClientWindow):
        super().__init__(main_window)
        self.logger = logger
        logger.info(sr_tr().mod.info.setup.start())
        load_start_time = time.time_ns()
        # status
        self.status = SR1ShipRenderStatus()

        self.dx = 0
        self.dy = 0
        self.width = main_window.width
        self.height = main_window.height

        self.main_batch = Batch()
        self.group_camera = CenterGroupCamera(
            window=main_window,
            order=10,
            parent=main_window.main_group,
            min_zoom=(1 / 2) ** 10,
            max_zoom=10,
        )
        self.part_group = Group(0, parent=self.group_camera)

        self.debug_label = Label(
            x=20,
            y=main_window.height - 100,
            font_size=DR_status.std_font_size,
            text="SR1 render!",
            font_name=Fonts.微软等宽无线,
            width=main_window.width - 20,
            height=20,
            anchor_x="left",
            anchor_y="top",
            batch=self.main_batch,
            group=Group(5, parent=self.part_group),
        )
        self.render_d_line = Line(
            0,
            0,
            0,
            0,
            width=5,
            color=(200, 200, 10, 255),
            batch=self.main_batch,
            group=Group(5, parent=self.part_group),
        )
        self.render_d_line.visible = self.status.draw_d_pos
        self.render_d_label = Label(
            "debug label NODATA",
            font_name=Fonts.微软等宽无线,
            x=main_window.width / 2,
            y=main_window.height / 2,
        )
        self.render_d_label.visible = self.status.draw_d_pos

        self.test_button = PressTextButton(
            x=100,
            y=100,
            width=150,
            height=30,
            text="test button",
            batch=self.main_batch,
            group=Group(5, parent=main_window.main_group),
        )
        # self.test_button.push_handlers(main_window)
        main_window.push_handlers(self.test_button)

        # Optional data
        self.textures: SR1Textures = SR1Textures()
        self.gen_draw: Optional[Generator] = None
        self.rust_ship: Optional[SR1Ship_rs] = None
        self.ship_name: Optional[str] = None

        # List/Dict data
        self.parts_sprite: Dict[int, List[Sprite]] = {}
        self.part_box_dict: Dict[int, Rectangle] = {}
        self.part_line_box: Dict[int, List[Line]] = {}
        self.part_line_list: List[Line] = []

        if DR_mod_runtime.use_DR_rust:
            self.rust_parts = None
            self.part_list_rs = SR1PartList_rs(
                "assets/builtin/PartList.xml", "builtin_part_list"
            )

        self.load_xml("assets/builtin/dock1.xml")

        load_end_time = time.time_ns()
        logger.info(
            sr_tr()
            .mod.info.setup.use_time()
            .format((load_end_time - load_start_time) / 1000000000)
        )

    @property
    def size(self) -> Tuple[int, int]:
        """渲染器的渲染大小"""
        return self.width, self.height

    @size.setter
    def size(self, value: Tuple[int, int]):
        if not self.width == value[0] or not self.height == value[1]:
            self.width, self.height = value

    def load_xml(self, file_path: str) -> bool:
        """
        加载 xml 文件
        :param file_path:
        :return:
        """
        try:
            start_time = time.time_ns()
            logger.info(sr_tr().sr1.ship.xml.loading().format(file_path))
            self.ship_name = file_path.split("/")[-1].split(".")[0]
            if DR_mod_runtime.use_DR_rust:
                self.rust_ship = SR1Ship_rs(file_path, self.part_list_rs, "a_new_ship")
            logger.info(sr_tr().sr1.ship.xml.load_done())
            logger.info(
                sr_tr()
                .sr1.ship.xml.load_time()
                .format((time.time_ns() - start_time) / 1000000000)
            )
            return True
        except Exception:
            traceback.print_exc()
            self.logger.error(traceback.format_exc())
            return False

    def gen_sprite(self, each_count: int = 100) -> Generator:
        """
        生成 sprite
        通过生成器减少一次性渲染的压力
        :param each_count: 每次生成的数量 (默认 100) (过大会导致卡顿)
        :return: 生成器
        """
        count = 0
        self.status.draw_done = False
        # rust 渲染
        if DR_mod_runtime.use_DR_rust:
            cache = self.rust_ship.as_dict()
            part_group = Group(2, parent=self.part_group)
            line_box_group = Group(6, parent=self.part_group)
            for p_id, parts in cache.items():
                p_id: int
                parts: List[Tuple[SR1PartType_rs, SR1PartData_rs]]
                batch = []
                for p_type, p_data in parts:
                    sprite_name = self.part_list_rs.get_part_type(
                        p_data.part_type_id
                    ).sprite
                    part_sprite = Sprite(
                        img=self.textures.get_texture(sprite_name),
                        x=p_data.x * 60,
                        y=p_data.y * 60,
                        z=random.random(),
                        batch=self.main_batch,
                        group=part_group,
                    )
                    part_sprite.rotation = p_data.angle_r
                    part_sprite.scale_x = -1 if p_data.flip_x else 1
                    part_sprite.scale_y = -1 if p_data.flip_y else 1

                    batch.append(part_sprite)
                part_box = self.rust_ship.get_part_box(p_id)
                if part_box:
                    # 线框
                    part_line_box = []
                    width = 4
                    color = (
                        random.randrange(0, 255),
                        random.randrange(0, 255),
                        random.randrange(0, 255),
                        random.randrange(100, 200),
                    )
                    (x, y), (x2, y2) = part_box
                    part_line_box.append(
                        Line(
                            x=x * 30,
                            y=y * 30,
                            x2=x * 30,
                            y2=y2 * 30,
                            batch=self.main_batch,
                            width=width,
                            color=color,
                            group=line_box_group,
                        )
                    )
                    part_line_box.append(
                        Line(
                            x=x * 30,
                            y=y2 * 30,
                            x2=x2 * 30,
                            y2=y2 * 30,
                            batch=self.main_batch,
                            width=width,
                            color=color,
                            group=line_box_group,
                        )
                    )
                    part_line_box.append(
                        Line(
                            x=x2 * 30,
                            y=y2 * 30,
                            x2=x2 * 30,
                            y2=y * 30,
                            batch=self.main_batch,
                            width=width,
                            color=color,
                            group=line_box_group,
                        )
                    )
                    part_line_box.append(
                        Line(
                            x=x2 * 30,
                            y=y * 30,
                            x2=x * 30,
                            y2=y * 30,
                            batch=self.main_batch,
                            width=width,
                            color=color,
                            group=line_box_group,
                        )
                    )
                    # 直接用循环得了
                    self.part_line_box[p_id] = part_line_box
                self.parts_sprite[p_id] = batch
                count += 1
                if count >= each_count:
                    count = 0
                    yield
            connect_line_group = Group(7, parent=self.part_group)
            for connect in self.rust_ship.connection:
                # 连接线
                parent_part_data = cache[connect[2]][0][1]
                child_part_data = cache[connect[3]][0][1]
                color = (
                    random.randrange(100, 255),
                    random.randrange(0, 255),
                    random.randrange(0, 255),
                    255,
                )
                self.part_line_list.append(
                    Line(
                        x=parent_part_data.x * 60,
                        y=parent_part_data.y * 60,
                        x2=child_part_data.x * 60,
                        y2=child_part_data.y * 60,
                        batch=self.main_batch,
                        group=connect_line_group,
                        width=1,
                        color=color,
                    )
                )
                count += 1
                if count >= each_count * 3:
                    count = 0
                    yield count

        # python 渲染
        # for part_id, part in part_datas.items():
        #     # 下面就是调用 pyglet 去渲染的部分
        #     # render_scale = DR_status.gui_scale  # 这个是 DR 的缩放比例 可以调节的
        #     # 在不缩放的情况下，XML的1个单位长度对应60个像素
        #     # render_x = part.x * 60
        #     # render_y = part.y * 60
        #     # cache_sprite = Sprite(img=self.textures.get_texture(part.textures),
        #     #                       x=render_x, y=render_y, z=random.random(),
        #     #                       batch=self.main_batch, group=self.part_group)
        #     # # 你得帮我换算一下 XML 里的 x y 和这里的屏幕像素的关系
        #     # # 旋转啥的不是大问题, 我找你要那个渲染代码就是要 x y 的换算逻辑
        #     # cache_sprite.rotation = SR1Rotation.get_rotation(part.angle)
        #     # if part.flip_x:
        #     #     cache_sprite.scale_x = -1
        #     # if part.flip_y:
        #     #     cache_sprite.scale_y = -1
        #     # self.parts_sprite[part.id] = cache_sprite
        #
        #     if DR_mod_runtime.use_DR_rust:
        #     count += 1
        #     if count >= each_count:
        #         count = 0
        #         yield count
        self.status.draw_done = True
        raise GeneratorExit

    def render_ship(self):
        """
        渲染船
        """
        self.status.draw_done = False
        logger.info(sr_tr().sr1.ship.ship.load().format(self.ship_name))
        start_time = time.perf_counter_ns()
        self.parts_sprite: Dict[int, Sprite] = {}
        self.part_line_box = {}
        self.part_line_list = []
        self.group_camera.reset()
        # 调用生成器 减少卡顿
        try:
            self.gen_draw = self.gen_sprite()
            if not self.status.draw_done:
                next(self.gen_draw)
        except (GeneratorExit, StopIteration):
            self.status.draw_done = True
        self.status.draw_call = False
        full_mass = 0
        if DR_mod_runtime.use_DR_rust:
            full_mass = self.rust_ship.mass
        logger.info(
            sr_tr()
            .sr1.ship.ship.load_time()
            .format((time.perf_counter_ns() - start_time) / 1000000000)
        )
        logger.info(
            sr_tr()
            .sr1.ship.ship.info()
            .format(
                len(self.rust_ship.as_list()),
                f"{full_mass}kg"
                if DR_mod_runtime.use_DR_rust
                else sr_tr().game.require_DR_rs(),
            )
        )

    def draw_batch(self, window: ClientWindow):
        if self.status.draw_done:
            self.render_d_label.text = (
                f"x: {self.group_camera.view_x} y: {self.group_camera.view_y}"
            )
            self.render_d_label.position = (
                self.group_camera.view_x + (self.window_pointer.width / 2),
                self.group_camera.view_y + (self.window_pointer.height / 2) + 10,
                0,
            )  # 0 for z
            self.render_d_line.x2 = self.group_camera.view_x
            self.render_d_line.y2 = self.group_camera.view_y

        gl.glEnable(gl.GL_SCISSOR_TEST)
        gl.glScissor(int(self.dx), int(self.dy), int(self.width), int(self.height))
        gl.glViewport(
            int(self.dx),
            int(self.dy),
            self.window_pointer.width,
            self.window_pointer.height,
        )
        self.main_batch.draw()  # use group camera, no need to with
        gl.glViewport(0, 0, self.window_pointer.width, self.window_pointer.height)
        gl.glScissor(0, 0, self.window_pointer.width, self.window_pointer.height)
        gl.glDisable(gl.GL_SCISSOR_TEST)

    def on_draw(self, dt: float, window):  # TODO: wait for pyglet 2.1
    # def on_draw(self, window: ClientWindow):
        if self.status.draw_call:
            self.render_ship()

        if not self.status.draw_done:
            try:
                next(self.gen_draw)
            except (GeneratorExit, StopIteration):
                self.status.draw_done = True
                self.logger.info(sr_tr().sr1.ship.ship.render.done())
            except TypeError:
                pass

        self.debug_label.draw()

    def on_resize(self, width: int, height: int, window: ClientWindow):
        self.debug_label.y = height - 100
        if not self.status.draw_done:
            return
        self.render_d_line.x2 = width // 2
        self.render_d_line.y2 = height // 2
        self.test_button._update_position()

    def on_mouse_scroll(
        self, x: int, y: int, scroll_x: int, scroll_y: int, window: ClientWindow
    ):
        if not self.status.draw_done:
            return
        if self.status.focus:
            mouse_dx = x - (self.width / 2) + self.dx
            mouse_dy = y - (self.height / 2) + self.dy
            # 鼠标缩放位置相对于屏幕中心的位置
            mouse_dx_d = mouse_dx - self.group_camera.view_x
            mouse_dy_d = mouse_dy - self.group_camera.view_y
            # 鼠标相对偏移量的偏移量
            if scroll_y == 0:
                zoom_d = 1
            else:
                zoom_d = ((2**scroll_y) - 1) * 0.5 + 1
            # 缩放的变换量
            if not (self.group_camera.zoom == 10 and scroll_y > 0):
                if self.group_camera.zoom * zoom_d >= 10:
                    zoom_d = 10 / self.group_camera.zoom
                    self.group_camera.zoom = 10
                else:
                    self.group_camera.zoom *= zoom_d
                mouse_dx_d *= 1 - zoom_d
                mouse_dy_d *= 1 - zoom_d
                self.group_camera.view_x += mouse_dx_d
                self.group_camera.view_y += mouse_dy_d
        elif self.status.moving:
            # 如果是在移动整体渲染位置
            size_x, size_y = self.size
            size_x += round(scroll_y) * 10
            size_y += round(scroll_y) * 10
            if size_x < 10:
                size_x = 10
            if size_y < 10:
                size_y = 10
            self.size = size_x, size_y

    def on_command(self, command: CommandText, window: ClientWindow):
        """解析命令"""
        self.logger.info(f"command: {command}")
        if command.find("render"):
            if command.find("reset"):
                self.group_camera.reset()
            else:
                self.status.draw_call = True
            print("应该渲染飞船的")

        elif command.find("debug"):
            if command.find("delta"):
                self.render_d_line.visible = not self.render_d_line.visible
                self.status.draw_mouse_d_pos = self.render_d_line.visible
                self.logger.info(f"sr1 mouse {self.status.draw_mouse_d_pos}")
            elif command.find("ship"):
                if self.status.draw_done:
                    for index, sprite in self.parts_sprite.items():
                        sprite.visible = not sprite.visible

        elif command.find("get_buf"):

            def screenshot(window):
                """
                从窗口截图
                :param window:
                :return:
                """
                from pyglet.gl import GLubyte, GL_RGBA, GL_UNSIGNED_BYTE, glReadPixels
                import pyglet

                format_str = "RGBA"
                buf = (GLubyte * (len(format_str) * window.width * window.height))()
                glReadPixels(
                    0, 0, window.width, window.height, GL_RGBA, GL_UNSIGNED_BYTE, buf
                )
                return pyglet.image.ImageData(
                    window.width, window.height, format_str, buf
                )

            image_data = screenshot(self.window_pointer)
            image_data.save("test.png")
        elif command.find("gen_img"):
            if not self.status.draw_done:
                return
            if not DR_mod_runtime.use_DR_rust:
                # 这个功能依赖于 DR rs (简称,我懒得在Python端实现)
                return
            img_box = self.rust_ship.img_pos
            img_size = (img_box[2] - img_box[0], img_box[3] - img_box[1])
            # 中心点是左上角坐标
            img_center = (abs(img_box[0]), abs(img_box[3]))
            try:
                from PIL import Image
            except ImportError:
                traceback.print_exc()
                print("PIL not found")
                return
            img = Image.new("RGBA", img_size)
            part_data = self.rust_ship.as_dict()
            for part, sprites in self.parts_sprite.items():
                for index, sprite in enumerate(sprites):
                    sprite_img = sprite.image
                    print(
                        f"sprite_img: {sprite_img} {part_data[part][index][1].x * 60} {part_data[part][index][1].y * 60}"
                    )
                    img_data = sprite_img.get_image_data()
                    fmt = img_data.format
                    if fmt != "RGB":
                        fmt = "RGBA"
                    pitch = -(img_data.width * len(fmt))
                    pil_image = Image.frombytes(
                        fmt,
                        (img_data.width, img_data.height),
                        img_data.get_data(fmt, pitch),
                    )

                    pil_image = pil_image.rotate(
                        -SR1Rotation.get_rotation(part_data[part][index][1].angle),
                        expand=True,
                    )

                    if part_data[part][index][1].flip_y:
                        pil_image.transpose(Image.FLIP_TOP_BOTTOM)
                    if part_data[part][index][1].flip_x:
                        pil_image.transpose(Image.FLIP_LEFT_RIGHT)

                    img.paste(
                        pil_image,
                        (
                            int(part_data[part][index][1].x * 60 + img_center[0]),
                            int(-part_data[part][index][1].y * 60 + img_center[1]),
                        ),
                    )

            img.save(f"test{time.time()}.png", "PNG")

        elif command.find("test"):
            if command.find("save"):
                if not self.status.draw_done:
                    return
                if not DR_mod_runtime.use_DR_rust:
                    return
                logger.info(sr_tr().sr1.ship.save.start().format(self.rust_ship))
                self.rust_ship.save("./test-save.xml")

    def on_mouse_drag(
        self,
        x: int,
        y: int,
        dx: int,
        dy: int,
        buttons: int,
        modifiers: int,
        window: ClientWindow,
    ):
        if self.status.focus:
            self.group_camera.view_x += dx
            self.group_camera.view_y += dy
            self.status.update_call = True
        elif self.status.moving:
            # 如果是在移动整体渲染位置
            self.dx += dx
            self.dy += dy

    def on_file_drop(self, x: int, y: int, paths: List[str], window: ClientWindow):
        if len(paths) > 1:
            for path in paths:
                try:
                    self.load_xml(path)
                except Exception:
                    traceback.print_exc()
        else:
            if Path(paths[0]).is_dir():
                for path in Path(paths[0]).glob("*.xml"):
                    try:
                        self.load_xml(str(path))
                    except ValueError:
                        traceback.print_exc()
            if self.load_xml(paths[0]):
                self.render_ship()
        # for path in paths:
        #     if self.load_xml(path):  # 加载成功一个就停下
        #         break
        # self.render_ship()

    @property
    def view(self):
        return self.window_pointer.view

    @view.setter
    def view(self, value: Mat4):
        self.window_pointer.view = value


if __name__ == "__main__":
    from objprint import op

    op(SR1ShipRenderStatus())
