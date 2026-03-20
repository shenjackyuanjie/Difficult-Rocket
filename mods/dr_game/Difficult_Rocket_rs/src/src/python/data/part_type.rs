use pyo3::prelude::*;

use crate::sr1_parse::types::SR1PartType;

#[pyclass(from_py_object)]
#[derive(Clone, Debug)]
#[pyo3(name = "SR1PartType_rs")]
pub struct PySR1PartType {
    pub data: SR1PartType,
}

impl PySR1PartType {
    pub fn new(data: SR1PartType) -> Self { Self { data } }

    pub fn ref_new(data: &SR1PartType) -> Self { Self { data: data.clone() } }
}

#[pymethods]
impl PySR1PartType {
    #[getter]
    fn get_name(&self) -> String { self.data.name.clone() }

    #[getter]
    fn get_description(&self) -> String { self.data.description.clone() }

    #[getter]
    fn get_sprite(&self) -> String { self.data.sprite.clone() }

    #[getter]
    fn get_mass(&self) -> f64 { self.data.mass }

    #[getter]
    fn get_width(&self) -> u32 { self.data.width }

    #[getter]
    fn get_height(&self) -> u32 { self.data.height }

    #[getter]
    fn get_friction(&self) -> f64 { self.data.friction }

    #[getter]
    fn get_hidden(&self) -> bool { self.data.hidden }

    #[getter]
    fn get_type(&self) -> String { self.data.p_type.into() }
}
