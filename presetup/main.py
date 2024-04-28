import subprocess
import sys
import os
import subprocess,sys
from utils import process
from logger.logger import p

def run_command(command):
    try:
        subprocess.run(['python3','-m','pipenv', 'run'] + command, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error executing command: {e}")
        sys.exit(1)

def main():
    pipfile_lock_path = os.path.join(os.getcwd(), 'Pipfile.lock')
    if not os.path.exists(pipfile_lock_path):
        print("Pipfile.lock not found. Running pipenv install...")
        try:
            subprocess.run(['python3','-m','pipenv', 'install'], check=True)
        except subprocess.CalledProcessError as e:
            print(f"Error installing dependencies: {e}")
            sys.exit(1)

    command = sys.argv[1:]
    if not command:
        print("No command provided. Using default command 'python3 execute.py'")
        command = ['python3', 'execute.py'] + sys.argv[1:]

    run_command(command)

if __name__ == "__main__":
    main()
