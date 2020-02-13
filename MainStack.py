import PyQt5.QtWidgets
import PyQt5.QtCore
import ctypes

import Program

import PyCute


class MainStack(PyQt5.QtWidgets.QWidget):

    def __init__(self):

        super().__init__()

        self.setWindowTitle("Unison")

        x = 100
        y = 100
        width = 1000
        height = 50

        self.setGeometry(x, y, width, height)
        self.user32 = ctypes.WinDLL('user32', use_last_error=True)

        self.program_list = [
            Program.Program(name="Messenger", identifier="Messenger: Eric", user32=self.user32),
            Program.Program(name="GroupMe", identifier="GroupMe", user32=self.user32),
            Program.Program(name="KakaoTalk", identifier="KakaoTalk", user32=self.user32),
            Program.Program(name="Task Manager", identifier="Task Manager", user32=self.user32),
            Program.Program(name="Messages for web", identifier="Messages", user32=self.user32)
        ]

        self.button_dict = self.get_button_dict()
        self.h_layout = self.get_h_layout()
        self.setLayout(self.h_layout)

        self.position_programs()

        self.show()

    def get_params(self):
        x = self.geometry().x()
        y = self.geometry().y()
        width = self.frameGeometry().width()
        height = self.frameGeometry().height()

        return x, y, width, height

    def get_button_dict(self):

        def toggle_visible_programs_helper(curr_program):
            def toggle_visible_programs():
                for temp_program in self.program_list:
                    if temp_program == curr_program:
                        temp_program.move(*self.get_params())
                        temp_program.maximize()

                    else:
                        temp_program.minimize()
            return toggle_visible_programs

        button_dict = {}
        for program in self.program_list:
            button_dict[program.name] = PyCute.Button(default_text=program.name,
                                                      connect_func=toggle_visible_programs_helper(program))
        return button_dict

    def get_h_layout(self):
        return PyCute.add_to_layout(PyQt5.QtWidgets.QHBoxLayout(), *[self.button_dict[key] for key in self.button_dict])

    def position_programs(self):
        for i, program in enumerate(self.program_list):
            if i == 0:
                program.maximize()
                program.move(*self.get_params())
            else:
                program.minimize()

    def moveEvent(self, e):
        for program in self.program_list:
            program.move(*self.get_params())

    def keyPressEvent(self, e):
        if e.key() == PyQt5.QtCore.Qt.Key_Escape:
            for program in self.program_list:
                program.minimize()
            self.close()

    def closeEvent(self, e):
        for program in self.program_list:
            program.minimize()
        self.close()
