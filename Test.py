def get_window_id(name):
    import Xlib.display

    d = Xlib.display.Display()
    print("sdf")

    r = d.screen().root
    print("sdf")

    window_ids = r.get_full_property(
        d.intern_atom('_NET_CLIENT_LIST'), Xlib.X.AnyPropertyType
    ).value

    for window_id in window_ids:
        print(window_id)
        window = d.create_resource_object('window', window_id)
        if window.get_wm_name() == name:
            return window_id


def run_app(window_id):
    from PyQt5.QtGui import QWindow
    from PyQt5.QtWidgets import QWidget, QVBoxLayout, QApplication, QPushButton

    app = QApplication([])
    main_widget = QWidget()
    layout = QVBoxLayout(main_widget)

    window = QWindow.fromWinId(window_id)
    widget = QWidget.createWindowContainer(window)
    layout.addWidget(widget)

    button = QPushButton('Close')
    button.clicked.connect(main_widget.close)
    layout.addWidget(button)

    main_widget.show()
    app.exec_()

# pid: 15464	handle: 787978	tid: 16160	title: Logitech G HUB	exe_path: C:\Program Files\LGHUB\lghub.exe


if __name__ == '__main__':
    # window_id = get_window_id('Spotify Premium')
    # if window_id:
    run_app(262248)