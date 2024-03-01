from cli_utils.logger.logger import setup_logger
p = setup_logger()
import os
from cli_utils import utils

CLEAR_PATH = True

def add(paths):
    p.info("adding...")
    user_path = os.path.expanduser("~")
    DATA_PATH = os.path.join(user_path,".rentDrive","data")
    utils.move_data(paths,DATA_PATH)
    
    
 
                
                
            


def status():
    p.info("status")
    

def pull():
    p.info("pull")