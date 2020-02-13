import os
import ctypes
from ctypes import wintypes
import win32process
import psutil


class Window:

    def __init__(self, **kwargs):

        self.user32 = kwargs.get("user32")

        self.name = kwargs.get("name")
        self.handle = kwargs.get("handle")

        self.pid = kwargs.get("pid")
        self.tid = kwargs.get("tid")
        self.title = kwargs.get("title")
        self.exe_path = kwargs.get("exe_path")

        self.is_visible = True

    def minimize(self):
        self.user32.ShowWindow(self.handle, 6)
        self.is_visible = False

    def maximize(self):
        self.user32.ShowWindow(self.handle, 9)
        self.user32.SetForegroundWindow(self.handle)
        self.bring_to_front()
        self.is_visible = True

    def bring_to_front(self):
        self.user32.BringWindowToTop(self.handle)

    def set_foreground(self):
        self.user32.SetForegroundWindow(self.handle)

    def toggle_visibility(self):
        self.maximize()
        self.minimize()
        if self.is_visible:
            self.minimize()
        else:
            self.maximize()

    def move(self, x, y, height, width):
        self.user32.MoveWindow(self.handle, x, y, height, width, True)

    def __str__(self):
        return "{}: {}\t{}: {}\t{}: {}\t{}: {}\t{}: {}".format(
            "pid", self.pid,
            "handle", self.handle,
            "tid", self.tid,
            "title", self.title,
            "exe_path", self.exe_path
        )


def get_window_list():

    WNDENUMPROC = ctypes.WINFUNCTYPE(wintypes.BOOL, wintypes.HWND, wintypes.LPARAM, )

    user32 = ctypes.WinDLL('user32', use_last_error=True)

    window_list = []
    @WNDENUMPROC
    def enum_proc(handle, lParam):
        if user32.IsWindowVisible(handle):
            pid = wintypes.DWORD()
            tid = user32.GetWindowThreadProcessId(handle, ctypes.byref(pid))
            length = user32.GetWindowTextLengthW(handle) + 1
            title = ctypes.create_unicode_buffer(length)
            user32.GetWindowTextW(handle, title, length)
            exe_path = psutil.Process(win32process.GetWindowThreadProcessId(handle)[1]).exe()
            window_list.append(Window(user32=user32, pid=pid.value, handle=handle, tid=tid,
                                      title=title.value, exe_path=exe_path))
        return True
    user32.EnumWindows(enum_proc, 0)
    return window_list


def find_window(target_name, exe_path=None):
    for window in get_window_list():
        if target_name.lower() in window.exe_path.split("\\")[-1].lower():
            window.name = target_name
            return window

    for window in get_window_list():
        if target_name.lower() in window.title.lower():
            window.name = target_name
            return window

    # if exe_path and os.path.exists(exe_path):
    #     os.startfile(exe_path)
    #
    #     for window in get_window_list():
    #         if target_name.lower() in window.title.lower():
    #             window.name = target_name
    #             return window

    return None


print(*get_window_list(), sep='\n')
