import datetime
from Common.UserData import UserData
from Common.get_interface_ip_address import get_interface_ip_address
from Server.send_post_async import send_post

class BaseEvent():
    """
        Базовый класс события
    """
    def __init__(self,_body: dict) -> None:
        self.event_body = _body  
        self.timestamp_received = datetime.datetime.now()
    
    def send_msg(self, delay_minutes):
        user_data = UserData()
        interface_name = "Ethernet"
        ip_address = get_interface_ip_address(interface_name)
        login = user_data.get_login()
        domain = user_data.get_domain_name()
        json_msg = {
            "id": self.event_body["id"],
            "ip_host": str(ip_address)+':'+"8888",
            "timestamp_received": self.timestamp_received.isoformat(),
            "status": "delay",
            "timestamp_delay": str(delay_minutes)+"min",
            "user data":  {"login": login, "domain_name": domain}
        }
        print(json_msg)
        send_post("http://192.168.0.9:5000/", json_msg)
    

