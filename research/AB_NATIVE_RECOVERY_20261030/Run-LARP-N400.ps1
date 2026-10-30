#requires -Version 5.1
<#
LARP N400 -- autonomous but bounded Windows recovery.
This script is part of the private repo GalexY3/proyecto-LARP.
It verifies all SIX pinned Git blobs and internal geometry SHA-256 values before
exporting float64-exact JSON. It pushes ONLY six exports + one audit manifest to
one NEW branch of the SAME PRIVATE GitHub repository. Does not run training or
expensive CI, change main, or publish files to another service.
It optionally attempts an ORIGINAL Wei 2010 build if CMake and a C++ compiler
are already installed; a Wei failure does not weaken N400 verification.
#>
param(
    [switch]$SkipWei,
    [switch]$NoPush
)
Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'
$ProgressPreference = 'SilentlyContinue'
$RepoName = 'GalexY3/proyecto-LARP'
$SourceBranch = 'research/ab-r-native-recovery-20261030'
$SourceScript = 'research/AB_NATIVE_RECOVERY_20261030/verify_and_export.py'
$WeiCommit = '0d1be2030518517199dff5c7e7514ee072037d59'
$OutputSubpath = 'research/AB_NATIVE_RECOVERY_20261030/private_exports'

function Require-Command([string]$Name) {
    $cmd = Get-Command $Name -ErrorAction SilentlyContinue
    if (-not $cmd) { throw "Falta '$Name'. Instala la herramienta o usa el comando de arranque facilitado." }
    return $cmd.Source
}
function Run-Checked([string]$Label, [scriptblock]$Action) {
    Write-Host "`n[ LARP ] $Label" -ForegroundColor Cyan
    & $Action
    if ($LASTEXITCODE -ne 0) {
        throw "$Label ha fallado (codigo $LASTEXITCODE). No se continuara ni se publicaran resultados incompletos."
    }
}
function Sha256-File([string]$Path) {
    return (Get-FileHash -Path $Path -Algorithm SHA256).Hash.ToLowerInvariant()
}

$Gh = Require-Command 'gh'
$Git = Require-Command 'git'
& $Gh auth status --hostname github.com *> $null
if ($LASTEXITCODE -ne 0) {
    Write-Host 'Conecta tu GitHub en el navegador para acceder al repositorio privado.' -ForegroundColor Yellow
    Run-Checked 'Autenticacion GitHub' { & $Gh auth login --hostname github.com --git-protocol https --web }
}
Run-Checked 'Configurar acceso Git HTTPS' { & $Gh auth setup-git }
Run-Checked 'Comprobar acceso al repo privado' { & $Gh repo view $RepoName --json nameWithOwner --jq '.nameWithOwner' }

