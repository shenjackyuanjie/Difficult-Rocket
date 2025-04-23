use windows_sys::Win32::{
    Foundation::HWND,
    System::Threading::GetCurrentProcessId,
    UI::WindowsAndMessaging::{EnumWindows, GetWindowThreadProcessId},
};

unsafe extern "system" fn enum_windows_proc(hwnd: HWND, lparam: isize) -> i32 {
    let mut process_id = 0;
    unsafe {
        GetWindowThreadProcessId(hwnd, &mut process_id);
        if process_id == GetCurrentProcessId() {
            println!("找到当前的窗口: {:?}", hwnd);
            *(lparam as *mut HWND) = hwnd;
            return 0;
        }
    }
    1
}

pub fn get_window_handler() -> Option<isize> {
    let mut window: HWND = std::ptr::null_mut();

    let result = unsafe { EnumWindows(Some(enum_windows_proc), &mut window as *mut _ as isize) };

    if result != 0 {
        return None;
    }

    Some(window as isize)
}
