# pylint: disable=syntax-error
from PySide6.QtCore import Signal
from PySide6.QtCore import QTimer, Qt, QSize, QPoint, QRect, QUrl
from PySide6.QtWidgets import QWidget, QPushButton, QVBoxLayout, QHBoxLayout, QGraphicsBlurEffect
from PySide6.QtWidgets import QApplication, QLabel
from PySide6.QtMultimedia import QAudioOutput, QMediaPlayer

from FormEvent.BaseWidgetEvent import BaseWidgetEvent
from FormEvent.TimeSetter import TimeSetter


class Event(BaseWidgetEvent):
    def __init__(self, _body: dict):
        super().__init__(_body)
        self.body = _body
        self.set_style_form_gui()
        self.create_base_form_gui()
        self.create_form_gui(_body)

    def create_form_gui(self, _body):

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

        self.time_setter = TimeSetter()

        self.button_layout.addWidget(self.postpone_5min_button)
        self.button_layout.addWidget(self.postpone_15min_button)
        self.button_layout.addWidget(self.time_setter)

        # подключение обработчиков событий
        self.postpone_5min_button.clicked.connect(
            lambda: self.postpone_notification(5))
        self.postpone_15min_button.clicked.connect(
            lambda: self.postpone_notification(5))
        self.time_setter.confirmed.connect(self.postpone_notification_hour)

    def closeEvent(self, event):
        print("closeEvent")
        self.play_sound_read()
        self.close_event.emit(self.body["id"])
        self.hide()

    def revert_close(self):
        print("revert_close")
        self.revert_hide_event.emit(self.body)

    def postpone_notification(self, delay):
        delay_ms = delay * 60 * 1000
        print("postpone_notification: ",delay)
        self.base_event.send_msg(delay)
        # Откладываем уведомление на delay_minutes минут
        QTimer.singleShot(delay_ms, self.revert_close)
        self.close_event.emit(self.body["id"])
    
    def postpone_notification_hour(self, delay):
        delay_ms = delay * 60 * 1000 * 60
        delay_min = delay * 60
        print("postpone_notification: ",delay_min)
        self.base_event.send_msg(delay_min)
        # Откладываем уведомление на delay_minutes минут
        QTimer.singleShot(delay_ms, self.revert_close)
        self.close_event.emit(self.body["id"])
