#  -------------------------------
#  Difficult Rocket
#  Copyright © 2020-2023 by shenjackyuanjie 3695888@qq.com
#  All rights reserved
#  -------------------------------

from __future__ import annotations

import time
import random
import traceback

from pathlib import Path
from typing import Generator

from pyglet.gl import gl
from pyglet.math import Mat4
from pyglet.text import Label
from pyglet.sprite import Sprite
from pyglet.graphics import Batch, Group
from pyglet.shapes import Line, Box, Rectangle

# from pyglet.window import mouse

from . import DR_mod_runtime
from .types import SR1Textures

# Difficult Rocket
from Difficult_Rocket import DR_status
from Difficult_Rocket.utils.translate import Tr
from Difficult_Rocket.client import ClientWindow
from Difficult_Rocket.api.types import Fonts, Options
from Difficult_Rocket.command.line import CommandText
from Difficult_Rocket.client.screen import BaseScreen
from Difficult_Rocket.api.camera import CenterGroupCamera, GroupCamera
from Difficult_Rocket.gui.widget.button import OreuiButton


from lib_not_dr import loggers

if DR_mod_runtime.use_DR_rust:
    from .Difficult_Rocket_rs import (
        SR1PartList_rs,
        SR1Ship_rs,
        SR1PartData_rs,
        SR1PartType_rs,
        assert_ship,
        # SR1Connection_rs
    )


logger = loggers.get_logger("client.dr_game_sr1_ship")
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


class SR1ShipSelecter(BaseScreen):
    """
    SR1 飞船选择器
    考虑到 sss 写的那一大堆东西实在有点离谱
    所以单独拿出来写个screen
    我估计以后还得有一堆类似重构(瘫倒)
    """

    name = "DR_game_sr1_ship_selecter"

    def __init__(self, main_window: ClientWindow):
        super().__init__(main_window)
        self.main_batch = Batch()
        self.main_group = GroupCamera(window=main_window)
        self.width = 178
        self.height = main_window.height - 150
        self.dx = 10
        self.dy = 70
        self.folder_path: Path = Path("assets/ships")
        self.buttons: dict[Path, OreuiButton] = {}
        self.background = Rectangle(
            x=0,
            y=0,
            color=(174, 129, 255, 100),
            width=self.width,
            height=self.height,
            batch=self.main_batch,
            group=Group(10, parent=main_window.main_group),
        )
        self.set_folder(self.folder_path)

    def set_folder(self, path: Path):
        if not path.is_dir():
            logger.warn(
                sr_tr().sr1.ship.ship.folder.invalid().format(path), tag="ship explorer"
            )
            return
        self.folder_path = path
        self.buttons.clear()
        group = Group(20, parent=self.main_group)

        for file in path.iterdir():
            if not file.is_file:
                continue
            # 尝试加载一下
            if assert_ship(str(file)):  # type: ignore
                logger.info(
                    sr_tr().sr1.ship.ship.valid().format(file), tag="ship explorer"
                )
                button = OreuiButton(
                    x=4,
                    y=len(self.buttons) * -(30 + 5) + self.height,
                    width=170,
                    height=30,
                    text=file.stem,
                    toggle_mode=False,
                    auto_release=True,
                    batch=self.main_batch,
                    group=group,
                )
                self.buttons[file] = button
            else:
                logger.warn(
                    sr_tr().sr1.ship.ship.invaild().format(file), tag="ship explorer"
                )

    def on_mouse_motion(self, x: int, y: int, dx: int, dy: int, window: ClientWindow):
        for btn in self.buttons.values():
            btn.on_mouse_motion(x - self.dx, y - self.dy - self.main_group.view_y, dx, dy)

    def on_mouse_press(
        self, x: int, y: int, button: int, modifiers: int, window: ClientWindow
    ):
        return any(
            btn.on_mouse_press(
                x - self.dx, y - self.dy - self.main_group.view_y, button, modifiers
            )
            for btn in self.buttons.values()
        )

    def on_mouse_release(
        self, x: int, y: int, button: int, modifiers: int, window: ClientWindow
    ):
        for file_path, btn in self.buttons.items():
            if btn.on_mouse_release(
                x - self.dx, y - self.dy - self.main_group.view_y, button, modifiers
            ):
                logger.info(f"选到了 {file_path}", tag="ship explorer")
                self.dispatch_event("select_ship", self, file_path)

    def on_mouse_scroll(
        self, x: int, y: int, scroll_x: float, scroll_y: float, window: ClientWindow
    ):
        if self.dx < x < self.dx + self.width and self.dy < y < self.dy + self.height:
            self.main_group.view_y -= int(scroll_y * 50)
            if self.main_group.view_y < 0:
                self.main_group.view_y = 0
            if self.main_group.view_y > len(self.buttons) * (30 + 5) - self.height:
                self.main_group.view_y = len(self.buttons) * (30 + 5) - self.height
            return True

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
        if self.dx < x < self.dx + self.width and self.dy < y < self.dy + self.height:
            self.main_group.view_y += dy
            if self.main_group.view_y < 0:
                self.main_group.view_y = 0
            if self.main_group.view_y > len(self.buttons) * (30 + 5) - self.height:
                self.main_group.view_y = len(self.buttons) * (30 + 5) - self.height
            return True

    def draw_batch_(self, window: ClientWindow):
        gl.glEnable(gl.GL_SCISSOR_TEST)
        gl.glScissor(int(self.dx), int(self.dy), int(self.width), int(self.height))
        gl.glViewport(
            int(self.dx),
            int(self.dy),
            window.width,
            window.height,
        )
        self.main_batch.draw()
        gl.glViewport(0, 0, window.width, window.height)
        gl.glScissor(0, 0, window.width, window.height)
        gl.glDisable(gl.GL_SCISSOR_TEST)

    def on_resize(self, width: int, height: int, window: ClientWindow):
        self.height = height - 100
        self.width = min(200, width)

    def on_cleanup(self, window: ClientWindow):
        del self.buttons


