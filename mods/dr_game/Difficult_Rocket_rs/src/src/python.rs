/*
 * -------------------------------
 * Difficult Rocket
 * Copyright © 2020-2023 by shenjackyuanjie 3695888@qq.com
 * All rights reserved
 * -------------------------------
 */

pub mod data {
    use std::collections::HashMap;

    use pyo3::prelude::*;

    use crate::sr1_data::part_list::RawPartList;
    use crate::types::sr1::{get_max_box, SR1PartData, SR1PartListTrait};
    use crate::types::sr1::{SR1PartList, SR1PartType, SR1Ship};

    #[pyclass]
    #[pyo3(name = "SR1PartType_rs")]
    pub struct PySR1PartType {
        pub data: SR1PartType,
    }

    #[pymethods]
    impl PySR1PartType {
        #[getter]
        fn get_name(&self) -> String { self.data.name.clone() }

        #[getter]
        fn get_mass(&self) -> f64 { self.data.mass.to_owned() }
    }

    impl PySR1PartType {
        pub fn new(data: SR1PartType) -> Self { Self { data } }
    }

    #[pyclass]
    #[pyo3(name = "SR1PartList_rs")]
    #[pyo3(text_signature = "(file_path = './configs/PartList.xml', list_name = 'NewPartList')")]
    pub struct PySR1PartList {
        pub data: SR1PartList,
    }

    #[pymethods]
    impl PySR1PartList {
        #[new]
        fn new(file_path: String, list_name: String) -> Self {
            let raw_part_list: RawPartList = RawPartList::from_file(file_path).unwrap();
            let data = raw_part_list.to_sr_part_list(Some(list_name));
            Self { data }
        }

        fn as_dict(&self) -> HashMap<String, PySR1PartType> {
            self.data.get_cache().iter().map(|(k, v)| (k.clone(), PySR1PartType::new(v.clone()))).collect()
        }

        fn get_part_type(&self, name: String) -> Option<PySR1PartType> {
            let part_type = self.data.get_part_type(name.clone());
            if let Some(part_type) = part_type {
                Some(PySR1PartType::new(part_type.clone()))
            } else {
                None
            }
        }
    }

    #[pyclass]
    #[pyo3(name = "SR1PartData_rs")]
    pub struct PySR1PartData {
        pub data: SR1PartData,
    }

    #[pyclass]
    #[pyo3(name = "SR1Ship_rs")]
    #[pyo3(text_signature = "(file_path = './configs/dock1.xml', part_list = './configs/PartList.xml', ship_name = 'NewShip')")]
    pub struct PySR1Ship {
        pub ship: SR1Ship,
        pub part_list: SR1PartList,
    }

    #[pymethods]
    impl PySR1Ship {
        #[new]
        fn new(file_path: String, part_list: String, ship_name: String) -> Self {
            let ship = SR1Ship::from_file(file_path, Some(ship_name)).unwrap();
            let part_list = SR1PartList::from_file(part_list).unwrap();
            Self { ship, part_list }
        }

        fn get_img_pos(&self) -> (i64, i64, i64, i64) {
            let mut img_pos = (0, 0, 0, 0);
            // -x, -y, +x, +y
            // 左下角，右上角
            let mut max_box = get_max_box(&self.ship.parts, &self.part_list);
            todo!();
            // img_pos
        }

        fn get_name(&self) -> String { self.ship.name.clone() }

        fn get_description(&self) -> String { self.ship.description.clone() }

        fn get_lift_off(&self) -> bool { self.ship.lift_off.to_owned() }

        fn get_touch_ground(&self) -> bool { self.ship.touch_ground.to_owned() }
    }
}

pub mod translate {
    use pyo3::prelude::*;
    use pyo3::types::PyDict;

    #[pyclass]
    #[pyo3(name = "TranslateConfig_rs")]
    #[pyo3(text_signature = "(language, raise_error = False, replace_normal = False, add_error = False, is_result = False, keep_get = False)")]
    pub struct PyTranslateConfig {
        pub raise_error: bool,
        pub replace_normal: bool,
        pub add_error: bool,
        pub is_result: bool,
        pub keep_get: bool,
        pub language: String,
    }

    #[pymethods]
    impl PyTranslateConfig {
        #[new]
        fn new(py_: Python, raise_error: bool, replace_normal: bool, language: Option<String>) -> Self {
            let dr_runtime = PyModule::import(py_, "Difficult_Rocket").unwrap().get_item("DR_runtime").unwrap();
            let default_language = dr_runtime.get_item("language").unwrap().extract::<String>().unwrap();
            Self {
                raise_error,
                replace_normal,
                add_error: false,
                is_result: false,
                keep_get: false,
                language: language.unwrap_or(default_language),
            }
        }

        // fn set(&self, py_: Python, item: String, value: BoolString) -> &Self {
        //     match item.as_str() {
        //         "raise_error" => self,
        //         _ => self,
        //     }
        // }
    }

    #[pyclass]
    pub struct PyTranslate {
        pub data: Py<PyAny>,
        pub get_list: Vec<(String, bool)>,
        pub config: PyTranslateConfig,
    }

    #[pymethods]
    impl PyTranslate {
        #[new]
        fn py_new(py_: Python, data: &PyAny) -> Self {
            let _ = data.is_instance_of::<PyDict>();
            Self {
                data: data.into_py(py_),
                get_list: Vec::new(),
                config: PyTranslateConfig::new(py_, false, false, None),
            }
        }
    }
}

pub mod console {
    use std::println;

    use pyo3::prelude::*;

    #[pyclass]
    #[pyo3(name = "Console_rs")]
    pub struct PyConsole {
        /// 向子线程发送结束信号
        pub stop_sender: Option<std::sync::mpsc::Sender<()>>,
        pub keyboard_input_receiver: Option<std::sync::mpsc::Receiver<String>>,
    }

    #[pymethods]
    impl PyConsole {
        #[new]
        fn new() -> Self {
            Self {
                stop_sender: None,
                keyboard_input_receiver: None,
            }
        }

        fn start(&mut self) {
            let (stop_sender, stop_receiver) = std::sync::mpsc::channel();
            let (keyboard_input_sender, keyboard_input_receiver) = std::sync::mpsc::channel();
            std::thread::spawn(move || {
                let std_in = std::io::stdin();
                loop {
                    if let Ok(()) = stop_receiver.try_recv() {
                        break;
                    }
                    let mut input = String::new();
                    let _ = std_in.read_line(&mut input);
                    if !input.is_empty() {
                        keyboard_input_sender.send(input).unwrap();
                    }
                    print!(">>");
                }
            });
            self.stop_sender = Some(stop_sender);
            self.keyboard_input_receiver = Some(keyboard_input_receiver);
        }

        fn stop(&self) -> bool {
            if let Some(sender) = &self.stop_sender {
                sender.send(()).unwrap();
                return true;
            }
            false
        }

        fn get_command(&self) -> Option<String> {
            // 获取输入
            if let Some(receiver) = &self.keyboard_input_receiver {
                if let Ok(string) = receiver.try_recv() {
                    return Some(string);
                }
            }
            None
        }
    }
}
