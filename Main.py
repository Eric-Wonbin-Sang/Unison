import sys
from PyQt5 import QtWidgets

import MainStack


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    gui = MainStack.MainStack()

    sys.exit(app.exec_())
