use std::io::Write;

use pyo3::prelude::*;

#[pyclass]
#[pyo3(name = "Console_rs")]
pub struct PyConsole {
    /// 向子线程发送结束信号
    pub stop_sender: Option<std::sync::mpsc::Sender<()>>,
    pub keyboard_input_receiver: Option<std::sync::mpsc::Receiver<String>>,
}

#[pymethods]
impl PyConsole {
    #[new]
    fn new() -> Self {
        Self {
            stop_sender: None,
            keyboard_input_receiver: None,
        }
    }

    fn start(&mut self) {
        let (stop_sender, stop_receiver) = std::sync::mpsc::channel();
        let (keyboard_input_sender, keyboard_input_receiver) = std::sync::mpsc::channel();
        std::thread::spawn(move || {
            let std_in = std::io::stdin();
            loop {
                if let Ok(()) = stop_receiver.try_recv() {
                    break;
                }
                let mut input = String::new();
                let _ = std_in.read_line(&mut input);
                if !input.is_empty() {
                    // 预处理
                    input = input.trim().to_string();
                    keyboard_input_sender.send(input).unwrap();
                }
            }
        });
        print!("rs>");
        std::io::stdout().flush().unwrap();
        self.stop_sender = Some(stop_sender);
        self.keyboard_input_receiver = Some(keyboard_input_receiver);
    }

    fn stop(&self) -> bool {
        if let Some(sender) = &self.stop_sender {
            sender.send(()).unwrap();
            return true;
        }
        false
    }

    fn new_command(&self) -> bool {
        print!("rs>");
        std::io::stdout().flush().unwrap();
        true
    }

    fn get_command(&self) -> Option<String> {
        // 获取输入
        if let Some(receiver) = &self.keyboard_input_receiver {
            if let Ok(string) = receiver.try_recv() {
                return Some(string);
            }
        }
        None
    }
}
