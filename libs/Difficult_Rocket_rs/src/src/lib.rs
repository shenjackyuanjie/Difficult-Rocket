use pyo3::intern;
use pyo3::prelude::*;

/// Formats the sum of two numbers as string.
#[pyfunction]
fn sum_as_string(a: usize, b: usize) -> PyResult<String> {
    Ok((a + b).to_string())
}

#[pyfunction]
fn test_call(py_obj: &PyAny) -> PyResult<bool> {
    py_obj.call_method0("draw")?;
    Ok(true)
}

#[pyfunction]
#[allow(non_snake_case)]
fn better_update_parts(render: &PyAny, option: &PyAny) -> PyResult<bool> {
    if !render.getattr(intern!(render.py(), "rendered")).unwrap().is_true().unwrap() {
        // Ok(false);
        return Ok(false);
        // println!("aaaaa");
    }
    if option.getattr("debug_d_pos").unwrap().is_true().unwrap() {
        let line = render.getattr("debug_line").unwrap();
        // line.
    }
    Ok(true)
}

#[pyfunction]
fn for_x_in_range(a: usize, b: usize) -> PyResult<()> {
    assert!(a <= b);
    for x in a..b {
        println!("{}", x);
    }
    Ok(())
}

/// A Python module implemented in Rust. The name of this function must match
/// the `lib.name` setting in the `Cargo.toml`, else Python will not be able to
/// import the module.
#[pymodule]
#[pyo3(name = "Difficult_Rocket_rs")]
fn module_init(_py: Python<'_>, m: &PyModule) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(sum_as_string, m)?)?;
    m.add_function(wrap_pyfunction!(for_x_in_range, m)?)?;
    m.add_function(wrap_pyfunction!(test_call, m)?)?;
    m.add_function(wrap_pyfunction!(better_update_parts, m)?)?;
    Ok(())
}