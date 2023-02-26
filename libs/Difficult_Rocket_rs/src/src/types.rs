/*
 * -------------------------------
 * Difficult Rocket
 * Copyright © 2020-2023 by shenjackyuanjie 3695888@qq.com
 * All rights reserved
 * -------------------------------
 */


pub mod sr1 {
    use super::math::{Shape, Point2D};
    use crate::sr1_data::part_list::{RawPartList, RawPartType, SR1PartTypeEnum, Location};
    use crate::sr1_data::part_list::Damage as RawDamage;

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
        }.to_string()
    }

    #[derive(Clone)]
    pub struct SR1PartData {
        pub x: f64,
        pub y: f64,
        pub id: i64,
        pub p_type: String,
        pub active: bool,
        pub angle: f64, // 弧度制
        pub angle_v: f64,
        pub editor_angle: usize,
        pub flip_x: bool,
        pub flip_y: bool,
        pub explode: bool,
        pub textures: String,
        pub connections: Option<Vec<((usize, usize), (isize, isize))>>
    }

    #[derive(Clone)]
    pub enum SR1PartAttr {
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
        Solar { charge_rate: f64, },
        Lander {
            max_angle: f64,
            min_length: f64,
            max_length: f64,
            angle_speed: f64,
            length_speed: f64,
            width: f64,
        }
    }

    #[derive(Copy, Clone)]
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
                explosion_size: Some(self.explosion_size)
            }
        }
    }

    #[derive(Clone)]
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
        pub shape: Option<Shape>,
        // 部件碰撞箱
        pub attr: Option<SR1PartAttr>
        // 部件特殊属性
    }

    #[derive(Clone)]
    pub struct SR1PartList {
        pub types: Vec<SR1PartType>,
        pub name: String,
    }

    pub trait SR1PartTypeData {
        fn to_sr_part_type(&self) -> SR1PartType;
        fn to_raw_part_type(&self) -> RawPartType;
    }

    impl SR1PartList {
        #[inline]
        pub fn new(name: String, types: Vec<SR1PartType>) -> Self {
            SR1PartList { name, types }
        }

        pub fn part_types_new(part_types: Vec<SR1PartType>, name: Option<String>) -> Self {
            let mut types: Vec<SR1PartType> = Vec::new();
            let name = match name {
                Some(name) => name,
                None => "NewPartList".to_string()
            };
            for part_type in part_types {
                types.insert(0, part_type);
            }
            SR1PartList::new(name, types)
        }

        // pub fn part_type_new(part_type: RawPartType) -> Self {
        //     let mut types: Vec<SR1PartType> = Vec::new();
        // }

        pub fn insert_part(&mut self, part: SR1PartType) -> () {
            self.types.insert(0, part);
        }
    }

    impl SR1PartTypeData for SR1PartType {
        fn to_sr_part_type(&self) -> SR1PartType {
            self.clone()
        }

        fn to_raw_part_type(&self) -> RawPartType {
            // let shape = crate::sr1_data::part_list::Shape;
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
                tank: None,
                engine: None,
                rcs: None,
                solar: None,
                // shape: Some(self.shape.clone()),
                shape: None,
                attach_points: None,
                lander: None,
            }
        }
    }

}

#[allow(unused)]
pub mod math {

    #[derive(Clone, Copy)]
    pub struct Point2D {
        pub x: f64,
        pub y: f64
    }

    impl Point2D {
        pub fn new(x: f64, y: f64) -> Self {
            Point2D{x, y}
        }

        #[inline]
        pub fn new_00() -> Self { Point2D { x: 0.0, y :0.0 } }

        #[inline]
        pub fn distance(&self, other: &Point2D) -> f64 {
            let dx = (other.x - self.x).powf(2.0);
            let dy = (other.y - self.y).powf(2.0);
            (dx + dy).powf(0.5)
        }

        #[inline]
        pub fn distance_00(&self) -> f64 {
            self.distance(&Point2D::new(0.0, 0.0))
        }

        #[inline]
        pub fn rotate_angle(&self, angle: f64) -> Self {
            let radius = angle.to_radians();
            let sin = radius.sin();
            let cos = radius.cos();
            let x = self.x * cos - self.y * sin;
            let y = self.x * sin + self.y * cos;
            Point2D{ x, y }
        }
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
        pub bounds: Vec<Edge>
    }

    impl Shape {
        pub fn new(x: Option<f64>, y: Option<f64>, angle: Option<f64>, bounds: Vec<Edge>) -> Self {
            let x = x.unwrap_or(0.0);
            let y = y.unwrap_or(0.0);
            let angle = angle.unwrap_or(0.0);
            Shape { pos: Point2D::new(x, y), angle, bounds }
        }

        pub fn new_width_height(width: f64, height: f64, angle: Option<f64>) -> Self {
            let d_width = width / 2.0;
            let d_height = height / 2.0;
            let mut edges: Vec<Edge> = vec![
                Edge::OneTimeLine{0: OneTimeLine::pos_new(-d_width, -d_height, d_width, -d_height)},
                Edge::OneTimeLine{0: OneTimeLine::pos_new(d_width, -d_height, d_width, d_height)},
                Edge::OneTimeLine{0: OneTimeLine::pos_new(d_width, d_height, -d_width, d_height)},
                Edge::OneTimeLine{0: OneTimeLine::pos_new(-d_width, d_height, -d_width, -d_height)}
            ];
            if let Some(angle) = angle {
                edges = edges.iter().map(|edge| {
                    match edge {
                        Edge::OneTimeLine(line) => {
                            let start = line.start.rotate_angle(angle);
                            let end = line.end.rotate_angle(angle);
                            Edge::OneTimeLine(OneTimeLine::point_new(&start, &end))
                        },
                        Edge::CircularArc(arc) => {
                            let pos = arc.pos.rotate_angle(angle);
                            Edge::CircularArc(CircularArc{ r: arc.r, pos, start_angle: arc.start_angle, end_angle: arc.end_angle })
                        }
                    }
                }).collect();
            }
            Shape { pos: Point2D::new_00(), angle: 0.0, bounds: edges}
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
        pub fn point_new(a: &Point2D, b: &Point2D) -> Self {
            OneTimeLine::pos_new(a.x, a.y, b.x, b.y)
        }

        pub fn point1_k_b_new(point: &Point2D, k: Option<f64>, b: Option<f64>) -> Self {
            let mut k_: f64;
            let mut b_: f64;
            match (k, b) {
                (Some(k), None) => {
                    k_ = k;
                    b_ = point.y - (k * point.x)
                },
                (None, Some(b)) => {
                    b_ = b;
                    k_ = (point.y - b) / point.x;
                },
                (Some(k), Some(b)) => {
                    k_ = k;
                    b_ = b;
                },
                _ => {
                    k_ = point.y / point.x;
                    b_ = 0.0;
                }
            }
            OneTimeLine{
                start: *point,
                end: Point2D::new(0.0, b_)
            }
        }

        pub fn rotate(&self, angle: f64) -> Self {
            OneTimeLine::point_new(&self.start.rotate_angle(angle), &self.end.rotate_angle(angle))
        }

        pub fn point_d() -> f64 {
            1.0
        }
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
        Lander
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
        pub connections: Option<Vec<usize>>
    }

    impl DRPartData {
        pub fn get_textures(&self) -> String {
            "aaa".to_string()
        }
    }
}
