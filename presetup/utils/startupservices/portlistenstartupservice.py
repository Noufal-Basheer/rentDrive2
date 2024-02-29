import socket
import threading
from utils.logger.logger import setup_logger
from ..logger.logger import setup_logger
import subprocess

def listen_ports():
    p = setup_logger()
    def receiver():
        receiver_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        receiver_socket.bind(('0.0.0.0', 4444))
        receiver_socket.listen(1)

        while True:
            connection, address = receiver_socket.accept()
            p.info("Connected to:", address)
            received_data = connection.recv(1024).decode()
            p.info("Received message:", received_data)
            if received_data in ["PULL"]:
                if received_data=="PULL":
                    try:
                        cmd = "rentdrive pull"
                        subprocess.run(cmd, shell=True, check=True)
                    except subprocess.CalledProcessError as e:
                        p.info(f"error occured while executing {cmd} : {str(e)}" )
            else:
                p.info(f"corrupt data recieved")
    receiver_thread = threading.Thread(target=receiver)
    receiver_thread.daemon = True
    receiver_thread.start()
    while True:
        pass 
