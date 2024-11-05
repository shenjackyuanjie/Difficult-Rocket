use crate::sr1_parse::IdType;
use crate::sr1_parse::{SR1PartData, SR1PartDataAttr, SR1Ship};
use crate::sr1_parse::{SR1PartDataTrait, SR1ShipTrait};

use quick_xml::de::from_str;
use quick_xml::events::Event;
use quick_xml::reader::Reader;
use quick_xml::se::to_string;
use serde::{Deserialize, Serialize};

/// https://docs.rs/quick-xml/latest/quick_xml/de/index.html#basics
/// using quick xml
#[derive(Debug, Serialize, Deserialize, Clone)]
#[serde(rename = "Ship")]
pub struct RawShip {
    #[serde(rename = "Parts")]
    pub parts: Parts,
    #[serde(rename = "Connections")]
    pub connects: Connections,
    #[serde(rename = "@version")]
    pub version: Option<i32>, // Option for https://github.com/shenjackyuanjie/Difficult-Rocket/issues/48
    // SR1 says version is also optional, let them happy
    // it's always 1
    #[serde(rename = "@liftedOff")]
    pub lift_off: i8,
    #[serde(rename = "@touchingGround")]
    pub touch_ground: Option<i8>, // Option for https://github.com/shenjackyuanjie/Difficult-Rocket/issues/49
    // SR1 says it's optional, let them happy
    // NOT always 0
    #[serde(rename = "DisconnectedParts")]
    pub disconnected: DisconnectedParts,
}

#[derive(Debug, Serialize, Deserialize, Clone)]
pub struct Part {
    #[serde(rename = "Tank")]
    pub tank: Option<Tank>,
    #[serde(rename = "Engine")]
    pub engine: Option<Engine>,
    #[serde(rename = "Pod")]
    pub pod: Option<Pod>,
    #[serde(rename = "@partType")]
    pub part_type_id: String,
    #[serde(rename = "@id")]
    pub id: IdType,
    #[serde(rename = "@x")]
    pub x: f64,
    #[serde(rename = "@y")]
    pub y: f64,
    /// Option for https://github.com/shenjackyuanjie/Difficult-Rocket/issues/47
    /// SR1 says it's optional, let them happy
    #[serde(rename = "@editorAngle")]
    pub editor_angle: Option<i32>,
    #[serde(rename = "@angle")]
    pub angle: f64,
    #[serde(rename = "@angleV")]
    pub angle_v: f64,
    #[serde(rename = "@flippedX")]
    pub flip_x: Option<i8>,
    #[serde(rename = "@flippedY")]
    pub flip_y: Option<i8>,
    // 降落伞
    #[serde(rename = "@chuteX")]
    pub chute_x: Option<f64>,
    #[serde(rename = "@chuteY")]
    pub chute_y: Option<f64>,
    #[serde(rename = "@chuteAngle")]
    pub chute_angle: Option<f64>,
    #[serde(rename = "@chuteHeight")]
    pub chute_height: Option<f64>,
    #[serde(rename = "@extension")]
    pub extension: Option<f64>,
    #[serde(rename = "@inflate")]
    pub inflate: Option<i8>,
    #[serde(rename = "@inflation")]
    pub inflation: Option<f64>,
    #[serde(rename = "@deployed")]
    pub exploded: Option<i8>,
    #[serde(rename = "@rope")]
    pub rope: Option<i8>,
    #[serde(rename = "@activated")]
    pub activated: Option<i8>,
    #[serde(rename = "@deployed")]
    pub deployed: Option<i8>,
}

#[derive(Debug, Serialize, Deserialize, Clone)]
pub struct Parts {
    #[serde(rename = "Part", default)]
    pub parts: Vec<Part>,
}

#[derive(Debug, Serialize, Deserialize, Clone)]
pub struct Connections {
    #[serde(rename = "$value", default)]
    pub connections: Vec<Connection>,
}

#[derive(Debug, Serialize, Deserialize, Clone)]
pub struct DisconnectedParts {
    #[serde(rename = "DisconnectedPart", default)]
    pub parts: Vec<DisconnectedPart>,
}

impl Parts {
    pub fn as_sr1_vec(&self) -> Vec<SR1PartData> {
        self.parts.iter().map(|x| x.to_sr_part_data()).collect()
    }
    pub fn from_vec_sr1(parts: Vec<SR1PartData>) -> Self {
        Parts {
            parts: parts.iter().map(|x| x.to_raw_part_data()).collect(),
        }
    }
}

impl Connections {
    pub fn as_vec(&self) -> Vec<Connection> {
        self.connections.clone()
    }
    pub fn from_vec(connections: Vec<Connection>) -> Self {
        Connections { connections }
    }
}

impl DisconnectedParts {
    pub fn as_sr1_vec(&self) -> Vec<(Vec<SR1PartData>, Vec<Connection>)> {
        self.parts.iter().map(|x| x.as_sr_part()).collect()
    }
    pub fn from_vec_sr1(parts_list: Vec<(Vec<SR1PartData>, Vec<Connection>)>) -> Self {
        DisconnectedParts {
            parts: parts_list
                .iter()
                .map(|(part, connects)| DisconnectedPart::from_sr_part(part.to_vec(), connects.to_vec()))
                .collect(),
        }
    }
}

#[derive(Debug, Serialize, Deserialize, Clone)]
pub struct Engine {
    #[serde(rename = "@fuel")]
    pub fuel: f64,
}

#[derive(Debug, Serialize, Deserialize, Clone)]
pub struct Tank {
    #[serde(rename = "@fuel")]
    pub fuel: f64,
}

