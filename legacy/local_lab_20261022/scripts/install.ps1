[CmdletBinding()]
param(
    [string]$PythonExe = "",
    [switch]$Offline,
    [string]$Wheelhouse = ""
)

$ErrorActionPreference = "Stop"
$repoRoot = [System.IO.Path]::GetFullPath((Join-Path $PSScriptRoot ".."))
$lockPath = Join-Path $repoRoot "requirements-lock.txt"
$venvDirectory = Join-Path $repoRoot ".venv"
$venvPython = Join-Path $venvDirectory "Scripts\python.exe"

if (-not (Test-Path -LiteralPath $lockPath -PathType Leaf)) {
    throw "Missing dependency lock: $lockPath"
}

# Prefer the Windows launcher to avoid silently selecting another Python minor.
$pythonPrefix = @()
if ($PythonExe) {
    $pythonCommand = (Get-Command $PythonExe -ErrorAction Stop).Source
} else {
    $launcher = Get-Command py -ErrorAction SilentlyContinue
    if ($launcher) {
        $pythonCommand = $launcher.Source
        $pythonPrefix = @("-3.13")
    } else {
        $pythonCommand = (Get-Command python -ErrorAction Stop).Source
    }
}

$versionProbe = 'import sys; print("%d.%d" % sys.version_info[:2]); sys.exit(0 if sys.version_info[:2] == (3, 13) else 2)'
& $pythonCommand @pythonPrefix -c $versionProbe
if ($LASTEXITCODE -ne 0) {
    throw "The reproducible CPU environment requires CPython 3.13. Supply -PythonExe with its executable."
}

if (-not (Test-Path -LiteralPath $venvPython -PathType Leaf)) {
    if (Test-Path -LiteralPath $venvDirectory) {
        throw "Existing .venv has no usable Windows Python; preserve it and choose a separate checkout/environment."
    }
    & $pythonCommand @pythonPrefix -m venv $venvDirectory
    if ($LASTEXITCODE -ne 0) { throw "Virtual environment creation failed." }
}

& $venvPython -c $versionProbe
if ($LASTEXITCODE -ne 0) { throw "Existing .venv is not CPython 3.13; it was not deleted." }

$pipArguments = @("-m", "pip", "install", "--disable-pip-version-check", "--no-input")
if ($Offline) {
    if (-not $Wheelhouse -or -not (Test-Path -LiteralPath $Wheelhouse -PathType Container)) {
        throw "Offline installation requires -Wheelhouse pointing to downloaded wheels for this lock."
    }
    $resolvedWheelhouse = (Resolve-Path -LiteralPath $Wheelhouse).Path
    $pipArguments += @("--no-index", "--find-links", $resolvedWheelhouse)
}
$pipArguments += @("--requirement", $lockPath)
& $venvPython @pipArguments
if ($LASTEXITCODE -ne 0) { throw "Locked dependency installation failed; no scientific phase was started." }

& $venvPython -m pip install --disable-pip-version-check --no-input --no-build-isolation --no-deps --editable $repoRoot
if ($LASTEXITCODE -ne 0) { throw "Editable project installation failed." }
& $venvPython -m pip check
if ($LASTEXITCODE -ne 0) { throw "Installed environment failed pip check." }

# Validate every pinned distribution and retain a new dated provenance record.
# This script performs setup only; tests/training remain explicit commands.
$manifestScript = @'
import datetime
import hashlib
import importlib.metadata
import json
import pathlib
import platform
import re
import sys

root = pathlib.Path(sys.argv[1])
lock = root / "requirements-lock.txt"
pins = {}
for line in lock.read_text(encoding="utf-8").splitlines():
    match = re.fullmatch(r"([A-Za-z0-9_.-]+)==(.+)", line.strip())
    if match:
        pins[match[1]] = match[2]
mismatch = {}
actual = {}
for name, expected in pins.items():
    installed = importlib.metadata.version(name)
    actual[name] = installed
    if installed != expected:
        mismatch[name] = {"expected": expected, "installed": installed}
if mismatch:
    raise SystemExit("Dependency lock mismatch: " + json.dumps(mismatch))
now = datetime.datetime.now(datetime.timezone.utc)
stamp = now.strftime("%Y%m%dT%H%M%S%fZ")
destination = root / "artifacts" / "installation" / (stamp + ".json")
destination.parent.mkdir(parents=True, exist_ok=True)
record = {
    "created_utc": now.isoformat(),
    "status": "DEPENDENCY_VERSIONS_VERIFIED",
    "python": sys.version,
    "executable": sys.executable,
    "platform": platform.platform(),
    "lock_sha256": hashlib.sha256(lock.read_bytes()).hexdigest(),
    "locked_packages": actual,
    "project_version": importlib.metadata.version("larp-research"),
    "pip_version": importlib.metadata.version("pip"),
    "runtime_scope": "CPU; version-pinned dependencies, not wheel-hash or OS locking",
    "scientific_phases_started": False,
}
with destination.open("x", encoding="utf-8") as stream:
    json.dump(record, stream, ensure_ascii=False, indent=2, allow_nan=False)
print("Installation manifest: " + str(destination))
'@
& $venvPython -c $manifestScript $repoRoot
if ($LASTEXITCODE -ne 0) { throw "Version verification or provenance recording failed." }

Write-Host "Installed LARP CPU environment. Run: .\.venv\Scripts\python.exe -m larp --help"
