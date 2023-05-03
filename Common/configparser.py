import configparser

config = configparser.ConfigParser()
config.read('config/config.ini')
db_config = config['agreement']
host = db_config['host']
HOST = host
host_server = db_config['HOSTSERVER']
HOST_SERVER = host_server
port_server = db_config['PORTSERVER']
PORT_SERVER = port_server
sound = db_config['SOUND']
SOUND = port_server
password = db_config['PASSWORD']
PASSWORD = password



def config_sound_toggle(toggle: bool):
    if toggle:
        db_config['SOUND'] = "ON"
    else:
        db_config['SOUND'] = "OFF"
    with open('config/config.ini', 'w') as configfile:
        config.write(configfile)

def get_sound_toggle()->bool:
    if db_config['SOUND'] == "ON":
        return True
    elif db_config['SOUND'] == "OFF":
        return False
