use pyo3::pyfunction;
use winit::{application::ApplicationHandler, event_loop::EventLoop, window::Window};

use windows_sys::Win32::Foundation::HWND;
use windows_sys::Win32::System::Threading::GetCurrentProcessId;
use windows_sys::Win32::UI::WindowsAndMessaging::{EnumWindows, GetWindowThreadProcessId};

#[pyfunction]
pub fn render_hack() {
    println!("render_hacking_start");
    render_main();
    println!("render_hacking_end");
}

#[derive(Default)]
struct App {
    window: Option<Window>,
}

impl ApplicationHandler for App {
    fn resumed(&mut self, event_loop: &winit::event_loop::ActiveEventLoop) {
        // 这里需要获取现有的窗口, 毕竟是运行在一个已有窗口的 Python 程序里
        // self.window = Some(event_loop.ge)
    }

    fn window_event(
        &mut self,
        event_loop: &winit::event_loop::ActiveEventLoop,
        window_id: winit::window::WindowId,
        event: winit::event::WindowEvent,
    ) {
    }
}

unsafe extern "system" fn enum_windows_proc(hwnd: HWND, lparam: isize) -> i32 {
    let mut process_id = 0;
    GetWindowThreadProcessId(hwnd, &mut process_id);
    if process_id == GetCurrentProcessId() {
        // 这里就是我们要找的窗口
        println!("Find window: {:?}", hwnd);
        return 0;
    }
    1
}

fn render_main() -> anyhow::Result<()> {
    unsafe {
        EnumWindows(Some(enum_windows_proc), 0);
    }

    // let event_loop = EventLoop::new()?;
    // let mut app = App::default();

    // event_loop.run_app(&mut app);

    Ok(())
}
