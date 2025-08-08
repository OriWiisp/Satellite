#!/usr/bin/env python3
"""
Satellite Remote Connect Preview GUI

A minimal cross-platform graphical interface that wraps the
``SatelliteRemoteConnectPreview`` module to establish a temporary WireGuard
VPN tunnel with ephemeral keys.  The interface allows the user to specify
connection parameters and connect/disconnect at the press of a button.

Note: a true "Liquid Glass" aesthetic or Notion-level interface would require
platform‑specific native APIs and significant design work that are outside the
scope of this sample.  This script focuses on functionality and a basic GUI
using Tkinter.
"""

import subprocess
import tkinter as tk
from tkinter import messagebox
from typing import Optional

from SatelliteRemoteConnectPreview import generate_key, write_config, bring_up

# Store state so we can tear down the tunnel on demand
tunnel_cfg: Optional[str] = None


def connect(endpoint: str, peer_public_key: str, address: str, psk: Optional[str]) -> None:
    """Set up the WireGuard tunnel using helpers from the CLI module."""
    global tunnel_cfg
    if tunnel_cfg:
        messagebox.showinfo("Already connected", "A VPN session is already active.")
        return
    try:
        private_key = generate_key()
        public_key = subprocess.check_output(["wg", "pubkey"], input=private_key).strip()
        cfg_file = write_config(private_key.decode(), peer_public_key, endpoint, address, psk)
        bring_up(cfg_file)
        tunnel_cfg = cfg_file
        messagebox.showinfo("Connected", f"VPN established. Local public key: {public_key.decode()}")
    except subprocess.CalledProcessError as e:
        messagebox.showerror("Error", f"Failed to establish VPN: {e}")


def disconnect() -> None:
    """Tear down the WireGuard tunnel if it is active."""
    global tunnel_cfg
    if not tunnel_cfg:
        messagebox.showinfo("Not connected", "No active VPN session to disconnect.")
        return
    subprocess.call(["wg-quick", "down", tunnel_cfg])
    subprocess.call(["rm", "-f", tunnel_cfg])
    tunnel_cfg = None
    messagebox.showinfo("Disconnected", "VPN session ended and temporary files removed.")


def build_ui(root: tk.Tk) -> None:
    root.title("Satellite Remote Connect Preview")
    root.geometry("400x300")

    tk.Label(root, text="Endpoint (host:port)").pack(pady=(10, 0))
    endpoint_entry = tk.Entry(root, width=40)
    endpoint_entry.pack()

    tk.Label(root, text="Peer Public Key").pack(pady=(10, 0))
    peer_key_entry = tk.Entry(root, width=40)
    peer_key_entry.pack()

    tk.Label(root, text="Local Address (e.g. 10.0.0.2/32)").pack(pady=(10, 0))
    address_entry = tk.Entry(root, width=40)
    address_entry.pack()

    tk.Label(root, text="Optional Pre-shared Key").pack(pady=(10, 0))
    psk_entry = tk.Entry(root, width=40)
    psk_entry.pack()

    def on_connect():
        connect(
            endpoint_entry.get().strip(),
            peer_key_entry.get().strip(),
            address_entry.get().strip(),
            psk_entry.get().strip() or None,
        )

    def on_disconnect():
        disconnect()

    tk.Button(root, text="Connect", command=on_connect).pack(pady=(20, 5))
    tk.Button(root, text="Disconnect", command=on_disconnect).pack()

    root.protocol("WM_DELETE_WINDOW", lambda: (disconnect(), root.destroy()))


def main() -> None:
    root = tk.Tk()
    build_ui(root)
    root.mainloop()


if __name__ == "__main__":
    main()
