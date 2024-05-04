from cli_utils.logger.logger import p

import os, shutil, hashlib, subprocess
import datetime, sys

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
                hash_val = compute_dir_hash(path)
                p.info(f"moving {path} to  {folder_path}")
                copied_folder = path.split("/")[-1]
                if os.path.exists(os.path.join(folder_path,copied_folder)):
                    shutil.rmtree(folder_path)
                shutil.move(path,os.path.join(folder_path,copied_folder))
                p.info("copied folder %s"%copied_folder)
                #to maintain a history.info file having hash and path
                write_to_info_file(folder_path,copied_folder,path,hash_val)
                
    return (folder_path,folder_name)



def write_to_info_file(folder_path,name,path,hash):
    info_file_path = os.path.join(folder_path,"hash.info")
    if not os.path.exists(info_file_path):
        with open(info_file_path,"w"):
            pass

    with open(info_file_path,"a") as file:
        file.write(f"{name},{path},{hash}\n")



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
        
        
def decrypt_file(restore_path,rentdrive_path):
    curr = os.getcwd()
    os.chdir(restore_path)
    for item in os.listdir(restore_path):
        if ".tar.gz.gpg" in item:
            hash= compute_file_hash(os.path.join(restore_path,item))
            if not read_and_verify_hash_from_history(item,rentdrive_path,hash):
                p.info(f"checksum calculation failed for {item}")
            res = gpg_decrypt_file(item)
            p.info(res)
            if res :
                os.remove(item)
    os.chdir(curr)
           
           
def gpg_decrypt_file(file_name):
    p.info(os.getcwd())
    p.info(os.listdir())
     #gpg --batch --passphrase your_passphrase -d mydirectory.tar.gz.gpg | tar xzf -
    paraphrase = "abcd"
    cmd = f'/usr/bin/gpg --batch --passphrase {paraphrase} -d {file_name} | /usr/bin/tar xzf -'
    try:
        proc_tar = subprocess.call(cmd, stdout=subprocess.PIPE,shell=True)
        p.info(f"gpg --batch --passphrase *** -d  {file_name} | tar xzf - ")
        if proc_tar != 0:
            p.error("encryption failed")
            return False
    except subprocess.CalledProcessError as e:
        p.info(f"error in encrypting the file ")
        return False
    return True
    

def get_path_and_name(data_path):
    if not os.path.exists(data_path) or os.listdir(data_path) is None:
        p.info(f"nothing to commit ... please add files before commiting")
        sys.exit(1)
    data_items = os.listdir(data_path)
    if not data_items:
        return (None,None)
    for item in data_items:
        if os.path.isdir(os.path.join(data_path,item)):
            p.info(f"testpoint 2 , {item} , {data_path}")
            return (os.path.join(data_path,item),item)
    return (None,None)
        
        
def restore(restore_path,rentdrive_path):
    if not os.path.exists(restore_path):
        p.info("Restore folder not found")
        return
    items = os.listdir(restore_path)
    wrong_hash_items = []
    p.info(items)
    decrypt_file(restore_path,rentdrive_path)
    for item in os.listdir(restore_path):
        move_restored_folder(os.path.join(restore_path,item))
    non_empty_folders_after_restore = []
    for item in os.listdir(restore_path):
        item_path = os.path.join(restore_path,item)
        if os.path.isdir(item_path):
            if len(os.listdir(item_path))>1:
                non_empty_folders_after_restore.append(item)
            else:
                shutil.rmtree(item_path)
        
    if non_empty_folders_after_restore:
        p.info(f"Few items are remaining in folder(s) {','.join(non_empty_folders_after_restore)} , please manually copy them to desired location")
        
def write_to_history(folder_path, folder_name, hash_val):
    history_file_path = os.path.join(folder_path, "History.info")
    time_stamp_obj = datetime.datetime.now()
    time_stamp = time_stamp_obj.strftime("%x") + " " + time_stamp_obj.strftime("%X")
    
    if not os.path.exists(history_file_path):
        fd = os.open(history_file_path, os.O_CREAT | os.O_WRONLY)
        os.close(fd)
    
    with open(history_file_path, "a") as file:
        file.write(f"{time_stamp},{folder_name},{hash_val}\n")
        

def read_and_verify_hash_from_history(file_name,rentdrive_path,hash):
    history_file_path = os.path.join(rentdrive_path, "History.info")
    with open(history_file_path, "r") as file:
        for line in file:
            parts = line.strip().split(",")
            folder_name = parts[1]
            hash_val = parts[2]
            if folder_name==file_name:
                if not hash_val==hash:
                    return False
            return True     

def move_restored_folder(folder_path):
    hash_info_filepath = os.path.join(folder_path,"hash.info")
    p.info(f"processing {folder_path}")
    p.info(f"reading hash.info")
    with open(hash_info_filepath, "r") as file:
        for line in file:
            parts = line.strip().split(",")
            name = parts[0]
            og_path = parts[1]
            hash_val = parts[2]
            curr_file_path=os.path.join(folder_path,name)
            if not os.path.exists(curr_file_path):
                p.info("skipping {name}")
                continue
            if os.path.isdir(curr_file_path):
                calculated_hash = compute_dir_hash(curr_file_path)
            else:
                calculated_hash = compute_file_hash(curr_file_path)
            p.info(f"calculated checksum for {name} : {calculated_hash} , required hash : {hash_val}")
            if not calculated_hash==hash_val:
                p.info(f"Checksum calculation failed")
                continue
            p.info(f"moving {name} to {og_path}")
            shutil.move(curr_file_path,og_path)
                
                    
    