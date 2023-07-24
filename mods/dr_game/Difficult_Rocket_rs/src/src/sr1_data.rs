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
    use serde::{Deserialize, Serialize};
    // use quick_xml::de::from_str;
    use crate::types::sr1::{SR1PartList, SR1PartType, SR1PartTypeAttr};
    use crate::types::sr1::{SR1PartListTrait, SR1PartTypeData};
    use serde_xml_rs::from_str;

    #[derive(Debug, Serialize, Deserialize, Clone)]
    pub struct RawPartList {
        #[serde(rename = "PartType")]
        pub part_types: Vec<RawPartType>,
    }

    #[allow(non_camel_case_types)]
    #[derive(Debug, Serialize, Deserialize, Copy, Clone, PartialEq)]
    pub enum SR1PartTypeEnum {
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

    impl AttachPoints {
        #[inline]
        pub fn new(attaches: Vec<AttachPoint>) -> Self { AttachPoints { points: attaches } }

        #[inline]
        pub fn unzip(&self) -> Vec<AttachPoint> { self.points.clone() }
    }

    #[derive(Debug, Serialize, Deserialize, Copy, Clone)]
    pub struct Damage {
        pub disconnect: i32,
        pub explode: i32,
        #[serde(rename = "explosionPower")]
        pub explosion_power: Option<u32>,
        #[serde(rename = "explosionSize")]
        pub explosion_size: Option<u32>,
    }

    impl Damage {
        #[inline]
        pub fn to_damage(&self) -> crate::types::sr1::Damage {
            crate::types::sr1::Damage {
                disconnect: self.disconnect.to_owned(),
                explode: self.explode.to_owned(),
                explosion_power: self.explosion_power.unwrap_or(100),
                explosion_size: self.explosion_size.unwrap_or(100),
            }
        }
    }

    #[derive(Debug, Serialize, Deserialize, Copy, Clone)]
    pub struct Tank {
        pub fuel: f64,
        #[serde(rename = "dryMass")]
        pub dry_mass: f64,
        #[serde(rename = "fuelType")]
        pub fuel_type: Option<i32>,
        // 0 -> 普通燃料
        // 1 -> Rcs
        // 2 -> 电量
        // 3 -> 固推
    }

    #[derive(Debug, Serialize, Deserialize, Copy, Clone)]
    pub struct Engine {
        pub power: f64,
        pub consumption: f64,
        pub size: f64,
        pub turn: f64,
        #[serde(rename = "fuelType")]
        pub fuel_type: Option<i32>,
        #[serde(rename = "throttleExponential")]
        pub throttle_exponential: Option<bool>,
    }

    #[derive(Debug, Serialize, Deserialize, Copy, Clone)]
    pub struct Rcs {
        pub power: f64,
        pub consumption: f64,
        pub size: f64,
    }

    #[derive(Debug, Serialize, Deserialize, Copy, Clone)]
    pub struct Solar {
        #[serde(rename = "chargeRate")]
        pub charge_rate: f64,
    }

    #[derive(Debug, Serialize, Deserialize, Copy, Clone)]
    pub struct Lander {
        #[serde(rename = "maxAngle")]
        pub max_angle: f64,
        #[serde(rename = "minLength")]
        pub min_length: f64,
        #[serde(rename = "maxLength")]
        pub max_length: f64,
        #[serde(rename = "angleSpeed")]
        pub angle_speed: Option<f64>,
        #[serde(rename = "lengthSpeed")]
        pub length_speed: Option<f64>,
        pub width: f64,
    }

    #[derive(Debug, Serialize, Deserialize, Clone)]
    pub struct RawPartType {
        // 基本属性
        pub id: String,
        pub name: String,
        pub description: String,
        pub sprite: String,
        pub r#type: SR1PartTypeEnum,
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
        #[serde(rename = "Rcs")]
        pub rcs: Option<Rcs>,
        #[serde(rename = "Solar")]
        pub solar: Option<Solar>,
        #[serde(rename = "Lander")]
        pub lander: Option<Lander>,
    }

    impl SR1PartTypeData for RawPartType {
        #[inline]
        fn to_sr_part_type(&self) -> SR1PartType {
            let part_attr: Option<SR1PartTypeAttr> = match self.r#type {
                SR1PartTypeEnum::tank => {
                    let tank = self.tank.unwrap();
                    Some(SR1PartTypeAttr::Tank {
                        fuel: tank.fuel,
                        dry_mass: tank.dry_mass,
                        fuel_type: tank.fuel_type.unwrap_or(0),
                    })
                }
                SR1PartTypeEnum::engine => {
                    let engine = self.engine.unwrap();
                    Some(SR1PartTypeAttr::Engine {
                        power: engine.power,
                        consumption: engine.consumption,
                        size: engine.size,
                        turn: engine.turn,
                        fuel_type: engine.fuel_type.unwrap_or(0),
                        throttle_exponential: engine.throttle_exponential.unwrap_or(false),
                    })
                }
                SR1PartTypeEnum::rcs => {
                    let rcs = self.rcs.unwrap();
                    Some(SR1PartTypeAttr::Rcs {
                        power: rcs.power,
                        consumption: rcs.consumption,
                        size: rcs.size,
                    })
                }
                SR1PartTypeEnum::solar => {
                    let solar = self.solar.unwrap();
                    Some(SR1PartTypeAttr::Solar {
                        charge_rate: solar.charge_rate,
                    })
                }
                SR1PartTypeEnum::lander => {
                    let lander = self.lander.unwrap();
                    Some(SR1PartTypeAttr::Lander {
                        max_angle: lander.max_angle,
                        min_length: lander.min_length,
                        max_length: lander.max_length,
                        angle_speed: lander.angle_speed.unwrap_or(0.0),
                        length_speed: lander.length_speed.unwrap_or(0.0),
                        width: lander.width,
                    })
                }
                _ => None,
            };
            let damage = self.damage.unwrap_or(Damage {
                disconnect: 0,
                explode: 0,
                explosion_power: Some(0u32),
                explosion_size: Some(0u32),
            });
            let attach_points: Option<Vec<AttachPoint>> = if let Some(attach_points) = &self.attach_points {
                Some(attach_points.unzip())
            } else {
                None
            };
            SR1PartType {
                id: self.id.clone(),
                name: self.name.clone(),
                description: self.description.clone(),
                sprite: self.sprite.clone(),
                p_type: self.r#type,
                mass: self.mass.to_owned(),
                width: self.width.to_owned(),
                height: self.height.to_owned(),
                friction: self.friction.unwrap_or(0.0),
                category: self.category.clone().unwrap_or("".to_string()),
                ignore_editor_intersections: self.ignore_editor_intersections.unwrap_or(false),
                disable_editor_rotation: self.disable_editor_rotation.unwrap_or(false),
                can_explode: self.can_explode.unwrap_or(false),
                cover_height: self.cover_height.unwrap_or(0),
                sandbox_only: self.sandbox_only.unwrap_or(false),
                drag: self.drag.unwrap_or(0.0),
                hidden: self.hidden.unwrap_or(false),
                buoyancy: self.buoyancy.unwrap_or(0.0),
                shape: None,
                damage: damage.to_damage(),
                attach_points,
                attr: part_attr,
            }
        }
        fn to_raw_part_type(&self) -> RawPartType { self.clone() }
    }

    impl RawPartList {
        #[inline]
        pub fn new(parts: Vec<RawPartType>) -> Self { RawPartList { part_types: parts } }

        #[inline]
        pub fn from_file(file_name: String) -> Option<RawPartList> {
            let part_list_file = fs::read_to_string(file_name).unwrap();
            let part_list: RawPartList = from_str(part_list_file.as_str()).unwrap();
            Some(part_list)
        }

        #[inline]
        pub fn list_print(&self) -> () {
            for part_data in self.part_types.iter() {
                println!("{:?}\n", part_data);
            }
        }
    }

    impl SR1PartListTrait for RawPartList {
        #[inline]
        fn to_sr_part_list(&self, name: Option<String>) -> SR1PartList {
            let mut types: Vec<SR1PartType> = Vec::new();
            for part_data in self.part_types.iter() {
                types.push(part_data.to_sr_part_type());
            }
            SR1PartList::part_types_new(types, name)
        }

        fn to_raw_part_list(&self) -> RawPartList { return self.clone(); }
    }

    #[inline]
    #[pyfunction]
    #[pyo3(name = "part_list_read_test", signature = (file_name = "./assets/builtin/PartList.xml".to_string()))]
    pub fn read_part_list_py(_py: Python, file_name: Option<String>) -> PyResult<()> {
        let file_name = file_name.unwrap_or("./assets/builtin/PartList.xml".to_string());
        let _parts = RawPartList::from_file(file_name);
        if let Some(parts) = _parts {
            // println!("{:?}", parts)
            parts.list_print();
            let _part_list = parts.to_sr_part_list(Some("Vanilla".to_string()));
        }
        Ok(())
    }
}

