import ctypes
from ctypes import wintypes


class Window:

    def __init__(self, **kwargs):

        self.user32 = kwargs.get("user32")

        self.name = kwargs.get("name")
        self.handle = kwargs.get("handle")

        self.pid = kwargs.get("pid")
        self.tid = kwargs.get("tid")
        self.title = kwargs.get("title")

        self.is_visible = True

    def minimize(self):
        self.user32.ShowWindow(self.handle, 6)
        self.is_visible = False

    def maximize(self):
        self.user32.ShowWindow(self.handle, 9)
        self.user32.SetForegroundWindow(self.handle)
        self.is_visible = True

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
        return "{}: {}\t{}: {}\t{}: {}\t{}: {}\t".format("pid", self.pid,
                                                         "handle", self.handle,
                                                         "tid", self.tid,
                                                         "title", self.title)


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
            window_list.append(Window(user32=user32, pid=pid.value, handle=handle, tid=tid, title=title.value))
        return True
    user32.EnumWindows(enum_proc, 0)
    return window_list


def find_window(target_name):
    for window in get_window_list():
        if target_name.lower() in window.title.lower():
            window.name = target_name
            return window
    return None


# user32 = ctypes.WinDLL('user32', use_last_error=True)
#
# window_list = get_window_list(user32=user32)
#
# print(*window_list, sep='\n')
#
# print("Handles")
#
#
# print(user32.FindWindowW(None, "Discord"))
# print(user32.FindWindowW("Discord", None))
