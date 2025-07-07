"""
Anonmal - Anonymous Isolated Terminal

A secure, isolated terminal environment for privacy-focused computing,
penetration testing, and malware analysis.

Features:
- Complete filesystem and process isolation using Bubblewrap
- Fork bomb and resource exhaustion protection
- VPN chaining support for enhanced anonymity
- Ephemeral sessions with no persistence
- Configurable security settings

Usage:
    sudo python3 -m anonmal.main

Security Notice:
    Always run with sudo for proper isolation and resource limits.
"""

__version__ = "1.0.0"
__author__ = "Anonmal Project"
__description__ = "Anonymous Isolated Terminal Environment"

# Core modules
from . import main
from . import container
from . import terminal
from . import vpn

__all__ = ['main', 'container', 'terminal', 'vpn']