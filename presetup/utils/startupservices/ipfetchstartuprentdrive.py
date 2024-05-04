#!/usr/bin/env python3
import time,json
import subprocess,requests
import logging,os

logging.basicConfig(
    filename='/opt/.rentdriveservices/ipfetchstartuprentdrive.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def read_rentessentials():
    essentials_data= {}
    if not os.path.exists("/opt/.rentdriveservices/.rentessentials.json"):
        logging.info("Coulnot find the essentials file. Please run the presetup again")

    with open("/opt/.rentdriveservices/.rentessentials.json", "r") as token_file:
        essentials_data = json.load(token_file)
    return essentials_data

def add_to_essentials(key,value):
    try:
        with open("/opt/.rentdriveservices/.rentessentials.json", "r") as essentials:
            existing_data = json.load(essentials)
    except FileNotFoundError:
        existing_data = {}
    
    existing_data[key] = value
    with open("/opt/.rentdriveservices/.rentessentials.json", "w") as essentials:
        json.dump(existing_data, essentials)

def get_value(key):
    essentials_data = read_rentessentials()
    try:
        value = essentials_data[key]
    except KeyError:
        value = None
        logging.info(f"unable to find key : {key}")
    return value

def update_ip_address(address):
    url = "http://127.0.0.1:8000/marketplace/update_ip"
    auth_token = get_value("token")
    if not auth_token:
        logging.info("unable to update, login to continue")
        return False
    headers = {
    "Authorization": "Bearer " + auth_token ,
    "accept": "application/json",
}
    params = {"ip_address": address}

    logging.info("Updating database")
    try:
        response = requests.put(url,headers=headers, params=params)
        if response.status_code == 200:
            logging.info("IP address updated successfully")
            return True
        else:
            logging.info("Failed to update IP address ",response.text)
            return False
    except Exception as e:
        logging.info(f"update_ip_address : {e}")
    

def join_vpn(): 
    try:
        id = get_value("zerotier-id")
        cmd = ['sudo', 'zerotier-cli', 'join', id]
        res = subprocess.call(cmd)
        logging.info("VPN joined successfully")
    except subprocess.CalledProcessError as e:
        logging.error("Error joining VPN: %s", str(e))

def get_ip_address():
    try:
        id = get_value("zerotier-id")
        cmd = ['sudo','zerotier-cli', 'get', id, 'ip']
        result = subprocess.Popen(cmd, stdout=subprocess.PIPE)
        ip_address = result.communicate()[0].decode().strip()
        logging.info(f"ip address : {ip_address}")
        return ip_address
    except Exception as e:
        logging.error("Error fetching IP address for interface %s: ", str(e))
        return None
    

def ip_fetch():
    current_ip = get_value("ip_address")
    ten_mins = 30 * 60
    join_vpn()
    while True:
        new_ip = get_ip_address()
        if new_ip and new_ip != current_ip:
            update_ip_address(new_ip)
            add_to_essentials("ip_address",new_ip)
            logging.info("IP address updated: %s", new_ip)
            
        time.sleep(ten_mins)

if __name__ == "__main__":
    ip_fetch()