$Stamp = Get-Date -Format 'yyyyMMdd-HHmmss'
$Base = Join-Path $env:LOCALAPPDATA 'LARP-N400-RECOVERY'
$RunRoot = Join-Path $Base $Stamp
$Clone = Join-Path $RunRoot 'proyecto-LARP'
New-Item -ItemType Directory -Path $RunRoot -Force | Out-Null
$Log = Join-Path $RunRoot 'sesion.txt'
Start-Transcript -Path $Log | Out-Null
try {
    Write-Host "Carpeta de trabajo: $RunRoot"
    Run-Checked 'Clonar rama privada sin alterar tu repositorio habitual' {
        & $Gh repo clone $RepoName $Clone -- --branch $SourceBranch --single-branch
    }
    Push-Location $Clone
    try {
        $BaseCommit = (& $Git rev-parse HEAD).Trim()
        if ($LASTEXITCODE -ne 0) { throw 'No puedo leer el commit base.' }
        Write-Host "Commit de origen: $BaseCommit"
        $Python = $null
        $PyArgs = @()
        $pyCommand = Get-Command py -ErrorAction SilentlyContinue
        if ($pyCommand) {
            & $pyCommand.Source -3 -c 'import sys; assert sys.version_info >= (3,10)'
            if ($LASTEXITCODE -eq 0) { $Python = $pyCommand.Source; $PyArgs = @('-3') }
        }
        if (-not $Python) {
            $pythonCommand = Get-Command python -ErrorAction SilentlyContinue
            if ($pythonCommand) {
                & $pythonCommand.Source -c 'import sys; assert sys.version_info >= (3,10)'
                if ($LASTEXITCODE -eq 0) { $Python = $pythonCommand.Source }
            }
        }
        if (-not $Python) {
            Write-Host 'Falta Python >=3.10. Instalo Python 3.12 mediante winget.' -ForegroundColor Yellow
            $Winget = Require-Command 'winget'
            Run-Checked 'Instalar Python 3.12' {
                & $Winget install --id Python.Python.3.12 --exact --silent --accept-package-agreements --accept-source-agreements
            }
            $Candidates = @(
                (Join-Path $env:LOCALAPPDATA 'Programs\Python\Python312\python.exe'),
                (Join-Path $env:ProgramFiles 'Python312\python.exe')
            )
            foreach ($Candidate in $Candidates) {
                if (Test-Path $Candidate) { $Python = $Candidate; $PyArgs = @(); break }
            }
            if (-not $Python) { throw 'Python se instalo pero no se encontro la ruta. Ejecuta de nuevo al abrir otra terminal.' }
        }
        $Venv = Join-Path $RunRoot '.venv'
        Run-Checked 'Crear entorno Python aislado' { & $Python @PyArgs -m venv $Venv }
        $VenvPython = Join-Path $Venv 'Scripts\python.exe'
        if (-not (Test-Path $VenvPython)) { throw 'No se encontro python.exe del entorno aislado.' }
        Run-Checked 'Instalar NumPy solo en el entorno aislado' { & $VenvPython -m pip install --disable-pip-version-check numpy }

        $SourceFull = Join-Path $Clone $SourceScript
        if (-not (Test-Path $SourceFull)) { throw "No existe el verificador: $SourceFull" }
        Run-Checked 'Autocomprobacion (datos sinteticos, NO nativos)' {
            & $VenvPython $SourceFull --self-test
        }
        Run-Checked 'VERIFICACION REAL de seis NPZ y hashes originales' {
            & $VenvPython $SourceFull --root $Clone
        }
        Run-Checked 'Exportacion bit-exacta de los SEIS originales' {
            & $VenvPython $SourceFull --root $Clone --write
        }

        $Exports = Join-Path $Clone $OutputSubpath
        $Json = @(Get-ChildItem -Path $Exports -Filter 'avian_*_N400_g*.json' -File)
        if ($Json.Count -ne 6) { throw "El exportador no creo seis JSON: $($Json.Count)" }
        # Audit is prepared AFTER verifying all six original blobs. No source ZIP is altered.
        $Manifest = [ordered]@{
            schema = 'larp-native-n400-private-transfer-v1'
            timestamp_utc = (Get-Date).ToUniversalTime().ToString('o')
            source_repo = $RepoName
            source_branch = $SourceBranch
            source_commit = $BaseCommit
            source_verifier = $SourceScript
            source_verifier_sha256 = (Sha256-File $SourceFull)
            python_version = (& $VenvPython --version 2>&1 | Out-String).Trim()
            numpy_version = (& $VenvPython -c 'import numpy; print(numpy.__version__)' | Out-String).Trim()
            classification = 'ORIGINAL_BINARIES_VERIFIED; TRAINING_NOT_RUN; WEI_NOT_YET_EVALUATED'
            files = @($Json | Sort-Object Name | ForEach-Object {
                [ordered]@{name=$_.Name; sha256=(Sha256-File $_.FullName); bytes=$_.Length}
            })
        }
        $ManifestPath = Join-Path $Exports 'TRANSFER_MANIFEST.json'
        [IO.File]::WriteAllText($ManifestPath, (($Manifest | ConvertTo-Json -Depth 10) + "`n"), (New-Object System.Text.UTF8Encoding($false)))

        $WeiStatus = 'SKIPPED_BY_REQUEST'
        if (-not $SkipWei) {
            $WeiStatus = 'BLOCKED_MISSING_CMAKE_OR_COMPILER'
            $CMake = Get-Command cmake -ErrorAction SilentlyContinue
            # Do not install GB of Visual Studio tools without the user's explicit choice.
            $Cpp = Get-Command cl -ErrorAction SilentlyContinue
            if (-not $Cpp) { $Cpp = Get-Command g++ -ErrorAction SilentlyContinue }
            if ($CMake -and $Cpp) {
                $WeiDir = Join-Path $RunRoot 'wei-original-2010'
                try {
                    Run-Checked 'Clonar CODIGO original Wei (no sustitutos)' {
                        & $Git clone https://github.com/1iyiwei/noise.git $WeiDir
                    }
                    Run-Checked 'Fijar commit historico Wei 2010' {
                        & $Git -C $WeiDir checkout --detach $WeiCommit
                    }
                    $WeiBuildDir = Join-Path $WeiDir 'build'
                    $WeiSourceDir = Join-Path $WeiDir 'RainbowNoise'
                    $BuildLog = Join-Path $RunRoot 'wei-build.log'
                    $BuildOutput = @(& $CMake.Source -S $WeiSourceDir -B $WeiBuildDir -DCMAKE_POLICY_VERSION_MINIMUM=3.5 2>&1)
                    $BuildOutput | Out-File -FilePath $BuildLog -Encoding utf8
                    if ($LASTEXITCODE -eq 0) {
                        $BuildOutput = @(& $CMake.Source --build $WeiBuildDir --config Release --target DartThrowing 2>&1)
                        $BuildOutput | Out-File -FilePath $BuildLog -Append -Encoding utf8
                    }
                    if ($LASTEXITCODE -eq 0) {
                        $WeiStatus = 'BUILT_NOT_BENCHMARKED'
                    } else {
                        $WeiStatus = 'BUILD_FAILED_LOG_SAVED'
                    }
                } catch {
                    $WeiStatus = 'BUILD_FAILED_LOG_SAVED'
                    $_ | Out-File -FilePath (Join-Path $RunRoot 'wei-error.txt') -Encoding utf8
                    Write-Warning "Wei no se pudo compilar: $($_.Exception.Message). La exportacion N400 permanece valida."
                }
            }
        }
        $Manifest['wei'] = $WeiStatus
        [IO.File]::WriteAllText($ManifestPath, (($Manifest | ConvertTo-Json -Depth 10) + "`n"), (New-Object System.Text.UTF8Encoding($false)))
        Write-Host "Resultado Wei: $WeiStatus"

        if ($NoPush) {
            Write-Host 'Modo --NoPush: archivos validados localmente, SIN publicacion.' -ForegroundColor Yellow
        } else {
            $TransferBranch = 'research/ab-r-native-export-' + $Stamp
            # Must create a NEW branch to preserve original sources and make the exports visible to ChatGPT.
            Run-Checked 'Crear rama privada de exportacion, sin tocar main' {
                & $Git switch -c $TransferBranch
            }
            $RelativeExports = ($OutputSubpath -replace '\\', '/')
            Run-Checked 'Agregar SOLO seis JSON y manifiesto a la rama nueva' {
                & $Git add -f -- "$RelativeExports"
            }
            $Added = @(& $Git diff --cached --name-only)
            if ($LASTEXITCODE -ne 0) { throw 'Error al revisar el staging.' }
            $ExpectedPaths = @($Json | ForEach-Object { "$RelativeExports/$($_.Name)" }) + "$RelativeExports/TRANSFER_MANIFEST.json"
            $Unexpected = @($Added | Where-Object { $_ -notin $ExpectedPaths })
            if ($Added.Count -ne 7 -or $Unexpected.Count -gt 0) {
                throw "Staging inesperado: $($Added -join ', '), extra: $($Unexpected -join ', ')"
            }
            $Login = (& $Gh api user --jq '.login').Trim()
            if ($LASTEXITCODE -ne 0 -or -not $Login) { throw 'No se pudo obtener usuario GitHub.' }
            Run-Checked 'Commit local, SIN cambiar identidad global Git' {
                & $Git -c "user.name=$Login" -c "user.email=larp-recovery@users.noreply.github.com" commit -m 'research(native): upload six exact original N400 exports and verification manifest'
            }
            Run-Checked 'Publicar SOLAMENTE la nueva rama privada' {
                & $Git push --set-upstream origin $TransferBranch
            }
            $Link = "https://github.com/$RepoName/tree/$TransferBranch/$RelativeExports"
            Write-Host "`nEXPORTACION COMPLETA EN GITHUB PRIVADO:" -ForegroundColor Green
            Write-Host $Link -ForegroundColor Green
            $Link | Set-Content -Path (Join-Path $RunRoot 'ENLACE_GITHUB.txt') -Encoding UTF8
        }
        Write-Host "`nCarpeta de recibos: $RunRoot" -ForegroundColor Green
        Write-Host "Verificacion y exportacion: 6/6 originales, sin entrenar modelos. Saldo AB-R preservado."
    } finally {
        Pop-Location
    }
} catch {
    Write-Host "`nLARP DETENIDO SIN FALSIFICAR EVIDENCIA: $($_.Exception.Message)" -ForegroundColor Red
    Write-Host "Conserva los logs en $RunRoot" -ForegroundColor Yellow
    throw
} finally {
    Stop-Transcript | Out-Null
}
