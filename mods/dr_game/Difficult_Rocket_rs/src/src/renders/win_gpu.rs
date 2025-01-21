use raw_window_handle::RawWindowHandle;
use winit::window::Window;
use wgpu::{Adapter, Device, Instance, Queue, Surface, SurfaceTargetUnsafe};
use pollster::block_on;

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
    pub fn new(window_handle: &RawWindowHandle) -> anyhow::Result<Self> {
        let unsafe_handle = SurfaceTargetUnsafe::RawHandle{
            raw_window_handle: window_handle.to_owned(),
            raw_display_handle: raw_window_handle::RawDisplayHandle::Windows(raw_window_handle::WindowsDisplayHandle::new())
        };

        let instance = Instance::default();
        let surface = unsafe {
            instance.create_surface_unsafe(unsafe_handle)
        }?;

        // 步骤2: 请求适配器（Adapter）
        let adapter = block_on(
            instance.request_adapter(&wgpu::RequestAdapterOptions {
                power_preference: wgpu::PowerPreference::HighPerformance,
                compatible_surface: Some(&surface),
                force_fallback_adapter: false,
            })
        ).expect("Failed to find合适的适配器");

        // 步骤3: 创建设备和队列（Device/Queue）
        let (device, queue) = block_on(
            adapter.request_device(
                &wgpu::DeviceDescriptor {
                    label: None,
                    // 如果需要特定功能（如深度缓冲），在此处声明
                    required_features: wgpu::Features::empty(),
                    // 根据需求调整限制（如纹理大小）
                    required_limits: wgpu::Limits::downlevel_defaults(),
                    memory_hints: wgpu::MemoryHints::default(),
                },
                None, // 追踪路径（Trace Path）
            )
        )?;

        // 步骤4: 配置Surface
        let surface_caps = surface.get_capabilities(&adapter);
        let surface_format = surface_caps.formats.iter()
            .find(|f| f.is_srgb())
            .unwrap_or(&surface_caps.formats[0]);

        // let initial_size = window_handle.window_size();
        // let size = 
        let config = wgpu::SurfaceConfiguration {
            usage: wgpu::TextureUsages::RENDER_ATTACHMENT,
            format: *surface_format,
            width: initial_size.width,
            height: initial_size.height,
            present_mode: wgpu::PresentMode::Fifo, // 垂直同步
            alpha_mode: surface_caps.alpha_modes[0],
            view_formats: vec![],
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
}