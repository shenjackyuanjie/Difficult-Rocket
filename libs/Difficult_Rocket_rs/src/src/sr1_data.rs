/*
 * -------------------------------
 * Difficult Rocket
 * Copyright © 2020-2023 by shenjackyuanjie 3695888@qq.com
 * All rights reserved
 * -------------------------------
 */

pub mod part_list {
    use pyo3::prelude::*;
    use serde::{Serialize, Deserialize};
    use serde_xml_rs::{to_string, from_reader};

    #[derive(Serialize, Deserialize, Clone)]
    pub struct PartList {
        #[serde(rename = "PartType")]
        part_types: Vec<PartType>
    }

    #[allow(non_camel_case_types)]
    #[derive(Serialize, Deserialize, Copy, Clone)]
    pub enum PartTypes {
        pod,
        detacher,
        wheel,
        fuselage,
        r#struct,
        tank,
        engine,
        parachute,
        nosecone,
        rcs,
        solar,
        dockconnector,
        dockport,
        lander
    }

    #[derive(Serialize, Deserialize, Copy, Clone)]
    pub enum Category {
        Satellite
    }

    #[derive(Serialize, Deserialize, Clone)]
    pub struct PartType {
        id: String,
        name: String,
        description: String,
        sprite: String,
        r#type: PartTypes,
        mass: f64,
        width: u32,
        height: u32,
        friction: Option<f64>,
        category: Option<Category>,
        #[serde(rename = "ignoreEditorIntersections")]
        ignore_editor_intersections: Option<bool>,
        #[serde(rename = "disableEditorRotation")]
        disable_editor_rotation: Option<bool>,
        #[serde(rename = "canExplode")]
        can_explode: Option<bool>,
        #[serde(rename = "coverHeight")]
        cover_height: Option<u32>,
        #[serde(rename = "sandboxOnly")]
        sandbox_only: Option<bool>,
        drag: Option<f64>,
        hidden: Option<bool>,
        buoyancy: Option<f64>
    }

}