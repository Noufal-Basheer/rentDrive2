import os,requests
from logger.logger import p
import json
from datetime import datetime, timedelta
from utils import runstartupservice as run
import socket,subprocess,sys
from utils import createParttiton as cp

PORT=4444

BASE_URL = "http://127.0.0.1:8000"

def process():
    check_if_user_logged_in()
    add_to_essentials("zerotier-id","856127940c5f3e4d")
    enable_port4444()
    invoke_startupscripts()
    create_rentdrive_user()
    update_presetup_complete()
    
def update_presetup_complete():
    url = BASE_URL + "/marketplace/presetup_done"
    auth_token = get_auth_token()
    if not auth_token:
        p.info("unable to update, login to continue")
        return False
    headers = {
    "Authorization": "Bearer " + auth_token ,
    "accept": "application/json",
}
    try:
        response = requests.put(url,headers=headers)
        if response.status_code == 200:
            p.info("Database updated successfully")
            return True
        else:
            p.info("Failed to database ",response.text)
            return False
    except Exception as e:
        p.info(f"updae_presetup_complete : {e}")

def check_if_user_logged_in():
    
    username = input("Enter username : \t")
    password = input("Enter password : \t")
    login(username, password)
    return True

def get_auth_token():
    token_data= {}
    token_path = "/opt/.rentdriveservices/.rentessentials.json"
    if os.path.exists(token_path):
        with open(token_path, "r") as token_file:
            token_data = json.load(token_file)
    if not token_data:
        return None
    token = token_data["token"]
    expiration_date_str = token_data["expiration_date"]
    expiration_date = datetime.strptime(expiration_date_str, "%Y-%m-%d %H:%M:%S")
    if datetime.now() > expiration_date:
        p.infog("Existing token expired. Please login again")
        return None
    else:
        p.info(token)
        return token


def add_to_essentials(key,value):
    try:
        with open("/opt/.rentdriveservices/.rentessentials.json", "r") as essentials:
            existing_data = json.load(essentials)
    except FileNotFoundError:
        existing_data = {}
    
    existing_data[key] = value
    with open("/opt/.rentdriveservices/.rentessentials.json", "w") as essentials:
        json.dump(existing_data, essentials)

    
def set_auth_token(auth_token):
    expiration_date = datetime.now() + timedelta(days=30)
    add_to_essentials("token",auth_token)
    add_to_essentials("expiration_date",expiration_date.strftime("%Y-%m-%d %H:%M:%S"))


def login(username, password):
    payload={
        "username": username,
        "password": password
    }
    url = BASE_URL+"/login"
    response = requests.post(url, data=payload)
    if response.status_code == 200:
        set_auth_token(response.json().get('access_token'))
        return True
    else:
        p.info("Error:", response.text)
        return False
    
def invoke_startupscripts():
    curr_dir = os.getcwd()
    service_list = ['portlistenstartuprentdrive.py','ipfetchstartuprentdrive.py']
    for service in service_list:
        p.info(f"{service}")
        service_dir = os.path.join(curr_dir,"utils/startupservices",service)
        service_name = service.split(".")[0] 
        p.info(f"adding {service} to startup")
        res = run.run_startup(service_name,service_name,service_dir)
        

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