use windows::{
    Win32::{
        System::Com::{CLSCTX_ALL, COINIT_APARTMENTTHREADED, COINIT_DISABLE_OLE1DDE, CoCreateInstance, CoInitializeEx},
        UI::Shell::{ITaskbarList, ITaskbarList3},
    },
    core::Interface,
};
use windows_sys::Win32::{
    Foundation::HWND,
    System::Threading::GetCurrentProcessId,
    UI::WindowsAndMessaging::{EnumWindows, GWLP_HINSTANCE, GetWindowLongPtrW, GetWindowThreadProcessId},
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

/// 返回窗口的 HWND 和 HINSTANCE
pub fn get_window_handler() -> Option<(isize, isize)> {
    let mut window: HWND = std::ptr::null_mut();

    let result = unsafe { EnumWindows(Some(enum_windows_proc), &mut window as *mut _ as isize) };

    if result != 0 {
        return None;
    }

    let h_instance = unsafe { GetWindowLongPtrW(window, GWLP_HINSTANCE) };

    Some((window as isize, h_instance))
}

/// 设置当前窗口的任务栏进度条进度
///
/// all: 全部
///
/// complete: 完成的
pub fn set_progress_value(all: u64, complete: u64) {
    // https://learn.microsoft.com/zh-cn/windows/win32/api/objbase/ne-objbase-coinit
    // https://learn.microsoft.com/zh-cn/windows/win32/api/combaseapi/nf-combaseapi-coinitializeex
    unsafe { CoInitializeEx(None, COINIT_APARTMENTTHREADED | COINIT_DISABLE_OLE1DDE).ok().expect("co init faild") };

    if let Some((handle, _)) = get_window_handler() {
        let i_taskbar: ITaskbarList3 =
            unsafe { CoCreateInstance(&ITaskbarList3::IID, None, CLSCTX_ALL).expect("faild to create ITaskBarList3") };
        if let Err(e) =
            unsafe { i_taskbar.SetProgressValue(windows::Win32::Foundation::HWND(handle as HWND), complete, all) }
        {
            println!("got error while setting progress value to {complete}/{all}: {e}");
        }
    }
}
