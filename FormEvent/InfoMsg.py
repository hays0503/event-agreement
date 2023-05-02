
from FormEvent.BaseWidgetEvent import BaseWidgetEvent
from PySide6.QtCore import QTimer
from PySide6.QtCore import Signal
from PySide6.QtCore import Qt, QSize, QPoint, QRect, QUrl
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import QWidget, QPushButton, QVBoxLayout, QHBoxLayout, QGraphicsBlurEffect
from PySide6.QtWidgets import QApplication, QLabel, QTextBrowser
from PySide6.QtMultimedia import QAudioOutput, QMediaPlayer


class InfoMsg(BaseWidgetEvent):

    def __init__(self, _body: dict):
        super().__init__(_body)
        self.body = _body
        self.set_style_form_gui()
        self.create_base_form_gui()
        self.create_form_gui()

    def create_form_gui(self):
        # Если в создоваемом уведомлений нет url то и создавать нечего не нужно
        # (кнопок для открытие url)
        if (self.base_body["url"] != "None"):
            self.open_document_button = QPushButton("Открыть информацию", self)
            self.open_document_button.setStyleSheet(
                "background-color: #00FF00; color: #000000; opacity: 1;")
            self.button_layout.addWidget(self.open_document_button)
            self.open_document_button.clicked.connect(self.open_document)
        ###############################################

    def closeEvent(self, event):
        print("closeEvent")
        self.play_sound_read()
        self.close_event.emit(self.body["id"])
        self.hide()

    def revert_close(self):
        print("revert_close")
        self.revert_hide_event.emit(self.body)

    def postpone_notification(self, delay_minutes):
        self.hide()
        self.base_event.send_msg(delay_minutes)
        # Откладываем уведомление на delay_minutes минут
        QTimer.singleShot(delay_minutes * 60 * 1000, self.showEvent)
