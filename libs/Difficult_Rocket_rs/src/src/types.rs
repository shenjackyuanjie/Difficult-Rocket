/*
 * -------------------------------
 * Difficult Rocket
 * Copyright © 2020-2023 by shenjackyuanjie 3695888@qq.com
 * All rights reserved
 * -------------------------------
 */

#[allow(dead_code)]
pub mod sr1 {
    use std::collections::HashMap;

    pub fn map_ptype_textures(ptype: String) -> String {
        let mut value_map: HashMap<&str, &str> = HashMap::with_capacity(27 * 2);
        value_map.insert("pod-1", "Pod");
        value_map.insert("detacher-1", "DetacherVertical");
        value_map.insert("detacher-2", "DetacherRadial");
        value_map.insert("wheel-1", "Wheel");
        value_map.insert("wheel-2", "Wheel");
        value_map.insert("fuselage-1", "Fuselage");
        value_map.insert("strut-1", "Beam");
        value_map.insert("fueltank-0", "TankTiny");
        value_map.insert("fueltank-1", "TankSmall");
        value_map.insert("fueltank-2", "TankMedium");
        value_map.insert("fueltank-3", "TankLarge");
        value_map.insert("fueltank-4", "Puffy750");
        value_map.insert("fueltank-5", "SideTank");
        value_map.insert("engine-0", "EngineTiny");
        value_map.insert("engine-1", "EngineSmall");
        value_map.insert("engine-2", "EngineMedium");
        value_map.insert("engine-3", "EngineLarge");
        value_map.insert("engine-4", "SolidRocketBooster");
        value_map.insert("ion-0", "EngineIon");
        value_map.insert("parachute-1", "ParachuteCanister");
        value_map.insert("nosecone-1", "NoseCone");
        value_map.insert("rcs-1", "RcsBlock");
        value_map.insert("solar-1", "SolarPanelBase");
        value_map.insert("battery-0", "Battery");
        value_map.insert("dock-1", "DockingConnector");
        value_map.insert("port-1", "DockingPort");
        value_map.insert("lander-1", "LanderLegPreview");
        let result = value_map.get(ptype.as_str());
        match result {
            None => "Pod".to_string(),
            Some(i) => {
                let i = *i;
                i.to_string()
            }
        }
    }

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
        pub connections: Option<Vec<(usize, usize)>>
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

        pub fn new_00() -> Self { Point2D { x: 0.0, y :0.0 } }

        #[inline]
        pub fn distance(&self, other: &Point2D) -> f64 {
            let dx = (other.x - self.x).powf(2.0);
            let dy = (other.y - self.y).powf(2.0);
            (dx + dy).powf(0.5)
        }

        #[inline]
        pub fn get_op(&self) -> f64 {
            self.distance(&Point2D::new(0.0, 0.0))
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
        pub k: f64,
        pub b: f64,
        // y = kx + b
        // kx + b - y = 0
        pub start: Point2D,
        // start point
        pub end: Point2D,
        // end point
    }

    #[derive(Clone, Copy)]
    pub enum Edge {
        OneTimeLine{data: OneTimeLine},
        CircularArc{data: CircularArc},
    }

    impl OneTimeLine {
        #[inline]
        pub fn pos_new(x1: f64, y1: f64, x2: f64, y2: f64) -> Self {
            let k = (x2 - x1) / (y2 - y1);
            let b = y1 - (x1 * k);
            let start = Point2D::new(x1, y1);
            let end = Point2D::new(x2, y2);
            OneTimeLine { k, b, start, end }
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
                k: k_,
                b: b_,
                start: *point,
                end: Point2D::new(0.0, b_)
            }
        }

        pub fn point_d() -> f64 {
            1.0
        }
    }
}

#[allow(dead_code)]
pub mod dr {
    use super::math;

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

    #[derive(Clone)]
    pub struct Shape {
        pub x: f64,
        pub y: f64,
        pub angle: f64,
        // 旋转角度 角度值
        pub bounds: Vec<math::Edge>
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
