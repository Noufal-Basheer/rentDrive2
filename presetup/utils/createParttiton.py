import subprocess, os
from logger.logger import p  

LUKS_NAME = "rentDrive"
user_path = os.path.expanduser("~")
MOUNT_PATH = os.path.join(user_path, ".rentDrive", "Logs")


def  initial_setup():
    format_partition("/dev/sda3")
    luks_format_partition("/dev/sda3")

def create_luks_partition():
    if luks_open_partition("/dev/sda3"):
        mount_partition("/home/epart")

def close_partition():
    unmount_partition("/home/epart")
    luks_close_partition()


def format_partition(partition_path):
    try:
        cmd = ["mkfs.ext4", partition_path]
        process = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        output, error = process.communicate(timeout=1)
        prompt_exists = b"Proceed anyway? (y,N)" in output
        
        if prompt_exists:
            process.stdin.write(b"y\n")
            process.stdin.flush() 
        process.wait()
        
        if process.returncode == 0:
            p.info("Partition formatted successfully.")
        else:
            p.error(f"Error formatting partition: {error.decode()}")
    except Exception as e:
        p.error(f"Exception occurred: {str(e)}")


def luks_format_partition(part_path):
    passphrase = "Commvault!12"
    passphrase_bytes = (passphrase + "\n").encode()
    p.info(f"{passphrase_bytes}")
    try:
        
        wipe_cmd = ["wipefs", "-a", part_path]
        subprocess.check_call(wipe_cmd)
        
        cmd = ["cryptsetup", "luksFormat", part_path] 
        process = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        output, error = process.communicate(passphrase_bytes,timeout=3)
        p.info(f"{output}")
        
        # if b"Enter passphrase for" in output:
        #     process.stdin.write(passphrase_bytes)
        #     process.stdin.flush() 
        # process.wait(4)
        
        if b"Verify passphrase:" in output:
            process.stdin.write(passphrase_bytes)
            process.stdin.flush() 
        process.wait(4)
        
        if process.returncode != 0:
                p.error(f"Error formatting LUKS partition: {error.decode().strip()}")
                p.error(f"Output: {output.decode().strip()}")
        else:
            p.info("Partition formatted successfully.")
    except subprocess.CalledProcessError as e:
        p.error(str(e))

def luks_open_partition(partition_path):
    passphrase = "Commvaul!12"
    try:
        cmd = ["cryptsetup", "luksOpen", partition_path, LUKS_NAME]
        process = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        output, error = process.communicate(input=passphrase.encode())
        process.wait(1)
        if process.returncode == 0:
            p.info("LUKS partition opened successfully.")
            return True
        else:
            p.error(f"Error opening LUKS partition: {error.decode()}")
            return False
    except subprocess.CalledProcessError as e:
        p.error(str(e))
        return False

def mount_partition(mount_path):
    try:
        mapper_path = "/dev/mapper/rentDrive"
        cmd = ["mount",mapper_path , mount_path]
        res = subprocess.call(cmd)
        p.info(f"Result: {res}")
    except subprocess.CalledProcessError as e:
        p.error(str(e))

def unmount_partition(mount_path):
    try:
        cmd = ["umount", mount_path]
        res = subprocess.call(cmd)
        p.info(f"Result: {res}")
    except subprocess.CalledProcessError as e:
        p.error(str(e))

def luks_close_partition():
    try:
        cmd = ["cryptsetup", "luksClose", LUKS_NAME]
        res = subprocess.call(cmd)
        p.info(f"Result: {res}")
    except subprocess.CalledProcessError as e:
        p.error(str(e))

def delete_partition(partition_path):
    try:
        cmd = ["wipefs", "-a", partition_path]
        res = subprocess.call(cmd)
        p.info(f"Result: {res}")
    except subprocess.CalledProcessError as e:
        p.error(str(e))
