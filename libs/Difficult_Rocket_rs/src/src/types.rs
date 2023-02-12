/*
 * -------------------------------
 * Difficult Rocket
 * Copyright © 2020-2023 by shenjackyuanjie 3695888@qq.com
 * All rights reserved
 * -------------------------------
 */

#[allow(dead_code)]
pub mod sr1 {
    use std::collections::HashMap;

    pub fn map_ptype_textures(ptype: String) -> String {
        let mut value_map: HashMap<&str, &str> = HashMap::with_capacity(27 * 2);
        value_map.insert("pod-1", "Pod");
        value_map.insert("detacher-1", "DetacherVertical");
        value_map.insert("detacher-2", "DetacherRadial");
        value_map.insert("wheel-1", "Wheel");
        value_map.insert("wheel-2", "Wheel");
        value_map.insert("fuselage-1", "Fuselage");
        value_map.insert("strut-1", "Beam");
        value_map.insert("fueltank-0", "TankTiny");
        value_map.insert("fueltank-1", "TankSmall");
        value_map.insert("fueltank-2", "TankMedium");
        value_map.insert("fueltank-3", "TankLarge");
        value_map.insert("fueltank-4", "Puffy750");
        value_map.insert("fueltank-5", "SideTank");
        value_map.insert("engine-0", "EngineTiny");
        value_map.insert("engine-1", "EngineSmall");
        value_map.insert("engine-2", "EngineMedium");
        value_map.insert("engine-3", "EngineLarge");
        value_map.insert("engine-4", "SolidRocketBooster");
        value_map.insert("ion-0", "EngineIon");
        value_map.insert("parachute-1", "ParachuteCanister");
        value_map.insert("nosecone-1", "NoseCone");
        value_map.insert("rcs-1", "RcsBlock");
        value_map.insert("solar-1", "SolarPanelBase");
        value_map.insert("battery-0", "Battery");
        value_map.insert("dock-1", "DockingConnector");
        value_map.insert("port-1", "DockingPort");
        value_map.insert("lander-1", "LanderLegPreview");
        let result = value_map.get(ptype.as_str());
        match result {
            None => "Pod".to_string(),
            Some(i) => {
                let i = *i;
                i.to_string()
            }
        }
    }

    pub struct SR1PartData {
        pub x: f64,
        pub y: f64,
        pub id: i64,
        pub p_type: String,
        pub active: bool,
        pub angle: f64, // 弧度制
        pub angle_v: f64,
        pub editor_angle: usize,
        pub flip_x: bool,
        pub flip_y: bool,
        pub explode: bool,
        pub textures: String,
        pub connections: Option<Vec<(usize, usize)>>
    }
}

#[allow(dead_code)]
pub mod dr {
    pub enum PartType {
        Pod,
        Separator,
        Wheel,
        Fuselage,
        Beam,
        Engine,
        FuelTank,
        Parachute,
        Nosecone,
        SolarPanel,
        Battery,
        Dock,
        Port,
        Lander
    }

    pub struct DRPartData {
        pub x: f64,
        pub y: f64,
        pub id: i64,
        pub p_type: PartType,
        pub active: bool,
        pub angle: f64, // 角度制
        pub angle_v: f64,
        pub editor_angle: usize,
    }
}

