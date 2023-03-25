/*
 * -------------------------------
 * Difficult Rocket
 * Copyright © 2020-2023 by shenjackyuanjie 3695888@qq.com
 * All rights reserved
 * -------------------------------
 */

use pyo3::prelude::*;

/// Instance of an on-screen image
/// See the module documentation for usage.
#[pyclass(name = "Sprite", subclass)]
#[pyo3(text_signature = "(img, x=0.0, y=0.0, z=0.0, \
                          batch=None, group=None, \
                          subpixel=False, program=None)")]
pub struct Sprite {
    // render
    pub batch: Py<PyAny>,
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
    pub animation: Option<Py<PyAny>>,
    pub texture: Option<Py<PyAny>>,
    pub paused: bool,
    // other
    pub rgba: (u8, u8, u8, u8),
}

#[pymethods]
impl Sprite {
    #[new]
    fn new(py_: Python, img: &PyAny, x: f64, y: f64, z: f64, batch: &PyAny, group: &PyAny) -> Self {
        // let img_class = PyModule::from_code(py_, "pyglet.image.Animation", "", "")?.getattr();
        let animation_class =
            PyModule::import(py_, "pyglet.image.Animation").unwrap().getattr("Animation").unwrap();
        let mut texture: Option<Py<PyAny>> = None;
        let mut animation: Option<Py<PyAny>> = None;
        if img.is_instance(animation_class).unwrap() {
            animation = Some(img.into());
        } else {
            texture = Some(img.into());
        }
        Sprite {
            batch: batch.into(),
            x,
            y,
            z,
            scale: 1.0,
            scale_x: 1.0,
            scale_y: 1.0,
            visible: true,
            vertex_list: None,
            frame_index: 0,
            animation,
            texture,
            paused: false,
            rgba: (255, 255, 255, 255),
            group_class: group.into(),
        }
    }
}
