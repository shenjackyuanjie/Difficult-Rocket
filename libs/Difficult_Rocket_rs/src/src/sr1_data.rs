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

    use quick_xml::de::from_str;
    // use serde_xml_rs::{from_str};

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
        Satellite,
        None
    }

    #[derive(Debug, Serialize, Deserialize, Copy, Clone)]
    pub enum Location {
        Top,
        Bottom,
        Left,
        Right,

        TopCenter,
        BottomCenter,
        LeftCenter,
        RightCenter,

        TopSide,
        BottomSide,
        LeftSide,
        RightSide
    }

    #[derive(Debug, Serialize, Deserialize, Copy, Clone)]
    pub struct Vertex {
        #[serde(rename = "@x")]
        pub x: Option<f64>,
        #[serde(rename = "@y")]
        pub y: Option<f64>,
    }

    #[derive(Debug, Serialize, Deserialize, Clone)]
    pub struct Shape {
        // #[serde(rename = "Vertex")]
        // pub vertex: Vec<Vertex>,
        #[serde(rename = "@sensor")]
        pub sensor: Option<bool>
    }

    #[derive(Debug, Serialize, Deserialize, Copy, Clone)]
    pub struct AttachPoint {
        pub location: Option<Location>,
        #[serde(rename = "@x")]
        pub x: Option<f64>,
        #[serde(rename = "@y")]
        pub y: Option<f64>,
        #[serde(rename = "@breakAngle")]
        pub break_angle: Option<i32>,
        #[serde(rename = "@breakForce")]
        pub break_force: Option<f64>,
        #[serde(rename = "@fuelLine")]
        pub fuel_line: Option<bool>,
        #[serde(rename = "@group")]
        pub group: Option<i32>,
        #[serde(rename = "@order")]
        pub order: Option<i32>,
    }

    #[derive(Debug, Serialize, Deserialize, Clone)]
    pub struct AttachPoints {
        #[serde(rename = "AttachPoint")]
        pub points: Vec<AttachPoint>
    }

    #[derive(Debug, Serialize, Deserialize, Clone)]
    pub struct PartAttr {
        // 单独类型节点
        // pub part_attr: Option<Vec<PartAttr>>,
    }

    #[derive(Debug, Serialize, Deserialize, Clone)]
    pub struct PartType {
        // https://docs.rs/quick-xml/latest/quick_xml/de/index.html
        // 基本属性
        #[serde(rename = "@id")]
        pub id: String,
        #[serde(rename = "@name")]
        pub name: String,
        #[serde(rename = "@description")]
        pub description: String,
        #[serde(rename = "@sprite")]
        pub sprite: String,
        #[serde(rename = "@type")]
        pub r#type: PartTypes,
        #[serde(rename = "@mass")]
        pub mass: f64,
        #[serde(rename = "@width")]
        pub width: u32,
        #[serde(rename = "@height")]
        pub height: u32,
        // 可选属性
        #[serde(rename = "@friction")]
        pub friction: Option<f64>,
        #[serde(rename = "@category")]
        pub category: Option<Category>,
        #[serde(rename = "@ignoreEditorIntersections")]
        pub ignore_editor_intersections: Option<bool>,
        #[serde(rename = "@disableEditorRotation")]
        pub disable_editor_rotation: Option<bool>,
        #[serde(rename = "@canExplode")]
        pub can_explode: Option<bool>,
        #[serde(rename = "@coverHeight")]
        pub cover_height: Option<u32>,
        #[serde(rename = "@sandboxOnly")]
        pub sandbox_only: Option<bool>,
        #[serde(rename = "@drag")]
        pub drag: Option<f64>,
        #[serde(rename = "@hidden")]
        pub hidden: Option<bool>,
        #[serde(rename = "@buoyancy")]
        pub buoyancy: Option<f64>,
        // 通用属性子节点
        #[serde(rename = "Shape")]
        pub shape: Option<Vec<Shape>>,
        #[serde(rename = "AttachPoints")]
        attach_points: Option<AttachPoints>,
        // #[serde(rename = "$value")]
        // pub value: PartAttr,
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
        let _parts = read_part_list(file_name);
        if let Some(parts) = _parts {
            println!("{:?}", parts)
        }
        // read_part_list(file_name);
        Ok(())
    }

}