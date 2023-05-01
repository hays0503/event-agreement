from PySide6.QtCore import Signal
from PySide6.QtCore import QTimer, Qt, QSize, QPoint, QRect, QUrl
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import QWidget, QPushButton, QVBoxLayout, QHBoxLayout, QGraphicsBlurEffect
from PySide6.QtWidgets import QApplication, QLabel, QTextBrowser
from PySide6.QtMultimedia import QAudioOutput, QMediaPlayer




class BaseWidgetEvent(QWidget):
    close_event = Signal(int)    
    revert_hide_event = Signal(int,dict)

    def __init__(self, _step: int, _body: dict):
        super().__init__()
        self.set_style_form_gui()
        self.create_form_gui()
    
    def set_geometry_base_widget(self):
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

    def create_form_gui(self):

        main_layout = QVBoxLayout(self)
        self.setStyleSheet(
            "background-color: #FFFFAA; opacity: 1;")
        messages_layout = QHBoxLayout()
        Text = str(self.body["msg"])
        TextMessages = QTextBrowser()
        TextMessages.setText(Text)
        messages_layout.addWidget(TextMessages)
        # Устанавливаем флаги для виджета
        self.setWindowFlags(
            Qt.WindowStaysOnTopHint | Qt.CustomizeWindowHint | Qt.FramelessWindowHint | Qt.Tool)
        # Отключаем кнопки закрытия и сворачивания
        self.setWindowFlag(Qt.WindowCloseButtonHint, False)
        self.setWindowFlag(Qt.WindowMinimizeButtonHint, False)
        self.setFixedSize(QSize(550, 300))

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
