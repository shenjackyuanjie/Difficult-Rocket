/*
 * -------------------------------
 * Difficult Rocket
 * Copyright © 2020-2023 by shenjackyuanjie 3695888@qq.com
 * All rights reserved
 * -------------------------------
 */

pub mod data {
    use pyo3::prelude::*;
    use serde_xml_rs::from_str;

    use crate::sr1_data::part_list::RawPartList;
    use crate::sr1_data::ship::RawShip;
    use crate::types::sr1::{SR1PartList, SR1PartListTrait, SR1Ship};

    #[pyclass]
    #[pyo3(name = "SR1PartList_rs")]
    #[pyo3(text_signature = "(file_path = './configs/PartList.xml', list_name = 'NewPartList')")]
    pub struct PySR1PartList {
        pub part_list: SR1PartList,
    }

    #[pymethods]
    impl PySR1PartList {
        #[new]
        fn new(file_path: String, list_name: String) -> Self {
            let raw_part_list: RawPartList = RawPartList::from_file(file_path).unwrap();
            Self {
                part_list: raw_part_list.to_sr_part_list(Some(list_name.to_string())),
            }
        }
    }
}
