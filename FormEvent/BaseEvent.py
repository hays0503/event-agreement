import datetime
import webbrowser
from Common.UserData import UserData
from Common.get_interface_ip_address import get_interface_ip_address
from Server.send_post_async import send_post
from PySide6.QtCore import QObject


class BaseEvent(QObject):
    """
        Базовый класс события
    """
    def __init__(self, _step: int, _body: dict, parent: QObject | None = ...) -> None:
        super().__init__(parent)
        self.step = _step
        self.body = _body  
        self.timestamp_received = datetime.datetime.now()
    
    def send_msg(self, delay_minutes):
        user_data = UserData()
        interface_name = "Ethernet"
        ip_address = get_interface_ip_address(interface_name)
        login = user_data.get_login()
        domain = user_data.get_domain_name()
        json_msg = {
            "id": self.body["id"],
            "ip_host": str(ip_address)+"8888",
            "timestamp_received": self.timestamp_received.isoformat(),
            "status": "delay",
            "timestamp_delay": str(delay_minutes)+"min",
            "user data":  {"login": login, "domain_name": domain}
        }
        print(json_msg)
        send_post("http://192.168.0.9:5000/", json_msg)
    
    def open_document(self):
        # Открываем браузер с договором
        if (self.body["url"] != "None"):
            webbrowser.open(self.body["url"])
        self.close()
