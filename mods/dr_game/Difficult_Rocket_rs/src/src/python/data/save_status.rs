use pyo3::prelude::*;

use crate::sr1_parse::model::SaveStatus;

#[pyclass(from_py_object)]
#[pyo3(name = "SaveStatus_rs")]
#[derive(Clone, Debug)]
pub struct PySaveStatus {
    pub status: SaveStatus,
}

#[pymethods]
impl PySaveStatus {
    #[new]
    fn new(save_default: bool) -> Self {
        Self {
            status: SaveStatus::new(save_default),
        }
    }
}

impl Default for PySaveStatus {
    fn default() -> Self { Self::new(false) }
}
