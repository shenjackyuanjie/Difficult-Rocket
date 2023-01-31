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

    #[pyclass(name = "Camera_rs")]
    pub struct CameraRs{
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

    #[pymethods]
    impl CameraRs {
        #[new]
        #[allow(unused_variables)]
        #[pyo3(signature = (window, zoom=1.0, dx=1.0, dy=1.0,min_zoom=1.0, max_zoom=1.0))]
        pub fn py_new(window: &PyAny, zoom: f64, dx: f64, dy: f64,min_zoom: f64, max_zoom: f64) -> PyResult<Self> {
            return Ok(CameraRs {dx, dy, zoom, min_zoom, max_zoom,
                                window: window.into()})
        }

        pub fn get_view(&self) -> PyResult<PyObject> {
            Ok(Python::with_gil(|py| -> PyResult<PyObject> {
                Ok(self.window.getattr(py, intern!(py, "view"))?)
            })?)
        }

        #[getter]
        pub fn get_zoom(&self) -> PyResult<f64> {
            Ok(self.zoom)
        }

        #[setter]
        pub fn set_zoom(&mut self, value: f64) -> PyResult<()> {
            self.zoom = value.min(self.max_zoom).max(self.min_zoom);
            Ok(())
        }

        #[allow(unused_variables)]
        pub fn start(&self) -> PyResult<()> {
            let view = self.get_view()?;
            Python::with_gil(|py| -> PyResult<()> {

                Ok(())
            })?;
            return Ok(())
        }

        #[allow(unused_variables)]
        pub fn end(&self) -> PyResult<()> {
            let view = self.get_view()?;
            return Ok(())
        }

        /// https://github.com/PyO3/pyo3/discussions/2931#discussioncomment-4820729 for finding this
        /// https://github.com/PyO3/pyo3/issues/1205#issuecomment-1164096251 for advice on `__enter__`
        pub fn __enter__(py_self: PyRef<Self>) -> PyResult<PyRef<Self>> {
            // println!("enter!");
            py_self.start()?;
            Ok(py_self)
        }

        pub fn __exit__(&mut self, _exc_type: PyObject, _exc_value: PyObject, _traceback: PyObject) -> PyResult<()>{
            // println!("exit!");
            self.end()?;
            return Ok(())
        }

        
    }

}
