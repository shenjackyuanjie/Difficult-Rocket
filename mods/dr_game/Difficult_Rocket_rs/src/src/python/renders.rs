use pyo3::prelude::*;

#[pyclass]
pub struct WgpuRenderPy {
    #[cfg(windows)]
    pub app: crate::renders::win_gpu::WgpuContext,
}

#[pymethods]
impl WgpuRenderPy {
    pub fn on_draw(&mut self) {
        #[cfg(windows)]
        self.app.on_draw();
    }
}

impl WgpuRenderPy {
    pub fn new(app: crate::renders::win_gpu::WgpuContext) -> Self { Self { app } }
}
