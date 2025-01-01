#[cfg(windows)]
mod win;

use pyo3::pyfunction;

#[pyfunction]
pub fn render_hack() {
    println!("render_hacking_start");
    #[cfg(windows)]
    win::render_main();
    #[cfg(not(windows))]
    println!("对不起不支持非 Windows 捏");
    println!("render_hacking_end");
}
