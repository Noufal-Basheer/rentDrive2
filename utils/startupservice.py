import os
import getpass

def create_systemd_service(script_path, service_name):
    service_content = f"""[Unit]
Description=Update IP Address Service
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

    return service_file_path

def enable_start_systemd_service(service_name):
    os.system(f'sudo systemctl enable {service_name}.service')
    os.system(f'sudo systemctl start {service_name}.service')


def run_startup():
    script_name = 'your_script.py'
    service_name = 'rentDrive_startup'

    script_path = os.path.abspath(script_name)

    service_file_path = create_systemd_service(script_path, service_name)
    enable_start_systemd_service(service_name)

    print(f"Systemd service file created at: {service_file_path}")
    print(f"Service '{service_name}' enabled and started.")