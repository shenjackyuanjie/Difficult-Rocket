/*
 * -------------------------------
 * Difficult Rocket
 * Copyright © 2020-2023 by shenjackyuanjie 3695888@qq.com
 * All rights reserved
 * -------------------------------
 */

pub mod camera {
    use pyo3::prelude::*;

    #[pyclass(name = "Camera_rs")]
    pub struct CameraRs{
        pub dx: f64,
        pub dy: f64,
        pub zoom: f64,
        pub max_zoom: f64,
        pub min_zoom: f64,
        pub window: PyObject,
    }

    #[pymethods]
    impl CameraRs {

    }

}
