pub mod part_list;
/// 所有的 Python 相关交互都应该在这里
pub mod py;
pub mod ship;

pub type IdType = i64;

use crate::dr_physics::math::{Edge, Shape};
use crate::dr_physics::math::{Point2D, Rotate};
use crate::sr1_parse::part_list::Damage as RawDamage;
use crate::sr1_parse::part_list::{AttachPoint, AttachPoints, Engine, Lander, Rcs, Shape as RawShape, Solar, Tank};
use crate::sr1_parse::part_list::{FuelType, RawPartList, RawPartType, SR1PartTypeEnum};
use crate::sr1_parse::ship::{
    Activate as RawActivate, Connection, Engine as RawEngine, Part as RawPartData, Pod as RawPod, RawShip,
    Staging as RawStaging, Step as RawStep, Tank as RawTank,
};
use crate::sr1_parse::ship::{Connections as RawConnections, DisconnectedParts, Parts as RawParts};

use std::cell::{Cell, RefCell};
use std::collections::HashMap;
use std::io::Cursor;
use std::ops::Deref;

use quick_xml::events::{BytesEnd, BytesStart, Event};
use quick_xml::writer::Writer;

pub type PartsWithConnections = Vec<(Vec<SR1PartData>, Vec<Connection>)>;

pub fn radians_map_to_degrees(angle: f64) -> f64 {
    let angle_string = angle.to_string();

    match angle_string.deref() {
        "1.570796" => 270.0,
        "3.141593" => 180.0,
        "4.712389" => 90.0,
        _ => angle.to_degrees(),
    }
}

#[derive(Debug, Copy, Clone)]
pub enum SR1PartTypeAttr {
    Tank {
        fuel: f64,
        dry_mass: f64,
        fuel_type: FuelType,
    },
    Engine {
        power: f64,
        consumption: f64,
        size: f64,
        turn: f64,
        // 我觉得用枚举体表示燃料种类更好。
        /// 0 -> 普通燃料
        /// 1 -> Rcs
        /// 2 -> 电量
        /// 3 -> 固推
        fuel_type: FuelType,
        throttle_exponential: bool,
    },
    Rcs {
        power: f64,
        consumption: f64,
        size: f64,
    },
    Solar {
        charge_rate: f64,
    },
    Lander {
        max_angle: f64,
        min_length: f64,
        max_length: f64,
        angle_speed: f64,
        length_speed: f64,
        width: f64,
    },
}

#[derive(Debug, Copy, Clone)]
pub struct Damage {
    /// 导致断裂的受力大小
    pub disconnect: f64,
    /// 导致爆炸的受力大小
    pub explode: f64,
    /// 爆炸威力（虽然在 sr1 里不是 0 就没用）
    pub explosion_power: f64,
    /// 爆炸影响范围（虽然在 sr1 里不是 0 就没用）
    pub explosion_size: f64,
}

impl Damage {
    pub fn as_raw_damage(&self) -> RawDamage {
        RawDamage {
            disconnect: self.disconnect,
            explode: self.explode,
            explosion_power: Some(self.explosion_power),
            explosion_size: Some(self.explosion_size),
        }
    }
}

#[derive(Debug, Clone)]
pub struct SR1PartType {
    /// 部件 ID
    pub id: String,
    /// 部件名称
    pub name: String,
    /// 部件描述
    pub description: String,
    /// 部件材质
    pub sprite: String,
    /// 部件类型
    pub p_type: SR1PartTypeEnum,
    /// 部件质量
    pub mass: f64,
    /// 部件宽度
    pub width: u32,
    /// 部件高度
    pub height: u32,
    /// 摩擦力
    pub friction: f64,
    /// 部件类别 (原版仅有 "Satellite" 可自定义)
    pub category: String,
    /// 是否忽略编辑器碰撞
    pub ignore_editor_intersections: bool,
    /// 是否禁用编辑器旋转
    pub disable_editor_rotation: bool,
    /// 是否可爆炸
    pub can_explode: bool,
    /// 覆盖高度 (原版仅在固态推进器使用)
    pub cover_height: u32,
    /// 是否只在沙盒模式显示
    pub sandbox_only: bool,
    /// 阻力
    pub drag: f64,
    /// 是否隐藏
    pub hidden: bool,
    /// 浮力
    pub buoyancy: f64,
    // 综合属性
    /// 部件受损相关属性
    pub damage: Damage,
    /// 部件碰撞箱
    pub shape: Option<Vec<RawShape>>,
    /// 部件连接点
    pub attach_points: Option<Vec<AttachPoint>>,
    /// 部件特殊属性
    pub attr: Option<SR1PartTypeAttr>,
}

