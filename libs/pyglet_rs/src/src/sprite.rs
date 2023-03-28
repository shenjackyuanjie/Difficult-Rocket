/*
 * -------------------------------
 * Difficult Rocket
 * Copyright © 2020-2023 by shenjackyuanjie 3695888@qq.com
 * All rights reserved
 * -------------------------------
 */

use pyo3::intern;
use pyo3::prelude::*;

/// Instance of an on-screen image
/// See the module documentation for usage.
#[pyclass(name = "Sprite_rs", subclass)]
#[pyo3(text_signature = "(img, x=0.0, y=0.0, z=0.0, \
                          blend_src=770, blend_dest=771, \
                          batch=None, group=None, \
                          subpixel=False, program=None)")]
pub struct Sprite {
    // render
    pub subpixel: bool,
    pub batch: Py<PyAny>,
    pub group: Option<Py<PyAny>>,
    pub user_group: Option<Py<PyAny>>,
    pub group_class: Py<PyAny>,
    // view
    pub x: f64,
    pub y: f64,
    pub z: f64,
    pub scale: f64,
    pub scale_x: f64,
    pub scale_y: f64,
    pub visible: bool,
    pub vertex_list: Option<Vec<()>>,
    // frame
    pub frame_index: u32,
    pub next_dt: f64,
    #[pyo3(get)]
    pub program: Option<Py<PyAny>>,
    pub animation: Option<Py<PyAny>>,
    pub texture: Option<Py<PyAny>>,
    pub paused: bool,
    // other
    pub rgba: (u8, u8, u8, u8),
}

#[pymethods]
impl Sprite {
    /// python code:
    /// 366:
    /// if isinstance(img, image.Animation):
    ///     self._animation = img
    ///     self._texture = img.frames[0].image.get_texture()
    ///     self._next_dt = img.frames[0].duration
    ///     if self._next_dt:
    ///         clock.schedule_once(self._animate, self._next_dt)
    /// else:
    ///     self._texture = img.get_texture()
    /// 375:
    /// if not program:
    ///     if isinstance(img, image.TextureArrayRegion):
    ///         self._program = get_default_array_shader()
    ///     else:
    ///         self._program = get_default_shader()
    /// else:
    ///     self._program = program
    /// 383:
    /// self._batch = batch or graphics.get_default_batch()
    /// self._user_group = group
    /// self._group = self.group_class(self._texture, blend_src, blend_dest, self.program, group)
    /// self._subpixel = subpixel
    /// 387:
    /// self._create_vertex_list()
    #[new]
    fn new(
        py_: Python,
        img: &PyAny,
        x: f64,
        y: f64,
        z: f64,
        blend_src: u32, // default 770 (GL_SRC_ALPHA)
        blend_dest: u32, // default 771 (GL_ONE_MINUS_SRC_ALPHA)
        batch_: &PyAny,
        group: &PyAny,
        subpixel: bool,
        program_: &PyAny,
    ) -> Self {
        let texture;
        let batch;
        let mut next_dt = 0.0;
        let mut animation = None;
        let mut program = program_;
        let sprite_group_class = PyModule::import(py_, "pyglet.sprite")
            .unwrap()
            .getattr("SpriteGroup")
            .unwrap();
        // 366
        let animation_class = PyModule::import(py_, "pyglet.image.Animation")
            .unwrap()
            .getattr("Animation")
            .unwrap();
        if img.is_instance(animation_class).unwrap() {
            animation = Some(img.into());
            texture = img
                .getattr(intern!(img.py(), "frames"))
                .unwrap()
                .get_item(0)
                .unwrap()
                .getattr(intern!(img.py(), "image"))
                .unwrap()
                .call_method0(intern!(img.py(), "get_texture"))
                .unwrap();
            let _next_dt = img
                .getattr(intern!(img.py(), "frames"))
                .unwrap()
                .get_item(0)
                .unwrap()
                .getattr(intern!(img.py(), "duration"));
            next_dt = match _next_dt {
                Ok(v) => v.extract().unwrap(),
                Err(_) => 0.0,
            }
        // 372
        } else {
            texture = img.call_method0(intern!(img.py(), "get_texture")).unwrap();
        }
        // 375
        if !program.is_true().unwrap() {
            let texture_array_region_class =
                PyModule::import(py_, "pyglet.image.TextureArrayRegion")
                    .unwrap()
                    .getattr("TextureArrayRegion")
                    .unwrap();
            if img.is_instance(texture_array_region_class).unwrap() {
                // self._program = get_default_array_shader()
                let get_default_array_shader = PyModule::import(py_, "pyglet.sprite")
                    .unwrap()
                    .getattr("get_default_array_shader")
                    .unwrap();
                program = get_default_array_shader.call0().unwrap();
            } else {
                // self._program = get_default_shader()
                let get_default_shader = PyModule::import(py_, "pyglet.sprite")
                    .unwrap()
                    .getattr("get_default_shader")
                    .unwrap();
                program = get_default_shader.call0().unwrap();
            }
        }
        // 383
        if !batch_.is_none() {
            batch = PyModule::import(py_, "pyglet.graphics")
                .unwrap()
                .getattr("get_default_batch")
                .unwrap()
                .call0()
                .unwrap();
        } else {
            batch = batch_;
        }
        // 385
        let group = sprite_group_class.call1((texture, blend_src, blend_dest, program, group));

        Sprite {
            subpixel,
            batch: batch.into(),
            group: Some(group.into()),
            user_group: Some(group.into()),
            group_class: group.into(),
            x,
            y,
            z,
            scale: 1.0,
            scale_x: 1.0,
            scale_y: 1.0,
            visible: true,
            vertex_list: None,
            frame_index: 0,
            next_dt,
            program: Some(program.into()),
            animation: animation,
            texture: Some(texture.into()),
            paused: false,
            rgba: (255, 255, 255, 255),
        }
    }
}
