/*
 * -------------------------------
 * Difficult Rocket
 * Copyright © 2020-2023 by shenjackyuanjie 3695888@qq.com
 * All rights reserved
 * -------------------------------
 */

mod dr_physics;
/// Python 交互
mod python;
/// 也许是一些渲染的东西
mod renders;
/// sr1 的逆天数据结构解析
mod sr1_parse;

use pyo3::{
    pyfunction, pymodule,
    types::{PyModule, PyModuleMethods},
    wrap_pyfunction, Bound, PyResult,
};

#[pyfunction]
fn get_version_str() -> String { env!("CARGO_PKG_VERSION").to_string() }

#[pymodule]
#[pyo3(name = "Difficult_Rocket_rs")]
fn module_init(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(get_version_str, m)?)?;
    m.add_function(wrap_pyfunction!(sr1_parse::py::read_part_list_py, m)?)?;
    m.add_function(wrap_pyfunction!(sr1_parse::py::py_raw_ship_from_file, m)?)?;
    m.add_function(wrap_pyfunction!(sr1_parse::py::py_assert_ship, m)?)?;
    m.add_function(wrap_pyfunction!(python::data::load_and_save_test, m)?)?;
    m.add_function(wrap_pyfunction!(renders::render_hack, m)?)?;
    m.add_class::<python::data::PySR1Ship>()?;
    m.add_class::<python::data::PySR1PartList>()?;
    m.add_class::<python::data::PySR1PartType>()?;
    m.add_class::<python::data::PySR1PartData>()?;
    m.add_class::<python::data::PySaveStatus>()?;
    m.add_class::<python::data::PySR1Connections>()?;
    m.add_class::<python::console::PyConsole>()?;
    // m.add_class::<python::editor::EditorArea>()?;
    Ok(())
}