#[allow(unused)]
pub mod ship {
    use std::error::Error;
    use std::fs;

    use pyo3::prelude::*;
    use serde::{Deserialize, Serialize};
    // use quick_xml::de::from_str;
    use serde_xml_rs::from_str;
    use serde_xml_rs::Error as XmlError;

    use super::part_list::SR1PartTypeEnum;

    use crate::types::sr1::{i8_to_bool, SR1PartDataTrait, SR1PartTypeAttr, SR1ShipTrait};
    use crate::types::sr1::{IdType, SR1PartData, SR1PartDataAttr, SR1Ship};

    #[derive(Debug, Serialize, Deserialize, Clone)]
    #[serde(rename = "Ship")]
    pub struct RawShip {
        #[serde(rename = "Parts")]
        pub parts: Parts,
        #[serde(rename = "Connections")]
        pub connects: Connections,
        pub version: Option<i32>, // Option for https://github.com/shenjackyuanjie/Difficult-Rocket/issues/48
        // SR1 says version is also optional, let them happy
        // it's always 1
        #[serde(rename = "liftedOff")]
        pub lift_off: i8,
        #[serde(rename = "touchingGround")]
        pub touch_ground: i8,
        #[serde(rename = "DisconnectedParts")]
        pub disconnected: Option<DisconnectedParts>,
    }

