use pyo3::prelude::*;

#[pyclass]
#[pyo3(name = "WgpuRender")]
pub struct WgpuRenderPy {
    #[cfg(windows)]
    pub app: crate::renders::win::WgpuContext,
}

#[pymethods]
impl WgpuRenderPy {
    pub fn on_draw(&mut self, clear: bool) {
        #[cfg(windows)]
        self.app.on_draw(clear);
    }

    pub fn on_resize(&mut self, width: u32, height: u32) {
        #[cfg(windows)]
        self.app.on_resize(width, height);
    }
}

impl WgpuRenderPy {
    pub fn new(app: crate::renders::win::WgpuContext) -> Self { Self { app } }
}
