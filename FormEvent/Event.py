import webbrowser
from PySide6.QtCore import QTimer, Qt, QSize, QPoint, QRect, QUrl
from PySide6.QtGui import QIcon, QAction, QLinearGradient, QColor, QPainter
from PySide6.QtWidgets import QWidget, QMainWindow, QPushButton, QVBoxLayout, QHBoxLayout, QGraphicsBlurEffect
from PySide6.QtWidgets import QApplication, QLabel, QSystemTrayIcon, QMenu, QMessageBox
from PySide6.QtMultimedia import QAudioOutput, QMediaPlayer
import random


class Event(QWidget):
    def __init__(self, _step: int, _body: dict):
        super().__init__()
        self.step = _step
        self.body = _body
        self.set_style_form_gui()
        self.create_form_gui()

    def create_form_gui(self):

        main_layout = QVBoxLayout(self)
        self.setStyleSheet(
            "background-color: #AAAAAA; opacity: 1;")

        messages_layout = QVBoxLayout()

        Text = str(self.body["msg"])

        TextMessages = QLabel(Text)
        messages_layout.addWidget(TextMessages)

        # Устанавливаем флаги для виджета
        self.setWindowFlags(
            Qt.WindowStaysOnTopHint | Qt.CustomizeWindowHint | Qt.FramelessWindowHint | Qt.Tool)

        # Отключаем кнопки закрытия и сворачивания
        self.setWindowFlag(Qt.WindowCloseButtonHint, False)
        self.setWindowFlag(Qt.WindowMinimizeButtonHint, False)

        ###############################################
        # Получаем первый экран из списка экранов
        desktop = QApplication.screens()[0]
        screen_rect = desktop.availableGeometry()  # Получаем размеры рабочей области
        widget_size = QSize(550, 200)  # Устанавливаем размер виджета
        widget_pos = QPoint(screen_rect.width() - widget_size.width(), screen_rect.height(
        ) - (widget_size.height() * self.step))  # Вычисляем позицию виджета
        # Устанавливаем геометрию виджета
        self.setGeometry(QRect(widget_pos, widget_size))

        ###############################################
        self.setWindowTitle("Пример окна с кнопками")

        # создание кнопок
        self.open_document_button = QPushButton("Открыть договор", self)
        self.open_document_button.setStyleSheet(
            "background-color: #4285f4; color: #000000; opacity: 1;")

        self.postpone_5min_button = QPushButton("Отложить на 5 минут", self)
        self.postpone_5min_button.setStyleSheet(
            "background-color: #00ffff; color: #000000; opacity: 1;")

        self.postpone_15min_button = QPushButton("Отложить на 15 минут", self)
        self.postpone_15min_button.setStyleSheet(
            "background-color: #ff00ff; color: #000000; opacity: 1;")

        self.postpone_1hour_button = QPushButton("Отложить на 1 час", self)
        self.postpone_1hour_button.setStyleSheet(
            "background-color: #ffff00; color: #000000; opacity: 1;")

        # создание горизонтального менеджера компоновки
        h_box = QHBoxLayout()
        h_box.addWidget(self.open_document_button)
        h_box.addWidget(self.postpone_5min_button)
        h_box.addWidget(self.postpone_15min_button)
        h_box.addWidget(self.postpone_1hour_button)

        main_layout.addLayout(messages_layout)
        main_layout.addLayout(h_box)

        self.setLayout(main_layout)

        # подключение обработчиков событий
        self.open_document_button.clicked.connect(self.open_document)
        self.postpone_5min_button.clicked.connect(
            lambda: self.postpone_notification(0.1))
        self.postpone_15min_button.clicked.connect(
            lambda: self.postpone_notification(0.1))
        self.postpone_1hour_button.clicked.connect(
            lambda: self.postpone_notification(0.1))

        self.player = QMediaPlayer()
        self.audio = QAudioOutput()

    def set_style_form_gui(self):
        self.setWindowOpacity(0.9)
        blur = QGraphicsBlurEffect()
        blur.setBlurRadius(10)  # Устанавливаем радиус размытия в пикселях
        self.setGraphicsEffect(blur)

    def open_document(self):
        # Открываем браузер с договором
        webbrowser.open(
            "http://192.168.0.9:3000/document-control/signing/documents-for-signing?id=121")
        self.close()

    def play_sound(self):
        self.player.setAudioOutput(self.audio)
        self.player.setSource(QUrl.fromLocalFile("./event.mp3"))
        self.audio.setVolume(100)
        self.player.play()

    def showEvent(self, *any_kwarg):
        self.show()

    def postpone_notification(self, delay_minutes):
        self.hide()
        # Откладываем уведомление на delay_minutes минут
        QTimer.singleShot(delay_minutes * 60 * 1000, self.showEvent)
