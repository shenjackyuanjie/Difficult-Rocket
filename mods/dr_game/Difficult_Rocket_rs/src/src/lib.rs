/*
 * -------------------------------
 * Difficult Rocket
 * Copyright © 2020-2023 by shenjackyuanjie 3695888@qq.com
 * All rights reserved
 * -------------------------------
 */

mod logger;
mod plugin;
mod python;
mod simulator;
mod sr1_data;
mod types;

use pyo3::prelude::*;

#[allow(unused)]
enum LoadState {
    Init,
    WaitStart,
    PreStart,
    Running,
    Clean,
}

#[pyfunction]
fn get_version_str() -> String { "0.2.14.0".to_string() }

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
    m.add_function(wrap_pyfunction!(sr1_data::part_list::read_part_list_py, m)?)?;
    m.add_function(wrap_pyfunction!(sr1_data::ship::py_raw_ship_from_file, m)?)?;
    m.add_function(wrap_pyfunction!(python::data::load_and_save_test, m)?)?;
    m.add_class::<python::data::PySR1Ship>()?;
    m.add_class::<python::data::PySR1PartList>()?;
    m.add_class::<python::data::PySR1PartType>()?;
    m.add_class::<python::console::PyConsole>()?;
    Ok(())
}

// pub fn run() {}

// fn init() {}
