#!/usr/bin/env bash
set -euo pipefail

main="src/satellite_remote/gui.py"
name="SatelliteRemoteConnectPreview"
dist="out/dist"
work="out/build"

pyinstaller --onefile --windowed --name "$name" --distpath "$dist" --workpath "$work" "$main"
if command -v hdiutil >/dev/null 2>&1; then
  hdiutil create "$name.dmg" -volname "$name" -srcfolder "$dist/$name.app" -ov -format UDZO
else
  echo "hdiutil not found; skipping DMG creation" >&2
fi
