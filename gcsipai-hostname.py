import subprocess
import sys

def change_hostname(new_hostname):
    try:
        # Command to change the hostname on Windows
        command = f"wmic computersystem where name='%COMPUTERNAME%' call rename name='{new_hostname}'"
        
        # Run the command
        result = subprocess.run(command, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        # Check if the command was successful
        if result.returncode == 0:
            print(f"Hostname successfully changed to '{new_hostname}'.")
            print("Please restart your computer for the changes to take effect.")
        else:
            print("Failed to change the hostname. Error:", result.stderr.decode())
    except subprocess.CalledProcessError as e:
        print(f"An error occurred: {e.stderr.decode()}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python change_hostname.py <new_hostname>")
        sys.exit(1)
    
    new_hostname = sys.argv[1]
    change_hostname(new_hostname)