impl SR1PartType {
    pub fn get_box(&self) -> ((f64, f64), (f64, f64)) {
        // -x, -y, x, y
        // 居中
        (
            (-(self.width as f64 / 2.0), -(self.height as f64 / 2.0)),
            (self.width as f64 / 2.0, self.height as f64 / 2.0),
        )
    }
}

#[derive(Debug, Clone)]
pub struct SR1PartList {
    pub types: Vec<SR1PartType>,
    pub cache: RefCell<Option<HashMap<String, SR1PartType>>>,
    pub name: String,
}

impl SR1PartList {
    pub fn new(name: String, types: Vec<SR1PartType>) -> SR1PartList {
        SR1PartList {
            types,
            cache: RefCell::new(None),
            name,
        }
    }

    pub fn from_file(file_name: String) -> Option<SR1PartList> {
        if let Ok(raw_list) = RawPartList::from_file(file_name) {
            let sr_list = raw_list.to_sr_part_list(None);
            return Some(sr_list);
        }
        None
    }

    pub fn get_cache(&self) -> HashMap<String, SR1PartType> {
        if self.cache.borrow().is_none() {
            let mut map = HashMap::new();
            for part in self.types.iter() {
                map.insert(part.id.clone(), part.clone());
            }
            let cache = Some(map.clone());
            self.cache.replace(cache);
        }
        self.cache.borrow().clone().unwrap()
    }

    pub fn get_part_type(&self, type_name: &String) -> Option<SR1PartType> {
        let cache = self.get_cache();
        cache.get(type_name).cloned()
    }

    pub fn part_types_new(part_types: Vec<SR1PartType>, name: Option<String>) -> Self {
        SR1PartList::new(name.unwrap_or("NewPartList".to_string()), part_types)
    }

    pub fn insert_part(&mut self, part: SR1PartType) {
        self.types.insert(0, part);
    }
}

pub trait SR1PartTypeData {
    fn to_sr_part_type(&self) -> SR1PartType;
    fn to_raw_part_type(&self) -> RawPartType;
}

pub trait SR1PartDataTrait {
    fn to_sr_part_data(&self) -> SR1PartData;
    fn to_raw_part_data(&self) -> RawPartData;
}

pub trait SR1PartListTrait {
    fn to_sr_part_list(&self, name: Option<String>) -> SR1PartList;
    #[allow(unused)]
    fn to_raw_part_list(&self) -> RawPartList;
}

pub trait SR1ShipTrait {
    fn to_sr_ship(&self, name: Option<String>) -> SR1Ship;
    #[allow(unused)]
    fn to_raw_ship(&self) -> RawShip;
}

impl SR1PartListTrait for SR1PartList {
    fn to_sr_part_list(&self, name: Option<String>) -> SR1PartList {
        if let Some(name) = name {
            let mut dupe = self.clone();
            dupe.name = name;
            dupe
        } else {
            self.clone()
        }
    }

    fn to_raw_part_list(&self) -> RawPartList {
        let mut types: Vec<RawPartType> = Vec::new();
        for part_type in self.types.iter() {
            types.insert(0, part_type.to_raw_part_type());
        }
        RawPartList::new(types)
    }
}

impl SR1PartTypeData for SR1PartType {
    fn to_sr_part_type(&self) -> SR1PartType {
        self.clone()
    }

