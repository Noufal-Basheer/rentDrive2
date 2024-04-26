import subprocess
import sys
import os

def run_command(command):
    try:
        # Run the command using Pipenv
        subprocess.run(['pipenv', 'run'] + command, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error executing command: {e}")
        sys.exit(1)

def main():
    # Check if Pipfile.lock exists
    pipfile_lock_path = os.path.join(os.getcwd(), 'Pipfile.lock')
    if not os.path.exists(pipfile_lock_path):
        print("Pipfile.lock not found. Running pipenv install...")
        try:
            subprocess.run(['pipenv', 'install'], check=True)
        except subprocess.CalledProcessError as e:
            print(f"Error installing dependencies: {e}")
            sys.exit(1)

    # Get the command line arguments excluding the script name
    command = sys.argv[1:]
    if not command:
        print("No command provided. Using default command 'python3 execute.py'")
        command = ['python3', 'execute.py'] + sys.argv[1:]

    # Run the command with Pipenv
    run_command(command)

if __name__ == "__main__":
    main()
