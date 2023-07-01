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
        value = socket.getfqdn()
        __domain_name = value.split('.')[1] if value else 'localhost'
        return __domain_name
    