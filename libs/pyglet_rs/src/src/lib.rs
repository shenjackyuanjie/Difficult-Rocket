/*
 * -------------------------------
 * Difficult Rocket
 * Copyright © 2020-2023 by shenjackyuanjie 3695888@qq.com
 * All rights reserved
 * -------------------------------
 */

mod math;
mod pymath;
mod sprite;

use pyo3::prelude::*;

#[pyfunction]
fn get_version_str() -> String {
    return "0.1.0".to_string();
}

#[pymodule]
#[pyo3(name = "pyglet_rs")]
fn module_init(_py: Python<'_>, m: &PyModule) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(get_version_str, m)?)?;
    m.add_class::<sprite::Sprite>()?;
    // vector
    m.add_class::<pymath::python_class::PyVector2>()?;
    Ok(())
}
