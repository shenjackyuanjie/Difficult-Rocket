/*
 * -------------------------------
 * Difficult Rocket
 * Copyright © 2020-2023 by shenjackyuanjie 3695888@qq.com
 * All rights reserved
 * -------------------------------
 */

// TODO libloading

/// https://docs.rs/libloading/latest/libloading/
/// 插件加载
///

pub mod plugin_trait {
    pub struct ModInfo {
        pub name: String,
        pub version: String
    }

    pub trait ModInfoTrait {
        fn info() -> ModInfo;
    }

}
