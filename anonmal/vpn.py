
import os
import json
import subprocess

SETTINGS_PATH = os.path.join(os.path.dirname(__file__), '../settings/vpn-settings.json')

def load_vpn_settings():
    with open(SETTINGS_PATH, 'r') as f:
        return json.load(f)

def connect_vpn():
    if os.geteuid() != 0:
        print('Error: This action must be run as root. Please run the script with sudo.')
        exit(1)
    settings = load_vpn_settings()
    if not settings.get('enabled', False):
        print('VPN is disabled in settings.')
        return
    vpn_type = settings.get('vpn_type', 'openvpn')
    config_files = settings.get('config_files', [])
    credentials = settings.get('credentials', {})
    auto_connect = settings.get('auto_connect', False)
    nested_vpns = settings.get('nested_vpns', [])
    # Only basic openvpn support for now
    if vpn_type == 'openvpn' and auto_connect and config_files:
        for conf in config_files:
            print(f'Connecting to OpenVPN: {conf}')
            cmd = ['openvpn', '--config', conf]
            if credentials:
                import tempfile
                with tempfile.NamedTemporaryFile('w', delete=False) as credfile:
                    credfile.write(f"{credentials.get('username','')}\n{credentials.get('password','')}\n")
                    credfile.flush()
                    cmd += ['--auth-user-pass', credfile.name]
                subprocess.Popen(cmd)
            else:
                subprocess.Popen(cmd)
    # Nested VPNs (basic)
    for nested in nested_vpns:
        ntype = nested.get('vpn_type')
        nconf = nested.get('config_file')
        if ntype == 'openvpn' and nconf:
            print(f'Connecting nested OpenVPN: {nconf}')
            subprocess.Popen(['openvpn', '--config', nconf])
        elif ntype == 'wireguard' and nconf:
            print(f'Connecting nested WireGuard: {nconf}')
            subprocess.Popen(['wg-quick', 'up', nconf])
