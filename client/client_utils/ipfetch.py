import socket
import os
import time
import os
import client_utils.registry as registry
from client_utils.logger.logger import setup_logger
p =setup_logger()


def get_ip_address():
    try:
        ip_address = socket.gethostbyname(socket.gethostname())
        return ip_address
    except Exception as e:
        return None
    
def main():
    current_ip = None
    ten_mins = 10*60
    #for checking in background every 10mins for change in ip
    while True:
        new_ip = get_ip_address()
        if new_ip and new_ip != current_ip:
            current_ip = new_ip
            registry.set_registry("ip_address", new_ip)
        time.sleep(ten_mins)


