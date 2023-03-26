/*
 * -------------------------------
 * Difficult Rocket
 * Copyright © 2020-2023 by shenjackyuanjie 3695888@qq.com
 * All rights reserved
 * -------------------------------
 */


pub mod python_class {
    use pyo3::prelude::*;

    use crate::math::matrix::{Matrix3, Matrix4};
    use crate::math::vector::{Vector2, Vector3, Vector4};

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

    #[allow(unused)]
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

    /// 这是一个用来自动给 impl xxx for xxx 的块去掉 trait 部分的宏
    /// 用于在为 pyclass 实现

    #[pymethods]
    impl PyVector2 {
        #[new]
        fn py_new(x: f64, y: f64) -> Self {
            return Self {
                data: Vector2::new(x, y),
            };
        }
    }

    #[pymethods]
    impl PyVector2 {
        fn __add__(&self, other: &Self) -> Self {
            return Self {
                data: self.data + other.data,
            };
        }
    }
}
