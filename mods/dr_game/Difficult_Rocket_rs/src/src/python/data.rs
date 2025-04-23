use std::collections::HashMap;

use pyo3::exceptions::PyValueError;
use pyo3::prelude::*;

use crate::dr_physics::math::{Point2D, Rotate};
use crate::sr1_parse::IdType;
use crate::sr1_parse::SaveStatus;
use crate::sr1_parse::part_list::RawPartList;
use crate::sr1_parse::ship::{Connection, RawConnectionData, RawShip};
use crate::sr1_parse::{SR1PartData, SR1PartListTrait, get_max_box};
use crate::sr1_parse::{SR1PartList, SR1PartType, SR1Ship};

use quick_xml::se::to_string;

#[pyclass]
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

#[pyclass]
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

#[pyclass]
#[derive(Clone, Debug)]
#[pyo3(name = "SR1PartList_rs")]
pub struct PySR1PartList {
    pub data: SR1PartList,
}

#[pymethods]
impl PySR1PartList {
    #[new]
    #[pyo3(text_signature = "(file_path = './assets/builtin/PartList.xml', list_name = 'NewPartList')")]
    fn new(file_path: String, list_name: String) -> Self {
        let raw_part_list: RawPartList = match RawPartList::from_file(file_path.clone()) {
            Ok(raw_part_list) => raw_part_list,
            Err(e) => {
                println!("ERROR!\n{}\n----------", e);
                panic!("Parse part list failed! {}\n{e}", file_path);
            }
        };
        let data = raw_part_list.to_sr_part_list(Some(list_name));
        Self { data }
    }

    fn as_dict(&self) -> HashMap<String, PySR1PartType> {
        let mut map = HashMap::new();
        for part_type in self.data.types.iter() {
            map.insert(part_type.name.clone(), PySR1PartType::ref_new(part_type));
        }
        map
    }

    fn get_part_type(&self, name: String) -> Option<PySR1PartType> {
        let part_type = self.data.get_part_type(&name);
        part_type.map(PySR1PartType::ref_new)
    }
}

#[pyclass]
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

#[pyclass]
#[derive(Debug, Clone)]
#[pyo3(name = "SR1Connection_rs")]
pub struct PySR1Connections {
    pub datas: Vec<Connection>,
}

#[pymethods]
impl PySR1Connections {
    /// 通过父节点获取连接
    fn search_connection_by_parent(&self, parent_id: IdType) -> Vec<RawConnectionData> {
        self.datas
            .iter()
            .filter(|x| x.get_parent() == parent_id && x.is_normal())
            .map(|x| x.as_normal_raw().unwrap())
            .collect()
    }
    /// 通过子节点获取连接
    fn search_by_child(&self, child_id: IdType) -> Vec<RawConnectionData> {
        self.datas
            .iter()
            .filter(|x| x.get_child() == child_id && x.is_normal())
            .map(|x| x.as_normal_raw().unwrap())
            .collect()
    }
    /// 通过父子中任意一个 id 搜索连接
    fn search_by_id(&self, any_id: IdType) -> Vec<RawConnectionData> {
        self.datas
            .iter()
            .filter(|x| (x.get_parent() == any_id || x.get_child() == any_id) && x.is_normal())
            .map(|x| x.as_normal_raw().unwrap())
            .collect()
    }
    /// 通过父子双方 id 获取连接
    ///
    /// 保险起见, 我还是返回一个 Vec
    ///
    /// 万一真有 双/多 连接呢
    fn search_by_both_id(&self, parent_id: IdType, child_id: IdType) -> Vec<RawConnectionData> {
        self.datas
            .iter()
            .filter(|x| x.get_parent() == parent_id && x.get_child() == child_id && x.is_normal())
            .map(|x| x.as_normal_raw().unwrap())
            .collect()
    }
    /// 获取所有连接的原始数据
    ///
    /// 万一你确实需要吭哧吭哧去处理原始数据呢
    fn get_raw_data(&self) -> Vec<RawConnectionData> {
        self.datas.iter().filter(|x| x.is_normal()).map(|x| x.as_normal_raw().unwrap()).collect()
    }
}

#[pyclass]
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
        // -x, -y, +x, +y
        // 左下角，右上角
        let mut max_box = get_max_box(&self.ship.parts, &self.part_list);
        // 每个坐标 * 60
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

    /// 待会直接加一个在 SR1 PartData上获取的API得了，现在这样太费劲了
    ///
    /// 加好了
    fn get_part_box(&self, part_id: IdType) -> Option<((f64, f64), (f64, f64))> {
        let part_data = self.ship.parts.iter().find(|&x| x.id == part_id);
        if let Some(part_data) = part_data {
            if let Some(part_type) = self.part_list.get_part_type(&part_data.part_type_id) {
                // rotate
                let radius = part_data.angle;
                let ((x1, y1), (x2, y2)) = part_type.get_box();
                let mut p1 = Point2D::new(x1, y1);
                let mut p2 = Point2D::new(x2, y2);
                p1.rotate_radius_mut(radius);
                p2.rotate_radius_mut(radius);
                // transform
                p1.add_mut(part_data.x * 2.0, part_data.y * 2.0);
                p2.add_mut(part_data.x * 2.0, part_data.y * 2.0);
                return Some(((p1.x, p1.y), (p2.x, p2.y)));
            }
        }
        None
    }

    /// 通过 part_id 获取 part_data
    ///
    /// 当然, 支持重叠 ID
    fn find_part_by_id(&self, part_id: IdType) -> Vec<PySR1PartData> {
        // 先搜链接到的部件
        // 这里的代码是 GitHub Copilot 帮我优化的
        // 赞美 GitHub Copilot !()
        let unconnected =
            self.ship.disconnected.iter().flat_map(|(group, _)| group.iter()).filter(|part| part.id == part_id);
        // 然后通过一个 chain 直接把他链接到这边
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

#[pyfunction]
pub fn load_and_save_test(file_name: String) -> PyResult<()> {
    let ship = RawShip::from_file(file_name).unwrap();
    match to_string(&ship) {
        Ok(s) => println!("{}", s),
        Err(e) => println!("{}", e),
    }
    Ok(())
}
