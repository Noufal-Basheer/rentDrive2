import subprocess
import sys
import os
import subprocess,sys


def run_command(command):
    try:
        subprocess.run(command, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error executing command: {e}")
        sys.exit(1)

def main():
    # link_path = '/usr/local/bin/rentdrive-cli'
    # if not os.path.exists(link_path):
    #     print("Please run setup.sh first")
    #     sys.exit(1)
    # project_directory = os.path.dirname(os.path.realpath(link_path))
    # os.chdir(project_directory)
    # os.environ["PIPENV_VENV_IN_PROJECT"] = "1" 
    
    try:
        subprocess.run(['python3','-m','pipenv', 'install'], check=True) 
    except subprocess.CalledProcessError as e:
        print(f"Error installing dependencies: {e}")
        sys.exit(1)

    command = sys.argv[1:]
    if not command:
        command=['python3', 'execute.py','-h'] 
    else:
        command = ['python3', 'execute.py'] + sys.argv[1:]

    run_command(command)

if __name__ == "__main__":
    main()
