"""
    Returns:
        _type_: _description_
"""
import os
import socket


class UserData():
    """
        Запросить данные пользователя в системе
    """
    def get_login(self)->str:
        """
            Запросить данные пользователя в системе (имя)
        """
        username = os.getlogin()
        return username

    def get_domain_name(self)->str:
        """
            Запросить данные пользователя в системе (домен)
        """
        domain_name = socket.getfqdn()
        return domain_name
    