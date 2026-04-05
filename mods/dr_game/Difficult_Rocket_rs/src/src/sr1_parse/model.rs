use std::collections::HashMap;

use crate::dr_physics::math::{Edge, Shape};
use crate::sr1_parse::raw::part_list::{
    AttachPoint, Damage as RawDamage, FuelType, SR1PartTypeEnum, Shape as RawShape,
};
use crate::sr1_parse::raw::ship::{Connection, Part as RawPart};
use crate::sr1_parse::util::{get_max_box, radians_map_to_degrees};

pub type IdType = i64;
pub type PartsWithConnections = Vec<(Vec<SR1PartData>, Vec<Connection>)>;

#[derive(Debug, Copy, Clone)]
pub enum SR1PartTypeAttr {
    Tank {
        fuel: f64,
        dry_mass: f64,
        fuel_type: FuelType,
    },
    Engine {
        power: f64,
        consumption: f64,
        size: f64,
        turn: f64,
        fuel_type: FuelType,
        throttle_exponential: bool,
    },
    Rcs {
        power: f64,
        consumption: f64,
        size: f64,
    },
    Solar {
        charge_rate: f64,
    },
    Lander {
        max_angle: f64,
        min_length: f64,
        max_length: f64,
        angle_speed: f64,
        length_speed: f64,
        width: f64,
    },
}

#[derive(Debug, Copy, Clone)]
pub struct Damage {
    pub disconnect: f64,
    pub explode: f64,
    pub explosion_power: f64,
    pub explosion_size: f64,
}

impl Damage {
    pub fn as_raw_damage(&self) -> RawDamage {
        RawDamage {
            disconnect: self.disconnect,
            explode: self.explode,
            explosion_power: Some(self.explosion_power),
            explosion_size: Some(self.explosion_size),
        }
    }
}

#[derive(Debug, Clone)]
pub struct SR1PartType {
    pub id: String,
    pub name: String,
    pub description: String,
    pub sprite: String,
    pub p_type: SR1PartTypeEnum,
    pub mass: f64,
    pub width: u32,
    pub height: u32,
    pub friction: f64,
    pub category: String,
    pub ignore_editor_intersections: bool,
    pub disable_editor_rotation: bool,
    pub can_explode: bool,
    pub cover_height: u32,
    pub sandbox_only: bool,
    pub drag: f64,
    pub hidden: bool,
    pub buoyancy: f64,
    pub damage: Damage,
    pub shape: Option<Vec<RawShape>>,
    pub attach_points: Option<Vec<AttachPoint>>,
    pub attr: Option<SR1PartTypeAttr>,
}

impl SR1PartType {
    pub fn get_box(&self) -> ((f64, f64), (f64, f64)) {
        (
            (-(self.width as f64 / 2.0), -(self.height as f64 / 2.0)),
            (self.width as f64 / 2.0, self.height as f64 / 2.0),
        )
    }
}

#[derive(Debug, Clone)]
pub struct SR1PartList {
    pub types: Vec<SR1PartType>,
    pub name: String,
}

impl SR1PartList {
    pub fn new(name: String, types: Vec<SR1PartType>) -> SR1PartList { SR1PartList { types, name } }

    pub fn get_part_type(&self, type_name: &String) -> Option<&SR1PartType> {
        self.types.iter().find(|part_type| &part_type.id == type_name)
    }

    pub fn part_types_new(part_types: Vec<SR1PartType>, name: Option<String>) -> Self {
        SR1PartList::new(name.unwrap_or("NewPartList".to_string()), part_types)
    }

    pub fn insert_part(&mut self, part: SR1PartType) { self.types.insert(0, part); }

    pub fn renamed(&self, name: Option<String>) -> SR1PartList {
        if let Some(name) = name {
            let mut dupe = self.clone();
            dupe.name = name;
            dupe
        } else {
            self.clone()
        }
    }
}

