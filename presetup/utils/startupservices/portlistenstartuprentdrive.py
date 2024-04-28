#!/usr/bin/env python3
import socket
import threading
import logging
import subprocess

# Configure logging
logging.basicConfig(
    filename='/opt/.rentdriveservices/portlistenstartuprentdrive.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# Create a logger
logger = logging.getLogger(__name__)

def listen_ports():
    def receiver():
        receiver_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        receiver_socket.bind(('0.0.0.0', 4444))
        receiver_socket.listen(1)
        logger.info("Listening on port 4444")

        while True:
            connection, address = receiver_socket.accept()
            logger.info("-----Incoming connection-------")
            logger.info("Connected to: %s", address)
            received_data = connection.recv(1024).decode()
            logger.info("Received message: %s", received_data)
            if received_data in ["PULL", "STATUS"]:
                if received_data == "PULL":
                    try:
                        cmd = "rentdrive pull"
                        subprocess.run(cmd, shell=True, check=True)
                        logger.info("Rentdrive pull command executed successfully")
                    except subprocess.CalledProcessError as e:
                        logger.error("Error occurred while executing '%s': %s", cmd, str(e))
            else:
                logger.info("Corrupt data received")
            connection.close()

    receiver_thread = threading.Thread(target=receiver)
    receiver_thread.daemon = True
    receiver_thread.start()
    while True:
        pass 

if __name__ == "__main__":
    listen_ports()
