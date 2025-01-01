use pyo3::{pyfunction, PyResult, Python};
use quick_xml::{de::from_str, events::Event, Reader};

use super::part_list::RawPartList;
use super::ship::RawShip;

#[pyfunction]
#[pyo3(name = "part_list_read_test", signature = (file_name = "./assets/builtin/PartList.xml".to_string()))]
pub fn read_part_list_py(_py: Python, file_name: Option<String>) -> PyResult<()> {
    let file_name = file_name.unwrap_or("./assets/builtin/PartList.xml".to_string());
    // let _parts = RawPartList::from_file(file_name);
    // if let Some(parts) = _parts {
    //     // println!("{:?}", parts)
    //     parts.list_print();
    //     let _part_list = parts.to_sr_part_list(Some("Vanilla".to_string()));
    // }
    println!("{:?}", RawPartList::from_file(file_name));
    Ok(())
}

#[pyfunction]
#[pyo3(name = "read_ship_test")]
#[pyo3(signature = (path = "./assets/builtin/dock1.xml".to_string()))]
pub fn py_raw_ship_from_file(path: String) -> PyResult<bool> {
    let file = std::fs::read_to_string(path)?;
    let raw_ship = from_str::<RawShip>(&file);
    match raw_ship {
        Ok(ship) => {
            println!("{:?}", ship);
            Ok(true)
        }
        Err(e) => {
            println!("{:?}", e);
            Ok(false)
        }
    }
}

#[pyfunction]
#[pyo3(name = "assert_ship")]
/// 校验这玩意是不是个船
pub fn py_assert_ship(path: String) -> bool {
    let file_data = match std::fs::read_to_string(path) {
        Ok(data) => data,
        Err(e) => {
            println!("ERROR while reading file!\n{}\n----------", e);
            return false;
        }
    };
    let mut reader = Reader::from_str(&file_data);
    // 读取第一个
    loop {
        match reader.read_event() {
            Ok(Event::Start(e)) => {
                if e.name().as_ref() == b"Ship" {
                    // 再验证一下 version, liftedOff, touchingGround
                    let mut founds = (false, false, false);
                    for attr in e.attributes().flatten() {
                        match attr.key.as_ref() {
                            b"version" => {
                                founds.0 = true;
                            }
                            b"liftedOff" => {
                                founds.1 = true;
                            }
                            b"touchingGround" => {
                                founds.2 = true;
                            }
                            _ => (),
                        }
                    }
                    if !(founds.0 && founds.1 && founds.2) {
                        println!(
                            "warning: {}{}{} not found",
                            if founds.0 { "" } else { "version " },
                            if founds.1 { "" } else { "liftedOff " },
                            if founds.2 { "" } else { "touchingGround " }
                        );
                        return false;
                    } else {
                        return true;
                    }
                }
            }
            Ok(Event::Eof) => {
                println!("EOF");
                return false;
            }
            Err(e) => {
                println!("ERROR while using xml to parse the file!\n{:?}\n----------", e);
                return false;
            }
            _ => (),
        }
    }
}
