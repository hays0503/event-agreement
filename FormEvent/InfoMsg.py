import webbrowser
from PySide6.QtCore import Signal, Slot
from PySide6.QtCore import QTimer, Qt, QSize, QPoint, QRect, QUrl
from PySide6.QtGui import QIcon, QAction, QLinearGradient, QColor, QPainter, QPixmap
from PySide6.QtWidgets import QWidget, QMainWindow, QPushButton, QVBoxLayout, QHBoxLayout, QGraphicsBlurEffect
from PySide6.QtWidgets import QApplication, QLabel, QSystemTrayIcon, QMenu, QMessageBox
from PySide6.QtMultimedia import QAudioOutput, QMediaPlayer
import random


class InfoMsg(QWidget):
    close_event = Signal(int)

    def __init__(self, _step: int, _body: dict):
        super().__init__()
        self.step = _step
        self.body = _body
        self.set_style_form_gui()
        self.create_form_gui()

    def create_form_gui(self):

        main_layout = QVBoxLayout(self)
        self.setStyleSheet(
            "background-color: #FFFFAA; opacity: 1;")

        messages_layout = QHBoxLayout()

        Text = str(self.body["msg"])

        TextMessages = QLabel(Text)
        TextMessages.setWordWrap(True)
        # обработка текста и добавление переноса строки при необходимости
        if len(TextMessages.text()) > 70:
            new_text = ""
            words = TextMessages.text().split()
            line_length = 0
            for word in words:
                if line_length + len(word) > 70:
                    new_text += "\n"
                    line_length = 0
                new_text += word + " "
                line_length += len(word) + 1
            TextMessages.setText(new_text.strip())

        
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
        # создание горизонтального менеджера компоновки
        h_box = QHBoxLayout()

        ###############################################
        self.setWindowTitle("Пример окна с кнопками")

        if (self.body["url"] != "None"):
            self.open_document_button = QPushButton("Открыть информацию", self)
            self.open_document_button.setStyleSheet(
                "background-color: #00FF00; color: #000000; opacity: 1;")
            h_box.addWidget(self.open_document_button)
            self.open_document_button.clicked.connect(self.open_document)
        ###############################################

        if(self.body["type"] == "info_msg"):
            # создание объекта QPixmap и загрузка изображения
            pixmap = QPixmap("./info_icon.svg")
            pixmap.scaled(8, 8)
            # создание объекта QLabel и установка изображения в него
            picture_icon = QLabel()            
            picture_icon.setPixmap(pixmap)            
            messages_layout.addWidget(picture_icon)

        main_layout.addLayout(messages_layout)
        main_layout.addLayout(h_box)

        self.setLayout(main_layout)

        self.player = QMediaPlayer()
        self.audio = QAudioOutput()

    def set_style_form_gui(self):
        self.setWindowOpacity(0.9)
        blur = QGraphicsBlurEffect()
        blur.setBlurRadius(10)  # Устанавливаем радиус размытия в пикселях
        self.setGraphicsEffect(blur)

    def open_document(self):
        # Открываем браузер с договором
        if (self.body["url"] != "None"):
            webbrowser.open(self.body["url"])
        self.close()

    def play_sound_new_document(self):
        self.player.setAudioOutput(self.audio)
        self.player.setSource(QUrl.fromLocalFile("./event.mp3"))
        self.audio.setVolume(100)
        self.player.play()

    def play_sound_read(self):
        self.player.setAudioOutput(self.audio)
        self.player.setSource(QUrl.fromLocalFile("./read.mp3"))
        self.audio.setVolume(100)
        self.player.play()

    def showEvent(self, *any_kwarg):
        self.show()

    def closeEvent(self):
        self.play_sound_read()

    def postpone_notification(self, delay_minutes):
        self.hide()
        # Откладываем уведомление на delay_minutes минут
        QTimer.singleShot(delay_minutes * 60 * 1000, self.showEvent)
