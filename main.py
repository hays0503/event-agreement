import os
import sys
from PySide6.QtGui import QIcon, QAction
from PySide6.QtWidgets import QApplication, QSystemTrayIcon, QMenu, QWidget, QLabel, QVBoxLayout, QInputDialog, QLineEdit
from Common.configparser import HOST, PASSWORD, PORT_SERVER, config_sound_toggle, get_sound_toggle
from Common.get_interface_ip_address import get_interface_ip_address

from Server.Server import Server


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.create_tray()
        self.create_form_gui()

        self.Server = Server(self)
        self.Server.run_tread()

    def create_form_gui(self):
        self.setGeometry(200, 200, 300, 200)
        self.setWindowTitle("Просмотр настроек")
        label_host = QLabel()
        label_port_server = QLabel()
        label_ip_server = QLabel()
        label_host.setText(f'Host(ip/address) куда отсылаем данные: {HOST}')
        label_ip_server.setText(
            f'Ip сервера куда принимаем: {get_interface_ip_address("Ethernet")}')
        label_port_server.setText(
            f'Port сервера куда принимаем: {PORT_SERVER}')

        layout = QVBoxLayout()
        layout.addWidget(label_host)
        layout.addWidget(label_ip_server)
        layout.addWidget(label_port_server)

        self.setLayout(layout)

    def create_tray(self):
        # Отображаем иконку приложения в трее
        patch = self.resource_path("./icon/icon.png")
        self.tray_icon = QSystemTrayIcon(QIcon(patch), self)
        self.tray_icon.show()

        # Создаем контекстное меню
        self.menu = QMenu(self)

        # Создаем кнопки в меню
        self.show_action = QAction("Показать", self)
        if get_sound_toggle():
            self.sound_action = QAction("[Звук выключить]", self)
        else:
            self.sound_action = QAction("[Звук включить]", self)
        self.exit_action = QAction("Выход", self)
        self.menu.addAction(self.show_action)
        self.menu.addAction(self.sound_action)
        self.menu.addAction(self.exit_action)

        # Устанавливаем контекстное меню на иконку в трее
        self.tray_icon.setContextMenu(self.menu)

        # При нажатии на "Показать" показываем главное окно
        self.show_action.triggered.connect(self.showNormal)

        self.sound_action.triggered.connect(self.sound_toggle)

        # При нажатии на "Выход" закрываем приложение
        self.exit_action.triggered.connect(self.ask_quit)

    def sound_toggle(self):
        if get_sound_toggle():
            self.sound_action.setText("[Звук включить]")
            config_sound_toggle(False)
        else:
            self.sound_action.setText("[Звук выключить]")
            config_sound_toggle(True)

    def ask_quit(self):
        password, okPressed = QInputDialog.getText(
            self, "Введите пароль", "Пароль:", QLineEdit.Password, "")
        print(PASSWORD)
        if okPressed and password == PASSWORD:
            print("Введенный пароль:", password)
            app.quit()

    def resource_path(self, relative_path):
        """ Get absolute path to resource, works for dev and for PyInstaller """
        try:
            # PyInstaller creates a temp folder and stores path in _MEIPASS
            base_path = sys._MEIPASS
        except Exception:
            base_path = os.path.abspath(".")

        return os.path.join(base_path, relative_path)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(False)

    window = MainWindow()
    # window.show()
    sys.exit(app.exec())
