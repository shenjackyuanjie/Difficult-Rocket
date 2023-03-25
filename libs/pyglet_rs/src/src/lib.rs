/*
 * -------------------------------
 * Difficult Rocket
 * Copyright © 2020-2023 by shenjackyuanjie 3695888@qq.com
 * All rights reserved
 * -------------------------------
 */

mod sprite;

use pyo3::prelude::*;

#[pymodule]
#[pyo3(name = "pyglet_rs")]
fn module_init(_py: Python<'_>, m: &PyModule) -> PyResult<()> {
    m.add_class::<sprite::Sprite>()?;
    Ok(())
}