    #[derive(Debug, Serialize, Deserialize, Clone)]
    pub struct Parts {
        #[serde(rename = "Part")]
        pub parts: Vec<Part>,
    }

    #[derive(Debug, Serialize, Deserialize, Clone)]
    pub struct Connections {
        #[serde(rename = "Connection")]
        pub connects: Option<Vec<Connection>>,
    }

    #[derive(Debug, Serialize, Deserialize, Clone)]
    pub struct Part {
        #[serde(rename = "Tank")]
        pub tank: Option<Tank>,
        #[serde(rename = "Engine")]
        pub engine: Option<Engine>,
        #[serde(rename = "Pod")]
        pub pod: Option<Pod>,
        #[serde(rename = "partType")]
        pub part_type_id: String,
        pub id: i64,
        pub x: f64,
        pub y: f64,
        #[serde(rename = "editorAngle")]
        pub editor_angle: Option<i32>, // Option for https://github.com/shenjackyuanjie/Difficult-Rocket/issues/47
        // SR1 says it's optional, let them happy
        pub angle: f64,
        #[serde(rename = "angleV")]
        pub angle_v: f64,
        #[serde(rename = "flippedX")]
        pub flip_x: Option<i8>,
        #[serde(rename = "flippedY")]
        pub flip_y: Option<i8>,
        // 降落伞
        #[serde(rename = "chuteX")]
        pub chute_x: Option<f64>,
        #[serde(rename = "chuteY")]
        pub chute_y: Option<f64>,
        #[serde(rename = "chuteAngle")]
        pub chute_angle: Option<f64>,
        #[serde(rename = "chuteHeight")]
        pub chute_height: Option<f64>,
        pub extension: Option<f64>,
        pub inflate: Option<i8>,
        pub inflation: Option<f64>,
        pub exploded: Option<i8>,
        pub rope: Option<i8>,
        // ?
        pub activated: Option<i8>,
        pub deployed: Option<i8>,
    }

    #[derive(Debug, Serialize, Deserialize, Clone)]
    pub struct Engine {
        pub fuel: f64,
    }

    #[derive(Debug, Serialize, Deserialize, Clone)]
    pub struct Tank {
        pub fuel: f64,
    }

    #[derive(Debug, Serialize, Deserialize, Clone)]
    pub struct Pod {
        #[serde(rename = "Staging")]
        pub stages: Staging,
        pub name: String,
        pub throttle: f64,
    }

    #[derive(Debug, Serialize, Deserialize, Clone)]
    pub struct Staging {
        #[serde(rename = "currentStage")]
        pub current_stage: i32,
        #[serde(rename = "Step")]
        pub steps: Option<Vec<Step>>,
    }

    #[derive(Debug, Serialize, Deserialize, Clone)]
    pub struct Step {
        #[serde(rename = "Activate")]
        pub activates: Option<Vec<Activate>>, // Option for https://github.com/shenjackyuanjie/Difficult-Rocket/issues/21
    }

    #[derive(Debug, Serialize, Deserialize, Clone)]
    #[serde(rename = "Activate")]
    pub struct Activate {
        #[serde(rename = "Id")]
        pub id: i64,
        pub moved: i8, // 1 or 0
    }

    #[derive(Debug, Serialize, Deserialize, Clone)]
    pub struct DisconnectedParts {
        #[serde(rename = "DisconnectedPart")]
        pub parts: Option<Vec<DisconnectedPart>>,
    }

