use crate::sr1_parse::part_list::{RawPartList, RawPartType};
use crate::sr1_parse::ship::{Part as RawPartData, RawShip};
use crate::sr1_parse::types::{SR1PartData, SR1PartList, SR1PartType, SR1Ship};

pub trait SR1PartTypeData {
    fn to_sr_part_type(&self) -> SR1PartType;
    fn to_raw_part_type(&self) -> RawPartType;
}

pub trait SR1PartDataTrait {
    fn to_sr_part_data(&self) -> SR1PartData;
    fn to_raw_part_data(&self) -> RawPartData;
}

pub trait SR1PartListTrait {
    fn to_sr_part_list(&self, name: Option<String>) -> SR1PartList;
    #[allow(unused)]
    fn to_raw_part_list(&self) -> RawPartList;
}

pub trait SR1ShipTrait {
    fn to_sr_ship(&self, name: Option<String>) -> SR1Ship;
    #[allow(unused)]
    fn to_raw_ship(&self) -> RawShip;
}
