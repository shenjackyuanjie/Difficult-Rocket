/*
 * -------------------------------
 * Difficult Rocket
 * Copyright © 2020-2023 by shenjackyuanjie 3695888@qq.com
 * All rights reserved
 * -------------------------------
 */


pub mod sr1 {

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
                Edge::OneTimeLine{data: OneTimeLine::pos_new(-d_width, -d_height, d_width, -d_height)},
                Edge::OneTimeLine{data: OneTimeLine::pos_new(d_width, -d_height, d_width, d_height)},
                Edge::OneTimeLine{data: OneTimeLine::pos_new(d_width, d_height, -d_width, d_height)},
                Edge::OneTimeLine{data: OneTimeLine::pos_new(-d_width, d_height, -d_width, -d_height)}
            ];
            if let Some(angle) = angle {

            }
            Shape { pos: Point2D::new_00(), angle: 0.0, bounds: edges}
        }
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
