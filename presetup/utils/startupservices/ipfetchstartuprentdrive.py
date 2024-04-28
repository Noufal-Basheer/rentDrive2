#!/usr/bin/env python3
import socket
import time
import os,subprocess
from logger import registry 
from logger.logger import p


def join_vpn():
    id = "856127940c5f3e4d"
    try:
        cmd = ['sudo','zerotier-cli','join',id]
        p.info("Joining the network")
        res = subprocess.call(cmd,check=True)
        p.info(res)

    except subprocess.CalledProcessError as e:
        p.info(str(e))

def get_ip_address():
    try:
        ip_address = socket.gethostbyname(socket.gethostname())
        return ip_address
    except Exception as e:
        return None
 
def ip_fetch():
    current_ip = None
    ten_mins = 10*60
    join_vpn()
    while True:
        new_ip = get_ip_address()
        if new_ip and new_ip != current_ip:
            current_ip = new_ip
            registry.set_registry("ip_address", new_ip)
            #update the database here
        time.sleep(ten_mins)
ip_fetch()