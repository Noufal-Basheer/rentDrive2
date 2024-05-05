import subprocess
import random
import string
from logger.logger import p
def generate_password(length=6):
    """Generate a random password."""
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for i in range(length))

def is_folder_shared(folder):
    """Check if the folder is already shared."""
    with open('/etc/samba/smb.conf', 'r') as file:
        samba_config = file.read()
        return f'[{folder}]' in samba_config

def setup_samba_share(folder, username):
    
    # if is_folder_shared(folder):
    #     p.info(f"The folder '{folder}' is already shared.")
    #     return
    password = generate_password()
    p.info("Creating NFS")
    subprocess.run(['echo', f'{password}', '|', 'sudo', 'smbpasswd', '-s', '-a', username], shell=True)

    samba_conf = f"""
    [rentdrive]
       path = {folder}
       writable = yes
       guest ok = yes
       read only = no
       create mask = 0777
       directory mask = 0777
       force user = {username}
    """

    with open('/etc/samba/smb.conf', 'a') as file:
        file.write(samba_conf)

    subprocess.run(['sudo', 'service', 'smbd', 'restart'])

    p.info(f"share configured successfully!\n")
    p.info(f" user: {username}")
    p.info(f"password: {password}")
    p.info("Please save the password for future access")