    fn to_raw_part_type(&self) -> RawPartType {
        let tank: Option<Tank> = match &self.attr {
            Some(attr) => match attr.to_owned() {
                SR1PartTypeAttr::Tank {
                    fuel,
                    dry_mass,
                    fuel_type,
                } => Some(Tank {
                    fuel,
                    dry_mass,
                    fuel_type: Some(fuel_type),
                }),
                _ => None,
            },
            _ => None,
        };
        let engine: Option<Engine> = match &self.attr {
            Some(attr) => match attr.to_owned() {
                SR1PartTypeAttr::Engine {
                    power,
                    consumption,
                    size,
                    turn,
                    fuel_type,
                    throttle_exponential,
                } => Some(Engine {
                    power,
                    consumption,
                    throttle_exponential: Some(throttle_exponential),
                    size,
                    turn,
                    fuel_type: Some(fuel_type),
                }),
                _ => None,
            },
            _ => None,
        };
        let rcs: Option<Rcs> = match &self.attr {
            Some(attr) => match attr.to_owned() {
                SR1PartTypeAttr::Rcs {
                    power,
                    consumption,
                    size,
                } => Some(Rcs {
                    power,
                    consumption,
                    size,
                }),
                _ => None,
            },
            _ => None,
        };
        let solar: Option<Solar> = match &self.attr {
            Some(attr) => match attr.to_owned() {
                SR1PartTypeAttr::Solar { charge_rate } => Some(Solar { charge_rate }),
                _ => None,
            },
            _ => None,
        };
        let lander: Option<Lander> = match &self.attr {
            Some(attr) => match attr.to_owned() {
                SR1PartTypeAttr::Lander {
                    max_angle,
                    min_length,
                    max_length,
                    angle_speed,
                    length_speed,
                    width,
                } => Some(Lander {
                    max_angle,
                    min_length,
                    max_length,
                    angle_speed: Some(angle_speed),
                    length_speed: Some(length_speed),
                    width,
                }),
                _ => None,
            },
            _ => None,
        };
        let attach_point: Option<AttachPoints> = match &self.attach_points {
            Some(attach_points) => {
                if !attach_points.is_empty() {
                    Some(AttachPoints::new(attach_points.clone()))
                } else {
                    None
                }
            }
            _ => None,
        };
        RawPartType {
            id: self.id.clone(),
            name: self.name.clone(),
            description: self.description.clone(),
            sprite: self.sprite.clone(),
            r#type: self.p_type,
            mass: self.mass,
            width: self.width,
            height: self.height,
            friction: Some(self.friction),
            category: Some(self.category.clone()),
            ignore_editor_intersections: Some(self.ignore_editor_intersections),
            disable_editor_rotation: Some(self.disable_editor_rotation),
            can_explode: Some(self.can_explode),
            cover_height: Some(self.cover_height),
            sandbox_only: Some(self.sandbox_only),
            drag: Some(self.drag),
            hidden: Some(self.hidden),
            buoyancy: Some(self.buoyancy),
            damage: Some(self.damage.as_raw_damage()),
            tank,
            engine,
            rcs,
            solar,
            shape: self.shape.clone(),
            attach_points: attach_point,
            lander,
        }
    }
}

impl SR1PartDataTrait for SR1PartData {
    fn to_sr_part_data(&self) -> SR1PartData {
        self.clone()
    }

    fn to_raw_part_data(&self) -> RawPartData {
        let (tank, engine) = if let Some(fuel) = &self.attr.fuel {
            match self.part_type {
                SR1PartTypeEnum::tank => (Some(RawTank { fuel: fuel.to_owned() }), None),
                SR1PartTypeEnum::engine => (None, Some(RawEngine { fuel: fuel.to_owned() })),
                _ => (None, None),
            }
        } else {
            (None, None)
        };
        let pod = match (&self.attr.name, &self.attr.throttle, &self.attr.current_stage, &self.attr.steps) {
            (Some(name), Some(throttle), Some(current_stage), Some(steps)) => Some({
                let mut actives = Vec::new();
                for step in steps {
                    let mut steps = Vec::new();
                    for active in step {
                        steps.push(RawActivate {
                            id: active.0.to_owned(),
                            moved: active.1.to_owned() as i8,
                        });
                    }
                    actives.push(RawStep { activates: steps });
                }
                let stages = RawStaging {
                    current_stage: current_stage.to_owned(),
                    steps: actives,
                };
                RawPod {
                    name: name.clone(),
                    throttle: throttle.to_owned(),
                    stages,
                }
            }),
            _ => None,
        };
        RawPartData {
            tank,
            engine,
            pod,
            part_type_id: self.part_type_id.clone(),
            id: self.id,
            x: self.x,
            y: self.y,
            editor_angle: Some(self.editor_angle),
            angle: self.angle,
            angle_v: self.angle_v,
            flip_x: Some(self.flip_x as i8),
            flip_y: Some(self.flip_y as i8),
            chute_x: self.attr.chute_x,
            chute_y: self.attr.chute_y,
            chute_height: self.attr.chute_height,
            extension: self.attr.extension,
            inflate: self.attr.inflate.map(|b| b as i8),
            inflation: self.attr.inflation,
            exploded: Some(self.explode as i8),
            rope: self.attr.rope.map(|b| b as i8),
            chute_angle: self.attr.chute_angle,
            activated: Some(self.active as i8),
            deployed: self.attr.deployed.map(|b| b as i8),
        }
    }
}

