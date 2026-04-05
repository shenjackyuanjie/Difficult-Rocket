use std::collections::HashMap;

use pyo3::prelude::*;

use crate::python::data::part_type::PySR1PartType;
use crate::sr1_parse::model::SR1PartList;
use crate::sr1_parse::ship_io::load_part_list_from_file;

#[pyclass(from_py_object)]
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
        let mut data = match load_part_list_from_file(file_path.clone()) {
            Ok(part_list) => part_list,
            Err(e) => {
                println!("ERROR!\n{}\n----------", e);
                panic!("Parse part list failed! {}\n{e}", file_path);
            }
        };
        data.name = list_name;
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
