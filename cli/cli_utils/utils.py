from cli_utils.logger.logger import setup_logger
p =setup_logger()
import os, shutil, hashlib, subprocess
import datetime




def move_data(paths,DATA_PATH):
    (folder_path,folder_name) = get_path_and_name(DATA_PATH)
    if folder_path is None:
        folder_name = datetime.datetime.now().strftime("%x").split("/")
        time  = datetime.datetime.now().strftime("%X").split(":")
        folder_name.append(time[0])
        folder_name="".join(folder_name)
        folder_path = os.path.join(DATA_PATH,folder_name)
        os.makedirs(folder_path)
        
        for dir in os.listdir(DATA_PATH):
            if os.path.isdir(dir):
                folder_name = dir
        p.info(f"reaced here, {folder_name} , {len(os.listdir(DATA_PATH))}")
        
    for path in paths:
        if os.path.exists(path):
            if os.path.isdir(path):
                p.info(f"moving {path} to  {folder_path}")
                shutil.move(path,folder_path)
    return (folder_path,folder_name)


def compute_file_hash(file_path):
    hasher = hashlib.sha256()
    with open(file_path, "rb") as file:
        while True:
            chunk = file.read(4096)
            if not chunk:
                break
            hasher.update(chunk)
    return hasher.hexdigest()


def compute_dir_hash(dir_path):
    p.info(f"computing hash value of {dir_path}")
    hasher = hashlib.sha256()
    for root, dirs, files in os.walk(dir_path):
        for file in files:
            file_path = os.path.join(root, file)
            file_hash = compute_file_hash(file_path)
            hasher.update(file_hash.encode())
    return hasher.hexdigest()
                


def gpg_encrypt_file(file_path,file_name):
    # tar czf - source | gpg --batch --passphrase your_passphrase -c -o mydirectory.tar.gz.gpg
    if not file_path:
        p.info("invalid file path")
        return False
    curr_dir = os.getcwd()
    os.chdir(os.path.dirname(file_path))
    paraphrase = "abcd"
    cmd_tar = ['/usr/bin/tar','czf','-',file_name]
    cmd_gpg = ['/usr/bin/gpg','--batch','--passphrase',paraphrase,'-c', '-o', f'{file_name}.tar.gz.gpg']
    try:
        proc_tar = subprocess.Popen(cmd_tar, stdout=subprocess.PIPE,shell=False)
        proc_gpg = subprocess.Popen(cmd_gpg, stdin=proc_tar.stdout, stdout=subprocess.PIPE,shell=False)
        proc_tar.stdout.close()
        stdout, stderr = proc_gpg.communicate()
        p.info(f"executing tar czf - {file_path} | gpg --batch --passphrase **** -c -o {file_name}.tar.gz.gpg ")
        if proc_gpg.returncode != 0:
            p.error("encryption failed")
    except subprocess.CalledProcessError as e:
        p.info(f"error in encrypting the file ")
    os.chdir(curr_dir)
        
        
def decrypt_file(DATA_PATH):
    curr = os.getcwd()
    os.chdir(DATA_PATH)
    for item in os.listdir(DATA_PATH):
        if ".tar.gz.gpg" in item:
            res = gpg_decrypt_file(item)
            if res :
                os.remove(item)
    os.chdir(curr)
           
           
def gpg_decrypt_file(file_name):
     #gpg --batch --passphrase your_passphrase -d mydirectory.tar.gz.gpg | tar xzf -
    paraphrase = "abcd"
    cmd_gpg = ['/usr/bin/gpg','--batch','--passphrase',paraphrase,'-d', f'{file_name}.tar.gz.gpg']
    cmd_tar = ['/usr/bin/tar','xzf','-']
    try:
        proc_tar = subprocess.Popen(cmd_tar, stdout=subprocess.PIPE,shell=False)
        proc_gpg = subprocess.Popen(cmd_gpg, stdin=proc_tar.stdout, stdout=subprocess.PIPE,shell=False)
        proc_tar.stdout.close()
        stdout, stderr = proc_gpg.communicate()
        p.info(f"gpg --batch --passphrase *** -d  {file_name} | tar xzf - ")
        if proc_gpg.returncode != 0:
            p.error("encryption failed")
            return False
    except subprocess.CalledProcessError as e:
        p.info(f"error in encrypting the file ")
        return False
    return True
    
        

    

def get_path_and_name(data_path):
    if not os.path.exists(data_path) or os.listdir(data_path) is None:
        p.info(f"nothing to commit ... please add files before commiting")
    data_items = os.listdir(data_path)
    for item in data_items:
        if os.path.isdir(os.path.join(data_path,item)):
            p.info(f"testpoint 2 , {item} , {data_path}")
            return (os.path.join(data_path,item),item)
    return None
        
        