#[derive(Debug, Clone)]
pub struct SR1PartData {
    /// 单独的属性
    pub attr: SR1PartDataAttr,
    // 基本状态属性
    /// x 坐标
    pub x: f64,
    /// y 坐标
    pub y: f64,
    /// 零件 id
    pub id: IdType,
    /// 旋转角度 弧度
    pub angle: f64,
    /// 旋转角速度 弧度/秒
    pub angle_v: f64,
    // 状态属性
    /// 零件类型
    pub part_type: SR1PartTypeEnum,
    /// 零件类型 id
    pub part_type_id: String,
    /// 零件被顺时针转了几个90度，影响连接点的位置，不影响碰撞箱
    /// 在游戏里计算飞船朝向也会参考
    pub editor_angle: i32,
    /// 是否水平翻转
    pub flip_x: bool,
    /// 是否垂直翻转
    pub flip_y: bool,
    /// 是否启用
    pub active: bool,
    /// 是否爆炸
    pub explode: bool,
}

impl SR1PartData {
    pub fn get_box(&self, part_type: &SR1PartType) -> (f64, f64, f64, f64) {
        let width = part_type.width;
        let height = part_type.height;
        let radius = self.angle;
        let mut shape = Shape::new_width_height(width as f64, height as f64, Some(radius));
        shape.move_xy(Some(self.x), Some(self.y));
        let mut pos_box = (0_f64, 0_f64, 0_f64, 0_f64);
        if let Edge::OneTimeLine(line) = shape.bounds[0] {
            pos_box.0 = line.start.x;
            pos_box.1 = line.start.y;
        }
        if let Edge::OneTimeLine(line) = shape.bounds[2] {
            pos_box.2 = line.start.x;
            pos_box.3 = line.start.y;
        }
        pos_box
    }

    pub fn angle_degrees(&self) -> f64 {
        radians_map_to_degrees(self.angle)
    }
}

#[derive(Debug, Clone)]
pub struct SR1PartDataAttr {
    // Tank | Engine
    pub fuel: Option<f64>,
    // Pod
    pub name: Option<String>,
    pub throttle: Option<f64>,
    pub current_stage: Option<i32>,
    pub steps: Option<Vec<Vec<(IdType, bool)>>>,
    // Solar
    pub extension: Option<f64>,
    // Parachute
    pub chute_x: Option<f64>,
    pub chute_y: Option<f64>,
    pub chute_height: Option<f64>,
    pub chute_angle: Option<f64>,
    pub inflate: Option<bool>,
    pub inflation: Option<f64>,
    pub deployed: Option<bool>,
    pub rope: Option<bool>,
    // part_type
    pub part_type: Cell<Option<SR1PartTypeEnum>>,
}

impl SR1PartDataAttr {
    pub fn guess_type(&self) -> SR1PartTypeEnum {
        if let Some(part_type) = self.part_type.get() {
            return part_type;
        }
        if self.fuel.is_some() {
            self.part_type.set(Some(SR1PartTypeEnum::tank));
            return self.part_type.get().unwrap();
        }
        if self.name.is_some() {
            self.part_type.set(Some(SR1PartTypeEnum::pod));
            return self.part_type.get().unwrap();
        }
        if self.extension.is_some() {
            self.part_type.set(Some(SR1PartTypeEnum::solar));
            return self.part_type.get().unwrap();
        }
        if self.chute_x.is_some() {
            self.part_type.set(Some(SR1PartTypeEnum::parachute));
            return self.part_type.get().unwrap();
        }
        SR1PartTypeEnum::strut // 默认为 Strut    开摆
    }

