/*
 * -------------------------------
 * Difficult Rocket
 * Copyright © 2020-2023 by shenjackyuanjie 3695888@qq.com
 * All rights reserved
 * -------------------------------
 */

pub mod part_list {
    use std::fs;

    use pyo3::prelude::*;
    use serde::{Serialize, Deserialize};
    use serde_xml_rs::{from_str};

    #[derive(Debug, Serialize, Deserialize, Clone)]
    pub struct PartList {
        #[serde(rename = "PartType")]
        part_types: Vec<PartType>
    }

    #[allow(non_camel_case_types)]
    #[derive(Debug, Serialize, Deserialize, Copy, Clone)]
    pub enum PartTypes {
        pod,
        detacher,
        wheel,
        fuselage,
        strut,
        tank,
        engine,
        parachute,
        nosecone,
        rcs,
        solar,
        dockconnector,
        dockport,
        lander
    }

    #[derive(Debug, Serialize, Deserialize, Copy, Clone)]
    pub enum Category {
        Satellite
    }

    #[derive(Debug, Serialize, Deserialize, Clone)]
    pub struct Vertex {
        pub x: f64,
        pub y: f64
    }

    #[derive(Debug, Serialize, Deserialize, Clone)]
    pub struct PartType {
        pub id: String,
        pub name: String,
        pub description: String,
        pub sprite: String,
        pub r#type: PartTypes,
        pub mass: f64,
        pub width: u32,
        pub height: u32,
        pub friction: Option<f64>,
        pub category: Option<Category>,
        #[serde(rename = "ignoreEditorIntersections")]
        pub ignore_editor_intersections: Option<bool>,
        #[serde(rename = "disableEditorRotation")]
        pub disable_editor_rotation: Option<bool>,
        #[serde(rename = "canExplode")]
        pub can_explode: Option<bool>,
        #[serde(rename = "coverHeight")]
        pub cover_height: Option<u32>,
        #[serde(rename = "sandboxOnly")]
        pub sandbox_only: Option<bool>,
        pub drag: Option<f64>,
        pub hidden: Option<bool>,
        pub buoyancy: Option<f64>,
        #[serde(rename = "@Shape")]
        pub shapes: Option<Vec<Vertex>>
    }

    #[inline]
    pub fn read_part_list(file_name: String) -> Option<PartList> {
        let part_list_file = fs::read_to_string(file_name.to_string());
        match part_list_file {
            Ok(part_list_file) => {
                let part_list: PartList = from_str(part_list_file.as_str()).unwrap();
                Some(part_list)
            },
            Err(_) => {
                println!("Error while reading File {}", file_name);
                None
            }
        }
    }

    #[pyfunction]
    #[pyo3(name = "part_list_read_test", signature = (file_name = "./configs/PartList.xml".to_string()))]
    pub fn read_part_list_py(_py: Python, file_name: Option<String>) -> PyResult<()> {
        let file_name = file_name.unwrap_or("./configs/PartList.xml".to_string());
        // let parts = read_part_list(file_name);
        read_part_list(file_name);
        Ok(())
    }

}