use std::collections::HashMap;
use std::io::Cursor;

use anyhow::Result;
use quick_xml::events::{BytesEnd, BytesStart, Event};
use quick_xml::writer::Writer;

use crate::sr1_parse::model::{IdType, PartsWithConnections, SR1PartData, SR1PartList, SR1Ship, SaveStatus};
use crate::sr1_parse::raw::part_list::{RawPartList, SR1PartTypeEnum};
use crate::sr1_parse::raw::ship::{Connection, RawShip};

type XmlWriter = Writer<Cursor<Vec<u8>>>;

fn bool_i8_string(value: bool) -> String { (value as i8).to_string() }

fn push_attr_owned(elem: &mut BytesStart<'_>, key: &'static str, value: String) {
    elem.push_attribute((key, value.as_str()));
}

fn write_start(writer: &mut XmlWriter, tag: &str) { writer.write_event(Event::Start(BytesStart::new(tag))).unwrap(); }

fn write_end(writer: &mut XmlWriter, tag: &str) { writer.write_event(Event::End(BytesEnd::new(tag))).unwrap(); }

fn write_empty(writer: &mut XmlWriter, elem: BytesStart<'_>) { writer.write_event(Event::Empty(elem)).unwrap(); }

fn build_part_start(part: &SR1PartData, save_status: &SaveStatus) -> BytesStart<'static> {
    let mut part_attr = BytesStart::new("Part");
    part_attr.push_attribute(("type", part.part_type_id.as_str()));
    push_attr_owned(&mut part_attr, "x", part.x.to_string());
    push_attr_owned(&mut part_attr, "y", part.y.to_string());
    push_attr_owned(&mut part_attr, "id", part.id.to_string());
    push_attr_owned(&mut part_attr, "editorAngle", part.editor_angle.to_string());
    push_attr_owned(&mut part_attr, "angle", part.angle.to_string());
    push_attr_owned(&mut part_attr, "angleV", part.angle_v.to_string());

    if part.flip_x && !save_status.save_default {
        push_attr_owned(&mut part_attr, "flippedX", bool_i8_string(part.flip_x));
    }
    if part.flip_y && !save_status.save_default {
        push_attr_owned(&mut part_attr, "flippedY", bool_i8_string(part.flip_y));
    }
    if part.active && !save_status.save_default {
        push_attr_owned(&mut part_attr, "activated", bool_i8_string(part.active));
    }

    part_attr
}

fn build_fuel_element(part: &SR1PartData) -> BytesStart<'static> {
    let tag = if part.part_type == SR1PartTypeEnum::tank {
        "Tank"
    } else {
        "Engine"
    };
    let mut elem = BytesStart::new(tag);
    push_attr_owned(&mut elem, "fuel", part.attr.fuel.unwrap().to_string());
    elem
}

fn build_stage_element(part: &SR1PartData) -> BytesStart<'static> {
    let mut stage_attr = BytesStart::new("Staging");
    push_attr_owned(&mut stage_attr, "currentStage", part.attr.current_stage.unwrap().to_string());
    stage_attr
}

fn build_activate_element(activate: &(IdType, bool)) -> BytesStart<'static> {
    let mut activate_attr = BytesStart::new("Activate");
    push_attr_owned(&mut activate_attr, "Id", activate.0.to_string());
    push_attr_owned(&mut activate_attr, "moved", bool_i8_string(activate.1));
    activate_attr
}

fn write_pod_part(writer: &mut XmlWriter, part_attr: BytesStart<'static>, part: &SR1PartData) {
    writer.write_event(Event::Start(part_attr.to_owned())).unwrap();

    let mut pod_elem = BytesStart::new("Pod");
    push_attr_owned(&mut pod_elem, "throttle", part.attr.throttle.unwrap().to_string());
    pod_elem.push_attribute(("name", part.attr.name.as_ref().unwrap().as_str()));
    writer.write_event(Event::Start(pod_elem)).unwrap();

    let stage_attr = build_stage_element(part);
    match &part.attr.steps {
        Some(steps) => {
            writer.write_event(Event::Start(stage_attr)).unwrap();
            for step in steps.iter() {
                write_start(writer, "Step");
                for activate in step.iter() {
                    write_empty(writer, build_activate_element(activate));
                }
                write_end(writer, "Step");
            }
            write_end(writer, "Staging");
        }
        None => write_empty(writer, stage_attr),
    }

    write_end(writer, "Pod");
    write_end(writer, "Part");
}

fn write_solar_attrs(part_attr: &mut BytesStart<'static>, part: &SR1PartData) {
    push_attr_owned(part_attr, "extension", part.attr.extension.unwrap().to_string());
}

fn write_parachute_attrs(part_attr: &mut BytesStart<'static>, part: &SR1PartData) {
    push_attr_owned(part_attr, "chuteX", part.attr.chute_x.unwrap().to_string());
    push_attr_owned(part_attr, "chuteY", part.attr.chute_y.unwrap().to_string());
    push_attr_owned(part_attr, "chuteHeight", part.attr.chute_height.unwrap().to_string());
    push_attr_owned(part_attr, "chuteAngle", part.attr.chute_angle.unwrap().to_string());
    push_attr_owned(part_attr, "inflate", bool_i8_string(part.attr.inflate.unwrap()));
    push_attr_owned(part_attr, "inflation", part.attr.inflation.unwrap().to_string());
    push_attr_owned(part_attr, "deployed", bool_i8_string(part.attr.deployed.unwrap()));
    push_attr_owned(part_attr, "rope", bool_i8_string(part.attr.rope.unwrap()));
}

