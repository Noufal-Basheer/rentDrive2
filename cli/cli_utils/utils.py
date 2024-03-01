from cli_utils.logger.logger import setup_logger
p =setup_logger()
import os, shutil
import datetime




def move_data(paths,RENTDRIVE_PATH):
       # tar czf - source | gpg --batch --passphrase your_passphrase -c -o mydirectory.tar.gz.gpg
    # gpg --batch --passphrase your_passphrase -d mydirectory.tar.gz.gpg | tar xzf -
    folder_name = datetime.datetime.now().strftime("%x").split("/")
    time  = datetime.datetime.now().strftime("%X").split(":")
    folder_name.append(time[0])
    folder_name="".join(folder_name)
    folder_path = os.path.join(RENTDRIVE_PATH,folder_name)
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    # for path in paths:
    #     if os.path.exists(path):
    #         if os.path.isdir(path):
    #             shutil.move(path,folder_path)
                