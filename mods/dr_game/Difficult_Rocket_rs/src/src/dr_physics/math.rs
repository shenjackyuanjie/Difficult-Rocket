use std::ops::Add;

pub const POINT_D: f64 = 1.0;

pub trait Rotate {
    // 懒了，直接实现一个协议得了
    fn rotate(&self, angle: f64) -> Self;
    fn rotate_radius(&self, radius: f64) -> Self;

    fn rotate_mut(&mut self, angle: f64);
    fn rotate_radius_mut(&mut self, radius: f64);
}

#[derive(Default, Clone, Copy)]
pub struct Point2D {
    pub x: f64,
    pub y: f64,
}

impl Point2D {
    pub fn new(x: f64, y: f64) -> Self { Self { x, y } }

    pub fn distance(&self, other: &Point2D) -> f64 {
        let dx = (other.x - self.x).powf(2.0);
        let dy = (other.y - self.y).powf(2.0);
        (dx + dy).powf(0.5)
    }

    pub fn distance_default(&self) -> f64 { self.distance(&Point2D::new(0.0, 0.0)) }

    pub fn add_mut(&mut self, x: f64, y: f64) {
        self.x += x;
        self.y += y;
    }
}

impl Rotate for Point2D {
    fn rotate_radius(&self, radius: f64) -> Self {
        let sin = radius.sin();
        let cos = radius.cos();
        let x = self.x * cos - self.y * sin;
        let y = self.x * sin + self.y * cos;

        Self { x, y }
    }

    fn rotate(&self, angle: f64) -> Self { self.rotate_radius(angle.to_radians()) }

    fn rotate_radius_mut(&mut self, radius: f64) { *self = self.rotate_radius(radius); }

    fn rotate_mut(&mut self, angle: f64) { self.rotate_radius_mut(angle.to_radians()) }
}

impl Add for Point2D {
    type Output = Self;

    fn add(self, rhs: Self) -> Self {
        Self {
            x: self.x + rhs.x,
            y: self.y + rhs.y,
        }
    }
}

#[derive(Clone, Copy)]
pub struct CircularArc {
    // 半径
    pub r: f64,
    // 圆心位置
    pub pos: Point2D,
    // 圆弧开始位置 角度值
    pub start_degree: f64,
    // 圆弧结束位置 角度值
    pub end_degree: f64,
}

#[derive(Clone, Copy)]
pub struct OneTimeLine {
    // pub k: f64,
    // pub b: f64,
    // y = kx + b
    // kx + b - y = 0

    // start point
    pub start: Point2D,
    // end point
    pub end: Point2D,
}

impl Rotate for OneTimeLine {
    fn rotate(&self, angle: f64) -> Self { self.rotate_radius(angle.to_radians()) }

    fn rotate_radius(&self, radius: f64) -> Self {
        OneTimeLine::point_new(&self.start.rotate_radius(radius), &self.end.rotate_radius(radius))
    }

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
    // 旋转角度 角度值
    pub degree: f64,
    pub bounds: Vec<Edge>,
}

impl Shape {
    pub fn new(x: Option<f64>, y: Option<f64>, degree: Option<f64>, bounds: Vec<Edge>) -> Self {
        let x = x.unwrap_or(0.0);
        let y = y.unwrap_or(0.0);
        let degree = degree.unwrap_or(0.0);

        Self {
            pos: Point2D::new(x, y),
            degree,
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
                            start_degree: arc.start_degree,
                            end_degree: arc.end_degree,
                        })
                    }
                })
                .collect();
        }

        Self {
            pos: Default::default(),
            degree: 0.0,
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
    pub fn pos_new(x1: f64, y1: f64, x2: f64, y2: f64) -> Self {
        // let k = (x2 - x1) / (y2 - y1);
        // let b = y1 - (x1 * k);
        let start = Point2D::new(x1, y1);
        let end = Point2D::new(x2, y2);

        Self { start, end }
    }

    pub fn point_new(a: &Point2D, b: &Point2D) -> Self { Self::pos_new(a.x, a.y, b.x, b.y) }

    pub fn point1_k_b_new(point: &Point2D, k: Option<f64>, b: Option<f64>) -> Self {
        let _k: f64;
        let b_: f64;
        match (k, b) {
            (Some(k), None) => {
                _k = k;
                b_ = point.y - (k * point.x)
            }
            (None, Some(b)) => {
                b_ = b;
                _k = (point.y - b) / point.x;
            }
            (Some(k), Some(b)) => {
                _k = k;
                b_ = b;
            }
            _ => {
                _k = point.y / point.x;
                b_ = 0.0;
            }
        }

        Self {
            start: *point,
            end: Point2D::new(0.0, b_),
        }
    }
}
