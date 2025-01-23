use std::num::NonZeroIsize;

use pollster::block_on;
use raw_window_handle::{RawWindowHandle, Win32WindowHandle};
use wgpu::{util::DeviceExt, Adapter, Device, Instance, InstanceDescriptor, Queue, Surface, SurfaceTargetUnsafe};

/// 定义一个结构体保存所有渲染上下文
#[derive(Debug)]
pub struct WgpuContext {
    pub surface: Surface<'static>,
    pub adapter: Adapter,
    pub device: Device,
    pub queue: Queue,
    pub config: wgpu::SurfaceConfiguration,
    pub render_pipeline: wgpu::RenderPipeline,
    pub vertex_buffer: wgpu::Buffer,
}

#[derive(Copy, Clone, Debug)]
struct Vertex {
    position: [f32; 3],
    color: [f32; 3],
}

impl Vertex {
    pub fn as_u8(&self) -> Vec<u8> {
        let mut data: Vec<u8> = Vec::with_capacity(6 * 4);
        data.extend_from_slice(&self.position.iter().map(|x| x.to_ne_bytes()).flatten().collect::<Vec<u8>>());
        data.extend_from_slice(&self.color.iter().map(|x| x.to_ne_bytes()).flatten().collect::<Vec<u8>>());
        data
    }

    pub fn extend_u8(&self, data: &mut Vec<u8>) {
        data.extend_from_slice(&self.position.iter().map(|x| x.to_ne_bytes()).flatten().collect::<Vec<u8>>());
        data.extend_from_slice(&self.color.iter().map(|x| x.to_ne_bytes()).flatten().collect::<Vec<u8>>());
    }
}

const SHADER: &str = r#"
// 顶点着色器

struct VertexInput {
    @location(0) position: vec3f,
    @location(1) color: vec3f,
};

struct VertexOutput {
    @builtin(position) clip_position: vec4f,
    @location(0) color: vec3f,
};

@vertex
fn vs_main(
    model: VertexInput,
) -> VertexOutput {
    var out: VertexOutput;
    out.color = model.color;
    out.clip_position = vec4f(model.position, 1.0);
    return out;
}

// 片元着色器

@fragment
fn fs_main(in: VertexOutput) -> @location(0) vec4f {
    return vec4f(in.color, 1.0);
}
"#;

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

        let shader = device.create_shader_module(wgpu::ShaderModuleDescriptor {
            label: Some("main shader"),
            source: wgpu::ShaderSource::Wgsl(SHADER.into()),
        });

        let render_pipline_layout = device.create_pipeline_layout(&wgpu::PipelineLayoutDescriptor {
            label: Some("Render Pipeline Layout"),
            bind_group_layouts: &[],
            push_constant_ranges: &[],
        });

        let render_pipeline = device.create_render_pipeline(&wgpu::RenderPipelineDescriptor {
            label: Some("Render Pipeline"),
            layout: Some(&render_pipline_layout),
            vertex: wgpu::VertexState {
                module: &shader,
                entry_point: Some("vs_main"),
                buffers: &[],
                compilation_options: Default::default(),
            },
            fragment: Some(wgpu::FragmentState {
                module: &shader,
                entry_point: Some("fs_main"),
                targets: &[Some(wgpu::ColorTargetState {
                    format: config.format,
                    blend: Some(wgpu::BlendState::REPLACE),
                    write_mask: wgpu::ColorWrites::ALL,
                })],
                compilation_options: Default::default(),
            }),
            primitive: wgpu::PrimitiveState {
                topology: wgpu::PrimitiveTopology::TriangleList, // 1.
                strip_index_format: None,
                front_face: wgpu::FrontFace::Ccw, // 2.
                cull_mode: Some(wgpu::Face::Back),
                // 将此设置为 Fill 以外的任何值都要需要开启 Feature::NON_FILL_POLYGON_MODE
                polygon_mode: wgpu::PolygonMode::Fill,
                // 需要开启 Features::DEPTH_CLIP_CONTROL
                unclipped_depth: false,
                // 需要开启 Features::CONSERVATIVE_RASTERIZATION
                conservative: false,
            },
            depth_stencil: None,
            multisample: wgpu::MultisampleState {
                count: 1,
                mask: !0,
                alpha_to_coverage_enabled: false,
            },
            multiview: None,
            cache: None,
        });

        let vertex_data = [
            Vertex {
                position: [-0.0868241, -0.49240386, 0.0],
                color: [0.5, 0.0, 0.5],
            },
            Vertex {
                position: [0.4131759, -0.49240386, 0.0],
                color: [0.5, 0.0, 0.5],
            },
            Vertex {
                position: [0.4131759, 0.49240386, 0.0],
                color: [0.5, 0.0, 0.5],
            },
            Vertex {
                position: [-0.0868241, -0.49240386, 0.0],
                color: [0.5, 0.0, 0.5],
            },
            Vertex {
                position: [0.4131759, 0.49240386, 0.0],
                color: [0.5, 0.0, 0.5],
            },
            Vertex {
                position: [-0.0868241, 0.49240386, 0.0],
                color: [0.5, 0.0, 0.5],
            },
        ];
        let mut data = Vec::new();
        for vertex in vertex_data.iter() {
            vertex.extend_u8(&mut data);
        }

        let vertex_buffer = device.create_buffer_init( &wgpu::util::BufferInitDescriptor {
            label: Some("Vertex Buffer"),
            contents: &data,
            usage: wgpu::BufferUsages::VERTEX,
        });

        Ok(Self {
            surface,
            adapter,
            device,
            queue,
            config,
            render_pipeline,
            vertex_buffer,
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
            // let _render_pass = encoder.begin_render_pass(&wgpu::RenderPassDescriptor {
            //     label: Some("Render Pass"),
            //     color_attachments: &[Some(wgpu::RenderPassColorAttachment {
            //         view: &view,
            //         resolve_target: None,
            //         ops: wgpu::Operations {
            //             load: wgpu::LoadOp::Clear(wgpu::Color {
            //                 r: 0.1,
            //                 g: 0.2,
            //                 b: 0.3,
            //                 a: 1.0,
            //             }),
            //             store: wgpu::StoreOp::Store,
            //         },
            //     })],
            //     ..Default::default()
            // });
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