fn write_part(writer: &mut XmlWriter, part: &SR1PartData, save_status: &SaveStatus) {
    let mut part_attr = build_part_start(part, save_status);

    match part.part_type {
        SR1PartTypeEnum::tank | SR1PartTypeEnum::engine => {
            let inner = build_fuel_element(part);
            writer.write_event(Event::Start(part_attr)).unwrap();
            write_empty(writer, inner);
            write_end(writer, "Part");
        }
        SR1PartTypeEnum::pod => write_pod_part(writer, part_attr, part),
        SR1PartTypeEnum::solar => {
            write_solar_attrs(&mut part_attr, part);
            write_empty(writer, part_attr);
        }
        SR1PartTypeEnum::parachute => {
            write_parachute_attrs(&mut part_attr, part);
            write_empty(writer, part_attr);
        }
        _ => write_empty(writer, part_attr),
    }
}

fn write_parts(writer: &mut XmlWriter, parts: &[SR1PartData], save_status: &SaveStatus) {
    write_start(writer, "Parts");
    for part in parts.iter() {
        write_part(writer, part, save_status);
    }
    write_end(writer, "Parts");
}

fn write_connection(writer: &mut XmlWriter, connect: &Connection) {
    match connect {
        Connection::Dock {
            dock_part,
            parent_part,
            child_part,
        } => {
            let mut dock_elem = BytesStart::new("DockConnection");
            push_attr_owned(&mut dock_elem, "dockPart", dock_part.to_string());
            push_attr_owned(&mut dock_elem, "parentPart", parent_part.to_string());
            push_attr_owned(&mut dock_elem, "childPart", child_part.to_string());
            write_empty(writer, dock_elem);
        }
        Connection::Normal {
            parent_attach_point,
            child_attach_point,
            parent_part,
            child_part,
        } => {
            let mut connect_elem = BytesStart::new("Connection");
            push_attr_owned(&mut connect_elem, "parentAttachPoint", parent_attach_point.to_string());
            push_attr_owned(&mut connect_elem, "childAttachPoint", child_attach_point.to_string());
            push_attr_owned(&mut connect_elem, "parentPart", parent_part.to_string());
            push_attr_owned(&mut connect_elem, "childPart", child_part.to_string());
            write_empty(writer, connect_elem);
        }
    }
}

fn write_connections(writer: &mut XmlWriter, connects: &[Connection]) {
    write_start(writer, "Connections");
    for connect in connects.iter() {
        write_connection(writer, connect);
    }
    write_end(writer, "Connections");
}

fn write_disconnected_parts(writer: &mut XmlWriter, data: &PartsWithConnections, save_status: &SaveStatus) {
    write_start(writer, "DisconnectedParts");
    for (parts, connects) in data.iter() {
        write_start(writer, "DisconnectedPart");
        write_parts(writer, parts, save_status);
        write_connections(writer, connects);
        write_end(writer, "DisconnectedPart");
    }
    write_end(writer, "DisconnectedParts");
}

fn write_ship_xml(data: &SR1Ship, save_status: &SaveStatus) -> String {
    let mut writer: XmlWriter = Writer::new(Cursor::new(Vec::new()));

    let mut ship_elem = BytesStart::new("Ship");
    push_attr_owned(&mut ship_elem, "version", data.version.to_string());
    push_attr_owned(&mut ship_elem, "liftedOff", bool_i8_string(data.lift_off));
    push_attr_owned(&mut ship_elem, "touchingGround", bool_i8_string(data.touch_ground));
    writer.write_event(Event::Start(ship_elem)).unwrap();

    write_parts(&mut writer, &data.parts, save_status);
    write_connections(&mut writer, &data.connections);
    write_disconnected_parts(&mut writer, &data.disconnected, save_status);
    write_end(&mut writer, "Ship");

    String::from_utf8(writer.into_inner().into_inner()).unwrap()
}

pub fn load_part_list_from_file(file_name: String) -> Result<SR1PartList> {
    let raw_list = RawPartList::from_file(file_name)?;
    Ok(raw_list.to_sr_part_list(None))
}

pub fn load_ship_from_file(file_name: String, ship_name: Option<String>) -> Result<SR1Ship> {
    if !std::path::Path::new(&file_name).exists() {
        anyhow::bail!("ship file not found: {file_name}");
    }
    let ship = RawShip::from_file(file_name).ok_or_else(|| anyhow::anyhow!("failed to parse ship file"))?;
    Ok(ship.to_sr_ship(ship_name))
}

pub fn save_ship_to_file(ship: &SR1Ship, file_name: String, save_status: &SaveStatus) -> Result<()> {
    std::fs::write(file_name, write_ship_xml(ship, save_status))?;
    Ok(())
}

impl SR1Ship {
    pub fn parse_part_list_to_part(&mut self, part_list: &SR1PartList) {
        for part in self.parts.iter_mut() {
            if let Some(part_type) = part_list.get_part_type(&part.part_type_id) {
                part.part_type = part_type.p_type;
            } else {
                part.part_type = SR1PartTypeEnum::strut;
            }
        }
        self.disconnected.iter_mut().for_each(|(disconnected_parts, _)| {
            disconnected_parts.iter_mut().for_each(|part| match part_list.get_part_type(&part.part_type_id) {
                Some(part_type) => part.part_type = part_type.p_type,
                None => part.part_type = SR1PartTypeEnum::strut,
            });
        })
    }

    pub fn part_as_hashmap(&self) -> HashMap<IdType, Vec<SR1PartData>> {
        let mut result: HashMap<IdType, Vec<SR1PartData>> = HashMap::new();
        for part_data in self.parts.iter() {
            if let Some(part_vec) = result.get_mut(&part_data.id) {
                part_vec.push(part_data.clone());
            } else {
                result.insert(part_data.id, vec![part_data.clone()]);
            }
        }
        result
    }
}
