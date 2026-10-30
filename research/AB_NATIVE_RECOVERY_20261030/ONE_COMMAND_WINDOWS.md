# Recuperación N400 con un único bloque de PowerShell

LARP - RECUPERACIÓN N400 EN WINDOWS CON UN SOLO PEGADO

Abre PowerShell normal (no hace falta abrirlo como administrador),
copia y pega todo el contenido de COMANDO_POWERSHELL.txt, pulsa Intro.

La instrucción comprueba Git, GitHub CLI, y los instala mediante winget
si faltan. Abre la autenticación de GitHub en navegador si es necesaria.
Descarga el script únicamente desde el repositorio PRIVADO y comprueba
su SHA-256 ANTES de ejecutarlo.

El script crea una carpeta de trabajo aislada bajo %LOCALAPPDATA%,
clona la rama research/ab-r-native-recovery-20261030, prepara Python/NumPy
sin alterar tu entorno global, exige que seis archivos NPZ coincidan con
sus hashes Git y científicos originales, exporta seis JSON exactos y
publica SOLO esos seis JSON y un manifiesto en una rama nueva PRIVADA.
No cambia main, no entrena modelos ni habilita CI.

Si CMake y compilador C++ ya están instalados, intenta compilar el Wei 2010
original. No declara benchmark funcional ni instala herramientas muy pesadas.

No puede eliminar completamente la interacción del inicio de sesión de
GitHub. Si GitHub requiere autorizar acceso al repositorio privado, debes
hacerlo en tu navegador.

Código SHA256 verificado: 6c07c80428fcb738047db15c7b21bba79138b1a63563561d21ceb9878b542ab5
Archivo Git blob: 2bf997d24c3bf454fc0a9bc3dd03ec46b3ca5814
Rama: research/ab-r-native-recovery-20261030

## Comando de inicio (copiar y pegar en PowerShell)

```powershell
& {
  $ErrorActionPreference = 'Stop'
  if (-not (Get-Command git -ErrorAction SilentlyContinue)) {
    if (-not (Get-Command winget -ErrorAction SilentlyContinue)) { throw 'Para instalar Git automaticamente, falta winget.' }
    winget install --id Git.Git --exact --silent --accept-package-agreements --accept-source-agreements
    if ($LASTEXITCODE -ne 0) { throw 'No se pudo instalar Git.' }
    $env:Path += ';' + (Join-Path $env:ProgramFiles 'Git\cmd')
  }
  if (-not (Get-Command gh -ErrorAction SilentlyContinue)) {
    if (-not (Get-Command winget -ErrorAction SilentlyContinue)) { throw 'Para instalar GitHub CLI automaticamente, falta winget.' }
    winget install --id GitHub.cli --exact --silent --accept-package-agreements --accept-source-agreements
    if ($LASTEXITCODE -ne 0) { throw 'No se pudo instalar GitHub CLI.' }
    $env:Path += ';' + (Join-Path $env:ProgramFiles 'GitHub CLI')
  }
  if (-not (Get-Command git -ErrorAction SilentlyContinue)) { throw 'No encuentro Git después de instalarlo; abre de nuevo PowerShell.' }
  if (-not (Get-Command gh -ErrorAction SilentlyContinue)) { throw 'No encuentro GitHub CLI después de instalarlo; abre de nuevo PowerShell.' }
  gh auth status --hostname github.com *> $null
  if ($LASTEXITCODE -ne 0) {
    gh auth login --hostname github.com --git-protocol https --web
    if ($LASTEXITCODE -ne 0) { throw 'No se completó el inicio de sesión en GitHub.' }
  }
  $ruta = Join-Path $env:TEMP 'Run-LARP-N400.ps1'
  $respuesta = gh api 'repos/GalexY3/proyecto-LARP/contents/research/AB_NATIVE_RECOVERY_20261030/Run-LARP-N400.ps1?ref=research/ab-r-native-recovery-20261030'
  if ($LASTEXITCODE -ne 0) { throw 'No tengo acceso al script privado de LARP en GitHub.' }
  $contenido = (($respuesta -join "`n") | ConvertFrom-Json).content
  [IO.File]::WriteAllBytes($ruta, [Convert]::FromBase64String(($contenido -replace '\s', '')))
  if ((Get-FileHash $ruta -Algorithm SHA256).Hash.ToLowerInvariant() -ne '6c07c80428fcb738047db15c7b21bba79138b1a63563561d21ceb9878b542ab5') {
    throw 'El script descargado no coincide con el SHA-256 verificado. No se ejecuta.'
  }
  & powershell.exe -NoProfile -ExecutionPolicy Bypass -File $ruta
}
```

Nota: el SHA256 del bootstrap está fijado, y el script no publica nada si los seis hashes Git/geométricos no pasan. Solo se escribe una rama NUEVA del mismo repositorio PRIVADO. Una sesión de GitHub puede requerir confirmar la autenticación en el navegador. CMake/compilador C++ no se instalan automáticamente por su tamaño; sin ellos la compilación original Wei queda registrada como bloqueada. La validación completa en un ordenador Windows real aún está PENDIENTE.
