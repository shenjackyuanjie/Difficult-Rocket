use std::collections::HashMap;

use nalgebra::Vector2;
use rapier2d_f64::geometry::TriMeshFlags;
use rapier2d_f64::math::{Point, Real};
use rapier2d_f64::parry::transformation::vhacd::VHACDParameters;

#[derive(Default)]
pub enum ConnectType {
    #[default]
    Stick,
    FixedPoint,
    RotatedPoint,
}

#[derive(Default)]
pub struct Connect {
    pub c_type: ConnectType,
    pub d_pos: f64,
    pub angel: f64,
}

pub struct DRObjectProps<'a> {
    pub x: f64,
    pub y: f64,
    pub dx: f64,
    pub dy: f64,
    pub id: i64,
    pub p_type: &'a str,
    pub active: bool,
    // 角度制
    pub angle: f64,
    pub angle_v: f64,
    pub flip_x: bool,
    pub flip_y: bool,
    pub connections: Option<Vec<usize>>,
    pub box_collider_type: bool,
    pub box_collider_data: BoxColliderEnum,
}

/// 为了保证能使用到 所有类型的 碰撞体
/// 写了这么长一个玩意
/// 形状参考
/// https://rapier.rs/docs/user_guides/rust/colliders
// use rapier2d_f64::geometry::ColliderBuilder;
pub enum BoxColliderEnum {
    /// 组合
    Compound(Vec<(Vector2<Real>, BoxColliderEnum)>),
    /// 球
    /// 半径
    Ball(Real),
    /// 矩形
    /// 宽 高
    Cuboid(Real, Real),
    /// 圆角矩形
    /// 宽 高 圆角半径
    RoundCuboid(Real, Real, Real),
    /// 三角形
    /// 三个点坐标
    Triangle(Point<Real>, Point<Real>, Point<Real>),
    /// 圆角三角形
    /// 三个点坐标 圆角半径
    RoundTriangle(Point<Real>, Point<Real>, Point<Real>, Real),
    /// 圆柱体 ( 横向 )
    /// 半径 高
    CapsuleX(Real, Real),
    /// 圆柱体 ( 纵向 )
    /// 半径 高
    CapsuleY(Real, Real),
    /// 复合形状
    /// 给一堆坐标
    Segment(Point<Real>, Point<Real>),
    /// 三角形面定义的几何体（有限元？）
    /// 使用由顶点和索引缓冲区定义的三角形网格形状
    TriMesh(Vec<Point<Real>>, Vec<[u32; 3]>),
    /// 三角形面定义的几何体（有限元？），带一系列可定义的Flags
    /// 三角形网格形状由其顶点和索引缓冲区以及控制其预处理的标志定义。
    TriMeshWithFlags(Vec<Point<Real>>, Vec<[u32; 3]>, TriMeshFlags),
    /// 给定一个多边形几何体，此方法将其分解为一系列凸多边形
    ConvexDecomposition(Vec<Point<Real>>, Vec<[u32; 2]>),
    /// 给定一个圆角的多边形几何体，此方法将其分解为一系列圆角的凸多边形，虽然不知道怎么分
    RoundConvexDecomposition(Vec<Point<Real>>, Vec<[u32; 2]>, Real),
    /// 给定一个多边形几何体，此方法将其分解为一系列凸多边形
    /// 由VHACDParameters指定算法的参数，这将影响分解的结果或质量
    ConvexDecompositionWithParams(Vec<Point<Real>>, Vec<[u32; 2]>, VHACDParameters),
    /// 给定一个圆角的多边形几何体，此方法将其分解为一系列圆角的凸多边形，虽然不知道怎么分
    /// 由VHACDParameters指定算法的参数，这将影响分解的结果或质量
    RoundConvexDecompositionWithParams(Vec<Point<Real>>, Vec<[u32; 2]>, VHACDParameters, Real),
    /// 给定一系列点，计算出对应的凸包络的多边形
    ConvexHull(Vec<Point<Real>>),
    /// 给定一系列点，计算出对应的凸包络的多边形，然后加上圆角
    RoundConvexHull(Vec<Point<Real>>, Real),
    /// 给定一系列点，按照凸多边形来计算碰撞箱，但不会算出这个凸多边形
    /// 如果实际上这些点并没有定义一个凸多边形，在计算过程可能导致bug
    ConvexPolyline(Vec<Point<Real>>),
    /// 给定一系列点，按照凸多边形加上圆角来计算碰撞箱，但不会算出这个凸多边形
    /// 如果实际上这些点并没有定义一个凸多边形，在计算过程可能导致bug
    RoundConvexPolyline(Vec<Point<Real>>, Real),
    /// 由顶点定义的多边形
    Polyline(Vec<(Real, Real)>),
    /// 由一系列高度定义的某种东西，大概是地面之类的
    Heightfield(Vec<(Real, Real)>),
    // 凸分解的复合形状
    // 就是不知道能不能真用上
    // 凸分解，好像可以略微提升复杂刚体碰撞的性能
    // todo
    // convex_decomposition
}

pub struct TankProps {
    /// 油量，if p_type==tank
    pub fuel_volume: f64,
    /// 空油罐的质量，if p_type==tank
    pub mass: f64,
    /// 燃油种类，if p_type==tank
    pub fuel_type: i32,
}

pub struct EngineProps {
    /// 推力大小，if p_type==engine
    pub power: f64,
    /// 消耗速率，if p_type==engine
    pub consumption_speed: f64,
    /// 大小，if p_type==engine
    // pub size: f64,
    /// 转向范围，if p_type==engine
    pub rotation_range: f64,
    /// 燃料类型，if p_type==engine
    pub fuel_type: f64,
    // pub throttle_exponential: f64,
}

// 至少目前而言，我认为这个trait没有任何用途。
// 当它真正发挥作用是时再取消对它的注释并删除这两行注释。

// pub trait DRComponentPropAttr<'a, T> {
//     fn name() -> &'a str;
//     fn get_all_attr() -> HashMap<&'a str, T>;
// }

/// 用于描述一个零件的属性
pub struct DRComponentProps<'a, T> {
    /// 部件 ID
    pub component_id: &'a str,
    /// 是否支持自定义形状
    /// shenjack: 折磨我的时候到了
    pub shape_can_be_customized: bool,
    /// 所有 raiper2d 支持的碰撞箱类型
    pub box_collider_data: BoxColliderEnum,
    // 基本属性
    /// 名称
    pub name: &'a str,
    /// 描述
    pub description: &'a str,
    // 纹理需要用字符串而非文件句柄来表示吗？
    /// 贴图
    pub texture: &'a str,
    /// pub r#type: SR1PartTypeEnum,
    /// 质量，单位500kg
    pub mass: f64,
    /// 宽度，用于判断放置时是否回合其他零件重叠
    pub width: f64,
    /// 高度，用于判断放置时是否回合其他零件重叠
    pub height: f64,
    // 可选属性
    /// 摩擦力
    pub friction: Option<f64>,
    /// 分类
    pub category: Option<&'a str>,
    /// 是否可以爆炸
    pub can_explode: Option<bool>,
    /// 好像是影响引擎下方连接点被连接时外面那层贴图的高度，装饰作用
    pub cover_height: Option<u32>,
    /// 是否只有沙盒可用
    pub sandbox_only: Option<bool>,
    /// 减阻效果
    pub drag: Option<f64>,
    /// 是否隐藏
    pub hidden: Option<bool>,
    /// 浮力
    pub buoyancy: Option<f64>,
    // 附加属性
    pub attr: HashMap<&'a str, T>,
}
