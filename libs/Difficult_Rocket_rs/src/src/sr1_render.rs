/*
 * -------------------------------
 * Difficult Rocket
 * Copyright © 2020-2023 by shenjackyuanjie 3695888@qq.com
 * All rights reserved
 * -------------------------------
 */

use std::collections::HashMap;
use pyo3::intern;
use pyo3::prelude::*;
use pyo3::types::PyDict;
use crate::sr1_render::types::Point;

#[allow(dead_code)]
pub mod types {
    use std::collections::HashMap;
    use pyo3::intern;
    use pyo3::prelude::*;
    use pyo3::types::PyDict;

    pub struct SR1PartData {
        pub x: f64,
        pub y: f64,
        pub id: usize,
        pub type_: String,
        pub active: bool,
        pub angle: f64,
        pub angle_v: f64,
        pub editor_angle: usize,
        pub flip_x: bool,
        pub flip_y: bool,
        pub explode: bool,
        pub textures: String,
        pub connections: Vec<usize>
    }

    pub struct Point {
        pub x: f64,
        pub y: f64,
        pub id: usize,
        pub type_: String
    }

    #[pyclass(name = "PartDatas")]
    pub struct PartDatas {
        pub part_structs: HashMap<usize, SR1PartData>
    }

    #[pymethods]
    impl PartDatas {
        #[new]
        pub fn py_new(py_part_data: &PyDict) -> PyResult<Self> {
            let datas: HashMap<usize, SR1PartData> = part_data_tp_SR1PartDatas(py_part_data)?;
            return Ok(PartDatas { part_structs: datas })
        }
    }

    impl PartDatas{
        pub fn get_rust_data(&self) -> &HashMap<usize, SR1PartData> {
            return &self.part_structs;
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
            connections: input.getattr(intern!(input.py(), "connections"))?.extract()?,
        })
    }

    #[allow(non_snake_case)]
    pub fn part_data_tp_SR1PartDatas(input: &PyDict) -> Result<HashMap<usize, SR1PartData>, PyErr> {
        let mut result: HashMap<usize, SR1PartData> = HashMap::with_capacity(input.len());
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

    pub fn part_datas_to_points(input: &PyDict) -> Result<HashMap<usize, Point>, PyErr> {
        let mut result: HashMap<usize, Point> = HashMap::with_capacity(input.len());
        for key in input.iter() {
            result.insert(key.0.extract()?, part_data_to_point(key.1)?);
        }
        return Ok(result);
    }

}




#[pyfunction]
#[allow(unused_variables)]
pub fn better_update_parts(render: &PyAny, option: &PyAny, window: &PyAny) -> PyResult<bool> {
    if !render.getattr(intern!(render.py(), "rendered"))?.is_true()? {
        return Ok(false);
    }
    let dx: usize = render.getattr(intern!(render.py(), "dx"))?.extract()?;
    let dy: usize = render.getattr(intern!(render.py(), "dy"))?.extract()?;
    let x_center: usize = window.getattr(intern!(window.py(), "width"))?.extract()?;
    let y_center: usize = window.getattr(intern!(window.py(), "height"))?.extract()?;
    let x_center: usize = x_center / 2;
    let y_center: usize = y_center / 2;
    let part_datas: &PyDict = render.getattr(intern!(render.py(), "part_data"))?.extract()?;
    let parts: HashMap<usize, Point> = types::part_datas_to_points(part_datas)?;
    if option.getattr("debug_d_pos")?.is_true()? {
        let line = render.getattr(intern!(render.py(), "debug_line"))?;
    }
    Ok(true)
}