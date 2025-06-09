// #[cfg(windows)]
// pub mod win;

pub mod opengl;

use pyo3::pyfunction;

#[pyfunction]
pub fn opengl_render(width: u32, height: u32) -> Option<opengl::DRglContent> { opengl::DRglContent::new(width, height) }

// #[pyfunction]
// pub fn render_hack() -> Option<crate::python::renders::WgpuRenderPy> {
//     println!("render_hacking_start");
//     #[cfg(windows)]
//     // let render = win::render_main();
//     let render = win::render_init();
//     #[cfg(not(windows))]
//     println!("对不起不支持非 Windows 捏");
//     println!("render_hacking_end");
//     render
// }

#[pyfunction]
pub fn set_progress_value(all: u64, complete: u64) {
    #[cfg(target_os = "windows")]
    {
        crate::platform::win::set_progress_value(all, complete);
    }
    #[cfg(not(target_os = "windows"))]
    {
        println!("非 windows 不支持设置任务栏进度条!");
    }
}
