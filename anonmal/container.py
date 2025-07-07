import subprocess
import os

SCRIPT_PATH = os.path.join(os.path.dirname(__file__), '../scripts/setup_container.sh')

def launch_container():
    if os.geteuid() != 0:
        print('Please run the script with sudo.')
        exit(1)
    cmd = ['bash', SCRIPT_PATH]
    subprocess.run(cmd)