/*
 * -------------------------------
 * Difficult Rocket
 * Copyright © 2020-2023 by shenjackyuanjie 3695888@qq.com
 * All rights reserved
 * -------------------------------
 */

mod sr1_render;

use pyo3::prelude::*;

#[pyfunction]
fn get_version_str() -> String {
    return String::from("0.0.5.0");
}

#[pyfunction]
fn test_call(py_obj: &PyAny) -> PyResult<bool> {
    py_obj.call_method0("draw")?;
    Ok(true)
}

/// A Python module implemented in Rust. The name of this function must match
/// the `lib.name` setting in the `Cargo.toml`, else Python will not be able to
/// import the module.
#[pymodule]
#[pyo3(name = "Difficult_Rocket_rs")]
fn module_init(_py: Python<'_>, m: &PyModule) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(get_version_str, m)?)?;
    m.add_function(wrap_pyfunction!(test_call, m)?)?;
    m.add_function(wrap_pyfunction!(sr1_render::better_update_parts, m)?)?;
    m.add_class::<sr1_render::types::PartDatas>()?;
    Ok(())
}