# https://stackoverflow.com/questions/37501191/how-to-get-windows-window-names-with-ctypes-in-python

import ctypes
from ctypes import wintypes
from collections import namedtuple


def get_window_list(user32):

    WindowInfo = namedtuple('WindowInfo', 'pid tid title')

    WNDENUMPROC = ctypes.WINFUNCTYPE(wintypes.BOOL, wintypes.HWND, wintypes.LPARAM, )

    result = []
    @WNDENUMPROC
    def enum_proc(hWnd, lParam):
        if user32.IsWindowVisible(hWnd):
            pid = wintypes.DWORD()
            tid = user32.GetWindowThreadProcessId(hWnd, ctypes.byref(pid))
            length = user32.GetWindowTextLengthW(hWnd) + 1
            title = ctypes.create_unicode_buffer(length)
            user32.GetWindowTextW(hWnd, title, length)
            result.append(WindowInfo(pid.value, tid, title.value))
        return True
    user32.EnumWindows(enum_proc, 0)
    return sorted(result)


if __name__ == '__main__':

    user32 = ctypes.WinDLL('user32', use_last_error=True)

    window_list = get_window_list(user32=user32)
    window_list = [window for window in window_list if window.title != ""]

    print(*window_list, sep='\n')

    handle = user32.FindWindowW(None, 'Messenger: Eric')
