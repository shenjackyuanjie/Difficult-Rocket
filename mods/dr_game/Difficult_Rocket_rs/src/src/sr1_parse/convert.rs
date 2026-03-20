use crate::sr1_parse::part_list::{
    AttachPoints, Engine, Lander, RawPartList, RawPartType, Rcs, Solar, Tank, SR1PartTypeEnum,
};
use crate::sr1_parse::ship::{
    Activate as RawActivate, Connections as RawConnections, DisconnectedParts, Engine as RawEngine,
    Part as RawPartData, Parts as RawParts, Pod as RawPod, RawShip, Staging as RawStaging, Step as RawStep,
    Tank as RawTank,
};
use crate::sr1_parse::traits::{SR1PartDataTrait, SR1PartListTrait, SR1PartTypeData, SR1ShipTrait};
use crate::sr1_parse::types::{SR1PartData, SR1PartList, SR1PartType, SR1PartTypeAttr, SR1Ship};

impl SR1PartListTrait for SR1PartList {
    fn to_sr_part_list(&self, name: Option<String>) -> SR1PartList {
        if let Some(name) = name {
            let mut dupe = self.clone();
            dupe.name = name;
            dupe
        } else {
            self.clone()
        }
    }

    fn to_raw_part_list(&self) -> RawPartList {
        let mut types: Vec<RawPartType> = Vec::new();
        for part_type in self.types.iter() {
            types.insert(0, part_type.to_raw_part_type());
        }
        RawPartList::new(types)
    }
}

impl SR1PartTypeData for SR1PartType {
    fn to_sr_part_type(&self) -> SR1PartType { self.clone() }

    fn to_raw_part_type(&self) -> RawPartType {
        let tank: Option<Tank> = match &self.attr {
            Some(attr) => match attr.to_owned() {
                SR1PartTypeAttr::Tank {
                    fuel,
                    dry_mass,
                    fuel_type,
                } => Some(Tank {
                    fuel,
                    dry_mass,
                    fuel_type: Some(fuel_type),
                }),
                _ => None,
            },
            _ => None,
        };
        let engine: Option<Engine> = match &self.attr {
            Some(attr) => match attr.to_owned() {
                SR1PartTypeAttr::Engine {
                    power,
                    consumption,
                    size,
                    turn,
                    fuel_type,
                    throttle_exponential,
                } => Some(Engine {
                    power,
                    consumption,
                    throttle_exponential: Some(throttle_exponential),
                    size,
                    turn,
                    fuel_type: Some(fuel_type),
                }),
                _ => None,
            },
            _ => None,
        };
        let rcs: Option<Rcs> = match &self.attr {
            Some(attr) => match attr.to_owned() {
                SR1PartTypeAttr::Rcs {
                    power,
                    consumption,
                    size,
                } => Some(Rcs {
                    power,
                    consumption,
                    size,
                }),
                _ => None,
            },
            _ => None,
        };
        let solar: Option<Solar> = match &self.attr {
            Some(attr) => match attr.to_owned() {
                SR1PartTypeAttr::Solar { charge_rate } => Some(Solar { charge_rate }),
                _ => None,
            },
            _ => None,
        };
        let lander: Option<Lander> = match &self.attr {
            Some(attr) => match attr.to_owned() {
                SR1PartTypeAttr::Lander {
                    max_angle,
                    min_length,
                    max_length,
                    angle_speed,
                    length_speed,
                    width,
                } => Some(Lander {
                    max_angle,
                    min_length,
                    max_length,
                    angle_speed: Some(angle_speed),
                    length_speed: Some(length_speed),
                    width,
                }),
                _ => None,
            },
            _ => None,
        };
        let attach_point: Option<AttachPoints> = match &self.attach_points {
            Some(attach_points) => {
                if !attach_points.is_empty() {
                    Some(AttachPoints::new(attach_points.clone()))
                } else {
                    None
                }
            }
            _ => None,
        };
        RawPartType {
            id: self.id.clone(),
            name: self.name.clone(),
            description: self.description.clone(),
            sprite: self.sprite.clone(),
            r#type: self.p_type,
            mass: self.mass,
            width: self.width,
            height: self.height,
            friction: Some(self.friction),
            category: Some(self.category.clone()),
            ignore_editor_intersections: Some(self.ignore_editor_intersections),
            disable_editor_rotation: Some(self.disable_editor_rotation),
            can_explode: Some(self.can_explode),
            cover_height: Some(self.cover_height),
            sandbox_only: Some(self.sandbox_only),
            drag: Some(self.drag),
            hidden: Some(self.hidden),
            buoyancy: Some(self.buoyancy),
            damage: Some(self.damage.as_raw_damage()),
            tank,
            engine,
            rcs,
            solar,
            shape: self.shape.clone(),
            attach_points: attach_point,
            lander,
        }
    }
}

impl SR1PartDataTrait for SR1PartData {
    fn to_sr_part_data(&self) -> SR1PartData { self.clone() }

    fn to_raw_part_data(&self) -> RawPartData {
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
                        steps.push(RawActivate {
                            id: active.0.to_owned(),
                            moved: active.1.to_owned() as i8,
                        });
                    }
                    actives.push(RawStep { activates: steps });
                }
                let stages = RawStaging {
                    current_stage: current_stage.to_owned(),
                    steps: actives,
                };
                RawPod {
                    name: name.clone(),
                    throttle: throttle.to_owned(),
                    stages,
                }
            }),
            _ => None,
        };
        RawPartData {
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

impl SR1ShipTrait for SR1Ship {
    fn to_sr_ship(&self, name: Option<String>) -> SR1Ship {
        if let Some(name) = name {
            let mut dupe = self.clone();
            dupe.name = name;
            dupe
        } else {
            self.clone()
        }
    }

    fn to_raw_ship(&self) -> RawShip {
        RawShip {
            parts: RawParts::from_vec_sr1(&self.parts),
            connects: RawConnections::from_vec(self.connections.clone()),
            version: self.version,
            lift_off: self.lift_off as i8,
            touch_ground: self.touch_ground as i8,
            disconnected: DisconnectedParts::from_vec_sr1(self.disconnected.clone()),
        }
    }
}
