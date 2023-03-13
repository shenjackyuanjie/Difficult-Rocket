/*
 * -------------------------------
 * Difficult Rocket
 * Copyright © 2020-2023 by shenjackyuanjie 3695888@qq.com
 * All rights reserved
 * -------------------------------
 */

use crate::types::sr1::SR1PartData;
use pyo3::intern;
use pyo3::prelude::*;
use std::collections::HashMap;
use std::time;

#[allow(dead_code)]
pub mod types {
    use pyo3::intern;
    use pyo3::prelude::*;
    use pyo3::types::PyDict;
    use std::collections::HashMap;

    use crate::types::sr1::SR1PartData;

    pub struct Point {
        pub x: f64,
        pub y: f64,
        pub id: usize,
        pub type_: String,
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
            return Ok(PartDatas {
                part_structs: datas,
            });
        }
    }

    #[allow(non_snake_case)]
    pub fn part_data_to_SR1PartData(input: &PyAny) -> PyResult<SR1PartData> {
        let connections = match input.getattr(intern!(input.py(), "connections")) {
            Ok(ok) => ok.extract()?,
            _ => None,
        };

        return Ok(SR1PartData {
            x: input.getattr(intern!(input.py(), "x"))?.extract()?,
            y: input.getattr(intern!(input.py(), "y"))?.extract()?,
            id: input.getattr(intern!(input.py(), "id"))?.extract()?,
            p_type: input.getattr(intern!(input.py(), "p_type"))?.extract()?,
            active: input.getattr(intern!(input.py(), "active"))?.extract()?,
            angle: input.getattr(intern!(input.py(), "angle"))?.extract()?,
            angle_v: input.getattr(intern!(input.py(), "angle_v"))?.extract()?,
            editor_angle: input
                .getattr(intern!(input.py(), "editor_angle"))?
                .extract()?,
            flip_x: input.getattr(intern!(input.py(), "flip_x"))?.extract()?,
            flip_y: input.getattr(intern!(input.py(), "flip_y"))?.extract()?,
            explode: input.getattr(intern!(input.py(), "explode"))?.extract()?,
            textures: input.getattr(intern!(input.py(), "textures"))?.extract()?,
            connections, // connections: input.getattr(intern!(input.py(), "connections"))?.extract()?,
        });
    }

    #[allow(non_snake_case)]
    pub fn part_data_tp_SR1PartDatas(input: &PyDict) -> PyResult<HashMap<i64, SR1PartData>> {
        let mut result: HashMap<i64, SR1PartData> = HashMap::with_capacity(input.len());
        for key in input.iter() {
            result.insert(key.0.extract()?, part_data_to_SR1PartData(key.1)?);
        }
        return Ok(result);
    }
}

#[pyfunction]
#[allow(unused_variables)]
pub fn better_update_parts(
    render: &PyAny,
    option: &PyAny,
    window: &PyAny,
    parts: &types::PartDatas,
    sr1_xml_scale: i32,
) -> PyResult<bool> {
    if !render
        .getattr(intern!(render.py(), "rendered"))?
        .is_true()?
    {
        return Ok(false);
    }
    let start_time = time::Instant::now();
    let x_center: f32 = window.getattr(intern!(window.py(), "width"))?.extract()?;
    let y_center: f32 = window.getattr(intern!(window.py(), "height"))?.extract()?;
    let x_center: f32 = x_center / 2.0;
    let y_center: f32 = y_center / 2.0;
    let datas: &HashMap<i64, SR1PartData> = &parts.part_structs;
    let part_sprites = render.getattr(intern!(render.py(), "parts_sprite"))?;
    let get_stuf_time = start_time.elapsed();

    for keys in datas {
        let sprite = part_sprites.get_item(keys.0)?;
        let new_x: f64 = keys.1.x * sr1_xml_scale as f64 + x_center as f64;
        let new_y: f64 = keys.1.y * sr1_xml_scale as f64 + y_center as f64;
        sprite.setattr(intern!(sprite.py(), "x"), new_x)?;
        sprite.setattr(intern!(sprite.py(), "y"), new_y)?;
    }
    let run_time = start_time.elapsed();
    Ok(true)
}
