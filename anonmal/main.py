import os
import subprocess
from .container import launch_container
from .terminal import launch_terminal
from .vpn import connect_vpn

def main():
    # Force sudo password prompt at the start if not already root
    if os.geteuid() != 0:
        try:
            subprocess.run(['sudo', '-v'], check=True)
        except Exception:
            print('Error: sudo authentication failed.')
            exit(1)
    print("Anonmal Launcher")
    print("1. Launch Container")
    print("2. Launch Terminal")
    print("3. Connect VPN")
    print("4. All (VPN, Container, Terminal)")
    print("0. Exit")
    choice = input("Select option: ")
    if choice == '1':
        launch_container()
    elif choice == '2':
        launch_terminal()
    elif choice == '3':
        connect_vpn()
    elif choice == '4':
        # Check for root once, and error if not root
        if os.geteuid() != 0:
            print('Error: This action must be run as root. Please run the script with sudo.')
            exit(1)
        connect_vpn()
        launch_container()
        launch_terminal()
    else:
        print("Bye!")

if __name__ == "__main__":
    main()