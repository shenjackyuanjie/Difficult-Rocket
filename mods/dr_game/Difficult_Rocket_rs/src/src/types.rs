/*
 * -------------------------------
 * Difficult Rocket
 * Copyright © 2020-2023 by shenjackyuanjie 3695888@qq.com
 * All rights reserved
 * -------------------------------
 */

pub mod sr1 {
    use std::cell::{Cell, RefCell};
    use std::collections::HashMap;

    use super::math::{Edge, Shape};
    use crate::sr1_data::part_list::Damage as RawDamage;
    use crate::sr1_data::part_list::{AttachPoint, AttachPoints, Engine, Lander, Rcs, Shape as RawShape, Solar, Tank};
    use crate::sr1_data::part_list::{RawPartList, RawPartType, SR1PartTypeEnum};
    use crate::sr1_data::ship::{
        Activate as RawActivate, Connection, Connections, DisconnectedPart as RawDisconnectedPart, DisconnectedParts as RawDisconnectedParts,
        Engine as RawEngine, Part as RawPartData, Parts as RawParts, Pod as RawPod, RawShip, Staging as RawStaging, Step as RawStep, Tank as RawTank,
    };
    use crate::types::math::{Point2D, Rotatable};

    #[allow(unused)]
    #[inline]
    pub fn map_ptype_textures(ptype: String) -> String {
        match ptype.as_str() {
            "pod-1" => "Pod",
            "detacher-1" => "DetacherVertical",
            "detacher-2" => "DetacherRadial",
            "wheel-1" => "Wheel",
            "wheel-2" => "Wheel",
            "fuselage-1" => "Fuselage",
            "strut-1" => "Beam",
            "fueltank-0" => "TankTiny",
            "fueltank-1" => "TankSmall",
            "fueltank-2" => "TankMedium",
            "fueltank-3" => "TankLarge",
            "fueltank-4" => "Puffy750",
            "fueltank-5" => "SideTank",
            "engine-0" => "EngineTiny",
            "engine-1" => "EngineSmall",
            "engine-2" => "EngineMedium",
            "engine-3" => "EngineLarge",
            "engine-4" => "SolidRocketBooster",
            "ion-0" => "EngineIon",
            "parachute-1" => "ParachuteCanister",
            "nosecone-1" => "NoseCone",
            "rcs-1" => "RcsBlock",
            "solar-1" => "SolarPanelBase",
            "battery-0" => "Battery",
            "dock-1" => "DockingConnector",
            "port-1" => "DockingPort",
            "lander-1" => "LanderLegPreview",
            _ => "Pod",
        }
        .to_string()
    }

    #[inline]
    pub fn i8_to_bool(i: i8) -> bool {
        match i {
            0 => false,
            _ => true,
        }
    }

    #[inline]
    pub fn bool_to_i8(b: bool) -> i8 {
        match b {
            false => 0,
            true => 1,
        }
    }

    #[inline]
    pub fn option_i8_to_option_bool(i: Option<i8>) -> Option<bool> {
        match i {
            Some(i) => Some(i8_to_bool(i)),
            None => None,
        }
    }

    #[inline]
    pub fn option_bool_to_option_i8(b: Option<bool>) -> Option<i8> {
        match b {
            Some(b) => Some(bool_to_i8(b)),
            None => None,
        }
    }

    #[derive(Debug, Copy, Clone)]
    pub enum SR1PartTypeAttr {
        Tank {
            fuel: f64,
            dry_mass: f64,
            fuel_type: i32,
        },
        Engine {
            power: f64,
            consumption: f64,
            size: f64,
            turn: f64,
            fuel_type: i32,
            // 0 -> 普通燃料
            // 1 -> Rcs
            // 2 -> 电量
            // 3 -> 固推
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
        pub disconnect: i32,
        // 断裂受力大小
        pub explode: i32,
        // 爆炸受力大小
        pub explosion_power: u32,
        // 爆炸力量
        pub explosion_size: u32,
        // 爆炸大小
    }

