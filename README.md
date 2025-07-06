# Anonmal - Anonymous Terminal

## How does Anonmal work?
- Disposable environment: Your real filesystem stays safe. All actions are sandboxed.
- Stacked VPNs: Not just one—chain 5, 10, or more for real privacy.
- No history: Close Anonmal and nothing is saved.

## About
Built for pentesters, privacy geeks, and anyone needing a truly anonymous terminal. Great for malware testing too.

## Installation

1. Make sure you have Python and Docker installed.
2. Go to the `scripts/` directory:
    ```sh
    cd scripts/
    ```
3. Make the setup script executable:
    ```sh
    chmod +x setup_container.sh
    ```
4. Run the setup container script to download the container (about 100 MB, one-time):
    ```sh
    ./setup_container.sh
    ```
5. Install Python dependencies:
    ```sh
    pip install -r requirements.txt
    ```
6. Configure settings and VPNs:
    ```sh
    python setup.py
    ```
7. Start Anonmal:
    ```sh
    python main.py
    ```

## Contributing
Pull requests welcome! Document your changes, show they work, and use your own branch.
