import os
import getpass
import subprocess,shutil
from logger.logger import p


def create_systemd_service(service_name,desc):
    script_path = f"/opt/.rentdriveservices/{service_name}.py"
    p.info(f"Setting script path for service : {service_name} : {script_path}")
    """
    to create startup services
    there are 2 startup service , 1 to fetch ip and update database and other for port
    """
    
    
    service_content = f"""[Unit]
Description={desc}
After=network.target

[Service]
ExecStart=/usr/bin/python3 {script_path}
WorkingDirectory={os.path.dirname(script_path)}
Restart=always
User={getpass.getuser()}

[Install]
WantedBy=multi-user.target
"""
    service_file_path = f'/etc/systemd/system/{service_name}.service'
    with open(service_file_path, 'w') as service_file:
        service_file.write(service_content)

    return True

def enable_start_systemd_service(service_name):
    try:
        res = os.system(f'sudo systemctl enable {service_name}.service')
        res2 = os.system(f'sudo systemctl start {service_name}.service')
        p.info(f"run {service_name} ,{res} , {res2}")
        return True
    except subprocess.CalledProcessError as e:
        p.error(f"error : {str(e)}")
    


def run_startup(script_name,service_name,script_path):
    move_script_to_opt(script_path)
    service_file_path = create_systemd_service(service_name,script_name+".rentdrive")
    enable_start_systemd_service(service_name)
    update_permissions("/etc/systemd/system/"+service_name+'.service')

    p.info(f"Systemd service file created at: {service_file_path}")
    p.info(f"Service '{service_name}' enabled and started.")
    
def update_permissions(filepath):
    try:
        cmd = ['chmod', '+x', filepath]
        res = subprocess.call(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if res == 0:
            p.info(f"Permissions updated successfully for {filepath}")
        else:
            p.info(f"Failed to update permissions for {filepath}")
    except Exception as e:
        p.info(f"An error occurred: {e}")

def move_script_to_opt(script_path):
    if not os.path.exists("/opt/.rentdriveservices"):
        os.makedirs("/opt/.rentdriveservices")
    shutil.copy(script_path,os.path.join("/opt/.rentdriveservices"))