    impl Damage {
        pub fn to_raw_damage(&self) -> RawDamage {
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
        pub id: String,
        // 部件 ID
        pub name: String,
        // 部件名称
        pub description: String,
        // 部件描述
        pub sprite: String,
        // 部件材质
        pub p_type: SR1PartTypeEnum,
        // 部件类型
        pub mass: f64,
        // 部件质量
        pub width: u32,
        // 部件宽度
        pub height: u32,
        // 部件高度
        pub friction: f64,
        // 摩擦力
        pub category: String,
        // 部件类别 (原版仅有 "Satellite" 可自定义)
        pub ignore_editor_intersections: bool,
        // 是否忽略编辑器碰撞
        pub disable_editor_rotation: bool,
        // 是否禁用编辑器旋转
        pub can_explode: bool,
        // 是否可爆炸
        pub cover_height: u32,
        // 覆盖高度 (原版仅在固态推进器使用)
        pub sandbox_only: bool,
        // 是否只在沙盒模式显示
        pub drag: f64,
        // 阻力
        pub hidden: bool,
        // 是否隐藏
        pub buoyancy: f64,
        // 浮力
        // 综合属性
        pub damage: Damage,
        // 部件受损相关属性
        pub shape: Option<Vec<RawShape>>,
        // 部件碰撞箱
        pub attach_points: Option<Vec<AttachPoint>>,
        // 部件连接点
        pub attr: Option<SR1PartTypeAttr>, // 部件特殊属性
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
        #[inline]
        pub fn new(name: String, types: Vec<SR1PartType>) -> SR1PartList {
            SR1PartList {
                types,
                cache: RefCell::new(None),
                name,
            }
        }

        #[inline]
        pub fn from_file(file_name: String) -> Option<SR1PartList> {
            if let Some(raw_list) = RawPartList::from_file(file_name) {
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
                self.cache.replace(cache.clone());
            }
            self.cache.borrow().clone().unwrap()
        }

        #[inline]
        pub fn get_part_type(&self, type_name: String) -> Option<SR1PartType> {
            let cache = self.get_cache();
            match cache.get(&type_name) {
                Some(part) => Some(part.clone()),
                None => None,
            }
        }

        pub fn part_types_new(part_types: Vec<SR1PartType>, name: Option<String>) -> Self {
            SR1PartList::new(name.unwrap_or("NewPartList".to_string()), part_types)
        }

        pub fn insert_part(&mut self, part: SR1PartType) -> () { self.types.insert(0, part); }
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
        fn to_raw_part_list(&self) -> RawPartList;
    }

    pub trait SR1ShipTrait {
        fn to_sr_ship(&self, name: Option<String>) -> SR1Ship;
        fn to_raw_ship(&self) -> RawShip;
    }

