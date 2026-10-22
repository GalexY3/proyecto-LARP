# Separate CUDA environment; preserve the original CPU environment.
$larpScaleRoot = Split-Path -Parent $PSScriptRoot
$larpScaleOriginalPython = Join-Path $larpScaleRoot '.venv/Scripts/python.exe'
$larpScalePython = Join-Path $larpScaleRoot '.venv-scale/Scripts/python.exe'
if (-not (Test-Path -LiteralPath $larpScaleOriginalPython)) { throw 'Original support environment is required.' }
if (-not (Test-Path -LiteralPath $larpScalePython)) {
    & $larpScaleOriginalPython -m venv (Join-Path $larpScaleRoot '.venv-scale')
    if ($LASTEXITCODE -ne 0) { throw 'CUDA environment creation failed.' }
}
& $larpScalePython -m pip install --disable-pip-version-check 'torch==2.11.0+cu128' --index-url 'https://download.pytorch.org/whl/cu128'
if ($LASTEXITCODE -ne 0) { throw 'CUDA wheel installation failed.' }
$larpScaleSite = Join-Path $larpScaleRoot '.venv-scale/Lib/site-packages'
$larpScaleUtf8 = [System.Text.UTF8Encoding]::new($false)
[System.IO.File]::WriteAllText((Join-Path $larpScaleSite 'reuse_larp_support.pth'), (Join-Path $larpScaleRoot '.venv/Lib/site-packages') + "`n", $larpScaleUtf8)
[System.IO.File]::WriteAllText((Join-Path $larpScaleSite 'larp_scale_source.pth'), (Join-Path $larpScaleRoot 'src') + "`n", $larpScaleUtf8)
& $larpScalePython -B -c 'import torch,larp; assert torch.cuda.is_available(); print(torch.__version__, torch.cuda.get_device_name())'
if ($LASTEXITCODE -ne 0) { throw 'CUDA runtime verification failed.' }