    pub fn get_part_type(&self) -> SR1PartTypeEnum {
        if let Some(part_type) = self.part_type.get() {
            return part_type;
        }
        self.guess_type()
    }
    #[allow(clippy::too_many_arguments)]
    pub fn new(
        fuel: Option<f64>,
        name: Option<String>,
        throttle: Option<f64>,
        current_stage: Option<i32>,
        steps: Option<Vec<Vec<(IdType, bool)>>>,
        extension: Option<f64>,
        chute_pos: (Option<f64>, Option<f64>),
        chute_height: Option<f64>,
        chute_angle: Option<f64>,
        inflate: Option<bool>,
        inflation: Option<f64>,
        deployed: Option<bool>,
        rope: Option<bool>,
        part_type: Option<SR1PartTypeEnum>,
    ) -> Self {
        SR1PartDataAttr {
            fuel,
            name,
            throttle,
            current_stage,
            steps,
            extension,
            chute_x: chute_pos.0,
            chute_y: chute_pos.1,
            chute_height,
            chute_angle,
            inflate,
            inflation,
            deployed,
            rope,
            part_type: Cell::new(part_type),
        }
    }

    pub fn from_raw(raw_data: &RawPartData, part_type: Option<SR1PartTypeEnum>, guess: bool) -> Self {
        let fuel = if let Some(tank) = &raw_data.tank {
            Some(tank.fuel.to_owned())
        } else {
            raw_data.engine.as_ref().map(|engine| engine.fuel.to_owned())
        };
        let (name, throttle, current_stage, steps) = if let Some(pod) = &raw_data.pod {
            (
                Some(pod.name.clone()),
                Some(pod.throttle),
                Some(pod.stages.current_stage),
                Some({
                    pod.stages
                        .steps
                        .iter()
                        .map(|step| step.activates.iter().map(|act| (act.id, act.moved != 0)).collect())
                        .collect()
                }),
            )
        } else {
            (None, None, None, None)
        };
        let results = SR1PartDataAttr {
            fuel,
            name,
            throttle,
            current_stage,
            steps,
            extension: raw_data.extension,
            chute_x: raw_data.chute_x,
            chute_y: raw_data.chute_y,
            chute_height: raw_data.chute_height,
            chute_angle: raw_data.chute_angle,
            inflate: raw_data.inflate.map(|i| i != 0),
            inflation: raw_data.inflation,
            deployed: raw_data.deployed.map(|i| i != 0),
            rope: raw_data.rope.map(|i| i != 0),
            part_type: Cell::new(part_type),
        };

        if guess & results.part_type.get().is_none() {
            results.guess_type();
        }
        results
    }
}

#[derive(Debug, Clone)]
pub struct SR1Ship {
    pub name: String,
    pub description: String,
    pub version: i32,
    pub lift_off: bool,
    pub touch_ground: bool,
    pub parts: Vec<SR1PartData>,
    pub connections: Vec<Connection>,
    pub disconnected: Vec<(Vec<SR1PartData>, Vec<Connection>)>,
}

#[derive(Debug, Clone, Copy)]
pub struct SaveStatus {
    pub save_default: bool,
}

impl SaveStatus {
    pub fn new(save_default: bool) -> Self {
        SaveStatus { save_default }
    }
}

impl SR1Ship {
    pub fn from_file(file_name: String, ship_name: Option<String>) -> Option<Self> {
        // 首先验证文件是否存在 不存在则返回None
        if !std::path::Path::new(&file_name).exists() {
            return None;
        }
        // 解析为 RawShip
        let ship = RawShip::from_file(file_name);
        match ship {
            Some(ship) => {
                // 解析为 SR1Ship
                let sr_ship = ship.to_sr_ship(ship_name);
                Some(sr_ship)
            }
            None => None,
        }
    }

