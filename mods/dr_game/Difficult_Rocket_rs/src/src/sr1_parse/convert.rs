use crate::sr1_parse::model::{SR1PartList, SR1PartType, SR1PartTypeAttr, SR1Ship};
use crate::sr1_parse::raw::part_list::{AttachPoints, Engine, Lander, RawPartList, RawPartType, Rcs, Solar, Tank};

impl SR1PartList {
    pub fn to_raw_part_list(&self) -> RawPartList {
        let mut types: Vec<RawPartType> = Vec::new();
        for part_type in self.types.iter() {
            types.insert(0, part_type.to_raw_part_type());
        }
        RawPartList::new(types)
    }
}

impl SR1PartType {
    pub fn to_raw_part_type(&self) -> RawPartType {
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

impl SR1Ship {}
