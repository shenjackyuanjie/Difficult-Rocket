/*
 * -------------------------------
 * Difficult Rocket
 * Copyright © 2020-2023 by shenjackyuanjie 3695888@qq.com
 * All rights reserved
 * -------------------------------
 */

pub mod vector {
    use std::ops::{Add, Div, Mul, Sub};

    #[derive(Debug, Clone, Copy, PartialEq, PartialOrd)]
    pub struct Vector2 {
        pub x: f64,
        pub y: f64,
    }

    #[derive(Debug, Clone, Copy, PartialEq, PartialOrd)]
    pub struct Vector3 {
        pub x: f64,
        pub y: f64,
        pub z: f64,
    }

    #[derive(Debug, Clone, Copy, PartialEq, PartialOrd)]
    pub struct Vector4 {
        pub x: f64,
        pub y: f64,
        pub z: f64,
        pub w: f64,
    }

    pub trait VectorTrait {
        fn len(&self) -> i8; // use short int to save memory (even if its not going to save a lot)
        fn floordiv(&self, other: &Self) -> Self;
        fn abs(&self) -> f64;
        fn neg(&self) -> Self;
        fn round(&self, ndigits: Option<i64>) -> Self;
        fn radd(&self, other: &Self) -> Self;
    }

    impl Add for Vector2 {
        type Output = Self;

        fn add(self, rhs: Self) -> Self::Output {
            Self::new(self.x + rhs.x, self.y + rhs.y)
        }
    }

    impl Sub for Vector2 {
        type Output = Self;

        fn sub(self, rhs: Self) -> Self::Output {
            Self::new(self.x - rhs.x, self.y - rhs.y)
        }
    }

    impl Mul for Vector2 {
        type Output = Self;

        fn mul(self, rhs: Self) -> Self::Output {
            Self::new(self.x * rhs.x, self.y * rhs.y)
        }
    }

    impl Div for Vector2 {
        type Output = Self;

        fn div(self, rhs: Self) -> Self::Output {
            Self::new(self.x / rhs.x, self.y / rhs.y)
        }
    }

    impl Add for Vector3 {
        type Output = Self;

        fn add(self, rhs: Self) -> Self::Output {
            Self::new(self.x + rhs.x, self.y + rhs.y, self.z + rhs.z)
        }
    }

    impl Sub for Vector3 {
        type Output = Self;

        fn sub(self, rhs: Self) -> Self::Output {
            Self::new(self.x - rhs.x, self.y - rhs.y, self.z - rhs.z)
        }
    }

    impl Mul for Vector3 {
        type Output = Self;

        fn mul(self, rhs: Self) -> Self::Output {
            Self::new(self.x * rhs.x, self.y * rhs.y, self.z * rhs.z)
        }
    }

    impl Div for Vector3 {
        type Output = Self;

        fn div(self, rhs: Self) -> Self::Output {
            Self::new(self.x / rhs.x, self.y / rhs.y, self.z / rhs.z)
        }
    }

    impl Add for Vector4 {
        type Output = Self;

        fn add(self, rhs: Self) -> Self::Output {
            Self::new(
                self.x + rhs.x,
                self.y + rhs.y,
                self.z + rhs.z,
                self.w + rhs.w,
            )
        }
    }

    impl Sub for Vector4 {
        type Output = Self;

        fn sub(self, rhs: Self) -> Self::Output {
            Self::new(
                self.x - rhs.x,
                self.y - rhs.y,
                self.z - rhs.z,
                self.w - rhs.w,
            )
        }
    }

    impl Mul for Vector4 {
        type Output = Self;

        fn mul(self, rhs: Self) -> Self::Output {
            Self::new(
                self.x * rhs.x,
                self.y * rhs.y,
                self.z * rhs.z,
                self.w * rhs.w,
            )
        }
    }

    impl Div for Vector4 {
        type Output = Self;

        fn div(self, rhs: Self) -> Self::Output {
            Self::new(
                self.x / rhs.x,
                self.y / rhs.y,
                self.z / rhs.z,
                self.w / rhs.w,
            )
        }
    }

    impl VectorTrait for Vector2 {
        fn len(&self) -> i8 {
            return 2;
        }
        fn floordiv(&self, other: &Self) -> Self {
            // 手动模拟python的//运算符
            Self::new((self.x / other.x).floor(), (self.y / other.y).floor())
        }