    pub fn parse_part_list_to_part(&mut self, part_list: &SR1PartList) {
        // parse parts
        for part in self.parts.iter_mut() {
            if let Some(part_type) = part_list.get_part_type(&part.part_type_id) {
                part.part_type = part_type.p_type;
            } else {
                part.part_type = SR1PartTypeEnum::strut;
            }
        }
        self.disconnected.iter_mut().for_each(|(disconnected_parts, _)| {
            disconnected_parts.iter_mut().for_each(|part| match part_list.get_part_type(&part.part_type_id) {
                Some(part_type) => part.part_type = part_type.p_type,
                None => part.part_type = SR1PartTypeEnum::strut,
            });
        })
        // for disconnects in self.disconnected.iter_mut() {
        //     for (parts, _) in disconnects.iter_mut() {
        //         for part in parts.iter_mut() {
        //             if let Some(part_type) = part_list.get_part_type(&part.part_type_id) {
        //                 part.part_type = part_type.p_type;
        //             } else {
        //                 part.part_type = SR1PartTypeEnum::strut;
        //             }
        //         }
        //     }
        // }
    }

    pub fn part_as_hashmap(&self) -> HashMap<IdType, Vec<SR1PartData>> {
        // 返回一个 HashMap 用于快速查找
        // 同时为了 防止出现多个相同的 PartID 造成的数据丢失
        // 采用 Vec 存储
        let mut result: HashMap<IdType, Vec<SR1PartData>> = HashMap::new();
        for part_data in self.parts.iter() {
            if let Some(part_vec) = result.get_mut(&part_data.id) {
                part_vec.push(part_data.clone());
            } else {
                result.insert(part_data.id, vec![part_data.clone()]);
            }
        }
        result
    }

