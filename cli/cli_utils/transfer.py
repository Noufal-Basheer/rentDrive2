import subprocess,paramiko
from cli_utils.logger.logger import p,os

def rsync_transfer(destination, files_to_transfer):
    source = " ".join(files_to_transfer)
    command = [
        "rsync",
        "--partial",
        "--append",
        "--progress",
        "--inplace",
        "--ignore-existing",
        "-e",
        "",
        source,
        f"rentdrive@{destination}:/home/rentdrive/data"
    ]
    
    try:
        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, encoding="utf-8")
        stdout, stderr = process.communicate()
        if process.returncode == 0:
            p.info("Transfer completed successfully.")
        else:
            p.error(f"Error: {stderr}")
    except Exception as e:
        p.error(f"An unexpected error occurred: {e}")

def paramiko_transfer(destination, files_to_transfer):
    source_files = " ".join(files_to_transfer)
    destination_path = f"/home/rentdrive/data/"
    username = "rentdrive"
    password = "Commvault!12"
    hostname = destination

    try:

        ssh_client = paramiko.SSHClient()
        ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        ssh_client.connect(hostname=hostname, username=username, password=password)

        sftp_client = ssh_client.open_sftp()

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


def paramiko_transfer(destination, files_to_transfer):
    source_files = " ".join(files_to_transfer)
    destination_path = f"/home/rentdrive/data/"
    username = "rentdrive"
    password = "Commvault!12"
    hostname = destination

    try:

        ssh_client = paramiko.SSHClient()
        ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        ssh_client.connect(hostname=hostname, username=username, password=password)

        sftp_client = ssh_client.open_sftp()

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

