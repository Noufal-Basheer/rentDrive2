import logging

import os
user_path = os.path.expanduser("~")
LOG_PATH = os.path.join(user_path, ".rentDrive", "Logs")
if not os.path.exists(LOG_PATH):
    os.makedirs(LOG_PATH)

def setup_logger():
    logger = logging.getLogger('my_logger')
    logger.setLevel(logging.DEBUG)

    file_handler = logging.FileHandler(LOG_PATH + '/rentDrive.log')
    file_handler.setLevel(logging.DEBUG)

    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)

    formatter = logging.Formatter('%(asctime)s - CLIENT - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger

p = setup_logger()