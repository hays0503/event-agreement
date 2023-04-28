from PySide6.QtWidgets import QListWidget
from PySide6.QtCore import QObject, Signal, Slot
from aiohttp import web
from Common.Tread_with_trace_qtread import ThreadWithTrace
from Common.get_interface_ip_address import get_interface_ip_address
from FormEvent.Event import Event
from FormEvent.InfoMsg import InfoMsg


from PySide6.QtCore import Signal, Slot
from PySide6.QtCore import QTimer, Qt, QSize, QPoint, QRect, QUrl
from PySide6.QtGui import QIcon, QAction, QLinearGradient, QColor, QPainter
from PySide6.QtWidgets import QWidget, QMainWindow, QPushButton, QVBoxLayout, QHBoxLayout, QGraphicsBlurEffect
from PySide6.QtWidgets import QApplication, QLabel, QSystemTrayIcon, QMenu, QMessageBox, QScrollArea
from PySide6.QtMultimedia import QAudioOutput, QMediaPlayer


class Server(QObject):
    create_event = Signal(int, dict)
    read_event = Signal(dict)
    minimize_event = Signal()

    def __init__(self, parent: QObject | None = ...) -> None:
        super().__init__(parent)
        self.create_event.connect(self.create_event_form)
        self.read_event.connect(self.read_event_form)
        self.step = 1
        self.windows_event = []
        self.list_windows = None


    def create_gui(self):
        self.list_windows = QWidget()

        self.v_box_Layout = QVBoxLayout()

        for Widget in self.windows_event:
            self.v_box_Layout.addWidget(Widget)

        self.list_windows.setLayout(self.v_box_Layout)
        #####################################################################################
        desktop = QApplication.screens()[0]
        rect = desktop.availableGeometry()

        # Устанавливаем геометрию виджета
        self.list_windows.setGeometry(QRect(rect.width() - self.list_windows.width(), rect.height(
        )-self.list_windows.height(), self.list_windows.width(), self.list_windows.height()))
        #####################################################################################
        # Создаем QScrollArea и добавляем в него QVBoxLayout
        self.scroll_area = QScrollArea(self.list_windows)
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setWidget(QWidget())
        self.scroll_area.widget().setLayout(self.v_box_Layout)
        self.scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        # Скрыть вертикальную полосу прокрутки
        self.scroll_bar = self.scroll_area.verticalScrollBar()
        self.scroll_bar.setStyleSheet("QScrollBar {visibility: hidden;}")
        #####################################################################################
        self.list_windows.setLayout(QVBoxLayout())
        self.list_windows.layout().addWidget(self.scroll_area)
        self.list_windows.setWindowFlags(
        Qt.WindowStaysOnTopHint | Qt.CustomizeWindowHint | Qt.FramelessWindowHint | Qt.Tool)
        #####################################################################################
        self.set_style_form_gui()
        self.list_windows.show()

    def set_style_form_gui(self):
        self.list_windows.setWindowOpacity(0.8)
        blur = QGraphicsBlurEffect()
        blur.setBlurRadius(10)  # Устанавливаем радиус размытия в пикселях
        self.list_windows.setGraphicsEffect(blur)

    def start_server(self):
        # Web - часть
        app = web.Application()
        app.add_routes([web.post('/', self.post_func)])
        # Имя интерфейса, для которого нужно получить IP-адрес
        interface_name = "Ethernet"
        ip_address = get_interface_ip_address(interface_name)
        web.run_app(host=ip_address, port=8888, app=app)

    def run_tread(self):
        self.server_threads = ThreadWithTrace(function=self.start_server)
        self.server_threads.start()

    async def post_func(self, request):
        #########################################
        # Обработчик входящих подключений
        body = await request.json()

        print("Принял сообщение=>", body)

        #########################################
        # Обработка включение контролера от упр сервера
        response_body = self.post_server_response(body)
        #########################################
        return web.json_response(response_body)

    @Slot(int, dict)
    def create_event_form(self, step, body):
        if len(self.windows_event) == 0:
            if self.list_windows == None:
                self.create_gui()
            else:
                self.list_windows.show()
            
        print("create_event_form")
        print("step= ", step, " body=", body)
        if (body["type"] == "new_document"):
            self.windows_event.append(Event(step, body))
        if (body["type"] == "info_msg"):
            self.windows_event.append(InfoMsg(step, body))
        current = len(self.windows_event)-1
        self.windows_event[current].close_event.connect(self.close_windows)
        self.windows_event[current].hide_event.connect(self.minimize_space)
        self.windows_event[current].revert_hide_event.connect(self.revert_minimize_space)
        self.windows_event[current].play_sound_new_document()
        self.v_box_Layout.addWidget(self.windows_event[current])
        
    
    @Slot(int, dict)
    def revert_minimize_space(self, step, body):
        self.create_event_form(step, body)


    @Slot(int)
    def close_windows(self, id: int):
        print("###########")
        print("len(self.windows_event)=", len(self.windows_event))
        print("id =", id)
        for item in self.windows_event:
            if item.body["id"] == id:
                self.windows_event.remove(item)
                break
        print("len(self.windows_event)=", len(self.windows_event))
        print("###########")
        if len(self.windows_event) == 0:
            self.list_windows.hide()

    @Slot(int)
    def minimize_space(self, delete_index: int):
        pass
        # print("self.windows_event ",self.windows_event)
        # print("minimize_space ",delete_index)
        # if(delete_index>=len(self.windows_event)):
        #     return
        # windows_gui = 0

        # if(self.step>1):
        #     self.step-=1

        # x = int(self.windows_event[delete_index][windows_gui].pos().x())
        # y = int(self.windows_event[delete_index][windows_gui].pos().y())
        # h = int(self.windows_event[delete_index][windows_gui].height())
        # self.windows_event[delete_index][windows_gui].move((x),(y+h))
        # self.minimize_space(delete_index+1)

    @Slot(dict)
    def read_event_form(self, body):
        pass
        # windows_gui = 0
        # json_event_old = 1

        # for _index, item in enumerate(self.windows_event):
        #     #Если нашли закрываем окно и удаляем окно
        #     if(item[json_event_old]["id"] == body["id"]):
        #         item[windows_gui].close()
        #         self.windows_event.pop(_index)
        #         self.minimize_space(_index)

    def post_server_response(self, body: any):

        # try:
        if (body["type"] == "new_document"):
            self.create_event.emit(self.step, body)
            self.step = self.step + 1
            return "Ответ"
        if (body["type"] == "info_msg"):
            self.create_event.emit(self.step, body)
            self.step = self.step + 1
            return "Ответ"
        if (body["type"] == "read_document"):
            self.read_event.emit(body)
            return "Ответ"

        return "Ответа нет"
        # except AttributeError:
        #     return {"status": "Эмулятор еще не запущен", "code": 500}
