use std::collections::HashMap;

use pyo3::exceptions::PyValueError;
use pyo3::prelude::*;

use crate::dr_physics::math::{Point2D, Rotate};
use crate::python::data::connections::PySR1Connections;
use crate::python::data::part_data::PySR1PartData;
use crate::python::data::part_list::PySR1PartList;
use crate::python::data::part_type::PySR1PartType;
use crate::python::data::save_status::PySaveStatus;
use crate::sr1_parse::types::{IdType, SR1PartList, SR1Ship};
use crate::sr1_parse::util::get_max_box;

#[pyclass(skip_from_py_object)]
#[derive(Clone, Debug)]
#[pyo3(name = "SR1Ship_rs")]
pub struct PySR1Ship {
    pub ship: SR1Ship,
    pub part_list: SR1PartList,
}

#[pymethods]
impl PySR1Ship {
    #[new]
    #[pyo3(text_signature = "(file_path = './assets/builtin/dock1.xml', part_list = None, ship_name = 'NewShip')")]
    #[pyo3(signature = (file_path, part_list=None, ship_name=None))]
    fn new(file_path: String, part_list: Option<PySR1PartList>, ship_name: Option<String>) -> PyResult<Self> {
        let ship = SR1Ship::from_file(file_path.clone(), Some(ship_name.unwrap_or("new ship".to_string())));
        match ship {
            Some(mut ship) => {
                let part_list = match part_list {
                    Some(part_list) => part_list.data,
                    None => SR1PartList::from_file("./assets/builtin/PartList.xml".to_string()).unwrap(),
                };
                ship.parse_part_list_to_part(&part_list);
                Ok(Self { ship, part_list })
            }
            None => Err(PyValueError::new_err(format!("Parse ship failed! {}", file_path))),
        }
    }

    fn disconnected_parts(&self) -> Vec<(Vec<(PySR1PartType, PySR1PartData)>, PySR1Connections)> {
        if self.ship.disconnected.is_empty() {
            return Vec::new();
        }
        let mut result = Vec::with_capacity(self.ship.disconnected.len());
        for (part_group, connections) in self.ship.disconnected.iter() {
            let mut group_parts = Vec::with_capacity(part_group.len());
            for part_data in part_group.iter() {
                if let Some(part_type) = self.part_list.get_part_type(&part_data.part_type_id) {
                    let part_type = PySR1PartType::new(part_type.clone());
                    let py_part_data = PySR1PartData::new(part_data.clone());
                    group_parts.push((part_type, py_part_data));
                }
            }
            result.push((
                group_parts,
                PySR1Connections {
                    datas: connections.clone(),
                },
            ));
        }
        result
    }

    #[getter]
    fn get_img_pos(&self) -> (i64, i64, i64, i64) {
        let mut max_box = get_max_box(&self.ship.parts, &self.part_list);
        max_box.0 *= 60.0;
        max_box.1 *= 60.0;
        max_box.2 *= 60.0;
        max_box.3 *= 60.0;
        (max_box.0 as i64, max_box.1 as i64, max_box.2 as i64, max_box.3 as i64)
    }

    #[getter]
    fn get_name(&self) -> String { self.ship.name.clone() }

    #[getter]
    fn get_description(&self) -> String { self.ship.description.clone() }

    #[getter]
    fn get_lift_off(&self) -> bool { self.ship.lift_off }

    #[getter]
    fn get_touch_ground(&self) -> bool { self.ship.touch_ground }

    #[getter]
    fn get_mass(&self) -> f64 {
        let mut mass = 0_f64;
        for part_data in self.ship.parts.iter() {
            if let Some(part_type) = self.part_list.get_part_type(&part_data.part_type_id) {
                mass += part_type.mass;
            }
        }
        mass
    }

    fn connections(&self) -> PySR1Connections {
        PySR1Connections {
            datas: self.ship.connections.clone(),
        }
    }

    fn as_list(&self) -> Vec<(PySR1PartType, PySR1PartData)> {
        let mut parts: Vec<(PySR1PartType, PySR1PartData)> = Vec::new();
        for part_data in self.ship.parts.iter() {
            if let Some(part_type) = self.part_list.get_part_type(&part_data.part_type_id) {
                let part_type = PySR1PartType::new(part_type.clone());
                let py_part_data = PySR1PartData::new(part_data.clone());
                parts.push((part_type, py_part_data));
            }
        }
        parts
    }

    fn as_dict(&self) -> HashMap<IdType, Vec<(PySR1PartType, PySR1PartData)>> {
        let mut parts: HashMap<IdType, Vec<(PySR1PartType, PySR1PartData)>> = HashMap::new();
        for part_data in self.ship.parts.iter() {
            if let Some(part_type) = self.part_list.get_part_type(&part_data.part_type_id) {
                let part_type = PySR1PartType::new(part_type.clone());
                let py_part_data = PySR1PartData::new(part_data.clone());
                if let Some(part_list) = parts.get_mut(&part_data.id) {
                    part_list.push((part_type, py_part_data));
                } else {
                    parts.insert(part_data.id, vec![(part_type, py_part_data)]);
                }
            }
        }
        parts
    }

    fn get_part_box(&self, part_id: IdType) -> Option<((f64, f64), (f64, f64))> {
        let part_data = self.ship.parts.iter().find(|&x| x.id == part_id);
        if let Some(part_data) = part_data {
            if let Some(part_type) = self.part_list.get_part_type(&part_data.part_type_id) {
                let radius = part_data.angle;
                let ((x1, y1), (x2, y2)) = part_type.get_box();
                let mut p1 = Point2D::new(x1, y1);
                let mut p2 = Point2D::new(x2, y2);
                p1.rotate_radius_mut(radius);
                p2.rotate_radius_mut(radius);
                p1.add_mut(part_data.x * 2.0, part_data.y * 2.0);
                p2.add_mut(part_data.x * 2.0, part_data.y * 2.0);
                return Some(((p1.x, p1.y), (p2.x, p2.y)));
            }
        }
        None
    }

    fn find_part_by_id(&self, part_id: IdType) -> Vec<PySR1PartData> {
        let unconnected =
            self.ship.disconnected.iter().flat_map(|(group, _)| group.iter()).filter(|part| part.id == part_id);
        self.ship
            .parts
            .iter()
            .filter(|x| x.id == part_id)
            .chain(unconnected)
            .map(|raw_data| PySR1PartData { data: raw_data.clone() })
            .collect()
    }

    #[pyo3(signature = (file_path, save_status=None))]
    fn save(&self, file_path: String, save_status: Option<PySaveStatus>) -> PyResult<()> {
        println!("{:?}", save_status);
        self.ship.save(file_path, &save_status.unwrap_or_default().status).unwrap();
        Ok(())
    }
}
