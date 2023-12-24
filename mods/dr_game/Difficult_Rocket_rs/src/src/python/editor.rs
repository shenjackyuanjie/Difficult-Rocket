/*
 * -------------------------------
 * Difficult Rocket
 * Copyright © 2020-2023 by shenjackyuanjie 3695888@qq.com
 * All rights reserved
 * -------------------------------
 */

use nalgebra::{Matrix2, Vector2};
use pyo3::prelude::*;
use rapier2d_f64::math::Real;

use crate::IdType;

/// Id 位置 碰撞体
pub type BoundedShape = (IdType, Vector2<Real>, EditorShapeEnum);

pub enum EditorShapeEnum {
    /// 矩形
    /// 一个方向的向量 另一个方向的向量
    Cuboid(Vector2<Real>, Vector2<Real>),
    /// 三角形
    /// 一个方向的向量 另一个方向的向量
    Triangle(Vector2<Real>, Vector2<Real>),
    /// 圆
    /// 半径
    Ball(Real),
    /// 组合
    Compound(Vec<EditorShapeEnum>),
}

// #[pyclass]
pub struct EditorArea {
    /// 存储所有碰撞箱信息
    pub collision_box: Vec<BoundedShape>,
}

impl EditorArea {
    /// 添加一个碰撞箱
    pub fn add_box(&mut self, box_data: BoundedShape) {
        self.collision_box.push(box_data);
    }

    /// 删除一个碰撞箱
    pub fn remove_box_by_id(&mut self, id: IdType) -> bool {
        for (i, box_data) in self.collision_box.iter().enumerate() {
            if box_data.0 == id {
                self.collision_box.remove(i);
                return true;
            }
        }
        false
    }

    /// 检查一个点是否碰撞到任意一个碰撞箱
    pub fn check_hit(&self, point: Vector2<Real>) -> Option<IdType> {
        for box_data in self.collision_box.iter() {
            match &box_data.2 {
                // 球 直接勾股定理秒了
                EditorShapeEnum::Ball(r) => {
                    if (point - box_data.1).norm() <= *r {
                        return Some(box_data.0);
                    }
                }
                // 矩形
                // 进行一个旋转
                EditorShapeEnum::Cuboid(dir1, dir2) => {
                    // 先平移坐标系
                    let point = point - box_data.1;
                    // 求出逆矩阵
                    let inv = Matrix2::new(dir1.x, dir2.x, dir1.y, dir2.y).try_inverse().unwrap();
                    // 变换
                    let point = inv * point;
                    // 判断是否在矩形内
                    if point.x >= 0.0 && point.x <= 1.0 && point.y >= 0.0 && point.y <= 1.0 {
                        return Some(box_data.0);
                    } else {
                        continue;
                    }
                }
                // 三角形
                EditorShapeEnum::Triangle(dir1, dir2) => {
                    // 先平移坐标系
                    let point = point - box_data.1;
                    // 求出逆矩阵
                    let inv = Matrix2::new(dir1.x, dir2.x, dir1.y, dir2.y).try_inverse().unwrap();
                    // 变换
                    let point = inv * point;
                    // 判断是否在三角形内
                    if point.x >= 0.0 && point.y >= 0.0 && point.x + point.y <= 1.0 {
                        return Some(box_data.0);
                    } else {
                        continue;
                    }
                }
                EditorShapeEnum::Compound(shapes) => {
                    for shape in shapes {
                        match shape {
                            // 球 直接勾股定理秒了
                            EditorShapeEnum::Ball(r) => {
                                if (point - box_data.1).norm() <= *r {
                                    return Some(box_data.0);
                                }
                            }
                            // 矩形
                            // 进行一个旋转
                            EditorShapeEnum::Cuboid(dir1, dir2) => {
                                // 先平移坐标系
                                let point = point - box_data.1;
                                // 求出逆矩阵
                                let inv = Matrix2::new(dir1.x, dir2.x, dir1.y, dir2.y).try_inverse().unwrap();
                                // 变换
                                let point = inv * point;
                                // 判断是否在矩形内
                                if point.x >= 0.0 && point.x <= 1.0 && point.y >= 0.0 && point.y <= 1.0 {
                                    return Some(box_data.0);
                                } else {
                                    continue;
                                }
                            }
                            // 三角形
                            EditorShapeEnum::Triangle(dir1, dir2) => {
                                // 先平移坐标系
                                let point = point - box_data.1;
                                // 求出逆矩阵
                                let inv = Matrix2::new(dir1.x, dir2.x, dir1.y, dir2.y).try_inverse().unwrap();
                                // 变换
                                let point = inv * point;
                                // 判断是否在三角形内
                                if point.x >= 0.0 && point.y >= 0.0 && point.x + point.y <= 1.0 {
                                    return Some(box_data.0);
                                } else {
                                    continue;
                                }
                            }
                            EditorShapeEnum::Compound(_) => {
                                panic!("Compound in Compound");
                            }
                        }
                    }
                }
            }
        }
        None
    }
}
