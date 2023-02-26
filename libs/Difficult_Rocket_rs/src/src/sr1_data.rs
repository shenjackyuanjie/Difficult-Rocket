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

    // use quick_xml::de::from_str;
    use serde_xml_rs::{from_str};

    #[derive(Debug, Serialize, Deserialize, Clone)]
    pub struct PartList {
        #[serde(rename = "PartType")]
        part_types: Vec<PartType>,
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
        lander,
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
        RightSide,
    }

    #[derive(Debug, Serialize, Deserialize, Copy, Clone)]
    pub struct Vertex {
        pub x: Option<f64>,
        pub y: Option<f64>,
    }

    #[derive(Debug, Serialize, Deserialize, Clone)]
    pub struct Shape {
        #[serde(rename = "Vertex")]
        pub vertex: Vec<Vertex>,
        #[serde(rename = "sensor")]
        pub sensor: Option<bool>,
    }

    #[derive(Debug, Serialize, Deserialize, Copy, Clone)]
    pub struct AttachPoint {
        pub location: Option<Location>,
        pub x: Option<f64>,
        pub y: Option<f64>,
        #[serde(rename = "flipX")]
        pub flip_x: Option<bool>,
        #[serde(rename = "flipY")]
        pub flip_y: Option<bool>,
        #[serde(rename = "breakAngle")]
        pub break_angle: Option<i32>,
        #[serde(rename = "breakForce")]
        pub break_force: Option<f64>,
        #[serde(rename = "fuelLine")]
        pub fuel_line: Option<bool>,
        pub group: Option<i32>,
        pub order: Option<i32>,
    }

    #[derive(Debug, Serialize, Deserialize, Clone)]
    pub struct AttachPoints {
        #[serde(rename = "AttachPoint")]
        pub points: Vec<AttachPoint>,
    }

    #[derive(Debug, Serialize, Deserialize, Copy, Clone)]
    pub struct Damage {
        disconnect: u32,
        explode: u32,
        #[serde(rename = "explosionPower")]
        explosion_power: u32,
        #[serde(rename = "explosionSize")]
        explosion_size: u32,
    }

    #[derive(Debug, Serialize, Deserialize, Copy, Clone)]
    pub struct Tank {
        fuel: f64,
        #[serde(rename = "dryMass")]
        dry_mass: f64,
    }

    #[derive(Debug, Serialize, Deserialize, Copy, Clone)]
    pub struct Engine {
        power: f64,
        consumption: f64,
        size: f64,
        turn: f64,
        #[serde(rename = "fuelType")]
        fuel_type: Option<i32>,
        #[serde(rename = "throttleExponential")]
        throttle_exponential: Option<bool>,
    }

    #[derive(Debug, Serialize, Deserialize, Copy, Clone)]
    pub struct Rcs {
        power: f64,
        consumption: f64,
        size: f64,
    }

    #[derive(Debug, Serialize, Deserialize, Copy, Clone)]
    pub struct Solar {
        #[serde(rename = "chargeRate")]
        charge_rate: f64,
    }

    #[derive(Debug, Serialize, Deserialize, Copy, Clone)]
    pub struct Lander {
        #[serde(rename = "maxAngle")]
        max_angle: i32,
        #[serde(rename = "minLength")]
        min_length: f64,
        #[serde(rename = "maxLength")]
        max_length: f64,
        #[serde(rename = "angleSpeed")]
        angle_speed: Option<i32>,
        #[serde(rename = "lengthSpeed")]
        length_speed: Option<f64>,
        width: f64,
    }

    #[derive(Debug, Serialize, Deserialize, Clone)]
    pub struct PartType {
        // 基本属性
        pub id: String,
        pub name: String,
        pub description: String,
        pub sprite: String,
        pub r#type: PartTypes,
        pub mass: f64,
        pub width: u32,
        pub height: u32,
        // 可选属性
        pub friction: Option<f64>,
        pub category: Option<String>,
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
        // 通用属性子节点
        #[serde(rename = "Shape")]
        pub shape: Option<Vec<Shape>>,
        #[serde(rename = "AttachPoints")]
        pub attach_points: Option<AttachPoints>,
        #[serde(rename = "Damage")]
        pub damage: Option<Damage>,
        // 特殊属性子节点
        #[serde(rename = "Tank")]
        pub tank: Option<Tank>,
        #[serde(rename = "Engine")]
        pub engine: Option<Engine>,
        #[serde(rename = "Tank")]
        pub rcs: Option<Rcs>,
        #[serde(rename = "Solar")]
        pub solar: Option<Solar>,
        #[serde(rename = "Lander")]
        pub lander: Option<Lander>,
    }

    impl PartList {
        pub fn list_print(&self) -> () {
            for part_data in self.part_types.iter() {
                println!("{:?}\n", part_data);
            }
        }
    }

    #[inline]
    pub fn read_part_list(file_name: String) -> Option<PartList> {
        let part_list_file = fs::read_to_string(file_name.to_string());

        match part_list_file {
            Ok(part_list_file) => {
                let part_list: PartList = from_str(part_list_file.as_str()).unwrap();
                Some(part_list)
            }
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
            // println!("{:?}", parts)
            parts.list_print()
        }
        // read_part_list(file_name);
        Ok(())
    }
}