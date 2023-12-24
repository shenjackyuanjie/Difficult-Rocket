use std::io;

use fs_err as fs;

// 输入XML文件的路径。
// 若文件不存在或非XML文件，则返回错误，否则返回文件句柄。
// 我认为该函数仍可改进，因为它的实现并未达到我所预期的那样。
pub fn read_xml(path: &str) -> io::Result<fs::File> {
    if path.split_inclusive('.').collect::<Vec<&str>>()[1] != "xml" {
        Err(io::Error::new(io::ErrorKind::Other, "This file is not an XML file!"))
    } else {
        fs::File::open(path)
    }
}

pub fn parse_xml(xml_file: fs::File) {
    todo!()
}
