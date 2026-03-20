use std::ops::Deref;

use crate::dr_physics::math::Point2D;
use crate::dr_physics::math::Rotate;
use crate::sr1_parse::types::{SR1PartData, SR1PartList};

pub fn radians_map_to_degrees(angle: f64) -> f64 {
    let angle_string = angle.to_string();

    match angle_string.deref() {
        "1.570796" => 270.0,
        "3.141593" => 180.0,
        "4.712389" => 90.0,
        _ => angle.to_degrees(),
    }
}

pub fn get_max_box(parts: &[SR1PartData], part_list: &SR1PartList) -> (f64, f64, f64, f64) {
    let mut max_box = (0_f64, 0_f64, 0_f64, 0_f64);
    for part in parts.iter() {
        let part_type = part_list.get_part_type(&part.part_type_id).unwrap();
        let ((x1, y1), (x2, y2)) = part_type.get_box();
        let mut p1 = Point2D::new(x1, y1);
        let mut p2 = Point2D::new(x2, y2);
        p1.rotate_radius_mut(part.angle);
        p2.rotate_radius_mut(part.angle);
        let p1 = p1
            + Point2D {
                x: part.x * 2.0,
                y: part.y * 2.0,
            };
        let p2 = p2
            + Point2D {
                x: part.x * 2.0,
                y: part.y * 2.0,
            };
        let (x1, y1, x2, y2) = (p1.x, p1.y, p2.x, p2.y);
        max_box.0 = max_box.0.min(x1).min(part.x);
        max_box.1 = max_box.1.min(y1).min(part.y);
        max_box.2 = max_box.2.max(x2).max(part.x);
        max_box.3 = max_box.3.max(y2).max(part.y);
    }

    max_box
}