#[derive(Debug, Clone)]
pub struct SR1PartData {
    pub attr: SR1PartDataAttr,
    pub x: f64,
    pub y: f64,
    pub id: IdType,
    pub angle: f64,
    pub angle_v: f64,
    pub part_type: SR1PartTypeEnum,
    pub part_type_id: String,
    pub editor_angle: i32,
    pub flip_x: bool,
    pub flip_y: bool,
    pub active: bool,
    pub explode: bool,
}

impl SR1PartData {
    pub fn get_box(&self, part_type: &SR1PartType) -> (f64, f64, f64, f64) {
        let width = part_type.width;
        let height = part_type.height;
        let radius = self.angle;
        let mut shape = Shape::new_width_height(width as f64, height as f64, Some(radius));
        shape.move_xy(Some(self.x), Some(self.y));
        let mut pos_box = (0_f64, 0_f64, 0_f64, 0_f64);
        if let Edge::OneTimeLine(line) = shape.bounds[0] {
            pos_box.0 = line.start.x;
            pos_box.1 = line.start.y;
        }
        if let Edge::OneTimeLine(line) = shape.bounds[2] {
            pos_box.2 = line.start.x;
            pos_box.3 = line.start.y;
        }
        pos_box
    }

    pub fn angle_degrees(&self) -> f64 { radians_map_to_degrees(self.angle) }

    pub fn get_corner_points(&self, part_type: &SR1PartType) -> ((f64, f64), (f64, f64)) {
        let (x1, y1, x2, y2) = self.get_box(part_type);
        ((x1 * 2.0, y1 * 2.0), (x2 * 2.0, y2 * 2.0))
    }

    pub fn to_raw_part_data(&self) -> crate::sr1_parse::raw::ship::Part {
        use crate::sr1_parse::raw::ship::{Activate, Engine as RawEngine, Part, Pod, Staging, Step, Tank as RawTank};

        let (tank, engine) = if let Some(fuel) = &self.attr.fuel {
            match self.part_type {
                SR1PartTypeEnum::tank => (Some(RawTank { fuel: fuel.to_owned() }), None),
                SR1PartTypeEnum::engine => (None, Some(RawEngine { fuel: fuel.to_owned() })),
                _ => (None, None),
            }
        } else {
            (None, None)
        };
        let pod = match (&self.attr.name, &self.attr.throttle, &self.attr.current_stage, &self.attr.steps) {
            (Some(name), Some(throttle), Some(current_stage), Some(steps)) => Some({
                let mut actives = Vec::new();
                for step in steps {
                    let mut steps = Vec::new();
                    for active in step {
                        steps.push(Activate {
                            id: active.0.to_owned(),
                            moved: active.1.to_owned() as i8,
                        });
                    }
                    actives.push(Step { activates: steps });
                }
                let stages = Staging {
                    current_stage: current_stage.to_owned(),
                    steps: actives,
                };
                Pod {
                    name: name.clone(),
                    throttle: throttle.to_owned(),
                    stages,
                }
            }),
            _ => None,
        };
        Part {
            tank,
            engine,
            pod,
            part_type_id: self.part_type_id.clone(),
            id: self.id,
            x: self.x,
            y: self.y,
            editor_angle: self.editor_angle,
            angle: self.angle,
            angle_v: self.angle_v,
            flip_x: Some(self.flip_x as i8),
            flip_y: Some(self.flip_y as i8),
            chute_x: self.attr.chute_x,
            chute_y: self.attr.chute_y,
            chute_height: self.attr.chute_height,
            extension: self.attr.extension,
            inflate: self.attr.inflate.map(|b| b as i8),
            inflation: self.attr.inflation,
            exploded: Some(self.explode as i8),
            rope: self.attr.rope.map(|b| b as i8),
            chute_angle: self.attr.chute_angle,
            activated: Some(self.active as i8),
            deployed: self.attr.deployed.map(|b| b as i8),
        }
    }
}

