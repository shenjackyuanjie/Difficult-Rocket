/*
 * -------------------------------
 * Difficult Rocket
 * Copyright © 2020-2023 by shenjackyuanjie 3695888@qq.com
 * All rights reserved
 * -------------------------------
 */

pub mod macros {}

pub mod vector {

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
        fn add(&self, other: &Self) -> Self;
        fn sub(&self, other: &Self) -> Self;
        fn mul(&self, other: &Self) -> Self;
        fn truediv(&self, other: &Self) -> Self;
        fn floordiv(&self, other: &Self) -> Self;
        fn abs(&self) -> f64;
        fn neg(&self) -> Self;
        fn round(&self, ndigits: Option<i64>) -> Self;
        fn radd(&self, other: &Self) -> Self;
    }

    impl VectorTrait for Vector2 {
        fn len(&self) -> i8 {
            return 2;
        }

        fn add(&self, other: &Self) -> Self {
            Self::new(self.x + other.x, self.y + other.y)
        }

        fn sub(&self, other: &Self) -> Self {
            Self::new(self.x - other.x, self.y - other.y)
        }

        fn mul(&self, other: &Self) -> Self {
            Self::new(self.x * other.x, self.y * other.y)
        }

        fn truediv(&self, other: &Self) -> Self {
            Self::new(self.x / other.x, self.y / other.y)
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

        fn add(&self, other: &Self) -> Self {
            Self::new(self.x + other.x, self.y + other.y, self.z + other.z)
        }

        fn sub(&self, other: &Self) -> Self {
            Self::new(self.x - other.x, self.y - other.y, self.z - other.z)
        }

        fn mul(&self, other: &Self) -> Self {
            Self::new(self.x * other.x, self.y * other.y, self.z * other.z)
        }

        fn truediv(&self, other: &Self) -> Self {
            Self::new(self.x / other.x, self.y / other.y, self.z / other.z)
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

        fn add(&self, other: &Self) -> Self {
            Self::new(
                self.x + other.x,
                self.y + other.y,
                self.z + other.z,
                self.w + other.w,
            )
        }

        fn sub(&self, other: &Self) -> Self {
            Self::new(
                self.x - other.x,
                self.y - other.y,
                self.z - other.z,
                self.w - other.w,
            )
        }

        fn mul(&self, other: &Self) -> Self {
            Self::new(
                self.x * other.x,
                self.y * other.y,
                self.z * other.z,
                self.w * other.w,
            )
        }

        fn truediv(&self, other: &Self) -> Self {
            Self::new(
                self.x / other.x,
                self.y / other.y,
                self.z / other.z,
                self.w / other.w,
            )
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

pub mod python_class {
    use pyo3::prelude::*;

    use super::matrix::{Matrix3, Matrix4};
    use super::vector::{Vector2, Vector3, Vector4};

    #[pyclass(name = "Vector2")]
    pub struct PyVector2 {
        pub data: Vector2,
    }

    #[pyclass(name = "Vector3")]
    pub struct PyVector3 {
        pub data: Vector3,
    }

    #[pyclass(name = "Vector4")]
    pub struct PyVector4 {
        pub data: Vector4,
    }

    #[pyclass(name = "Matrix3")]
    pub struct PyMatrix3 {
        pub data: Matrix3,
    }

    #[pyclass(name = "Matrix4")]
    pub struct PyMatrix4 {
        pub data: Matrix4,
    }

    pub trait PyCalc {
        fn __add__(&self, other: &Self) -> Self;
        fn __sub__(&self, other: &Self) -> Self;
        fn __mul__(&self, other: &Self) -> Self;
        fn __truediv__(&self, other: &Self) -> Self;
        fn __floordiv__(&self, other: &Self) -> Self;
        fn __abs__(&self) -> f64;
        fn __neg__(&self) -> Self;
        fn __round__(&self, ndigits: Option<i64>) -> Self;
        fn __radd__(&self, other: &PyAny) -> Self;
        fn __eq__(&self, other: &Self) -> bool;
        fn __ne__(&self, other: &Self) -> bool;
    }

    #[pymethods]
    impl PyVector2 {
        #[new]
        fn py_new(x: f64, y: f64) -> Self {
            return PyVector2 {
                data: Vector2::new(x, y),
            };
        }
    }
}
