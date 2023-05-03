from PySide6.QtGui import QPainter, QLinearGradient, QColor
from PySide6.QtWidgets import QWidget, QApplication
import sys

class Example(QWidget):
    def __init__(self):
        super().__init__()

    def paintEvent(self, event):
        painter = QPainter(self)
        gradient = QLinearGradient(self.rect().topLeft(), self.rect().bottomRight())
        gradient.setColorAt(0, QColor(255, 247, 227)) # светло-желтый цвет в начале
        gradient.setColorAt(1, QColor(255, 255, 255)) # белый цвет в конце
        painter.setBrush(gradient)
        painter.drawRect(self.rect())

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec_())
