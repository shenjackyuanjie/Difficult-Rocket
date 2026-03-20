use pyo3::prelude::*;

use crate::sr1_parse::ship::{Connection, RawConnectionData};
use crate::sr1_parse::types::IdType;

#[pyclass(skip_from_py_object)]
#[derive(Debug, Clone)]
#[pyo3(name = "SR1Connection_rs")]
pub struct PySR1Connections {
    pub datas: Vec<Connection>,
}

#[pymethods]
impl PySR1Connections {
    fn search_connection_by_parent(&self, parent_id: IdType) -> Vec<RawConnectionData> {
        self.datas
            .iter()
            .filter(|x| x.get_parent() == parent_id && x.is_normal())
            .map(|x| x.as_normal_raw().unwrap())
            .collect()
    }

    fn search_by_child(&self, child_id: IdType) -> Vec<RawConnectionData> {
        self.datas
            .iter()
            .filter(|x| x.get_child() == child_id && x.is_normal())
            .map(|x| x.as_normal_raw().unwrap())
            .collect()
    }

    fn search_by_id(&self, any_id: IdType) -> Vec<RawConnectionData> {
        self.datas
            .iter()
            .filter(|x| (x.get_parent() == any_id || x.get_child() == any_id) && x.is_normal())
            .map(|x| x.as_normal_raw().unwrap())
            .collect()
    }

    fn search_by_both_id(&self, parent_id: IdType, child_id: IdType) -> Vec<RawConnectionData> {
        self.datas
            .iter()
            .filter(|x| x.get_parent() == parent_id && x.get_child() == child_id && x.is_normal())
            .map(|x| x.as_normal_raw().unwrap())
            .collect()
    }

    fn get_raw_data(&self) -> Vec<RawConnectionData> {
        self.datas.iter().filter(|x| x.is_normal()).map(|x| x.as_normal_raw().unwrap()).collect()
    }
}
