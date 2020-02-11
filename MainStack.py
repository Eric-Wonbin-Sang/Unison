import PyQt5.QtWidgets
import ctypes

import PyCute


class Program:

    def __init__(self, **kwargs):

        self.user32 = kwargs.get("user32")

        self.name = kwargs.get("name")
        self.identifier = kwargs.get("identifier")
        self.handle = self.user32.FindWindowW(None, self.identifier)

        self.is_visible = True

    def minimize(self):
        self.user32.ShowWindow(self.handle, 6)
        self.is_visible = False

    def maximize(self):
        self.user32.ShowWindow(self.handle, 9)
        self.is_visible = True

    def toggle_visibility(self):
        if self.is_visible:
            self.minimize()
        else:
            self.maximize()
        self.is_visible = not self.is_visible

    def move(self, x, y, height, width):
        self.user32.MoveWindow(self.handle, x, y, height, width, True)


class MainStack(PyQt5.QtWidgets.QWidget):

    def __init__(self):

        super().__init__()

        self.setWindowTitle("Stats Software")
        self.setGeometry(100, 100, 700, 50)

        self.user32 = ctypes.WinDLL('user32', use_last_error=True)

        self.program_list = [
            # Program(name="Messenger", identifier="Messenger: Eric", user32=self.user32),
            # Program(name="GroupMe", identifier="GroupMe", user32=self.user32),
            # Program(name="KakaoTalk", identifier="KakaoTalk", user32=self.user32),
            Program(name="Task Manager", identifier="Task Manager", user32=self.user32)
        ]

        self.button_dict = self.get_button_dict()

        self.h_layout = PyQt5.QtWidgets.QHBoxLayout()

        PyCute.add_to_layout(self.h_layout, *[self.button_dict[key] for key in self.button_dict])

        self.setLayout(self.h_layout)

        self.position_programs()

        self.show()

    def get_button_dict(self):
        button_dict = {}
        for program in self.program_list:
            button_dict[program.name] = PyCute.Button(default_text=program.name, connect_func=program.toggle_visibility)
        return button_dict

    def position_programs(self):

        x = self.geometry().x()
        y = self.geometry().y() + self.frameGeometry().height()
        height = 500
        width = self.frameGeometry().width()

        for program in self.program_list:
            program.move(x, y, height, width)
            program.maximize()
