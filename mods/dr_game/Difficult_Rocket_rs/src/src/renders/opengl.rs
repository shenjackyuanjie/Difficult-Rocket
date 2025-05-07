use std::ffi::{CStr, c_void};

use pyo3::{pyclass, pymethods};

#[cfg(windows)]
use windows_sys::Win32::Graphics::OpenGL;

#[pyclass]
pub struct DRglContent {
    pub gl: gl33::GlFns,
    pub width: u32,
    pub height: u32,
}

fn get_proc(name: *const u8) -> *const c_void { unsafe { OpenGL::wglGetProcAddress(name).unwrap() as *const c_void } }

impl DRglContent {
    pub fn new(width: u32, height: u32) -> Option<Self> {
        let gl_fn = unsafe { gl33::GlFns::load_from(&get_proc) }.unwrap();
        let gl_string = unsafe { CStr::from_ptr(gl_fn.GetString(gl33::GL_VERSION) as *const i8) }
            .to_str()
            .unwrap()
            .to_string();
        println!("正在初始化到一个 {gl_string}");
        #[cfg(windows)]
        unsafe {
            let gl_str = OpenGL::glGetString(OpenGL::GL_VERSION) as *const i8;
            let stringed = CStr::from_ptr(gl_str).to_str().unwrap().to_string();
            println!("windows 给的 gl: {stringed}")
        }

        Some(Self {
            gl: gl_fn,
            width,
            height,
        })
    }
}

#[pymethods]
impl DRglContent {
    pub fn on_draw(&self) {
        // https://github.com/bwasty/learn-opengl-rs/blob/master/src/_1_getting_started/_2_1_hello_triangle.rs
    }

    pub fn on_resize(&mut self, width: u32, height: u32) {
        self.width = width;
        self.height = height;
    }
}
