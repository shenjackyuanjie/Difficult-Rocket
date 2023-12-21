use std::io;

use fs_err as fs;

// Input the directory of the xml file.
// If file does not exsit or not the XML file, return errors or return file handle.
// I think this fuction can be improved as its implementations are not as good as what I expected.
pub fn read_xml(dir: &str) -> io::Result<fs::File> {
    if dir.split_inclusive('.').collect::<Vec<&str>>()[1] != "xml" {
        Err(io::Error::new(io::ErrorKind::Other, "This file is not an XML file!"))
    } else {
        fs::File::open(dir)
    }
}

pub fn parse_xml(xml_file: fs::File) {
    todo!()
}