#[derive(Debug, Clone)]
pub struct SR1PartDataAttr {
    pub fuel: Option<f64>,
    pub name: Option<String>,
    pub throttle: Option<f64>,
    pub current_stage: Option<i32>,
    pub steps: Option<Vec<Vec<(IdType, bool)>>>,
    pub extension: Option<f64>,
    pub chute_x: Option<f64>,
    pub chute_y: Option<f64>,
    pub chute_height: Option<f64>,
    pub chute_angle: Option<f64>,
    pub inflate: Option<bool>,
    pub inflation: Option<f64>,
    pub deployed: Option<bool>,
    pub rope: Option<bool>,
    pub part_type: Option<SR1PartTypeEnum>,
}

impl SR1PartDataAttr {
    pub fn guess_type(&mut self) -> SR1PartTypeEnum {
        if let Some(part_type) = self.part_type {
            return part_type;
        }
        if self.fuel.is_some() {
            self.part_type = Some(SR1PartTypeEnum::tank);
            return SR1PartTypeEnum::tank;
        }
        if self.name.is_some() {
            self.part_type = Some(SR1PartTypeEnum::pod);
            return SR1PartTypeEnum::pod;
        }
        if self.extension.is_some() {
            self.part_type = Some(SR1PartTypeEnum::solar);
            return SR1PartTypeEnum::solar;
        }
        if self.chute_x.is_some() {
            self.part_type = Some(SR1PartTypeEnum::parachute);
        }
        SR1PartTypeEnum::strut
    }

    pub fn get_part_type(&mut self) -> SR1PartTypeEnum {
        if let Some(part_type) = self.part_type {
            return part_type;
        }
        self.guess_type()
    }

    pub unsafe fn get_part_type_none_mut(&self) -> SR1PartTypeEnum {
        let slf = self as *const Self as *mut Self;
        unsafe { (*slf).get_part_type() }
    }

    #[allow(clippy::too_many_arguments)]
    pub fn new(
        fuel: Option<f64>,
        name: Option<String>,
        throttle: Option<f64>,
        current_stage: Option<i32>,
        steps: Option<Vec<Vec<(IdType, bool)>>>,
        extension: Option<f64>,
        chute_pos: (Option<f64>, Option<f64>),
        chute_height: Option<f64>,
        chute_angle: Option<f64>,
        inflate: Option<bool>,
        inflation: Option<f64>,
        deployed: Option<bool>,
        rope: Option<bool>,
        part_type: Option<SR1PartTypeEnum>,
    ) -> Self {
        SR1PartDataAttr {
            fuel,
            name,
            throttle,
            current_stage,
            steps,
            extension,
            chute_x: chute_pos.0,
            chute_y: chute_pos.1,
            chute_height,
            chute_angle,
            inflate,
            inflation,
            deployed,
            rope,
            part_type,
        }
    }

    pub fn from_raw(raw_data: &RawPart, part_type: Option<SR1PartTypeEnum>, guess: bool) -> Self {
        let fuel = if let Some(tank) = &raw_data.tank {
            Some(tank.fuel.to_owned())
        } else {
            raw_data.engine.as_ref().map(|engine| engine.fuel.to_owned())
        };
        let (name, throttle, current_stage, steps) = if let Some(pod) = &raw_data.pod {
            (
                Some(pod.name.clone()),
                Some(pod.throttle),
                Some(pod.stages.current_stage),
                Some({
                    pod.stages
                        .steps
                        .iter()
                        .map(|step| step.activates.iter().map(|act| (act.id, act.moved != 0)).collect())
                        .collect()
                }),
            )
        } else {
            (None, None, None, None)
        };
        let mut results = SR1PartDataAttr {
            fuel,
            name,
            throttle,
            current_stage,
            steps,
            extension: raw_data.extension,
            chute_x: raw_data.chute_x,
            chute_y: raw_data.chute_y,
            chute_height: raw_data.chute_height,
            chute_angle: raw_data.chute_angle,
            inflate: raw_data.inflate.map(|i| i != 0),
            inflation: raw_data.inflation,
            deployed: raw_data.deployed.map(|i| i != 0),
            rope: raw_data.rope.map(|i| i != 0),
            part_type,
        };

        if guess && results.part_type.is_none() {
            results.guess_type();
        }
        results
    }
}

