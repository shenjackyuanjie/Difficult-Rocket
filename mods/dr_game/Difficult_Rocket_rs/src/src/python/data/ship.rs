use std::collections::HashMap;

use pyo3::exceptions::PyValueError;
use pyo3::prelude::*;

use crate::python::data::connections::PySR1Connections;
use crate::python::data::part_data::PySR1PartData;
use crate::python::data::part_list::PySR1PartList;
use crate::python::data::part_type::PySR1PartType;
use crate::python::data::save_status::PySaveStatus;
use crate::sr1_parse::model::{IdType, SR1PartList, SR1Ship};
use crate::sr1_parse::ship_io::{load_part_list_from_file, load_ship_from_file, save_ship_to_file};

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
        let ship = load_ship_from_file(file_path.clone(), Some(ship_name.unwrap_or("new ship".to_string()))).ok();
        match ship {
            Some(mut ship) => {
                let part_list = match part_list {
                    Some(part_list) => part_list.data,
                    None => load_part_list_from_file("./assets/builtin/PartList.xml".to_string()).unwrap(),
                };
                ship.parse_part_list_to_part(&part_list);
                Ok(Self { ship, part_list })
            }
            None => Err(PyValueError::new_err(format!("Parse ship failed! {}", file_path))),
        }
    }

    fn disconnected_parts(&self) -> Vec<(Vec<(PySR1PartType, PySR1PartData)>, PySR1Connections)> {
        self.ship
            .resolved_disconnected_parts(&self.part_list)
            .into_iter()
            .map(|(group_parts, connections)| {
                (
                    group_parts
                        .into_iter()
                        .map(|(part_type, part_data)| (PySR1PartType::new(part_type), PySR1PartData::new(part_data)))
                        .collect(),
                    PySR1Connections { datas: connections },
                )
            })
            .collect()
    }

    #[getter]
    fn get_img_pos(&self) -> (i64, i64, i64, i64) { self.ship.img_bounds(&self.part_list) }

    #[getter]
    fn get_name(&self) -> String { self.ship.name.clone() }

    #[getter]
    fn get_description(&self) -> String { self.ship.description.clone() }

    #[getter]
    fn get_lift_off(&self) -> bool { self.ship.lift_off }

    #[getter]
    fn get_touch_ground(&self) -> bool { self.ship.touch_ground }

    #[getter]
    fn get_mass(&self) -> f64 { self.ship.total_mass(&self.part_list) }

    fn connections(&self) -> PySR1Connections {
        PySR1Connections {
            datas: self.ship.connections.clone(),
        }
    }

    fn as_list(&self) -> Vec<(PySR1PartType, PySR1PartData)> {
        self.ship
            .resolved_parts(&self.part_list)
            .into_iter()
            .map(|(part_type, part_data)| (PySR1PartType::new(part_type), PySR1PartData::new(part_data)))
            .collect()
    }

    fn as_dict(&self) -> HashMap<IdType, Vec<(PySR1PartType, PySR1PartData)>> {
        self.ship
            .resolved_parts_by_id(&self.part_list)
            .into_iter()
            .map(|(id, parts)| {
                (
                    id,
                    parts
                        .into_iter()
                        .map(|(part_type, part_data)| (PySR1PartType::new(part_type), PySR1PartData::new(part_data)))
                        .collect(),
                )
            })
            .collect()
    }

    fn get_part_box(&self, part_id: IdType) -> Option<((f64, f64), (f64, f64))> {
        self.ship.part_box(&self.part_list, part_id)
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
        save_ship_to_file(&self.ship, file_path, &save_status.unwrap_or_default().status).unwrap();
        Ok(())
    }
}
