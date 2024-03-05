import os
from utils.logger.logger import setup_logger
p=setup_logger()
import shutil

def process():
    movetobin()
    print("hello")

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

