#!/usr/bin/env python3
import time
import subprocess,netifaces
import logging

id = "856127940c5f3e4d"
logging.basicConfig(
    filename='/opt/.rentdriveservices/ipfetchstartuprentdrive.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def join_vpn(): 
    try:
        cmd = ['sudo', 'zerotier-cli', 'join', id]
        res = subprocess.call(cmd)
        logging.info("VPN joined successfully")
    except subprocess.CalledProcessError as e:
        logging.error("Error joining VPN: %s", str(e))

def get_ip_address():
    try:
        cmd = ['sudo','zerotier-cli', 'get', id, 'ip']
        result = subprocess.Popen(cmd, stdout=subprocess.PIPE)
        ip_address = result.communicate()[0].decode().strip()
        logging.info(f"ip address : {ip_address}")
        return ip_address
    except Exception as e:
        logging.error("Error fetching IP address for interface %s: ", str(e))
        return None
def ip_fetch():
    current_ip = None
    ten_mins = 10 * 60
    join_vpn()
    while True:
        new_ip = get_ip_address()
        if new_ip and new_ip != current_ip:
            current_ip = new_ip
            logging.info("IP address updated: %s", current_ip)
            # Update the database here
        time.sleep(ten_mins)

if __name__ == "__main__":
    ip_fetch()
