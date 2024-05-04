import subprocess,paramiko,tempfile
from cli_utils.logger.logger import p,os
from cryptography.fernet import Fernet

key = b'NIApu6z7lD3kLRn3iJzh0r6byv-RUCuLMN5Q6R5TDMM='
cipher_suite = Fernet(key)
pwd = b'gAAAAABmNkJAL6ZWRMkZZOEFa9bPD6ri95C1Tk8-wTsLQX0iMiUvDWhkTypmnmu2MJpV3jSYgYJ9fnTkYEphFYBXs-Aejwr_Sg=='
password = cipher_suite.decrypt(pwd).decode()

def rsync_transfer(destination, files_to_transfer):
  
    try:
        command = [
            "sshpass",
            "-p",
            password,
            "rsync",
            "--partial",
            "--append",
            "--progress",
            "--inplace",
            "--ignore-existing",
        ]

        for file in files_to_transfer:
            command.append(file)
        
        command.append(f"rentdrive@{destination}:/home/rentdrive/data")

        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, encoding="utf-8")
        stdout, stderr = process.communicate()
        
        if process.returncode == 0:
            p.info("Transfer completed successfully.")
        else:
            p.error(f"Error: {stderr}")
    except Exception as e:
        p.error(f"An unexpected error occurred: {e}")


def paramiko_transfer(destination, files_to_transfer):
    destination_path = f"/home/rentdrive/data2/"
    username = "rentdrive"
    hostname = destination

    try:

        ssh_client = paramiko.SSHClient()
        ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        ssh_client.connect(hostname=hostname, username=username, password=password)

        sftp_client = ssh_client.open_sftp()

        try:
            sftp_client.chdir(destination_path)
        except IOError:
            sftp_client.mkdir(os.path.dirname(destination_path))
            sftp_client.chdir(os.path.dirname(destination_path))

        for file in files_to_transfer:
            local_file = file
            remote_file = destination_path + os.path.basename(file)
            sftp_client.put(local_file, remote_file)
            p.info(f"Transferred {local_file} to server")
        sftp_client.close()
        ssh_client.close()

        p.info("Transfer completed successfully.")
    except Exception as e:
        p.error(f"An error occurred: {e}")

#

