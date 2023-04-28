import datetime
import webbrowser
from PySide6.QtCore import Signal
from PySide6.QtCore import QTimer, Qt, QSize, QPoint, QRect, QUrl
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import QWidget, QPushButton, QVBoxLayout, QHBoxLayout, QGraphicsBlurEffect
from PySide6.QtWidgets import QApplication, QLabel, QTextBrowser
from PySide6.QtMultimedia import QAudioOutput, QMediaPlayer
from Common.get_interface_ip_address import get_interface_ip_address

from Server.send_post_async import send_post


class InfoMsg(QWidget):
    close_event = Signal(int)
    hide_event = Signal(int)

    def __init__(self, _step: int, _body: dict):
        super().__init__()
        self.step = _step
        self.body = _body
        self.timestamp_received = datetime.datetime.now()       
        self.set_style_form_gui()
        self.create_form_gui()

    def create_form_gui(self):

        main_layout = QVBoxLayout(self)
        self.setStyleSheet(
            "background-color: #FFFFAA; opacity: 1;")

        messages_layout = QHBoxLayout()

        Text = str(self.body["msg"])

        TextMessages = QTextBrowser()
        TextMessages.setText(Text)
        # TextMessages.setWordWrap(True)
        # обработка текста и добавление переноса строки при необходимости
        # if len(TextMessages.text()) > 70:
        #     new_text = ""
        #     words = TextMessages.text().split()
        #     line_length = 0
        #     for word in words:
        #         if line_length + len(word) > 70:
        #             new_text += "\n"
        #             line_length = 0
        #         new_text += word + " "
        #         line_length += len(word) + 1
        #     TextMessages.setText(new_text.strip())

        messages_layout.addWidget(TextMessages)

        # Устанавливаем флаги для виджета
        self.setWindowFlags(
            Qt.WindowStaysOnTopHint | Qt.CustomizeWindowHint | Qt.FramelessWindowHint | Qt.Tool)

        # Отключаем кнопки закрытия и сворачивания
        self.setWindowFlag(Qt.WindowCloseButtonHint, False)
        self.setWindowFlag(Qt.WindowMinimizeButtonHint, False)
        self.setFixedSize(QSize(550, 300))
        ###############################################
        # Получаем первый экран из списка экранов
        desktop = QApplication.screens()[0]
        screen_rect = desktop.availableGeometry()  # Получаем размеры рабочей области
        widget_size = QSize(550, 300)  # Устанавливаем размер виджета
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

        if (self.body["type"] == "info_msg"):
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

    def closeEvent(self, event):        
        self.play_sound_read()
        self.close()

    def postpone_notification(self, delay_minutes):
        self.hide()
        self.send_msg(delay_minutes) 
        # Откладываем уведомление на delay_minutes минут
        QTimer.singleShot(delay_minutes * 60 * 1000, self.showEvent)
    
    def send_msg(self,delay_minutes):
        interface_name = "Ethernet"
        ip_address = get_interface_ip_address(interface_name)
        json_msg = {
            
            "id":self.body["id"],
            "ip_host":str(ip_address)+"8888",
            "timestamp_received":self.timestamp_received.isoformat(),
            "status":"delay",
            "timestamp_delay":str(delay_minutes)+"min"
        } 
        print(json_msg)
        send_post("http://192.168.0.9:5000/",json_msg)
