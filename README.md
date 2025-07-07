# Anonmal - Anonymous Terminal

## How does Anonmal work?
- Disposable environment: Your real filesystem stays safe. All actions are sandboxed.
- Stacked VPNs: Not just one-chain 5, 10, or more for real privacy.
- No history: Close Anonmal and nothing is saved.

## About
Built for pentesters, privacy geeks, and anyone needing a truly anonymous terminal. Great for malware testing too.

## Installation

1. Make sure you have Python and Docker installed.
2. Configure settings and VPNs:
    ```sh
    python3 gui_setup.py
    ```
3. Go to the `scripts/` directory:
    ```sh
    cd scripts/
    ```
4. Make the setup script executable:
    ```sh
    chmod +x setup_container.sh
    ```
5. Run the setup container script to download the container (about 100 MB, one-time):
    ```sh
    ./setup_container.sh
    ```
6. Install Python dependencies:
    ```sh
    pip install -r requirements.txt
    ```
7. Start Anonmal:
    ```sh
    python3 main.py
    ```

## Contributing
Pull requests welcome! Document your changes, show they work, and use your own branch.
