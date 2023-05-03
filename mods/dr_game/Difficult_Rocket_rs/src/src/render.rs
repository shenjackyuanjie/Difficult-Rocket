/*
 * -------------------------------
 * Difficult Rocket
 * Copyright © 2020-2023 by shenjackyuanjie 3695888@qq.com
 * All rights reserved
 * -------------------------------
 */

pub mod camera {

    use pyo3::intern;
    use pyo3::prelude::*;

    #[pyclass(name = "Camera_rs", subclass)]
    pub struct CameraRs {
        pub window: Py<PyAny>,
        #[pyo3(get, set)]
        pub dx: f64,
        #[pyo3(get, set)]
        pub dy: f64,
        pub zoom: f64,
        #[pyo3(get, set)]
        pub max_zoom: f64,
        #[pyo3(get, set)]
        pub min_zoom: f64,
    }

    #[pyclass(extends = CameraRs, name = "CenterCamera_rs")]
    pub struct CenterCameraRs;

    #[pymethods]
    impl CenterCameraRs {
        #[new]
        #[pyo3(signature = (window, zoom=1.0, dx=1.0, dy=1.0, min_zoom=1.0, max_zoom=1.0))]
        pub fn py_new(window: &PyAny, zoom: f64, dx: f64, dy: f64, min_zoom: f64, max_zoom: f64) -> PyResult<(Self, CameraRs)> {
            return Ok((
                CenterCameraRs {},
                CameraRs {
                    dx,
                    dy,
                    zoom,
                    min_zoom,
                    max_zoom,
                    window: window.into(),
                },
            ));
        }

        // pub fn __enter__(py_self: PyRef<Self>) -> PyResult<PyRef<Self>> {
        //     // println!("enter!");
        //     CenterCameraRs::begin()?;
        //     Ok(py_self)
        // }

        pub fn begin(self_: PyRef<'_, Self>) -> PyResult<()> {
            println!("begin!");
            let super_: &CameraRs = self_.as_ref();
            // 获取父类
            Python::with_gil(|py| -> PyResult<()> {
                let view = super_.window.getattr(py, intern!(py, "view"))?;
                // 获取存储的 view
                let x: f64 = super_.window.getattr(py, intern!(py, "width"))?.extract(py)?;
                let y: f64 = super_.window.getattr(py, intern!(py, "height"))?.extract(py)?;
                let x: f64 = x / 2.0 / super_.zoom + (super_.dx / super_.zoom);
                let y: f64 = y / 2.0 / super_.zoom + (super_.dy / super_.zoom);
                // 计算中心点

                // view.call_method1(py, "translate", (x, y))?;
                // view.call_method1(py, "scale", (super_.zoom, super_.zoom))?;

                let args = ((x * super_.zoom, y * super_.zoom, 0),);
                let view_matrix = view.call_method1(py, intern!(py, "translate"), args)?;
                // view_matrix = self.view.translate((x * zoom, y * zoom, 0))

                let args = ((super_.zoom, super_.zoom, 1),);
                let view_matrix = view_matrix.call_method1(py, intern!(py, "scale"), args)?;
                // view_matrix = view_matrix.scale((zoom, zoom, 1))

                super_.window.setattr(py, intern!(py, "view"), view_matrix)?;
                // self.view = view_matrix
                Ok(())
            })?;
            Ok(())
        }
    }

    #[pymethods]
    impl CameraRs {
        #[new]
        #[pyo3(signature = (window, zoom=1.0, dx=1.0, dy=1.0, min_zoom=1.0, max_zoom=1.0))]
        pub fn py_new(window: &PyAny, zoom: f64, dx: f64, dy: f64, min_zoom: f64, max_zoom: f64) -> PyResult<Self> {
            return Ok(CameraRs {
                dx,
                dy,
                zoom,
                min_zoom,
                max_zoom,
                window: window.into(),
            });
        }

        pub fn get_view(&self) -> PyResult<PyObject> {
            Ok(Python::with_gil(|py| -> PyResult<PyObject> {
                Ok(self.window.getattr(py, intern!(py, "view"))?)
            })?)
        }