#[derive(Debug, Serialize, Deserialize, Clone)]
pub struct Pod {
    #[serde(rename = "Staging")]
    pub stages: Staging,
    #[serde(rename = "@name")]
    pub name: String,
    #[serde(rename = "@throttle")]
    pub throttle: f64,
}

#[derive(Debug, Serialize, Deserialize, Clone)]
pub struct Staging {
    #[serde(rename = "@currentStage")]
    pub current_stage: i32,
    #[serde(rename = "Step", default)]
    pub steps: Vec<Step>,
}

#[derive(Debug, Serialize, Deserialize, Clone)]
pub struct Step {
    /// ~~Option for https://github.com/shenjackyuanjie/Difficult-Rocket/issues/21~~
    /// Now is (default)
    #[serde(rename = "Activate", default)]
    pub activates: Vec<Activate>,
}

#[derive(Debug, Serialize, Deserialize, Clone)]
#[serde(rename = "Activate")]
pub struct Activate {
    #[serde(rename = "@Id")]
    pub id: IdType,
    #[serde(rename = "@moved")]
    pub moved: i8, // 1 or 0
}

#[derive(Debug, Serialize, Deserialize, Clone)]
pub struct DisconnectedPart {
    #[serde(rename = "Parts")]
    pub parts: Parts,
    #[serde(rename = "Connections")]
    pub connects: Connections,
}

impl DisconnectedPart {
    pub fn as_sr_part(&self) -> (Vec<SR1PartData>, Vec<Connection>) {
        (self.parts.as_sr1_vec(), self.connects.as_vec())
    }

    pub fn from_sr_part(parts: Vec<SR1PartData>, connects: Vec<Connection>) -> Self {
        Self {
            parts: Parts::from_vec_sr1(parts),
            connects: Connections::from_vec(connects),
        }
    }
}

pub type RawConnectionData = (i32, i32, IdType, IdType);

#[derive(Debug, Serialize, Deserialize, Clone)]
pub enum Connection {
    #[serde(rename = "Connection")]
    Normal {
        #[serde(rename = "@parentAttachPoint")]
        parent_attach_point: i32,
        #[serde(rename = "@childAttachPoint")]
        child_attach_point: i32,
        #[serde(rename = "@parentPart")]
        parent_part: IdType,
        #[serde(rename = "@childPart")]
        child_part: IdType,
    },
    #[serde(rename = "DockConnection")]
    Dock {
        #[serde(rename = "@dockPart")]
        dock_part: IdType,
        #[serde(rename = "@parentPart")]
        parent_part: IdType,
        #[serde(rename = "@childPart")]
        child_part: IdType,
    },
}

pub type RawDockConnectionData = (IdType, IdType, IdType);

impl Connection {
    pub fn as_normal_raw(&self) -> Option<RawConnectionData> {
        match self {
            Connection::Normal {
                parent_attach_point,
                child_attach_point,
                parent_part,
                child_part,
            } => Some((*parent_attach_point, *child_attach_point, *parent_part, *child_part)),
            _ => None,
        }
    }
    pub fn as_dock_raw(&self) -> Option<RawDockConnectionData> {
        match self {
            Connection::Dock {
                dock_part,
                parent_part,
                child_part,
            } => Some((*dock_part, *parent_part, *child_part)),
            _ => None,
        }
    }
    /// 通用的获取父节点
    pub fn get_parent(&self) -> IdType {
        match self {
            Connection::Normal { parent_part, .. } => *parent_part,
            Connection::Dock { parent_part, .. } => *parent_part,
        }
    }
    /// 通用的获取子节点
    pub fn get_child(&self) -> IdType {
        match self {
            Connection::Normal { child_part, .. } => *child_part,
            Connection::Dock { child_part, .. } => *child_part,
        }
    }
    /// 是否为 Dock 类型
    pub fn is_dock(&self) -> bool {
        matches!(self, Connection::Dock { .. })
    }
    /// 是否为 Normal 类型
    pub fn is_normal(&self) -> bool {
        matches!(self, Connection::Normal { .. })
    }
}

impl SR1PartDataTrait for Part {
    fn to_sr_part_data(&self) -> SR1PartData {
        let attr = SR1PartDataAttr::from_raw(self, None, true);
        let part_type = attr.get_part_type();
        SR1PartData {
            attr,
            x: self.x,
            y: self.y,
            id: self.id,
            angle: self.angle,
            angle_v: self.angle_v,
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
    fn to_sr_ship(&self, name: Option<String>) -> SR1Ship {
        SR1Ship {
            name: name.unwrap_or("NewShip".to_string()),
            description: "".to_string(),
            version: self.version.unwrap_or(1_i32),
            parts: self.parts.as_sr1_vec(),
            connections: self.connects.as_vec(),
            lift_off: self.lift_off != 0,
            touch_ground: self.touch_ground.to_owned().map(|i| i != 0).unwrap_or(true),
            disconnected: self.disconnected.as_sr1_vec(),
        }
    }

    fn to_raw_ship(&self) -> RawShip {
        self.clone()
    }
}

impl RawShip {
    pub fn from_file(path: String) -> Option<RawShip> {
        let ship_file = std::fs::read_to_string(path); // for encoding error
        if let Err(e) = ship_file {
            println!("ERROR while reading file!\n{}\n----------", e);
            return None;
        }
        let ship_file = ship_file.unwrap();
        let ship = from_str(&ship_file);
        match ship {
            Ok(ship) => Some(ship),
            Err(e) => {
                println!("ERROR in serde!\n{}", e);
                None
            }
        }
    }

    #[allow(unused)]
    pub fn save(&self, file_name: String) -> anyhow::Result<()> {
        let part_list_file = to_string(self)?;
        print!("{:?}", part_list_file);
        std::fs::write(file_name, part_list_file)?;
        Ok(())
    }
}