    pub fn save(&self, file_name: String, save_status: &SaveStatus) -> Option<()> {
        macro_rules! option_push_attr {
            ($elem: ident, $test_block: expr, $push: expr) => {
                if ($test_block) {
                    $elem.push_attribute($push);
                }
            };
        }

        fn write_parts(parts: &[SR1PartData], writer: &mut Writer<Cursor<Vec<u8>>>, save_status: &SaveStatus) {
            writer.write_event(Event::Start(BytesStart::new("Parts"))).unwrap();
            for part in parts.iter() {
                let mut part_attr = BytesStart::new("Part");
                part_attr.push_attribute(("type", part.part_type_id.as_str()));
                part_attr.push_attribute(("x", part.x.to_string().as_str()));
                part_attr.push_attribute(("y", part.y.to_string().as_str()));
                part_attr.push_attribute(("id", part.id.to_string().as_str()));
                part_attr.push_attribute(("editorAngle", part.editor_angle.to_string().as_str()));
                part_attr.push_attribute(("angle", part.angle.to_string().as_str()));
                part_attr.push_attribute(("angleV", part.angle_v.to_string().as_str()));
                option_push_attr!(
                    part_attr,
                    part.flip_x && !save_status.save_default,
                    ("flippedX", (part.flip_x as i8).to_string().as_str())
                );
                option_push_attr!(
                    part_attr,
                    part.flip_y && !save_status.save_default,
                    ("flippedY", (part.flip_y as i8).to_string().as_str())
                );
                option_push_attr!(
                    part_attr,
                    part.active && !save_status.save_default,
                    ("activated", (part.active as i8).to_string().as_str())
                );
                let inner_attr: Option<BytesStart> = match part.part_type {
                    SR1PartTypeEnum::tank | SR1PartTypeEnum::engine => {
                        let mut tank_attr = BytesStart::new({
                            if part.part_type == SR1PartTypeEnum::tank {
                                "Tank"
                            } else {
                                "Engine"
                            }
                        });
                        tank_attr.push_attribute(("fuel", part.attr.fuel.unwrap().to_string().as_str()));
                        Some(tank_attr)
                    }
                    SR1PartTypeEnum::pod => {
                        writer.write_event(Event::Start(part_attr.to_owned())).unwrap();
                        // pod tag
                        let mut pod_elem = BytesStart::new("Pod");
                        pod_elem.push_attribute(("throttle", part.attr.throttle.unwrap().to_string().as_str()));
                        pod_elem.push_attribute(("name", part.attr.name.as_ref().unwrap().as_str()));
                        writer.write_event(Event::Start(pod_elem.to_owned())).unwrap();

                        let mut stage_attr = BytesStart::new("Staging");
                        stage_attr
                            .push_attribute(("currentStage", part.attr.current_stage.unwrap().to_string().as_str()));
                        match &part.attr.steps {
                            Some(steps) => {
                                writer.write_event(Event::Start(stage_attr)).unwrap();
                                for step in steps.iter() {
                                    writer.write_event(Event::Start(BytesStart::new("Step"))).unwrap();
                                    for activate in step.iter() {
                                        let mut activate_attr = BytesStart::new("Activate");
                                        activate_attr.push_attribute(("Id", activate.0.to_string().as_str()));
                                        activate_attr
                                            .push_attribute(("moved", (activate.1 as i8).to_string().as_str()));
                                        writer.write_event(Event::Empty(activate_attr)).unwrap();
                                    }
                                    writer.write_event(Event::End(BytesEnd::new("Step"))).unwrap();
                                }
                                writer.write_event(Event::End(BytesEnd::new("Staging"))).unwrap();
                            }
                            None => {
                                writer.write_event(Event::Empty(stage_attr)).unwrap();
                            }
                        }
                        writer.write_event(Event::End(BytesEnd::new("Pod"))).unwrap();
                        writer.write_event(Event::End(BytesEnd::new("Part"))).unwrap();
                        Some(pod_elem)
                    }
                    SR1PartTypeEnum::solar => {
                        part_attr.push_attribute(("extension", part.attr.extension.unwrap().to_string().as_str()));
                        None
                    }
                    SR1PartTypeEnum::parachute => {
                        part_attr.push_attribute(("chuteX", part.attr.chute_x.unwrap().to_string().as_str()));
                        part_attr.push_attribute(("chuteY", part.attr.chute_y.unwrap().to_string().as_str()));
                        part_attr.push_attribute(("chuteHeight", part.attr.chute_height.unwrap().to_string().as_str()));
                        part_attr.push_attribute(("chuteAngle", part.attr.chute_angle.unwrap().to_string().as_str()));
                        part_attr.push_attribute(("inflate", (part.attr.inflate.unwrap() as i8).to_string().as_str()));
                        part_attr.push_attribute(("inflation", part.attr.inflation.unwrap().to_string().as_str()));
                        part_attr
                            .push_attribute(("deployed", (part.attr.deployed.unwrap() as i8).to_string().as_str()));
                        part_attr.push_attribute(("rope", (part.attr.rope.unwrap() as i8).to_string().as_str()));
                        None
                    }
                    _ => None,
                };
                match inner_attr {
                    Some(inner_attr) => match part.part_type {
                        SR1PartTypeEnum::pod => {}
                        _ => {
                            writer.write_event(Event::Start(part_attr)).unwrap();
                            writer.write_event(Event::Empty(inner_attr)).unwrap();
                            writer.write_event(Event::End(BytesEnd::new("Part"))).unwrap();
                        }
                    },
                    None => {
                        writer.write_event(Event::Empty(part_attr)).unwrap();
                    }
                }
            }
            writer.write_event(Event::End(BytesEnd::new("Parts"))).unwrap();
        }

        fn write_connections(connects: &[Connection], writer: &mut Writer<Cursor<Vec<u8>>>) {
            writer.write_event(Event::Start(BytesStart::new("Connections"))).unwrap();
            for connect in connects.iter() {
                match connect {
                    Connection::Dock {
                        dock_part,
                        parent_part,
                        child_part,
                    } => {
                        let mut dock_elem = BytesStart::new("DockConnection");
                        dock_elem.push_attribute(("dockPart", dock_part.to_string().as_str()));
                        dock_elem.push_attribute(("parentPart", parent_part.to_string().as_str()));
                        dock_elem.push_attribute(("childPart", child_part.to_string().as_str()));
                        writer.write_event(Event::Empty(dock_elem)).unwrap();
                    }
                    Connection::Normal {
                        parent_attach_point,
                        child_attach_point,
                        parent_part,
                        child_part,
                    } => {
                        let mut connect_elem = BytesStart::new("Connection");
                        connect_elem.push_attribute(("parentAttachPoint", parent_attach_point.to_string().as_str()));
                        connect_elem.push_attribute(("childAttachPoint", child_attach_point.to_string().as_str()));
                        connect_elem.push_attribute(("parentPart", parent_part.to_string().as_str()));
                        connect_elem.push_attribute(("childPart", child_part.to_string().as_str()));
                        writer.write_event(Event::Empty(connect_elem)).unwrap();
                    }
                }
            }
            writer.write_event(Event::End(BytesEnd::new("Connections"))).unwrap();
        }

        fn write_disconnect(
            data: &PartsWithConnections,
            writer: &mut Writer<Cursor<Vec<u8>>>,
            save_status: &SaveStatus,
        ) {
            writer.write_event(Event::Start(BytesStart::new("DisconnectedParts"))).unwrap();
            for (parts, connects) in data.iter() {
                writer.write_event(Event::Start(BytesStart::new("DisconnectedPart"))).unwrap();
                write_parts(parts, writer, save_status);
                write_connections(connects, writer);
                writer.write_event(Event::End(BytesEnd::new("DisconnectedPart"))).unwrap();
            }
            writer.write_event(Event::End(BytesEnd::new("DisconnectedParts"))).unwrap();
        }

        fn write_data(data: &SR1Ship, save_status: &SaveStatus) -> String {
            let mut writer: Writer<Cursor<Vec<u8>>> = Writer::new(Cursor::new(Vec::new()));
            {
                // ship attr
                let mut ship_elem = BytesStart::new("Ship");
                ship_elem.push_attribute(("version", data.version.to_string().as_str()));
                ship_elem.push_attribute(("liftedOff", (data.lift_off as i8).to_string().as_str()));
                ship_elem.push_attribute(("touchingGround", (data.touch_ground as i8).to_string().as_str()));
                writer.write_event(Event::Start(ship_elem)).unwrap();
            }
            write_parts(&data.parts, &mut writer, save_status);
            write_connections(&data.connections, &mut writer);
            write_disconnect(&data.disconnected, &mut writer, save_status);
            writer.write_event(Event::End(BytesEnd::new("Ship"))).unwrap();

            String::from_utf8(writer.into_inner().into_inner()).unwrap()
        }
        std::fs::write(file_name, write_data(self, save_status)).unwrap();
        Some(())
    }
}

