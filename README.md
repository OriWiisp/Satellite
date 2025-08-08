# Satellite

Temporary WireGuard VPN connectivity tools.

## CLI usage

```bash
python SatelliteRemoteConnectPreview.py --endpoint <host:port> --peer-public-key <base64_key> --address <ip/cidr> [--psk <base64_psk>]
```

## GUI prototype

```bash
python SatelliteRemoteConnectPreviewGUI.py
```

The GUI is a minimal Tkinter implementation focused on functionality. Advanced
visuals such as the "Liquid Glass" effect or full Notion‑style design would
require native macOS APIs and additional design work beyond this proof of
concept.
