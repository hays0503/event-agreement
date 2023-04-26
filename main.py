import sys
from PySide6.QtCore import QTimer
from PySide6.QtGui import QIcon, QAction, QLinearGradient, QColor, QPainter
from PySide6.QtWidgets import QApplication, QSystemTrayIcon, QMenu, QMessageBox, QWidget, QMainWindow, QPushButton, QHBoxLayout, QGraphicsBlurEffect

from Server.Server import Server


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.create_tray()
        self.create_form_gui()
        self.set_style_form_gui()

        self.Server = Server(self)
        self.Server.run_tread()
        # self.Server.start_server()

    def create_form_gui(self):
        self.setGeometry(200, 200, 300, 200)
        self.setWindowTitle("Пример окна с кнопками")

        # создание кнопок
        open_document_button = QPushButton("Открыть договор", self)
        open_document_button.setStyleSheet(
            "background-color: #4285f4; color: #000000; opacity: 1;")

        postpone_5min_button = QPushButton("Отложить на 5 минут", self)
        postpone_5min_button.setStyleSheet(
            "background-color: #00ffff; color: #000000; opacity: 1;")

        postpone_15min_button = QPushButton("Отложить на 15 минут", self)
        postpone_15min_button.setStyleSheet(
            "background-color: #ff00ff; color: #000000; opacity: 1;")

        postpone_1hour_button = QPushButton("Отложить на 1 час", self)
        postpone_1hour_button.setStyleSheet(
            "background-color: #ffff00; color: #000000; opacity: 1;")

        # создание горизонтального менеджера компоновки
        h_box = QHBoxLayout()
        h_box.addWidget(open_document_button)
        h_box.addWidget(postpone_5min_button)
        h_box.addWidget(postpone_15min_button)
        h_box.addWidget(postpone_1hour_button)
        self.setLayout(h_box)

        # подключение обработчиков событий
        open_document_button.clicked.connect(self.open_document)
        postpone_5min_button.clicked.connect(
            lambda: self.postpone_notification(5))
        postpone_15min_button.clicked.connect(
            lambda: self.postpone_notification(15))
        postpone_1hour_button.clicked.connect(
            lambda: self.postpone_notification(60))

    def set_style_form_gui(self):
        self.setWindowOpacity(0.8)
        blur = QGraphicsBlurEffect()
        blur.setBlurRadius(10)  # Устанавливаем радиус размытия в пикселях
        self.setGraphicsEffect(blur)

    def create_tray(self):
        # Отображаем иконку приложения в трее
        self.tray_icon = QSystemTrayIcon(QIcon("icon.png"), self)
        self.tray_icon.show()

        # Создаем контекстное меню
        menu = QMenu(self)

        # Создаем кнопки в меню
        show_action = QAction("Показать", self)
        exit_action = QAction("Выход", self)
        menu.addAction(show_action)
        menu.addAction(exit_action)

        # Устанавливаем контекстное меню на иконку в трее
        self.tray_icon.setContextMenu(menu)

        # При нажатии на "Показать" показываем главное окно
        show_action.triggered.connect(self.showNormal)

        # При нажатии на "Выход" закрываем приложение
        exit_action.triggered.connect(app.quit)

    def open_document(self):
        # Открываем браузер с договором
        import webbrowser
        webbrowser.open(
            "http://192.168.0.9:3000/document-control/signing/documents-for-signing?id=121")

    def postpone_notification(self, delay_minutes):
        # Откладываем уведомление на delay_minutes минут
        QTimer.singleShot(delay_minutes * 60 * 1000, lambda: QMessageBox.information(
            self, "Напоминание", f"Прошло {delay_minutes} минут"))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(False)

    window = MainWindow()
    window.setWindowTitle("Пример трей-приложения")
    # window.show()
    sys.exit(app.exec())
