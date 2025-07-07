
import os
import json
import subprocess

SETTINGS_PATH = os.path.join(os.path.dirname(__file__), '../settings/terminal-settings.json')

def load_terminal_settings():
    with open(SETTINGS_PATH, 'r') as f:
        return json.load(f)

def launch_terminal():
    settings = load_terminal_settings()
    shell = settings.get('shell', 'bash')
    shell_options = settings.get('shell_options', [])
    prompt = settings.get('prompt', 'anonmal$ ')
    motd = settings.get('motd', '')
    env = os.environ.copy()
    env['PS1'] = prompt
    if 'history_file' in settings:
        env['HISTFILE'] = settings['history_file']
    if motd:
        print(motd)
    subprocess.run([shell] + shell_options, env=env)
