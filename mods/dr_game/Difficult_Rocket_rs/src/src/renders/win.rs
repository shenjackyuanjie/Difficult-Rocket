use std::num::NonZeroIsize;

use winit::window::WindowAttributes;
use winit::{application::ApplicationHandler, event_loop::EventLoop, window::Window};

use windows_sys::Win32::Foundation::HWND;
use windows_sys::Win32::System::Threading::GetCurrentProcessId;
use windows_sys::Win32::UI::WindowsAndMessaging::{EnumWindows, GetWindowThreadProcessId};

use raw_window_handle::{RawWindowHandle, Win32WindowHandle, WinRtWindowHandle};

struct App {
    window: Option<Window>,
    parent: RawWindowHandle,
}

impl ApplicationHandler for App {
    fn resumed(&mut self, event_loop: &winit::event_loop::ActiveEventLoop) {
        // 这里需要获取现有的窗口, 毕竟是运行在一个已有窗口的 Python 程序里
        // self.window = Some(event_loop.ge)
        let mut window_attribute = unsafe { WindowAttributes::default().with_parent_window(Some(self.parent.clone())) };
    }

    fn window_event(
        &mut self,
        event_loop: &winit::event_loop::ActiveEventLoop,
        window_id: winit::window::WindowId,
        event: winit::event::WindowEvent,
    ) {
    }
}

impl App {
    pub fn new(handle: RawWindowHandle) -> Self {
        Self {
            window: None,
            parent: handle,
        }
    }
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

pub fn render_main() -> anyhow::Result<()> {
    let mut window: HWND = std::ptr::null_mut();

    let result = unsafe { EnumWindows(Some(enum_windows_proc), &mut window as *mut _ as isize) };

    if result != 0 {
        println!("Find window failed");
        return Err(anyhow::anyhow!("Find window failed"));
    }
    println!("找到 pyglet 的窗口: {:?}", window);
    let win32_handle = Win32WindowHandle::new(NonZeroIsize::new(window as isize).unwrap());
    let raw_handle = RawWindowHandle::Win32(win32_handle);
    let app = App::new(raw_handle);

    Ok(())
}