    impl SR1PartListTrait for SR1PartList {
        fn to_sr_part_list(&self, name: Option<String>) -> SR1PartList {
            return if let Some(name) = name {
                let mut dupe = self.clone();
                dupe.name = name;
                dupe
            } else {
                self.clone()
            };
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
        fn to_sr_part_type(&self) -> SR1PartType { self.clone() }

        fn to_raw_part_type(&self) -> RawPartType {
            let tank: Option<Tank> = match &self.attr {
                Some(attr) => match attr.to_owned() {
                    SR1PartTypeAttr::Tank { fuel, dry_mass, fuel_type } => Some(Tank {
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
                    SR1PartTypeAttr::Rcs { power, consumption, size } => Some(Rcs { power, consumption, size }),
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
                    if attach_points.len() > 0 {
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
                r#type: self.p_type.clone(),
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
                damage: Some(self.damage.to_raw_damage()),
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
        #[inline]
        fn to_sr_part_data(&self) -> SR1PartData { self.clone() }

        #[inline]
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
                        let mut steps_ = Vec::new();
                        for active in step {
                            steps_.push(RawActivate {
                                id: active.0.to_owned(),
                                moved: bool_to_i8(active.1.to_owned()),
                            });
                        }
                        actives.push(RawStep { activates: Some(steps_) });
                    }
                    let stages = RawStaging {
                        current_stage: current_stage.to_owned(),
                        steps: Some(actives),
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
                editor_angle: self.editor_angle,
                angle: self.angle,
                angle_v: self.angle_v,
                flip_x: Some(bool_to_i8(self.flip_x)),
                flip_y: Some(bool_to_i8(self.flip_y)),
                chute_x: self.attr.chute_x,
                chute_y: self.attr.chute_y,
                chute_height: self.attr.chute_height,
                extension: self.attr.extension,
                inflate: option_bool_to_option_i8(self.attr.inflate),
                inflation: self.attr.inflation,
                exploded: Some(bool_to_i8(self.explode)),
                rope: option_bool_to_option_i8(self.attr.rope),
                chute_angle: self.attr.chute_angle,
                activated: Some(bool_to_i8(self.active)),
                deployed: option_bool_to_option_i8(self.attr.deployed),
            }
        }
    }

    #[derive(Debug, Clone)]
    pub struct SR1PartData {
        // 单独的属性
        pub attr: SR1PartDataAttr,
        // 基本状态属性
        pub x: f64,
        pub y: f64,
        pub id: i64,
        pub angle: f64, // 弧度制
        pub angle_v: f64,
        // 状态属性
        pub part_type: SR1PartTypeEnum,
        pub part_type_id: String,
        pub editor_angle: i32,
        pub flip_x: bool,
        pub flip_y: bool,
        pub active: bool,

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
            match shape.bounds[0] {
                Edge::OneTimeLine(line) => {
                    pos_box.0 = line.start.x;
                    pos_box.1 = line.start.y;
                }
                _ => {}
            }
            match shape.bounds[2] {
                Edge::OneTimeLine(line) => {
                    pos_box.2 = line.start.x;
                    pos_box.3 = line.start.y;
                }
                _ => {}
            }
            pos_box
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
        pub steps: Option<Vec<Vec<(i64, bool)>>>,
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
        pub fn new(
            fuel: Option<f64>,
            name: Option<String>,
            throttle: Option<f64>,
            current_stage: Option<i32>,
            steps: Option<Vec<Vec<(i64, bool)>>>,
            extension: Option<f64>,
            chute_x: Option<f64>,
            chute_y: Option<f64>,
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
                chute_x,
                chute_y,
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
            } else if let Some(engine) = &raw_data.engine {
                Some(engine.fuel.to_owned())
            } else {
                None
            };
            let (name, throttle, current_stage, steps) = if let Some(pod) = &raw_data.pod {
                (
                    Some(pod.name.clone()),
                    Some(pod.throttle),
                    Some(pod.stages.current_stage),
                    Some({
                        let mut steps = Vec::new();
                        match &pod.stages.steps {
                            Some(step_vec) => {
                                for step in step_vec {
                                    let mut step_vec = Vec::new();
                                    if let Some(active) = &step.activates {
                                        for act in active {
                                            step_vec.push((act.id, i8_to_bool(act.moved)));
                                        }
                                    }
                                    steps.push(step_vec);
                                }
                            }
                            None => {}
                        }
                        steps
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
                inflate: option_i8_to_option_bool(raw_data.inflate),
                inflation: raw_data.inflation,
                deployed: option_i8_to_option_bool(raw_data.deployed),
                rope: option_i8_to_option_bool(raw_data.rope),
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
        pub parts: Vec<SR1PartData>,
        pub connections: Vec<Connection>,
        pub lift_off: bool,
        pub touch_ground: bool,
        pub disconnected: Option<Vec<(Vec<SR1PartData>, Option<Vec<Connection>>)>>,
    }

    impl SR1Ship {
        pub fn from_file(file_name: String, ship_name: Option<String>) -> Option<Self> {
            // 首先验证文件是否存在 不存在则返回None
            if !std::path::Path::new(&file_name).exists() {
                return None;
            }
            // 解析为 RawShip
            let ship: RawShip = RawShip::from_file(file_name).unwrap();
            Some(ship.to_sr_ship(ship_name))
        }

        pub fn parse_part_list_to_part(&mut self, part_list: SR1PartList) {
            // parse parts
            for part in self.parts.iter_mut() {
                let part_type_id = part.part_type_id.clone();
                if let Some(part_type) = part_list.get_part_type(part_type_id) {
                    part.part_type = part_type.p_type;
                } else {
                    part.part_type = SR1PartTypeEnum::strut;
                }
            }
            for disconnects in self.disconnected.iter_mut() {
                for (parts, _) in disconnects.iter_mut() {
                    for part in parts.iter_mut() {
                        let part_type_id = part.part_type_id.clone();
                        if let Some(part_type) = part_list.get_part_type(part_type_id) {
                            part.part_type = part_type.p_type;
                        } else {
                            part.part_type = SR1PartTypeEnum::strut;
                        }
                    }
                }
            }
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
            let mut parts = Vec::new();
            for part in &self.parts {
                parts.push(part.to_raw_part_data());
            }
            let connections = Connections {
                connects: Some(self.connections.clone()),
            };
            let disconnected = match &self.disconnected {
                Some(disconnected) => {
                    let mut disconnected_vec: Vec<RawDisconnectedPart> = Vec::new();
                    for (parts, connections) in disconnected {
                        let mut raw_parts = Vec::new();
                        for part in parts {
                            raw_parts.push(part.to_raw_part_data());
                        }
                        disconnected_vec.push(RawDisconnectedPart {
                            parts: RawParts { parts: raw_parts },
                            connects: Connections {
                                connects: connections.clone(),
                            },
                        });
                    }
                    Some(RawDisconnectedParts {
                        parts: Some(disconnected_vec),
                    })
                }
                _ => None,
            };
            RawShip {
                parts: RawParts { parts },
                connects: connections,
                version: 1,
                lift_off: bool_to_i8(self.lift_off),
                touch_ground: bool_to_i8(self.touch_ground),
                disconnected,
            }
        }
    }

    pub fn get_max_box(parts: &Vec<SR1PartData>, part_list: &SR1PartList) -> (f64, f64, f64, f64) {
        let mut max_box = (0_f64, 0_f64, 0_f64, 0_f64);
        for part in parts.iter() {
            let part_type = part_list.get_part_type(part.part_type_id.clone()).unwrap();
            let ((x1, y1), (x2, y2)) = part_type.get_box();
            // rotate
            let mut p1 = Point2D::new(x1, y1);
            let mut p2 = Point2D::new(x2, y2);
            p1.rotate_radius_mut(part.angle);
            p2.rotate_radius_mut(part.angle);
            let p1 = p1.add(part.x * 2.0, part.y * 2.0);
            let p2 = p2.add(part.x * 2.0, part.y * 2.0);
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
}

#[allow(unused)]
pub mod math {

    pub trait Rotatable {
        // 懒了，直接实现一个协议得了
        fn rotate(&self, angle: f64) -> Self;
        fn rotate_radius(&self, radius: f64) -> Self;

        fn rotate_mut(&mut self, angle: f64);
        fn rotate_radius_mut(&mut self, radius: f64);
    }

    #[derive(Clone, Copy)]
    pub struct Point2D {
        pub x: f64,
        pub y: f64,
    }

    impl Point2D {
        pub fn new(x: f64, y: f64) -> Self { Point2D { x, y } }

        #[inline]
        pub fn new_00() -> Self { Point2D { x: 0.0, y: 0.0 } }

        #[inline]
        pub fn distance(&self, other: &Point2D) -> f64 {
            let dx = (other.x - self.x).powf(2.0);
            let dy = (other.y - self.y).powf(2.0);
            (dx + dy).powf(0.5)
        }

        #[inline]
        pub fn distance_00(&self) -> f64 { self.distance(&Point2D::new(0.0, 0.0)) }

        #[inline]
        pub fn add(&self, x: f64, y: f64) -> Self { Point2D::new(self.x + x, self.y + y) }

        #[inline]
        pub fn add_mut(&mut self, x: f64, y: f64) -> () {
            self.x += x;
            self.y += y;
        }
    }

    impl Rotatable for Point2D {
        #[inline]
        fn rotate(&self, angle: f64) -> Self { self.rotate_radius(angle.to_radians()) }

        #[inline]
        fn rotate_radius(&self, radius: f64) -> Self {
            let sin = radius.sin();
            let cos = radius.cos();
            let x = self.x * cos - self.y * sin;
            let y = self.x * sin + self.y * cos;
            Point2D { x, y }
        }

        #[inline]
        fn rotate_mut(&mut self, angle: f64) { self.rotate_radius_mut(angle.to_radians()) }

        #[inline]
        fn rotate_radius_mut(&mut self, radius: f64) { *self = self.rotate_radius(radius); }
    }

    #[derive(Clone, Copy)]
    pub struct CircularArc {
        pub r: f64,
        // 半径
        pub pos: Point2D,
        // 圆心位置
        pub start_angle: f64,
        // 圆弧开始位置 角度值
        pub end_angle: f64,
        // 圆弧结束位置 角度值
    }

    #[derive(Clone, Copy)]
    pub struct OneTimeLine {
        // pub k: f64,
        // pub b: f64,
        // y = kx + b
        // kx + b - y = 0
        pub start: Point2D,
        // start point
        pub end: Point2D,
        // end point
    }

    impl Rotatable for OneTimeLine {
        fn rotate(&self, angle: f64) -> Self { self.rotate_radius(angle.to_radians()) }

        fn rotate_radius(&self, radius: f64) -> Self { OneTimeLine::point_new(&self.start.rotate_radius(radius), &self.end.rotate_radius(radius)) }

        fn rotate_mut(&mut self, angle: f64) { self.rotate_radius_mut(angle.to_radians()) }

        fn rotate_radius_mut(&mut self, radius: f64) { *self = self.rotate_radius(radius); }
    }

    #[derive(Clone, Copy)]
    pub enum Edge {
        OneTimeLine(OneTimeLine),
        CircularArc(CircularArc),
    }

    #[derive(Clone)]
    pub struct Shape {
        pub pos: Point2D,
        pub angle: f64,
        // 旋转角度 角度值
        pub bounds: Vec<Edge>,
    }

    impl Shape {
        pub fn new(x: Option<f64>, y: Option<f64>, angle: Option<f64>, bounds: Vec<Edge>) -> Self {
            let x = x.unwrap_or(0.0);
            let y = y.unwrap_or(0.0);
            let angle = angle.unwrap_or(0.0);
            Shape {
                pos: Point2D::new(x, y),
                angle,
                bounds,
            }
        }

        pub fn new_width_height(width: f64, height: f64, radius: Option<f64>) -> Self {
            let d_width = width / 2.0;
            let d_height = height / 2.0;
            let mut edges: Vec<Edge> = vec![
                Edge::OneTimeLine(OneTimeLine::pos_new(-d_width, -d_height, d_width, -d_height)),
                Edge::OneTimeLine(OneTimeLine::pos_new(d_width, -d_height, d_width, d_height)),
                Edge::OneTimeLine(OneTimeLine::pos_new(d_width, d_height, -d_width, d_height)),
                Edge::OneTimeLine(OneTimeLine::pos_new(-d_width, d_height, -d_width, -d_height)),
            ];
            if let Some(radius) = radius {
                edges = edges
                    .iter()
                    .map(|edge| match edge {
                        Edge::OneTimeLine(line) => {
                            let start = line.start.rotate_radius(radius);
                            let end = line.end.rotate_radius(radius);
                            Edge::OneTimeLine(OneTimeLine::point_new(&start, &end))
                        }
                        Edge::CircularArc(arc) => {
                            let pos = arc.pos.rotate_radius(radius);
                            Edge::CircularArc(CircularArc {
                                r: arc.r,
                                pos,
                                start_angle: arc.start_angle,
                                end_angle: arc.end_angle,
                            })
                        }
                    })
                    .collect();
            }
            Shape {
                pos: Point2D::new_00(),
                angle: 0.0,
                bounds: edges,
            }
        }

        pub fn move_xy(&mut self, x: Option<f64>, y: Option<f64>) {
            let x = x.unwrap_or(0.0);
            let y = y.unwrap_or(0.0);
            for edge in self.bounds.iter() {
                match edge {
                    Edge::OneTimeLine(mut line) => {
                        line.start.x += x;
                        line.start.y += y;
                        line.end.x += x;
                        line.end.y += y;
                    }
                    Edge::CircularArc(mut arc) => {
                        arc.pos.x += x;
                        arc.pos.y += y;
                    }
                }
            }
        }
    }

    impl OneTimeLine {
        #[inline]
        pub fn pos_new(x1: f64, y1: f64, x2: f64, y2: f64) -> Self {
            // let k = (x2 - x1) / (y2 - y1);
            // let b = y1 - (x1 * k);
            let start = Point2D::new(x1, y1);
            let end = Point2D::new(x2, y2);
            OneTimeLine { start, end }
        }

        #[inline]
        pub fn point_new(a: &Point2D, b: &Point2D) -> Self { OneTimeLine::pos_new(a.x, a.y, b.x, b.y) }

        pub fn point1_k_b_new(point: &Point2D, k: Option<f64>, b: Option<f64>) -> Self {
            let mut k_: f64;
            let mut b_: f64;
            match (k, b) {
                (Some(k), None) => {
                    k_ = k;
                    b_ = point.y - (k * point.x)
                }
                (None, Some(b)) => {
                    b_ = b;
                    k_ = (point.y - b) / point.x;
                }
                (Some(k), Some(b)) => {
                    k_ = k;
                    b_ = b;
                }
                _ => {
                    k_ = point.y / point.x;
                    b_ = 0.0;
                }
            }
            OneTimeLine {
                start: *point,
                end: Point2D::new(0.0, b_),
            }
        }

        pub fn point_d() -> f64 { 1.0 }
    }
}

#[allow(dead_code)]
pub mod dr {

    #[derive(Clone, Copy)]
    pub enum ConnectType {
        Stick,
        FixedPoint,
        RotatePoint,
    }

    #[derive(Clone, Copy)]
    pub struct Connect {
        pub c_type: ConnectType,
        pub d_pos: f64,
        pub angel: f64,
    }

    #[derive(Clone, Copy)]
    pub enum PartType {
        Pod,
        Separator,
        Wheel,
        Fuselage,
        Beam,
        Engine,
        FuelTank,
        Parachute,
        Nosecone,
        SolarPanel,
        Battery,
        Dock,
        Port,
        Lander,
    }

    pub struct DRPartData {
        pub x: f64,
        pub y: f64,
        pub dx: f64,
        pub dy: f64,
        pub id: i64,
        pub p_type: PartType,
        pub active: bool,
        pub angle: f64, // 角度制
        pub angle_v: f64,
        pub flip_x: bool,
        pub flip_y: bool,
        pub connections: Option<Vec<usize>>,
    }
}
