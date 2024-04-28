import os
from logger.logger import p
from logger import registry
from utils import runstartupservice as run
import shutil,socket,subprocess,sys
from utils import createParttiton as cp

PORT=4444

def process():
    # if not check_port():
    enable_port4444()
    invoke_startupscripts()
    registry.set_registry("PRE_SETUP_COMPLETE","True")  
    create_rentdrive_user()
    
    
    # cp.initial_setup()
    # cp.create_luks_partition()
    
    
    
    
def invoke_startupscripts():
    curr_dir = os.getcwd()
    service_list = ['portlistenstartuprentdrive.py','ipfetchstartuprentdrive.py']
    for service in service_list:
        p.info(f"{service}")
        service_dir = os.path.join(curr_dir,"utils/startupservices",service)
        service_name = service.split(".")[0] 
        p.info(f"adding {service} to startup")
        res = run.run_startup(service_name,service_name,service_dir)
        
    
def movetobin():
    curpath = os.getcwd()
    binpath = '/usr/bin'
    rentdrivepath = os.path.join(curpath, 'utils/test.py')
    p.info(f"rentdrivepath: {rentdrivepath}")
    try:
        shutil.copy(rentdrivepath, binpath)
        p.info("rentdrive.py has been moved to /usr/bin.")
    except Exception as e:
        print(f"Error: {e}")



def check_port():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(1) 
        s.connect(('localhost', PORT))
        s.close()
        p.info("port is open at 4444")  
        return True  
    except Exception as e:
        p.info(" port 4444 is closed")
        return False 
    
    
def enable_port4444():
    try:
        cmd1 = ['sudo', 'iptables', '-A', 'INPUT', '-p', 'tcp', '--dport', str(PORT), '-j', 'ACCEPT']
        p.info("adding port 4444 to iptables")
        p.info(f"Executing : {' '.join(cmd1)}")
        (res1)=subprocess.run(cmd1, check=True)
        p.info(f" {res1} ")

        p.info("permanently saving it to iptables")
        p.info(f"Executing : iptables-save")
        (res2)=subprocess.run(['sudo', 'iptables-save'], check=True, stdout=subprocess.DEVNULL)
        p.info(f"{res2}")
        p.info(f"setting up the port")
        return True
    except subprocess.CalledProcessError as e:
        p.info(f"exception occured {str(e)}")
        sys.exit(1)

def create_rentdrive_user():
    username= "rentdrive"
    password= "Commvault!12"
    try:
        p.info("Creating user rentdrive")
        create_user_cmd = ["sudo", "useradd", "-m", username]
        subprocess.run(create_user_cmd, check=True)
        p.info("Setting the password")
        set_password_cmd = ["sudo", "passwd", username]
        set_password_proc = subprocess.Popen(set_password_cmd, stdin=subprocess.PIPE)
        set_password_proc.communicate((password + "\n" + password + "\n").encode())
        p.info("adding root privileges")
        grant_root_cmd = ["sudo", "usermod", "-aG", "sudo", username]
        subprocess.run(grant_root_cmd, check=True)
    except subprocess.CalledProcessError as e:
        p.info(str(e))