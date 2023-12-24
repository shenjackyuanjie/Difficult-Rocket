use crate::sr1_parse::{SR1PartList, SR1PartType, SR1PartTypeAttr};
use crate::sr1_parse::{SR1PartListTrait, SR1PartTypeData};

use fs_err as fs;
use pyo3::prelude::*;
use quick_xml::de::from_str;
use serde::{Deserialize, Serialize};

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

impl From<SR1PartTypeEnum> for String {
    fn from(val: SR1PartTypeEnum) -> Self {
        match val {
            SR1PartTypeEnum::pod => "pod".to_string(),
            SR1PartTypeEnum::detacher => "detacher".to_string(),
            SR1PartTypeEnum::wheel => "wheel".to_string(),
            SR1PartTypeEnum::fuselage => "fuselage".to_string(),
            SR1PartTypeEnum::strut => "strut".to_string(),
            SR1PartTypeEnum::tank => "tank".to_string(),
            SR1PartTypeEnum::engine => "engine".to_string(),
            SR1PartTypeEnum::parachute => "parachute".to_string(),
            SR1PartTypeEnum::nosecone => "nosecone".to_string(),
            SR1PartTypeEnum::rcs => "rcs".to_string(),
            SR1PartTypeEnum::solar => "solar".to_string(),
            SR1PartTypeEnum::dockconnector => "dockconnector".to_string(),
            SR1PartTypeEnum::dockport => "dockport".to_string(),
            SR1PartTypeEnum::lander => "lander".to_string(),
        }
    }
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
    #[serde(rename = "@x")]
    pub x: Option<f64>,
    #[serde(rename = "@y")]
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
    #[serde(rename = "@x")]
    pub x: Option<f64>,
    #[serde(rename = "@y")]
    pub y: Option<f64>,
    #[serde(rename = "@flipX")]
    pub flip_x: Option<bool>,
    #[serde(rename = "@flipY")]
    pub flip_y: Option<bool>,
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
    pub points: Vec<AttachPoint>,
}

impl AttachPoints {
    pub fn new(attaches: Vec<AttachPoint>) -> Self {
        AttachPoints { points: attaches }
    }

    pub fn unzip(&self) -> Vec<AttachPoint> {
        self.points.clone()
    }
}

#[derive(Debug, Serialize, Deserialize, Copy, Clone)]
pub struct Damage {
    #[serde(rename = "@disconnect")]
    pub disconnect: f64,
    #[serde(rename = "@explode")]
    pub explode: f64,
    #[serde(rename = "@explosionPower")]
    pub explosion_power: Option<f64>,
    #[serde(rename = "@explosionSize")]
    pub explosion_size: Option<f64>,
}

impl Damage {
    pub fn take_damage(&self) -> crate::sr1_parse::Damage {
        crate::sr1_parse::Damage {
            disconnect: self.disconnect,
            explode: self.explode,
            explosion_power: self.explosion_power.unwrap_or(100_f64),
            explosion_size: self.explosion_size.unwrap_or(100_f64),
        }
    }
}

// This enumeration can be considered to replace the integer-represented "fuel type".
pub enum FuelType {
    Common,
    Rcs,
    Battery,
    Soild,
}

#[derive(Debug, Serialize, Deserialize, Copy, Clone)]
pub struct Tank {
    #[serde(rename = "@fuel")]
    pub fuel: f64,
    #[serde(rename = "@dryMass")]
    pub dry_mass: f64,
    // 0 -> 普通燃料
    // 1 -> Rcs
    // 2 -> 电量
    // 3 -> 固推
    #[serde(rename = "@fuelType")]
    pub fuel_type: Option<i32>,
}

#[derive(Debug, Serialize, Deserialize, Copy, Clone)]
pub struct Engine {
    #[serde(rename = "@power")]
    pub power: f64,
    #[serde(rename = "@consumption")]
    pub consumption: f64,
    #[serde(rename = "@size")]
    pub size: f64,
    #[serde(rename = "@turn")]
    pub turn: f64,
    #[serde(rename = "@fuelType")]
    pub fuel_type: Option<i32>,
    #[serde(rename = "@throttleExponential")]
    pub throttle_exponential: Option<bool>,
}

#[derive(Debug, Serialize, Deserialize, Copy, Clone)]
pub struct Rcs {
    #[serde(rename = "@power")]
    pub power: f64,
    #[serde(rename = "@consumption")]
    pub consumption: f64,
    #[serde(rename = "@size")]
    pub size: f64,
}

#[derive(Debug, Serialize, Deserialize, Copy, Clone)]
pub struct Solar {
    #[serde(rename = "@chargeRate")]
    pub charge_rate: f64,
}

#[derive(Debug, Serialize, Deserialize, Copy, Clone)]
pub struct Lander {
    #[serde(rename = "@maxAngle")]
    pub max_angle: f64,
    #[serde(rename = "@minLength")]
    pub min_length: f64,
    #[serde(rename = "@maxLength")]
    pub max_length: f64,
    #[serde(rename = "@angleSpeed")]
    pub angle_speed: Option<f64>,
    #[serde(rename = "@lengthSpeed")]
    pub length_speed: Option<f64>,
    #[serde(rename = "@width")]
    pub width: f64,
}

#[derive(Debug, Serialize, Deserialize, Clone)]
pub struct RawPartType {
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
    pub r#type: SR1PartTypeEnum,
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
    pub category: Option<String>,
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
            disconnect: 0_f64,
            explode: 0_f64,
            explosion_power: Some(0_f64),
            explosion_size: Some(0_f64),
        });
        let attach_points: Option<Vec<AttachPoint>> =
            self.attach_points.as_ref().map(|attach_points| attach_points.unzip());
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
            damage: damage.take_damage(),
            attach_points,
            attr: part_attr,
        }
    }
    fn to_raw_part_type(&self) -> RawPartType {
        self.clone()
    }
}

impl RawPartList {
    pub fn new(parts: Vec<RawPartType>) -> Self {
        RawPartList { part_types: parts }
    }

    pub fn from_file(file_name: String) -> Option<RawPartList> {
        let part_list_file = fs::read_to_string(file_name).unwrap();
        let part_list: RawPartList = from_str(part_list_file.as_str()).unwrap();
        Some(part_list)
    }

    pub fn list_print(&self) {
        for part_data in self.part_types.iter() {
            println!("{:?}\n", part_data);
        }
    }
}

impl SR1PartListTrait for RawPartList {
    fn to_sr_part_list(&self, name: Option<String>) -> SR1PartList {
        let mut types: Vec<SR1PartType> = Vec::new();
        for part_data in self.part_types.iter() {
            types.push(part_data.to_sr_part_type());
        }
        SR1PartList::part_types_new(types, name)
    }

    fn to_raw_part_list(&self) -> RawPartList {
        self.clone()
    }
}

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
