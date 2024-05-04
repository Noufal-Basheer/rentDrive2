from cli_utils.logger.logger import p
from cli_utils.logger import registry
import os
from cli_utils import utils,apirequests,transfer
import shutil

CLEAR_PATH = True
USER_PATH = "/opt/"
RENTDRIVE_PATH=os.path.join(USER_PATH,".rentdrive")
DATA_PATH = os.path.join(USER_PATH,".rentdrive","data")
RESTORE_PATH = os.path.join(USER_PATH,".rentdrive","restore")
if not os.path.exists(DATA_PATH):
    os.makedirs(DATA_PATH)



def add(paths):
    utils.move_data(paths,DATA_PATH)
    
                
def commit():
    (FOLDER_PATH,FOLDER_NAME)=utils.get_path_and_name(DATA_PATH)
    if not FOLDER_PATH:
        p.info("Nothing to commit")
        return True
    hash_val_of_dir = utils.compute_dir_hash(FOLDER_PATH)
    p.info(f"hash val of {FOLDER_PATH} : {hash_val_of_dir}")
    utils.gpg_encrypt_file(FOLDER_PATH,FOLDER_NAME)
    shutil.rmtree(FOLDER_PATH)
    #api to store hash value
    
    return True         
            


def status():
    p.info("status")
    

def pull():
    p.info("pull")
    #api to do scp from lentee to lender

    
def push():
    if not registry.get_registry("ticket_id"):
        p.info("No ative tickets found")
        return 
    files_to_transfer = []
    for item in os.listdir(DATA_PATH):
        if item.endswith(".gpg"):
            hash = utils.compute_file_hash(os.path.join(DATA_PATH,item))
            utils.write_to_history(os.path.join(USER_PATH,".rentdrive"),item,hash)
            files_to_transfer.append(os.path.join(DATA_PATH,item))
    p.info("Processing..")
    # ip_address = apirequests.get_lender_ip()
    ip_address = "10.147.20.67"
    p.info(files_to_transfer)
    transfer.paramiko_transfer(ip_address,files_to_transfer)



def restore():
    p.info("restoring")
    utils.restore(RESTORE_PATH,RENTDRIVE_PATH)

def config(username,password):
    p.info("configuring....")
    auth_token = apirequests.login(username,password)
    if auth_token:
        p.info("configuration successfull")
        registry.set_registry("auth_token",auth_token)
        p.info("getting tickets")
        apirequests.get_ticket_data()
    else:
        p.info("Invalid credentials")
    

def test():
    p.info("getting tickets")
    apirequests.get_lender_ip()