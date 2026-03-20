use std::collections::HashMap;
use std::io::Cursor;

use quick_xml::events::{BytesEnd, BytesStart, Event};
use quick_xml::writer::Writer;

use crate::sr1_parse::part_list::SR1PartTypeEnum;
use crate::sr1_parse::ship::{Connection, RawShip};
use crate::sr1_parse::traits::SR1ShipTrait;
use crate::sr1_parse::types::{IdType, PartsWithConnections, SR1PartData, SR1PartList, SR1Ship, SaveStatus};

impl SR1Ship {
    pub fn from_file(file_name: String, ship_name: Option<String>) -> Option<Self> {
        if !std::path::Path::new(&file_name).exists() {
            return None;
        }
        let ship = RawShip::from_file(file_name);
        match ship {
            Some(ship) => Some(ship.to_sr_ship(ship_name)),
            None => None,
        }
    }

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

    pub fn save(&self, file_name: String, save_status: &SaveStatus) -> Option<()> {
        macro_rules! option_push_attr {
            ($elem: ident, $test_block: expr, $push: expr) => {
                if $test_block {
                    $elem.push_attribute($push);
                }
            };
        }

        fn write_parts(parts: &[SR1PartData], writer: &mut Writer<Cursor<Vec<u8>>>, save_status: &SaveStatus) {
            writer.write_event(Event::Start(BytesStart::new("Parts"))).unwrap();
            for part in parts.iter() {
                let mut part_attr = BytesStart::new("Part");
                part_attr.push_attribute(("type", part.part_type_id.as_str()));
                part_attr.push_attribute(("x", part.x.to_string().as_str()));
                part_attr.push_attribute(("y", part.y.to_string().as_str()));
                part_attr.push_attribute(("id", part.id.to_string().as_str()));
                part_attr.push_attribute(("editorAngle", part.editor_angle.to_string().as_str()));
                part_attr.push_attribute(("angle", part.angle.to_string().as_str()));
                part_attr.push_attribute(("angleV", part.angle_v.to_string().as_str()));
                option_push_attr!(
                    part_attr,
                    part.flip_x && !save_status.save_default,
                    ("flippedX", (part.flip_x as i8).to_string().as_str())
                );
                option_push_attr!(
                    part_attr,
                    part.flip_y && !save_status.save_default,
                    ("flippedY", (part.flip_y as i8).to_string().as_str())
                );
                option_push_attr!(
                    part_attr,
                    part.active && !save_status.save_default,
                    ("activated", (part.active as i8).to_string().as_str())
                );
                let inner_attr: Option<BytesStart> = match part.part_type {
                    SR1PartTypeEnum::tank | SR1PartTypeEnum::engine => {
                        let mut tank_attr =
                            BytesStart::new(if part.part_type == SR1PartTypeEnum::tank { "Tank" } else { "Engine" });
                        tank_attr.push_attribute(("fuel", part.attr.fuel.unwrap().to_string().as_str()));
                        Some(tank_attr)
                    }
                    SR1PartTypeEnum::pod => {
                        writer.write_event(Event::Start(part_attr.to_owned())).unwrap();
                        let mut pod_elem = BytesStart::new("Pod");
                        pod_elem.push_attribute(("throttle", part.attr.throttle.unwrap().to_string().as_str()));
                        pod_elem.push_attribute(("name", part.attr.name.as_ref().unwrap().as_str()));
                        writer.write_event(Event::Start(pod_elem.to_owned())).unwrap();

                        let mut stage_attr = BytesStart::new("Staging");
                        stage_attr
                            .push_attribute(("currentStage", part.attr.current_stage.unwrap().to_string().as_str()));
                        match &part.attr.steps {
                            Some(steps) => {
                                writer.write_event(Event::Start(stage_attr)).unwrap();
                                for step in steps.iter() {
                                    writer.write_event(Event::Start(BytesStart::new("Step"))).unwrap();
                                    for activate in step.iter() {
                                        let mut activate_attr = BytesStart::new("Activate");
                                        activate_attr.push_attribute(("Id", activate.0.to_string().as_str()));
                                        activate_attr
                                            .push_attribute(("moved", (activate.1 as i8).to_string().as_str()));
                                        writer.write_event(Event::Empty(activate_attr)).unwrap();
                                    }
                                    writer.write_event(Event::End(BytesEnd::new("Step"))).unwrap();
                                }
                                writer.write_event(Event::End(BytesEnd::new("Staging"))).unwrap();
                            }
                            None => {
                                writer.write_event(Event::Empty(stage_attr)).unwrap();
                            }
                        }
                        writer.write_event(Event::End(BytesEnd::new("Pod"))).unwrap();
                        writer.write_event(Event::End(BytesEnd::new("Part"))).unwrap();
                        Some(pod_elem)
                    }
                    SR1PartTypeEnum::solar => {
                        part_attr.push_attribute(("extension", part.attr.extension.unwrap().to_string().as_str()));
                        None
                    }
                    SR1PartTypeEnum::parachute => {
                        part_attr.push_attribute(("chuteX", part.attr.chute_x.unwrap().to_string().as_str()));
                        part_attr.push_attribute(("chuteY", part.attr.chute_y.unwrap().to_string().as_str()));
                        part_attr.push_attribute(("chuteHeight", part.attr.chute_height.unwrap().to_string().as_str()));
                        part_attr.push_attribute(("chuteAngle", part.attr.chute_angle.unwrap().to_string().as_str()));
                        part_attr.push_attribute(("inflate", (part.attr.inflate.unwrap() as i8).to_string().as_str()));
                        part_attr.push_attribute(("inflation", part.attr.inflation.unwrap().to_string().as_str()));
                        part_attr
                            .push_attribute(("deployed", (part.attr.deployed.unwrap() as i8).to_string().as_str()));
                        part_attr.push_attribute(("rope", (part.attr.rope.unwrap() as i8).to_string().as_str()));
                        None
                    }
                    _ => None,
                };
                match inner_attr {
                    Some(inner_attr) => match part.part_type {
                        SR1PartTypeEnum::pod => {}
                        _ => {
                            writer.write_event(Event::Start(part_attr)).unwrap();
                            writer.write_event(Event::Empty(inner_attr)).unwrap();
                            writer.write_event(Event::End(BytesEnd::new("Part"))).unwrap();
                        }
                    },
                    None => {
                        writer.write_event(Event::Empty(part_attr)).unwrap();
                    }
                }
            }
            writer.write_event(Event::End(BytesEnd::new("Parts"))).unwrap();
        }

        fn write_connections(connects: &[Connection], writer: &mut Writer<Cursor<Vec<u8>>>) {
            writer.write_event(Event::Start(BytesStart::new("Connections"))).unwrap();
            for connect in connects.iter() {
                match connect {
                    Connection::Dock {
                        dock_part,
                        parent_part,
                        child_part,
                    } => {
                        let mut dock_elem = BytesStart::new("DockConnection");
                        dock_elem.push_attribute(("dockPart", dock_part.to_string().as_str()));
                        dock_elem.push_attribute(("parentPart", parent_part.to_string().as_str()));
                        dock_elem.push_attribute(("childPart", child_part.to_string().as_str()));
                        writer.write_event(Event::Empty(dock_elem)).unwrap();
                    }
                    Connection::Normal {
                        parent_attach_point,
                        child_attach_point,
                        parent_part,
                        child_part,
                    } => {
                        let mut connect_elem = BytesStart::new("Connection");
                        connect_elem.push_attribute(("parentAttachPoint", parent_attach_point.to_string().as_str()));
                        connect_elem.push_attribute(("childAttachPoint", child_attach_point.to_string().as_str()));
                        connect_elem.push_attribute(("parentPart", parent_part.to_string().as_str()));
                        connect_elem.push_attribute(("childPart", child_part.to_string().as_str()));
                        writer.write_event(Event::Empty(connect_elem)).unwrap();
                    }
                }
            }
            writer.write_event(Event::End(BytesEnd::new("Connections"))).unwrap();
        }

        fn write_disconnect(
            data: &PartsWithConnections,
            writer: &mut Writer<Cursor<Vec<u8>>>,
            save_status: &SaveStatus,
        ) {
            writer.write_event(Event::Start(BytesStart::new("DisconnectedParts"))).unwrap();
            for (parts, connects) in data.iter() {
                writer.write_event(Event::Start(BytesStart::new("DisconnectedPart"))).unwrap();
                write_parts(parts, writer, save_status);
                write_connections(connects, writer);
                writer.write_event(Event::End(BytesEnd::new("DisconnectedPart"))).unwrap();
            }
            writer.write_event(Event::End(BytesEnd::new("DisconnectedParts"))).unwrap();
        }

        fn write_data(data: &SR1Ship, save_status: &SaveStatus) -> String {
            let mut writer: Writer<Cursor<Vec<u8>>> = Writer::new(Cursor::new(Vec::new()));
            {
                let mut ship_elem = BytesStart::new("Ship");
                ship_elem.push_attribute(("version", data.version.to_string().as_str()));
                ship_elem.push_attribute(("liftedOff", (data.lift_off as i8).to_string().as_str()));
                ship_elem.push_attribute(("touchingGround", (data.touch_ground as i8).to_string().as_str()));
                writer.write_event(Event::Start(ship_elem)).unwrap();
            }
            write_parts(&data.parts, &mut writer, save_status);
            write_connections(&data.connections, &mut writer);
            write_disconnect(&data.disconnected, &mut writer, save_status);
            writer.write_event(Event::End(BytesEnd::new("Ship"))).unwrap();

            String::from_utf8(writer.into_inner().into_inner()).unwrap()
        }
        std::fs::write(file_name, write_data(self, save_status)).unwrap();
        Some(())
    }
}
