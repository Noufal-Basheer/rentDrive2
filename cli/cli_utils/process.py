from cli_utils.logger.logger import setup_logger
p = setup_logger()
import os
from cli_utils import utils

CLEAR_PATH = True
USER_PATH = os.path.expanduser("~")
DATA_PATH = os.path.join(USER_PATH,".rentDrive","data")


def add(paths):
    global FOLDER_PATH,FOLDER_NAME
    p.info("add")
    (FOLDER_PATH,FOLDER_NAME) = utils.move_data(paths,DATA_PATH)
    hash_val_of_dir = utils.compute_dir_hash(FOLDER_PATH)
    p.info(f"hash val of {FOLDER_PATH} : {hash_val_of_dir}")
    
    
 
                
def commit():
    if not (FOLDER_PATH or FOLDER_NAME):
        utils.get_path_and_name(DATA_PATH)
        
    utils.gpg_encrypt_file(FOLDER_PATH,FOLDER_NAME)         
            


def status():
    
    p.info("status")
    

def pull():
    p.info("pull")
    

def restore():
    p.info("restore")
    