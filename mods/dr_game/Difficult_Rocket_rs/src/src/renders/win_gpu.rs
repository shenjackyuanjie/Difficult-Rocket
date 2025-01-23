use std::num::NonZeroIsize;

use pollster::block_on;
use raw_window_handle::{RawWindowHandle, Win32WindowHandle};
use wgpu::{Adapter, Device, Instance, InstanceDescriptor, Queue, Surface, SurfaceTargetUnsafe};

/// 定义一个结构体保存所有渲染上下文
#[derive(Debug)]
pub struct WgpuContext {
    pub surface: Surface<'static>,
    pub adapter: Adapter,
    pub device: Device,
    pub queue: Queue,
    pub config: wgpu::SurfaceConfiguration,
}

impl WgpuContext {
    pub fn new(unsafe_handle: SurfaceTargetUnsafe) -> anyhow::Result<Self> {
        let mut descripter = InstanceDescriptor::default();
        descripter.backends = wgpu::Backends::from_comma_list("vulkan,dx12");

        let instance = Instance::new(&descripter);
        let surface = unsafe { instance.create_surface_unsafe(unsafe_handle) }?;

        // 步骤2: 请求适配器（Adapter）
        let adapter = block_on(instance.request_adapter(&wgpu::RequestAdapterOptions {
            power_preference: wgpu::PowerPreference::HighPerformance,
            compatible_surface: Some(&surface),
            force_fallback_adapter: false,
        }))
        .expect("没找到合适的适配器");

        // 步骤3: 创建设备和队列（Device/Queue）
        let (device, queue) = block_on(adapter.request_device(
            &wgpu::DeviceDescriptor {
                label: Some("主设备"),
                // 如果需要特定功能（如深度缓冲），在此处声明
                required_features: wgpu::Features::empty(),
                // 根据需求调整限制（如纹理大小）
                required_limits: wgpu::Limits::downlevel_defaults(),
                memory_hints: wgpu::MemoryHints::default(),
            },
            None, // 追踪路径（Trace Path）
        ))?;

        // 步骤4: 配置Surface
        let surface_caps = surface.get_capabilities(&adapter);
        let surface_format = surface_caps.formats.iter().find(|f| f.is_srgb()).unwrap_or(&surface_caps.formats[0]);

        let height = 100;
        let width = 100;
        // let size =
        let config = wgpu::SurfaceConfiguration {
            usage: wgpu::TextureUsages::RENDER_ATTACHMENT,
            format: *surface_format,
            width,
            height,
            present_mode: wgpu::PresentMode::Fifo, // 垂直同步
            alpha_mode: surface_caps.alpha_modes[0],
            view_formats: vec![],
            desired_maximum_frame_latency: 1,
        };
        surface.configure(&device, &config);

        Ok(Self {
            surface,
            adapter,
            device,
            queue,
            config,
        })
    }

    pub fn on_resize(&mut self, width: u32, height: u32) {
        self.config.width = width;
        self.config.height = height;
        self.surface.configure(&self.device, &self.config);
    }

    fn inner_on_draw(&mut self) -> anyhow::Result<()> {
        let output = self.surface.get_current_texture()?;
        let view = output.texture.create_view(&wgpu::TextureViewDescriptor::default());
        let mut encoder = self.device.create_command_encoder(&wgpu::CommandEncoderDescriptor {
            label: Some("Render Encoder"),
        });
        {
            let _render_pass = encoder.begin_render_pass(&wgpu::RenderPassDescriptor {
                label: Some("Render Pass"),
                color_attachments: &[Some(wgpu::RenderPassColorAttachment {
                    view: &view,
                    resolve_target: None,
                    ops: wgpu::Operations {
                        load: wgpu::LoadOp::Clear(wgpu::Color {
                            r: 0.1,
                            g: 0.2,
                            b: 0.3,
                            a: 1.0,
                        }),
                        store: wgpu::StoreOp::Store,
                    },
                })],
                ..Default::default()
            });
        }
        self.queue.submit(std::iter::once(encoder.finish()));
        output.present();

        Ok(())
    }

    pub fn on_draw(&mut self) {
        match self.inner_on_draw() {
            Ok(_) => {}
            Err(e) => {
                println!("Failed to draw: {:?}", e);
            }
        }
    }
}

pub fn render_init() -> Option<crate::python::renders::WgpuRenderPy> {
    let handler = match crate::platform::win::get_window_handler() {
        Some(handler) => handler,
        None => {
            println!("找不到 pyglet 创建的窗口");
            return None;
        }
    };

    let win32_handle = Win32WindowHandle::new(NonZeroIsize::new(handler).unwrap());
    let raw_handle: RawWindowHandle = RawWindowHandle::Win32(win32_handle);
    let unsafe_handle = SurfaceTargetUnsafe::RawHandle {
        raw_window_handle: raw_handle,
        raw_display_handle: raw_window_handle::RawDisplayHandle::Windows(raw_window_handle::WindowsDisplayHandle::new()),
    };

    let content = match WgpuContext::new(unsafe_handle) {
        Ok(content) => content,
        Err(e) => {
            println!("Failed to create wgpu context: {:?}", e);
            return None;
        }
    };

    let py_warped = crate::python::renders::WgpuRenderPy::new(content);

    Some(py_warped)
}
