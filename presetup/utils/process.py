import os
from utils.logger.logger import setup_logger
from utils import presetupfunctions as pre
p=setup_logger()
import shutil,socket

def process():
    pre.enable_port4444()
    check_port(4444)
    

def movetobin():
    curpath = os.getcwd()
    binpath = '/usr/bin'
    rentdrivepath = os.path.join(curpath, 'utils/test.py')
    p.info(f"rentdrivepath: {rentdrivepath}")
    try:
        shutil.copy(rentdrivepath, binpath)
        print("rentdrive.py has been moved to /usr/bin.")
    except Exception as e:
        print(f"Error: {e}")



def check_port(port):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(1) 
        s.connect(('localhost', port))
        s.close()  
        return True  
    except Exception as e:
        return False 
port = 4444
if check_port(port):
    p.info(f"Port {port} is open and accepting connections.")
else:
    p.info(f"Port {port} is closed.")