use pyo3::prelude::*;

use crate::dr_physics::math::{Point2D, Rotate};
use crate::python::data::part_type::PySR1PartType;
use crate::sr1_parse::types::{IdType, SR1PartData};

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
        let radius = self.data.angle;
        let ((x1, y1), (x2, y2)) = part_type.data.get_box();
        let mut p1 = Point2D::new(x1, y1);
        let mut p2 = Point2D::new(x2, y2);
        p1.rotate_radius_mut(radius);
        p2.rotate_radius_mut(radius);
        p1.add_mut(self.data.x * 2.0, self.data.y * 2.0);
        p2.add_mut(self.data.x * 2.0, self.data.y * 2.0);
        ((p1.x, p1.y), (p2.x, p2.y))
    }
}
