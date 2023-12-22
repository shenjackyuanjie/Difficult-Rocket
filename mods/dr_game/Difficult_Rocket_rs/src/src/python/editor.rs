/*
 * -------------------------------
 * Difficult Rocket
 * Copyright © 2020-2023 by shenjackyuanjie 3695888@qq.com
 * All rights reserved
 * -------------------------------
 */


use nalgebra::Vector2;
use pyo3::prelude::*;

use crate::data_type::dr::BoxColliderEnum;

// #[pyclass]
pub struct EditorArea {
    /// 存储所有碰撞箱信息
    pub collision_box: Vec<BoxColliderEnum>,
}
