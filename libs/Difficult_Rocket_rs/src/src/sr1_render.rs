/*
 * -------------------------------
 * Difficult Rocket
 * Copyright © 2020-2023 by shenjackyuanjie 3695888@qq.com
 * All rights reserved
 * -------------------------------
 */

use std::collections::HashMap;
use std::time;
use pyo3::intern;
use pyo3::prelude::*;
// use pyo3::types::PyDict;
use crate::sr1_render::types::SR1PartData;

#[allow(dead_code)]
pub mod types {
    use std::collections::HashMap;
    use pyo3::intern;
    use pyo3::prelude::*;
    use pyo3::types::{PyDict};

    pub struct SR1PartData {
        pub x: f64,
        pub y: f64,
        pub id: i64,
        pub type_: String,
        pub active: bool,
        pub angle: f64,
        pub angle_v: f64,
        pub editor_angle: usize,
        pub flip_x: bool,
        pub flip_y: bool,
        pub explode: bool,
        pub textures: String,
        // pub connections: Vec<usize>
    }

    pub struct Point {
        pub x: f64,
        pub y: f64,
        pub id: usize,
        pub type_: String
    }

    #[pyclass(name = "PartDatas")]
    pub struct PartDatas {
        pub part_structs: HashMap<i64, SR1PartData>,
    }

    impl PartDatas {
        fn get_rust_data(&self) -> &HashMap<i64, SR1PartData> {
            return &self.part_structs;
        }
    }

    #[pymethods]
    impl PartDatas {
        #[new]
        fn py_new(py_part_data: &PyDict) -> PyResult<Self> {
            let datas: HashMap<i64, SR1PartData> = part_data_tp_SR1PartDatas(py_part_data)?;
            return Ok(PartDatas { part_structs: datas })
        }
    }


    #[allow(non_snake_case)]
    pub fn part_data_to_SR1PartData(input: &PyAny) -> Result<SR1PartData, PyErr> {
        return Ok(SR1PartData{
            x: input.getattr(intern!(input.py(), "x"))?.extract()?,
            y: input.getattr(intern!(input.py(), "y"))?.extract()?,
            id: input.getattr(intern!(input.py(), "id"))?.extract()?,
            type_: input.getattr(intern!(input.py(), "type_"))?.extract()?,
            active: input.getattr(intern!(input.py(), "active"))?.extract()?,
            angle: input.getattr(intern!(input.py(), "angle"))?.extract()?,
            angle_v: input.getattr(intern!(input.py(), "angle_v"))?.extract()?,
            editor_angle: input.getattr(intern!(input.py(), "editor_angle"))?.extract()?,
            flip_x: input.getattr(intern!(input.py(), "flip_x"))?.extract()?,
            flip_y: input.getattr(intern!(input.py(), "flip_y"))?.extract()?,
            explode: input.getattr(intern!(input.py(), "explode"))?.extract()?,
            textures: input.getattr(intern!(input.py(), "textures"))?.extract()?,
            // connections: input.getattr(intern!(input.py(), "connections"))?.extract()?,
        })
    }

    #[allow(non_snake_case)]
    pub fn part_data_tp_SR1PartDatas(input: &PyDict) -> Result<HashMap<i64, SR1PartData>, PyErr> {
        let mut result: HashMap<i64, SR1PartData> = HashMap::with_capacity(input.len());
        for key in input.iter() {
            result.insert(key.0.extract()?, part_data_to_SR1PartData(key.1)?);
        }
        return Ok(result)
    }

    pub fn part_data_to_point(input: &PyAny) -> Result<Point, PyErr> {
        return Ok(Point{
            x: input.getattr(intern!(input.py(), "x"))?.extract()?,
            y: input.getattr(intern!(input.py(), "y"))?.extract()?,
            id: input.getattr(intern!(input.py(), "id"))?.extract()?,
            type_: input.getattr(intern!(input.py(), "type_"))?.extract()?
        })
    }

    pub fn part_datas_to_points(input: &PyDict) -> Result<HashMap<i64, Point>, PyErr> {
        let mut result: HashMap<i64, Point> = HashMap::with_capacity(input.len());
        for key in input.iter() {
            result.insert(key.0.extract()?, part_data_to_point(key.1)?);
        }
        return Ok(result);
    }

}



#[pyfunction]
#[allow(unused_variables)]
pub fn better_update_parts(render: &PyAny, option: &PyAny, window: &PyAny,
                           parts: &types::PartDatas, sr1_xml_scale: i32) -> PyResult<bool> {
    if !render.getattr(intern!(render.py(), "rendered"))?.is_true()? {
        return Ok(false);
    }
    let start_time = time::Instant::now();
    let x_center: f32 = window.getattr(intern!(window.py(), "width"))?.extract()?;
    let y_center: f32 = window.getattr(intern!(window.py(), "height"))?.extract()?;
    let x_center: f32 = x_center / 2.0;
    let y_center: f32 = y_center / 2.0;
    let datas: &HashMap<i64, SR1PartData> = &parts.part_structs;
    let part_sprites = render.getattr(intern!(render.py(), "parts_sprite"))?;
    // let part_sprites: &PyDict = part_sprites.downcast::<PyDict>()?;
    let get_stuf_time = start_time.elapsed();
    // println!("get stuf took {} second", get_stuf_time.as_secs_f64());

    for keys in datas {
        // let index = keys.0.to_string();
        let sprite = part_sprites.get_item(keys.0)?;
        let new_x: f64 = keys.1.x * sr1_xml_scale as f64 + x_center as f64;
        let new_y: f64 = keys.1.y * sr1_xml_scale as f64 + y_center as f64;
        sprite.setattr(intern!(sprite.py(), "x"), new_x)?;
        sprite.setattr(intern!(sprite.py(), "y"), new_y)?;
        // part_sprites.set_item(keys.0, sprite)?;
        // println!("{}", keys.0);
    }
    let run_time = start_time.elapsed();
    // println!("run took {} second or {} fps", run_time.as_secs_f64(), 1 as f64 / run_time.as_secs_f64());
    // render.setattr(intern!(render.py(), "parts_sprite"), part_sprites)?;
    // println!("dx: {} dy: {} scale: {}", dx, dy, render_scale);
    Ok(true)
}