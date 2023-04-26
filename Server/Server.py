from PySide6.QtCore import QObject, Signal, Slot
from aiohttp import web
from Common.Tread_with_trace_qtread import ThreadWithTrace
from Common.get_interface_ip_address import get_interface_ip_address
from FormEvent.Event import Event


class Server(QObject):
    create_event = Signal(int, dict)

    def __init__(self, parent: QObject | None = ...) -> None:
        super().__init__(parent)
        self.create_event.connect(self.create_event_form)
        self.step = 1

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
        windows_event = Event(step, body)
        windows_event.show()

    def post_server_response(self, body: any):

        # try:
        if (body["type"] == "read"):

            self.create_event.emit(self.step, body)
            if (self.step <= 4):
                self.step = self.step + 1
            else:
                self.step = 1
            response_body = "Ответ"

        return response_body

        # except AttributeError:
        #     return {"status": "Эмулятор еще не запущен", "code": 500}