#[derive(Debug, Clone)]
pub struct SR1Ship {
    pub name: String,
    pub description: String,
    pub version: i32,
    pub lift_off: bool,
    pub touch_ground: bool,
    pub parts: Vec<SR1PartData>,
    pub connections: Vec<Connection>,
    pub disconnected: Vec<(Vec<SR1PartData>, Vec<Connection>)>,
}

impl SR1Ship {
    pub fn renamed(&self, name: Option<String>) -> SR1Ship {
        if let Some(name) = name {
            let mut dupe = self.clone();
            dupe.name = name;
            dupe
        } else {
            self.clone()
        }
    }

    pub fn img_bounds(&self, part_list: &SR1PartList) -> (i64, i64, i64, i64) {
        let mut max_box = get_max_box(&self.parts, part_list);
        max_box.0 *= 60.0;
        max_box.1 *= 60.0;
        max_box.2 *= 60.0;
        max_box.3 *= 60.0;
        (max_box.0 as i64, max_box.1 as i64, max_box.2 as i64, max_box.3 as i64)
    }

    pub fn total_mass(&self, part_list: &SR1PartList) -> f64 {
        self.parts
            .iter()
            .filter_map(|part_data| part_list.get_part_type(&part_data.part_type_id).map(|part_type| part_type.mass))
            .sum()
    }

    pub fn resolved_parts(&self, part_list: &SR1PartList) -> Vec<(SR1PartType, SR1PartData)> {
        self.parts
            .iter()
            .filter_map(|part_data| {
                part_list
                    .get_part_type(&part_data.part_type_id)
                    .map(|part_type| (part_type.clone(), part_data.clone()))
            })
            .collect()
    }

    pub fn resolved_parts_by_id(&self, part_list: &SR1PartList) -> HashMap<IdType, Vec<(SR1PartType, SR1PartData)>> {
        let mut parts = HashMap::new();
        for (part_type, part_data) in self.resolved_parts(part_list) {
            parts.entry(part_data.id).or_insert_with(Vec::new).push((part_type, part_data));
        }
        parts
    }

    pub fn resolved_disconnected_parts(
        &self,
        part_list: &SR1PartList,
    ) -> Vec<(Vec<(SR1PartType, SR1PartData)>, Vec<Connection>)> {
        self.disconnected
            .iter()
            .map(|(part_group, connections)| {
                let group_parts = part_group
                    .iter()
                    .filter_map(|part_data| {
                        part_list
                            .get_part_type(&part_data.part_type_id)
                            .map(|part_type| (part_type.clone(), part_data.clone()))
                    })
                    .collect();
                (group_parts, connections.clone())
            })
            .collect()
    }

    pub fn part_box(&self, part_list: &SR1PartList, part_id: IdType) -> Option<((f64, f64), (f64, f64))> {
        self.parts.iter().find(|part_data| part_data.id == part_id).and_then(|part_data| {
            part_list
                .get_part_type(&part_data.part_type_id)
                .map(|part_type| part_data.get_corner_points(part_type))
        })
    }

    pub fn to_raw_ship(&self) -> crate::sr1_parse::raw::ship::RawShip {
        use crate::sr1_parse::raw::ship::{Connections, DisconnectedParts, Parts, RawShip};

        RawShip {
            parts: Parts::from_vec_sr1(&self.parts),
            connects: Connections::from_vec(self.connections.clone()),
            version: self.version,
            lift_off: self.lift_off as i8,
            touch_ground: self.touch_ground as i8,
            disconnected: DisconnectedParts::from_vec_sr1(self.disconnected.clone()),
        }
    }
}

#[derive(Debug, Clone, Copy)]
pub struct SaveStatus {
    pub save_default: bool,
}

impl SaveStatus {
    pub fn new(save_default: bool) -> Self { SaveStatus { save_default } }
}
