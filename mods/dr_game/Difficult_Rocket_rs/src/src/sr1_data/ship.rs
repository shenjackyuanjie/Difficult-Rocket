use std::error::Error;
use std::fs;

use pyo3::prelude::*;
use serde::{Deserialize, Serialize};
// use quick_xml::de::from_str;
use serde_xml_rs::from_str;
use serde_xml_rs::Error as XmlError;

use super::part_list::SR1PartTypeEnum;

use crate::data_type::sr1::{IdType, SR1PartData, SR1PartDataAttr, SR1Ship};
use crate::data_type::sr1::{SR1PartDataTrait, SR1PartTypeAttr, SR1ShipTrait};

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
    pub touch_ground: Option<i8>, // Option for https://github.com/shenjackyuanjie/Difficult-Rocket/issues/49
    // SR1 says it's optional, let them happy
    // NOT always 0
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
        let attr = SR1PartDataAttr::from_raw(self, None, true);
        let part_type = attr.get_part_type();
        SR1PartData {
            attr,
            x: self.x.to_owned(),
            y: self.y.to_owned(),
            id: self.id.to_owned(),
            angle: self.angle.to_owned(),
            angle_v: self.angle_v.to_owned(),
            flip_x: self.flip_x.unwrap_or(0_i8) != 0,
            flip_y: self.flip_y.unwrap_or(0_i8) != 0,
            editor_angle: self.editor_angle.unwrap_or(0_i32),
            part_type,
            part_type_id: self.part_type_id.clone(),
            active: self.activated.unwrap_or(0_i8) != 0,
            explode: self.exploded.unwrap_or(0_i8) != 0,
        }
    }

    fn to_raw_part_data(&self) -> Part {
        self.clone()
    }
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
            lift_off: self.lift_off != 0,
            touch_ground: self.touch_ground.to_owned().map(|i| i != 0).unwrap_or(true),
            disconnected,
        }
    }

    #[inline]
    fn to_raw_ship(&self) -> RawShip {
        self.clone()
    }
}

impl RawShip {
    #[inline]
    pub fn from_file(path: String) -> Option<RawShip> {
        let ship_file = fs::read_to_string(path); // for encoding error
        if let Err(e) = ship_file {
            println!("ERROR!\n{:?}\n----------", e);
            return None;
        }
        let ship_file = ship_file.unwrap();
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
        }
    }
    Ok(true)
}
