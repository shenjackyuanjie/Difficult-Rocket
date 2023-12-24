/*
 * -------------------------------
 * Difficult Rocket
 * Copyright © 2020-2023 by shenjackyuanjie 3695888@qq.com
 * All rights reserved
 * -------------------------------
 */

mod dr_physics;
mod python;
mod sr1_parse;

use pyo3::prelude::*;

pub type IdType = i64;

#[pyfunction]
fn get_version_str() -> String {
    "0.3.1".to_string()
}

#[pyfunction]
fn test_call(py_obj: &PyAny) -> PyResult<bool> {
    py_obj.call_method0("draw")?;
    Ok(true)
}

#[pymodule]
#[pyo3(name = "Difficult_Rocket_rs")]
fn module_init(_py: Python<'_>, m: &PyModule) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(get_version_str, m)?)?;
    m.add_function(wrap_pyfunction!(test_call, m)?)?;
    m.add_function(wrap_pyfunction!(sr1_parse::part_list::read_part_list_py, m)?)?;
    m.add_function(wrap_pyfunction!(sr1_parse::ship::py_raw_ship_from_file, m)?)?;
    m.add_function(wrap_pyfunction!(python::data::load_and_save_test, m)?)?;
    m.add_class::<python::data::PySR1Ship>()?;
    m.add_class::<python::data::PySR1PartList>()?;
    m.add_class::<python::data::PySR1PartType>()?;
    m.add_class::<python::data::PySR1PartData>()?;
    m.add_class::<python::data::PySaveStatus>()?;
    m.add_class::<python::console::PyConsole>()?;
    // m.add_class::<python::editor::EditorArea>()?;
    Ok(())
}
