import PyQt5.QtWidgets
import PyQt5.QtCore
import time
import ctypes

import Window

import PyCute


class MainStack(PyQt5.QtWidgets.QWidget):

    def __init__(self):

        super().__init__()

        self.setWindowTitle("Unison")

        self.program_list = [
            Window.find_window("Messenger"),
            Window.find_window("Logitech G HUB"),
            Window.find_window("Discord"),
            Window.find_window("Spotify"),
            Window.find_window("CONSOLE")
        ]

        print("---------------")

        for program in self.program_list:
            print(program)

        x = 100
        y = 100
        width = 350 * len(self.program_list)
        height = 50

        self.window_height = 750

        self.setGeometry(x, y, width, height)
        self.user32 = ctypes.WinDLL('user32', use_last_error=True)

        self.button_dict = self.get_button_dict()

        self.v_layout = PyQt5.QtWidgets.QVBoxLayout()
        self.h_layout = self.get_h_layout()
        PyCute.add_to_layout(self.v_layout, self.h_layout, PyCute.get_spacer())
        self.setLayout(self.v_layout)

        self.position_programs()

        self.show()

    def get_window_params(self):
        x = self.geometry().x()
        y = self.geometry().y() + self.frameGeometry().height() - 30
        width = self.frameGeometry().width()
        height = self.window_height

        return x, y, width, height

    def get_button_dict(self):

        def toggle_visible_programs_helper(curr_program):
            def toggle_visible_programs():
                for temp_program in self.program_list:
                    if temp_program == curr_program:
                        temp_program.maximize()

                        temp_program.set_foreground()
                        temp_program.move(*self.get_window_params())
                    else:
                        temp_program.minimize()
            return toggle_visible_programs

        button_dict = {}
        for program in self.program_list:
            if program:
                button_dict[program.name] = PyCute.Button(default_text=program.name,
                                                          connect_func=toggle_visible_programs_helper(program))
        return button_dict

    def get_h_layout(self):
        return PyCute.add_to_layout(PyQt5.QtWidgets.QHBoxLayout(), *[self.button_dict[key] for key in self.button_dict])

    def position_programs(self):
        for i, program in enumerate(self.program_list):
            if i == 0:
                program.maximize()
                program.move(*self.get_window_params())
            else:
                program.minimize()

    def moveEvent(self, e):
        for program in self.program_list:
            if program.is_visible:
                program.move(*self.get_window_params())

    def resizeEvent(self, e):
        for program in self.program_list:
            if program.is_visible:
                program.move(*self.get_window_params())

    def showEvent(self, e):
        for program in self.program_list:
            if program.is_visible:
                program.maximize()
                break

    def hideEvent(self, e):
        for program in self.program_list:
            if program.is_visible:
                program.minimize()
                program.is_visible = True
                break

    def keyPressEvent(self, e):
        if e.key() == PyQt5.QtCore.Qt.Key_Escape:
            for program in self.program_list:
                if program:
                    program.minimize()
            self.close()

    def closeEvent(self, e):
        for program in self.program_list:
            if program:
                program.minimize()
        self.close()
