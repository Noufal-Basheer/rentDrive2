import subprocess
import sys
import os
import subprocess,sys

def run_command(command):
    try:
        subprocess.run(['python3','-m','pipenv', 'run'] + command, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error executing command: {e}")
        sys.exit(1)

def install_requirements():
    try:
        subprocess.run(['python3', '-m', 'pipenv', 'install', '-r', 'requirements.txt'], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error installing requirements: {e}")
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
    if os.path.exists('requirements.txt'):
        print("Installing dependencies from requirements.txt...")
        install_requirements()

    command = sys.argv[1:]
    if not command:
        command=['python3', 'execute.py'] 
    else:
        command = ['python3', 'execute.py'] + sys.argv[1:]

    run_command(command)

if __name__ == "__main__":
    main()
