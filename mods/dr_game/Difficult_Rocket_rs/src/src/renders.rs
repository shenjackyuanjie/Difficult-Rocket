#[cfg(windows)]
pub mod win;

use pyo3::pyfunction;

#[pyfunction]
pub fn render_hack() -> Option<crate::python::renders::WgpuRenderPy> {
    println!("render_hacking_start");
    #[cfg(windows)]
    // let render = win::render_main();
    let render = win::render_init();
    #[cfg(not(windows))]
    println!("对不起不支持非 Windows 捏");
    println!("render_hacking_end");
    render
}
