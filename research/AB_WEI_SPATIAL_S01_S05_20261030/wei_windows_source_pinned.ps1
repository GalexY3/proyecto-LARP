<#
LARP/MHU. Wei original source build diagnostic for local Windows PowerShell.
Status: PREPARED_NOT_EXECUTED. No remote CI; no measured AB-R cycle.
Default Inspect reads original log only; Build requires explicit -Mode Build.
Reproduces unmodified upstream MIT-licensed Wei source pinned to SHA.
#>
[CmdletBinding()]
param(
    [ValidateSet('Inspect','Build')]
    [string]$Mode = 'Inspect',
    [string]$OriginalLog = "$env:LOCALAPPDATA\LARP-N400-RECOVERY\20261030-053103\wei-build.log",
    [string]$Workspace = "$env:LOCALAPPDATA\LARP-WEI-ORIGINAL-20261030"
)
$ErrorActionPreference = 'Stop'
$PinnedSha = '0d1be2030518517199dff5c7e7514ee072037d59'
$Repo = 'https://github.com/1iyiwei/noise.git'
New-Item -ItemType Directory -Force -Path $Workspace | Out-Null

if ($Mode -eq 'Inspect') {
    if (Test-Path -LiteralPath $OriginalLog) {
        Write-Host "Existing Windows Wei build log:" $OriginalLog
        Get-FileHash -Algorithm SHA256 -LiteralPath $OriginalLog | Format-List
        Get-Content -LiteralPath $OriginalLog -Tail 160
    } else {
        Write-Warning "Original Wei build log not found: $OriginalLog"
    }
    return
}
function Invoke-Logged {
    param([string]$Exe, [string[]]$Args, [string]$Tag)
    $out = Join-Path $Workspace ($Tag + '.stdout.log')
    $err = Join-Path $Workspace ($Tag + '.stderr.log')
    $escaped = $Args | ForEach-Object {
        if ($_ -match '[\s"]') { '"' + ($_.Replace('"','\"')) + '"' } else { $_ }
    }
    $arguments = [string]::Join(' ', [string[]]$escaped)
    $p = Start-Process -FilePath $Exe -ArgumentList $arguments -NoNewWindow -PassThru -Wait -RedirectStandardOutput $out -RedirectStandardError $err
    [pscustomobject]@{ tag=$Tag; exit_code=$p.ExitCode; arguments=$Args; stdout=$out; stderr=$err } | ConvertTo-Json -Depth 5 | Set-Content -LiteralPath (Join-Path $Workspace ($Tag+'.receipt.json')) -Encoding UTF8
    if ($p.ExitCode -ne 0) {
        Get-Content -LiteralPath $err -Tail 80
        throw "$Tag failed with exit $($p.ExitCode); logs retained in $Workspace"
    }
}
$git = (Get-Command git -ErrorAction Stop).Source
$cmake = (Get-Command cmake -ErrorAction Stop).Source
$src = Join-Path $Workspace 'upstream-noise'
if (-not (Test-Path -LiteralPath $src)) {
    Invoke-Logged $git @('clone','--no-checkout',$Repo,$src) 'git_clone'
}
Invoke-Logged $git @('-C',$src,'checkout','--detach',$PinnedSha) 'git_checkout'
$head = (& $git -C $src rev-parse HEAD).Trim()
if ($LASTEXITCODE -ne 0 -or $head -ne $PinnedSha) { throw "Source SHA mismatch: $head" }
$treeStatus = & $git -C $src status --porcelain
if ($LASTEXITCODE -ne 0 -or (($treeStatus -join '').Trim() -ne '')) { throw 'Dirty upstream source. Refuse to modify or build it.' }
$sourceRoot = Join-Path $src 'RainbowNoise'
$build = Join-Path $Workspace 'build'
# Policy flag changes build configuration only, not Wei source.
Invoke-Logged $cmake @('-S',$sourceRoot,'-B',$build,'-DCMAKE_POLICY_VERSION_MINIMUM=3.5') 'configure'
Invoke-Logged $cmake @('--build',$build,'--target','DartThrowing','--config','Release','--parallel','2') 'compile_dartthrowing'
$bins = @(Get-ChildItem -Path $build -Recurse -Filter 'DartThrowing.exe' -File)
if ($bins.Count -ne 1) { throw "Expected one DartThrowing.exe; found $($bins.Count)" }
$bin = $bins[0]
$receipt=[ordered]@{
    status='BUILT_ORIGINAL_UPSTREAM_SHA__NOT_QUOTA_PARITY'
    original_upstream_sha=$head
    cmake_version=((& $cmake --version | Select-Object -First 1) -join '')
    exe=$bin.FullName
    exe_sha256=(Get-FileHash -Algorithm SHA256 -LiteralPath $bin.FullName).Hash
    original_log=$OriginalLog
    workspace=$Workspace
    note='No 5-class run, no seed control, no 400-point quota parity tested.'
}
$receipt | ConvertTo-Json -Depth 6 | Set-Content -LiteralPath (Join-Path $Workspace 'receipt.json') -Encoding UTF8
$receipt | Format-List
