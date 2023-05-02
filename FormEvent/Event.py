# pylint: disable=syntax-error
from PySide6.QtCore import Signal
from PySide6.QtCore import QTimer, Qt, QSize, QPoint, QRect, QUrl
from PySide6.QtWidgets import QWidget, QPushButton, QVBoxLayout, QHBoxLayout, QGraphicsBlurEffect
from PySide6.QtWidgets import QApplication, QLabel
from PySide6.QtMultimedia import QAudioOutput, QMediaPlayer

from FormEvent.BaseWidgetEvent import BaseWidgetEvent

class Event(BaseWidgetEvent):
    def __init__(self, _body: dict):
        super().__init__(_body)
        self.body = _body
        self.set_style_form_gui()
        self.create_base_form_gui()
        self.create_form_gui(_body)

    def create_form_gui(self,_body):

        if (_body["url"] != "None"):
            self.open_document_button = QPushButton("Открыть договор", self)
            self.open_document_button.setStyleSheet(
                "background-color: #4285f4; color: #000000; opacity: 1;")
            self.button_layout.addWidget(self.open_document_button)
            self.open_document_button.clicked.connect(self.open_document)
        ###############################################

        self.postpone_5min_button = QPushButton("Отложить на 5 минут", self)
        self.postpone_5min_button.setStyleSheet(
            "background-color: #00ffff; color: #000000; opacity: 1;")

        self.postpone_15min_button = QPushButton("Отложить на 15 минут", self)
        self.postpone_15min_button.setStyleSheet(
            "background-color: #ff00ff; color: #000000; opacity: 1;")

        self.postpone_1hour_button = QPushButton("Отложить на 1 час", self)
        self.postpone_1hour_button.setStyleSheet(
            "background-color: #ffff00; color: #000000; opacity: 1;")

        self.button_layout.addWidget(self.postpone_5min_button)
        self.button_layout.addWidget(self.postpone_15min_button)
        self.button_layout.addWidget(self.postpone_1hour_button)


        # подключение обработчиков событий
        self.postpone_5min_button.clicked.connect(
            lambda: self.postpone_notification(0.1))
        self.postpone_15min_button.clicked.connect(
            lambda: self.postpone_notification(0.1))
        self.postpone_1hour_button.clicked.connect(
            lambda: self.postpone_notification(0.1))

    def closeEvent(self, event):
        print("closeEvent")
        self.play_sound_read()
        self.close_event.emit(self.body["id"])
        self.hide()

    def revert_close(self):
        print("revert_close")
        self.revert_hide_event.emit(self.body)

    def postpone_notification(self, delay_minutes):
        print("postpone_notification")
        self.base_event.send_msg(delay_minutes)
        # Откладываем уведомление на delay_minutes минут
        QTimer.singleShot(delay_minutes * 60 * 1000, self.revert_close)
        self.close_event.emit(self.body["id"])
        