        fn abs(&self) -> f64 {
            return (self.x.powi(2) + self.y.powi(2)).sqrt();
        }

        fn neg(&self) -> Self {
            Self::new(-self.x, -self.y)
        }

        fn round(&self, ndigits: Option<i64>) -> Self {
            match ndigits {
                Some(ndigits) => {
                    let ndigits = ndigits as i32;
                    Self::new(
                        self.x.round() * 10.0_f64.powi(ndigits),
                        self.y.round() * 10.0_f64.powi(ndigits),
                    )
                }
                None => Self::new(self.x.round(), self.y.round()),
            }
        }

        fn radd(&self, other: &Self) -> Self {
            Self::new(self.x + other.x, self.y + other.y)
        }
    }

    impl VectorTrait for Vector3 {
        fn len(&self) -> i8 {
            return 3;
        }

        fn floordiv(&self, other: &Self) -> Self {
            // 手动模拟python的//运算符
            Self::new(
                (self.x / other.x).floor(),
                (self.y / other.y).floor(),
                (self.z / other.z).floor(),
            )
        }

        fn abs(&self) -> f64 {
            return (self.x.powi(2) + self.y.powi(2) + self.z.powi(2)).sqrt();
        }

        fn neg(&self) -> Self {
            Self::new(-self.x, -self.y, -self.z)
        }

        fn round(&self, ndigits: Option<i64>) -> Self {
            match ndigits {
                Some(ndigits) => {
                    let ndigits = ndigits as i32;
                    Self::new(
                        self.x.round() * 10.0_f64.powi(ndigits),
                        self.y.round() * 10.0_f64.powi(ndigits),
                        self.z.round() * 10.0_f64.powi(ndigits),
                    )
                }
                None => Self::new(self.x.round(), self.y.round(), self.z.round()),
            }
        }

        fn radd(&self, other: &Self) -> Self {
            Self::new(self.x + other.x, self.y + other.y, self.z + other.z)
        }
    }

    impl VectorTrait for Vector4 {
        fn len(&self) -> i8 {
            return 4;
        }

        fn floordiv(&self, other: &Self) -> Self {
            // 手动模拟python的//运算符
            Self::new(
                (self.x / other.x).floor(),
                (self.y / other.y).floor(),
                (self.z / other.z).floor(),
                (self.w / other.w).floor(),
            )
        }

        fn abs(&self) -> f64 {
            return (self.x.powi(2) + self.y.powi(2) + self.z.powi(2) + self.w.powi(2)).sqrt();
        }

        fn neg(&self) -> Self {
            Self::new(-self.x, -self.y, -self.z, -self.w)
        }

        fn round(&self, ndigits: Option<i64>) -> Self {
            match ndigits {
                Some(ndigits) => {
                    let ndigits = ndigits as i32;
                    Self::new(
                        self.x.round() * 10.0_f64.powi(ndigits),
                        self.y.round() * 10.0_f64.powi(ndigits),
                        self.z.round() * 10.0_f64.powi(ndigits),
                        self.w.round() * 10.0_f64.powi(ndigits),
                    )
                }
                None => Self::new(
                    self.x.round(),
                    self.y.round(),
                    self.z.round(),
                    self.w.round(),
                ),
            }
        }

        fn radd(&self, other: &Self) -> Self {
            Self::new(
                self.x + other.x,
                self.y + other.y,
                self.z + other.z,
                self.w + other.w,
            )
        }
    }

    impl Vector2 {
        pub fn new(x: f64, y: f64) -> Self {
            Self { x, y }
        }
    }

    impl Vector3 {
        pub fn new(x: f64, y: f64, z: f64) -> Self {
            Self { x, y, z }
        }
    }

    impl Vector4 {
        pub fn new(x: f64, y: f64, z: f64, w: f64) -> Self {
            Self { x, y, z, w }
        }
    }
}

pub mod matrix {
    use super::vector::{Vector3, Vector4};

    #[derive(Debug, Clone, Copy, PartialEq, PartialOrd)]
    pub struct Matrix3 {
        pub line1: Vector3,
        pub line2: Vector3,
        pub line3: Vector3,
    }

    #[derive(Debug, Clone, Copy, PartialEq, PartialOrd)]
    pub struct Matrix4 {
        pub line1: Vector4,
        pub line2: Vector4,
        pub line3: Vector4,
        pub line4: Vector4,
    }
}