    #[derive(Debug, Serialize, Deserialize, Clone)]
    pub struct DisconnectedPart {
        #[serde(rename = "Parts")]
        pub parts: Parts,
        #[serde(rename = "Connections")]
        pub connects: Connections,
    }

    #[derive(Debug, Serialize, Deserialize, Clone)]
    pub struct Connection {
        #[serde(rename = "parentAttachPoint")]
        pub parent_attach_point: i32,
        #[serde(rename = "childAttachPoint")]
        pub child_attach_point: i32,
        #[serde(rename = "parentPart")]
        pub parent_part: IdType,
        #[serde(rename = "childPart")]
        pub child_part: IdType,
    }

    impl SR1PartDataTrait for Part {
        fn to_sr_part_data(&self) -> SR1PartData {
            let attr = SR1PartDataAttr::from_raw(&self, None, true);
            let part_type = attr.get_part_type();
            SR1PartData {
                attr,
                x: self.x.to_owned(),
                y: self.y.to_owned(),
                id: self.id.to_owned(),
                angle: self.angle.to_owned(),
                angle_v: self.angle_v.to_owned(),
                flip_x: i8_to_bool(self.flip_x.unwrap_or(0_i8)),
                flip_y: i8_to_bool(self.flip_y.unwrap_or(0_i8)),
                editor_angle: self.editor_angle.unwrap_or(0_i32),
                part_type,
                part_type_id: self.part_type_id.clone(),
                active: i8_to_bool(self.activated.unwrap_or(0_i8)),
                explode: i8_to_bool(self.exploded.unwrap_or(0_i8)),
            }
        }

        fn to_raw_part_data(&self) -> Part { self.clone() }
    }

    impl SR1ShipTrait for RawShip {
        #[inline]
        fn to_sr_ship(&self, name: Option<String>) -> SR1Ship {
            let mut parts = Vec::new();
            for part in &self.parts.parts {
                parts.push(part.to_sr_part_data());
            }
            let disconnected = match &self.disconnected {
                Some(disconnect) => match &disconnect.parts {
                    Some(disconnected_parts) => {
                        let mut disconnected_parts_vec = Vec::new();
                        for disconnected_part in disconnected_parts {
                            let mut parts_vec = Vec::new();
                            for part in &disconnected_part.parts.parts {
                                parts_vec.push(part.to_sr_part_data());
                            }
                            disconnected_parts_vec.push((parts_vec, disconnected_part.connects.connects.clone()));
                        }
                        Some(disconnected_parts_vec)
                    }
                    None => None,
                },
                _ => None,
            };
            let connections = match &self.connects.connects {
                Some(connections) => connections.clone(),
                _ => Vec::new(),
            };
            SR1Ship {
                name: name.unwrap_or("NewShip".to_string()),
                description: "".to_string(),
                version: self.version.unwrap_or(1_i32),
                parts,
                connections,
                lift_off: i8_to_bool(self.lift_off.to_owned()),
                touch_ground: i8_to_bool(self.touch_ground.to_owned()),
                disconnected,
            }
        }

        #[inline]
        fn to_raw_ship(&self) -> RawShip { self.clone() }
    }

    impl RawShip {
        #[inline]
        pub fn from_file(path: String) -> Option<RawShip> {
            let ship_file = fs::read_to_string(path).unwrap();
            let ship = from_str(&ship_file);
            match ship {
                Ok(ship) => Some(ship),
                Err(e) => {
                    println!("ERROR!\n{:?}\n----------", e);
                    match e {
                        XmlError::ParseIntError { source } => {
                            println!("ParseIntError: {:?}", source.kind());
                            None
                        }
                        _ => None,
                    }
                }
            }
        }

        #[inline]
        pub fn save(&self, file_name: String) -> Option<()> {
            let part_list_file = serde_xml_rs::to_string(self);
            print!("{:?}", part_list_file);
            if let Ok(part_list_file) = part_list_file {
                fs::write(file_name, part_list_file).unwrap();
                Some(())
            } else {
                None
            }
        }
    }

    #[pyfunction]
    #[pyo3(name = "read_ship_test")]
    #[pyo3(signature = (path = "./assets/builtin/dock1.xml".to_string()))]
    pub fn py_raw_ship_from_file(path: String) -> PyResult<bool> {
        let file = fs::read_to_string(path).unwrap();
        let raw_ship = from_str::<RawShip>(&file);
        match raw_ship {
            Ok(ship) => {
                println!("{:?}", ship);
            }
            Err(e) => {
                println!("{:?}", e);
                // println!("{:?}", e.provide());
            }
        }
        Ok(true)
    }
}
