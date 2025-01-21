//! 目前我有一个cpython程序
//! 使用pyglet通过OpenGL创建一个窗口
//! 其中会通过pyo3调用rust代码(也就是不需要通过手动ffi来调用)
//! 调用rust代码的步骤比较自由, 可以在 Python 侧的渲染循环开始之前调用, 也可以在渲染循环中调用
//! 甚至自定义某个阶段的回调函数, 由 Python 侧调用
//! 我想在rust部分能够直接在pyglet创建的窗口上绘制内容 要怎么做呢？
//! 请优先考虑Windows平台下的实现即可
//! 不一定拘泥与使用 OpenGL 来渲染, 也可以使用其他的渲染方式
//! 其他桌面平台如macOS/Linux的需求可以先行忽略
//! 不需要考虑 web 平台或者移动平台 的需求
//! 但是请保留移植的可能性

use std::num::NonZeroIsize;

use winit::event::WindowEvent;
use winit::platform::run_on_demand::EventLoopExtRunOnDemand;
use winit::platform::windows::EventLoopBuilderExtWindows;
use winit::window::WindowAttributes;
use winit::{application::ApplicationHandler, event_loop::EventLoop, window::Window};

use windows_sys::Win32::Foundation::HWND;
use windows_sys::Win32::System::Threading::GetCurrentProcessId;
use windows_sys::Win32::UI::WindowsAndMessaging::{EnumWindows, GetWindowThreadProcessId};

use raw_window_handle::{RawWindowHandle, Win32WindowHandle};

struct App {
    window: Option<Window>,
    parent: RawWindowHandle,
}

impl ApplicationHandler for App {
    fn resumed(&mut self, event_loop: &winit::event_loop::ActiveEventLoop) {
        // 这里需要获取现有的窗口, 毕竟是运行在一个已有窗口的 Python 程序里
        if self.window.is_none() {
            println!("Create window");
            let window_attribute = unsafe { WindowAttributes::default().with_parent_window(Some(self.parent.clone())) };
            let window = event_loop.create_window(window_attribute).unwrap();
            self.window = Some(window);
        }
    }

    fn window_event(
        &mut self,
        event_loop: &winit::event_loop::ActiveEventLoop,
        _window_id: winit::window::WindowId,
        event: winit::event::WindowEvent,
    ) {
        match event {
            WindowEvent::CloseRequested => {
                println!("Close window");
                event_loop.exit();
            }
            WindowEvent::Destroyed => {
                println!("Window destroyed");
                event_loop.exit();
            }
            WindowEvent::RedrawRequested => {
                println!("Redraw window");
                // self.ref_window().
                event_loop.exit();
            }
            WindowEvent::MouseInput { button, .. } => {
                println!("Mouse input: {:?}", button);
            }
            WindowEvent::Moved(pos) => {
                println!("Window moved: {:?}", pos);
            }
            _ => {}
        }
    }
}

impl App {
    pub fn new(handle: RawWindowHandle) -> Self {
        Self {
            window: None,
            parent: handle,
        }
    }

    pub fn ref_window(&self) -> &Window { self.window.as_ref().unwrap() }
}

unsafe extern "system" fn enum_windows_proc(hwnd: HWND, lparam: isize) -> i32 {
    let mut process_id = 0;
    GetWindowThreadProcessId(hwnd, &mut process_id);
    if process_id == GetCurrentProcessId() {
        println!("找到当前的窗口: {:?}", hwnd);
        *(lparam as *mut HWND) = hwnd;
        return 0;
    }
    1
}

fn render_thread(handler: isize) -> anyhow::Result<()> {
    let window = handler as HWND;
    let win32_handle = Win32WindowHandle::new(NonZeroIsize::new(window as isize).unwrap());
    let raw_handle = RawWindowHandle::Win32(win32_handle);

    let mut app = App::new(raw_handle);

    let event_loop = EventLoop::builder().with_any_thread(true).build()?;
    // let event_loop = EventLoop::new()?;
    event_loop.run_app(&mut app)?;

    Ok(())
}

pub fn render_main() {
    let mut window: HWND = std::ptr::null_mut();

    let result = unsafe { EnumWindows(Some(enum_windows_proc), &mut window as *mut _ as isize) };

    if result != 0 {
        println!("Find window failed");
        return;
    }
    println!("找到 pyglet 的窗口: {:?}", window);

    // let window_ptr = window as isize;

    let win32_handle = Win32WindowHandle::new(NonZeroIsize::new(window as isize).unwrap());
    let raw_handle: RawWindowHandle = RawWindowHandle::Win32(win32_handle);

    let mut app = App::new(raw_handle);

    let mut event_loop = EventLoop::new().unwrap();
    // let event_loop = EventLoop::new()?;
    // event_loop.run_app(&mut app).unwrap();

    let threaded_event_loop = event_loop.run_app_on_demand(&mut app).unwrap();

    std::thread::spawn(move || {
        // render_thread(window as isize).unwrap();
    });
}
