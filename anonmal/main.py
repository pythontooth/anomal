
import os
import subprocess
import sys
from .container import launch_container
from .terminal import launch_terminal
from .vpn import connect_vpn

def ensure_venv():
    venv_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'venv')
    if not os.path.exists(venv_dir):
        print('[anonmal] Creating Python virtual environment...')
        subprocess.run([sys.executable, '-m', 'venv', venv_dir], check=True)
    activate = os.path.join(venv_dir, 'bin', 'activate_this.py')
    if os.path.exists(activate):
        with open(activate) as f:
            exec(f.read(), {'__file__': activate})

def launch_isolated_terminal():
    print('[anonmal] Isolated terminal environment is now active.')
    print('[anonmal] Fork bomb protection and resource limits are enabled.')
    print('[anonmal] Type "exit" to safely leave, or just hit Ctrl+C')
    print('[anonmal] Remember: if the system failed, it wasn\'t yours :) stay safe.')

def main():
    print('🛡️  Launching Anonmal v0.1 - Secure Isolated Terminal')
    print('=' * 50)
    
    if os.geteuid() != 0:
        print('❌ [anonmal] Please run this script with sudo!!')
        print('   Example: sudo python3 -m anonmal.main')
        sys.exit(1)

    try:
        ensure_venv()
        print('✅ [anonmal] Virtual environment ready')
    except Exception as e:
        print(f'⚠️  [anonmal] Virtual environment setup failed: {e}')
        print('   Continuing without venv...')

    try:
        print('🔒 [anonmal] Setting up VPN connections...')
        connect_vpn()
        print('✅ [anonmal] VPN setup completed')
    except Exception as e:
        print(f'⚠️  [anonmal] VPN setup failed: {e}')
        print('   Continuing without VPN. Your network may not be anonymous!')

    try:
        print('🐧 [anonmal] Creating isolated environment...')
        print('   This may take a few minutes on first run...')
        launch_isolated_terminal()
        launch_container()
    except KeyboardInterrupt:
        print('\n🛑 [anonmal] System was terminated, not yours fortunetly. Cleaning up...')
        sys.exit(0)
    except Exception as e:
        print(f'❌ [anonmal] Container setup failed: {e}')
        print('💡 [anonmal] Try running: sudo apt install debootstrap bubblewrap')
        print('the system failed, but not yours :) stay safe.')
        sys.exit(1)

if __name__ == "__main__":
    main()