        #[getter]
        pub fn get_position(&self) -> (f64, f64) { return (self.dx, self.dy); }

        #[setter]
        pub fn set_position(&mut self, value: (f64, f64)) -> () {
            self.dx = value.0;
            self.dy = value.1;
        }

        #[getter]
        pub fn get_zoom(&self) -> PyResult<f64> { Ok(self.zoom) }

        #[setter]
        pub fn set_zoom(&mut self, value: f64) -> PyResult<()> {
            self.zoom = value.min(self.max_zoom).max(self.min_zoom);
            Ok(())
        }

        pub fn begin(&self) -> PyResult<()> {
            Python::with_gil(|py| -> PyResult<()> {
                let view = self.window.getattr(py, intern!(py, "view"))?;

                let x: f64 = self.window.getattr(py, intern!(py, "width"))?.extract(py)?;
                let y: f64 = self.window.getattr(py, intern!(py, "height"))?.extract(py)?;
                let x: f64 = x / 2.0 / self.zoom + (self.dx / self.zoom);
                let y: f64 = y / 2.0 / self.zoom + (self.dy / self.zoom);
                // use to get center of the screen

                let args = ((x * self.zoom, y * self.zoom, 0),);
                let view_matrix = view.call_method1(py, intern!(py, "translate"), args)?;
                // view_matrix = self.view.translate((x * zoom, y * zoom, 0))

                let args = ((self.zoom, self.zoom, 1),);
                let view_matrix = view_matrix.call_method1(py, intern!(py, "scale"), args)?;
                // view_matrix = view_matrix.scale((zoom, zoom, 1))

                self.window.setattr(py, intern!(py, "view"), view_matrix)?;
                // self.view = view_matrix
                Ok(())
            })?;
            return Ok(());
        }

        pub fn end(&self) -> PyResult<()> {
            Python::with_gil(|py| -> PyResult<()> {
                let view = self.window.getattr(py, intern!(py, "view"))?;

                let x: f64 = self.window.getattr(py, intern!(py, "width"))?.extract(py)?;
                let y: f64 = self.window.getattr(py, intern!(py, "height"))?.extract(py)?;
                let x: f64 = x / 2.0 / self.zoom + (self.dx / self.zoom);
                let y: f64 = y / 2.0 / self.zoom + (self.dy / self.zoom);

                let args = ((1.0 / self.zoom, 1.0 / self.zoom, 1),);
                let view_matrix = view.call_method1(py, intern!(py, "scale"), args)?;

                let args = ((-x * self.zoom, -y * self.zoom, 0),);
                let view_matrix = view_matrix.call_method1(py, intern!(py, "translate"), args)?;

                self.window.setattr(py, intern!(py, "view"), view_matrix)?;
                Ok(())
            })?;
            return Ok(());
        }

        /// https://github.com/PyO3/pyo3/discussions/2931#discussioncomment-4820729 for finding this
        /// https://github.com/PyO3/pyo3/issues/1205#issuecomment-1164096251 for advice on `__enter__`
        pub fn __enter__(py_self: PyRef<Self>) -> PyResult<PyRef<Self>> {
            // println!("enter!");
            py_self.begin()?;
            Ok(py_self)
        }

        pub fn __exit__(&self, _exc_type: PyObject, _exc_value: PyObject, _traceback: PyObject) -> PyResult<()> {
            // println!("exit!");
            self.end()?;
            return Ok(());
        }
    }
}

pub mod screen {
    use pyo3::prelude::*;
    // use crate::types::sr1::SR1PartData;

    #[pyclass]
    #[pyo3(name = "PartFrame_rs")]
    pub struct PartFrame {
        pub box_size: i32,
        pub width: i64,
        pub height: i64,
        // pub frame_box: Vec<Vec<SR1PartData>>
    }

    #[pymethods]
    impl PartFrame {
        #[new]
        pub fn py_new() -> PyResult<Self> {
            Ok(PartFrame {
                box_size: 111,
                width: 111,
                height: 111,
            })
        }
    }
}
