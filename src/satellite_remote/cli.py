#!/usr/bin/env python3
"""
Satellite Remote Connect Preview

Establishes a temporary WireGuard VPN tunnel with ephemeral keys for secure remote
access to remote machines. Keys and configuration files are generated at runtime and
removed on exit to provide an additional layer of security.
"""

import argparse
import atexit
import os
import subprocess
import tempfile
import time
from pathlib import Path

def generate_key() -> bytes:
    """Generate a new WireGuard private key."""
    return subprocess.check_output(["wg", "genkey"]).strip()

def write_config(private_key: str, peer_public_key: str, endpoint: str, address: str, psk: str | None) -> str:
    """Write a temporary WireGuard configuration file and return its path."""
    cfg_lines = [
        "[Interface]",
        f"PrivateKey = {private_key}",
        f"Address = {address}",
        "ListenPort = 0",
        "",
        "[Peer]",
        f"PublicKey = {peer_public_key}",
        "AllowedIPs = 0.0.0.0/0, ::/0",
        f"Endpoint = {endpoint}",
        "PersistentKeepalive = 25",
    ]
    if psk:
        cfg_lines.append(f"PresharedKey = {psk}")
    cfg_content = "\n".join(cfg_lines)

    temp = tempfile.NamedTemporaryFile("w", delete=False)
    os.chmod(temp.name, 0o600)
    temp.write(cfg_content)
    temp.close()
    return temp.name

def bring_up(cfg_file: str) -> None:
    """Bring up the WireGuard interface using wg-quick and register clean-up handlers."""
    subprocess.check_call(["wg-quick", "up", cfg_file])
    atexit.register(lambda: subprocess.call(["wg-quick", "down", cfg_file]))
    atexit.register(lambda: os.remove(cfg_file))

def main() -> None:
    parser = argparse.ArgumentParser(description="Establish a temporary WireGuard VPN tunnel.")
    parser.add_argument("--endpoint", required=True, help="Remote peer endpoint in host:port format")
    parser.add_argument("--peer-public-key", required=True, help="Remote peer public key")
    parser.add_argument("--address", required=True, help="Local tunnel address, e.g. 10.0.0.2/32")
    parser.add_argument("--psk", help="Optional base64 preshared key for an extra security layer")
    args = parser.parse_args()

    private_key = generate_key()
    public_key = subprocess.check_output(["wg", "pubkey"], input=private_key).strip()
    cfg_file = write_config(private_key.decode(), args.peer_public_key, args.endpoint, args.address, args.psk)
    print(f"Temporary configuration written to {cfg_file}")
    print(f"Local public key: {public_key.decode()}")
    bring_up(cfg_file)
    print("VPN connection established. Press Ctrl+C to disconnect.")
    try:
        while True:
            time.sleep(60)
    except KeyboardInterrupt:
        print("Disconnecting...")

if __name__ == "__main__":
    main()
