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

pub mod types {
    use std::collections::HashMap;
    use pyo3::intern;
    use pyo3::prelude::*;
    use pyo3::types::iter::PyDictIterator;
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

    #[pyclass]
    pub struct PartDatas {
        pub part_structs: HashMap<usize, SR1PartData>
    }

    #[pymethods]
    impl PartDatas {
        #[new]
        pub fn py_new(py_part_data: &PyDict) -> PyResult<Self>{
            let mut
        }
    }

    #[allow(dead_code)]
    pub fn convert_py_any_sr1_part_data(input: &PyAny) -> Result<SR1PartData, PyErr> {
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

    pub fn get_point_from_sr1_part_data(input: &PyAny) -> Result<Point, PyErr> {
        return Ok(Point{
            x: input.getattr(intern!(input.py(), "x"))?.extract()?,
            y: input.getattr(intern!(input.py(), "y"))?.extract()?,
            id: input.getattr(intern!(input.py(), "id"))?.extract()?,
            type_: input.getattr(intern!(input.py(), "type_"))?.extract()?
        })
    }

    pub fn point_dict_from_part_datas(input: &PyDict) -> Result<HashMap<usize, Point>, PyErr> {
        let mut result: HashMap<usize, Point> = HashMap::with_capacity(input.len());
        for key in &input.iter() {
            key[]
        }
        return Ok(result);
    }

}




#[pyfunction]
#[allow(non_snake_case)]
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
    let parts: HashMap<usize, Point> = types::point_dict_from_part_datas(part_datas)?;
    if option.getattr("debug_d_pos")?.is_true()? {
        let line = render.getattr(intern!(render.py(), "debug_line"))?;
    }
    Ok(true)
}