SR1ShipSelecter.register_event_type("select_ship")


class SR1ShipEditor(BaseScreen):
    """SR1 飞船编辑器"""

    name = "DR_game_sr1_ship_editor"

    def __init__(self, main_window: ClientWindow):
        super().__init__(main_window)
        self.logger = logger
        logger.info(sr_tr().mod.info.setup.start(), tag="setup")
        load_start_time = time.time_ns()
        # status
        self.status = SR1ShipRenderStatus()

        selecter = main_window.get_sub_screen(SR1ShipSelecter.name)
        if selecter is None:
            self.logger.error("selecter not found")
        else:

            def select(explorer: SR1ShipSelecter, file_path: Path):
                self.load_xml(file_path)
                self.render_ship()

            selecter.set_handler("select_ship", select)

        self.dx = 0
        self.dy = 0
        self.width = main_window.width
        self.height = main_window.height

        self.main_batch = Batch()
        self.buttons_batch = Batch()
        self.ships_buttons_batch = Batch()
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
            thickness=5,
            color=(200, 200, 10, 255),
            batch=self.main_batch,
            group=Group(5, parent=self.part_group),
        )
        self.render_d_line.visible = self.status.draw_d_pos
        self.render_d_label = Label(
            "debug label NODATA",
            font_name=Fonts.微软等宽无线,
            x=main_window.width // 2,
            y=main_window.height // 2,
        )
        self.render_d_label.visible = self.status.draw_d_pos

        # Optional data
        self.textures: SR1Textures = SR1Textures()
        self.gen_draw: Generator | None = None
        self.rust_ship: SR1Ship_rs | None = None  # type: ignore
        self.ship_name: str | None = None

        # List/Dict data
        self.part_sprites: dict[int, tuple[Sprite, Box]] = {}
        self.part_outlines: dict[int, list[Line]] = {}
        self.connection_lines: list[Line] = []

        if DR_mod_runtime.use_DR_rust:
            self.rust_parts = None
            self.part_list_rs = SR1PartList_rs(  # type: ignore
                "assets/builtin/PartList.xml", "builtin_part_list"
            )

        # self.load_xml("assets/builtin/dock1.xml")

        load_end_time = time.time_ns()
        logger.info(
            sr_tr()
            .mod.info.setup.use_time()
            .format((load_end_time - load_start_time) / 1000000000),
            tag="setup",
        )

        # Buttons
        self.buttons_group = Group(100, parent=main_window.main_group)
        self.ships_buttons_group = Group(100, parent=main_window.main_group)

    @property
    def size(self) -> tuple[int, int]:
        """渲染器的渲染大小"""
        return self.width, self.height

    @size.setter
    def size(self, value: tuple[int, int]):
        if not self.width == value[0] or not self.height == value[1]:
            self.width, self.height = value

    def load_xml(self, file_path: Path) -> bool:
        """
        加载 xml 文件
        :param file_path:
        :return:
        """
        try:
            start_time = time.time_ns()
            logger.info(sr_tr().sr1.ship.xml.loading().format(file_path), tag="load_xml")
            self.ship_name = file_path.stem
            if DR_mod_runtime.use_DR_rust:
                self.rust_ship = SR1Ship_rs(  # type: ignore
                    str(file_path), self.part_list_rs, "a_new_ship"
                )
            logger.info(sr_tr().sr1.ship.xml.load_done(), tag="load_xml")
            logger.info(
                sr_tr()
                .sr1.ship.xml.load_time()
                .format((time.time_ns() - start_time) / 1000000000),
                tag="load_xml",
            )
            return True
        except Exception:
            traceback.print_exc()
            self.logger.error(traceback.format_exc(), tag="load_xml")
            return False

    def part_render_init(
        self,
        part_data: SR1PartData_rs,
        part_type: SR1PartType_rs,
        part_group: Group,
        line_group: Group,
        batch: Batch,
    ) -> tuple[Sprite, Box]:
        """
        还是重写一下渲染逻辑
        把渲染单个部件的逻辑提取出来放到这里
        """
        randomer = random.Random(part_data.id)
        texture = self.textures.get_texture(part_type.sprite)
        part_sprite = Sprite(
            img=texture,
            x=int(part_data.x * 60),
            y=int(part_data.y * 60),
            z=randomer.randint(-100, 100),
            batch=batch,
            group=part_group,
        )
        part_sprite.rotation = part_data.angle_r
        part_sprite.scale_x = -1 if part_data.flip_x else 1
        part_sprite.scale_y = -1 if part_data.flip_y else 1
        line_colors = (
            randomer.randrange(0, 255),
            randomer.randrange(0, 255),
            randomer.randrange(0, 255),
            200,
        )
        width = 4
        (x, y), (x2, y2) = part_data.get_part_box_by_type(part_type)
        box = Box(
            x=x * 30,
            y=y * 30,
            width=part_type.width * 30,
            height=part_type.height * 30,
            thickness=width,
            color=line_colors,
            batch=batch,
            group=line_group,
        )
        box.rotation = part_data.angle_r
        return part_sprite, box

    def sprite_batch(self, draw_batch: int = 500) -> Generator:
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
            self.rust_ship: SR1Ship_rs
            # 2 先渲染
            # 6 后渲染
            # 保证部件不会遮盖住连接线
            part_group = Group(2, parent=self.part_group)
            line_group = Group(6, parent=self.part_group)

            # 渲染连接的部件
            for part_type, part_data in self.rust_ship.as_list():
                # 渲染部件
                part_sprite, part_box = self.part_render_init(
                    part_data, part_type, part_group, line_group, self.main_batch
                )
                part_box.opacity = 100
                self.part_sprites[part_data.id] = (part_sprite, part_box)
                # TODO: 连接线渲染
                count += 2
                if count >= draw_batch:
                    yield count
                    count = 0

            # 渲染未连接的部件
            for part_groups, part_connections in self.rust_ship.disconnected_parts():
                for part_type, part_data in part_groups:
                    # 出于一些魔法原因, 这玩意居然能跑, part_groups 不需要加 [0]
                    # 未连接的需要同时把连接线也给渲染了
                    # TODO: 连接线渲染
                    part_sprite, part_box = self.part_render_init(
                        part_data, part_type, part_group, line_group, self.main_batch
                    )
                    part_box.opacity = 100
                    part_box._thickness = 2
                    part_box._update_vertices()
                    # ignore, pyglet 没写这个的 @property, 等我 issue + pr
                    # 未连接的部件透明度降低
                    part_sprite.opacity = 100
                    self.part_sprites[part_data.id] = (part_sprite, part_box)
                count += 2
                if count >= draw_batch:
                    yield count
                    count = 0

            # for connect in self.rust_ship.connections().get_raw_data():
            #     # 连接线
            #     # parent_part_data = cache[connect[2]][0][1]
            #     # child_part_data = cache[connect[3]][0][1]
            #     # color = (
            #     #     random.randrange(100, 255),
            #     #     random.randrange(0, 255),
            #     #     random.randrange(0, 255),
            #     #     255,
            #     # )
            #     # self.part_line_list.append(
            #     #     Line(
            #     #         x=parent_part_data.x * 60,
            #     #         y=parent_part_data.y * 60,
            #     #         x2=child_part_data.x * 60,
            #     #         y2=child_part_data.y * 60,
            #     #         batch=self.main_batch,
            #     #         group=connect_line_group,
            #     #         width=1,
            #     #         color=color,
            #     #     )
            #     # )
            #     count += 1
            #     if count >= draw_batch * 3:
            #         count = 0
            #         yield count

        self.status.draw_done = True
        raise GeneratorExit

    def render_ship(self):
        """
        渲染船
        """
        self.status.draw_done = False
        logger.info(sr_tr().sr1.ship.ship.load().format(self.ship_name), tag="ship")
        start_time = time.perf_counter_ns()
        self.part_sprites = {}
        self.connection_lines: list[Line] = []
        self.group_camera.reset()
        # 调用生成器 减少卡顿
        try:
            self.gen_draw = self.sprite_batch()
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
            .format((time.perf_counter_ns() - start_time) / 1000000000),
            tag="ship",
        )
        logger.info(
            sr_tr()
            .sr1.ship.ship.info()
            .format(
                len(self.rust_ship.as_list()),
                f"{full_mass}kg"
                if DR_mod_runtime.use_DR_rust
                else sr_tr().game.require_DR_rs(),
            ),
            tag="ship",
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

        # 外面这一层 gl 是用来实现子窗口的
        gl.glEnable(gl.GL_SCISSOR_TEST)
        gl.glScissor(int(self.dx), int(self.dy), int(self.width), int(self.height))
        gl.glViewport(
            int(self.dx),
            int(self.dy),
            self.window_pointer.width,
            self.window_pointer.height,
        )
        self.main_batch.draw()  # use group camera, no need to with
        self.buttons_batch.draw()  # use group camera, no need to with
        gl.glViewport(0, 0, self.window_pointer.width, self.window_pointer.height)
        gl.glScissor(0, 0, self.window_pointer.width, self.window_pointer.height)
        gl.glDisable(gl.GL_SCISSOR_TEST)

        explorer = window.get_sub_screen(SR1ShipSelecter.name)
        if explorer is not None:
            explorer.draw_batch(window)

    def on_draw(self, window: ClientWindow):
        if self.status.draw_call:
            self.render_ship()
        if not self.status.draw_done:
            try:
                if not isinstance(self.gen_draw, Generator):
                    return
                next(self.gen_draw)
            except (GeneratorExit, StopIteration):
                self.status.draw_done = True
                self.logger.info(sr_tr().sr1.ship.ship.render.done())
            except TypeError:
                pass

        # self.debug_label.draw()

    def on_resize(self, width: int, height: int, window: ClientWindow):
        self.debug_label.y = height - 100
        if not self.status.draw_done:
            return
        self.render_d_line.x2 = width // 2
        self.render_d_line.y2 = height // 2
        self.width = width
        self.height = height

    def on_mouse_scroll(
        self, x: int, y: int, scroll_x: float, scroll_y: float, window: ClientWindow
    ):
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
                self.group_camera.view_x += int(mouse_dx_d)
                self.group_camera.view_y += int(mouse_dy_d)
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
                    for index, sprite in self.part_sprites.values():
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
        # elif command.find("gen_img"):
        #     if not self.status.draw_done:
        #         return
        #     if not DR_mod_runtime.use_DR_rust:
        #         # 这个功能依赖于 DR rs (简称,我懒得在Python端实现)
        #         return
        #     img_box = self.rust_ship.img_pos
        #     img_size = (img_box[2] - img_box[0], img_box[3] - img_box[1])
        #     # 中心点是左上角坐标
        #     img_center = (abs(img_box[0]), abs(img_box[3]))
        #     try:
        #         from PIL import Image
        #     except ImportError:
        #         traceback.print_exc()
        #         print("PIL not found")
        #         return
        #     img = Image.new("RGBA", img_size)
        #     part_data = self.rust_ship.as_dict()
        #     for sprites, box in self.part_sprites.values():
        #         for index, sprite in enumerate(sprites):
        #             sprite_img = sprite.image
        #             print(
        #                 f"sprite_img: {sprite_img} {part_data[part][index][1].x * 60} "
        #                 f"{part_data[part][index][1].y * 60}"
        #             )
        #             img_data = sprite_img.get_image_data()
        #             fmt = img_data.format
        #             if fmt != "RGB":
        #                 fmt = "RGBA"
        #             pitch = -(img_data.width * len(fmt))
        #             pil_image = Image.frombytes(
        #                 fmt,
        #                 (img_data.width, img_data.height),
        #                 img_data.get_data(fmt, pitch),
        #             )

        #             pil_image = pil_image.rotate(
        #                 -SR1Rotation.get_rotation(part_data[part][index][1].angle),
        #                 expand=True,
        #             )

        #             if part_data[part][index][1].flip_y:
        #                 pil_image.transpose(Image.Transpose.FLIP_TOP_BOTTOM)
        #             if part_data[part][index][1].flip_x:
        #                 pil_image.transpose(Image.Transpose.FLIP_LEFT_RIGHT)

        #             img.paste(
        #                 pil_image,
        #                 (
        #                     int(part_data[part][index][1].x * 60 + img_center[0]),
        #                     int(-part_data[part][index][1].y * 60 + img_center[1]),
        #                 ),
        #             )

        #     img.save(f"test{time.time()}.png", "PNG")

        elif command.find("save"):
            print("应该保存飞船的")
            # if command.find("save"):
            if not self.status.draw_done:
                logger.warn("not draw done", tag="save ship")
                return
            if not DR_mod_runtime.use_DR_rust:
                return
            print("saving")
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

    def on_file_drop(self, x: int, y: int, paths: list[str], window: ClientWindow):  # type: ignore
        if len(paths) == 1:
            # only file/path
            self.load_xml(Path(paths[0]))
            self.render_ship()
        else:
            ...

    @property
    def view(self):
        return self.window_pointer.view

    @view.setter
    def view(self, value: Mat4):
        self.window_pointer.view = value
