from PySide6.QtCore import QObject, Signal, Slot
from aiohttp import web
from Common.Tread_with_trace_qtread import ThreadWithTrace
from Common.UserData import UserData
from Common.get_interface_ip_address import get_interface_ip_address
from FormEvent.Event import Event
from FormEvent.InfoMsg import InfoMsg


from PySide6.QtCore import Signal, Slot
from PySide6.QtCore import Qt, QRect
from PySide6.QtWidgets import QWidget, QVBoxLayout, QGraphicsBlurEffect
from PySide6.QtWidgets import QApplication, QScrollArea

import datetime

from Server.send_post_async import send_post

class Server(QObject):
    create_event = Signal(dict)
    read_event = Signal(int)
    minimize_event = Signal()

    def __init__(self, parent: QObject | None = ...) -> None:
        super().__init__(parent)
        self.create_event.connect(self.create_event_form)
        self.read_event.connect(self.close_windows)
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

    def send_power_on(self):
        user_data = UserData()
        interface_name = "Ethernet"
        ip_address = get_interface_ip_address(interface_name)
        login = user_data.get_login()
        domain = user_data.get_domain_name()
        json_msg = {
            "ip_host": str(ip_address)+':'+"8888",
            "time_start": datetime.datetime.now().isoformat(),
            "status": "start",
            "user data":  {"login": login, "domain_name": domain}
        }
        print(json_msg)
        send_post("http://192.168.0.9:5000/", json_msg)

    def run_tread(self):
        self.server_threads = ThreadWithTrace(function=self.start_server)
        self.server_threads.start()
        self.send_power_on()
        

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

    @Slot(dict)
    def create_event_form(self, body):
        if len(self.windows_event) == 0:
            if self.list_windows == None:
                self.create_gui()
            else:
                self.list_windows.show()

        print("create_event_form")
        print("body=", body)
        if (body["type"] == "new_document"):
            self.windows_event.append(Event(body))
        elif (body["type"] == "info_msg"):
            self.windows_event.append(InfoMsg(body))
        elif (body["type"] == "info_msg_warning"):
            self.windows_event.append(InfoMsg(body))
        elif (body["type"] == "info_msg_works"):
            self.windows_event.append(InfoMsg(body))
        else:
            print("Не известный тип окна")
            return

        current = len(self.windows_event)-1
        self.windows_event[current].close_event.connect(self.close_windows)
        self.windows_event[current].revert_hide_event.connect(
            self.revert_minimize_space)
        self.windows_event[current].play_sound_new_document()
        self.v_box_Layout.addWidget(self.windows_event[current])

    @Slot(dict)
    def revert_minimize_space(self, body):
        self.create_event_form(body)

    @Slot(int)
    def close_windows(self, id: int):
        print("close_windows")
        for _index, item in enumerate(self.windows_event):
            print(item.body["id"])
            print("id ", id)
            if item.body["id"] == id:
                if(self.windows_event[_index].isVisible()):
                    # Пробуем закрыть окно
                    self.windows_event[_index].hide()
                # Пробуем удалить элемент
                self.windows_event.pop(_index)
        # Если окна в области просмотра закончились закрываем область просмотра
        if len(self.windows_event) == 0:
            try:
                self.list_windows.hide()
            except Exception as e:
                print(e)
        print("self.windows_event", self.windows_event)

    def post_server_response(self, body: any):
        # try:
        if (body["type"] == "new_document"):
            self.create_event.emit(body)
            return "Ответ"
        if (body["type"] == "info_msg"):
            self.create_event.emit(body)
            return "Ответ"
        if (body["type"] == "info_msg_warning"):
            self.create_event.emit(body)
            return "Ответ"
        if (body["type"] == "info_msg_works"):
            self.create_event.emit(body)
            return "Ответ"
        if (body["type"] == "read_document"):
            self.read_event.emit(body["id"])
            return "Ответ"

        return "Ответа нет"
        # except AttributeError:
        #     return {"status": "Эмулятор еще не запущен", "code": 500}
