![Anonmal Logo](Anonmal_Logo.png)
# Anonmal - Anonymous Isolated Terminal

A secure and fully isolated from you machine enviroment with built-in support for nested VPNs.
Just like a VM but you start it in one click, and optimized for bad hardware and pentesters!

## Features

- Uses Bubblewrap for filesystem and process isolation
- Strict CPU, memory, and process limits prevent resource exhaustion problems
- Multiple layers of protection against resource attacks
- Support for nested VPN connections for extra anonymity
- All session data is temporeral and will clean up on exit
- Easy-to-use (lie) GUI for customizing security settings - python3 gui_setup.py

## How Anonmal Works
- Your computer's filesystem is isolated from the Anomal enviroment
- Think of anomal as an Virtual Machine but way more light, and easier to use
- Anonmal has also capabiity to utilize OpenVPN and Wireguard as another protection layer
- If the Anonmal envorment fails it will just clean up and exit, you system will be safe.

## Use Cases

- Testing malwares
- Pentesting stuff
- Just trying to be anonymous and safe :p
- You wanna try some risky stuff ;)

## Installation
```bash
# Install required system packages
sudo apt update
sudo apt install -y python3 python3-pip python3-venv
sudo apt install -y debootstrap bubblewrap

# For VPN support (optional)
sudo apt install -y openvpn wireguard-tools
```

### Setup

1. **Clone and setup the project:**
    ```bash
    git clone https://github.com/pythontooth/anomal.git
    cd anonmal
    python3 -m venv venv (optional but for extra safety)
    source venv/bin/activate (optional but for extra safety)
    pip install -r requirements.txt
    ```

2. **Configure settings (optional):**
    ```bash
    python3 -m anonmal.gui_setup
    ```

3. **Make setup script executable:**
    ```bash
    chmod +x scripts/setup_container.sh
    ```

4. **Run Anonmal:**
    ```bash
    sudo python3 -m anonmal.main
    ```

## Configuration

### Container Settings (`settings/container-settings.json`)
- `cpu_limit`: CPU usage limit (0.1-2.0) - 2.0 = 2 cores
- `memory_limit`: RAM limit (e.g., "512m", "1g")
- `pids_limit`: Maximum number of processes (recommended: 32-128)
- `default_packages`: Packages to install in the container, they will be saved in template container

## Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Add tests for new functionality or nah
4. Document your changes
5. Submit a pull request

## Security Disclaimer

While Anonmal provides strong isolation, no security solution is perfect.
- Keep your host system updated
- Use trusted VPN providers (they might spy on you ;0)
- Regularly review and update configurations
- Test in non-production environments first (especially its like v0.1)

## TODO

- Build a separate terminal interface for the isolated environment with configuration menu (probably using GTK 3)
- Add installation options: minimal setup with basic tools like curl, wget, nmap, and a full installation packed with comprehensive toolsets
- Implement emergency features for when the host machine runs into trouble or system failures occur
- Consider integrating a collection of free VPNs that work out of the box without manual setup

## License

This project is provided as-is for educational and security research purposes.
