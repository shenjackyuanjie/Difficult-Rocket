use pyo3::prelude::*;

use crate::python::data::part_type::PySR1PartType;
use crate::sr1_parse::model::{IdType, SR1PartData};

#[pyclass(skip_from_py_object)]
#[derive(Clone, Debug)]
#[pyo3(name = "SR1PartData_rs")]
pub struct PySR1PartData {
    pub data: SR1PartData,
}

impl PySR1PartData {
    pub fn new(data: SR1PartData) -> Self { Self { data } }
}

#[pymethods]
impl PySR1PartData {
    #[getter]
    fn get_id(&self) -> IdType { self.data.id }

    #[getter]
    fn get_part_type_id(&self) -> String { self.data.part_type_id.clone() }

    #[getter]
    fn get_pos(&self) -> (f64, f64) { (self.data.x, self.data.y) }

    #[getter]
    fn get_x(&self) -> f64 { self.data.x }

    #[getter]
    fn get_y(&self) -> f64 { self.data.y }

    #[getter]
    fn get_activate(&self) -> bool { self.data.active }

    #[getter]
    fn get_angle(&self) -> f64 { self.data.angle }

    #[getter]
    fn get_angle_r(&self) -> f64 { self.data.angle_degrees() }

    #[getter]
    fn get_angle_v(&self) -> f64 { self.data.angle_v }

    #[getter]
    fn get_explode(&self) -> bool { self.data.explode }

    #[getter]
    fn get_flip_x(&self) -> bool { self.data.flip_x }

    #[getter]
    fn get_flip_y(&self) -> bool { self.data.flip_y }

    fn get_part_box_by_type(&self, part_type: PySR1PartType) -> ((f64, f64), (f64, f64)) {
        self.data.get_corner_points(&part_type.data)
    }
}