impl SR1ShipTrait for SR1Ship {
    #[inline]
    fn to_sr_ship(&self, name: Option<String>) -> SR1Ship {
        if let Some(name) = name {
            let mut dupe = self.clone();
            dupe.name = name;
            dupe
        } else {
            self.clone()
        }
    }

    #[inline]
    fn to_raw_ship(&self) -> RawShip {
        RawShip {
            parts: RawParts::from_vec_sr1(self.parts.clone()),
            connects: RawConnections::from_vec(self.connections.clone()),
            version: Some(self.version),
            lift_off: self.lift_off as i8,
            touch_ground: Some(self.touch_ground as i8),
            disconnected: DisconnectedParts::from_vec_sr1(self.disconnected.clone()),
        }
    }
}

pub fn get_max_box(parts: &[SR1PartData], part_list: &SR1PartList) -> (f64, f64, f64, f64) {
    let mut max_box = (0_f64, 0_f64, 0_f64, 0_f64);
    for part in parts.iter() {
        let part_type = part_list.get_part_type(&part.part_type_id).unwrap();
        let ((x1, y1), (x2, y2)) = part_type.get_box();
        // rotate
        let mut p1 = Point2D::new(x1, y1);
        let mut p2 = Point2D::new(x2, y2);
        p1.rotate_radius_mut(part.angle);
        p2.rotate_radius_mut(part.angle);
        // let p1 = p1.add(part.x * 2.0, part.y * 2.0);
        // let p2 = p2.add(part.x * 2.0, part.y * 2.0);
        let p1 = p1
            + Point2D {
                x: part.x * 2.0,
                y: part.y * 2.0,
            };
        let p2 = p2
            + Point2D {
                x: part.x * 2.0,
                y: part.y * 2.0,
            };
        let (x1, y1, x2, y2) = (p1.x, p1.y, p2.x, p2.y);
        // get max box
        max_box.0 = max_box.0.min(x1).min(part.x);
        max_box.1 = max_box.1.min(y1).min(part.y);
        max_box.2 = max_box.2.max(x2).max(part.x);
        max_box.3 = max_box.3.max(y2).max(part.y);
        // * 60 print again
        // println!("{} {} {} {} id:{}", x1 * 60.0, y1 * 60.0, x2 * 60.0, y2 * 60.0, part.id)
    }

    max_box
}
