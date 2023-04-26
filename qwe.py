from PySide6.QtCore import QUrl
from PySide6.QtWidgets import QApplication, QPushButton
from PySide6.QtMultimedia import QMediaPlayer, QAudioOutput

app = QApplication()

player = QMediaPlayer()
audio = QAudioOutput()

player.setAudioOutput(audio)
audio.setVolume(100)


def play():
    player.setSource(QUrl.fromLocalFile("./event.mp3"))
    player.play()


button = QPushButton("Play")
button.clicked.connect(play)
button.show()

app.exec()
