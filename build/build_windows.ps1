param(
    [switch]$Console
)

$main = "src/satellite_remote/gui.py"
$windowed = if ($Console) { "" } else { "--noconsole" }
$dist = "out/dist"
$work = "out/build"

pyinstaller --onefile $windowed --name SatelliteRemoteConnectPreview --distpath $dist --workpath $work $main
