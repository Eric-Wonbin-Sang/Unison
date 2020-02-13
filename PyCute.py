import PyQt5.QtWidgets
import PyQt5.QtCore


class Button(PyQt5.QtWidgets.QPushButton):

    def __init__(self, default_text, connect_func=None):

        super().__init__(str(default_text))

        self.default_text = default_text
        self.connect_func = connect_func

        if connect_func:
            self.clicked.connect(connect_func)


class TextBox(PyQt5.QtWidgets.QLineEdit):

    def __init__(self, text=None):

        super().__init__()

        # self.text = str(text)

        if self.text:
            self.setText(str(text))


class DropDown(PyQt5.QtWidgets.QComboBox):

    def __init__(self, option_list, default_option=None):

        super().__init__()

        self.option_list = option_list
        self.default_option = default_option

        self.setup()

    def setup(self):
        for option in self.option_list:
            self.addItem(option)
        if self.default_option in self.option_list:
            self.setCurrentIndex(self.option_list.index(self.default_option))


class Label(PyQt5.QtWidgets.QLabel):

    def __init__(self, **kwargs):

        super().__init__()

        self.text = str(kwargs.get("default_text"))
        self.setText(self.text)

        if kwargs.get("align_right"):
            self.setAlignment(PyQt5.QtCore.Qt.AlignRight | PyQt5.QtCore.Qt.AlignVCenter)


def remove_from_layout(layout):
    for i in reversed(range(layout.count())):
        layout.itemAt(i).widget().setParent(None)


def get_spacer():
    return PyQt5.QtWidgets.QSpacerItem(20, 40, PyQt5.QtWidgets.QSizePolicy.Minimum,
                                       PyQt5.QtWidgets.QSizePolicy.Expanding)


def add_to_layout(parent_layout, *args):
    for arg in args:
        if type(arg) == tuple:
            parent_layout.addWidget(*arg)
        elif PyQt5.QtWidgets.QLayout in type(arg).__mro__:
            parent_layout.addLayout(arg)
        elif PyQt5.QtWidgets.QSpacerItem in type(arg).__mro__:
            parent_layout.addSpacerItem(arg)
        else:
            parent_layout.addWidget(arg)
    return parent_layout