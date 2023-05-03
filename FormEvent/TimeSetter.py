from PySide6.QtWidgets import QApplication, QWidget, QSpinBox, QSlider, QVBoxLayout, QHBoxLayout, QLabel, QPushButton
from PySide6.QtCore import Qt, Signal


class TimeSetter(QWidget):

    # создаем новый сигнал "confirmed"
    confirmed = Signal(int)

    def __init__(self):
        super().__init__()

        # создаем SpinBox для ввода значения от 1 до 24
        self.spin_box = QSpinBox(self)
        self.spin_box.setMinimum(1)
        self.spin_box.setMaximum(48)

        # создаем Slider для изменения значения SpinBox
        self.slider = QSlider(self)
        self.slider.setOrientation(Qt.Horizontal)
        self.slider.setMinimum(1)
        self.slider.setMaximum(48)
        self.slider.setTickInterval(1)
        self.slider.setTickPosition(QSlider.TicksBelow)

        # создаем вертикальный layout и добавляем в него SpinBox, Slider, QHBoxLayout и кнопку "Подтвердить"
        vbox = QVBoxLayout(self)
        vbox.addWidget(self.spin_box)
        vbox.addWidget(self.slider)

        # создаем горизонтальный layout и добавляем в него label для отображения значения Slider
        hbox = QHBoxLayout()
        self.label = QLabel(str(self.slider.value())+" час(ов)", self)
        hbox.addWidget(self.label)
        vbox.addLayout(hbox)

        # создаем кнопку "Подтвердить" и добавляем ее в вертикальный layout
        self.confirm_button = QPushButton("Отложить на 1 час", self)
        vbox.addWidget(self.confirm_button)

        # подключаем слоты для изменения значений
        self.spin_box.valueChanged.connect(self.set_time_value)
        self.slider.valueChanged.connect(self.spin_box.setValue)

        self.spin_box.valueChanged.connect(self.slider.setValue)
        self.slider.valueChanged.connect(self.set_time_value)

        # подключаем clicked сигнал кнопки "Подтвердить" к методу on_confirm_button_clicked
        self.confirm_button.clicked.connect(self.on_confirm_button_clicked)

    def set_time_value(self, value: int):
        Text = str(value)+" час(ов)"
        self.confirm_button.setText("Отложить на "+Text)
        self.label.setText(Text)

    def on_confirm_button_clicked(self):
        # испускаем сигнал "confirmed" и передаем значение SpinBox
        self.confirmed.emit(self.spin_box.value())


if __name__ == '__main__':
    app = QApplication()
    form = TimeSetter()

    # подключаемся к сигналу "confirmed" и выводим значение в консоль
    form.confirmed.connect(lambda value: print(
        "Значение подтверждено:", value))

    form.show()
    app.exec()
