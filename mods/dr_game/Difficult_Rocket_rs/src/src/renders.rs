use pyo3::pyfunction;
use winit::{application::ApplicationHandler, event_loop::EventLoop, window::Window};

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

fn render_main() -> anyhow::Result<()> {
    let event_loop = EventLoop::new()?;
    let mut app = App::default();

    event_loop.run_app(&mut app);

    Ok(())
}
