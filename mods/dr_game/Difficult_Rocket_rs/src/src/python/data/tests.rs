use pyo3::prelude::*;

use quick_xml::se::to_string;

use crate::sr1_parse::ship::RawShip;

#[pyfunction]
pub fn load_and_save_test(file_name: String) -> PyResult<()> {
    let ship = RawShip::from_file(file_name).unwrap();
    match to_string(&ship) {
        Ok(s) => println!("{}", s),
        Err(e) => println!("{}", e),
    }
    Ok(())
}
