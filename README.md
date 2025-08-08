# Satellite

Temporary WireGuard VPN connectivity tools.

## Project layout

- `src/satellite_remote/cli.py` – command‑line helper for creating a temporary
  WireGuard tunnel
- `src/satellite_remote/gui.py` – Tkinter GUI wrapper around the CLI helpers
- `build/` – scripts for packaging the GUI into standalone binaries

## CLI usage

```bash
python -m satellite_remote.cli --endpoint <host:port> --peer-public-key <base64_key> --address <ip/cidr> [--psk <base64_psk>]
```

## GUI prototype

```bash
python -m satellite_remote.gui
```

## Building standalone binaries

### Windows (.exe)

Requires [PyInstaller](https://pyinstaller.org/). Run from PowerShell:

```powershell
pwsh build/build_windows.ps1
```

The executable will be written to `dist/SatelliteRemoteConnectPreview.exe`.

### macOS (.dmg)

Requires PyInstaller and the `hdiutil` tool (macOS only). Run:

```bash
./build/build_macos.sh
```

This creates `dist/SatelliteRemoteConnectPreview.app` and, if `hdiutil` is
available, a `SatelliteRemoteConnectPreview.dmg` disk image.

The GUI remains a minimal Tkinter implementation focused on functionality.
Advanced visuals such as the "Liquid Glass" effect or a full Notion‑style design
would require native macOS APIs and additional design work beyond this proof of
concept.
