import psutil
import socket

ip_address = None

def get_interface_ip_address(interface_name):
    global ip_address
    addrs = psutil.net_if_addrs()
    if (ip_address==None):
        for name, interfaces in addrs.items():
            if name == interface_name:
                for addr in interfaces:
                    if addr.family == socket.AF_INET:
                        ip_address = addr.address
                        break
    return ip_address
