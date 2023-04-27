from PySide6.QtCore import QObject, Signal, Slot
from aiohttp import web
from Common.Tread_with_trace_qtread import ThreadWithTrace
from Common.get_interface_ip_address import get_interface_ip_address
from FormEvent.Event import Event


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
        self.windows_event.append([Event(step, body),body,step])
        current = len(self.windows_event)-1
        windows_gui = 0
        self.windows_event[current][windows_gui].close_event.connect(self.minimize_space)
        self.windows_event[current][windows_gui].show()
        self.windows_event[current][windows_gui].play_sound_new_document()

    @Slot(int)
    def minimize_space(self,delete_index:int):
        print("minimize_space ",delete_index)
        if(delete_index>=len(self.windows_event)):
            return
        if(delete_index>=5):
            return
        windows_gui = 0
        json_event_old = 1
        x = int(self.windows_event[delete_index][windows_gui].pos().x())
        y = int(self.windows_event[delete_index][windows_gui].pos().y())
        h = int(self.windows_event[delete_index][windows_gui].height())
        print(x,y)
        self.windows_event[delete_index][windows_gui].move((x),(y+h))
        x = int(self.windows_event[delete_index][windows_gui].pos().x())
        y = int(self.windows_event[delete_index][windows_gui].pos().y())        
        h = int(self.windows_event[delete_index][windows_gui].height())
        print(x,y)
        self.minimize_space(delete_index+1)
    
    @Slot(dict)
    def read_event_form(self, body):
        windows_gui = 0
        json_event_old = 1

        for _index, item in enumerate(self.windows_event):
            #Если нашли закрываем окно и удаляем окно 
            if(item[json_event_old]["id"] == body["id"]): 
                item[windows_gui].close()
                self.windows_event.pop(_index)
                self.minimize_space(_index)



    def post_server_response(self, body: any):

        # try:
        if (body["type"] == "new_document"):
            self.create_event.emit(self.step, body)
            if (self.step <= 4):
                self.step = self.step + 1
            else:
                self.step = 1            
            return "Ответ"
        if (body["type"] == "read_document"):
            self.read_event.emit(body)
            return "Ответ"
        
        return "Ответа нет"
        # except AttributeError:
        #     return {"status": "Эмулятор еще не запущен", "code": 500}
