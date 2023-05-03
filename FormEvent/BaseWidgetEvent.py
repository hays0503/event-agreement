import os
import sys
from PySide6.QtCore import Signal
from PySide6.QtCore import Qt, QSize, QPoint, QRect, QUrl
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import QWidget,QVBoxLayout, QHBoxLayout, QGraphicsBlurEffect
from PySide6.QtWidgets import QApplication, QLabel, QTextBrowser
from PySide6.QtMultimedia import QAudioOutput, QMediaPlayer
from PySide6.QtGui import QPainter, QLinearGradient, QColor
from PySide6.QtWidgets import QWidget, QApplication
from Common.configparser import get_sound_toggle
from FormEvent.BaseEvent import BaseEvent
import webbrowser


class BaseWidgetEvent(QWidget):
    # Событие закрытие окна (id:int=событие)
    close_event = Signal(int)
    revert_hide_event = Signal(dict)

    def __init__(self, _body: dict):
        super().__init__()
        self.base_event = BaseEvent(_body)
        self.base_body = _body
        self.set_style_form_gui()

    def set_geometry_base_widget(self):
        ###############################################
        # Получаем первый экран из списка экранов
        desktop = QApplication.screens()[0]
        screen_rect = desktop.availableGeometry()  # Получаем размеры рабочей области
        widget_size = QSize(550, 300)  # Устанавливаем размер виджета
        widget_pos = QPoint(screen_rect.width() - widget_size.width(), screen_rect.height(
        ) - (widget_size.height()))  # Вычисляем позицию виджета
        # Устанавливаем геометрию виджета
        self.setGeometry(QRect(widget_pos, widget_size))
        # Установка фиксированного размера
        self.setFixedSize(QSize(550, 300))
        ###############################################

    def resource_path(self,relative_path):
        """ Get absolute path to resource, works for dev and for PyInstaller """
        try:
            # PyInstaller creates a temp folder and stores path in _MEIPASS
            base_path = sys._MEIPASS
        except Exception:
            base_path = os.path.abspath(".")

        return os.path.join(base_path, relative_path)

    def create_base_form_gui(self):
        # Базовый вертикальный макет
        self.main_layout = QVBoxLayout(self)

        # Макет для сообщения
        self.messages_layout = QHBoxLayout()

        # Макет для кнопок
        self.button_layout = QHBoxLayout()

        # Создаем браузер для просмотра текста
        TextMessages = QTextBrowser()
        TextMessages.setText(str(self.base_body["msg"]))
        self.messages_layout.addWidget(TextMessages)

        # Если сообщение с тэгом info_msg(информация)
        # Создаем с такой картинкой виджет
        if (self.base_body["type"] == "info_msg"):
            # создание объекта QPixmap и загрузка изображения
            patch = self.resource_path("./icon/info_icon.png")
            pixmap = QPixmap(patch)
            pixmap.scaled(8, 8)
            # создание объекта QLabel и установка изображения в него
            picture_icon = QLabel()
            picture_icon.setPixmap(pixmap)
            self.messages_layout.addWidget(picture_icon)
        
        # Сообщение с информацией важной
        if (self.base_body["type"] == "info_msg_warning"):
            # создание объекта QPixmap и загрузка изображения
            patch = self.resource_path("./icon/info_msg_warning.png")
            pixmap = QPixmap(patch)
            pixmap.scaled(8, 8)
            # создание объекта QLabel и установка изображения в него
            picture_icon = QLabel()
            picture_icon.setPixmap(pixmap)
            self.messages_layout.addWidget(picture_icon)
        
        # Сообщение о технической работе сервиса(технические работы)
        if (self.base_body["type"] == "info_msg_works"):
            # создание объекта QPixmap и загрузка изображения
            patch = self.resource_path("./icon/info_msg_works.png")
            pixmap = QPixmap(patch)
            pixmap.scaled(8, 8)
            # создание объекта QLabel и установка изображения в него
            picture_icon = QLabel()
            picture_icon.setPixmap(pixmap)
            self.messages_layout.addWidget(picture_icon)

        self.main_layout.addLayout(self.messages_layout)
        self.main_layout.addLayout(self.button_layout)

        self.setLayout(self.main_layout)

        self.player = QMediaPlayer()
        self.audio = QAudioOutput()

    def set_style_form_gui(self):
        self.setWindowOpacity(0.9)
        blur = QGraphicsBlurEffect()
        blur.setBlurRadius(10)  # Устанавливаем радиус размытия в пикселях
        self.setGraphicsEffect(blur)
        # Установка стиля
        self.setStyleSheet("background-color: #FFFFAA; opacity: 1;")
        # Устанавливаем флаги для виджета
        self.setWindowFlags(Qt.WindowStaysOnTopHint |
                            Qt.CustomizeWindowHint | Qt.FramelessWindowHint | Qt.Tool)
        # Отключаем кнопки закрытия и сворачивания
        self.setWindowFlag(Qt.WindowCloseButtonHint, False)
        self.setWindowFlag(Qt.WindowMinimizeButtonHint, False)
        # Установка название окна(не показывается т.к встроенно в другой виджет)
        self.setWindowTitle("Уведомление")

    def paintEvent(self, event):
            painter = QPainter(self)
            gradient = QLinearGradient(self.rect().topLeft(), self.rect().bottomRight())
            gradient.setColorAt(0, QColor(255, 247, 227)) # светло-желтый цвет в начале
            gradient.setColorAt(1, QColor(255, 255, 255)) # белый цвет в конце
            painter.setBrush(gradient)
            painter.drawRect(self.rect())

    def play_sound_new_document(self):
        self.player.setAudioOutput(self.audio)
        patch = self.resource_path("./sound/event.mp3")
        self.player.setSource(QUrl.fromLocalFile(patch))
        self.audio.setVolume(100)
        if get_sound_toggle():
            self.player.play()

    def play_sound_read(self):
        self.player.setAudioOutput(self.audio)
        patch = self.resource_path("./sound/read.mp3")
        self.player.setSource(QUrl.fromLocalFile(patch))
        self.audio.setVolume(100)
        if get_sound_toggle():
            self.player.play()

    def open_document(self):
        # Открываем браузер с договором
        if (self.base_body["url"] != "None"):
            webbrowser.open(self.base_body["url"])
        self.close()
